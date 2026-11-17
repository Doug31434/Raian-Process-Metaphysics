# BWTC Render Toolkit — Nov 3 2026

Companion to `claude/bwtc_3d_centers_render.html` (the render source, saved as render.html). These are the helper scripts that turn it into 1000px transparent PNGs. Rebuild in a fresh session:

```
mkdir -p r3d/out && cd r3d && npm init -y && npm install three@0.160.0
# save render.html, shoot.js, shoot_layers.js, composite.py, bloom.py here
python3 -m http.server 8765 &   # run_in_background
node shoot.js green && python3 bloom.py green                         # single-pass forms: orange, green
node shoot_layers.js red && python3 composite.py red                  # layered forms: red, yellow
```

Playwright and Chromium are preinstalled in the cloud workspace (require("playwright") works; do not reinstall).

## shoot.js

```
const { chromium } = require('playwright');
(async () => {
  const forms = (process.argv[2] || 'red,orange,yellow,green,blue,indigo,violet').split(',');
  const browser = await chromium.launch({ args: ['--use-gl=angle', '--use-angle=swiftshader', '--enable-unsafe-swiftshader'] });
  const page = await browser.newPage({ viewport: { width: 1000, height: 1000 } });
  page.on('console', m => console.log('console:', m.text()));
  page.on('pageerror', e => console.log('error:', e.message));
  for (const f of forms) {
    await page.goto(`http://localhost:8765/render.html?form=${f}&size=1000`);
    await page.waitForSelector('body[data-done="1"]', { timeout: 60000 });
    await page.locator('canvas').screenshot({ path: `out/${f}.png`, omitBackground: true });
    console.log('rendered', f);
  }
  await browser.close();
})();
```

## shoot_layers.js

```
const { chromium } = require('playwright');
(async () => {
  const browser = await chromium.launch({ args: ['--use-gl=angle', '--use-angle=swiftshader', '--enable-unsafe-swiftshader'] });
  const page = await browser.newPage({ viewport: { width: 1000, height: 1000 } });
  page.on('pageerror', e => console.log('error:', e.message));
  for (const layer of ['shell','back','front']) {
    await page.goto(`http://localhost:8765/render.html?form=${process.argv[2]||'red'}&size=1000&layer=${layer}`);
    await page.waitForSelector('body[data-done="1"]', { timeout: 60000 });
    await page.locator('canvas').screenshot({ path: `out/${process.argv[2]||'red'}_${layer}.png`, omitBackground: true });
  }
  await browser.close();
})();
```

## composite.py

```
import sys
from PIL import Image, ImageFilter
f=sys.argv[1]
L={k:Image.open(f'out/{f}_{k}.png').convert('RGBA') for k in ['shell','back','front']}
def bloom(im, r, k):
    b=im.filter(ImageFilter.GaussianBlur(r)); b.putalpha(b.getchannel('A').point(lambda v:int(v*k))); return Image.alpha_composite(b, im)
back=bloom(L['back'].filter(ImageFilter.GaussianBlur(3.2)), 8, 0.45)
front=bloom(L['front'], 6, 0.55)
out=Image.alpha_composite(Image.alpha_composite(L['shell'], back), front)
out.save(f'out/{f}.png')
sh=Image.new('RGB',(600,600),(245,239,224)); v=out.resize((600,600)); sh.paste(v,(0,0),v); sh.save(f'out/{f}_view.png')
```

## bloom.py (single-pass forms)

```
import sys
from PIL import Image, ImageFilter
f=sys.argv[1]
im=Image.open(f'out/{f}.png').convert('RGBA')
b=im.filter(ImageFilter.GaussianBlur(6)); b.putalpha(b.getchannel('A').point(lambda v:int(v*0.5)))
out=Image.alpha_composite(b, im); out.save(f'out/{f}.png')
sh=Image.new('RGB',(600,600),(245,239,224)); v=out.resize((600,600)); sh.paste(v,(0,0),v); sh.save(f'out/{f}_view.png')
```
