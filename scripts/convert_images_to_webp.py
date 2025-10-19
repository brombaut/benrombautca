import os
from PIL import Image, ExifTags

IMAGE_EXTENSIONS = {'.png', '.jpg', '.jpeg', '.gif', '.bmp', '.tiff'}
SRC_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src'))

def is_image(filename):
    ext = os.path.splitext(filename)[1].lower()
    return ext in IMAGE_EXTENSIONS

def auto_orient(img):
    try:
        exif = img._getexif()
        if exif:
            for orientation in ExifTags.TAGS.keys():
                if ExifTags.TAGS[orientation] == 'Orientation':
                    break
            orientation_value = exif.get(orientation)
            if orientation_value == 3:
                img = img.rotate(180, expand=True)
            elif orientation_value == 6:
                img = img.rotate(270, expand=True)
            elif orientation_value == 8:
                img = img.rotate(90, expand=True)
    except Exception:
        pass
    return img

def convert_to_webp(image_path):
    ext = os.path.splitext(image_path)[1].lower()
    if ext == '.webp':
        return  # Already webp
    webp_path = os.path.splitext(image_path)[0] + '.webp'
    try:
        with Image.open(image_path) as img:
            img = auto_orient(img)
            img.save(webp_path, 'webp')
        print(f"Converted: {image_path} -> {webp_path}")
    except Exception as e:
        print(f"Failed to convert {image_path}: {e}")

for root, dirs, files in os.walk(SRC_DIR):
    for file in files:
        if is_image(file):
            file_path = os.path.join(root, file)
            convert_to_webp(file_path)
