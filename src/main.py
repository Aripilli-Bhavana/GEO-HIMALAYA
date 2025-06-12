#main.py
import requests
import os
from configparser import ConfigParser
from matcher.matcher import get_relevant_metadata

# Load LLM server config
config = ConfigParser()
config.read(os.path.join(os.path.dirname(__file__), "..", "conf", "server.conf"))

LLM_HOST = config.get("llm", "host", fallback="localhost")
LLM_PORT = config.get("llm", "port", fallback="11434")
LLM_URL = f"http://{config.get('llm', 'host')}:{config.get('llm', 'port')}/api/chat"

print("GEO-Him")
model_choice = "mistral:latest"
print(f" Using model: {model_choice}")
print(f" LLM Server: {LLM_URL}")

while True:
    user_query = input("\nEnter your question (or 'quit' to exit): ").strip()

    if user_query.lower() in ['quit', 'exit', 'q']:
        print(" Bye!")
        break

    if not user_query:
        print(" Sorry, no data found as per your query.")
        continue

    print("🔍 Searching relevant datasets...")
    context = get_relevant_metadata(user_query)

    if not context:
        print("\n--- Response ---")
        print(" Sorry, no data found as per your query.")
        continue

    system_prompt = (
      "You are a GIS data assistant for Uttarakhand. Follow these STRICT rules:\n"
    "1. Response format MUST be EXACTLY:\n"
    "   LLM Response: The <objects> are: <comma-separated values from type column>.\n"
    " View Operation: SELECT DISTINCT type FROM <correct_table>;\n"
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
    

    final_prompt = f"""{system_prompt}

Context from Uttarakhand Datasets:
{context}

User Question: {user_query}

Answer (based only on the above dataset context):"""

    print("\n--- Prompt sent to LLM ---")
    print(f"Context length: {len(context)} characters")
    print(f"Query: {user_query}")

    try:
        print("\n🤖 Generating response...")
        response = requests.post(
            LLM_URL,
            json={
                "model":"mistral:latest",
                "messages": [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": f"{context}\n\n{user_query}"}
                ],
                "stream": False,
                "options": {
                    "temperature": 0.1,
                    "top_p": 0.9,
                    "max_tokens": 500
                }
            },
            
        )

        if response.status_code == 200:
            result = response.json().get("message", {}).get("content", "No response from LLM.")
        else:
            result = f" Error: HTTP {response.status_code} - {response.text}"

    except requests.exceptions.Timeout:
        result = " Request timed out. Please check if the LLM server is running."
    except requests.exceptions.ConnectionError:
        result = f" Cannot connect to LLM server at {LLM_URL}. Please check if Ollama is running."
    except Exception as e:
        result = f" Error contacting LLM server: {e}"

    print("\n")
    print(result)
    