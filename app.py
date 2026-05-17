from flask import Flask, request, render_template, jsonify, url_for
from werkzeug.utils import secure_filename
from pathlib import Path
import os
import pandas as pd
from processing import load_data, validate_data, summarize_data

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def index():
    return render_template('index.html', css_url=url_for('static', filename='css/style.css'))

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    filename = secure_filename(file.filename)
    file_path = Path(app.config['UPLOAD_FOLDER']) / filename
    file.save(file_path)

    try:
        df = load_data(file_path)
        df = validate_data(df)
        summary = summarize_data(df)
        return render_template('summary.html', summary=summary, css_url=url_for('static', filename='css/style.css'))
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
