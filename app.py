import os
import uuid
from werkzeug.utils import secure_filename
from pathlib import Path
import random
from flask import Flask, flash, request, redirect, url_for, render_template, jsonify
from flask_cors import CORS, cross_origin
import chaosencryptor.src.models
from PIL import Image
import json

DEBUG = True
dirp = Path(__file__).parents[0]
template_folder = os.path.join(dirp, 'templates')
static_folder = os.path.join(template_folder, 'static')
media_folder = os.path.join(static_folder)
media_base_url = '/static'

app = Flask(__name__, template_folder=template_folder, static_folder=static_folder)
cors = CORS(app)
# media folder should be in static
app.config['UPLOAD_FOLDER'] = media_folder
app.config['MAX_CONTENT_LENGTH'] = 16*1024*1024 # 16MB
app.config['NEXT_IMAGE_ID'] = 1
app.config['store'] = {'images': {}, 'current_upimg': None}

IMAGE_EXTENSIONS = set(['png'])

def verify_image_extension(s):
    return '.' in s and s.rsplit('.',1)[1].lower() in IMAGE_EXTENSIONS

@app.route('/')
def main():
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
    app.config['store']['current_upimg'] = img_path
    #print(app.config['store']['current_upimg'])

    return result, 200

@app.route('/encrypt', methods=['GET'])
def encrypt():

    model = request.args.get('model')

    encrypter = getattr(chaosencryptor.src.models, model)()

    im = Image.open(app.config['store']['current_upimg'])
    name = im.filename
    im = im.convert('RGB')
    image, key = encrypter.encrypt(image=im, name=name)

    img_path = f'{name.rsplit(".", 1)[0]}_encrypted{random.randint(0, 99999)}.png'

    image.save(img_path)

    app.config['store']['current_encryptimg'] = img_path

    result = {
        'message': 'Image encrypted',
        'key': json.dumps(key),
        'url': f'{media_base_url}/{os.path.basename(img_path)}'
    }

    return result, 200

@app.route('/decrypt', methods=['POST'])
def decrypt():
    result = {'uploaded': False}
    keystring = request.form.get('keystring')
    model = request.form.get('model')

    if not keystring:
        result['message'] = 'No key provided'
        return result, 404
    
    # Success
    # open the current uploaded image
    im = Image.open(app.config['store']['current_upimg'])
    name = im.filename
    im = im.convert('RGB')

    # load the json string
    key = json.loads(keystring.replace('\\', ''))

    decrypter = getattr(chaosencryptor.src.models, model)()

    image = decrypter.decrypt(image=im, key=key)

    img_path = f'{name.rsplit(".", 1)[0]}_decrypted{random.randint(0, 99999)}.png'

    image.save(img_path)

    app.config['store']['current_decryptimg'] = img_path

    result = {
        'message': 'Image decrypted',
        'url': f'{media_base_url}/{os.path.basename(img_path)}'
    }

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
        app.run(debug=True, use_reloader=True)
    else:
        app.run()
