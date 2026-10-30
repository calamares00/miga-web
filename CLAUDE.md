# Miga website

Static site for https://miga.calamares.org (GitHub Pages, `CNAME`), in Spanish (`/`) and English
(`/en/`).

## Conventions

- Commits, pull requests, code comments and technical docs are written in **English**. Site texts
  stay in Spanish and English.
- Do not edit the generated HTML by hand: change `tools/build.py` (texts of both languages live
  there) or `content/*.md`, then run `python3 tools/build.py` (needs the `markdown` package) and
  commit the regenerated pages together with the source change.
- `calamares00/miga-app` and `calamares00/miga-server` are private: the site must not link to
  them, offer APK downloads or mention source code. Only `calamares00/miga-packs` is public.
- `PLAY_PUBLIC` in `tools/build.py` switches the download buttons from "join the beta" (email)
  to the Play Store page.
- `content/privacy-es.md` and `content/privacy-en.md` are the privacy policy linked from Google
  Play. Keep them identical to `PRIVACY.md` and `app/src/main/assets/docs/privacy-*.md` in
  `calamares00/miga-app`.
- `assets/img/screens/*.svg` are drawn by `tools/mockups.py` with the app's "Huerta" colours.

## Recipe pack catalogue

`packs/catalog.json` is the app's default catalogue. It is the `catalog.json` built in
`calamares00/miga-packs`, with `downloadUrl` and `coverImageUrl` made absolute
(`https://raw.githubusercontent.com/calamares00/miga-packs/main/...`). Update it whenever a pack
is added or its version changes there, and copy its `cover.jpg` to `assets/img/packs/<id>.jpg`
(the build fails without it).
