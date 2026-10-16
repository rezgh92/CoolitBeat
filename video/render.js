#!/usr/bin/env node
/* Deterministic frame renderer: drives scene.html in headless Chromium (SwiftShader WebGL) and writes one JPEG per frame.
   usage: node render.js --url http://127.0.0.1:8765/scene.html --out frames --start 0 --end 1000 [--fps 30] [--quality 93]
   Frames are numbered globally so several workers can split the range and ffmpeg reads them in order. */
const { chromium } = require('playwright');
const fs = require('fs'); const path = require('path');
const args = Object.fromEntries(process.argv.slice(2).reduce((a, v, i, arr) => { if (v.startsWith('--')) a.push([v.slice(2), arr[i + 1]]); return a; }, []));
const url = args.url || 'http://127.0.0.1:8765/scene.html';
const out = args.out || 'frames'; fs.mkdirSync(out, { recursive: true });
const fps = +(args.fps || 30); const start = +(args.start || 0); const end = +(args.end || 0); const quality = +(args.quality || 93);
const probe = args.probe ? args.probe.split(',').map(Number) : null;   // explicit frame list for contact sheets
(async () => {
  const b = await chromium.launch({ args: ['--use-gl=angle', '--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--ignore-gpu-blocklist', '--disable-dev-shm-usage'] });
  const p = await b.newPage({ viewport: { width: 1920, height: 1080 }, deviceScaleFactor: 1 });
  p.on('console', m => { if (m.type() === 'error' || /ERR|warn/i.test(m.text())) console.log('page:', m.text()); });
  p.on('pageerror', e => console.log('pageerror:', e.message));
  await p.goto(url, { waitUntil: 'load' });
  await p.waitForFunction(() => window.ready === true, null, { timeout: 300000 });
  const list = probe || Array.from({ length: end - start }, (_, i) => start + i);
  const t0 = Date.now();
  for (let k = 0; k < list.length; k++) {
    const f = list[k]; const file = path.join(out, String(f).padStart(6, '0') + '.jpg');
    if (!probe && fs.existsSync(file)) continue;
    await p.evaluate(t => window.renderFrame(t), f / fps);
    await p.screenshot({ path: file, type: 'jpeg', quality });
    if (k % 50 === 0) console.log(`frame ${f} (${k + 1}/${list.length}) ${((Date.now() - t0) / 1000).toFixed(0)} s`);
  }
  await b.close();
  console.log('done', list.length, 'frames in', ((Date.now() - t0) / 1000).toFixed(0), 's');
})().catch(e => { console.error('ERR', e.stack || e.message); process.exit(1); });
