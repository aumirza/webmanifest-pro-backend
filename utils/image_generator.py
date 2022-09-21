from io import BytesIO
import os
import shutil
import uuid
from utils import get_file_path, get_image_path, make_zipfile
from PIL import Image
from werkzeug.utils import secure_filename


async def generate_images_zip(image):
    temp_dir_name = uuid.uuid4().hex
    temp_image_dir = get_image_path('', temp_dir_name)
    os.mkdir(temp_image_dir)

    # if not isinstance(image, BytesIO):
    #     file_name = secure_filename(image.filename)
    #     img_path = get_image_path(file_name, temp_dir_name)
    #     image.save(img_path)
    # else:
    file_name = 'image.png'
    img_path = get_image_path(file_name, temp_dir_name)
    with open(img_path, "wb") as binary_file:
        binary_file.write(image.getbuffer())

    temp_zip_dir = get_file_path('', temp_dir_name)
    os.mkdir(temp_zip_dir)
    zip_file_path = get_file_path('images.zip', temp_dir_name)

    img = Image.open(img_path)
    os.remove(img_path)
    generate_diff_images(img, temp_dir_name)
    make_zipfile(zip_file_path, temp_image_dir)

    shutil.rmtree(temp_image_dir, ignore_errors=False, onerror=None)

    return zip_file_path


def generate_diff_images(img, image_dir):
    android_chrome_192X192 = img.resize((192, 192))
    android_chrome_512X512 = img.resize((512, 512))
    apple_touch_icon = img.resize((180, 180))
    favicon_16X16 = img.resize((16, 16))
    favicon_32X32 = img.resize((32, 32))
    favicon = img.resize((64, 64))
    mstile_150X150 = img.resize((150, 150))
    safari_pinned_tab = img.resize((512, 512))

    android_chrome_192X192.save(
        get_image_path('android-chrome-192x192.png', image_dir))
    android_chrome_512X512.save(
        get_image_path('android-chrome-512x512.png', image_dir))
    apple_touch_icon.save(
        get_image_path('apple-touch-icon.png', image_dir))
    favicon_16X16.save(get_image_path('favicon-16x16.png', image_dir))
    favicon_32X32.save(get_image_path('favicon-32x32.png', image_dir))
    favicon.save(get_image_path('favicon.ico', image_dir))
    mstile_150X150.save(
        get_image_path('mstile-150x150.png', image_dir))
    safari_pinned_tab.save(
        get_image_path('safari-pinned-tab.png', image_dir))
