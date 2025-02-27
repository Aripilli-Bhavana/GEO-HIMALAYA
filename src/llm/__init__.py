import ollama
import re
from flask import Response

MODEL_NAME = "mistral"

def extract_query_tag(response: str) -> str:
    """
    Extracts the SQL query enclosed within the <Query> tags.
    """
    match = re.search(r"<Query:\s*(.*?)\s*>", response, re.DOTALL)
    return match.group(1) if match else "No <Query> tag found in the response."

def generate_responses(prompt: str, num_responses: int = 2):
    responses = []
    for _ in range(num_responses):
        response = ollama.generate(
            model=MODEL_NAME,
            prompt=prompt,
            options={
                "num_ctx": 4096,
                "temperature": 0.0,  # Higher temperature for varied responses
                "top_p": 0.9,
                "repeat_penalty": 1.2,
                "num_predict": 256,
            }
        )
        responses.append(response["response"])
    return responses

