import re
import psycopg2
import psycopg2.extras
import json
import os
from shapely.wkb import loads
import geojson
from helper import logger

def read_config(file_path):
    config = {}
    with open(file_path, 'r') as f:
        for line in f:
            line = line.strip()
            if not line or '=' not in line:  # Skip empty or malformed lines
                continue
            key, value = line.split('=', 1)
            config[key.strip()] = value.strip()
    return config

def extract_sql_query(text: str) -> str:
    # Define a basic pattern to identify spatial SQL queries for PostGIS
    sql_keywords = ["SELECT", "ST_", "INSERT", "UPDATE", "DELETE", "CREATE", "DROP", "ALTER"]
    
    # Check if the whole text is a spatial SQL query
    if any(keyword in text.upper() for keyword in sql_keywords):
        return text  # The text is already an SQL query
    
    # Extract query from sql``` ``` block
    match = re.search(r'sql```(.*?)```', text, re.DOTALL)
    if match:
        return match.group(1).strip()
    
    return "FALSE"



def run_query(response_from_llm: str, aoi: str):
    aoi_prefix = f"WITH aoi AS (SELECT ST_GeomFromText('{aoi}', 4326) AS geom)"
    sql_query_from_llm = extract_sql_query(response_from_llm)
    if sql_query_from_llm == "FALSE":
        return False, "Sorry couldn't understand your request"

    sql_query = f"{aoi_prefix} {sql_query_from_llm}"
    conf_path = os.path.join(os.path.dirname(__file__), "..", "..", "conf", "database.conf")
    config = read_config(conf_path)

    connection = None
    try:
        connection = psycopg2.connect(
            host=config['SERVER'],
            port=config['PORT'],
            user=config['USER'],
            password=config['PASSWORD'],
            database=config['DATABASE']
        )
        cursor = connection.cursor(cursor_factory=psycopg2.extras.DictCursor)  # Use DictCursor

        cursor.execute(sql_query)
        features = []
        for row in cursor.fetchall():
            geom_wkb = row['geom']  # Now it's safe to use column names
            geometry = loads((geom_wkb))  # Convert WKB to a Shapely geometry
            feature = geojson.Feature(
                geometry=geojson.loads(geojson.dumps(geometry.__geo_interface__)),  
                properties={}  # Add additional properties if needed
            )
            features.append(feature)

        feature_collection = geojson.FeatureCollection(features)
        return True, feature_collection

    except Exception as e:
        logger.log("ERROR", str(e))
        return False, str(e)

    finally:
        if connection:
            connection.close()