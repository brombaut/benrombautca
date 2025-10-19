import os

# Set the directory you want to clean up
SRC_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src'))


TARGET_DIRS = [
    os.path.abspath(os.path.join(SRC_DIR, 'hiking')),
    os.path.abspath(os.path.join(SRC_DIR, 'running')),
    os.path.abspath(os.path.join(SRC_DIR, 'bookshelf'))
]

IMAGE_EXTENSIONS = {'.png', '.jpg', '.jpeg', '.gif', '.bmp', '.tiff', '.svg'}  # Exclude .webp

def is_non_webp_image(filename):
    ext = os.path.splitext(filename)[1].lower()
    return ext in IMAGE_EXTENSIONS

deleted_files = 0
for target_dir in TARGET_DIRS:
    for root, dirs, files in os.walk(target_dir):
        for file in files:
            if is_non_webp_image(file):
                file_path = os.path.join(root, file)
                try:
                    os.remove(file_path)
                    print(f"Deleted: {file_path}")
                    deleted_files += 1
                except Exception as e:
                    print(f"Failed to delete {file_path}: {e}")

print(f"\nTotal non-webp images deleted: {deleted_files}")
