# web-miga

Website of [Miga](https://github.com/calamares00/miga-app), the family recipe book and shopping list app
for Android: features, the sync server, recipe packs and the privacy policy.

Static HTML and CSS with no third-party requests, ready for GitHub Pages. Every link is relative, so
it works at `https://calamares00.github.io/miga-web/` and on its own domain alike.

## Structure

| Path | Content |
| :--- | :--- |
| `index.html`, `en/index.html` | Home page in Spanish and English (generated) |
| `privacy/`, `en/privacy/` | Privacy policy (generated from `content/privacy-*.md`) |
| `packs/catalog.json` | Official recipe packs catalogue the app reads by default |
| `assets/` | Styles, script, logo, app screens and miga-server screenshots |
| `content/` | Privacy policy sources: the same text as `PRIVACY.md` in the app |
| `tools/build.py` | Builds the HTML pages from the texts it holds |
| `tools/mockups.py` | Draws the illustrative phone screens in `assets/img/screens/` |

## Editing

```bash
pip install markdown
python3 tools/build.py        # after changing texts in tools/build.py or content/*.md
python3 tools/mockups.py      # only to redraw the illustrative screens
python3 -m http.server        # preview at http://localhost:8000
```

When the privacy policy changes in the app, copy `PRIVACY.md` to `content/privacy-es.md` and
`app/src/main/assets/docs/privacy-en.md` to `content/privacy-en.md`, then rebuild.

### Real screenshots

The phone screens in `assets/img/screens/*.svg` are illustrations in the app's Huerta colours. To use
real screenshots, save them as PNG (portrait, about 1080×2280) in the same folder and change the
`.svg` extension of that screen in `tools/build.py`.

### Recipe packs

Add each pack's ZIP (a book exported from Miga as a "Miga file") under `packs/zips/`, its cover
under `packs/covers/`, and an entry in `packs/catalog.json`:

```json
{
  "id": "cocina-de-la-abuela",
  "name": "Cocina de la abuela",
  "author": "Ana",
  "description": "Guisos, potajes y postres de siempre.",
  "coverImageUrl": "covers/abuela.jpg",
  "latestVersion": 1,
  "recipeCount": 24,
  "downloadUrl": "zips/abuela.zip"
}
```

Increase `latestVersion` when a pack changes so the app offers the update.

## Publishing

The site is served at **https://miga.calamares.org** (the `CNAME` file) with GitHub Pages: in the
repository settings, **Pages › Build and deployment**, deploy from the `main` branch, root folder, with
`miga.calamares.org` as the custom domain and HTTPS enforced. The DNS has a `CNAME` record for
`miga.calamares.org` pointing to `calamares00.github.io`.

The app reads the packs catalogue from `https://miga.calamares.org/packs/catalog.json`, and Google
Play links to the privacy policy at `https://miga.calamares.org/privacy/`.

## License

[GPL-3.0](LICENSE), like the app. Product data shown in the app comes from Open Food Facts (ODbL).
