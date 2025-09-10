import os
from pathlib import Path
from PIL import Image

# Base directory of your project (two levels up from this script)
BASE_DIR = Path(__file__).resolve().parent.parent

# Configuration with absolute paths
INPUT_DIR = BASE_DIR / "output" / "images"
WEBP_QUALITY = 85
SKIP_IF_LARGER = True

def get_kb(path):
    return os.path.getsize(path) / 1024

def crop_center_square(img):
    w, h = img.size
    min_dim = min(w, h)
    left = (w - min_dim) // 2
    top = (h - min_dim) // 2
    return img.crop((left, top, left + min_dim, top + min_dim))

def crop_center_16_9(img):
    w, h = img.size
    target_ratio = 16 / 9
    current_ratio = w / h

    if current_ratio > target_ratio:
        new_width = int(h * target_ratio)
        left = (w - new_width) // 2
        return img.crop((left, 0, left + new_width, h))
    else:
        new_height = int(w / target_ratio)
        top = (h - new_height) // 2
        return img.crop((0, top, w, top + new_height))

def process_image(file_path):
    filename = os.path.basename(file_path)
    name, ext = os.path.splitext(filename)
    ext = ext.lower()

    if ext not in [".jpg", ".jpeg", ".png"]:
        return

    input_kb = get_kb(file_path)

    with Image.open(file_path) as img:
        img = img.convert("RGB")
        original_img = img

        # Crop square
        if "square" in name.lower():
            img = crop_center_square(img)

        # Crop 16:9
        elif "thumb" in name.lower():
            img = crop_center_16_9(img)

        # Save WebP version
        webp_path = os.path.splitext(file_path)[0] + ".webp"
        img.save(webp_path, "WEBP", quality=WEBP_QUALITY)
        webp_kb = get_kb(webp_path)

        # Check if WebP is larger
        if SKIP_IF_LARGER and webp_kb > input_kb:
            os.remove(webp_path)
            print(f"⚠️ Skipped: {filename} → {os.path.basename(webp_path)} | WebP was larger ({webp_kb:.1f} KB > {input_kb:.1f} KB)")
        else:
            os.remove(file_path)
            report_change(filename, os.path.basename(webp_path), input_kb, webp_kb)

def report_change(original_name, new_name, original_kb, new_kb):
    change_kb = new_kb - original_kb
    percent_change = (change_kb / original_kb) * 100

    if percent_change > 0:
        print(f"⚠️ Increased: {original_name} -> {new_name} | {original_kb:.1f} KB → {new_kb:.1f} KB (+{percent_change:.1f}%)")
    else:
        print(f"✅ Reduced: {original_name} -> {new_name} | {original_kb:.1f} KB → {new_kb:.1f} KB (-{abs(percent_change):.1f}%)")

# Process all images
def processImages():
    for root, dirs, files in os.walk(INPUT_DIR):
        for file in files:
            process_image(os.path.join(root, file))
