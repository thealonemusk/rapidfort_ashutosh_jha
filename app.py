from flask import Flask, request, jsonify, render_template, send_file
from werkzeug.utils import secure_filename
import os
from docx2pdf import convert
from PyPDF2 import PdfReader, PdfWriter
import pythoncom  # For COM initialization on Windows
import logging

app = Flask(__name__)

# Configure upload folder
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'docx'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Ensure uploads directory exists
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# Logging setup
logging.basicConfig(level=logging.ERROR, format='%(asctime)s - %(message)s')

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part in the request'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400

    if not allowed_file(file.filename):
        return jsonify({'error': 'Only .docx files are allowed'}), 400

    password = request.form.get('password')  # Get password from request form
    if file:
        try:
            filename = secure_filename(file.filename)
            docx_path = os.path.join(app.root_path, app.config['UPLOAD_FOLDER'], filename)
            pdf_filename = filename.rsplit('.', 1)[0] + '.pdf'
            pdf_path = os.path.join(app.root_path, app.config['UPLOAD_FOLDER'], pdf_filename)

            # Save .docx file
            file.save(docx_path)

            # Convert to PDF
            pythoncom.CoInitialize()  # Initialize COM
            convert(docx_path, pdf_path)

            # Add password protection if password is provided
            if password:
                protected_pdf_path = os.path.join(app.root_path, app.config['UPLOAD_FOLDER'], f"protected_{pdf_filename}")
                add_password_protection(pdf_path, protected_pdf_path, password)
                pdf_path = protected_pdf_path  # Use the protected PDF path

            # Get file metadata
            file_metadata = {
                'filename': filename,
                'size': os.path.getsize(docx_path),  # File size in bytes
                'pdf_file': os.path.basename(pdf_path),
                'download_url': f'/download/{os.path.basename(pdf_path)}'
            }
            return jsonify({
                'message': 'File uploaded and converted successfully',
                'metadata': file_metadata
            })
        except Exception as e:
            logging.error(f"Error in file conversion: {e}")
            return jsonify({'error': 'File conversion failed. Please try again.'}), 500
        finally:
            pythoncom.CoUninitialize()  # Clean up COM

@app.route('/download/<filename>')
def download_file(filename):
    try:
        file_path = os.path.join(app.root_path, app.config['UPLOAD_FOLDER'], filename)
        if not os.path.exists(file_path):
            return jsonify({'error': 'File not found'}), 404
        return send_file(file_path, as_attachment=True)
    except Exception as e:
        logging.error(f"Error in file download: {e}")
        return jsonify({'error': 'Failed to download the file. Please try again.'}), 500

def add_password_protection(input_pdf_path, output_pdf_path, password):
    """Add password protection to a PDF."""
    try:
        pdf_reader = PdfReader(input_pdf_path)
        pdf_writer = PdfWriter()

        for page in pdf_reader.pages:
            pdf_writer.add_page(page)

        pdf_writer.encrypt(password)
        with open(output_pdf_path, 'wb') as output_file:
            pdf_writer.write(output_file)
    except Exception as e:
        logging.error(f"Error adding password protection: {e}")
        raise

@app.errorhandler(404)
def not_found_error(error):
    return jsonify({'error': 'Resource not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8080, debug=True)
