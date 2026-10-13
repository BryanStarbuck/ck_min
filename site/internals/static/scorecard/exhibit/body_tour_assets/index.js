// index.js: runs body_tour.html, the Body Tour contents page. The 3D figure shows every
// Exhibit 11 finding at once; pointing at a body part (in the list or on the figure) turns
// the camera to that part and lights it up. Clicking goes to that part's page.

import { Stage } from './stage.js';
import { PARTS, mountPartsNav } from './parts.js';

mountPartsNav(null);

const host = document.querySelector('[data-bt-stage]');
const stage = new Stage(host, { autoRotate: true, ariaLabel: host.getAttribute('data-label') || undefined });

const every = {};
PARTS.forEach((p) => p.findings.forEach((f) => { every[f] = 'on'; }));
const base = {
  cam: 'hero',
  show: ['neckVessels', 'larynx', 'trachea', 'lungs', 'heart', 'aorta', 'brainAll', 'spine', 'cord'],
  findings: every,
};
stage.setScene(base, { instant: true });

// hotspots that sit on the figure
const layer = document.createElement('div');
layer.className = 'bt-labels';
host.appendChild(layer);
const spots = PARTS.map((p) => {
  const a = document.createElement('a');
  a.className = 'bt-hotspot';
  a.href = p.file;
  a.dataset.part = p.key;
  a.setAttribute('aria-label', p.label + ': open the ' + p.label.toLowerCase() + ' page');
  a.innerHTML = `<span>${p.label}</span>`;
  layer.appendChild(a);
  return { p, a };
});
stage.onFrame = () => {
  const r = host.getBoundingClientRect();
  spots.forEach(({ p, a }) => {
    const c = stage.anchorClient(p.anchor);
    if (!c) return;
    a.style.transform = `translate(${Math.round(c.x - r.left)}px, ${Math.round(c.y - r.top)}px)`;
  });
};

// pointing at a part
const rows = Array.from(document.querySelectorAll('.bt-partlist a[data-part]'));
let timer = null, hot = null;
function focusPart(key) {
  clearTimeout(timer);
  if (hot === key) return;
  hot = key;
  const p = PARTS.find((x) => x.key === key);
  if (!p) return;
  const findings = {};
  p.findings.forEach((f) => { findings[f] = 'hit'; });
  stage.autoRotate = false;
  stage.setScene({ cam: p.cam, show: base.show, focus: p.organs, findings, skin: 0.8 });
  rows.forEach((r) => r.classList.toggle('is-hot', r.dataset.part === key));
  spots.forEach(({ a }) => a.classList.toggle('is-hot', a.dataset.part === key));
}
function release() {
  clearTimeout(timer);
  timer = setTimeout(() => {
    hot = null;
    stage.autoRotate = true;
    stage.userTurned = false;
    stage.setScene(base);
    rows.forEach((r) => r.classList.remove('is-hot'));
    spots.forEach(({ a }) => a.classList.remove('is-hot'));
  }, 900);
}
[...rows, ...spots.map((s) => s.a)].forEach((el) => {
  el.addEventListener('mouseenter', () => focusPart(el.dataset.part));
  el.addEventListener('focus', () => focusPart(el.dataset.part));
  el.addEventListener('mouseleave', release);
  el.addEventListener('blur', release);
});
