import requests
import os
from configparser import ConfigParser
from matcher.matcher import get_relevant_metadata

# Load LLM server config
config = ConfigParser()
config.read(os.path.join(os.path.dirname(__file__), "..", "conf", "server.conf"))

LLM_HOST = config.get("llm", "host", fallback="localhost")
LLM_PORT = config.get("llm", "port", fallback="11434")
LLM_URL = f"http://{LLM_HOST}:{LLM_PORT}/api/chat"

print("GEO-Him")
model_choice = "mistral:latest"
print(f" Using model: {model_choice}")
print(f" LLM Server: {LLM_URL}")

while True:
    user_query = input("\nEnter your question (or 'quit' to exit): ").strip()

    if user_query.lower() in ['quit', 'exit', 'q']:
        print(" Bye!")
        break

    if not user_query:
        print(" Sorry, no data found as per your query.")
        continue

    print("🔍 Searching relevant datasets...")
    context = get_relevant_metadata(user_query)

    if not context:
        print("\n--- Response ---")
        print(" Sorry, no data found as per your query.")
        continue

    system_prompt = f"""
### SYSTEM MESSAGE:
You are a SQL query generation expert with access to a PostGIS-enabled geospatial database. Your task is to generate accurate SQL queries strictly using the metadata provided.

### RULES:
1. Use only table/column names available in metadata.
2. AOI filtering must always be done using:
   JOIN aoi ON ST_Intersects(table.geom, aoi.geom)
3. Output format MUST be:

---
LLM Response: <natural language result summary based on metadata like this - LLM Response: The roads are: Foot path, Village road (Pucca), Cart track, District road, National highway, Village road (Kuchha), City road, State highway.>


View Operation:
<valid SQL query here>
---

4. If query is invalid or no match found:
LLM Response: No data found for this query.
View Operation: SELECT * FROM unknown_table;

5. Never include explanations, assumptions or unused columns.

### Examples:

Query: show me roads
LLM Response: The roads are: Foot path, Village road (Pucca), Cart track, District road, National highway, Village road (Kuchha), City road, State highway.
View Operation:
SELECT DISTINCT type FROM uttarakhand_roads
JOIN aoi ON ST_Intersects(uttarakhand_roads.geom, aoi.geom);

Query: show forests
LLM Response: The forests are: Forest Evergreen/Semi Evergreen - Dense/Close, Forest Evergreen/Semi Evergreen - Open, Forest - Deciduous (Dry/Moist/Thorn) - Dense/Close, Forest - Forest Blank, Forest - Scrub Forest, Forest - Deciduous (Dry/Moist/Thorn) - Open, Forest - Forest Plantation.
View Operation:
SELECT DISTINCT forest_description FROM uttarakhand_forest
JOIN aoi ON ST_Intersects(uttarakhand_forest.geom, aoi.geom);


Question: Show Forest area which passes through city roads  
AOI : aoi  
Query:  
SELECT forest.geom  
FROM uttarakhand_forest AS forest  
JOIN aoi ON ST_Intersects(forest.geom, aoi.geom)  
WHERE EXISTS (  
    SELECT 1 FROM uttarakhand_roads AS roads  
    WHERE ST_Intersects(forest.geom, roads.geom)  
    AND roads.type = 'City road'  
    AND ST_Intersects(roads.geom, aoi.geom)  
);  

Question: Find all soil types that are located within 500 meters of a river.  
AOI : aoi  
Query:  
SELECT soil.geom, soil.type  
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
Query:  
SELECT roads.type, roads.geom, ST_Length(roads.geom::geography) AS length  
FROM uttarakhand_roads AS roads  
JOIN aoi ON ST_Intersects(roads.geom, aoi.geom)  
ORDER BY length DESC  
LIMIT 1;  

Question: Show largest area of land use as forest  
AOI : aoi  
Query:  
SELECT lulc.type, lulc.geom, ST_Area(lulc.geom::geography) AS area  
FROM uttarakhand_lulc AS lulc  
JOIN aoi ON ST_Intersects(lulc.geom, aoi.geom)  
WHERE lulc.type  ~* 'forest.*$'  
ORDER BY area DESC  
LIMIT 1;  

Question: Show the barren lands within 10m of a water body  
AOI : aoi  
Query:  
SELECT barren_lands.type, barren_lands.geom  
FROM uttarakhand_lulc AS barren_lands  
JOIN aoi ON ST_Intersects(barren_lands.geom, aoi.geom)  
WHERE barren_lands.type IN ('Barren Rocky', 'Gullied / Ravinous land', 'Sandy Area')  
AND EXISTS (  
    SELECT 1 FROM uttarakhand_lulc AS water_bodies  
    WHERE water_bodies.type IN ('Water Body', 'Lakes/Ponds', 'Reservoir/tanks', 'Canal', 'Waterlogged / Marshy Land')  
    AND ST_DWithin(barren_lands.geom, water_bodies.geom, 10)  
    AND ST_Intersects(water_bodies.geom, aoi.geom)  
);  

Question: Find built-up area near drainage  
AOI : aoi  
Query:  
SELECT built_ups.type, built_ups.geom  
FROM uttarakhand_lulc AS built_ups  
JOIN aoi ON ST_Intersects(built_ups.geom, aoi.geom)  
WHERE built_ups.type  ~* 'built[_-]*up.*$'  
AND EXISTS (  
    SELECT 1 FROM uttarakhand_drainage AS water_bodies  
    WHERE water_bodies.type IN ('Branch canal', 'River', 'Distributory canal', 'Stream', 'Drain','Main canal')  
    AND ST_DWithin(built_ups.geom, water_bodies.geom, 10)  
    AND ST_Intersects(water_bodies.geom, aoi.geom)  
);  

---

### CONTEXT FROM METADATA:
{context}

### USER QUERY:
{user_query}

--- RESPONSE:
"""

    final_prompt = system_prompt

    print("\n--- Prompt sent to LLM ---")
    print(f"Context length: {len(context)} characters")
    print(f"Query: {user_query}")

    try:
        print("\n🤖 Generating response...")
        response = requests.post(
            LLM_URL,
            json={
                "model": model_choice,
                "messages": [
                    {"role": "system", "content": final_prompt},
                    {"role": "user", "content": ""}
                ],
                "stream": False,
                "options": {
                    "temperature": 0.1,
                    "top_p": 0.9,
                    "max_tokens": 500
                }
            },
        )

        if response.status_code == 200:
            result = response.json().get("message", {}).get("content", "No response from LLM.")
        else:
            result = f" Error: HTTP {response.status_code} - {response.text}"

    except requests.exceptions.Timeout:
        result = " Request timed out. Please check if the LLM server is running."
    except requests.exceptions.ConnectionError:
        result = f" Cannot connect to LLM server at {LLM_URL}. Please check if Ollama is running."
    except Exception as e:
        result = f" Error contacting LLM server: {e}"

    print("\n")
    print(result)
