from flask import Blueprint, request, jsonify, Response
from llm import generate_responses  # New function for streaming
from helper import response_helper

main = Blueprint("main", __name__)

@main.route("/", methods=["POST"])
def process_request():
    """
    Handles POST requests by streaming the model's response.
    """
    data = request.get_json()
    if not data or "message" not in data:
        return jsonify({"error": "Missing 'message' in request"}), 400
    if not data or "aoi" not in data:
        return jsonify({"error": "Missing 'aoi' in request"}), 400
    
    
    llm_response = generate_responses(data["message"]) 
    response = response_helper.get_result_from_db(llm_response, data["aoi"])
    if response[0] : 
        return response[1]
    else :
        return response[1], 500
    
