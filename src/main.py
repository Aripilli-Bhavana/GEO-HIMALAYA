from flask import Flask
from server.routes import main  # Import routes
from builder import metadata_builder
import os
from flask_cors import CORS

app = Flask(__name__)
app.register_blueprint(main)
CORS(app) 

if __name__ == "__main__":
    metadata_builder.build()
    app.run(host="0.0.0.0", port=5000, debug=True)

