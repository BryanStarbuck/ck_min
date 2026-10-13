// tour.js: runs one body-part page ({part}.html).
//
// The page holds two <section class="bt-story" data-tab="bullet|charge"> blocks. Each
// <article class="bt-step"> inside one is a card of text plus a
// <script type="application/json" class="bt-scene"> telling the 3D stage what to show
// while that card is the one being read. Scrolling makes the card nearest the reading
// line active; the tabs swap which story is showing.

import { Stage } from './stage.js';
import { mountPartsNav } from './parts.js';

const part = document.body.dataset.part;
mountPartsNav(part);

const host = document.querySelector('[data-bt-stage]');
const stage = new Stage(host, { ariaLabel: host.getAttribute('data-label') || undefined });

// ---- HUD on the stage: step counter, legend, buttons
const hud = document.createElement('div');
hud.className = 'bt-hud';
hud.innerHTML = `
  <div class="bt-legend" aria-hidden="true">
    <span><i class="lg-hit"></i>Reached by this cause</span>
    <span><i class="lg-miss"></i>Not reached</span>
    <span class="lg-b"><i class="lg-path"></i>The State's bullet path</span>
    <span class="lg-c"><i class="lg-charge"></i>Blast and jet</span>
  </div>
  <div class="bt-tools">
    <button type="button" data-act="replay" title="Play this step's animation again">Replay</button>
    <button type="button" data-act="reset" title="Turn the body back to the planned view">Reset view</button>
  </div>`;
host.appendChild(hud);
const count = document.createElement('div');
count.className = 'bt-count';
host.appendChild(count);
const hint = document.createElement('div');
hint.className = 'bt-hint';
hint.textContent = 'Drag to turn the body';
host.appendChild(hint);
hud.querySelector('[data-act="replay"]').addEventListener('click', () => stage.replay());
hud.querySelector('[data-act="reset"]').addEventListener('click', () => { stage.yawTarget = 0; stage.userTurned = false; });

// ---- card-to-body leader line (desktop)
const NS = 'http://www.w3.org/2000/svg';
const lead = document.createElementNS(NS, 'svg');
lead.setAttribute('class', 'bt-card-lead');
lead.setAttribute('aria-hidden', 'true');
const leadPath = document.createElementNS(NS, 'path');
leadPath.setAttribute('pathLength', '1');
const leadDot = document.createElementNS(NS, 'circle');
leadDot.setAttribute('r', '5');
lead.append(leadPath, leadDot);
document.body.appendChild(lead);

// ---- stories, steps, tabs
const stories = Array.from(document.querySelectorAll('.bt-story'));
const tabs = Array.from(document.querySelectorAll('.bt-tab'));
const scenes = new Map();
stories.forEach((st) => st.querySelectorAll('.bt-step').forEach((step, i, all) => {
  const js = step.querySelector('script.bt-scene');
  let sc = {};
  if (js) { try { sc = JSON.parse(js.textContent); } catch (e) { console.warn('[body tour] bad scene JSON in', step.id, e); } }
  scenes.set(step, sc);
  step.dataset.n = String(i + 1);
  step.dataset.of = String(all.length);
  Array.from(step.querySelector('.bt-card').children).forEach((c, k) => c.style.setProperty('--i', k));
}));

let tab = null, active = null;

function selectTab(name, { scroll = true, instant = false } = {}) {
  if (!stories.some((s) => s.dataset.tab === name)) name = stories[0].dataset.tab;
  tab = name;
  stories.forEach((s) => { s.hidden = s.dataset.tab !== name; });
  tabs.forEach((t) => {
    const on = t.dataset.tab === name;
    t.setAttribute('aria-selected', String(on));
    t.tabIndex = on ? 0 : -1;
  });
  document.body.dataset.tab = name;
  hud.querySelector('.lg-b').style.display = name === 'bullet' ? '' : 'none';
  hud.querySelector('.lg-c').style.display = name === 'charge' ? '' : 'none';
  if (history.replaceState) history.replaceState(null, '', '#' + name);
  active = null;
  const story = stories.find((s) => s.dataset.tab === name);
  story.querySelectorAll('.bt-step').forEach((s) => s.classList.remove('is-active', 'was-seen'));
  if (scroll) {
    const top = document.querySelector('.bt-main').getBoundingClientRect().top + window.scrollY - (parseFloat(getComputedStyle(document.documentElement).getPropertyValue('--bar-h')) || 0);
    window.scrollTo({ top: Math.max(0, top), behavior: instant ? 'auto' : 'smooth' });
  }
  pick(true, instant);
}

tabs.forEach((t) => {
  t.addEventListener('click', () => selectTab(t.dataset.tab));
  t.addEventListener('keydown', (e) => {
    if (e.key !== 'ArrowRight' && e.key !== 'ArrowLeft') return;
    const i = tabs.indexOf(t), j = (i + (e.key === 'ArrowRight' ? 1 : -1) + tabs.length) % tabs.length;
    tabs[j].focus(); selectTab(tabs[j].dataset.tab);
  });
});
document.querySelectorAll('[data-goto-tab]').forEach((b) => b.addEventListener('click', (e) => { e.preventDefault(); selectTab(b.dataset.gotoTab); }));

// A step becomes active once the top of its card rises above this line.
function triggerLine() {
  return window.innerWidth <= 900 ? window.innerHeight * 0.8 : window.innerHeight * 0.62;
}

function pick(force = false, instant = false) {
  const story = stories.find((s) => s.dataset.tab === tab);
  if (!story) return;
  const line = triggerLine();
  const steps = Array.from(story.querySelectorAll('.bt-step'));
  let best = steps[0];
  steps.forEach((step) => {
    if (step.querySelector('.bt-card').getBoundingClientRect().top < line) best = step;
  });
  if (!best || (best === active && !force)) return;
  if (active) { active.classList.remove('is-active'); active.classList.add('was-seen'); }
  active = best;
  active.classList.add('is-active');
  const sc = scenes.get(active) || {};
  stage.setScene(sc, { instant });
  count.innerHTML = `<b>${active.dataset.n}</b> / ${active.dataset.of}`;
  leadPath.classList.remove('is-in'); leadDot.classList.remove('is-in');
  void leadPath.getBoundingClientRect();
  leadPath.classList.add('is-in'); leadDot.classList.add('is-in');
  const color = tab === 'charge' ? 'var(--charge)' : 'var(--bullet)';
  leadPath.style.stroke = color; leadDot.style.fill = color;
}

let ticking = false;
window.addEventListener('scroll', () => {
  if (ticking) return;
  ticking = true;
  requestAnimationFrame(() => { ticking = false; pick(); });
}, { passive: true });
window.addEventListener('resize', () => pick(true, true));
window.addEventListener('hashchange', () => {
  const h = location.hash.slice(1);
  if ((h === 'bullet' || h === 'charge') && h !== tab) selectTab(h);
});

// Each frame, bend a line from the active card's edge to the point it talks about.
stage.onFrame = () => {
  if (!active || window.innerWidth <= 900) { lead.style.opacity = '0'; return; }
  const sc = scenes.get(active) || {};
  const anchor = sc.point || (sc.labels && sc.labels[0] && sc.labels[0][0]);
  const p = anchor && stage.anchorClient(anchor);
  const card = active.querySelector('.bt-card').getBoundingClientRect();
  const vis = card.bottom > 80 && card.top < window.innerHeight - 40;
  if (!p || !p.inView || !vis) { lead.style.opacity = '0'; return; }
  lead.style.opacity = '1';
  // End at the point's own label when it has one (card -> label -> body), else at the point.
  let tx = p.x, ty = p.y;
  const box = stage.labelBox(anchor);
  if (box && box.right < card.left) { tx = box.right; ty = box.top + box.height / 2; }
  const x1 = card.left - 2, y1 = Math.min(Math.max(card.top + 34, ty), card.bottom - 30);
  const mx = (x1 + tx) / 2;
  leadPath.setAttribute('d', `M${x1},${y1} C${mx},${y1} ${mx},${ty} ${tx},${ty}`);
  leadDot.setAttribute('cx', tx); leadDot.setAttribute('cy', ty);
};

const start = location.hash.slice(1);
selectTab(start === 'charge' ? 'charge' : 'bullet', { scroll: false, instant: true });
