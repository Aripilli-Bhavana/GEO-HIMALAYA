import ollama

# Define the model name (same as what you pulled via Ollama)
MODEL_NAME = "mistral"  # Change to "llama3", "gemma", etc.

# Function to generate a response
def generate_response(prompt: str) -> str:
    response = ollama.generate(
        model=MODEL_NAME,
        prompt=prompt,
        options={
            "num_ctx": 4096,  # Context length
            "temperature": 0.0,  # Deterministic response
            "top_p": 0.7,  # Reduce randomness
            "repeat_penalty": 1.5,  # Prevent repetition
            "num_predict": 256,  # Max tokens to generate
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

