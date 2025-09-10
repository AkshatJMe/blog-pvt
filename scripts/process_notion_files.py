import os
import re
import zipfile
import shutil
import datetime
import hashlib
import json
from pathlib import Path

# Always resolve from project root
BASE_DIR = Path(__file__).resolve().parent.parent

NOTION_DIR = BASE_DIR / "notion"
OUTPUT_BLOG_DIR = BASE_DIR / "output" / "blog"
OUTPUT_IMAGE_DIR = BASE_DIR / "output" / "images"
ALLOWED_IMAGE_EXTS = {".jpg", ".jpeg", ".png", ".gif", ".webp", ".svg"}

# -----------------------------

def slugify(text: str) -> str:
    return re.sub(r'[^a-z0-9]+', '-', text.lower()).strip('-')

def to_webp(filename: str) -> str:
    stem = Path(filename).stem
    return f"{stem}.webp"

def unique_slug(title: str) -> str:
    base = slugify(title)
    hash_suffix = hashlib.md5(title.encode("utf-8")).hexdigest()[:32]
    return f"{base}-{hash_suffix}"

def extract_zip(zip_path: Path, extract_to: Path):
    with zipfile.ZipFile(zip_path, 'r') as z:
        z.extractall(extract_to)

def parse_notion_md(md_path: Path):
    lines = md_path.read_text(encoding="utf-8").splitlines(keepends=True)
    title = ""
    idx = 0
    while idx < len(lines):
        if lines[idx].startswith("# "):
            title = lines[idx].lstrip("# ").strip()
            idx += 1
            break
        idx += 1

    while idx < len(lines) and lines[idx].strip() == "":
        idx += 1

    key_re = re.compile(r'^\s*([A-Za-z0-9_]+)\s*:\s*(.*)$')
    meta = {}
    current_key = None

    if idx < len(lines) and key_re.match(lines[idx]):
        while idx < len(lines):
            line = lines[idx]
            m = key_re.match(line)
            if m:
                key = m.group(1).strip()
                val = m.group(2).rstrip("\n")
                meta[key] = val
                current_key = key
                idx += 1
                continue
            else:
                if current_key == "description":
                    meta["description"] = meta.get("description", "") + ("\n" + line.rstrip("\n"))
                    idx += 1
                    continue
                break

    body_lines = lines[idx:]
    while body_lines and body_lines[0].strip() == "":
        body_lines.pop(0)

    return title, meta, body_lines

def build_frontmatter(title: str, meta: dict, slug: str, square_img: str, thumb_img: str):
    fm = []
    fm.append("+++")
    fm.append(f'title = {json.dumps(title)}')
    if "description" in meta and meta["description"].strip() != "":
        fm.append(f'description = {json.dumps(meta["description"].strip())}')

    if square_img:
        webp_sq = to_webp(square_img)
        fm.append(f'imagesq = "/images/blog/{slug}/{webp_sq}"')

    if thumb_img:
        webp_thumb = to_webp(thumb_img)
        fm.append(f'image = "/images/blog/{slug}/{webp_thumb}"')

    if "authorName" in meta and meta["authorName"].strip() != "":
        fm.append(f'authorName = {json.dumps(meta["authorName"].strip())}')

    if "Date" in meta and meta["Date"].strip() != "":
        date_raw = meta["Date"].strip()
        parsed = None
        for fmt in ("%B %d, %Y", "%b %d, %Y", "%Y-%m-%d"):
            try:
                d = datetime.datetime.strptime(date_raw, fmt)
                parsed = d
                break
            except Exception:
                continue
        if parsed:
            fm.append(f'date = {parsed.strftime("%Y-%m-%dT%H:%M:%S+05:30")}')
        else:
            fm.append(f'date = {json.dumps(date_raw)}')

    if "tags" in meta and meta["tags"].strip() != "":
        tags = [t.strip() for t in re.split(r',\s*', meta["tags"].strip()) if t.strip()]
        fm.append("tags = " + json.dumps(tags))

    fm.append("+++")
    fm.append("")
    return "\n".join(fm)

def process_images_and_replace(content: str, slug: str):
    first_image = None

    def repl(m):
        nonlocal first_image
        alt = m.group(1)
        target = m.group(2).strip()
        if re.match(r'https?://', target):
            return m.group(0)
        filename = Path(target).name
        stem = Path(filename).stem

        webp_filename = f"{stem}.webp"

        if first_image is None:
            first_image = webp_filename
        
        return f'![{alt}](/images/blog/{slug}/{webp_filename})'

    new_content = re.sub(r'!\[(.*?)\]\((.*?)\)', repl, content)
    return new_content, first_image

def process_blog():
    Path(OUTPUT_BLOG_DIR).mkdir(parents=True, exist_ok=True)
    Path(OUTPUT_IMAGE_DIR).mkdir(parents=True, exist_ok=True)

    notion_zip = None
    for f in os.listdir(NOTION_DIR):
        if f.endswith(".zip"):
            notion_zip = Path(NOTION_DIR) / f
            break
    if not notion_zip:
        raise FileNotFoundError("No .zip found in notion/ folder")

    extract_to = Path(NOTION_DIR) / "extracted"
    if extract_to.exists():
        shutil.rmtree(extract_to)
    extract_to.mkdir()
    extract_zip(notion_zip, extract_to)

    md_files = list(extract_to.rglob("*.md"))
    if not md_files:
        raise FileNotFoundError("No .md file found inside the zip")
    md_file = md_files[0]

    title, meta, body_lines = parse_notion_md(md_file)
    if not title:
        title = md_file.stem

    slug = slugify(title)
    raw_content = "".join(body_lines)
    content_with_images, first_image = process_images_and_replace(raw_content, slug)

    target_img_dir = Path(OUTPUT_IMAGE_DIR) / slug
    target_img_dir.mkdir(parents=True, exist_ok=True)

    # Rename and copy notion metadata images
    square_img_name, thumb_img_name = None, None
    src_square = Path(NOTION_DIR) / "square.jpeg"
    src_thumb = Path(NOTION_DIR) / "thumb.jpeg"

    if src_square.exists():
        square_img_name = f"{slug}-square.jpeg"
        shutil.copy2(src_square, target_img_dir / square_img_name)
    if src_thumb.exists():
        thumb_img_name = f"{slug}-thumb.jpeg"
        shutil.copy2(src_thumb, target_img_dir / thumb_img_name)

    # Copy images from extracted zip
    for img in md_file.parent.iterdir():
        if img.is_file() and img.suffix.lower() in ALLOWED_IMAGE_EXTS:
            shutil.copy2(img, target_img_dir / img.name)

    frontmatter = build_frontmatter(title, meta, slug, square_img_name, thumb_img_name)
    final_md = frontmatter + content_with_images

    blog_out = Path(OUTPUT_BLOG_DIR) / f"{slug}.md"
    blog_out.write_text(final_md, encoding="utf-8")

    print("✅ Blog processed")
    print(f"Title: {title}")
    print(f"Slug: {slug}")
    print(f"Saved markdown: {blog_out}")
    print(f"Images directory: {target_img_dir}")
    if square_img_name or thumb_img_name:
        print(f"Main images: square={square_img_name}, thumb={thumb_img_name}")
    else:
        print("⚠️ No metadata images found in notion/")