// anatomy.js: the procedural anatomical bust behind every Body Tour page.
//
// Everything is built from code (no model files), so a teammate can move an organ by
// editing a number. Units are centimetres. Axes are the patient's own:
//   +x = the patient's LEFT, +y = up, +z = the front of the body.
//   y = 0 is the sternal notch (the dip at the base of the throat).
// Every mesh is baked in these model coordinates with an identity transform, because the
// shaders in stage.js read the raw vertex position to place injuries, fluid and the blast
// wave. Do not give a mesh its own position/rotation/scale; bake it into the geometry.
//
// The anatomy is simplified and positions are approximate. It is an illustration for a
// lay reader, not a reconstruction from the sealed medical examiner report.

import * as THREE from './three.module.min.js';

const V3 = (a) => new THREE.Vector3(a[0], a[1], a[2]);
const clamp01 = (t) => Math.min(1, Math.max(0, t));
const smooth01 = (t) => { t = clamp01(t); return t * t * (3 - 2 * t); };
const lerp = (a, b, t) => a + (b - a) * t;

// Catmull-Rom through table rows sorted by their first column, descending.
function rowInterp(rows, key, col) {
  const n = rows.length;
  if (key >= rows[0][0]) return rows[0][col];
  if (key <= rows[n - 1][0]) return rows[n - 1][col];
  let i = 0;
  while (!(rows[i][0] >= key && key >= rows[i + 1][0])) i++;
  const p0 = rows[Math.max(0, i - 1)][col], p1 = rows[i][col];
  const p2 = rows[i + 1][col], p3 = rows[Math.min(n - 1, i + 2)][col];
  const t = (rows[i][0] - key) / (rows[i][0] - rows[i + 1][0]);
  const t2 = t * t, t3 = t2 * t;
  return 0.5 * (2 * p1 + (-p0 + p2) * t + (2 * p0 - 5 * p1 + 4 * p2 - p3) * t2 + (-p0 + 3 * p1 - 3 * p2 + p3) * t3);
}

// ---------------------------------------------------------------------------
// Skin: a stack of superellipse cross-sections from the hips to under the jaw.
// Row: [y, half-width, front z, back z, superellipse exponent]
// ---------------------------------------------------------------------------
const SKIN_ROWS = [
  [13.5, 5.5, 3.5, -8.2, 2.1],
  [11.0, 5.8, 3.8, -8.5, 2.1],
  [8.0, 6.0, 4.1, -8.7, 2.1],
  [5.0, 6.3, 4.4, -9.0, 2.15],
  [2.5, 7.0, 5.0, -9.6, 2.2],
  [1.5, 9.4, 5.4, -10.0, 2.4],
  [0.5, 13.8, 6.0, -10.5, 2.7],
  [-0.8, 17.8, 7.0, -11.0, 3.0],
  [-2.5, 19.8, 8.2, -11.3, 3.1],
  [-5.5, 20.2, 9.7, -11.6, 3.0],
  [-8.0, 18.0, 10.6, -11.7, 2.9],
  [-10.5, 16.9, 11.1, -11.6, 2.8],
  [-14.0, 16.5, 11.1, -11.4, 2.7],
  [-18.0, 16.0, 10.6, -11.0, 2.6],
  [-23.0, 15.5, 10.1, -10.4, 2.5],
  [-29.0, 14.9, 9.8, -9.7, 2.4],
  [-35.0, 15.4, 10.1, -9.8, 2.4],
  [-41.0, 16.8, 10.4, -10.4, 2.5],
  [-46.0, 17.2, 10.1, -10.5, 2.5],
];
const SKIN_TOP = 13.5, SKIN_BOTTOM = -46;

function skinSection(y) {
  return {
    w: rowInterp(SKIN_ROWS, y, 1), f: rowInterp(SKIN_ROWS, y, 2),
    b: rowInterp(SKIN_ROWS, y, 3), n: rowInterp(SKIN_ROWS, y, 4),
  };
}

// Small surface details on the front and back of the torso.
function skinBumps(x, y, front) {
  let dz = 0;
  if (front) {
    const pec = Math.exp(-(((Math.abs(x) - 7.5) / 3.8) ** 2)) * Math.exp(-(((y + 10.5) / 4.2) ** 2));
    dz += 0.9 * pec;
    dz += 0.55 * Math.exp(-((x / 1.1) ** 2) - (((y - 9.4) / 1.1) ** 2)); // Adam's apple
    dz -= 0.35 * Math.exp(-((x / 1.6) ** 2) - (((y + 0.2) / 0.9) ** 2)); // sternal notch dip
  } else {
    dz += 0.45 * Math.exp(-((x / 1.5) ** 2)) * smooth01((10 - y) / 6); // spine groove
  }
  return dz;
}

function skinPointAt(theta, y) {
  const s = skinSection(y);
  const c = Math.cos(theta), sn = Math.sin(theta);
  const e = 2 / s.n;
  const x = s.w * Math.sign(c) * Math.abs(c) ** e;
  const front = sn >= 0;
  let z = (front ? s.f : s.b) * Math.abs(sn) ** e;
  z += skinBumps(x, y, front);
  return [x, y, z];
}

export function insideSkin(x, y, z) {
  const s = skinSection(y);
  const zz = z >= 0 ? z / s.f : z / -s.b;
  return (Math.abs(x) / s.w) ** s.n + Math.abs(zz) ** s.n <= 1;
}

// The skin surface point straight in front of (or behind) the body at (x, y).
export function skinZ(x, y, side = 'front') {
  const s = skinSection(y);
  const r = Math.min(0.999, Math.abs(x) / s.w);
  const c = r ** (s.n / 2);
  const sn = Math.sqrt(1 - c * c);
  const front = side === 'front';
  return (front ? s.f : s.b) * sn ** (2 / s.n) + skinBumps(x, y, front);
}

function insideNeckColumn(p) {
  if (p[1] > SKIN_TOP || p[1] < 0) return false;
  const s = skinSection(p[1]);
  const zz = p[2] >= 0 ? p[2] / s.f : p[2] / -s.b;
  return (Math.abs(p[0]) / s.w) ** s.n + Math.abs(zz) ** s.n < 0.94;
}

// ---------------------------------------------------------------------------
// Head shape: a deformed sphere (cranium, jaw, chin, nose, brow, eye sockets, ears).
// ---------------------------------------------------------------------------
function headShape(ux, uy, uz) {
  let x = ux * 8.0;
  let y = 21.2 + uy * (uy > 0 ? 11.2 : 11.6);
  let z = uz * 10.0;
  const low = smooth01((-uy - 0.05) / 0.95);
  x *= 1 - 0.32 * smooth01((-uy - 0.78) / 0.22);
  if (uz < 0) z *= 1 - 0.25 * low;
  z += 3.6 * low * Math.max(0, uz) ** 0.7;
  const fn = Math.max(0, uz);
  z += 2.0 * Math.exp(-(x * x) / 1.4 - ((y - 19.0) ** 2) / 5.0) * fn * fn;
  z += 0.6 * Math.exp(-((y - 24.6) ** 2) / 1.6) * Math.exp(-(x * x) / 18) * fn;
  z -= 0.9 * (Math.exp(-(((x - 3.2) ** 2) + (y - 22.2) ** 2) / 1.4) + Math.exp(-(((x + 3.2) ** 2) + (y - 22.2) ** 2) / 1.4)) * fn;
  const side = Math.abs(ux);
  x += Math.sign(ux) * 1.1 * Math.exp(-((y - 20.2) ** 2) / 4.5 - ((z + 0.8) ** 2) / 2.2) * smooth01((side - 0.6) / 0.3);
  return [x, y, z];
}

function insideHead(p) {
  const dx = p[0] / 7.7, dy = (p[1] - 21.2) / 11.0, dz = (p[2] - 0.6) / 9.6;
  return dx * dx + dy * dy + dz * dz < 0.9;
}

// ---------------------------------------------------------------------------
// The spine. [name, y of the vertebral body centre, z of the body centre]
// ---------------------------------------------------------------------------
export const SPINE = [
  ['C1', 13.6, -2.9], ['C2', 11.9, -2.7], ['C3', 10.2, -2.55], ['C4', 8.5, -2.5],
  ['C5', 6.8, -2.55], ['C6', 5.1, -2.75], ['C7', 3.35, -3.15],
  ['T1', 1.4, -3.8], ['T2', -0.7, -4.5], ['T3', -2.9, -5.1], ['T4', -5.2, -5.6],
  ['T5', -7.6, -6.0], ['T6', -10.0, -6.2], ['T7', -12.5, -6.3], ['T8', -15.0, -6.25],
  ['T9', -17.6, -6.1], ['T10', -20.2, -5.85], ['T11', -22.9, -5.5], ['T12', -25.7, -5.0],
  ['L1', -28.8, -4.4], ['L2', -32.1, -3.8], ['L3', -35.4, -3.4], ['L4', -38.7, -3.3], ['L5', -42.0, -3.6],
];
export const VERT = {};
SPINE.forEach(([n, y, z], i) => { VERT[n] = { name: n, y, z, i }; });

function vertDims(name) {
  if (name[0] === 'C') return { rx: 1.45, rz: 1.05, h: 1.2, canal: 0.85, spin: name === 'C7' ? 3.0 : 1.9 };
  if (name[0] === 'T') {
    const k = +name.slice(1);
    return { rx: 1.7 + 0.06 * k, rz: 1.35 + 0.05 * k, h: 1.55 + 0.05 * k, canal: 0.7, spin: 3.2 };
  }
  return { rx: 2.5, rz: 1.85, h: 2.4, canal: 0.85, spin: 2.7 };
}
export function canalZ(name) { const v = VERT[name], d = vertDims(name); return v.z - d.rz - d.canal - 0.15; }

// ---------------------------------------------------------------------------
// Ribs. Index 0..11 = rib 1..12. W = lateral half-width, D = half-depth,
// CZ = centre z of the rib ellipse, DROP = how far the rib falls front to back,
// FX = x of the front (bony) end. Ribs 11 and 12 float.
// ---------------------------------------------------------------------------
const RIB_W = [5.6, 8.6, 10.9, 12.6, 13.6, 14.2, 14.4, 14.3, 13.8, 13.0, 11.6, 9.6];
const RIB_D = [5.0, 7.0, 8.2, 8.9, 9.3, 9.5, 9.6, 9.5, 9.2, 8.8, 8.2, 7.6];
const RIB_CZ = [-0.8, -0.6, -0.4, -0.2, 0, 0, 0, -0.1, -0.3, -0.6, -1.2, -1.8];
const RIB_DROP = [2.4, 4.6, 6.6, 8.4, 9.6, 10.6, 11.4, 11.8, 11.8, 11.2, 8.0, 6.0];
const RIB_FX = [4.2, 5.6, 6.8, 7.8, 8.8, 9.8, 10.6, 11.4, 12.2, 12.6, 0, 0];
const STERN_Y = [-0.9, -4.6, -7.0, -9.3, -11.5, -13.6, -15.6];

// The inside of the rib cage at height y (used to keep the lungs inside the ribs).
const CAGE_ROWS = (() => {
  const rows = [[4.6, 5.4, 3.6, -2.2]];
  for (let k = 0; k < 10; k++) {
    const yT = VERT['T' + (k + 1)].y;
    rows.push([yT - RIB_DROP[k] * 0.45, RIB_W[k] - 0.9, RIB_D[k] - 0.9, RIB_CZ[k]]);
  }
  rows.sort((a, b) => b[0] - a[0]);
  return rows;
})();
export function cage(y) {
  return { w: rowInterp(CAGE_ROWS, y, 1), d: rowInterp(CAGE_ROWS, y, 2), cz: rowInterp(CAGE_ROWS, y, 3) };
}
function sternumZ(y) { return skinZ(0, y, 'front') - 1.1; }

// ---------------------------------------------------------------------------
// The heart sits left of centre, behind the breastbone; its apex points left, down, forward.
// ---------------------------------------------------------------------------
export const HEART_C = [1.4, -11.0, 3.2];
const HEART_AXIS = new THREE.Vector3(0.7, -0.45, 0.5).normalize();

// ---------------------------------------------------------------------------
// Vessel and airway centre lines (model coordinates).
// ---------------------------------------------------------------------------
export const PATHS = {
  aorta: [[1.0, -8.0, 3.5], [0.6, -4.6, 3.3], [0.4, -1.8, 2.0], [1.4, -1.3, -0.6], [2.2, -2.8, -3.0], [2.0, -6.5, -4.3], [1.8, -15, -4.9], [1.2, -26, -3.8], [0.6, -36, -1.8]],
  pulmonary: [[0.2, -9.6, 5.6], [0.9, -7.4, 4.6], [1.6, -5.9, 2.8], [4.0, -6.6, 1.0], [6.4, -7.4, -0.2]],
  pulmonaryR: [[1.6, -5.9, 2.8], [-1.4, -6.6, 1.6], [-5.6, -7.6, 0.4]],
  svc: [[-2.4, -1.6, 2.8], [-2.6, -5.0, 2.8], [-2.7, -8.8, 2.6]],
  brachioceph: [[0.0, -1.9, 2.4], [-1.0, -0.4, 2.4], [-1.9, 1.2, 2.2]],
  carotidL: [[0.9, -1.5, 1.7], [1.7, 1.2, 1.5], [2.2, 4.0, 1.35], [2.4, 6.6, 1.25], [2.45, 8.9, 1.0]],
  carotidLInt: [[2.45, 8.9, 1.0], [2.7, 11.5, 0.2], [2.9, 14.6, -0.8], [2.4, 17.4, -0.4]],
  carotidLExt: [[2.45, 8.9, 1.0], [2.8, 10.6, 2.2], [3.2, 12.6, 2.8]],
  carotidR: [[-1.9, 1.2, 2.2], [-2.2, 4.0, 1.35], [-2.4, 6.6, 1.25], [-2.45, 8.9, 1.0]],
  carotidRInt: [[-2.45, 8.9, 1.0], [-2.7, 11.5, 0.2], [-2.9, 14.6, -0.8], [-2.4, 17.4, -0.4]],
  carotidRExt: [[-2.45, 8.9, 1.0], [-2.8, 10.6, 2.2], [-3.2, 12.6, 2.8]],
  subclavianL: [[1.8, -1.6, -0.2], [3.6, 1.4, -0.4], [6.0, 2.4, 0.2], [9.5, 1.4, 0.0], [13.0, 0.0, -0.8]],
  subclavianR: [[-1.9, 1.2, 2.2], [-3.6, 1.6, 0.6], [-6.0, 2.4, 0.2], [-9.5, 1.4, 0.0], [-13.0, 0.0, -0.8]],
  vertebralL: [[3.6, 1.4, -0.4], [2.6, 3.6, -1.9], [2.5, 6.8, -2.2], [2.5, 10.2, -2.3], [2.3, 13.0, -2.9], [1.0, 15.2, -2.9], [0.2, 16.4, -1.9]],
  vertebralR: [[-3.6, 1.6, 0.6], [-2.6, 3.6, -1.9], [-2.5, 6.8, -2.2], [-2.5, 10.2, -2.3], [-2.3, 13.0, -2.9], [-1.0, 15.2, -2.9], [-0.2, 16.4, -1.9]],
  basilar: [[0, 16.3, -1.9], [0, 18.2, -1.4], [0, 20.0, -1.0]],
  jugularIL: [[3.6, 14.4, -1.6], [3.5, 11.6, -0.2], [3.4, 8.6, 0.9], [3.4, 5.4, 1.05], [3.1, 2.2, 1.6], [2.6, 0.2, 2.2], [0.4, -1.2, 2.8], [-2.3, -1.6, 2.8]],
  jugularIR: [[-3.6, 14.4, -1.6], [-3.5, 11.6, -0.2], [-3.4, 8.6, 0.9], [-3.4, 5.4, 1.05], [-3.1, 2.2, 1.6], [-2.6, 0.2, 2.4], [-2.4, -1.6, 2.8]],
  jugularEL: [[5.6, 12.4, 0.4], [5.4, 9.4, 1.0], [5.5, 6.4, 0.85], [5.6, 3.6, 0.6], [5.4, 1.4, 0.4], [4.8, 0.2, 0.6]],
  jugularER: [[-5.6, 12.4, 0.4], [-5.4, 9.4, 1.0], [-5.5, 6.4, 0.85], [-5.6, 3.6, 0.6], [-5.4, 1.4, 0.4], [-4.8, 0.2, 0.6]],
  subclavVeinL: [[13.0, -0.6, 0.4], [8.0, 0.6, 1.2], [4.8, 0.2, 0.6], [2.6, 0.2, 2.2]],
  subclavVeinR: [[-13.0, -0.6, 0.4], [-8.0, 0.6, 1.2], [-4.8, 0.2, 0.6], [-2.6, 0.2, 2.4]],
  trachea: [[0, 5.8, 1.85], [0, 3.0, 1.55], [0, 0.0, 0.9], [0.05, -2.8, -0.1], [0.15, -5.0, -0.8], [0.25, -6.3, -1.2]],
  bronchusL: [[0.25, -6.3, -1.2], [2.0, -7.0, -1.4], [3.6, -7.8, -1.6], [4.9, -8.6, -1.7]],
  bronchusR: [[0.25, -6.3, -1.2], [-1.6, -7.2, -1.2], [-2.9, -8.2, -1.1], [-3.9, -9.2, -1.0]],
  esophagus: [[0, 6.8, 0.3], [0, 3.0, -0.3], [0.1, -1.0, -1.4], [0.4, -5.0, -2.6], [0.7, -10.0, -3.0], [1.0, -16.0, -2.7], [1.8, -24.0, -1.4]],
  brainstem: [[0, 21.3, -1.2], [0, 19.0, -2.0], [0, 16.8, -2.9], [0, 14.8, -3.5]],
  strapL: [[1.3, 10.8, 3.3], [1.5, 8.6, 3.95], [1.6, 5.6, 3.85], [1.8, 2.0, 4.5], [1.9, -0.6, 4.9]],
  strapR: [[-1.3, 10.8, 3.3], [-1.5, 8.6, 3.95], [-1.6, 5.6, 3.85], [-1.8, 2.0, 4.5], [-1.9, -0.6, 4.9]],
  scmL: [[6.4, 17.2, -3.4], [6.0, 13.0, -1.6], [5.0, 8.5, 0.6], [3.6, 4.5, 3.0], [2.2, 1.0, 5.0]],
  scmR: [[-6.4, 17.2, -3.4], [-6.0, 13.0, -1.6], [-5.0, 8.5, 0.6], [-3.6, 4.5, 3.0], [-2.2, 1.0, 5.0]],
  clavicleL: [[2.0, 0.6, 5.3], [5.5, 1.0, 5.6], [10.0, 0.9, 4.0], [14.0, 0.4, 0.6], [16.6, -0.6, -1.4]],
  clavicleR: [[-2.0, 0.6, 5.3], [-5.5, 1.0, 5.6], [-10.0, 0.9, 4.0], [-14.0, 0.4, 0.6], [-16.6, -0.6, -1.4]],
  mandible: [[6.0, 17.6, 0.2], [5.6, 14.6, -0.4], [5.3, 12.2, 0.4], [4.0, 10.6, 4.4], [1.8, 10.0, 6.6], [0, 9.9, 7.1], [-1.8, 10.0, 6.6], [-4.0, 10.6, 4.4], [-5.3, 12.2, 0.4], [-5.6, 14.6, -0.4], [-6.0, 17.6, 0.2]],
};

function curve(points) {
  return new THREE.CatmullRomCurve3(points.map(V3), false, 'catmullrom', 0.5);
}
function tube(points, radius, tubular = 64, radial = 10) {
  return new THREE.TubeGeometry(curve(points), tubular, radius, radial, false);
}
// A tube squashed toward the neck's centre line, for flat muscles (straps, SCM).
function flatTube(points, radius, factor, tubular = 48, radial = 12) {
  const cv = curve(points);
  const g = new THREE.TubeGeometry(cv, tubular, radius, radial, false);
  const pos = g.attributes.position;
  for (let i = 0; i <= tubular; i++) {
    const c = cv.getPointAt(i / tubular);
    const r = new THREE.Vector3(c.x, 0, c.z + 2).normalize();
    for (let j = 0; j <= radial; j++) {
      const k = i * (radial + 1) + j;
      const v = new THREE.Vector3().fromBufferAttribute(pos, k).sub(c);
      const along = v.dot(r);
      v.addScaledVector(r, along * (factor - 1));
      pos.setXYZ(k, c.x + v.x, c.y + v.y, c.z + v.z);
    }
  }
  g.computeVertexNormals();
  return g;
}

// Smooth 3D value noise, and a ridged version whose creases look like brain folds.
function hash3(x, y, z) {
  const h = Math.sin(x * 127.1 + y * 311.7 + z * 74.7) * 43758.5453;
  return h - Math.floor(h);
}
function vnoise(x, y, z) {
  const xi = Math.floor(x), yi = Math.floor(y), zi = Math.floor(z);
  const xf = x - xi, yf = y - yi, zf = z - zi;
  const u = xf * xf * (3 - 2 * xf), v = yf * yf * (3 - 2 * yf), w = zf * zf * (3 - 2 * zf);
  const c = (a, b, d) => hash3(xi + a, yi + b, zi + d);
  const x00 = lerp(c(0, 0, 0), c(1, 0, 0), u), x10 = lerp(c(0, 1, 0), c(1, 1, 0), u);
  const x01 = lerp(c(0, 0, 1), c(1, 0, 1), u), x11 = lerp(c(0, 1, 1), c(1, 1, 1), u);
  return lerp(lerp(x00, x10, v), lerp(x01, x11, v), w);
}
function ridge(x, y, z) { return 1 - Math.abs(2 * vnoise(x, y, z) - 1); }

function deformSphere(wSeg, hSeg, fn) {
  const g = new THREE.SphereGeometry(1, wSeg, hSeg);
  const pos = g.attributes.position;
  for (let i = 0; i < pos.count; i++) {
    const p = fn(pos.getX(i), pos.getY(i), pos.getZ(i));
    pos.setXYZ(i, p[0], p[1], p[2]);
  }
  g.computeVertexNormals();
  return g;
}

function ellipsoid(c, r, w = 32, h = 24) {
  return deformSphere(w, h, (x, y, z) => [c[0] + x * r[0], c[1] + y * r[1], c[2] + z * r[2]]);
}

// Merge several non-indexed or indexed geometries into one (position + normal only).
function merge(geoms) {
  let total = 0, idxTotal = 0;
  const parts = geoms.map((g) => {
    const gi = g.index ? g : g.toNonIndexed();
    if (!gi.attributes.normal) gi.computeVertexNormals();
    total += gi.attributes.position.count;
    idxTotal += gi.index ? gi.index.count : gi.attributes.position.count;
    return gi;
  });
  const pos = new Float32Array(total * 3), nor = new Float32Array(total * 3);
  const idx = new Uint32Array(idxTotal);
  let off = 0, ioff = 0;
  for (const g of parts) {
    pos.set(g.attributes.position.array, off * 3);
    nor.set(g.attributes.normal.array, off * 3);
    if (g.index) { for (let i = 0; i < g.index.count; i++) idx[ioff + i] = g.index.array[i] + off; ioff += g.index.count; }
    else { for (let i = 0; i < g.attributes.position.count; i++) idx[ioff + i] = off + i; ioff += g.attributes.position.count; }
    off += g.attributes.position.count;
  }
  const out = new THREE.BufferGeometry();
  out.setAttribute('position', new THREE.BufferAttribute(pos, 3));
  out.setAttribute('normal', new THREE.BufferAttribute(nor, 3));
  out.setIndex(new THREE.BufferAttribute(idx, 1));
  return out;
}

function bake(g, m) { g.applyMatrix4(m); return g; }
function orientTo(dirFrom, dirTo) { return new THREE.Matrix4().makeRotationFromQuaternion(new THREE.Quaternion().setFromUnitVectors(dirFrom.clone().normalize(), dirTo.clone().normalize())); }

// ---------------------------------------------------------------------------
// Builders
// ---------------------------------------------------------------------------
function buildSkinSurface() {
  const rows = 120, cols = 72;
  const pos = [], idx = [];
  for (let r = 0; r <= rows; r++) {
    const y = lerp(SKIN_TOP, SKIN_BOTTOM, r / rows);
    for (let c = 0; c <= cols; c++) pos.push(...skinPointAt((c / cols) * Math.PI * 2, y));
  }
  for (let r = 0; r < rows; r++) for (let c = 0; c < cols; c++) {
    const a = r * (cols + 1) + c, b = a + cols + 1;
    idx.push(a, b, a + 1, b, b + 1, a + 1);
  }
  const g = new THREE.BufferGeometry();
  g.setAttribute('position', new THREE.Float32BufferAttribute(pos, 3));
  g.setIndex(idx);
  g.computeVertexNormals();
  const head = deformSphere(64, 48, headShape);
  return merge([g, head]);
}

function buildSkinLines() {
  const v = [];
  const seg = (a, b) => {
    if (insideHead(a) && insideHead(b)) return;
    v.push(...a, ...b);
  };
  // torso and neck rings every 2.2 cm, meridians every 10 degrees
  for (let y = SKIN_TOP; y >= SKIN_BOTTOM - 0.01; y -= 2.2) {
    let prev = null;
    for (let c = 0; c <= 96; c++) {
      const p = skinPointAt((c / 96) * Math.PI * 2, y);
      if (prev) seg(prev, p);
      prev = p;
    }
  }
  for (let m = 0; m < 36; m++) {
    const th = (m / 36) * Math.PI * 2;
    let prev = null;
    for (let r = 0; r <= 140; r++) {
      const p = skinPointAt(th, lerp(SKIN_TOP, SKIN_BOTTOM, r / 140));
      if (prev) seg(prev, p);
      prev = p;
    }
  }
  // head: latitude rings and longitude lines, skipping what hides inside the neck
  const H = 40, W = 48;
  const hp = (i, j) => {
    const phi = (i / H) * Math.PI, th = (j / W) * Math.PI * 2;
    return headShape(Math.sin(phi) * Math.cos(th), Math.cos(phi), Math.sin(phi) * Math.sin(th));
  };
  const hseg = (a, b) => { if (insideNeckColumn(a) && insideNeckColumn(b)) return; v.push(...a, ...b); };
  for (let i = 2; i < H; i += 2) for (let j = 0; j < W; j++) hseg(hp(i, j), hp(i, j + 1));
  for (let j = 0; j < W; j += 2) for (let i = 0; i < H; i++) hseg(hp(i, j), hp(i + 1, j));
  const g = new THREE.BufferGeometry();
  g.setAttribute('position', new THREE.Float32BufferAttribute(v, 3));
  return g;
}

function buildVertebra(name) {
  const v = VERT[name], d = vertDims(name);
  const parts = [];
  // local frame: the body axis follows the curve of the spine
  const i = v.i;
  const up = SPINE[Math.max(0, i - 1)], dn = SPINE[Math.min(SPINE.length - 1, i + 1)];
  const axis = new THREE.Vector3(0, up[1] - dn[1], up[2] - dn[2]).normalize();
  const rot = orientTo(new THREE.Vector3(0, 1, 0), axis);
  const at = (local) => new THREE.Matrix4().makeTranslation(0, v.y, v.z).multiply(rot).multiply(local);
  if (name !== 'C1') {
    const body = new THREE.CylinderGeometry(1, 1, d.h, 22, 1);
    bake(body, new THREE.Matrix4().makeScale(d.rx, 1, d.rz));
    parts.push(bake(body, at(new THREE.Matrix4())));
  }
  const canalR = d.canal + 0.25;
  const ringR = canalR + 0.35;
  const cz = -d.rz - d.canal - 0.15;
  const ring = new THREE.TorusGeometry(ringR, name === 'C1' ? 0.45 : 0.32, 8, 26);
  bake(ring, new THREE.Matrix4().makeRotationX(Math.PI / 2));
  bake(ring, new THREE.Matrix4().makeScale(name === 'C1' ? 1.5 : 1.15, 1, 1));
  parts.push(bake(ring, at(new THREE.Matrix4().makeTranslation(0, 0, cz))));
  // spinous process: points back and, in the chest, steeply down
  const tilt = name[0] === 'T' ? 0.6 : name[0] === 'C' ? 0.25 : 0.05;
  const spin = new THREE.BoxGeometry(name[0] === 'C' ? 0.42 : 0.5, name[0] === 'C' ? 0.55 : 0.75, d.spin);
  bake(spin, new THREE.Matrix4().makeTranslation(0, 0, -d.spin / 2));
  bake(spin, new THREE.Matrix4().makeRotationX(-tilt));
  parts.push(bake(spin, at(new THREE.Matrix4().makeTranslation(0, 0, cz - ringR))));
  // transverse processes
  const tw = name[0] === 'C' ? d.rx + 1.3 : d.rx + 1.7;
  const tr = new THREE.BoxGeometry(tw * 2, 0.55, 0.65);
  parts.push(bake(tr, at(new THREE.Matrix4().makeTranslation(0, 0.05, cz + 0.2))));
  if (name === 'C2') { // the dens, a peg reaching up into the ring of C1
    const dens = new THREE.CylinderGeometry(0.45, 0.6, 1.4, 12);
    parts.push(bake(dens, at(new THREE.Matrix4().makeTranslation(0, 1.2, 0.1))));
  }
  if (name === 'C1') { // lateral masses
    [1, -1].forEach((s) => parts.push(bake(new THREE.BoxGeometry(0.9, 0.9, 1.4), at(new THREE.Matrix4().makeTranslation(s * 1.5, 0, -0.1)))));
  }
  return merge(parts);
}

function buildSpine() {
  const verts = SPINE.map(([n]) => buildVertebra(n));
  const discs = [];
  for (let i = 1; i < SPINE.length - 1; i++) {
    const a = SPINE[i], b = SPINE[i + 1];
    const d = vertDims(a[0]);
    const mid = [0, (a[1] + b[1]) / 2, (a[2] + b[2]) / 2];
    const axis = new THREE.Vector3(0, a[1] - b[1], a[2] - b[2]);
    const gap = Math.max(0.2, axis.length() - (vertDims(a[0]).h + vertDims(b[0]).h) / 2);
    const g = new THREE.CylinderGeometry(1, 1, gap * 0.95, 20);
    bake(g, new THREE.Matrix4().makeScale(d.rx * 0.95, 1, d.rz * 0.95));
    bake(g, orientTo(new THREE.Vector3(0, 1, 0), axis.normalize()));
    bake(g, new THREE.Matrix4().makeTranslation(...mid));
    discs.push(g);
  }
  return { spine: merge(verts), discs: merge(discs) };
}

function cordPoints() {
  const pts = [[0, 16.8, -2.9], [0, 14.8, -3.6]];
  for (const [n] of SPINE) {
    if (n === 'L2') break;
    pts.push([0, VERT[n].y, canalZ(n)]);
  }
  return pts;
}

function buildRibs() {
  const bones = [], carts = [];
  for (let k = 0; k < 12; k++) {
    const T = VERT['T' + (k + 1)];
    const dT = vertDims('T' + (k + 1));
    const floating = k >= 10;
    [1, -1].forEach((s) => {
      const W = RIB_W[k], D = RIB_D[k], cz = RIB_CZ[k];
      const phiS = -Math.PI / 2 + 0.5;
      const phiE = floating ? -0.2 - (k - 10) * 0.25 : Math.acos(Math.min(0.98, RIB_FX[k] / W));
      const pts = [[s * (dT.rx + 0.5), T.y + 0.3, T.z - 0.5]];
      const N = 12;
      for (let i = 0; i <= N; i++) {
        const t = i / N;
        const phi = lerp(phiS, phiE, t);
        const y = T.y - RIB_DROP[k] * Math.pow(t, 1.35);
        pts.push([s * W * Math.cos(phi), y, cz + D * Math.sin(phi)]);
      }
      bones.push(tube(pts, k === 0 ? 0.5 : 0.42, 72, 8));
      if (!floating) {
        const e = pts[pts.length - 1];
        let target;
        if (k < 7) target = [s * 1.6, STERN_Y[k], sternumZ(STERN_Y[k]) - 0.2];
        else {
          const ty = [-17.0, -19.3, -21.5][k - 7], tx = [4.2, 6.0, 8.0][k - 7];
          target = [s * tx, ty, skinZ(tx, ty, 'front') - 1.6];
        }
        const mid = [lerp(e[0], target[0], 0.5) + s * 0.6, lerp(e[1], target[1], 0.55), Math.max(e[2], target[2]) + 0.5];
        carts.push(tube([e, mid, target], 0.3, 24, 8));
      }
    });
  }
  return { ribs: merge(bones), cartilage: merge(carts) };
}

function buildSternum() {
  const o = [[-2.6, 0.2], [-0.8, 0.0], [0, -0.4], [0.8, 0.0], [2.6, 0.2], [2.5, -1.4], [1.6, -4.6], [1.9, -5.0], [1.9, -10.0], [1.6, -15.8], [0.9, -16.4], [0.6, -19.6], [0, -19.9], [-0.6, -19.6], [-0.9, -16.4], [-1.6, -15.8], [-1.9, -10.0], [-1.9, -5.0], [-1.6, -4.6], [-2.5, -1.4]];
  const shape = new THREE.Shape(o.map(([x, y]) => new THREE.Vector2(x, y)));
  const g = new THREE.ExtrudeGeometry(shape, { depth: 1.1, bevelEnabled: true, bevelThickness: 0.15, bevelSize: 0.15, bevelSegments: 2, steps: 1, curveSegments: 6 });
  const pos = g.attributes.position;
  for (let i = 0; i < pos.count; i++) {
    const y = pos.getY(i);
    pos.setZ(i, sternumZ(y) - 1.2 + pos.getZ(i));
  }
  g.computeVertexNormals();
  return g;
}

function buildScapulae() {
  const out = [];
  [1, -1].forEach((s) => {
    const A = [s * 6.0, -2.4], B = [s * 7.5, -17.0], C = [s * 15.4, -4.6];
    const pos = [], idx = [];
    const N = 8;
    for (let i = 0; i <= N; i++) for (let j = 0; j <= N - i; j++) {
      const a = 1 - (i + j) / N, b = i / N, c = j / N;
      const x = A[0] * a + B[0] * b + C[0] * c, y = A[1] * a + B[1] * b + C[1] * c;
      pos.push(x, y, skinZ(x, y, 'back') + 1.6 + 0.5 * c);
    }
    let k = 0; const rowStart = [];
    for (let i = 0; i <= N; i++) { rowStart.push(k); k += N - i + 1; }
    for (let i = 0; i < N; i++) for (let j = 0; j < N - i; j++) {
      const a = rowStart[i] + j, b = rowStart[i + 1] + j;
      idx.push(a, b, a + 1);
      if (j < N - i - 1) idx.push(a + 1, b, b + 1);
    }
    const g = new THREE.BufferGeometry();
    g.setAttribute('position', new THREE.Float32BufferAttribute(pos, 3));
    g.setIndex(idx); g.computeVertexNormals();
    out.push(g);
    out.push(tube([[s * 6.5, -4.4, skinZ(6.5, -4.4, 'back') + 1.4], [s * 12.0, -1.0, skinZ(12, -1, 'back') + 1.3], [s * 16.2, -0.6, -2.6]], 0.45, 24, 8));
  });
  return merge(out);
}

function buildSkull() {
  const cranium = deformSphere(48, 36, (x, y, z) => {
    let px = x * 7.4, py = 22.6 + y * 9.0, pz = -0.9 + z * 9.5;
    if (py < 16.2) py = 16.2 + (py - 16.2) * 0.25;
    return [px, py, pz];
  });
  const orbits = [1, -1].map((s) => {
    const g = new THREE.TorusGeometry(1.75, 0.28, 8, 24);
    bake(g, new THREE.Matrix4().makeTranslation(s * 3.2, 21.9, 7.4));
    return g;
  });
  const jaw = tube(PATHS.mandible, 0.75, 96, 8);
  return merge([cranium, ...orbits, jaw]);
}

function brainHemisphere(s) {
  return deformSphere(72, 54, (ux, uy, uz) => {
    const cx = s * 3.6, cy = 23.8, cz = -0.4;
    let x = ux * 3.5, y = uy * (uy > 0 ? 5.8 : 4.6), z = uz * 8.4;
    if (s * ux < 0) x = -s * 3.45 * Math.pow(Math.abs(ux), 0.32); // flat inner face along the midline
    if (uy < 0) {
      // temporal lobe hangs low at the side, in the middle third
      y -= 1.6 * Math.exp(-(((uz - 0.1) / 0.38) ** 2)) * (-uy) * Math.max(0, s * ux);
      if (uz > 0.45) y *= 0.8; // flatter under the frontal lobe
    }
    const p = [cx + x, cy + y, cz + z];
    const g = 0.42 * (ridge(p[0] * 0.95 + 11, p[1] * 0.95, p[2] * 0.95) - 0.62) + 0.16 * (ridge(p[0] * 2.1, p[1] * 2.1 + 5, p[2] * 2.1) - 0.62);
    const n = new THREE.Vector3(x / 3.5, y / 5.5, z / 8.4).normalize();
    const lat = Math.max(0, s * ux) > 0.15 || uy > -0.2 ? 1 : 0.3;
    return [p[0] + n.x * g * lat, p[1] + n.y * g * lat, p[2] + n.z * g * lat];
  });
}

function buildCerebellum() {
  return deformSphere(56, 36, (ux, uy, uz) => {
    let x = ux * 4.8, y = uy * 2.6, z = uz * 3.1;
    const p = [x, 18.2 + y, -5.9 + z];
    p[1] += 0.12 * Math.sin(p[1] * 7.5 + p[2] * 1.4) * (1 - Math.abs(uy));
    p[2] += 0.55 * Math.exp(-((x / 0.9) ** 2)) * Math.max(0, -uz); // midline notch at the back
    return p;
  });
}

function buildLung(s) {
  const C = [s * 8.3, -9.4, -0.8];
  const H = V3(HEART_C);
  return deformSphere(64, 56, (ux, uy, uz) => {
    const ry = uy > 0 ? 12.9 : 11.8;
    let x = C[0] + ux * 7.6, y = C[1] + uy * ry, z = C[2] + uz * 9.8;
    // taper toward the apex, which tucks in toward the midline and back
    const t = clamp01((y - C[1]) / 12.5);
    const f = 1 - 0.4 * Math.pow(t, 1.5);
    x = C[0] * (1 - 0.55 * t) + (x - C[0]) * f;
    z = C[2] - 1.3 * t + (z - C[2]) * f;
    // round the top into a dome instead of a point
    if (uy > 0.75) y -= 1.6 * Math.pow((uy - 0.75) / 0.25, 2);
    // the inner face is flatter (the middle of the chest belongs to the heart)
    if (s * (x - C[0]) < 0) x = C[0] + (x - C[0]) * 0.62;
    // domed base sitting on the diaphragm, dipping lower at the back
    if (uy < 0) {
      const r2 = ((x - C[0]) / 7.6) ** 2 + ((z - C[2]) / 9.8) ** 2;
      const b = smooth01(-uy);
      y += 4.6 * (1 - Math.min(1, r2)) * b;
      y -= 3.0 * Math.max(0, -(z - C[2]) / 9.8) * b;
    }
    // keep inside the ribs
    const cg = cage(y);
    const maxX = cg.w - 0.5;
    if (Math.abs(x) > maxX) x = Math.sign(x) * maxX;
    const zMax = cg.cz + cg.d - 0.4, zMin = cg.cz - cg.d + 0.6;
    if (z > zMax) z = zMax;
    if (z < zMin) z = zMin;
    // make room for the heart (the left lung's cardiac notch is deeper)
    const p = new THREE.Vector3(x, y, z);
    const rh = s > 0 ? 6.5 : 5.3;
    const hc = s > 0 ? H.clone() : H.clone().add(new THREE.Vector3(-1.2, 0.4, -0.6));
    const d = p.distanceTo(hc);
    if (d < rh && y < -3.5) p.sub(hc).setLength(rh).add(hc);
    // stay off the spine
    if (Math.abs(p.x) < 4.2 && p.z < -3.0) p.x = s * 4.2;
    return [p.x, p.y, p.z];
  });
}

function buildHeart() {
  const prof = [[0.01, 5.0], [2.6, 4.6], [3.8, 3.4], [4.5, 1.6], [4.6, 0], [4.3, -1.8], [3.6, -3.6], [2.5, -5.0], [1.2, -5.9], [0.01, -6.3]]
    .map(([r, y]) => new THREE.Vector2(r, y));
  const g = new THREE.LatheGeometry(prof, 48);
  bake(g, new THREE.Matrix4().makeScale(1, 1, 0.74));
  // a shallow groove between the two ventricles
  const pos = g.attributes.position;
  for (let i = 0; i < pos.count; i++) {
    const x = pos.getX(i), y = pos.getY(i), z = pos.getZ(i);
    const ang = Math.atan2(x, z);
    const groove = 0.35 * Math.exp(-(((ang - 0.6) / 0.18) ** 2)) * smooth01((3 - y) / 4);
    const r = Math.hypot(x, z);
    if (r > 0.01) { const k = (r - groove) / r; pos.setX(i, x * k); pos.setZ(i, z * k); }
  }
  g.computeVertexNormals();
  bake(g, orientTo(new THREE.Vector3(0, -1, 0), HEART_AXIS));
  bake(g, new THREE.Matrix4().makeTranslation(...HEART_C));
  const ra = ellipsoid([HEART_C[0] - 3.3, HEART_C[1] + 1.6, HEART_C[2] - 0.4], [2.4, 2.6, 2.2]);
  const la = ellipsoid([HEART_C[0] + 0.4, HEART_C[1] + 2.6, HEART_C[2] - 3.1], [2.5, 1.9, 1.8]);
  return merge([g, ra, la]);
}

function buildPericardium() {
  const c = [HEART_C[0] - 0.5, HEART_C[1] + 1.0, HEART_C[2] - 0.6];
  return deformSphere(48, 36, (ux, uy, uz) => {
    const p = new THREE.Vector3(ux * 5.9, uy * 6.6, uz * 5.0);
    // tilt it along the heart's long axis
    p.applyMatrix4(orientTo(new THREE.Vector3(0, -1, 0), new THREE.Vector3(0.45, -0.75, 0.35)));
    if (uy > 0.55) p.y += 1.6 * (uy - 0.55); // the sac climbs a little up the great vessels
    return [c[0] + p.x, c[1] + p.y, c[2] + p.z];
  });
}

function buildChestWall() {
  const rows = 46, cols = 64, pos = [], idx = [];
  const y0 = 3.6, y1 = -27;
  for (let r = 0; r <= rows; r++) {
    const y = lerp(y0, y1, r / rows);
    const cg = cage(y);
    for (let c = 0; c <= cols; c++) {
      const th = (c / cols) * Math.PI * 2;
      let x = cg.w * Math.cos(th), z = cg.cz + cg.d * Math.sin(th);
      if (z < -3 && Math.abs(x) < 3) z = Math.max(z, -6.5); // the spine bulges into the chest at the back
      pos.push(x, y, z);
    }
  }
  for (let r = 0; r < rows; r++) for (let c = 0; c < cols; c++) {
    const a = r * (cols + 1) + c, b = a + cols + 1;
    idx.push(a, b, a + 1, b, b + 1, a + 1);
  }
  const g = new THREE.BufferGeometry();
  g.setAttribute('position', new THREE.Float32BufferAttribute(pos, 3));
  g.setIndex(idx); g.computeVertexNormals();
  return g;
}

function buildLarynx() {
  const thy = new THREE.CylinderGeometry(1.9, 1.6, 2.8, 32, 6, true, -1.95, 3.9);
  const pos = thy.attributes.position;
  for (let i = 0; i < pos.count; i++) {
    const x = pos.getX(i), z = pos.getZ(i);
    const ang = Math.atan2(x, z);
    pos.setZ(i, z * 1.05 + 0.5 * Math.pow(Math.max(0, Math.cos(ang)), 4) * smooth01((pos.getY(i) + 0.6) / 1.8));
  }
  thy.computeVertexNormals();
  bake(thy, new THREE.Matrix4().makeTranslation(0, 8.6, 1.8));
  const cricoid = new THREE.CylinderGeometry(1.42, 1.38, 1.0, 28, 1, true);
  bake(cricoid, new THREE.Matrix4().makeTranslation(0, 6.4, 1.9));
  const hyoid = new THREE.TorusGeometry(2.0, 0.24, 6, 24, Math.PI * 1.15);
  bake(hyoid, new THREE.Matrix4().makeRotationX(Math.PI / 2));
  const hm = (Math.PI * 1.15) / 2; // turn the U so its middle faces forward
  bake(hyoid, new THREE.Matrix4().makeRotationY(Math.atan2(-Math.cos(hm), Math.sin(hm))));
  bake(hyoid, new THREE.Matrix4().makeTranslation(0, 10.9, 1.4));
  return merge([thy, cricoid, hyoid]);
}

function buildTrachea() {
  const cv = curve(PATHS.trachea);
  const parts = [new THREE.TubeGeometry(cv, 60, 1.12, 16, false), tube(PATHS.bronchusL, 0.74, 32, 12), tube(PATHS.bronchusR, 0.8, 32, 12)];
  // C-shaped cartilage rings, open at the back
  const L = cv.getLength();
  for (let d = 0.4; d < L - 0.3; d += 0.85) {
    const t = d / L, c = cv.getPointAt(t), tg = cv.getTangentAt(t);
    const ring = new THREE.TorusGeometry(1.2, 0.17, 6, 20, Math.PI * 1.5);
    bake(ring, new THREE.Matrix4().makeRotationZ(-Math.PI / 4)); // gap ends up at the back
    bake(ring, new THREE.Matrix4().makeRotationX(Math.PI / 2));
    bake(ring, orientTo(new THREE.Vector3(0, 1, 0), tg));
    bake(ring, new THREE.Matrix4().makeTranslation(c.x, c.y, c.z));
    parts.push(ring);
  }
  return merge(parts);
}

function buildThyroidGland() {
  const l = ellipsoid([1.9, 4.4, 2.4], [0.9, 1.8, 0.8], 20, 16);
  const r = ellipsoid([-1.9, 4.4, 2.4], [0.9, 1.8, 0.8], 20, 16);
  const isth = ellipsoid([0, 4.0, 3.15], [1.4, 0.55, 0.35], 16, 10);
  return merge([l, r, isth]);
}

// ---------------------------------------------------------------------------
// Organ catalogue. kind sets the default look; group names let a scene say
// "show": ["neck"] instead of listing every structure.
// ---------------------------------------------------------------------------
export const COLORS = {
  bone: 0xe9e1cc, cartilage: 0xa6dbe8, lung: 0xe8939b, heart: 0xc74450, sac: 0xf1e2c4,
  artery: 0xe2434c, vein: 0x4a74d6, nerve: 0xf4d27c, brain: 0xeab8b2, muscle: 0xb85a4e,
  gland: 0xd98a63, airway: 0xbfe4ee, gut: 0xd8a07a, skin: 0x7fd3ff, wall: 0xd06a72,
};

export function buildAnatomy() {
  const spine = buildSpine();
  const ribs = buildRibs();
  const G = {
    skinSurface: buildSkinSurface(),
    skinLines: buildSkinLines(),
    skull: buildSkull(),
    brain: merge([brainHemisphere(1), brainHemisphere(-1)]),
    cerebellum: buildCerebellum(),
    brainstem: tube(PATHS.brainstem, 1.05, 24, 14),
    cord: tube(cordPoints(), 0.55, 200, 10),
    spine: spine.spine,
    discs: spine.discs,
    ribs: ribs.ribs,
    cartilage: ribs.cartilage,
    sternum: buildSternum(),
    clavicles: merge([tube(PATHS.clavicleL, 0.62, 40, 10), tube(PATHS.clavicleR, 0.62, 40, 10)]),
    scapulae: buildScapulae(),
    chestWall: buildChestWall(),
    lungL: buildLung(1),
    lungR: buildLung(-1),
    pleuraL: null, pleuraR: null,
    heart: buildHeart(),
    pericardium: buildPericardium(),
    aorta: merge([tube(PATHS.aorta, 1.25, 96, 14), tube(PATHS.brachioceph, 0.8, 16, 10)]),
    pulmonary: merge([tube(PATHS.pulmonary, 1.05, 40, 12), tube(PATHS.pulmonaryR, 0.85, 30, 10)]),
    svc: tube(PATHS.svc, 0.95, 20, 10),
    carotidL: merge([tube(PATHS.carotidL, 0.55, 48, 10), tube(PATHS.carotidLInt, 0.42, 32, 8), tube(PATHS.carotidLExt, 0.36, 16, 8)]),
    carotidR: merge([tube(PATHS.carotidR, 0.55, 48, 10), tube(PATHS.carotidRInt, 0.42, 32, 8), tube(PATHS.carotidRExt, 0.36, 16, 8)]),
    subclavian: merge([tube(PATHS.subclavianL, 0.5, 36, 8), tube(PATHS.subclavianR, 0.5, 36, 8)]),
    vertebralA: merge([tube(PATHS.vertebralL, 0.24, 60, 6), tube(PATHS.vertebralR, 0.24, 60, 6), tube(PATHS.basilar, 0.3, 12, 6)]),
    jugularIL: tube(PATHS.jugularIL, 0.72, 64, 10),
    jugularIR: tube(PATHS.jugularIR, 0.72, 64, 10),
    jugularEL: tube(PATHS.jugularEL, 0.42, 40, 8),
    jugularER: tube(PATHS.jugularER, 0.42, 40, 8),
    subclavVein: merge([tube(PATHS.subclavVeinL, 0.6, 30, 8), tube(PATHS.subclavVeinR, 0.6, 30, 8)]),
    larynx: buildLarynx(),
    trachea: buildTrachea(),
    thyroidGland: buildThyroidGland(),
    strapL: flatTube(PATHS.strapL, 0.75, 0.35),
    strapR: flatTube(PATHS.strapR, 0.75, 0.35),
    scm: merge([flatTube(PATHS.scmL, 1.25, 0.5), flatTube(PATHS.scmR, 1.25, 0.5)]),
    esophagus: tube(PATHS.esophagus, 0.7, 60, 10),
  };
  G.pleuraL = G.lungL.clone(); scaleAbout(G.pleuraL, [8.0, -9.5, -0.8], 1.05);
  G.pleuraR = G.lungR.clone(); scaleAbout(G.pleuraR, [-8.0, -9.5, -0.8], 1.05);
  return G;
}

function scaleAbout(g, c, s) {
  bake(g, new THREE.Matrix4().makeTranslation(-c[0], -c[1], -c[2]));
  bake(g, new THREE.Matrix4().makeScale(s, s, s));
  bake(g, new THREE.Matrix4().makeTranslation(c[0], c[1], c[2]));
}

// kind: color + how strongly it shows when nothing asks for it ("ghost").
export const ORGANS = {
  skull: { color: COLORS.bone, ghost: 0.10, label: 'Skull' },
  brain: { color: COLORS.brain, ghost: 0.12, label: 'Brain' },
  cerebellum: { color: COLORS.brain, ghost: 0.12, label: 'Cerebellum' },
  brainstem: { color: COLORS.brain, ghost: 0.10, label: 'Brain stem' },
  cord: { color: COLORS.nerve, ghost: 0.16, label: 'Spinal cord' },
  spine: { color: COLORS.bone, ghost: 0.14, label: 'Spine' },
  discs: { color: COLORS.cartilage, ghost: 0.08, label: 'Discs' },
  ribs: { color: COLORS.bone, ghost: 0.12, label: 'Ribs' },
  cartilage: { color: COLORS.cartilage, ghost: 0.08, label: 'Rib cartilage' },
  sternum: { color: COLORS.bone, ghost: 0.12, label: 'Breastbone' },
  clavicles: { color: COLORS.bone, ghost: 0.14, label: 'Collarbones' },
  scapulae: { color: COLORS.bone, ghost: 0.06, label: 'Shoulder blades' },
  chestWall: { color: COLORS.wall, ghost: 0.0, label: 'Chest wall' },
  lungL: { color: COLORS.lung, ghost: 0.10, label: 'Left lung' },
  lungR: { color: COLORS.lung, ghost: 0.10, label: 'Right lung' },
  pleuraL: { color: COLORS.artery, ghost: 0.0, label: 'Left chest cavity' },
  pleuraR: { color: COLORS.artery, ghost: 0.0, label: 'Right chest cavity' },
  heart: { color: COLORS.heart, ghost: 0.12, label: 'Heart' },
  pericardium: { color: COLORS.sac, ghost: 0.04, label: 'Heart sac' },
  aorta: { color: COLORS.artery, ghost: 0.10, label: 'Aorta' },
  pulmonary: { color: COLORS.vein, ghost: 0.08, label: 'Lung arteries' },
  svc: { color: COLORS.vein, ghost: 0.08, label: 'Great vein' },
  carotidL: { color: COLORS.artery, ghost: 0.12, label: 'Left carotid artery' },
  carotidR: { color: COLORS.artery, ghost: 0.12, label: 'Right carotid artery' },
  subclavian: { color: COLORS.artery, ghost: 0.08, label: 'Subclavian arteries' },
  vertebralA: { color: COLORS.artery, ghost: 0.08, label: 'Vertebral arteries' },
  jugularIL: { color: COLORS.vein, ghost: 0.12, label: 'Left internal jugular vein' },
  jugularIR: { color: COLORS.vein, ghost: 0.10, label: 'Right internal jugular vein' },
  jugularEL: { color: COLORS.vein, ghost: 0.12, label: 'Left external jugular vein' },
  jugularER: { color: COLORS.vein, ghost: 0.10, label: 'Right external jugular vein' },
  subclavVein: { color: COLORS.vein, ghost: 0.06, label: 'Subclavian veins' },
  larynx: { color: COLORS.cartilage, ghost: 0.12, label: 'Voice box' },
  trachea: { color: COLORS.airway, ghost: 0.12, label: 'Windpipe' },
  thyroidGland: { color: COLORS.gland, ghost: 0.06, label: 'Thyroid gland' },
  strapL: { color: COLORS.muscle, ghost: 0.08, label: 'Left strap muscles' },
  strapR: { color: COLORS.muscle, ghost: 0.06, label: 'Right strap muscles' },
  scm: { color: COLORS.muscle, ghost: 0.05, label: 'Neck muscles' },
  esophagus: { color: COLORS.gut, ghost: 0.05, label: 'Food pipe' },
};

export const GROUPS = {
  neck: ['larynx', 'trachea', 'carotidL', 'carotidR', 'jugularIL', 'jugularIR', 'jugularEL', 'jugularER', 'strapL', 'strapR', 'thyroidGland'],
  neckVessels: ['carotidL', 'carotidR', 'jugularIL', 'jugularIR', 'jugularEL', 'jugularER'],
  airway: ['larynx', 'trachea'],
  head: ['skull', 'brain', 'cerebellum', 'brainstem'],
  brainAll: ['brain', 'cerebellum', 'brainstem'],
  spineAll: ['spine', 'discs', 'cord'],
  chestBones: ['ribs', 'cartilage', 'sternum', 'clavicles'],
  lungs: ['lungL', 'lungR'],
  heartAll: ['heart', 'pericardium', 'aorta', 'pulmonary', 'svc'],
  vessels: ['aorta', 'carotidL', 'carotidR', 'subclavian', 'vertebralA', 'jugularIL', 'jugularIR', 'jugularEL', 'jugularER', 'svc', 'pulmonary'],
  arteriesUp: ['aorta', 'carotidL', 'carotidR', 'vertebralA', 'subclavian'],
  bones: ['skull', 'spine', 'ribs', 'sternum', 'clavicles', 'scapulae'],
};

// ---------------------------------------------------------------------------
// Named points that labels, lines and effects attach to.
// ---------------------------------------------------------------------------
const entry = [2.1, 5.6, skinZ(2.1, 5.6, 'front') - 0.05];
// The State's bullet angle, downward from level. Sworn (prelim Day 4): about 410 ft flat and
// 68 ft lower, about 9 degrees to his seated neck. Published estimates: about 6 degrees, range
// 4 to 10. The path is drawn at the sworn angle; bullet.range shades the estimate range.
// Sources and reasoning: site/docs/scorecard/exhibit/locations.md
export const BULLET_ANGLE = { sworn: 9, estimate: 6, min: 4, max: 10 };
// The State's one-line direction ("front to back, slightly left to right, and downward").
export function stateDir(deg) { return new THREE.Vector3(-0.15, -Math.tan((deg * Math.PI) / 180), -1).normalize(); }
export const STATE_DIR = stateDir(BULLET_ANGLE.sworn);
export const TRACK_LEN = 8.9;
const trackLen = TRACK_LEN;
const trackEnd = V3(entry).addScaledVector(STATE_DIR, trackLen);
const spineHit = V3(entry).addScaledVector(STATE_DIR, (entry[2] - (VERT.C6.z + 0.9)) / -STATE_DIR.z);
// Where the transmitter sat. Measured on the front camera (locations.md): the MagClip sits
// about 4.7 cm below the T-shirt neckline and 5 to 7 cm right of centre, just under the right
// collarbone, in every frame where it shows. DEVICE_XY is the centre of the 44 x 45 x 18.5 mm
// housing behind that clip. DEVICE_ZONE is the dashed outline: from the measured spot down to
// the written accounts that put it near or under the right nipple.
export const NIPPLE_R = [-10.0, -14.5];
export const DEVICE_XY = [-6.0, -4.2];
export const DEVICE_ZONE = { cx: -8.0, cy: -10.4, rx: 4.2, ry: 7.6 };
const device = [DEVICE_XY[0], DEVICE_XY[1], skinZ(DEVICE_XY[0], DEVICE_XY[1], 'front') + 0.95];
const jetVec = V3(entry).sub(V3(device));
// Angle of the line from the transmitter up to the wound, above level, in degrees.
export const JET_ANGLE = (Math.atan2(jetVec.y, Math.hypot(jetVec.x, jetVec.z)) * 180) / Math.PI;

export const ANCHORS = {
  entry,
  trackEnd: trackEnd.toArray(),
  spineHit: spineHit.toArray(),
  roof: V3(entry).addScaledVector(STATE_DIR, -95).toArray(),
  strapL: [1.6, 5.9, 3.95],
  carotidL: [2.4, 6.3, 1.3],
  ijvL: [3.4, 6.6, 1.05],
  ejvL: [5.5, 6.6, 0.85],
  cartilages: [0.4, 7.9, 3.9],
  thyroidCart: [0, 9.2, 4.1],
  cricoid: [0, 6.4, 3.35],
  tracheaRing: [0, 3.4, 2.75],
  windpipe: [0, 5.0, 2.95],
  neckBack: [0, 6.0, -8.6],
  c2: [1.3, 11.9, -2.6],
  c7: [1.3, 3.35, -3.1],
  c2c7: [1.5, 7.6, -2.5],
  cordGap: [0, 7.4, canalZ('C4')],
  apexL: [4.4, 2.6, -1.9],
  apexR: [-4.4, 2.6, -1.9],
  intercostalL: [7.2, -4.2, -8.8],
  intercostalR: [-7.2, -4.2, -8.8],
  hemothoraxL: [10.2, -19.5, -1.5],
  hemothoraxR: [-10.2, -19.5, -1.5],
  heart: [HEART_C[0] + 2.4, HEART_C[1] - 1.4, HEART_C[2] + 3.0],
  sac: [HEART_C[0] + 3.6, HEART_C[1] - 0.6, HEART_C[2] + 3.4],
  sacTop: [0.4, -4.9, 3.0],
  aortaArch: [0.6, -1.4, 1.2],
  vermis: [0, 18.4, -8.9],
  cerebellum: [3.3, 18.0, -7.9],
  parietalL: [3.9, 29.1, -2.6],
  parietalR: [-3.9, 29.1, -2.6],
  brainTop: [0, 30.0, -1.0],
  brainstem: [0, 17.6, -2.6],
  device,
  deviceLow: [DEVICE_ZONE.cx, DEVICE_ZONE.cy - DEVICE_ZONE.ry, skinZ(DEVICE_ZONE.cx, DEVICE_ZONE.cy - DEVICE_ZONE.ry, 'front') + 0.4],
  deviceHigh: [DEVICE_ZONE.cx, DEVICE_ZONE.cy + DEVICE_ZONE.ry, skinZ(DEVICE_ZONE.cx, DEVICE_ZONE.cy + DEVICE_ZONE.ry, 'front') + 0.4],
  nippleR: [NIPPLE_R[0], NIPPLE_R[1], skinZ(NIPPLE_R[0], NIPPLE_R[1], 'front') + 0.2],
  jetMid: V3(device).lerp(V3(entry), 0.5).toArray(),
  track6End: V3(entry).addScaledVector(stateDir(BULLET_ANGLE.estimate), TRACK_LEN).toArray(),
  sternalNotch: [0, -0.1, skinZ(0, -0.1, 'front')],
  collarR: [-6.0, 1.6, 6.2],
  lungL: [10.6, -9.0, 5.2],
  lungR: [-10.6, -9.0, 5.2],
  mouth: [0, 12.6, 8.4],
};

// Exhibit 11 findings, each tied to a place on an organ. A scene sets each one's state:
// "on" (just shown), "hit" (this explanation reaches it), "miss" (it does not, without a second cause).
export const FINDINGS = {
  entry: { anchor: 'entry', regions: [] },
  strap: { anchor: 'strapL', regions: [{ organ: 'strapL', c: [1.6, 5.8, 3.8], r: 2.2 }] },
  carotid: { anchor: 'carotidL', regions: [{ organ: 'carotidL', c: [2.4, 6.2, 1.3], r: 2.4 }] },
  ijv: { anchor: 'ijvL', regions: [{ organ: 'jugularIL', c: [3.4, 6.4, 1.0], r: 2.4 }] },
  ejv: { anchor: 'ejvL', regions: [{ organ: 'jugularEL', c: [5.5, 6.4, 0.85], r: 2.4 }] },
  cartilages: { anchor: 'cartilages', regions: [{ organ: 'larynx', c: [0.5, 7.6, 3.0], r: 3.4 }, { organ: 'trachea', c: [0.4, 4.0, 2.0], r: 2.8 }] },
  c2c7: { anchor: 'c2c7', regions: [{ organ: 'spine', box: [[0.2, 2.5, -9.5], [5.0, 12.8, 0.6]] }] },
  cord: { anchor: 'cordGap', regions: [{ organ: 'cord', box: [[-2, 4.6, -8.0], [2, 10.0, -2.0]] }] },
  apexL: { anchor: 'apexL', regions: [{ organ: 'lungL', c: [4.4, 1.9, -2.1], r: 3.8 }] },
  apexR: { anchor: 'apexR', regions: [{ organ: 'lungR', c: [-4.4, 1.9, -2.1], r: 3.8 }] },
  intercostalL: { anchor: 'intercostalL', regions: [{ organ: 'chestWall', c: [5.0, -0.6, -6.6], r: 5.2 }, { organ: 'chestWall', c: [8.6, -8.6, -8.4], r: 5.4 }] },
  intercostalR: { anchor: 'intercostalR', regions: [{ organ: 'chestWall', c: [-5.0, -0.6, -6.6], r: 5.2 }, { organ: 'chestWall', c: [-8.6, -8.6, -8.4], r: 5.4 }] },
  hemothoraxL: { anchor: 'hemothoraxL', regions: [{ organ: 'pleuraL', fill: -13.0 }] },
  hemothoraxR: { anchor: 'hemothoraxR', regions: [{ organ: 'pleuraR', fill: -13.0 }] },
  hemopericardium: { anchor: 'sac', regions: [{ organ: 'pericardium', fill: -8.0 }] },
  vermis: { anchor: 'vermis', regions: [{ organ: 'cerebellum', c: [0, 18.3, -7.4], r: 2.6 }] },
  parietal: { anchor: 'parietalL', regions: [{ organ: 'brain', c: [3.7, 28.3, -2.7], r: 4.6 }, { organ: 'brain', c: [-3.7, 28.3, -2.7], r: 4.6 }] },
};

// Camera shots: pos (where the camera stands) and look (what it aims at), in cm.
export const SHOTS = {
  'full': { pos: [62, 14, 150], look: [0, -6, 0] },
  'hero': { pos: [50, 12, 124], look: [0, -3, 0] },
  'full-front': { pos: [0, 6, 160], look: [0, -6, 0] },
  'upper-front-left': { pos: [55, 18, 95], look: [1, 2, 0] },
  'neck-front-left': { pos: [30, 12, 52], look: [1.5, 6, 0] },
  'neck-front': { pos: [0, 9, 58], look: [0.5, 6, 0] },
  'neck-left': { pos: [58, 9, 8], look: [0, 6.5, -1] },
  'neck-section': { pos: [2, 40, 13], look: [0.6, 4.6, -1.6] },
  'neck-back-left': { pos: [40, 14, -46], look: [0.5, 7, -2] },
  'spine-left': { pos: [60, 6, -6], look: [0, 6, -2.8] },
  'spine-back-left': { pos: [36, 12, -56], look: [0.8, 7, -3] },
  'spine-long-left': { pos: [96, 2, 10], look: [0, -6, -3] },
  'chest-front': { pos: [8, -4, 92], look: [0, -8, 0] },
  'chest-front-left': { pos: [52, 2, 80], look: [0, -7, 0] },
  'chest-front-right': { pos: [-48, 2, 82], look: [-1, -7, 0] },
  'chest-back': { pos: [-6, -2, -96], look: [0, -7, -2] },
  'chest-top': { pos: [6, 58, 46], look: [0, -5, 0] },
  'heart-front-left': { pos: [34, -4, 58], look: [1.4, -9.5, 3] },
  'heart-close': { pos: [24, -6, 38], look: [1.6, -10, 3] },
  'lungs-apex': { pos: [22, 20, 52], look: [0, 1.5, -1] },
  'head-left': { pos: [56, 23, 12], look: [0, 21, -1] },
  'head-back-left': { pos: [40, 30, -46], look: [0, 21, -3] },
  'head-top-back': { pos: [18, 64, -24], look: [0, 22, -2] },
  'head-neck-left': { pos: [70, 16, 6], look: [0, 14, -2] },
  'neck-to-heart': { pos: [56, 2, 70], look: [1, -3, 1] },
  'neck-to-brain': { pos: [62, 22, 34], look: [0.5, 15, -1] },
  'device-front': { pos: [-26, -2, 78], look: [-3, -5, 4] },
  'device-close': { pos: [-16, -8, 46], look: [-6, -11, 7] },
  'jet-side-right': { pos: [-64, -2, 46], look: [-2, -4, 3] },
};
