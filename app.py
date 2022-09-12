import os
import shutil
from flask import Flask, jsonify, request, send_file
from werkzeug.utils import secure_filename
from PIL import Image
import uuid

from backend.utils import allowed_file, get_file_path, get_image_path, make_zipfile
from backend.utils.image_generator import generate_images

app = Flask(__name__)

app.config['IMAGE_UPLOADS_FOLDER'] = 'temp_images'
ALLOWED_IMAGE_EXTENSIONS = ['PNG', 'JPG', 'JPEG', 'GIF']
app.config['TEMP_ZIP_FOLDER'] = 'temp_zip'


@app.route('/', methods=['GET'])
def home():
    return jsonify({'message': 'Hello World!'})


@app.route('/', methods=['POST'])
def crop():

    image = request.files.get('image')

    if image and allowed_file(image.filename):

        temp_dir_name = uuid.uuid4().hex

        file_name = secure_filename(image.filename)
        temp_image_dir = get_image_path('', temp_dir_name)
        os.mkdir(temp_image_dir)
        img_path = get_image_path(file_name, temp_dir_name)
        image.save(img_path)

        temp_zip_dir = get_file_path(
            app.config['TEMP_ZIP_FOLDER'], temp_dir_name)
        os.mkdir(temp_zip_dir)
        zip_file = os.path.join(temp_zip_dir, 'images.zip')

        img = Image.open(img_path)
        os.remove(img_path)
        generate_images(img, temp_dir_name)
        make_zipfile(zip_file, temp_image_dir)

        shutil.rmtree(temp_image_dir, ignore_errors=False, onerror=None)

        return send_file(zip_file, as_attachment=True)

    return jsonify({'message': 'error'})


if __name__ == '__main__':
    app.run(debug=True)
