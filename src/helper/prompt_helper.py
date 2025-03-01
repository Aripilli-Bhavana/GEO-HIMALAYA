

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
        3. ** Attributes are case sensitive**
        4. **Restrict** the SQL Query to be performed only within the given Area of Interest.
        5. The Area of Interest geoemtry is provided in WKT format.
        6. **DO NOT** assume any missing table or column.
        7. Ensure the SQL is syntactically correct and optimized for PostGIS.

        ### Examples
            Question: Show Forest area which passes through city roads
            AOI : aoi
            Query:  SELECT forest.geom
                        FROM uttarakhand_forest AS forest
                        JOIN aoi ON ST_Intersects(forest.geom, aoi.geom)  
                        WHERE EXISTS (
                            SELECT 1 FROM uttarakhand_roads AS roads
                            WHERE ST_Intersects(forest.geom, roads.geom)  
                            AND roads.road_type = 'City road'  
                            AND ST_Intersects(roads.geom, aoi.geom)  
                        );


            Question: Find all soil types that are located within 500 meters of a river.
            AOI : aoi
            Query: SELECT soil.geom, soil.soil_type
                    FROM uttarakhand_soil AS soil
                    JOIN aoi ON ST_Intersects(soil.geom, aoi.geom)  
                    WHERE EXISTS (
                        SELECT 1 FROM uttarakhand_drainage AS river
                        WHERE ST_DWithin(soil.geom, river.geom, 500)  
                        AND ST_Intersects(river.geom, aoi.geom)  
                    )
                    ORDER BY ST_Distance(soil.geom, (SELECT geom FROM aoi)) ASC;
            Question: Show the longest road and its type
            AOI : aoi
            Query: SELECT roads.road_type, roads.geom, ST_Length(roads.geom::geography) AS length
                    FROM uttarakhand_roads AS roads
                    JOIN aoi ON ST_Intersects(roads.geom, aoi.geom)  
                    ORDER BY length DESC
                    LIMIT 1;
            
            Question : Show largest area of land use as forest
            AOI : aoi
            Query : SELECT lulc.lulc_type, lulc.geom, ST_Area(lulc.geom::geography) AS area
                        FROM uttarakhand_lulc AS lulc
                        JOIN aoi ON ST_Intersects(lulc.geom, aoi.geom) 
                        WHERE lulc.lulc_type IN ('Forest Plantation')  
                        ORDER BY area DESC
                        LIMIT 1;
            Question : Show the  barren lands with 10m vicinity of  water body
            AOI : aoi
            Query : SELECT barren_lands.lulc_type, barren_lands.geom
                        FROM uttarakhand_lulc AS barren_lands
                        JOIN aoi ON ST_Intersects(barren_lands.geom, aoi.geom)  
                        WHERE barren_lands.lulc_type IN ('Barren Rocky', 'Gullied / Ravinous land', 'Sandy Area')  
                        AND EXISTS (
                            SELECT 1 FROM uttarakhand_lulc AS water_bodies
                            WHERE water_bodies.lulc_type IN ('Water Body', 'Lakes/Ponds', 'Reservoir/tanks', 'Canal', 'Waterlogged / Marshy Land') 
                            AND ST_DWithin(barren_lands.geom, water_bodies.geom, 10)  
                            AND ST_Intersects(water_bodies.geom, aoi.geom)  
                        );
             Question : Find built-up area near water body
            AOI : aoi
            Query : SELECT built_ups.lulc_type, built_ups.geom
                        FROM uttarakhand_lulc AS built_ups
                        JOIN aoi ON ST_Intersects(built_ups.geom, aoi.geom)  
                        WHERE built_ups.lulc_type  ~* 'built[\s_-]*up.*$'  
                        AND EXISTS (
                            SELECT 1 FROM uttarakhand_lulc AS water_bodies
                            WHERE water_bodies.lulc_type IN ('Water Body', 'Lakes/Ponds', 'Reservoir/tanks', 'Canal', 'Waterlogged / Marshy Land') 
                            AND ST_DWithin(built_ups.geom, water_bodies.geom, 10)  
                            AND ST_Intersects(water_bodies.geom, aoi.geom)  
                        );

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

