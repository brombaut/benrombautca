import os

IMAGE_EXTENSIONS = {'.png', '.jpg', '.jpeg', '.gif', '.bmp', '.svg', '.webp'}
SRC_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src'))

def is_image(filename):
    return any(filename.lower().endswith(ext) for ext in IMAGE_EXTENSIONS)

def format_size(size_bytes):
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size_bytes < 1024:
            return f"{size_bytes:.2f} {unit}"
        size_bytes /= 1024
    return f"{size_bytes:.2f} TB"

webp_total = 0
other_total = 0
for root, dirs, files in os.walk(SRC_DIR):
    for file in files:
        if is_image(file):
            file_path = os.path.join(root, file)
            size = os.path.getsize(file_path)
            if file.lower().endswith('.webp'):
                webp_total += size
            else:
                other_total += size
            print(f"{file_path}: {format_size(size)}")

print(f"\nTotal size of .webp images: {format_size(webp_total)}")
print(f"Total size of other images: {format_size(other_total)}")
print(f"Total size of all images: {format_size(webp_total + other_total)}")
