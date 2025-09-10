import shutil
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

# Paths
NOTION_DIR = BASE_DIR / "notion"
OUTPUT_BLOG_DIR = BASE_DIR / "output" / "blog"
OUTPUT_IMAGE_DIR = BASE_DIR / "output" / "images"

def delete_contents(folder: Path):
    """Delete all files and subfolders inside a folder but keep the folder itself."""
    if folder.exists() and folder.is_dir():
        for item in folder.iterdir():
            if item.is_file() or item.is_symlink():
                item.unlink()
                print(f"🗑 Deleted file: {item}")
            elif item.is_dir():
                shutil.rmtree(item)
                print(f"🗑 Deleted folder: {item}")
    else:
        print(f"⚠️ Folder not found: {folder}")

def cleanup():
    # Clean contents inside notion folder but keep folder itself
    delete_contents(NOTION_DIR)

    # Clean contents inside output/blog
    delete_contents(OUTPUT_BLOG_DIR)

    # Clean contents inside output/images
    delete_contents(OUTPUT_IMAGE_DIR)

    print("✅ Cleanup complete!")