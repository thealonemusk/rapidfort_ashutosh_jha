from flask import Flask, request, jsonify, render_template, send_file
from werkzeug.utils import secure_filename
import os
from docx2pdf import convert

app = Flask(__name__)

# Configure upload folder
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'docx'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Create uploads directory if it doesn't exist
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    file = request.files['file']

    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    if not allowed_file(file.filename):
        return jsonify({'error': 'Only .docx files are allowed'}), 400

    if file:
        filename = secure_filename(file.filename)
        docx_path = os.path.join(app.root_path, app.config['UPLOAD_FOLDER'], filename)
        pdf_filename = filename.rsplit('.', 1)[0] + '.pdf'
        pdf_path = os.path.join(app.root_path, app.config['UPLOAD_FOLDER'], pdf_filename)
        
        # Save the uploaded .docx file
        file.save(docx_path)
        
        # Convert to PDF
        try:
            convert(docx_path, pdf_path)
            return jsonify({
                'message': 'File uploaded and converted successfully',
                'original_file': filename,
                'pdf_file': pdf_filename,
                'download_url': f'/download/{pdf_filename}'
            })
        except Exception as e:
            return jsonify({'error': f'Conversion failed: {str(e)}'}), 500

@app.route('/download/<filename>')
def download_file(filename):
    try:
        return send_file(
            os.path.join(app.root_path, app.config['UPLOAD_FOLDER'], filename),
            as_attachment=True
        )
    except Exception as e:
        return jsonify({'error': f'Download failed: {str(e)}'}), 404

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8080, debug=True)