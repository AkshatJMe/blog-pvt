import shutil
from pathlib import Path

# Get the base directory of the project, relative to this script
BASE_DIR = Path(__file__).resolve().parent.parent  # goes up from scripts/

# ---------- CONFIG ----------
OUTPUT_BLOG_DIR = BASE_DIR / "output" / "blog"      # Notion exported markdown files
OUTPUT_IMAGE_DIR = BASE_DIR / "output" / "images"   # Notion exported images (flat or folders)

BLOG_CONTENT_DIR = BASE_DIR / "content" / "blog"    # Target for blog posts
BLOG_IMAGE_DIR = BASE_DIR / "static" / "images" / "blog"     # Target for images
# ----------------------------

def copy_if_newer(src: Path, dest: Path):
    """Copy src to dest if dest doesn't exist or src is newer."""
    if not dest.exists() or src.stat().st_mtime > dest.stat().st_mtime:
        shutil.copy2(src, dest)
        print(f"📄 Copied: {src.relative_to(src.parent)} → {dest.relative_to(dest.parent)}")
    else:
        print(f"↪️  Skipped (up-to-date): {src.relative_to(src.parent)}")

def transfer_to_blog():
    # Ensure target dirs exist
    BLOG_CONTENT_DIR.mkdir(parents=True, exist_ok=True)
    BLOG_IMAGE_DIR.mkdir(parents=True, exist_ok=True)

    print(f"📁 Copying blog posts to: {BLOG_CONTENT_DIR}")
    print(f"🖼 Copying images to:     {BLOG_IMAGE_DIR}")

    # Copy .md files (non-destructive)
    for md_file in OUTPUT_BLOG_DIR.glob("*.md"):
        target = BLOG_CONTENT_DIR / md_file.name
        copy_if_newer(md_file, target)

    # Copy image files and folders (non-destructive)
    for item in OUTPUT_IMAGE_DIR.iterdir():
        target = BLOG_IMAGE_DIR / item.name

        if item.is_file():
            copy_if_newer(item, target)

        elif item.is_dir():
            target.mkdir(parents=True, exist_ok=True)
            for sub_item in item.rglob("*"):
                if sub_item.is_file():
                    relative_path = sub_item.relative_to(item)
                    sub_target = target / relative_path
                    sub_target.parent.mkdir(parents=True, exist_ok=True)
                    copy_if_newer(sub_item, sub_target)

    print("✅ Blog transfer complete! All new or updated files copied.")