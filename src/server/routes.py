from flask import Blueprint, request, jsonify
import requests
from configparser import ConfigParser
from src.matcher.matcher import get_relevant_metadata
import os
from spellchecker import SpellChecker

routes = Blueprint("routes", __name__)

# Initialize spell checker instance
spell = SpellChecker()

def correct_spelling(text):
    words = text.split()
    corrected_words = []
    for word in words:
        corrected = spell.correction(word)
        corrected_words.append(corrected if corrected else word)
    return " ".join(corrected_words)

# Load LLM configuration
def load_config():
    config = ConfigParser()
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(os.path.dirname(current_dir))
    config_path = os.path.join(project_root, "conf", "server.conf")

    config.read(config_path)

    host = config.get("llm", "host", fallback="localhost")
    port = config.get("llm", "port", fallback="11434")
    return f"http://{host}:{port}/api/generate"

LLM_URL = load_config()

@routes.route("/chat", methods=["POST"])
def chat():
    try:
        data = request.get_json()
        if not data or not data.get("query", "").strip():
            return jsonify({"error": "Query is required"}), 400

        query = data["query"].strip()
        query = correct_spelling(query)

        context = get_relevant_metadata(query)

        system_prompt = (
          "You are a GIS data assistant for Uttarakhand. Follow these STRICT rules:\n"
    "1. Response format MUST be EXACTLY:\n"
    "   LLM Response: The <objects> are: <comma-separated values from type column>.\n"
    "   View Operation: SELECT DISTINCT type FROM <correct_table>;\n"
    "\n"
    "2. For 'show me <objects>' queries:\n"
    "   - List ALL distinct values from the 'type' column (or equivalent)\n"
    "   - Use EXACT values as stored in the database\n"
    "   - Maintain original capitalization and formatting\n"
    "\n"
    "3. Never:\n"
    "   - Summarize or categorize data\n"
    "   - Add explanations or interpretations\n"
    "   - Skip any values from the 'type' column\n"
    "\n"
    "4. If no matching data exists, respond EXACTLY:\n"
    "   LLM Response: No data found for this query.\n"
    "   View Operation: SELECT * FROM unknown_table;\n"
    "\n"
    "5. Example responses REQUIRED:\n"
    "   For 'show me roads':\n"
    "   LLM Response: The roads are: Foot path, Village road (Pucca), Cart track, District road, National highway, Village road (Kuchha), City road, State highway.\n"
    "   View Operation: SELECT DISTINCT type FROM uttarakhand_roads;\n"
    "\n"
    "   For 'show me forests':\n"
    "   LLM Response: The forests are: Forest Evergreen/Semi Evergreen - Dense/Close, Forest Evergreen/Semi Evergreen - Open, Forest - Deciduous (Dry/Moist/Thorn) - Dense/Close, Forest - Forest Blank, Forest - Scrub Forest, Forest - Deciduous (Dry/Moist/Thorn) - Open, Forest - Forest Plantation.\n"
    "   View Operation: SELECT DISTINCT forest_description FROM uttarakhand_forest;"
        )

        full_prompt = f"""{system_prompt}

Dataset Context:
{context}

User Query: {query}

You must return both:
1. LLM Response: Answer to the user query.
2. View Operation: A SQL SELECT query matching the query. If no data matches, write: SELECT * FROM unknown_table WHERE condition;

Begin your response:

LLM Response:"""

        payload = {
            "model": "llama3:latest",
            "prompt": full_prompt,
            "stream": False,
            "options": {
                "temperature": 0.1,
                "top_p": 0.9,
                "max_tokens": 500
            }
        }

        response = requests.post(LLM_URL, json=payload, timeout=30)

        if response.status_code == 200:
            llm_output = response.json().get("response", "No response from LLM.")
            has_data = not llm_output.strip().startswith("Sorry, no data found as per your query")
            return jsonify({
                "response": llm_output,
                "has_data": has_data,
                "context_length": len(context)
            })
        else:
            return jsonify({
                "error": f"LLM server error: HTTP {response.status_code}",
                "details": response.text
            }), 500

    except requests.exceptions.Timeout:
        return jsonify({"error": "Request to LLM server timed out"}), 504
    except requests.exceptions.ConnectionError:
        return jsonify({"error": f"Cannot connect to LLM server at {LLM_URL}"}), 503
    except Exception as e:
        return jsonify({"error": f"Internal server error: {str(e)}"}), 500

@routes.route("/health", methods=["GET"])
def health_check():
    try:
        test_payload = {
            "model": "llama3:latest",
            "prompt": "Test",
            "stream": False,
            "options": {"max_tokens": 1}
        }
        response = requests.post(LLM_URL, json=test_payload, timeout=5)
        llm_status = "connected" if response.status_code == 200 else "disconnected"
    except:
        llm_status = "disconnected"

    return jsonify({
        "status": "healthy",
        "llm_server": LLM_URL,
        "llm_status": llm_status
    })

@routes.route("/datasets", methods=["GET"])
def get_datasets():
    from src.matcher.matcher import load_metadata
    metadata = load_metadata()

    datasets = [{
        "name": name,
        "table_name": info.get("table_name"),
        "description": info.get("description"),
        "columns": list(info.get("columns", {}).keys())
    } for name, info in metadata.items()]

    return jsonify({"datasets": datasets})
