import psycopg2
import json
import os

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

def get_db_metadata(config):
    connection = None
    try:
        connection = psycopg2.connect(
            host=config['SERVER'],
            port=config['PORT'],
            user=config['USER'],
            password=config['PASSWORD'],
            database=config['DATABASE']
        )
        cursor = connection.cursor()
        
        # Fetch table names
        cursor.execute("""
            WITH metadata AS (
            SELECT 
                c.table_name,
                c.table_schema,  -- Include table_schema in GROUP BY
                obj_description((c.table_schema || '.' || c.table_name)::regclass, 'pg_class') AS table_description,
                jsonb_object_agg(
                    c.column_name, 
                    jsonb_build_object(
                        'data_type', c.data_type,
                        'description', col_description((c.table_schema || '.' || c.table_name)::regclass, c.ordinal_position)
                    )
                ) AS columns
            FROM information_schema.columns c
            WHERE c.table_schema = 'public'
	    AND c.table_name IN ('uttarakhand_drainage', 'uttarakhand_forest','uttarakhand_soil','uttarakhand_roads','lulc_uttarakhand_2015')
            GROUP BY c.table_name, c.table_schema
        )
        SELECT jsonb_object_agg(
            table_name, 
            jsonb_build_object(
                'description', table_description,
                'columns', columns
            )
        ) AS metadata_json
        FROM metadata;
                """)
        db_metadata = cursor.fetchall()
        
        return db_metadata
    except Exception as e:
        print(f"Error: {e}")
        return None
    finally:
        if connection:
            connection.close()

def save_to_json(data, file_path):
    with open(file_path, 'w') as f:
        json.dump(data, f, indent=4)

def build():
    conf_path = os.path.join(os.path.dirname(__file__), "..","..","conf", "database.conf")
    config = read_config(conf_path)
   
    metadata_dir = os.path.join(os.path.dirname(__file__), "..", "..", "metadata")
    metadata_path = os.path.join(metadata_dir, "metadata.json")

    # Ensure the metadata directory exists
    if not os.path.exists(metadata_dir):
        print(f"Creating metadata directory at: {metadata_dir}")
        os.makedirs(metadata_dir, exist_ok=True)

    if not os.path.exists(metadata_path):
        print(f"Metadata file not found, generating at: {metadata_path}")
        metadata = get_db_metadata(config)
        if metadata:
            save_to_json(metadata, metadata_path)
            print("Database metadata saved successfully.")
        else:
            print("Failed to retrieve database metadata.")
    else:
        print("Metadata file already exists.")


