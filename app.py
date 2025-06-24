from flask import Flask, request, jsonify, render_template, send_file
import uuid
import os
import subprocess
import platform

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
OUTPUT_FOLDER = 'outputs'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

# Endpoint 1: Generate unique code from text
@app.route('/generate-code', methods=['POST'])
def generate_code():
    data = request.get_json()
    input_text = data.get('text')
    if not input_text:
        return jsonify({'error': 'No text provided'}), 400

    unique_code = uuid.uuid4().hex  # Generate unique code
    return jsonify({'unique_code': unique_code})

# Endpoint 2: Convert DOCX to PDF
@app.route('/convert-docx', methods=['POST'])
def convert_docx():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    if not file.filename.endswith('.docx'):
        return jsonify({'error': 'Only DOCX files are allowed'}), 400

    # Save uploaded file
    input_path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(input_path)

    # Detect platform and set correct LibreOffice path
    if platform.system() == "Windows":
        libreoffice_path = r"C:\Program Files\LibreOffice\program\soffice.exe"
    else:
        libreoffice_path = "libreoffice"

    # Convert using LibreOffice
    try:
        subprocess.run([
            libreoffice_path, '--headless', '--convert-to', 'pdf', '--outdir',
            OUTPUT_FOLDER, input_path
        ], check=True)
    except subprocess.CalledProcessError as e:
        return jsonify({'error': f'LibreOffice conversion failed: {e}'}), 500

    output_pdf = os.path.splitext(file.filename)[0] + '.pdf'
    output_path = os.path.join(OUTPUT_FOLDER, output_pdf)

    return send_file(output_path, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
