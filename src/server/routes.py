from flask import Blueprint, request, jsonify, Response
from llm import generate_responses  # New function for streaming
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
    
    return generate_responses(data["message"]) 
