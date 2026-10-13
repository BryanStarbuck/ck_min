// stage.js: renders the anatomical bust and plays one "scene" at a time.
//
// A scene is plain data (see CLAUDE.md in site/docs/scorecard/exhibit/ for the full list):
//   cam      shot name from SHOTS in anatomy.js, or {pos:[x,y,z], look:[x,y,z]}
//   show     organs or groups drawn solid          focus   organs drawn solid and glowing
//   hide     organs removed entirely               skin    0..1, the see-through body mesh
//   findings {findingId: "on" | "hit" | "miss"}     section {y: number}  cut the body there
//   bullet   {in, track, zone, frags, needed:[...]} charge  {device, zone, jet, wave, radiate, surge}
//   labels   [[anchor, text, side, kind], ...]       measure [[fromAnchor|"path", toAnchor], ...]
// Everything not named in show/focus/hide is drawn as a faint ghost.

import * as THREE from './three.module.min.js';
import { buildAnatomy, ORGANS, GROUPS, ANCHORS, FINDINGS, SHOTS, STATE_DIR, PATHS, skinZ, insideSkin, DEVICE_ZONE, BULLET_ANGLE, stateDir, TRACK_LEN } from './anatomy.js';

const REDUCED = typeof matchMedia === 'function' && matchMedia('(prefers-reduced-motion: reduce)').matches;
const STATE_COL = {
  on: new THREE.Color(0.95, 0.30, 0.30),
  hit: new THREE.Color(1.0, 0.14, 0.16),
  miss: new THREE.Color(1.0, 0.62, 0.08),
};
const ease = (t) => (t < 0.5 ? 4 * t * t * t : 1 - Math.pow(-2 * t + 2, 3) / 2);
const easeOut = (t) => 1 - Math.pow(1 - t, 3);
const clamp01 = (t) => Math.min(1, Math.max(0, t));
const IN_PER_CM = 1 / 2.54;

// ---------------------------------------------------------------------------
// The organ shader: soft lighting, a glowing rim, injury glows, "obliterated"
// dissolve boxes, a rising fluid level, and the blast-wave ripple.
// ---------------------------------------------------------------------------
const ORGAN_VS = /* glsl */ `
#include <clipping_planes_pars_vertex>
varying vec3 vModel;
varying vec3 vNormalV;
varying vec3 vViewV;
void main() {
  vModel = position;
  vec4 mvPosition = modelViewMatrix * vec4(position, 1.0);
  vNormalV = normalize(normalMatrix * normal);
  vViewV = -mvPosition.xyz;
  gl_Position = projectionMatrix * mvPosition;
  #include <clipping_planes_vertex>
}`;

const ORGAN_FS = /* glsl */ `
#include <clipping_planes_pars_fragment>
uniform vec3 uColor;
uniform vec3 uRim;
uniform float uOpacity;
uniform float uFocus;
uniform float uDim;
uniform float uTime;
uniform vec4 uRegPos[6];
uniform vec4 uRegCol[6];
uniform vec4 uBoxMin[2];
uniform vec4 uBoxMax[2];
uniform vec4 uBoxCol[2];
uniform vec4 uFill;
uniform vec3 uFillCol;
uniform vec3 uFillEdge;
uniform vec4 uWave;
uniform vec3 uWaveCol;
uniform float uWaveOn;
varying vec3 vModel;
varying vec3 vNormalV;
varying vec3 vViewV;

float hash(vec3 p) { p = fract(p * 0.3183099 + 0.1); p *= 17.0; return fract(p.x * p.y * p.z * (p.x + p.y + p.z)); }
float noise(vec3 x) {
  vec3 i = floor(x); vec3 f = fract(x); f = f * f * (3.0 - 2.0 * f);
  return mix(mix(mix(hash(i), hash(i + vec3(1,0,0)), f.x), mix(hash(i + vec3(0,1,0)), hash(i + vec3(1,1,0)), f.x), f.y),
             mix(mix(hash(i + vec3(0,0,1)), hash(i + vec3(1,0,1)), f.x), mix(hash(i + vec3(0,1,1)), hash(i + vec3(1,1,1)), f.x), f.y), f.z);
}

void main() {
  #include <clipping_planes_fragment>
  vec3 n = normalize(vNormalV);
  vec3 v = normalize(vViewV);
  if (!gl_FrontFacing) n = -n;
  float ndv = clamp(dot(n, v), 0.0, 1.0);
  float fres = pow(1.0 - ndv, 2.2);
  vec3 L = normalize(vec3(-0.35, 0.7, 0.62));
  float diff = clamp(dot(n, L), 0.0, 1.0);
  float hemi = 0.5 + 0.5 * n.y;
  vec3 solid = uColor * (0.30 + 0.62 * diff + 0.16 * hemi);
  vec3 hv = normalize(L + v);
  solid += vec3(0.16) * pow(clamp(dot(n, hv), 0.0, 1.0), 30.0);
  solid += uRim * fres * (0.45 + 0.9 * uFocus);
  solid += uRim * uFocus * 0.10 * (0.5 + 0.5 * sin(uTime * 3.0));
  vec3 ghost = uColor * 0.45 + uRim * fres * 1.25;
  vec3 col = mix(solid, ghost, uDim);
  float alpha = uOpacity * mix(1.0, 0.25 + 0.75 * fres, uDim);

  for (int i = 0; i < 6; i++) {
    float amt = uRegCol[i].a;
    if (amt <= 0.001) continue;
    float d = distance(vModel, uRegPos[i].xyz);
    float r = uRegPos[i].w;
    float k = 1.0 - smoothstep(r * 0.3, r, d);
    k *= 0.7 + 0.6 * noise(vModel * 1.4 + uTime * 0.12);
    k = clamp(k * amt, 0.0, 1.0);
    vec3 hot = uRegCol[i].rgb * (1.05 + 0.25 * sin(uTime * 2.4));
    col = mix(col, hot, k);
    alpha = max(alpha, k * 0.92);
  }
  for (int j = 0; j < 2; j++) {
    float amt = uBoxCol[j].a;
    if (amt <= 0.001) continue;
    vec3 lo = uBoxMin[j].xyz; vec3 hi = uBoxMax[j].xyz;
    vec3 ins = step(lo, vModel) * step(vModel, hi);
    if (ins.x * ins.y * ins.z > 0.5) {
      float nz = noise(vModel * 1.35);
      float th = amt * 0.72;
      if (nz < th - 0.05) discard;
      float edge = 1.0 - smoothstep(0.0, 0.14, nz - th + 0.05);
      col = mix(col, uBoxCol[j].rgb * 1.35, max(edge, 0.6 * amt));
      alpha = max(alpha, 0.85 * amt);
    }
  }
  if (uFill.x > 0.001) {
    float lv = uFill.y + sin(vModel.x * 0.9 + uTime * 1.6) * 0.12;
    float below = 1.0 - smoothstep(lv - 0.3, lv + 0.3, vModel.y);
    float edge = 1.0 - smoothstep(0.0, 0.45, abs(vModel.y - lv));
    col = mix(col, uFillCol * (0.75 + 0.6 * fres), below * uFill.x);
    col = mix(col, uFillEdge * 1.3, edge * uFill.x);
    alpha = max(alpha, max(below * (0.38 + 0.4 * fres), edge) * uFill.x);
  }
  if (uWaveOn > 0.001) {
    float d = distance(vModel, uWave.xyz);
    float band = 1.0 - smoothstep(0.0, 2.6, abs(d - uWave.w));
    float behind = (1.0 - smoothstep(0.0, 9.0, uWave.w - d)) * step(d, uWave.w);
    col += uWaveCol * (band * 1.4 + behind * 0.25) * uWaveOn;
    alpha = max(alpha, (band * 0.7 + behind * 0.12) * uWaveOn);
  }
  gl_FragColor = vec4(col, alpha);
}`;

function organMaterial(color, rim, clip) {
  const arr4 = (n) => Array.from({ length: n }, () => new THREE.Vector4());
  return new THREE.ShaderMaterial({
    vertexShader: ORGAN_VS,
    fragmentShader: ORGAN_FS,
    transparent: true,
    depthWrite: false,
    side: THREE.DoubleSide,
    blending: THREE.AdditiveBlending,
    clipping: true,
    clippingPlanes: clip,
    uniforms: {
      uColor: { value: new THREE.Color(color) },
      uRim: { value: new THREE.Color(rim) },
      uOpacity: { value: 0.1 },
      uFocus: { value: 0 },
      uDim: { value: 1 },
      uTime: { value: 0 },
      uRegPos: { value: arr4(6) },
      uRegCol: { value: arr4(6) },
      uBoxMin: { value: arr4(2) },
      uBoxMax: { value: arr4(2) },
      uBoxCol: { value: arr4(2) },
      uFill: { value: new THREE.Vector4(0, -30, 0, 0) },
      uFillCol: { value: new THREE.Color(0.62, 0.03, 0.06) },
      uFillEdge: { value: new THREE.Color(1.0, 0.3, 0.3) },
      uWave: { value: new THREE.Vector4(0, 0, 0, 0) },
      uWaveCol: { value: new THREE.Color(1.0, 0.62, 0.22) },
      uWaveOn: { value: 0 },
    },
  });
}

function glowTexture() {
  const c = document.createElement('canvas');
  c.width = c.height = 128;
  const g = c.getContext('2d');
  const gr = g.createRadialGradient(64, 64, 0, 64, 64, 64);
  gr.addColorStop(0, 'rgba(255,255,255,1)');
  gr.addColorStop(0.25, 'rgba(255,255,255,0.55)');
  gr.addColorStop(1, 'rgba(255,255,255,0)');
  g.fillStyle = gr; g.fillRect(0, 0, 128, 128);
  const t = new THREE.CanvasTexture(c);
  t.colorSpace = THREE.SRGBColorSpace;
  return t;
}

const V3 = (a) => new THREE.Vector3(a[0], a[1], a[2]);

function resolveOrgans(list) {
  const out = new Set();
  (list || []).forEach((k) => {
    if (GROUPS[k]) GROUPS[k].forEach((o) => out.add(o));
    else if (ORGANS[k]) out.add(k);
  });
  return out;
}

// How strongly an organ shows when it is asked to "show". Big organs stay see-through
// so what sits behind them can still be read.
const SHOW_OPACITY = { lungL: 0.42, lungR: 0.42, pericardium: 0.22, chestWall: 0.0, pleuraL: 0, pleuraR: 0, skull: 0.22, scapulae: 0.3, cartilage: 0.6, discs: 0.6, scm: 0.4, thyroidGland: 0.7, esophagus: 0.6, brain: 0.9 };

export class Stage {
  constructor(host, opts = {}) {
    this.host = host;
    this.opts = opts;
    this.time = 0;
    this.yaw = 0; this.yawTarget = 0;
    this.autoRotate = !!opts.autoRotate;
    this.animations = [];
    this.labels = [];
    this.findingState = {};
    this.effectSig = { bullet: '', charge: '' };
    this.ready = false;

    host.classList.add('bt-stage');
    this.canvasWrap = document.createElement('div');
    this.canvasWrap.className = 'bt-canvas';
    host.appendChild(this.canvasWrap);
    this.svg = document.createElementNS('http://www.w3.org/2000/svg', 'svg');
    this.svg.setAttribute('class', 'bt-svg');
    this.svg.setAttribute('aria-hidden', 'true');
    host.appendChild(this.svg);
    this.labelLayer = document.createElement('div');
    this.labelLayer.className = 'bt-labels';
    this.labelLayer.setAttribute('aria-hidden', 'true');
    host.appendChild(this.labelLayer);

    try {
      this.renderer = new THREE.WebGLRenderer({ antialias: true, powerPreference: 'high-performance' });
    } catch (e) {
      this.fail();
      return;
    }
    this.renderer.setPixelRatio(Math.min(window.devicePixelRatio || 1, 2));
    this.renderer.setClearColor(0x04070b, 1);
    this.renderer.localClippingEnabled = true;
    this.canvasWrap.appendChild(this.renderer.domElement);
    this.renderer.domElement.setAttribute('role', 'img');
    this.renderer.domElement.setAttribute('aria-label', opts.ariaLabel || 'A see-through 3D model of the head, neck and chest');

    this.scene = new THREE.Scene();
    this.camera = new THREE.PerspectiveCamera(30, 1, 1, 2000);
    this.model = new THREE.Group();
    this.scene.add(this.model);
    this.clipPlane = new THREE.Plane(new THREE.Vector3(0, -1, 0), 1000);
    this.clipFloor = new THREE.Plane(new THREE.Vector3(0, 1, 0), 1000);
    this.clip = [this.clipPlane, this.clipFloor];
    this.glowTex = glowTexture();

    this.buildModel();
    this.buildEffects();
    this.camPos = V3(SHOTS.full.pos); this.camLook = V3(SHOTS.full.look);
    this.camFrom = null;
    this.applyCamera();
    this.bindPointer();
    this.resize();
    if (typeof ResizeObserver === 'function') {
      this.ro = new ResizeObserver(() => this.resize());
      this.ro.observe(host);
    } else window.addEventListener('resize', () => this.resize());
    this.clock = new THREE.Clock();
    this.ready = true;
    this.loop = this.loop.bind(this);
    requestAnimationFrame(this.loop);
  }

  fail() {
    this.host.classList.add('bt-nogl');
    const m = document.createElement('div');
    m.className = 'bt-nogl-msg';
    m.textContent = 'This browser could not start the 3D view (WebGL is off or unavailable). The written walk-through still works: keep scrolling.';
    this.host.appendChild(m);
  }

  // -------------------------------------------------------------------------
  buildModel() {
    const G = buildAnatomy();
    this.organs = {};
    const rimFor = (k) => (k.startsWith('jugular') || k === 'svc' || k === 'pulmonary' || k === 'subclavVein' ? 0x8fb4ff : k === 'cord' ? 0xffe9a8 : k.startsWith('lung') ? 0xffc2c6 : k === 'chestWall' ? 0xff9aa0 : 0x9fdcff);
    Object.keys(ORGANS).forEach((k) => {
      if (!G[k]) return;
      const mat = organMaterial(ORGANS[k].color, rimFor(k), this.clip);
      const mesh = new THREE.Mesh(G[k], mat);
      mesh.renderOrder = k.startsWith('pleura') || k === 'pericardium' || k === 'chestWall' ? 3 : 1;
      this.model.add(mesh);
      const g = ORGANS[k].ghost;
      this.organs[k] = { mesh, mat, op: g, opT: g, focus: 0, focusT: 0, ghost: g };
    });
    // the see-through body: a faint rim-lit surface plus a contour mesh of lines
    this.skinMat = organMaterial(0x0c2a3c, 0x67c8ff, this.clip);
    this.skinMat.uniforms.uOpacity.value = 0.55;
    this.skin = new THREE.Mesh(G.skinSurface, this.skinMat);
    this.skin.renderOrder = 8;
    this.model.add(this.skin);
    this.lineMat = new THREE.LineBasicMaterial({ color: 0x7fd3ff, transparent: true, opacity: 0.2, blending: THREE.AdditiveBlending, depthWrite: false, clippingPlanes: this.clip });
    this.skinLines = new THREE.LineSegments(G.skinLines, this.lineMat);
    this.skinLines.renderOrder = 9;
    this.model.add(this.skinLines);
    this.skinLevel = 1; this.skinLevelT = 1;

    // finding regions: give every region its own slot on its organ's material
    this.regions = [];
    const used = {};
    Object.entries(FINDINGS).forEach(([id, f]) => {
      f.regions.forEach((r) => {
        const o = this.organs[r.organ];
        if (!o) return;
        used[r.organ] = used[r.organ] || { s: 0, b: 0 };
        const reg = { id, organ: r.organ, amt: 0, amtT: 0, col: STATE_COL.on.clone() };
        if (r.box) {
          reg.type = 'box'; reg.slot = used[r.organ].b++;
          o.mat.uniforms.uBoxMin.value[reg.slot].set(...r.box[0], 0);
          o.mat.uniforms.uBoxMax.value[reg.slot].set(...r.box[1], 0);
        } else if (r.fill !== undefined) {
          reg.type = 'fill'; reg.level = r.fill; reg.low = r.organ === 'pericardium' ? -17.5 : -26;
        } else {
          reg.type = 'sphere'; reg.slot = used[r.organ].s++;
          o.mat.uniforms.uRegPos.value[reg.slot].set(...r.c, r.r);
        }
        this.regions.push(reg);
      });
    });

    // section disc (the cut face when the body is sliced)
    this.sectionDisc = null;
  }

  makeSectionDisc(y) {
    if (this.sectionDisc) { this.model.remove(this.sectionDisc); this.sectionDisc.geometry.dispose(); }
    const shape = new THREE.Shape();
    const ring = [];
    for (let i = 0; i < 96; i++) {
      const th = (i / 96) * Math.PI * 2;
      // walk outward from the centre until we leave the skin
      let r = 0.5, x = 0, z = 0;
      for (; r < 30; r += 0.08) {
        const nx = Math.cos(th) * r, nz = Math.sin(th) * r;
        if (!insideSkin(nx, y, nz)) break;
        x = nx; z = nz;
      }
      ring.push(new THREE.Vector2(x, -z));
    }
    shape.setFromPoints(ring);
    const g = new THREE.ShapeGeometry(shape);
    g.applyMatrix4(new THREE.Matrix4().makeRotationX(-Math.PI / 2));
    g.applyMatrix4(new THREE.Matrix4().makeTranslation(0, y + 0.01, 0));
    const m = new THREE.MeshBasicMaterial({ color: 0x3a0c12, transparent: true, opacity: 0.0, depthWrite: false, side: THREE.DoubleSide });
    this.sectionDisc = new THREE.Mesh(g, m);
    this.sectionDisc.renderOrder = 0;
    this.model.add(this.sectionDisc);
  }

  // -------------------------------------------------------------------------
  buildEffects() {
    const fx = (this.fx = {});
    const add = (o) => { this.model.add(o); return o; };
    const glowMat = (color, op) => new THREE.MeshBasicMaterial({ color, transparent: true, opacity: op, blending: THREE.AdditiveBlending, depthWrite: false });
    const line = (pts, r, color, op, seg = 64) => {
      const cv = new THREE.CatmullRomCurve3(pts.map(V3));
      const core = new THREE.Mesh(new THREE.TubeGeometry(cv, seg, r, 8, false), glowMat(color, op));
      const halo = new THREE.Mesh(new THREE.TubeGeometry(cv, seg, r * 3.2, 10, false), glowMat(color, op * 0.22));
      core.renderOrder = halo.renderOrder = 6;
      const grp = new THREE.Group(); grp.add(core, halo); add(grp);
      grp.userData = { meshes: [core, halo], curve: cv, p: 0 };
      grp.visible = false;
      return grp;
    };
    const dashed = (a, b, color) => {
      const A = V3(a), B = V3(b), len = A.distanceTo(B);
      const n = Math.max(6, Math.round(len / 1.1));
      const grp = new THREE.Group();
      const mat = new THREE.MeshBasicMaterial({ color, transparent: true, opacity: 0.95, depthWrite: false, depthTest: false });
      for (let i = 0; i < n; i++) {
        const p0 = A.clone().lerp(B, i / n), p1 = A.clone().lerp(B, (i + 0.58) / n);
        const seg = new THREE.Mesh(new THREE.CylinderGeometry(0.13, 0.13, p0.distanceTo(p1), 6), mat);
        seg.position.copy(p0).lerp(p1, 0.5);
        seg.quaternion.setFromUnitVectors(new THREE.Vector3(0, 1, 0), p1.clone().sub(p0).normalize());
        seg.renderOrder = 7;
        grp.add(seg);
      }
      grp.visible = false; grp.userData = { p: 0, n };
      return add(grp);
    };
    const sprite = (color, size) => {
      const s = new THREE.Sprite(new THREE.SpriteMaterial({ map: this.glowTex, color, transparent: true, blending: THREE.AdditiveBlending, depthWrite: false, depthTest: false }));
      s.scale.setScalar(size); s.renderOrder = 7; s.visible = false;
      return add(s);
    };

    const entry = V3(ANCHORS.entry), end = V3(ANCHORS.trackEnd);
    // --- bullet
    fx.incoming = line([ANCHORS.roof, ANCHORS.entry], 0.16, 0x9be7ff, 0.95, 40);
    fx.track = line([ANCHORS.entry, ANCHORS.trackEnd], 0.2, 0x9be7ff, 1.0, 40);
    fx.tip = sprite(0xcff4ff, 3.2);
    {
      const pts = [entry.x, entry.y, entry.z], idx = [];
      const steps = 24;
      for (let i = 0; i <= steps; i++) {
        const deg = BULLET_ANGLE.min + ((BULLET_ANGLE.max - BULLET_ANGLE.min) * i) / steps;
        const p = entry.clone().addScaledVector(stateDir(deg), TRACK_LEN);
        pts.push(p.x, p.y, p.z);
        if (i > 0) idx.push(0, i, i + 1);
      }
      const g = new THREE.BufferGeometry();
      g.setAttribute('position', new THREE.Float32BufferAttribute(pts, 3));
      g.setIndex(idx);
      const m = new THREE.MeshBasicMaterial({ color: 0x9be7ff, transparent: true, opacity: 0, side: THREE.DoubleSide, depthWrite: false, depthTest: false, blending: THREE.AdditiveBlending });
      fx.fan = add(new THREE.Mesh(g, m));
      fx.fan.renderOrder = 6; fx.fanOp = 0; fx.fanOpT = 0;
      fx.line6 = line([ANCHORS.entry, ANCHORS.track6End], 0.07, 0xe6fbff, 0.8, 16);
    }
    const len = entry.distanceTo(end);
    const capG = new THREE.CapsuleGeometry(3.4, len, 10, 32);
    capG.applyMatrix4(new THREE.Matrix4().makeRotationFromQuaternion(new THREE.Quaternion().setFromUnitVectors(new THREE.Vector3(0, 1, 0), STATE_DIR)));
    const mid = entry.clone().lerp(end, 0.5);
    capG.applyMatrix4(new THREE.Matrix4().makeTranslation(mid.x, mid.y, mid.z));
    const zoneMat = organMaterial(0x2b6f8a, 0x9be7ff, this.clip);
    zoneMat.uniforms.uOpacity.value = 0;
    fx.zone = add(new THREE.Mesh(capG, zoneMat));
    fx.zone.renderOrder = 5; fx.zoneOp = 0; fx.zoneOpT = 0;
    fx.frags = [];
    const fragDirs = [[0.3, -0.7, -0.4], [-0.5, -0.6, -0.3], [0.7, -0.2, -0.5], [-0.2, -0.9, 0.1], [0.1, -0.4, -0.9], [0.6, -0.8, 0.0], [-0.6, -0.3, -0.6]];
    fragDirs.forEach((d, i) => {
      const s = sprite(0xfff1c2, 1.1);
      s.userData = { dir: V3(d).normalize(), dist: 2.2 + (i % 3) * 0.9 };
      fx.frags.push(s);
    });
    fx.fragP = 0; fx.fragT = 0;
    fx.needed = {
      toC2: dashed(ANCHORS.entry, ANCHORS.c2, 0xffb02e),
      toSac: dashed(ANCHORS.trackEnd, ANCHORS.sacTop, 0xffb02e),
      toBrain: dashed(ANCHORS.trackEnd, ANCHORS.parietalL, 0xffb02e),
      toRight: dashed(ANCHORS.trackEnd, ANCHORS.hemothoraxR, 0xffb02e),
      toBack: dashed(ANCHORS.trackEnd, ANCHORS.intercostalR, 0xffb02e),
      toVermis: dashed(ANCHORS.trackEnd, ANCHORS.vermis, 0xffb02e),
    };

    // --- shaped charge
    const dev = V3(ANCHORS.device);
    const devG = new THREE.BoxGeometry(4.4, 4.5, 1.85, 2, 2, 1);
    devG.applyMatrix4(new THREE.Matrix4().makeRotationY(-0.28));
    devG.applyMatrix4(new THREE.Matrix4().makeRotationX(-0.14));
    devG.applyMatrix4(new THREE.Matrix4().makeTranslation(dev.x, dev.y, dev.z));
    const devMat = organMaterial(0x7a4318, 0xffb050, this.clip);
    devMat.uniforms.uOpacity.value = 0; devMat.uniforms.uDim.value = 0.1;
    fx.device = add(new THREE.Mesh(devG, devMat));
    fx.device.renderOrder = 6; fx.devOp = 0; fx.devOpT = 0;
    fx.devGlow = sprite(0xff9a3c, 11);
    fx.devGlow.position.copy(dev);
    // possible placement: a patch on the right chest from under the collarbone to below the pectoral
    const patchPts = [];
    for (let i = 0; i <= 40; i++) {
      const a = (i / 40) * Math.PI * 2;
      const x = DEVICE_ZONE.cx + Math.cos(a) * DEVICE_ZONE.rx, y = DEVICE_ZONE.cy + Math.sin(a) * DEVICE_ZONE.ry;
      patchPts.push(new THREE.Vector3(x, y, skinZ(x, y, 'front') + 0.35));
    }
    // a dashed outline (short tube segments, so it has real width) over a faint fill
    fx.patch = new THREE.Group();
    const patchMat = new THREE.MeshBasicMaterial({ color: 0xffb35a, transparent: true, opacity: 0, depthWrite: false, depthTest: false });
    for (let i = 0; i < patchPts.length - 1; i += 2) {
      const p0 = patchPts[i], p1 = patchPts[i + 1];
      const seg = new THREE.Mesh(new THREE.CylinderGeometry(0.14, 0.14, p0.distanceTo(p1), 6), patchMat);
      seg.position.copy(p0).lerp(p1, 0.5);
      seg.quaternion.setFromUnitVectors(new THREE.Vector3(0, 1, 0), p1.clone().sub(p0).normalize());
      fx.patch.add(seg);
    }
    const fill = [];
    const fillIdx = [];
    const cx = DEVICE_ZONE.cx, cy = DEVICE_ZONE.cy;
    fill.push(cx, cy, skinZ(cx, cy, 'front') + 0.3);
    patchPts.forEach((q) => fill.push(q.x, q.y, q.z - 0.05));
    for (let i = 1; i < patchPts.length; i++) fillIdx.push(0, i, i + 1 > patchPts.length - 1 ? 1 : i + 1);
    const fg = new THREE.BufferGeometry();
    fg.setAttribute('position', new THREE.Float32BufferAttribute(fill, 3));
    fg.setIndex(fillIdx);
    const fillMat = new THREE.MeshBasicMaterial({ color: 0xff9a3c, transparent: true, opacity: 0, depthWrite: false, depthTest: false, side: THREE.DoubleSide, blending: THREE.AdditiveBlending });
    fx.patch.add(new THREE.Mesh(fg, fillMat));
    fx.patch.userData = { patchMat, fillMat };
    fx.patch.renderOrder = 7;
    add(fx.patch);
    fx.patchOp = 0; fx.patchOpT = 0;
    // straight from the transmitter to the wound: the true angle, up and across his body
    fx.jet = line([ANCHORS.device, ANCHORS.jetMid, ANCHORS.entry], 0.28, 0xffc46b, 1.0, 48);
    fx.flash = sprite(0xffe3b0, 1);
    fx.flash.position.copy(dev);
    const waveMat = new THREE.ShaderMaterial({
      transparent: true, depthWrite: false, blending: THREE.AdditiveBlending, side: THREE.DoubleSide,
      uniforms: { uOp: { value: 0 }, uCol: { value: new THREE.Color(1.0, 0.55, 0.18) } },
      vertexShader: 'varying vec3 vN; varying vec3 vV; void main(){ vec4 mv = modelViewMatrix*vec4(position,1.0); vN = normalize(normalMatrix*normal); vV = -mv.xyz; gl_Position = projectionMatrix*mv; }',
      fragmentShader: 'uniform float uOp; uniform vec3 uCol; varying vec3 vN; varying vec3 vV; void main(){ float f = pow(1.0-abs(dot(normalize(vN), normalize(vV))), 2.5); gl_FragColor = vec4(uCol*(0.15+f), (0.05+f*0.8)*uOp); }',
    });
    fx.wave = add(new THREE.Mesh(new THREE.SphereGeometry(1, 48, 32), waveMat));
    fx.wave.position.copy(dev); fx.wave.renderOrder = 4; fx.wave.visible = false;
    fx.waveR = 0; fx.waveRun = -1;
    // damage radiating from one point at the front-left of the neck
    fx.rays = ['strapL', 'carotidL', 'ijvL', 'ejvL', 'cartilages', 'c2', 'c2c7', 'c7'].map((k) => {
      const a = entry.clone(), b = V3(ANCHORS[k]);
      const l = line([a.toArray(), a.clone().lerp(b, 0.5).toArray(), b.toArray()], 0.09, 0xffb45a, 0.9, 16);
      return l;
    });
    // pressure surge riding the arteries up to the brain
    const join = (...ps) => ps.flat();
    const routes = [
      join(PATHS.aorta.slice(0, 3).reverse().slice(-1), PATHS.carotidL, PATHS.carotidLInt.slice(1)),
      join([[0, -1.9, 2.4]], PATHS.carotidR, PATHS.carotidRInt.slice(1)),
      join(PATHS.subclavianL.slice(0, 2), PATHS.vertebralL.slice(1), PATHS.basilar.slice(1)),
      join([[-1.9, 1.2, 2.2]], PATHS.vertebralR, PATHS.basilar.slice(1)),
    ];
    fx.surge = routes.map((pts) => {
      const cv = new THREE.CatmullRomCurve3(pts.map(V3));
      const beads = [0, 0.33, 0.66].map((o) => { const s = sprite(0xff5a5a, 2.0); s.userData = { o }; return s; });
      return { cv, beads };
    });
    fx.surgeOn = 0; fx.surgeOnT = 0;
  }

  // -------------------------------------------------------------------------
  bindPointer() {
    const el = this.renderer.domElement;
    el.style.touchAction = 'pan-y';
    let down = false, lastX = 0;
    el.addEventListener('pointerdown', (e) => { down = true; lastX = e.clientX; this.userTurned = true; el.setPointerCapture(e.pointerId); this.host.classList.add('is-dragging'); });
    el.addEventListener('pointermove', (e) => {
      if (!down) return;
      const dx = e.clientX - lastX; lastX = e.clientX;
      this.yawTarget = Math.max(-Math.PI, Math.min(Math.PI, this.yawTarget + dx * 0.009));
    });
    const up = () => { down = false; this.host.classList.remove('is-dragging'); };
    el.addEventListener('pointerup', up); el.addEventListener('pointercancel', up);
    el.addEventListener('dblclick', () => { this.yawTarget = 0; });
  }

  resize() {
    if (!this.renderer) return;
    const r = this.host.getBoundingClientRect();
    const w = Math.max(10, r.width), h = Math.max(10, r.height);
    this.w = w; this.h = h;
    this.renderer.setSize(w, h, false);
    this.renderer.domElement.style.width = w + 'px';
    this.renderer.domElement.style.height = h + 'px';
    this.camera.aspect = w / h;
    this.camera.updateProjectionMatrix();
    this.svg.setAttribute('viewBox', `0 0 ${w} ${h}`);
  }

  // -------------------------------------------------------------------------
  shot(cam) {
    const s = typeof cam === 'string' ? SHOTS[cam] || SHOTS.full : cam || SHOTS.full;
    const pos = V3(s.pos), look = V3(s.look);
    // narrow (phone) stages need the camera further back to keep the framing
    const aspect = this.w / this.h || 1.5;
    if (aspect < 1.25) {
      const f = Math.min(1.9, Math.pow(1.25 / aspect, 0.8));
      pos.sub(look).multiplyScalar(f).add(look);
    }
    return { pos, look };
  }

  setScene(sc, { instant = false } = {}) {
    if (!this.ready) return;
    this.current = sc || {};
    const s = this.current;
    // camera
    const target = this.shot(s.cam || 'full');
    if (instant || REDUCED) { this.camPos.copy(target.pos); this.camLook.copy(target.look); this.camFrom = null; }
    else this.camFrom = { pos: this.camPos.clone(), look: this.camLook.clone(), to: target, t: 0, dur: 1.35 };
    this.yawTarget = 0;
    // organs
    const show = resolveOrgans(s.show), focus = resolveOrgans(s.focus), hide = resolveOrgans(s.hide);
    Object.entries(this.organs).forEach(([k, o]) => {
      const so = SHOW_OPACITY[k] !== undefined ? SHOW_OPACITY[k] : 1;
      if (hide.has(k)) { o.opT = 0; o.focusT = 0; }
      else if (focus.has(k)) { o.opT = Math.max(so, k.startsWith('lung') ? 0.6 : so); o.focusT = 1; }
      else if (show.has(k)) { o.opT = so; o.focusT = 0; }
      else { o.opT = o.ghost; o.focusT = 0; }
    });
    this.skinLevelT = s.skin === undefined ? 1 : s.skin;
    // findings
    this.findingState = Object.assign({}, s.findings || {});
    this.regions.forEach((r) => {
      const st = this.findingState[r.id];
      r.amtT = st && st !== 'off' ? 1 : 0;
      if (st && STATE_COL[st]) r.target = STATE_COL[st];
      if (instant || REDUCED) { r.amt = r.amtT; if (r.target) r.col.copy(r.target); }
    });
    // section
    if (s.section && typeof s.section.y === 'number') {
      this.clipPlane.constant = s.section.y;
      this.clipFloor.constant = -(s.section.y - (s.section.depth || 1.6));
      this.makeSectionDisc(s.section.y);
    } else {
      this.clipPlane.constant = 1000;
      this.clipFloor.constant = 1000;
      if (this.sectionDisc) this.sectionDisc.visible = false;
    }
    this.setBullet(s.bullet || null, instant);
    this.setCharge(s.charge || null, instant);
    this.setLabels(s.labels || [], s.measure || []);
    if (instant || REDUCED) {
      Object.values(this.organs).forEach((o) => { o.op = o.opT; o.focus = o.focusT; });
      this.skinLevel = this.skinLevelT;
    }
  }

  replay() {
    if (!this.current) return;
    this.effectSig = { bullet: '', charge: '' };
    this.setScene(this.current);
  }

  setBullet(b, instant) {
    const fx = this.fx;
    const sig = JSON.stringify(b || {});
    const changed = sig !== this.effectSig.bullet;
    this.effectSig.bullet = sig;
    b = b || {};
    fx.zoneOpT = b.zone ? 0.38 : 0;
    fx.fanOpT = b.range ? 0.4 : 0;
    fx.line6.visible = !!b.range; fx.line6.userData.p = 1;
    Object.entries(fx.needed).forEach(([k, l]) => {
      const on = (b.needed || []).includes(k);
      if (!on) { l.visible = false; l.userData.p = 0; return; }
      if (!l.visible || changed) { l.visible = true; l.userData.p = instant || REDUCED ? 1 : 0; l.userData.delay = 1.6; }
    });
    if (!changed && !instant) return;
    this.cancel('bullet');
    const show = (g, on) => { g.visible = !!on; g.userData.p = on && (instant || REDUCED) ? 1 : 0; };
    show(fx.incoming, b.in); show(fx.track, b.track);
    fx.tip.visible = false;
    fx.frags.forEach((f) => (f.visible = false));
    fx.fragP = 0;
    if (instant || REDUCED) {
      if (b.frags) { fx.fragP = 1; fx.frags.forEach((f) => (f.visible = true)); }
      return;
    }
    let t0 = 0.5;
    if (b.in) { this.anim('bullet', t0, 0.9, (p) => { fx.incoming.userData.p = easeOut(p); fx.tip.visible = p < 1; fx.tip.position.copy(fx.incoming.userData.curve.getPointAt(easeOut(p))); }); t0 += 0.9; }
    if (b.track) { this.anim('bullet', t0, 0.7, (p) => { fx.track.userData.p = easeOut(p); fx.tip.visible = p < 1; fx.tip.position.copy(fx.track.userData.curve.getPointAt(easeOut(p))); }); t0 += 0.7; }
    if (b.frags) this.anim('bullet', t0, 0.7, (p) => { fx.fragP = easeOut(p); fx.frags.forEach((f) => (f.visible = true)); });
  }

  setCharge(c, instant) {
    const fx = this.fx;
    const sig = JSON.stringify(c || {});
    const changed = sig !== this.effectSig.charge;
    this.effectSig.charge = sig;
    c = c || {};
    fx.devOpT = c.device ? 1 : 0;
    fx.patchOpT = c.zone ? 0.9 : 0;
    fx.surgeOnT = c.surge ? 1 : 0;
    if (!changed && !instant) return;
    this.cancel('charge');
    fx.jet.visible = !!c.jet; fx.jet.userData.p = c.jet && (instant || REDUCED) ? 1 : 0;
    fx.rays.forEach((r) => { r.visible = !!c.radiate; r.userData.p = c.radiate && (instant || REDUCED) ? 1 : 0; });
    fx.wave.visible = false; fx.waveRun = -1; fx.flash.visible = false;
    if (instant || REDUCED) return;
    let t0 = 0.6;
    if (c.wave || c.jet) {
      this.anim('charge', t0, 0.5, (p) => { fx.flash.visible = p < 1; fx.flash.scale.setScalar(4 + 26 * easeOut(p)); fx.flash.material.opacity = 1 - p; });
    }
    if (c.jet) this.anim('charge', t0, 0.45, (p) => { fx.jet.userData.p = easeOut(p); });
    if (c.wave) { fx.waveRun = 0; this.waveStart = this.time + t0; }
    if (c.radiate) this.anim('charge', t0 + 0.4, 0.9, (p) => fx.rays.forEach((r, i) => { r.userData.p = easeOut(clamp01(p * 1.6 - i * 0.08)); }));
  }

  anim(group, delay, dur, fn) {
    this.animations.push({ group, start: this.time + delay, dur, fn, done: false });
  }
  cancel(group) { this.animations = this.animations.filter((a) => a.group !== group); }

  // -------------------------------------------------------------------------
  setLabels(list, measures) {
    this.labelLayer.textContent = '';
    this.svg.textContent = '';
    this.labels = [];
    const mk = (anchor, text, side, kind, extra) => {
      const el = document.createElement('div');
      el.className = 'bt-label k-' + (kind || 'note');
      el.textContent = text;
      this.labelLayer.appendChild(el);
      const ln = document.createElementNS('http://www.w3.org/2000/svg', 'line');
      ln.setAttribute('class', 'bt-lead k-' + (kind || 'note'));
      ln.setAttribute('pathLength', '1');
      const dot = document.createElementNS('http://www.w3.org/2000/svg', 'circle');
      dot.setAttribute('class', 'bt-dot k-' + (kind || 'note'));
      dot.setAttribute('r', '3.6');
      this.svg.appendChild(ln); this.svg.appendChild(dot);
      const L = { anchor, el, ln, dot, side: side || 'auto', born: this.time, ...extra };
      this.labels.push(L);
      return L;
    };
    list.forEach(([anchor, text, side, kind]) => { if (ANCHORS[anchor] || anchor === 'path') mk(anchor, text, side, kind); });
    measures.forEach(([a, b, text]) => {
      const pa = a === 'path' ? this.nearestOnTrack(V3(ANCHORS[b])) : V3(ANCHORS[a]);
      const pb = V3(ANCHORS[b]);
      const d = pa.distanceTo(pb);
      const inch = Math.round(d * IN_PER_CM * 2) / 2;
      const label = text || `about ${inch} in (${Math.round(d)} cm)`;
      const L = mk(null, label, 'r', 'measure', { pa, pb, measure: true });
      const ml = document.createElementNS('http://www.w3.org/2000/svg', 'line');
      ml.setAttribute('class', 'bt-measure'); ml.setAttribute('pathLength', '1');
      this.svg.insertBefore(ml, this.svg.firstChild);
      L.ml = ml;
    });
  }

  nearestOnTrack(p) {
    const a = V3(ANCHORS.entry), b = V3(ANCHORS.trackEnd);
    const ab = b.clone().sub(a);
    const t = clamp01(p.clone().sub(a).dot(ab) / ab.lengthSq());
    return a.add(ab.multiplyScalar(t));
  }

  project(v) {
    const w = this.model.localToWorld(v.clone());
    const p = w.project(this.camera);
    return { x: (p.x * 0.5 + 0.5) * this.w, y: (-p.y * 0.5 + 0.5) * this.h, z: p.z };
  }

  // The on-screen box of the label attached to an anchor, if that label is showing.
  labelBox(id) {
    const L = this.labels.find((x) => x.anchor === id && x.el.classList.contains('is-in'));
    return L ? L.el.getBoundingClientRect() : null;
  }

  anchorClient(id) {
    if (!ANCHORS[id] || !this.ready) return null;
    const p = this.project(V3(ANCHORS[id]));
    const r = this.host.getBoundingClientRect();
    return { x: r.left + p.x, y: r.top + p.y, inView: p.x > 0 && p.x < this.w && p.y > 0 && p.y < this.h && p.z < 1 };
  }

  layoutLabels() {
    const W = this.w, H = this.h;
    const narrow = W < 520;
    const gap = narrow ? 34 : 64;
    const placed = [];
    this.labels.forEach((L) => {
      let ax, ay;
      if (L.measure) {
        const a = this.project(L.pa), b = this.project(L.pb);
        L.ml.setAttribute('x1', a.x); L.ml.setAttribute('y1', a.y); L.ml.setAttribute('x2', b.x); L.ml.setAttribute('y2', b.y);
        ax = (a.x + b.x) / 2; ay = (a.y + b.y) / 2;
      } else {
        const p = L.anchor === 'path' ? this.project(this.nearestOnTrack(V3(ANCHORS.trackEnd))) : this.project(V3(ANCHORS[L.anchor]));
        ax = p.x; ay = p.y;
      }
      const bw = L.el.offsetWidth, bh = L.el.offsetHeight;
      let side = L.side;
      if (side === 'auto') side = ax < W / 2 ? 'l' : 'r';
      let x, y;
      if (side === 'l') { x = ax - gap - bw; y = ay - bh / 2 - 14; }
      else if (side === 'r') { x = ax + gap; y = ay - bh / 2 - 14; }
      else if (side === 't') { x = ax - bw / 2; y = ay - gap - bh; }
      else { x = ax - bw / 2; y = ay + gap * 0.7; }
      x = Math.max(8, Math.min(W - bw - 8, x));
      y = Math.max(8, Math.min(H - bh - 8, y));
      placed.push({ L, x, y, bw, bh, ax, ay, side });
    });
    // push overlapping labels apart vertically
    placed.sort((a, b) => a.y - b.y);
    for (let i = 0; i < placed.length; i++) for (let j = 0; j < i; j++) {
      const A = placed[j], B = placed[i];
      const overlapX = A.x < B.x + B.bw && B.x < A.x + A.bw;
      if (overlapX && B.y < A.y + A.bh + 6) B.y = A.y + A.bh + 6;
    }
    placed.forEach(({ L, x, y, bw, bh, ax, ay }) => {
      if (y + bh > H - 4) y = H - bh - 4;
      L.el.style.transform = `translate(${Math.round(x)}px, ${Math.round(y)}px)`;
      // leader from the nearest edge of the label to the point
      const ex = ax < x ? x : ax > x + bw ? x + bw : ax;
      const ey = ay < y ? y : ay > y + bh ? y + bh : y + bh / 2;
      L.ln.setAttribute('x1', ex); L.ln.setAttribute('y1', ey);
      L.ln.setAttribute('x2', ax); L.ln.setAttribute('y2', ay);
      L.dot.setAttribute('cx', ax); L.dot.setAttribute('cy', ay);
      const age = this.time - L.born;
      const on = age > (REDUCED ? 0 : 0.9);
      L.el.classList.toggle('is-in', on);
      L.ln.classList.toggle('is-in', on);
      L.dot.classList.toggle('is-in', on);
      if (L.ml) L.ml.classList.toggle('is-in', on);
    });
  }

  // -------------------------------------------------------------------------
  applyCamera() {
    const drift = REDUCED ? 0 : 1;
    const t = this.time;
    const pos = this.camPos.clone();
    const dist = pos.distanceTo(this.camLook);
    pos.x += Math.sin(t * 0.21) * dist * 0.012 * drift;
    pos.y += Math.sin(t * 0.17) * dist * 0.008 * drift;
    this.camera.position.copy(pos);
    this.camera.lookAt(this.camLook);
  }

  loop() {
    requestAnimationFrame(this.loop);
    if (!this.ready || document.hidden) return;
    const dt = Math.min(0.05, this.clock.getDelta());
    this.time += dt;
    const k = 1 - Math.exp(-dt * 4.2);
    // camera move
    if (this.camFrom) {
      const c = this.camFrom;
      c.t += dt / c.dur;
      const e = ease(clamp01(c.t));
      this.camPos.lerpVectors(c.pos, c.to.pos, e);
      this.camLook.lerpVectors(c.look, c.to.look, e);
      if (c.t >= 1) this.camFrom = null;
    }
    if (this.autoRotate && !this.userTurned) this.yawTarget = Math.sin(this.time * 0.18) * 0.65;
    this.yaw += (this.yawTarget - this.yaw) * (1 - Math.exp(-dt * 5));
    this.model.rotation.y = this.yaw;
    this.applyCamera();
    // organs
    Object.entries(this.organs).forEach(([key, o]) => {
      o.op += (o.opT - o.op) * k;
      o.focus += (o.focusT - o.focus) * k;
      const u = o.mat.uniforms;
      u.uOpacity.value = o.op;
      u.uFocus.value = o.focus;
      u.uTime.value = this.time;
      const solid = o.op > 0.3;
      const injured = this.regionActive(key);
      u.uDim.value = solid ? Math.max(0, 1 - (o.op - 0.3) / 0.5) * 0.6 : 1;
      o.mat.blending = solid || injured ? THREE.NormalBlending : THREE.AdditiveBlending;
      o.mat.depthWrite = o.op > 0.95;
      o.mesh.visible = o.op > 0.004 || injured;
    });
    this.skinLevel += (this.skinLevelT - this.skinLevel) * k;
    this.lineMat.opacity = 0.2 * this.skinLevel;
    this.skinMat.uniforms.uOpacity.value = 0.5 * this.skinLevel;
    this.skinMat.uniforms.uTime.value = this.time;
    this.skin.visible = this.skinLines.visible = this.skinLevel > 0.01;
    // findings
    this.regions.forEach((r) => {
      r.amt += (r.amtT - r.amt) * (1 - Math.exp(-dt * 2.4));
      if (r.target) r.col.lerp(r.target, k);
      const u = this.organs[r.organ].mat.uniforms;
      if (r.type === 'sphere') u.uRegCol.value[r.slot].set(r.col.r, r.col.g, r.col.b, r.amt);
      else if (r.type === 'box') { u.uBoxCol.value[r.slot].set(r.col.r, r.col.g, r.col.b, r.amt); }
      else if (r.type === 'fill') { u.uFill.value.set(r.amt > 0.01 ? 1 : 0, r.low + (r.level - r.low) * r.amt, 0, 0); u.uFillEdge.value.copy(r.col); }
    });
    if (this.sectionDisc) {
      const on = this.clipPlane.constant < 900;
      this.sectionDisc.visible = on;
      this.sectionDisc.material.opacity += ((on ? 0.55 : 0) - this.sectionDisc.material.opacity) * k;
    }
    this.updateEffects(dt, k);
    // animations
    this.animations.forEach((a) => {
      const p = (this.time - a.start) / a.dur;
      if (p < 0) return;
      a.fn(clamp01(p));
      if (p >= 1) a.done = true;
    });
    this.animations = this.animations.filter((a) => !a.done);
    this.renderer.render(this.scene, this.camera);
    this.layoutLabels();
    if (this.onFrame) this.onFrame();
  }

  regionActive(organ) {
    return this.regions.some((r) => r.organ === organ && r.amt > 0.01);
  }

  updateEffects(dt, k) {
    const fx = this.fx;
    const draw = (g) => {
      if (!g.visible) return;
      g.userData.meshes.forEach((m) => {
        const total = m.geometry.index.count;
        m.geometry.setDrawRange(0, Math.floor((total * g.userData.p) / 6) * 6);
      });
    };
    [fx.incoming, fx.track, fx.jet, ...fx.rays].forEach(draw);
    fx.fanOp += (fx.fanOpT - fx.fanOp) * k;
    fx.fan.visible = fx.fanOp > 0.005;
    fx.fan.material.opacity = fx.fanOp;
    draw(fx.line6);
    fx.zoneOp += (fx.zoneOpT - fx.zoneOp) * k;
    fx.zone.visible = fx.zoneOp > 0.01;
    fx.zone.material.uniforms.uOpacity.value = fx.zoneOp;
    fx.zone.material.uniforms.uTime.value = this.time;
    const hit = V3(ANCHORS.spineHit);
    fx.frags.forEach((f) => {
      if (!f.visible) return;
      f.position.copy(hit).addScaledVector(f.userData.dir, f.userData.dist * fx.fragP);
      f.material.opacity = 0.5 + 0.5 * Math.sin(this.time * 6 + f.userData.dist);
    });
    Object.values(fx.needed).forEach((l) => {
      if (!l.visible) return;
      if (l.userData.delay > 0) { l.userData.delay -= dt; return; }
      l.userData.p = Math.min(1, l.userData.p + dt * 1.1);
      const shown = Math.ceil(l.userData.n * l.userData.p);
      l.children.forEach((c, i) => { c.visible = i < shown; });
    });
    // device
    fx.devOp += (fx.devOpT - fx.devOp) * k;
    fx.device.visible = fx.devOp > 0.01;
    fx.device.material.uniforms.uOpacity.value = fx.devOp;
    fx.device.material.uniforms.uFocus.value = 1;
    fx.device.material.uniforms.uTime.value = this.time;
    fx.device.material.blending = THREE.NormalBlending;
    fx.devGlow.visible = fx.devOp > 0.05;
    fx.devGlow.material.opacity = fx.devOp * (0.55 + 0.25 * Math.sin(this.time * 3.2));
    fx.patchOp += (fx.patchOpT - fx.patchOp) * k;
    fx.patch.visible = fx.patchOp > 0.01;
    fx.patch.userData.patchMat.opacity = fx.patchOp;
    fx.patch.userData.fillMat.opacity = fx.patchOp * 0.16;
    // blast wave
    const W = Object.values(this.organs);
    if (fx.waveRun >= 0) {
      const t = this.time - this.waveStart;
      if (t >= 0) {
        const p = clamp01(t / 2.4);
        fx.waveR = 46 * easeOut(p);
        fx.wave.visible = p < 1;
        fx.wave.scale.setScalar(Math.max(0.01, fx.waveR));
        fx.wave.material.uniforms.uOp.value = (1 - p) * 0.9;
        const on = p < 1 ? 1 - p * 0.6 : 0;
        W.forEach((o) => {
          o.mat.uniforms.uWave.value.set(fx.flash.position.x, fx.flash.position.y, fx.flash.position.z, fx.waveR);
          o.mat.uniforms.uWaveOn.value = on;
        });
        if (p >= 1) fx.waveRun = -1;
      }
    } else W.forEach((o) => { o.mat.uniforms.uWaveOn.value = 0; });
    // surge
    fx.surgeOn += (fx.surgeOnT - fx.surgeOn) * k;
    fx.surge.forEach((r) => r.beads.forEach((b) => {
      b.visible = fx.surgeOn > 0.02;
      if (!b.visible) return;
      const t = (this.time * 0.42 + b.userData.o) % 1;
      b.position.copy(r.cv.getPointAt(t));
      b.material.opacity = fx.surgeOn * Math.sin(Math.PI * t);
    }));
  }
}
