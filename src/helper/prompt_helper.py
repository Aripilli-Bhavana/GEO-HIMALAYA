

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
    ### SYSTEM MESSAGE :
    You are a GIS expert with access to geospatial database with following tables. 
    **Database details :**
    {metadata_str}
    
    Database deatails has database name , column names with its description.
    Use only the provided database details to answer questions related to available data.
    


    ### **User Query:**
    {message}

    ### **Final Response Rules:**
    - Ensure **all** required steps have been completed before returning the final answer.
    - The final answer should be only SQL Query statement

    ### **Response (ONLY use the metadata, no assumptions, no extra details):**
    """
    return prompt


