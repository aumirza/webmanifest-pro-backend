from backend.utils import get_image_path


def generate_images(img, temp_image_dir):

    android_chrome_192X192 = img.resize((192, 192))
    android_chrome_512X512 = img.resize((512, 512))
    apple_touch_icon = img.resize((180, 180))
    favicon_16X16 = img.resize((16, 16))
    favicon_32X32 = img.resize((32, 32))
    favicon = img.resize((64, 64))
    mstile_150X150 = img.resize((150, 150))
    safari_pinned_tab = img.resize((512, 512))

    android_chrome_192X192.save(get_image_path(
        'android-chrome-192x192.png', temp_image_dir))
    android_chrome_512X512.save(get_image_path(
        'android-chrome-512x512.png', temp_image_dir))
    apple_touch_icon.save(get_image_path(
        'apple-touch-icon.png', temp_image_dir))
    favicon_16X16.save(get_image_path('favicon-16x16.png', temp_image_dir))
    favicon_32X32.save(get_image_path('favicon-32x32.png', temp_image_dir))
    favicon.save(get_image_path('favicon.ico', temp_image_dir))
    mstile_150X150.save(get_image_path(
        'mstile-150x150.png', temp_image_dir))
    safari_pinned_tab.save(get_image_path(
        'safari-pinned-tab.png', temp_image_dir))
