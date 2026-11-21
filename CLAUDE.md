# Miga website

Static site for https://miga.calamares.org (GitHub Pages, `CNAME`), in Spanish (`/`) and English
(`/en/`). A short home page plus one page per section (`PAGES` in `tools/build.py`: features,
health, assistant, family/sync, packs, FAQ), each with breadcrumb, previous/next links and the
download block (`#descargar` / `#download`). Anchors of the old one-page site (`#salud`...) are
sent to their page by `assets/main.js` (`LEGACY_ANCHORS`).

## Conventions

- Commits, pull requests, code comments and technical docs are written in **English**. Site texts
  stay in Spanish and English.
- Do not edit the generated HTML by hand: change `tools/build.py` (texts of both languages live
  there) or `content/*.md`, then run `python3 tools/build.py` (needs the `markdown` package) and
  commit the regenerated pages together with the source change.
- `calamares00/miga-app` is private: the site must not link to it, offer APK downloads or call
  the app open source. `calamares00/miga-server` and `calamares00/miga-packs` are public.
- `PLAY_PUBLIC` in `tools/build.py` switches the download buttons from "join the beta" (email)
  to the Play Store page.
- `content/privacy-es.md` and `content/privacy-en.md` are the privacy policy linked from Google
  Play. Keep them identical to `PRIVACY.md` and `app/src/main/assets/docs/privacy-*.md` in
  `calamares00/miga-app`.
- `assets/img/screens/{es,en}/*.webp` are real screenshots of the app: `StoreShotsEsTest` and
  `StoreShotsEnTest` in `calamares00/miga-app` install recipe packs from miga-packs and drive the
  app's interface; `tools/screens.py` turns their PNGs into these WebP files (see its docstring).
  `assets/img/og.png`, the preview when the site is shared, is drawn from them by `tools/og.mjs`
  (Playwright).

## Recipe pack catalogue

`packs/catalog.json` is the app's default catalogue. It is the `catalog.json` built in
`calamares00/miga-packs`, with `downloadUrl` and `coverImageUrl` made absolute
(`https://raw.githubusercontent.com/calamares00/miga-packs/main/...`). Update it whenever a pack
is added or its version changes there, and copy its `cover.jpg` to `assets/img/packs/<id>.jpg`
(the build fails without it).

## OpenRouter return page

`openrouter/index.html` is hand-written (not built by `tools/build.py`): the `callback_url` of the
app's "Connect with OpenRouter" (OAuth PKCE). It hands `?code=` to the app (`miga://openrouter`)
and shows it to paste by hand. Keep it out of the sitemap.
