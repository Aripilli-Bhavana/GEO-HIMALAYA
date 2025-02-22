import os
from llama_cpp import Llama

# Define model path
MODEL_PATH = os.path.expanduser("models/mistral-7b-instruct-v0.2.Q5_K_M.gguf")

# Load the model
llm = Llama(
    model_path=MODEL_PATH, 
    n_ctx=4096, 
    temperature=0.0,  # Make it deterministic
    top_p=0.7,  # Reduce randomness
    repeat_penalty=1.5,  # Strong penalty for repetition
    verbose=True
)

# Function to process queries
def generate_response(prompt: str) -> str:
    response = llm(prompt, max_tokens=256)
    return response["choices"][0]["text"]
