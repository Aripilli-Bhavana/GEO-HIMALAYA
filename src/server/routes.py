from flask import Blueprint, request, jsonify
from llm import generate_response  # Import the function
from helper import prompt_helper

main = Blueprint("main", __name__)

@main.route("/", methods=["POST"])
def process_request():
    data = request.get_json()
    if not data or "message" not in data:
        return jsonify({"error": "Missing 'message' in request"}), 400

    prompt = prompt_helper.prepare_prompt(data["message"])
    response = generate_response(prompt)
    
    return jsonify({"response": response})
