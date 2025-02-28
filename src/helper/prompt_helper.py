

import json
import os
from langchain.prompts import PromptTemplate

def get_prompt_template()-> PromptTemplate:
    """
    Reutrns pronpmt template
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
    # Construct the prompt
    prompt_template = PromptTemplate(
    input_variables=["user_query"],
    template="""
        ### SYSTEM MESSAGE:
        You are a SQL query generation expert with access to a PostGIS-enabled geospatial database. Your task is to generate **accurate and optimized SQL queries** based strictly on the following metadata:

        **Database Schema:**
        {metadata}

        

        ### Instructions:
        1. Generate SQL queries that **only** use the provided metadata.
        2. **Table names are case sensitive**
        2. **Restrict** the SQL Query to be performed only within the given Area of Interest.
        3. The Area of Interest geoemtry is provided in WKT format.
        4. **DO NOT** assume any missing table or column.
        5. Ensure the SQL is syntactically correct and optimized for PostGIS.

        ### Examples
            Question: Show Forest Type which passes through city roads
            AOI : aoi
            Query:  SELECT uttarakhand_forest.forest_description, uttarakhand_forest.geom
                        FROM uttarakhand_forest
                        JOIN uttarakhand_roads 
                        ON ST_Intersects(uttarakhand_forest.geom, uttarakhand_roads.geom)
                        WHERE uttarakhand_roads.road_type = 'City road'
                        AND ST_Intersects(uttarakhand_forest.geom, (SELECT geom FROM aoi));




            Question: Find all soil types that are located within 500 meters of a river.
            AOI : aoi
            Query: SELECT uttarakhand_soil.soil_type, uttarakhand_soil.geom
                        FROM uttarakhand_soil
                        JOIN uttarakhand_drainage 
                        ON ST_DWithin(uttarakhand_soil.geom, uttarakhand_drainage.geom, 500)
                        WHERE uttarakhand_drainage.drainage_type = 'River'
                        AND ST_Intersects(uttarakhand_soil.geom, (SELECT geom FROM aoi));
            Question: Show the longest road and its type
            AOI : aoi
            Query: SELECT road_type, shape_leng, geom
                        FROM uttarakhand_roads
                        WHERE ST_Intersects(geom, (SELECT geom FROM aoi))
                        ORDER BY shape_leng DESC
                        LIMIT 1;
        ---

        ### **User Query:**
        {user_query}
        AOI : aoi

        ---

        ### **Expected Response Format:**
        -- SQL Query only

        ---

        ### **Response:**
        """
    )
    return prompt_template

def get_metadata() : 
    """
    Reads metadata.json from the metadata directory and returns the same.
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
    return metadata_str

