from flask import Flask
from server.routes import main  # Import routes
from builder import metadata_builder
import os

METADATA_FILE = metadata_path = os.path.join(os.path.dirname(__file__), "..","..","metadata", "metadata_db.json")
app = Flask(__name__)
app.register_blueprint(main)

if __name__ == "__main__":
    if not os.path.exists(METADATA_FILE):
        print("Metadata file not found. Generating metadata...")
        metadata_builder.build()
    app.run(host="0.0.0.0", port=5000, debug=True)

