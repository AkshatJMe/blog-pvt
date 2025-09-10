from pathlib import Path
from PIL import Image

BASE_DIR = Path(__file__).resolve().parent.parent
NOTION_DIR = BASE_DIR / "notion"

# Allowed image extensions to check
ALLOWED_EXTS = {".jpg", ".jpeg", ".png", ".gif", ".bmp", ".tiff", ".webp"}

def convert_to_jpeg_inplace(image_path: Path, quality=85):
    with Image.open(image_path) as img:
        img = img.convert("RGB")  # JPEG does not support transparency
        jpeg_path = image_path.with_suffix(".jpeg")
        img.save(jpeg_path, "JPEG", quality=quality)
    
    # Remove original file if different from jpeg
    if image_path != jpeg_path:
        image_path.unlink()
    print(f"Converted {image_path.name} -> {jpeg_path.name}")

def process_notion_images():
    if not NOTION_DIR.exists():
        print(f"Notion folder does not exist: {NOTION_DIR}")
        return

    for file in NOTION_DIR.iterdir():
        if file.is_file() and file.suffix.lower() in ALLOWED_EXTS:
            name_lower = file.stem.lower()
            if "square" in name_lower or "thumb" in name_lower:
                convert_to_jpeg_inplace(file)


