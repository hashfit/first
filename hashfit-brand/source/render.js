const { chromium } = require('playwright-core');
const fs = require('fs'), path = require('path');
const SRC = '/home/user/first/hashfit-brand/svg', DST = '/home/user/first/hashfit-brand/png';
(async () => {
  fs.mkdirSync(DST, { recursive: true });
  const browser = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium-1194/chrome-linux/chrome' });
  for (const f of fs.readdirSync(SRC).filter(f => f.endsWith('.svg'))) {
    const svg = fs.readFileSync(path.join(SRC, f), 'utf8');
    const [, w, h] = svg.match(/width="(\d+)" height="(\d+)"/).map(Number);
    const scale = w < 1200 ? 2 : 1;
    const page = await browser.newPage({ viewport: { width: w, height: h }, deviceScaleFactor: scale });
    await page.setContent(`<html><body style="margin:0;background:transparent">${svg}</body></html>`);
    await page.locator('svg').screenshot({ path: path.join(DST, f.replace('.svg', '.png')), omitBackground: true });
    await page.close();
  }
  await browser.close();
})();
