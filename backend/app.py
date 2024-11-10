from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os
import json

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Ensure the 'data' directory exists for file storage
os.makedirs("data", exist_ok=True)

@app.route('/upload', methods=['POST'])
def upload_file():
    """Handle file upload."""
    if 'file' not in request.files:
        return jsonify({"error": "No file provided"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "Empty filename"}), 400

    file_type = file.filename.split('.')[-1].lower()
    if file_type not in ['geojson', 'csv', 'zip']:
        return jsonify({"error": "Unsupported file type"}), 400

    file_path = os.path.join("data", file.filename)
    file.save(file_path)

    return jsonify({"message": f"{file.filename} uploaded successfully"}), 200

@app.route('/data/<filename>', methods=['GET'])
def get_file(filename):
    """Serve a specific file's data."""
    if not filename.endswith('.geojson'):
        return jsonify({"error": "File type not supported for download"}), 400
    
    file_path = os.path.join("data", filename)
    if os.path.exists(file_path):
        with open(file_path) as f:
            geojson_data = json.load(f)
        return jsonify(geojson_data)
    else:
        return jsonify({"error": "File not found"}), 404

@app.route('/data', methods=['GET'])
def get_data():
    """Serve stored data."""
    data_files = os.listdir("data")
    return jsonify({"files": data_files}), 200

@app.route('/filter', methods=['POST'])
def filter_data():
    """Apply filters to data (mockup)."""
    filters = request.json.get("filters", {})
    # For demonstration, return filters received (implement filter logic as needed)
    return jsonify({"filtered_data": filters}), 200

if __name__ == '__main__':
    app.run(debug=True)
