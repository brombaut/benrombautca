import os
from PIL import Image

# === Configuration ===
SRC_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src'))


TARGET_DIR_CONFIGS = {
    'hiking': {'max_width': 800, 'max_height': 800},
    'running': {'max_width': 1200, 'max_height': 1200},
    'bookshelf': {'max_width': 150, 'max_height': 195},
}

QUALITY = 100
METHOD = 6  # Compression efficiency: 0=fastest, 6=best
OVERWRITE = True  # Overwrite existing .webp files

def is_webp_image(filename: str) -> bool:
    return os.path.splitext(filename)[1].lower() == '.webp'

# === Main ===
for target_dir, target_config in TARGET_DIR_CONFIGS.items():
    print(f"\nProcessing directory: {target_dir} "
          f"(max {target_config['max_width']}x{target_config['max_height']})")
    target_dir = os.path.abspath(os.path.join(SRC_DIR, target_dir))
    for root, dirs, files in os.walk(target_dir):
        for file in files:
            if not is_webp_image(file):
                continue

            full_path = os.path.join(root, file)
            try:
                with Image.open(full_path) as img:
                    orig_w, orig_h = img.size

                    # Compute new dimensions
                    ratio = min(target_config['max_width'] / orig_w, target_config['max_height'] / orig_h, 1.0)
                    new_w, new_h = int(orig_w * ratio), int(orig_h * ratio)

                    # Skip if already small enough
                    if (new_w, new_h) == (orig_w, orig_h):
                        print(f"⏩ Skipping (already small enough): {os.path.relpath(full_path, SRC_DIR)}")
                        continue

                    # Resize image
                    resized = img.resize((new_w, new_h), Image.LANCZOS)

                    # Either overwrite or save separately
                    output_path = full_path if OVERWRITE else os.path.splitext(full_path)[0] + "_resized.webp"

                    # Save resized image
                    resized.convert("RGB").save(
                        output_path,
                        "webp",
                        quality=QUALITY,
                        method=METHOD,
                        optimize=True,
                    )

                    print(f"✅ Resized: {os.path.relpath(full_path, SRC_DIR)} "
                          f"({orig_w}x{orig_h} → {new_w}x{new_h})")

            except Exception as e:
                print(f"❌ Failed to process {os.path.relpath(full_path, SRC_DIR)}: {e}")

print("\n🎉 Done! All .webp images resized where needed.")