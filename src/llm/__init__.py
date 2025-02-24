import ollama
import os

# Ensure the environment variable is set
os.environ["OLLAMA_HOST"] = "http://localhost:11434"

# Define the model name
MODEL_NAME = "mistral"

def generate_response(prompt: str) -> str:
    response = ollama.generate(
        model=MODEL_NAME,
        prompt=prompt,
        options={
            "num_ctx": 4096,
            "temperature": 0.0,
            "top_p": 0.7,
            "repeat_penalty": 1.5,
            "num_predict": 256,
        }
    )
    return response["response"]

if __name__ == "__main__":
    print("Ollama Chatbot (Type 'exit' to quit)")
    while True:
        user_input = input("You: ")
        if user_input.lower() in ["exit", "quit"]:
            print("Exiting chat...")
            break
        
        response = generate_response(user_input)
        print(f"Bot: {response}")
