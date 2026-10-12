"""Build the website gallery from your original photos.

Usage (from the project folder):
    python scripts/build_gallery.py

Reads photos.json, the list of picked photos. Each entry:
    {"src": "TUL00404.JPG", "name": "01-patio", "alt": "description", "hero": true}
  src  - file name inside photos-original/ (searched in subfolders too, e.g. photos-original/Natal/)
  name - output name; the gallery follows the order of photos.json
  alt  - short description (for accessibility and Google)
  hero - optional; this photo becomes the big cover image at the top of the page
  group - optional; "around" puts it in the Around Tulum strip (Location section) instead of the gallery
  alt_es - optional Spanish caption
To swap a photo, change "src". To drop one, delete its line. To reorder, move lines.

Writes images/gallery/<name>.jpg (1800px), images/gallery/thumbs/<name>.jpg (700px) and gallery.json.
"""
import json
from pathlib import Path
from PIL import Image, ImageOps

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "photos-original"
OUT = ROOT / "images" / "gallery"
THUMBS = OUT / "thumbs"

def find(name):
    hits = [p for p in SRC.rglob(name) if "_review" not in p.parts]
    return hits[0] if hits else None

def save(img, path, edge, q):
    im = img.copy(); im.thumbnail((edge, edge), Image.LANCZOS)
    im.save(path, "JPEG", quality=q, optimize=True, progressive=True)

def main():
    OUT.mkdir(parents=True, exist_ok=True); THUMBS.mkdir(exist_ok=True)
    picks = json.loads((ROOT / "photos.json").read_text(encoding="utf-8"))
    entries = []
    for p in picks:
        f = find(p["src"])
        if not f:
            print("MISSING", p["src"]); continue
        img = Image.open(f); img.draft("RGB", (3600, 3600))
        img = ImageOps.exif_transpose(img).convert("RGB")
        img = ImageOps.autocontrast(img, cutoff=0.3, preserve_tone=True)  # gentle levels fix
        name = p["name"] + ".jpg"
        save(img, OUT / name, 1800, 82)
        save(img, THUMBS / name, 700, 78)
        e = {"full": f"images/gallery/{name}", "thumb": f"images/gallery/thumbs/{name}", "alt": p.get("alt", "")}
        if p.get("alt_es"): e["alt_es"] = p["alt_es"]
        if p.get("group"): e["group"] = p["group"]
        if p.get("hero"): e["hero"] = True
        entries.append(e)
        print("ok", p["src"], "->", name)
    (ROOT / "gallery.json").write_text(json.dumps(entries, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"\n{len(entries)} photos -> gallery.json")

if __name__ == "__main__":
    main()
