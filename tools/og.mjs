// Draws assets/img/og.png (the 1200x630 preview shown when the site is shared) from the real
// screenshots in assets/img/screens/es. Needs Playwright with Chromium:
//
//     node tools/og.mjs
import { chromium } from 'playwright';
import { fileURLToPath } from 'node:url';
import path from 'node:path';
import { readFileSync } from 'node:fs';

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
// Inlined: a page set from a string cannot load local files.
const screen = name => 'data:image/webp;base64,' + readFileSync(path.join(root, 'assets/img/screens/es', name + '.webp')).toString('base64');
const html = `<!doctype html><html><head><meta charset="utf-8"><style>
  body { margin: 0; width: 1200px; height: 630px; overflow: hidden; font-family: system-ui, sans-serif;
         background: radial-gradient(circle at 85% 20%, #1f3a2c 0, #0f1310 60%); color: #e8ede9; }
  .text { position: absolute; left: 64px; top: 150px; width: 560px; }
  .chip { display: inline-block; background: #1d3527; color: #a8dcbf; font-weight: 700; font-size: 22px;
          padding: 8px 18px; border-radius: 999px; }
  h1 { font-size: 76px; line-height: 1.04; margin: 26px 0 0; font-weight: 800; letter-spacing: -1px; }
  h1 em { font-style: normal; color: #6bbf93; }
  .phone { position: absolute; width: 270px; padding: 9px; border-radius: 38px; background: #050706;
           box-shadow: 0 30px 60px rgba(0,0,0,.55), 0 0 0 1.5px #2a312c inset; }
  .phone img { width: 100%; display: block; border-radius: 30px; aspect-ratio: 360 / 781; object-fit: cover; object-position: top; }
  .back { left: 690px; top: 120px; transform: rotate(-6deg); opacity: .92; }
  .front { left: 890px; top: 40px; transform: rotate(4deg); }
</style></head><body>
  <div class="text"><span class="chip">Android · Sin cuentas ni anuncios</span>
  <h1>Tus recetas.<br>Tus libros. <em>Tu cocina.</em></h1></div>
  <div class="phone back"><img src="${screen('books')}"></div>
  <div class="phone front"><img src="${screen('recipe')}"></div>
</body></html>`;

const browser = await chromium.launch();
const page = await browser.newPage({ viewport: { width: 1200, height: 630 } });
await page.setContent(html, { waitUntil: 'load' });
await page.screenshot({ path: path.join(root, 'assets/img/og.png') });
await browser.close();
