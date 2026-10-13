// parts.js: the one list of Body Tour pages. The top-bar menu on every {part}.html is
// built from this list, so adding a part here (plus its page) puts it in every menu.
// The static list on body_tour.html is written by hand; keep it in the same order.

export const ICONS = {
  neck: '<circle cx="12" cy="6.6" r="3.9"/><path d="M9.6 10v4.4c0 1.2-1.6 2.4-5 4M14.4 10v4.4c0 1.2 1.6 2.4 5 4"/><path d="M13.9 13.3l-1.6.9"/>',
  brain: '<path d="M9 4.5a3 3 0 0 0-3 3 3 3 0 0 0-1.6 5.3A3 3 0 0 0 7 17.6a2.5 2.5 0 0 0 5 .4V5.6A2.4 2.4 0 0 0 9 4.5Z"/><path d="M15 4.5a3 3 0 0 1 3 3 3 3 0 0 1 1.6 5.3 3 3 0 0 1-2.6 4.8 2.5 2.5 0 0 1-5 .4"/><path d="M8.2 9.6c.9.2 1.6.9 1.8 1.8M15.8 9.6c-.9.2-1.6.9-1.8 1.8"/>',
  heart: '<path d="M12 20s-7-4.4-7-10.1A4 4 0 0 1 12 7.3a4 4 0 0 1 7 2.6C19 15.6 12 20 12 20Z"/><path d="M9.5 10.5h2l1-2 1.2 4 .8-2h1.5"/>',
  lungs: '<path d="M12 3.5v8.5M12 12l-2.4 2.1M12 12l2.4 2.1"/><path d="M9.2 8.2C6.1 8.4 4 13 4 17c0 1.8 1.3 2.6 2.7 2.1l2.9-1.2v-8.3c0-.6-.1-1.1-.4-1.4Z"/><path d="M14.8 8.2c3.1.2 5.2 4.8 5.2 8.8 0 1.8-1.3 2.6-2.7 2.1l-2.9-1.2v-8.3c0-.6.1-1.1.4-1.4Z"/>',
  spine: '<rect x="9" y="2.8" width="6" height="3.1" rx="1.2"/><rect x="8.4" y="7.4" width="7.2" height="3.1" rx="1.2"/><rect x="8.4" y="12" width="7.2" height="3.1" rx="1.2"/><rect x="9" y="16.6" width="6" height="3.1" rx="1.2"/><path d="M12 5.9v1.5M12 10.5V12M12 15.1v1.5M12 19.7v1.6"/>',
  back: '<path d="M15 5l-7 7 7 7"/>',
  next: '<path d="M9 5l7 7-7 7"/>',
  body: '<circle cx="12" cy="4.6" r="2.4"/><path d="M8 21v-6.5L6.5 9.6c-.3-1 .4-1.9 1.4-1.9h8.2c1 0 1.7.9 1.4 1.9L16 14.5V21"/>',
};

export function icon(name, cls = '') {
  return `<svg class="${cls}" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">${ICONS[name] || ''}</svg>`;
}

// key: page file name without .html. organs/findings: what lights up for this part on the
// body_tour.html figure. anchor: where its hotspot sits. cam: the close-up shot used there.
export const PARTS = [
  {
    key: 'neck', label: 'Neck', file: 'neck.html',
    words: '"complex entrance gunshot wound"; the left neck vessels "sequentially perforated"; "multiple disruptions of the thyroid, cricoid, and tracheal cartilages"',
    short: 'Entry wound, the four left-side vessels and muscles in order, the voice box and windpipe',
    lean: 'Fits either; the order runs sideways',
    organs: ['larynx', 'trachea', 'carotidL', 'jugularIL', 'jugularEL', 'strapL'],
    findings: ['entry', 'strap', 'carotid', 'ijv', 'ejv', 'cartilages'],
    anchor: 'entry', cam: 'neck-front-left',
  },
  {
    key: 'brain', label: 'Brain', file: 'brain.html',
    words: 'Subarachnoid bleeding around "the cerebellar vermis and the parietal regions"',
    short: 'Bleeding on the surface of the brain: low at the back, and at the top',
    lean: 'Top of the brain leans blast',
    organs: ['brain', 'cerebellum', 'brainstem'],
    findings: ['vermis', 'parietal'],
    anchor: 'parietalL', cam: 'head-left',
  },
  {
    key: 'heart', label: 'Heart', file: 'heart.html',
    words: '"hemopericardium"',
    short: 'Blood inside the sac around the heart',
    lean: 'Leans blast',
    organs: ['heart', 'pericardium', 'aorta'],
    findings: ['hemopericardium'],
    anchor: 'sac', cam: 'heart-front-left',
  },
  {
    key: 'lungs', label: 'Lungs', file: 'lungs.html',
    words: '"left and right hemothorax"; "bilateral apical and posterior intercostal hemorrhages, pulmonary apical hemorrhages/hematomas"',
    short: 'Blood in both chest cavities, bleeding between the ribs on both sides, bleeding in the tops of the lungs',
    lean: 'Both sides lean blast',
    organs: ['lungL', 'lungR', 'ribs'],
    findings: ['hemothoraxL', 'hemothoraxR', 'intercostalL', 'intercostalR', 'apexL', 'apexR'],
    anchor: 'lungR', cam: 'chest-front-left',
  },
  {
    key: 'spine', label: 'Spine', file: 'spine.html',
    words: '"obliterate[ed] the left side of the C2-7 vertebrae and transect[ed] the cervical spinal cord"; a "significant portion" of the cord "traumatically absent"',
    short: 'Six neck bones destroyed on the left; the spinal cord cut, with a length of it missing',
    lean: 'Six bones lean blast; the cut cord fits either',
    organs: ['spine', 'cord'],
    findings: ['c2c7', 'cord'],
    anchor: 'c2', cam: 'spine-long-left',
  },
];

export function partByKey(k) { return PARTS.find((p) => p.key === k); }

// Fills <nav data-bt-parts> in the top bar: pills on wide screens, a menu on narrow ones.
export function mountPartsNav(current) {
  const host = document.querySelector('[data-bt-parts]');
  if (!host) return;
  const pills = PARTS.map((p) => `<a href="${p.file}"${p.key === current ? ' aria-current="page"' : ''}>${icon(p.key)}${p.label}</a>`).join('');
  const cur = partByKey(current);
  host.innerHTML = `
    <div class="bt-parts" role="list">${pills}</div>
    <div class="bt-parts-menu">
      <button type="button" aria-haspopup="true" aria-expanded="false">${cur ? cur.label : 'Body parts'} <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" aria-hidden="true"><path d="M6 9l6 6 6-6"/></svg></button>
      <div class="bt-pop">${PARTS.map((p) => `<a href="${p.file}"${p.key === current ? ' aria-current="page"' : ''}>${icon(p.key)}${p.label}</a>`).join('')}<a href="body_tour.html">${icon('body')}All body parts</a></div>
    </div>`;
  const menu = host.querySelector('.bt-parts-menu');
  const btn = menu.querySelector('button');
  btn.addEventListener('click', (e) => {
    e.stopPropagation();
    const open = !menu.classList.contains('open');
    menu.classList.toggle('open', open);
    btn.setAttribute('aria-expanded', String(open));
  });
  document.addEventListener('click', () => { menu.classList.remove('open'); btn.setAttribute('aria-expanded', 'false'); });
  document.addEventListener('keydown', (e) => { if (e.key === 'Escape') { menu.classList.remove('open'); btn.setAttribute('aria-expanded', 'false'); } });
}
