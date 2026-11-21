# web-miga

Website of Miga, the family recipe book and shopping list app
for Android: features, the sync server, recipe packs and the privacy policy.

Static HTML and CSS with no third-party requests, ready for GitHub Pages. Every link is relative, so
it works at `https://calamares00.github.io/miga-web/` and on its own domain alike.

## Structure

| Path | Content |
| :--- | :--- |
| `index.html`, `en/index.html` | Home page in Spanish and English (generated): hero, showcase and links to each section |
| `funciones/`, `salud/`, `asistente/`, `familia/`, `packs/index.html`, `preguntas/` | Section pages in Spanish (generated); in English under `en/` as `features/`, `health/`, `assistant/`, `family/`, `packs/`, `faq/` |
| `privacy/`, `en/privacy/` | Privacy policy (generated from `content/privacy-*.md`) |
| `packs/catalog.json` | Official recipe packs catalogue the app reads by default |
| `assets/` | Styles, script, logo, app screens and miga-server screenshots |
| `content/` | Privacy policy sources: the same text as `PRIVACY.md` in the app |
| `tools/build.py` | Builds the HTML pages from the texts it holds |
| `tools/screens.py` | Turns the app's screenshots into `assets/img/screens/{es,en}/*.webp` |
| `tools/og.mjs` | Draws `assets/img/og.png`, the preview when the site is shared |

## Editing

```bash
pip install markdown
python3 tools/build.py        # after changing texts in tools/build.py or content/*.md
python3 -m http.server        # preview at http://localhost:8000
```

When the privacy policy changes in the app, copy `PRIVACY.md` to `content/privacy-es.md` and
`app/src/main/assets/docs/privacy-en.md` to `content/privacy-en.md`, then rebuild.

### Real screenshots

The phone screens in `assets/img/screens/{es,en}/` are screenshots of the real app, taken by its
screenshot tests with recipe packs installed. To refresh them, take new screenshots (see the
docstring of `tools/screens.py`), run `python3 tools/screens.py <folder>` (needs Pillow) and
`node tools/og.mjs` (needs Playwright), then rebuild.

### Recipe packs

The packs live in the public repository
[calamares00/miga-packs](https://github.com/calamares00/miga-packs). `packs/catalog.json` is the
`catalog.json` built there, with absolute `downloadUrl` and `coverImageUrl`. The home page shows
the packs of each language with the covers in `assets/img/packs/<id>.jpg` (a copy of
`packs/<id>/cover.jpg` from miga-packs), so the site makes no third-party requests.

### Google Play

While Miga is in closed testing, `PLAY_PUBLIC = False` in `tools/build.py` makes the download
buttons ask people to join the beta by email. Set it to `True` once the app is in production and
the buttons link to its Play Store page.

## Publishing

The site is served at **https://miga.calamares.org** (the `CNAME` file) with GitHub Pages: in the
repository settings, **Pages › Build and deployment**, deploy from the `main` branch, root folder, with
`miga.calamares.org` as the custom domain and HTTPS enforced. The DNS has a `CNAME` record for
`miga.calamares.org` pointing to `calamares00.github.io`.

The app reads the packs catalogue from `https://miga.calamares.org/packs/catalog.json`, and Google
Play links to the privacy policy at `https://miga.calamares.org/privacy/`.

## License

Site code: [GPL-3.0](LICENSE). Product data shown in the app comes from Open Food Facts (ODbL).
