from flask import Flask, request, jsonify, render_template, send_file
from flask_cors import CORS  
from werkzeug.utils import secure_filename
import os
from docx2pdf import convert
from PyPDF2 import PdfReader, PdfWriter
import pythoncom
import logging
import tempfile
from datetime import datetime

app = Flask(__name__)
CORS(app)  

class Config:
    UPLOAD_FOLDER = os.environ.get('UPLOAD_FOLDER', 'uploads')
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size
    ALLOWED_EXTENSIONS = {'docx'}

app.config.from_object(Config)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('app.log')
    ]
)

# Ensure upload folder exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

def cleanup_old_files():
    """Clean up files older than 1 hour"""
    current_time = datetime.now()
    for filename in os.listdir(app.config['UPLOAD_FOLDER']):
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file_modified = datetime.fromtimestamp(os.path.getmtime(file_path))
        if (current_time - file_modified).total_seconds() > 3600:  # 1 hour
            try:
                os.remove(file_path)
                logging.info(f"Cleaned up old file: {filename}")
            except Exception as e:
                logging.error(f"Error cleaning up file {filename}: {e}")

@app.route('/api/health')
def health_check():
    """Health check endpoint"""
    return jsonify({'status': 'healthy', 'timestamp': datetime.now().isoformat()})

@app.route('/api/convert', methods=['POST'])
def upload_file():
    try:
        cleanup_old_files()  # Clean up old files before processing new ones
        
        if 'file' not in request.files:
            return jsonify({'error': 'No file part in the request'}), 400

        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400

        if not allowed_file(file.filename):
            return jsonify({'error': 'Only .docx files are allowed'}), 400

        password = request.form.get('password')

        # Create unique filename
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        original_filename = secure_filename(file.filename)
        filename = f"{timestamp}_{original_filename}"
        
        docx_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        pdf_filename = filename.rsplit('.', 1)[0] + '.pdf'
        pdf_path = os.path.join(app.config['UPLOAD_FOLDER'], pdf_filename)

        # Save and convert file
        file.save(docx_path)
        pythoncom.CoInitialize()
        try:
            convert(docx_path, pdf_path)
        finally:
            pythoncom.CoUninitialize()

        # Add password if provided
        if password:
            protected_pdf_path = os.path.join(app.config['UPLOAD_FOLDER'], f"protected_{pdf_filename}")
            add_password_protection(pdf_path, protected_pdf_path, password)
            os.remove(pdf_path)  # Remove unprotected version
            pdf_path = protected_pdf_path

        # Generate download URL
        download_url = f"/api/download/{os.path.basename(pdf_path)}"
        
        return jsonify({
            'success': True,
            'message': 'File converted successfully',
            'download_url': download_url,
            'filename': os.path.basename(pdf_path),
            'size': os.path.getsize(pdf_path)
        })

    except Exception as e:
        logging.error(f"Conversion error: {str(e)}")
        return jsonify({'error': 'File conversion failed', 'details': str(e)}), 500

@app.route('/api/download/<filename>')
def download_file(filename):
    try:
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        if not os.path.exists(file_path):
            return jsonify({'error': 'File not found'}), 404
        return send_file(file_path, as_attachment=True)
    except Exception as e:
        logging.error(f"Download error: {str(e)}")
        return jsonify({'error': 'Download failed'}), 500

def add_password_protection(input_pdf_path, output_pdf_path, password):
    try:
        pdf_reader = PdfReader(input_pdf_path)
        pdf_writer = PdfWriter()

        for page in pdf_reader.pages:
            pdf_writer.add_page(page)

        pdf_writer.encrypt(password)
        with open(output_pdf_path, 'wb') as output_file:
            pdf_writer.write(output_file)
    except Exception as e:
        logging.error(f"Password protection error: {str(e)}")
        raise

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)