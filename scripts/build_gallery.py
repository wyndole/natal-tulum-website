"""Turn the original photos into web-sized images and write gallery.json.

Usage (from the project folder):
    pip install pillow
    python scripts/build_gallery.py

Reads:  photos-original/  (full-size photos downloaded from the Google Photos "Natal" album)
Writes: images/gallery/<name>.jpg (1800px long edge), images/gallery/thumbs/<name>.jpg (700px)
        gallery.json  (order = filename order; rename files 01-..., 02-... to control order)

To pick the hero photo, name its file starting with "hero" (e.g. hero-pool.jpg).
Existing alt text in gallery.json is kept when you re-run.
"""
import json, re
from pathlib import Path
from PIL import Image, ImageOps

ROOT = Path(__file__).resolve().parent.parent
SRC, OUT = ROOT / "photos-original", ROOT / "images" / "gallery"
THUMBS = OUT / "thumbs"
EXTS = {".jpg", ".jpeg", ".png", ".webp", ".heic"}

try:
    from pillow_heif import register_heif_opener; register_heif_opener()
except ImportError:
    pass

def slug(name):
    return re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")

def save(img, path, edge, q):
    im = img.copy(); im.thumbnail((edge, edge), Image.LANCZOS)
    im.save(path, "JPEG", quality=q, optimize=True, progressive=True)

def main():
    OUT.mkdir(parents=True, exist_ok=True); THUMBS.mkdir(exist_ok=True)
    old = {}
    gj = ROOT / "gallery.json"
    if gj.exists():
        old = {p["full"]: p for p in json.loads(gj.read_text(encoding="utf-8"))}
    entries = []
    files = sorted(p for p in SRC.iterdir() if p.suffix.lower() in EXTS)
    for f in files:
        name = slug(f.stem) + ".jpg"
        full, thumb = f"images/gallery/{name}", f"images/gallery/thumbs/{name}"
        try:
            img = ImageOps.exif_transpose(Image.open(f)).convert("RGB")
        except Exception as e:
            print(f"skip {f.name}: {e}"); continue
        save(img, OUT / name, 1800, 82)
        save(img, THUMBS / name, 700, 78)
        entry = {"full": full, "thumb": thumb, "alt": old.get(full, {}).get("alt", "")}
        if f.stem.lower().startswith("hero"): entry["hero"] = True
        entries.append(entry)
        print("ok", f.name, "->", name)
    gj.write_text(json.dumps(entries, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"\n{len(entries)} photos written to gallery.json")

if __name__ == "__main__":
    main()
