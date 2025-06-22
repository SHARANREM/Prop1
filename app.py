from flask import Flask, request, jsonify, send_file, render_template
import os
import tempfile
import subprocess
from PyPDF2 import PdfReader, PdfWriter
from PIL import Image
import platform
app = Flask(__name__, static_folder='static', template_folder='templates')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/merge', methods=['POST'])
def merge_files():
    pdf_files = request.files.getlist('pdfFiles')
    image_files = request.files.getlist('imageFiles')

    writer = PdfWriter()

    # Process PDF files
    for i, file in enumerate(pdf_files):
        reader = PdfReader(file)

        page_range = request.form.get(f'page_range_{i}')
        pages_to_include = parse_page_ranges(page_range, len(reader.pages)) if page_range else range(len(reader.pages))

        for page_num in pages_to_include:
            writer.add_page(reader.pages[page_num])

    # Process image files
    for j, img_file in enumerate(image_files):
        orientation = request.form.get(f'orientation_{j}', 'portrait')

        img = Image.open(img_file)
        img = img.convert("RGB")

        if orientation == 'portrait':
            pdf_page = img.resize((595, 842))
        else:
            pdf_page = img.resize((842, 595))

        temp_img_path = tempfile.mktemp(suffix='.pdf')
        pdf_page.save(temp_img_path, "PDF")

        image_reader = PdfReader(temp_img_path)
        for page in image_reader.pages:
            writer.add_page(page)

        os.remove(temp_img_path)

    temp_dir = tempfile.mkdtemp()
    output_path = os.path.join(temp_dir, 'merged.pdf')

    with open(output_path, 'wb') as out_file:
        writer.write(out_file)

    return send_file(output_path, as_attachment=True)

@app.route('/convert-to-pdf', methods=['POST'])
def convert_office_to_pdf():
    uploaded_file = request.files.get('file')
    if not uploaded_file:
        return jsonify({'error': 'No file uploaded'}), 400

    temp_dir = tempfile.mkdtemp()
    input_path = os.path.join(temp_dir, uploaded_file.filename)
    uploaded_file.save(input_path)

    # LibreOffice conversion
    try:
        if platform.system() == 'Windows':
            libreoffice_cmd = r"C:\Program Files\LibreOffice\program\soffice.exe"
        else:
            libreoffice_cmd = "libreoffice"

        subprocess.run([
            libreoffice_cmd, '--headless', '--convert-to', 'pdf', '--outdir', temp_dir, input_path
        ], check=True)

    except subprocess.CalledProcessError:
        return jsonify({'error': 'Conversion failed'}), 500

    output_filename = os.path.splitext(uploaded_file.filename)[0] + '.pdf'
    output_path = os.path.join(temp_dir, output_filename)

    if not os.path.exists(output_path):
        return jsonify({'error': 'PDF file not created'}), 500

    return send_file(output_path, as_attachment=True)

def parse_page_ranges(page_range_str, total_pages):
    pages = set()
    ranges = page_range_str.split(',')
    for r in ranges:
        if '-' in r:
            start, end = map(int, r.split('-'))
            for p in range(start, end + 1):
                if 1 <= p <= total_pages:
                    pages.add(p - 1)
        else:
            p = int(r)
            if 1 <= p <= total_pages:
                pages.add(p - 1)
    return sorted(pages)

if __name__ == '__main__':
    app.run(debug=True)
