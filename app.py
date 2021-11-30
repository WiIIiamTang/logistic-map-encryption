import os
import uuid
from werkzeug.utils import secure_filename
from pathlib import Path
from flask import Flask, flash, request, redirect, url_for, render_template, jsonify
from flask_cors import CORS, cross_origin
import chaosencryptor.models
from PIL import Image
import pickle

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
    app.config['store']['current_upimg'] = img_path
    #print(app.config['store']['current_upimg'])

    return result, 200


@app.route('/encrypt', methods=['GET'])
def encrypt():

    model = request.args.get('model')

    encrypter = getattr(chaosencryptor.models, model)()

    im = Image.open(app.config['store']['current_upimg'])
    name = im.filename
    im = im.convert('RGB')
    image, key = encrypter.encrypt(image=im, name=name)

    img_path = f'{name.rsplit(".", 1)[0]}_encrypted{app.config["NEXT_IMAGE_ID"]}.png'

    image.save(img_path)

    app.config['store']['current_encryptimg'] = img_path

    key_path = os.path.join(app.config['UPLOAD_FOLDER'], f'{secure_filename(str(uuid.uuid4()))}.key')

    with open(key_path, 'wb') as f:
        pickle.dump(key, f)

    result = {
        'message': 'Image encrypted',
        'key': os.path.basename(key_path),
        'url': f'{media_base_url}/{os.path.basename(img_path)}'
    }

    return result, 200

@app.route('/decrypt', methods=['GET'])
def decrypt():

    result = {'uploaded': False}
    keyname = request.args.get('keyname')
    model = request.args.get('model')

    if not keyname:
        result['message'] = 'No keyname provided'
        return result, 404
    
    # Success
    im = Image.open(app.config['store']['current_encryptimg'])
    name = im.filename
    im = im.convert('RGB')

    with open(os.path.join(app.config['UPLOAD_FOLDER'], keyname), 'rb') as f:
        key = pickle.load(f)

    decrypter = getattr(chaosencryptor.models, model)()

    image = decrypter.decrypt(image=im, key=key)

    img_path = f'{name.rsplit(".", 1)[0]}_decrypted{app.config["NEXT_IMAGE_ID"]}.png'

    image.save(img_path)

    app.config['store']['current_decryptimg'] = img_path

    #key_path = os.path.join(app.config['UPLOAD_FOLDER'], 'imgkey.key')

    #with open(key_path, 'wb') as f:
        #pickle.dump(key, f)

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
        app.run(debug=True, use_reloader=True, port=5001)
    else:
        app.run()
