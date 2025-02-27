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

def generate_responses_stream(prompt: str):
    """
    Generates and streams responses chunk by chunk.
    """
    def generate():
        response_text = ""
        for chunk in ollama.chat(
            model=MODEL_NAME,
            messages=[{"role": "system", "content": prompt}],
            options={
                "temperature": 0.0,
                "top_p": 0.9,
                "repeat_penalty": 1.2
            },
            stream=True
        ):
            content = chunk.get("message", {}).get("content", "")
            response_text += content
            yield content  # Stream each chunk as it arrives

        # Extract SQL query from final response
        extracted_query = extract_query_tag(response_text)
        yield f"\n\nExtracted Query: {extracted_query}"

    return Response(generate(), content_type="text/plain")
