# Taumorrow — start page

Source of truth: `src/index.src.html` (English text in the markup, translations in the `I18N` dictionary).

Build (writes `index.html`, one folder per language, icons, `og.png`, `sitemap.xml`, `robots.txt`, `manifest.webmanifest`):

    python3 tools/build.py

Never edit the generated `index.html` or `<lang>/index.html` by hand; edit `src/index.src.html` and rebuild.
Published by GitHub Pages at https://taumorrow.com (CNAME); taumorrow.de and taumorrow.eu redirect here.
