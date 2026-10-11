// Offline threshold check (no browser, no app, no network). Task 5.1 in the README.
// Builds two synthetic 400x250 PNGs that differ in one 15x15 square, then runs the plugin's REAL compare
// function (cypress-visual-regression 5.3.0) with several errorThreshold values.
// Usage (after `npm install`):  npm run check:threshold
const { PNG } = require('pngjs');
const fs = require('fs'), os = require('os'), path = require('path');
const { compareSnapshots } = require('cypress-visual-regression');

const root = fs.mkdtempSync(path.join(os.tmpdir(), 'vr-'));
const spec = { relative: 'threshold-check.js' };
function image(w, h, squareColour) {
  const p = new PNG({ width: w, height: h });
  for (let y = 0; y < h; y++) for (let x = 0; x < w; x++) {
    const i = (y * w + x) * 4, c = x < 15 && y < 15 ? squareColour : [240, 240, 240];
    p.data[i] = c[0]; p.data[i + 1] = c[1]; p.data[i + 2] = c[2]; p.data[i + 3] = 255;
  }
  return PNG.sync.write(p);
}
fs.mkdirSync(path.join(root, 'base', spec.relative), { recursive: true });
fs.mkdirSync(path.join(root, 'actual'), { recursive: true });
fs.writeFileSync(path.join(root, 'base', spec.relative, 'card.png'), image(400, 250, [0, 0, 255]));
fs.writeFileSync(path.join(root, 'actual', 'card.png'), image(400, 250, [255, 0, 0]));

(async () => {
  console.log('Image: 400 x 250 = 100000 px; changed square: 15 x 15 = 225 px');
  for (const t of [0.5, 0.005, 0.001, 0]) {
    const r = await compareSnapshots({
      screenshotName: 'card', screenshotAbsolutePath: path.join(root, 'actual', 'card.png'),
      baseDirectory: path.join(root, 'base'), diffDirectory: path.join(root, 'diff'),
      spec, retryAttempt: 0, generateDiff: 'fail',
      pluginOptions: { errorThreshold: t, pixelmatchOptions: { threshold: 0.1 } },
    });
    console.log(`errorThreshold ${String(t).padEnd(6)} -> mismatched ${r.mismatchedPixels}, fraction ${r.percentage}, test FAILS: ${!!r.error}`);
  }
  fs.rmSync(root, { recursive: true, force: true });
})();
