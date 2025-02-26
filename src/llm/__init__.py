import ollama
import os
import re

# Ensure the environment variable is set
os.environ["OLLAMA_HOST"] = "http://localhost:11434"

# Define the model name
MODEL_NAME = "deepseek-r1:14b"

def extract_query_tag(response: str) -> str:
    """
    Extracts the SQL query enclosed within the <Query> tags from the response.
    If not found, returns an appropriate message.
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
                "num_ctx": 10240,
                "temperature": 0.0,  
                "top_p": 0.9,
                "repeat_penalty": 1.2,
                "num_predict": 256,
            }
        )
        full_response = response["response"]
        query = extract_query_tag(full_response)
        responses.append((full_response, query))
    return responses

if __name__ == "__main__":
    print("Ollama Chatbot (Type 'exit' to quit)")
    while True:
        user_input = input("You: ")
        if user_input.lower() in ["exit", "quit"]:
            print("Exiting chat...")
            break
        
        responses = generate_responses(user_input)
        print("\nBot Responses:")
        for i, (full_resp, query) in enumerate(responses, start=1):
            print(f"{i}. Full Response:\n{full_resp}\n")
            print(f"   Extracted Query: {query}\n")


