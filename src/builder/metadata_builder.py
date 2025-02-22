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
        
        # Fetch table metadata
        cursor.execute("""
            SELECT table_name
            FROM information_schema.tables
            WHERE table_schema = 'public';
        """)
        tables = cursor.fetchall()
        
        db_metadata = {}
        
        for (table_name,) in tables:
            cursor.execute(f"""
                SELECT column_name, data_type, is_nullable, column_default
                FROM information_schema.columns
                WHERE table_name = '{table_name}';
            """)
            columns = cursor.fetchall()
            
            db_metadata[table_name] = [
                {
                    "column_name": col[0],
                    "data_type": col[1],
                    "is_nullable": col[2],
                    "default": col[3]
                }
                for col in columns
            ]
        
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
    metadata = get_db_metadata(config)
    metadata_path = os.path.join(os.path.dirname(__file__), "..","..","metadata", "metadata_db.json")
    if metadata:
        save_to_json(metadata, metadata_path)
        print("Database metadata saved to metadata_db.json")
    else:
        print("Failed to retrieve database metadata")
