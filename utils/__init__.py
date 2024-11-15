
import os
from zipfile import ZipFile
from config import ALLOWED_IMAGE_EXTENSIONS, IMAGE_UPLOADS_FOLDER, TEMP_ZIP_FOLDER


def allowed_file(filename):
    if not ('.' in filename):
        return False
    ext = filename.rsplit('.', 1)[1]
    return ext.upper() in ALLOWED_IMAGE_EXTENSIONS


def get_image_path(filename, dir):
    return os.path.join(os.getcwd(), IMAGE_UPLOADS_FOLDER, dir, filename)


def get_file_path(filename, dir):
    return os.path.join(os.getcwd(), TEMP_ZIP_FOLDER, dir, filename)


def make_zipfile(output_filename, source_dir):
    with ZipFile(output_filename, 'w') as zipObj:
        for folderName, subfolders, filenames in os.walk(source_dir):
            for filename in filenames:
                filePath = get_file_path(filename, folderName)
                zipObj.write(filePath, os.path.basename(filePath))
