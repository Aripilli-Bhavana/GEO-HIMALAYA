import ollama
import os

# Ensure the environment variable is set
os.environ["OLLAMA_HOST"] = "http://localhost:11434"

# Define the model name
MODEL_NAME = "deepseek-r1:14b"

def generate_responses(prompt: str, num_responses: int = 2):
    responses = []
    for _ in range(num_responses):
        response = ollama.generate(
            model=MODEL_NAME,
            prompt=prompt,
            options={
                "num_ctx": 8192,
                "temperature": 0.0,  # Higher temperature for varied responses
                "top_p": 0.9,
                "repeat_penalty": 1.2,
                "num_predict": 256,
            }
        )
        responses.append(response["response"])
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
        for i, resp in enumerate(responses, start=1):
            print(f"{i}. {resp}\n")

