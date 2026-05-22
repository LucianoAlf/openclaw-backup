#!/usr/bin/env node
import fs from 'node:fs';
import path from 'node:path';
import { chromium } from '/root/.openclaw/workspace/repos/open-design/node_modules/.pnpm/playwright@1.60.0/node_modules/playwright/index.mjs';

const args = Object.fromEntries(process.argv.slice(2).map((a, i, arr) => {
  if (!a.startsWith('--')) return [];
  const k = a.slice(2);
  const v = arr[i + 1] && !arr[i + 1].startsWith('--') ? arr[i + 1] : 'true';
  return [k, v];
}).filter(Boolean));

const brand = args.brand || 'school';
const prompt = args.prompt;
if (!prompt) {
  console.error('Missing --prompt');
  process.exit(2);
}

const cfg = {
  school: { ds: 'user:la-music-school', title: 'LA Music School · Open Design real run' },
  kids: { ds: 'user:la-music-kids', title: 'LA Music Kids · Open Design real run' },
  sonoramente: { ds: 'user:la-music-sonoramente', title: 'SonoraMente LA · Open Design real run' },
}[brand];
if (!cfg) throw new Error(`Unsupported --brand ${brand}`);

const base = args.base || 'http://127.0.0.1:17456';
const outRoot = args.out || `/root/.openclaw/workspace/outputs/opendesign-lahq-${brand}-${Date.now()}`;
fs.mkdirSync(outRoot, { recursive: true });

function slug() {
  return 'lahq-od-real-' + Date.now().toString(36) + '-' + Math.random().toString(36).slice(2, 8);
}
async function json(url, opts = {}) {
  const r = await fetch(url, { ...opts, headers: { 'Content-Type': 'application/json', ...(opts.headers || {}) } });
  const t = await r.text();
  let d;
  try { d = JSON.parse(t); } catch { d = { raw: t }; }
  if (!r.ok) throw new Error(`${opts.method || 'GET'} ${url} ${r.status}: ${t}`);
  return d;
}

const id = args.projectId || slug();
const created = await json(`${base}/api/projects`, {
  method: 'POST',
  body: JSON.stringify({
    id,
    name: cfg.title,
    skillId: args.skill || 'la-music-carousel',
    designSystemId: cfg.ds,
    pendingPrompt: prompt,
    metadata: { kind: 'freeform', intent: 'lahq-open-design-skill-run' },
    skipDiscoveryBrief: true,
  }),
});
const conversationId = created.conversationId;
fs.writeFileSync(path.join(outRoot, 'project-create.json'), JSON.stringify(created, null, 2));

const runCreated = await json(`${base}/api/runs`, {
  method: 'POST',
  headers: { 'X-OD-Client': 'web' },
  body: JSON.stringify({
    agentId: args.agent || 'codex',
    message: prompt,
    currentPrompt: prompt,
    projectId: id,
    conversationId,
    assistantMessageId: null,
    clientRequestId: crypto.randomUUID(),
    skillId: args.skill || 'la-music-carousel',
    skillIds: [],
    designSystemId: cfg.ds,
    attachments: [],
    commentAttachments: [],
    model: args.model || 'gpt-5.5',
    reasoning: null,
  }),
});
const runId = runCreated.runId;
fs.writeFileSync(path.join(outRoot, 'run-create.json'), JSON.stringify(runCreated, null, 2));
console.log(JSON.stringify({ event: 'started', brand, projectId: id, runId, outRoot }));

let finalStatus = 'unknown';
for (let i = 0; i < Number(args.maxTicks || 180); i++) {
  await new Promise(r => setTimeout(r, Number(args.intervalMs || 5000)));
  const st = await json(`${base}/api/runs/${runId}`).catch(e => ({ error: String(e) }));
  const files = await json(`${base}/api/projects/${id}/files`).catch(e => ({ files: [], error: String(e) }));
  finalStatus = st.status || st.run?.status || st.value || 'unknown';
  fs.writeFileSync(path.join(outRoot, 'last-status.json'), JSON.stringify({ status: st, files }, null, 2));
  const paths = (files.files || []).map(f => f.path || f.name || '');
  console.log(JSON.stringify({ event: 'tick', i, status: finalStatus, files: paths }));
  if (['succeeded', 'failed', 'canceled', 'cancelled'].includes(String(finalStatus))) break;
}

const filesNow = await json(`${base}/api/projects/${id}/files`).catch(() => ({ files: [] }));
const html = (filesNow.files || []).map(f => f.path || f.name).find(p => p === 'index.html')
  || (filesNow.files || []).map(f => f.path || f.name).find(p => String(p).endsWith('.html'));
if (html) {
  const browser = await chromium.launch({ headless: true, executablePath: '/usr/bin/google-chrome-stable', args: ['--no-sandbox'] });
  const page = await browser.newPage({ viewport: { width: 1080, height: 1350 }, deviceScaleFactor: 1 });
  await page.goto(`${base}/api/projects/${id}/raw/${html}`, { waitUntil: 'networkidle', timeout: 60000 });
  await page.screenshot({ path: path.join(outRoot, 'agent-output-1080x1350.png'), fullPage: false });
  const check = await page.evaluate(() => ({
    w: document.documentElement.scrollWidth,
    h: document.documentElement.scrollHeight,
    text: document.body.innerText,
    imgs: [...document.images].map(i => ({ src: i.getAttribute('src'), ok: i.complete, w: i.naturalWidth, h: i.naturalHeight })),
    fonts: [...document.fonts].map(f => ({ family: f.family, status: f.status, weight: f.weight })),
  }));
  fs.writeFileSync(path.join(outRoot, 'render-check.json'), JSON.stringify(check, null, 2));
  await browser.close();
}
fs.writeFileSync(path.join(outRoot, 'summary.json'), JSON.stringify({ brand, projectId: id, runId, status: finalStatus, html, outRoot }, null, 2));
console.log(JSON.stringify({ event: 'done', brand, projectId: id, runId, status: finalStatus, html, outRoot }));
