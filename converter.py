from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import tempfile
import pypandoc
from werkzeug.utils import secure_filename

app = Flask(__name__)
CORS(app)  # Abilita CORS per tutte le rotte

# Estensioni supportate
ALLOWED_EXTENSIONS = {'txt', 'md', 'csv', 'docx', 'rtf'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/convert', methods=['POST'])
def convert_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    file = request.files['file']

    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    if not allowed_file(file.filename):
        return jsonify({'error': 'File type not allowed'}), 400

    filename = secure_filename(file.filename)
    ext = filename.rsplit('.', 1)[1].lower()

    # Salva il file temporaneamente
    with tempfile.NamedTemporaryFile(delete=False, suffix='.' + ext) as tmp:
        file.save(tmp.name)
        tmp_path = tmp.name

    try:
        # Conversione con pypandoc
        text = pypandoc.convert_file(tmp_path, 'plain')
    except Exception as e:
        os.unlink(tmp_path)
        return jsonify({'error': f'Conversion failed: {str(e)}'}), 500

    os.unlink(tmp_path)
    return jsonify({'text': text})

@app.route('/', methods=['GET'])
def health():
    return "OK", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
