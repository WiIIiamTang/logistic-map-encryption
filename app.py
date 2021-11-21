import os
import uuid
from werkzeug.utils import secure_filename
from pathlib import Path
from flask import Flask, flash, request, redirect, url_for, render_template, jsonify
from flask_cors import CORS, cross_origin

DEBUG = False
dirp = Path(__file__).parents[0]
template_folder = os.path.join(dirp, 'templates')
static_folder = os.path.join(template_folder, 'static')
media_folder = os.path.join(static_folder)
media_base_url = '/static'

if DEBUG:
    app = Flask(__name__)
else:
    app = Flask(__name__, template_folder=template_folder, static_folder=static_folder)
cors = CORS(app)
app.config['UPLOAD_FOLDER'] = media_folder
app.config['MAX_CONTENT_LENGTH'] = 16*1024*1024 # 16MB
app.config['NEXT_IMAGE_ID'] = 1
app.config['store'] = {'images': {}}

IMAGE_EXTENSIONS = set(['png'])

def verify_image_extension(s):
    return '.' in s and s.rsplit('.',1)[1].lower() in IMAGE_EXTENSIONS

@app.route('/')
def main():
    if DEBUG:
        return '<div><h1>dev server</h1></div>'
    else:
        return render_template('index.html')

@app.route('/upimg', methods=['POST'])
def upimg():
    result = {'uploaded': False}
    form_input_name = 'file'

    if form_input_name not in request.files:
        result['message'] = 'No file found'
        return result, 404

    file = request.files[form_input_name]

    if not file or not file.filename:
        result['message'] = 'No filename selected'
        return result, 404

    if not verify_image_extension(file.filename):
        result['message'] = 'File extension not allowed'
        return result, 415
    
    # Success
    ext = file.filename.rsplit('.',1)[1].lower()
    new_filename = f'{app.config["NEXT_IMAGE_ID"]}_{secure_filename(str(uuid.uuid4()))}.{ext}'
    img_path = os.path.join(app.config['UPLOAD_FOLDER'], new_filename)
    app.config['store']['images'][app.config['NEXT_IMAGE_ID']] = {
        '_name': new_filename,
        'url': f'{media_base_url}/{new_filename}' 
    }
    result['message'] = 'Image uploaded'
    result['id'] = app.config['NEXT_IMAGE_ID']
    result['url'] = f'{media_base_url}/{new_filename}'
    result['uploaded'] = True
    app.config['NEXT_IMAGE_ID'] += 1
    file.save(img_path)
    return result, 200

if DEBUG:
    @app.route('/images', methods=['GET'])
    def images():
        return app.config['store']['images'], 200

    @app.route('/images/<int:id>', methods=['GET'])
    def images_id(id):
        if app.config['store']['images'].get(id):
            return app.config['store']['images'][id], 200
        else:
            return {'message': 'Did not find image'}, 404


if __name__ == '__main__':
    if DEBUG:
        app.run(debug=True, use_reloader=True, port=5001)
    else:
        app.run()
