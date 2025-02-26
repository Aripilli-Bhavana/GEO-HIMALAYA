from flask import Blueprint, request, jsonify, Response
from llm import generate_responses_stream  # New function for streaming
from helper import prompt_helper

main = Blueprint("main", __name__)

@main.route("/", methods=["POST"])
def process_request():
    """
    Handles POST requests by streaming the model's response.
    """
    data = request.get_json()
    if not data or "message" not in data:
        return jsonify({"error": "Missing 'message' in request"}), 400

    prompt = prompt_helper.prepare_prompt(data["message"])
    
    return generate_responses_stream(prompt)  # Return streamed response
