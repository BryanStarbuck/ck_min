#!/usr/bin/env node
// Generates images/images.yaml (formerly hierarchy_images.yaml) from inventory.tsv + the CLUSTERS merge map.
// Mirror dir depth maps to page level:  depth1 -> level_3, depth2 -> level_4, depth3 -> level_5, depth4 -> level_6.
// The merge map re-parents small/related top-level mirror dirs under a real concept cluster.
'use strict';
const fs = require('fs');
const path = require('path');
const os = require('os');

const SCRATCH = __dirname;
const SIDE = path.join(os.homedir(), 'BGit/Bryan_git/personal_large_files_bridge/_Mirror/Politics/Charlie_Kirk_Mi');
const CLUSTERS = require('./clusters.json'); // { title, key, members:[mirrorDirPrefix,...] }

// ---------- load inventory ----------
const rows = fs.readFileSync(path.join(SCRATCH, 'inventory.tsv'), 'utf8')
  .split('\n').slice(1).filter(Boolean)
  .map(l => { const [sha256, dir, filename, orig_path, has_desc] = l.split('\t'); return { sha256, dir, filename, orig_path, has_desc }; });

// ---------- read an ai_description sidecar, return the description body ----------
function readDesc(relPath) {
  const p = path.join(SIDE, relPath + '.ai_description');
  if (!fs.existsSync(p)) return '';
  const raw = fs.readFileSync(p, 'utf8');
  const i = raw.indexOf('description:');
  if (i === -1) return '';
  // strip the YAML block scalar header, de-indent, collapse to a single paragraph
  let body = raw.slice(i).replace(/^description:\s*[>|][-+]?\s*\n?/, '');
  body = body.split('\n').map(s => s.replace(/^ {2}/, '')).join('\n').trim();
  const overview = body.replace(/^##\s*Overview\s*\n/i, '').split(/\n##\s/)[0].trim();
  return overview.replace(/\s+/g, ' ').trim();
}

// ---------- assign every image to a cluster path ----------
const memberToCluster = [];
for (const c of CLUSTERS) for (const m of c.members) memberToCluster.push({ prefix: m, cluster: c });
memberToCluster.sort((a, b) => b.prefix.length - a.prefix.length); // longest prefix wins

function clusterFor(dir) {
  for (const { prefix, cluster } of memberToCluster) {
    if (dir === prefix || dir.startsWith(prefix + '/')) return { cluster, rest: dir.slice(prefix.length).replace(/^\//, '') };
  }
  return null;
}

const tree = new Map(); // key -> node
function nodeAt(pathSegs, titles) {
  let cur = tree, node = null;
  for (let i = 0; i < pathSegs.length; i++) {
    const seg = pathSegs[i];
    if (!cur.has(seg)) cur.set(seg, { title: titles[i], _key: null, seg, images: [], children: new Map() });
    node = cur.get(seg);
    cur = node.children;
  }
  return node;
}

// Collapse redundant copies: same sha256 filed twice in the SAME dir ("foo (1).png" beside "foo.png").
// Cross-filed images — same sha256 in DIFFERENT concept dirs — are deliberate and stay in every cluster.
const seenInDir = new Set();
let collapsed = 0;
const deduped = rows.filter(r => {
  const k = r.sha256 + '\t' + r.dir;
  if (seenInDir.has(k)) { collapsed++; return false; }
  seenInDir.add(k); return true;
});

// Which shas legitimately live in more than one concept dir — recorded on each entry so a later
// pass can see the image is load-bearing for several concepts at once.
const dirsBySha = new Map();
for (const r of deduped) {
  if (!dirsBySha.has(r.sha256)) dirsBySha.set(r.sha256, new Set());
  dirsBySha.get(r.sha256).add(r.dir);
}

const unassigned = [];
for (const r of deduped) {
  const hit = clusterFor(r.dir);
  if (!hit) { unassigned.push(r); continue; }
  const segs = [hit.cluster.key];
  const titles = [hit.cluster.title];
  if (hit.rest) for (const s of hit.rest.split('/')) { segs.push(s); titles.push(s.replace(/_/g, ' ').trim()); }
  const node = nodeAt(segs, titles);
  node.images.push(r);
}

// ---------- unique _key generation (unique across the whole file) ----------
const used = new Set();
function mkKey(seg, parentKey) {
  let base = seg.replace(/[^A-Za-z0-9_]+/g, '_').replace(/^_+|_+$/g, '');
  base = base.split('_').filter(Boolean).slice(0, 4).join('_');
  if (!base) base = 'Node';
  let k = base;
  if (used.has(k) && parentKey) k = (parentKey.split('_')[0] + '_' + base).split('_').slice(0, 4).join('_');
  let n = 2; const stem = k;
  while (used.has(k)) k = stem + '_' + n++;
  used.add(k); return k;
}
(function assignKeys(map, parentKey) {
  for (const node of map.values()) { node._key = mkKey(node.seg, parentKey); assignKeys(node.children, node._key); }
})(tree, null);

// ---------- counts ----------
function total(node) { let t = node.images.length; for (const c of node.children.values()) t += total(c); return t; }

// ---------- YAML emit ----------
const q = s => '"' + String(s).replace(/\\/g, '\\\\').replace(/"/g, '\\"') + '"';
const out = [];
let overfull = 0, descCount = 0;

function emitNode(node, level, indent) {
  const pad = ' '.repeat(indent);
  const direct = node.images.length;
  if (direct > 12) overfull++;
  out.push(`${pad}- level_${level}:`);
  out.push(`${pad}    title: ${q(node.title)}`);
  out.push(`${pad}    _key: ${node._key}`);
  out.push(`${pad}    number_of_images: ${direct}`);
  out.push(`${pad}    number_of_images_recursive: ${total(node)}`);
  if (direct > 12) out.push(`${pad}    needs_split: true   # over the 12 ceiling — split on a later pass`);
  if (direct === 0) { out.push(`${pad}    images: []`); }
  else {
    out.push(`${pad}    images:`);
    for (const im of node.images) {
      const d = readDesc(im.orig_path.replace('~/_Mirror/Politics/Charlie_Kirk_Mi/', ''));
      if (d) descCount++;
      out.push(`${pad}      - image:`);
      out.push(`${pad}          cid: ""`);
      out.push(`${pad}          sha256: ${im.sha256}`);
      out.push(`${pad}          file_path: ${q(im.orig_path)}`);
      out.push(`${pad}          ai_description: ${d ? q(d) : '""'}`);
      const others = [...(dirsBySha.get(im.sha256) || [])].filter(x => x !== im.dir);
      if (others.length) out.push(`${pad}          also_filed_in: [${others.map(q).join(', ')}]`);
    }
  }
  if (node.children.size) {
    out.push(`${pad}    level_${level + 1}:`);
    for (const c of node.children.values()) emitNode(c, level + 1, indent + 6);
  }
}

out.push('# images.yaml — image evidence hierarchy for the Charlie Kirk site.');
out.push('# GENERATED first pass. Source: ~/_Mirror/Politics/Charlie_Kirk_Mi (1,666 images).');
out.push('# Clusters follow the mirror\'s own concept filing; mirror depth maps to page level.');
out.push('# cid is intentionally empty (IPFS not assigned yet). fingerprint deferred; sha256 is the identity.');
out.push('# Nodes marked needs_split exceed the 12-image ceiling and get split on a later pass.');
out.push('level_3:');
for (const node of tree.values()) emitNode(node, 3, 2);

fs.writeFileSync(path.join(SCRATCH, 'images.yaml'), out.join('\n') + '\n');

// ---------- report ----------
const leafCount = (function count(map) { let n = 0; for (const c of map.values()) { n += 1 + count(c.children); } return n; })(tree);
console.log(`level_3 clusters : ${tree.size}`);
console.log(`total nodes      : ${leafCount}`);
console.log(`images placed    : ${deduped.length - unassigned.length} / ${deduped.length} (collapsed ${collapsed} redundant same-dir copies from ${rows.length})`);
console.log(`unassigned       : ${unassigned.length}`);
console.log(`descriptions in  : ${descCount}`);
console.log(`nodes over 12    : ${overfull}`);
if (unassigned.length) console.log('unassigned dirs  :', [...new Set(unassigned.map(u => u.dir))].join(', '));
