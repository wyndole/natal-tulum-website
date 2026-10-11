# Natal Tulum — website

Static website for the Natal condo (La Veleta, Tulum). Plain HTML/CSS/JS — no build step,
so it can be hosted free on GitHub Pages, Netlify or Cloudflare Pages.

## Folder layout
| Path | What it is |
|---|---|
| `index.html` | The page (EN, with ES toggle) |
| `css/style.css`, `js/main.js` | Styling, gallery/lightbox, language toggle |
| `photos-original/` | Full-size photos from the Google Photos **Natal** album (not pushed to GitHub) |
| `images/gallery/` | Web-sized photos + thumbnails (generated) |
| `gallery.json` | Photo list the page reads (generated; add `alt` text here) |
| `scripts/build_gallery.py` | Resizes originals and rebuilds `gallery.json` |

## Adding photos
1. In Google Photos, open the **Natal** album → ⋮ menu → **Download all** (saves a .zip).
2. Unzip into `photos-original/`.
3. Optional: rename to set order (`01-living.jpg`, `02-kitchen.jpg` …) and name the cover `hero-….jpg`.
4. Run `python scripts/build_gallery.py`.

## Preview locally
`python -m http.server 8000` in this folder, then open http://localhost:8000
(opening index.html directly won't load the gallery because of browser file restrictions).

## To-do
- [ ] Fill in guests / bedrooms / baths (marked `[#]` in index.html)
- [ ] Add Airbnb / VRBO / contact links
- [ ] Alt text for photos in gallery.json
- [ ] Choose hosting + domain
