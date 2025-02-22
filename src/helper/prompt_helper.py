

import json
import os

def prepare_prompt(message: str) -> str:
    """
    Reads metadata.json from the metadata directory and prepares a prompt 
    to answer the question based on metadata only.
    """
    metadata_path = os.path.join(os.path.dirname(__file__), "..","..","metadata", "metadata.json")


    # Load metadata
    try:
        with open(metadata_path, "r", encoding="utf-8") as file:
            metadata = json.load(file)
    except FileNotFoundError:
        return f"Error: Metadata file not found. at {metadata_path}"
    except json.JSONDecodeError:
        return "Error: Metadata file is not a valid JSON."

    # Format metadata into a readable context
    metadata_str = json.dumps(metadata, indent=2)
    print(metadata_str)
    # Construct the prompt
    prompt = f"""
    You are a GIS expert with access to the following geospatial datasets. 
    Use only the provided metadata to answer questions related to available layers, their types, and paths.
    Metadata:
    {metadata_str}


    **Query:**
    {message}
    
    """
    return prompt


