// PRISM-15 Rev A explainer video: deterministic scene program. window.renderFrame(T) renders the frame at global time T (s).
import * as THREE from 'three';
import { STLLoader } from 'three/addons/loaders/STLLoader.js';
import { RoomEnvironment } from 'three/addons/environments/RoomEnvironment.js';

const W = 1920, H = 1080;
const TL = await (await fetch('timeline.json')).json();
const P = await (await fetch('design/params.json')).json();
const EXPL = await (await fetch('cad/exploded_offsets.json')).json();
const parseCSV = (txt) => { const L = txt.trim().split('\n'); const h = L[0].split(','); return L.slice(1).map(r => { const c = r.split(','); const o = {}; h.forEach((k, i) => o[k] = c[i]); return o; }); };
const ART = parseCSV(await (await fetch('design/artwork_prism15_ttv.csv')).text());
const ARTG = parseCSV(await (await fetch('design/artwork_prism_g_example.csv')).text());

// ---------- renderer, scene, lights ----------
const canvas = document.getElementById('c'); canvas.width = W; canvas.height = H;
const Q = new URLSearchParams(location.search); const AA = Q.get('aa') !== '0', ENV = Q.get('env') !== '0';
const renderer = new THREE.WebGLRenderer({ canvas, antialias: AA, alpha: true, preserveDrawingBuffer: true });
renderer.setSize(W, H, false); renderer.setPixelRatio(1);
renderer.outputColorSpace = THREE.SRGBColorSpace; renderer.toneMapping = THREE.ACESFilmicToneMapping; renderer.toneMappingExposure = 1.05;
const scene = new THREE.Scene(); scene.background = null;
if (ENV && (Q.get('mat') || 'matcap') === 'ibl') { const pmrem = new THREE.PMREMGenerator(renderer); scene.environment = pmrem.fromScene(new RoomEnvironment(), 0.04).texture; }
const camera = new THREE.PerspectiveCamera(32, W / H, 0.5, 3000); camera.up.set(0, 0, 1);
scene.add(new THREE.HemisphereLight(0xe8eef4, 0x1a1410, 0.55));
const key = new THREE.DirectionalLight(0xffffff, 1.6); key.position.set(-160, -220, 300); scene.add(key);
const fill = new THREE.DirectionalLight(0xbfd4e6, 0.55); fill.position.set(240, 120, 140); scene.add(fill);
const rim = new THREE.DirectionalLight(0xffe2c0, 0.5); rim.position.set(40, 260, -40); scene.add(rim);

const MATMODE = Q.get('mat') || 'matcap';
// matcap textures baked once from the image-based-lighting materials: a sphere rendered head-on with the PMREM environment and the scene lights
const bakeMatcap = (mat) => {
  const rt = new THREE.WebGLRenderTarget(512, 512, { colorSpace: THREE.SRGBColorSpace }); const sc = new THREE.Scene();
  const pm = new THREE.PMREMGenerator(renderer); sc.environment = pm.fromScene(new RoomEnvironment(), 0.04).texture;
  const s = new THREE.Mesh(new THREE.SphereGeometry(1, 96, 64), mat); sc.add(s);
  const l1 = new THREE.DirectionalLight(0xffffff, 1.6); l1.position.set(-0.5, 0.9, 0.8); sc.add(l1);
  const l2 = new THREE.DirectionalLight(0xbfd4e6, 0.55); l2.position.set(0.9, -0.3, 0.5); sc.add(l2);
  const l3 = new THREE.DirectionalLight(0xffe2c0, 0.5); l3.position.set(0.2, 0.3, -1.0); sc.add(l3);
  sc.add(new THREE.HemisphereLight(0xe8eef4, 0x1a1410, 0.55));
  const cam = new THREE.OrthographicCamera(-1, 1, 1, -1, 0.1, 10); cam.position.set(0, 0, 3); cam.lookAt(0, 0, 0);
  renderer.setRenderTarget(rt); renderer.render(sc, cam); renderer.setRenderTarget(null); pm.dispose(); return rt.texture;
};
// cheap studio reflection map for the Phong+env mode: six canvas faces (+Z bright zenith with soft boxes, -Z dark floor)
const studioCube = (() => {
  const face = (paint) => { const c = document.createElement('canvas'); c.width = c.height = 256; const g = c.getContext('2d'); paint(g, c); return c; };
  const grad = (g, c, top, bot) => { const r = g.createLinearGradient(0, 0, 0, 256); r.addColorStop(0, top); r.addColorStop(1, bot); g.fillStyle = r; g.fillRect(0, 0, 256, 256); };
  const box = (g, x, y, w, h, a) => { const r = g.createRadialGradient(x + w / 2, y + h / 2, 4, x + w / 2, y + h / 2, Math.max(w, h)); r.addColorStop(0, `rgba(255,250,240,${a})`); r.addColorStop(0.55, `rgba(255,250,240,${a * 0.75})`); r.addColorStop(1, 'rgba(255,250,240,0)'); g.fillStyle = r; g.fillRect(x - w, y - h, 3 * w, 3 * h); };
  const px = face((g, c) => { grad(g, c, '#9fb1c2', '#2a3036'); box(g, 60, 30, 130, 70, 0.95); });
  const nx = face((g, c) => { grad(g, c, '#8d9eae', '#262b30'); box(g, 90, 60, 90, 50, 0.5); });
  const py = face((g, c) => { grad(g, c, '#95a7b8', '#272c31'); box(g, 40, 40, 170, 60, 0.7); });
  const ny = face((g, c) => { grad(g, c, '#aebfcf', '#2b3136'); box(g, 50, 20, 150, 80, 1.0); });
  const pz = face((g, c) => { grad(g, c, '#e8eef3', '#c4ced8'); box(g, 30, 60, 200, 90, 1.0); });
  const nz = face((g, c) => { grad(g, c, '#15181b', '#0a0c0e'); });
  const tex = new THREE.CubeTexture([px, nx, py, ny, pz, nz]); tex.colorSpace = THREE.SRGBColorSpace; tex.needsUpdate = true; return tex;
})();
const MC = {};
if (MATMODE === 'matcap') { MC.copper = bakeMatcap(new THREE.MeshStandardMaterial({ color: 0xc27a46, metalness: 0.88, roughness: 0.34 })); MC.copper3 = bakeMatcap(new THREE.MeshStandardMaterial({ color: 0xcf8650, metalness: 0.85, roughness: 0.30 })); MC.steel = bakeMatcap(new THREE.MeshStandardMaterial({ color: 0x9aa3a8, metalness: 0.9, roughness: 0.32 })); MC.mesh = bakeMatcap(new THREE.MeshStandardMaterial({ color: 0xb9c0c4, metalness: 0.7, roughness: 0.5 })); MC.dark = bakeMatcap(new THREE.MeshStandardMaterial({ color: 0x3a3d40, metalness: 0.3, roughness: 0.7 })); MC.ceramic = bakeMatcap(new THREE.MeshStandardMaterial({ color: 0xe9e4da, metalness: 0.0, roughness: 0.75 })); }
const mk = (color, kind) => { // kind: copper | steel | dark | ceramic | mesh
  if (MATMODE === 'matcap') { const tex = MC[kind] || MC.copper; return new THREE.MeshMatcapMaterial({ matcap: tex, color: 0xffffff }); }
  if (MATMODE === 'ibl') return new THREE.MeshStandardMaterial({ color, metalness: kind === 'copper' ? 0.88 : kind === 'steel' ? 0.9 : kind === 'mesh' ? 0.7 : kind === 'dark' ? 0.3 : 0.0, roughness: kind === 'copper' ? 0.34 : kind === 'steel' ? 0.32 : kind === 'ceramic' ? 0.75 : 0.6, envMapIntensity: 1.0 });
  if (MATMODE === 'std') return new THREE.MeshStandardMaterial({ color, metalness: kind === 'copper' ? 0.45 : kind === 'steel' ? 0.5 : 0.1, roughness: kind === 'copper' ? 0.38 : 0.5 });
  const spec = kind === 'copper' ? 0x7a4a2a : kind === 'steel' ? 0x8a9096 : kind === 'mesh' ? 0x707880 : 0x222222;
  if (MATMODE === 'penv' && (kind === 'copper' || kind === 'steel' || kind === 'mesh')) return new THREE.MeshPhongMaterial({ color, specular: spec, shininess: kind === 'copper' ? 42 : 70, envMap: studioCube, combine: THREE.MultiplyOperation, reflectivity: kind === 'copper' ? 0.55 : 0.6, emissive: 0x000000 });
  return new THREE.MeshPhongMaterial({ color, specular: spec, shininess: kind === 'copper' ? 48 : kind === 'steel' ? 70 : 12, emissive: 0x000000 });
};
const PE = MATMODE === 'penv';
const MAT = { copper: mk(PE ? 0xd98a54 : 0xc27a46, 'copper'), copper2: mk(PE ? 0xcf7f4a : 0xb86f3e, 'copper'), copper3: mk(PE ? 0xe2955e : 0xcf8650, 'copper3'), steel: mk(PE ? 0xb8c0c6 : 0x9aa3a8, 'steel'), dark: mk(0x3a3d40, 'dark'), ceramic: mk(0xe9e4da, 'ceramic'), mesh: mk(0xb9c0c4, 'mesh') };
if (MATMODE === 'matcap') { MAT.copper2.color.set(0xeadfd4); }
if (MATMODE !== 'ibl') { key.intensity = 2.6; fill.intensity = 1.1; rim.intensity = 0.9; scene.children.find(l => l.isHemisphereLight).intensity = 1.1; const top = new THREE.DirectionalLight(0xfff1e0, 0.7); top.position.set(20, 40, 400); scene.add(top); }
const PART_MAT = { core: MAT.copper, grate_land: MAT.copper2, grate_web: MAT.copper3, plenum: MAT.copper2, plenum_frames: MAT.copper, separator: MAT.copper3, cap: MAT.copper, boss_in: MAT.copper2, boss_out: MAT.copper2, guard: MAT.mesh, screws: MAT.steel, frame: MAT.steel, ttv_block: MAT.dark, ttv_tiles: MAT.ceramic };
const PLATE = ['core', 'grate_land', 'grate_web', 'plenum', 'plenum_frames', 'separator', 'cap', 'boss_in', 'boss_out', 'guard'];
const TTV = ['screws', 'frame', 'ttv_block', 'ttv_tiles'];
const SECT = ['core', 'grate_land', 'grate_web', 'plenum', 'plenum_frames', 'separator', 'cap', 'boss_in', 'boss_out', 'guard'];

// ---------- geometry loading ----------
const loader = new STLLoader();
const loadSTL = (url) => new Promise((res) => loader.load(url, g => { g.computeVertexNormals(); g.computeBoundingBox(); res(g); }, undefined, () => res(null)));
const full = new THREE.Group(); scene.add(full);
const secX = new THREE.Group(); scene.add(secX); secX.visible = false;
const secY = new THREE.Group(); scene.add(secY); secY.visible = false;
const M = {}, SX = {}, SY = {};
await Promise.all([...PLATE, ...TTV].map(async n => { const g = await loadSTL(`cad/${n}.stl`); if (!g) return; const m = new THREE.Mesh(g, PART_MAT[n]); m.name = n; M[n] = m; full.add(m); }));
await Promise.all(SECT.map(async n => { const gx = await loadSTL(`sections/x06_${n}.stl`); if (gx) { const m = new THREE.Mesh(gx, PART_MAT[n]); SX[n] = m; secX.add(m); } const gy = await loadSTL(`sections/y10_${n}.stl`); if (gy) { const m = new THREE.Mesh(gy, PART_MAT[n]); SY[n] = m; secY.add(m); } }));
const centroid = (n) => { const b = M[n].geometry.boundingBox; return new THREE.Vector3((b.min.x + b.max.x) / 2, (b.min.y + b.max.y) / 2, (b.min.z + b.max.z) / 2); };
const setVisible = (names, v) => names.forEach(n => { if (M[n]) M[n].visible = v; });
const resetParts = () => { Object.values(M).forEach(m => { m.position.set(0, 0, 0); m.visible = true; }); full.rotation.set(0, 0, 0); full.position.set(0, 0, 0); };

// ---------- helper geometry: heat slab, kerf highlights, orifice glow, contact shadow, arrows ----------
const LINES = P.lines.x, KIND = P.lines.kind;
const heat = new THREE.Mesh(new THREE.BoxGeometry(108, 108, 1.2), new THREE.MeshBasicMaterial({ color: 0xff4a1a, transparent: true, opacity: 0.0, depthWrite: false }));
heat.position.z = -0.8; scene.add(heat);
const kerfHi = new THREE.Group(); scene.add(kerfHi);
LINES.forEach((x, i) => { const k = KIND[i]; const m = new THREE.Mesh(new THREE.BoxGeometry(k.startsWith('edge') ? 0.5 : 0.6, 108, 2.1), new THREE.MeshBasicMaterial({ color: k === 'in' ? 0x4aa3e8 : 0xf08a3c, transparent: true, opacity: 0, depthWrite: false })); m.position.set(x, 0, 1.85); kerfHi.add(m); });
const oriGeo = new THREE.BoxGeometry(1, 1, 0.7);
const oriGlow = new THREE.InstancedMesh(oriGeo, new THREE.MeshBasicMaterial({ color: 0x9fe2ff, transparent: true, opacity: 0, depthWrite: false }), ART.length);
{ const mt = new THREE.Matrix4(); const s = new THREE.Vector3(); ART.forEach((r, i) => { s.set(+r.w_mm + 0.15, +r.h_mm + 0.15, 1); mt.compose(new THREE.Vector3(+r.x_mm, +r.y_mm, 4.3), new THREE.Quaternion(), s); oriGlow.setMatrixAt(i, mt); }); oriGlow.instanceMatrix.needsUpdate = true; scene.add(oriGlow); }
const shadowTex = (() => { const c = document.createElement('canvas'); c.width = c.height = 256; const g = c.getContext('2d'); const r = g.createRadialGradient(128, 128, 20, 128, 128, 128); r.addColorStop(0, 'rgba(0,0,0,0.55)'); r.addColorStop(1, 'rgba(0,0,0,0)'); g.fillStyle = r; g.fillRect(0, 0, 256, 256); return new THREE.CanvasTexture(c); })();
const shadow = new THREE.Mesh(new THREE.PlaneGeometry(420, 420), new THREE.MeshBasicMaterial({ map: shadowTex, transparent: true, depthWrite: false })); shadow.position.z = -0.95; scene.add(shadow);
const arrowGeo = (() => { const shaft = new THREE.CylinderGeometry(0.14, 0.14, 2.2, 10); shaft.translate(0, 1.1, 0); const head = new THREE.ConeGeometry(0.42, 0.9, 12); head.translate(0, 2.6, 0); const g = new THREE.BufferGeometry(); const pos = [], nor = []; [shaft, head].forEach(x => { const a = x.toNonIndexed(); pos.push(...a.attributes.position.array); nor.push(...a.attributes.normal.array); }); g.setAttribute('position', new THREE.Float32BufferAttribute(pos, 3)); g.setAttribute('normal', new THREE.Float32BufferAttribute(nor, 3)); return g; })();
const arrows = new THREE.Group(); scene.add(arrows); arrows.visible = false;
const mkArrow = (p, dir, color) => { const m = new THREE.Mesh(arrowGeo, new THREE.MeshStandardMaterial({ color, emissive: color, emissiveIntensity: 0.6, metalness: 0.2, roughness: 0.5 })); m.position.copy(p); m.quaternion.setFromUnitVectors(new THREE.Vector3(0, 1, 0), dir.clone().normalize()); arrows.add(m); return m; };

// ---------- particles ----------
const rng = (seed => () => { seed |= 0; seed = seed + 0x6D2B79F5 | 0; let t = Math.imul(seed ^ seed >>> 15, 1 | seed); t = t + Math.imul(t ^ t >>> 7, 61 | t) ^ t; return ((t ^ t >>> 14) >>> 0) / 4294967296; })(1234);
const COLD = new THREE.Color(0x4aa3e8), HOT = new THREE.Color(0xf07a2c);
class FlowPath { // waypoints with per-segment durations (s); position by arc length within each segment of the Catmull-Rom curve
  constructor(pts, durs, finStart, finEnd) {
    this.curve = new THREE.CatmullRomCurve3(pts.map(p => new THREE.Vector3(...p)), false, 'centripetal', 0.5);
    this.n = pts.length; const lens = [0]; const poly = this.curve.getSpacedPoints(600); // u of each waypoint via nearest sampled point
    this.uWp = pts.map(p => { let best = 0, bd = 1e9; const v = new THREE.Vector3(...p); poly.forEach((q, i) => { const d = q.distanceToSquared(v); if (d < bd) { bd = d; best = i; } }); return best / 600; });
    this.tWp = [0]; durs.forEach(d => this.tWp.push(this.tWp[this.tWp.length - 1] + d)); this.T = this.tWp[this.tWp.length - 1];
    this.finStart = this.tWp[finStart] / this.T; this.finEnd = this.tWp[finEnd] / this.T;
  }
  at(f) { // f in [0,1] of the time schedule -> point, temperature 0..1, stage index
    f = Math.max(0, Math.min(0.999999, f)); const t = f * this.T; let i = 0; while (i < this.n - 2 && this.tWp[i + 1] <= t) i++;
    const s = (t - this.tWp[i]) / (this.tWp[i + 1] - this.tWp[i]); const u = this.uWp[i] + (this.uWp[i + 1] - this.uWp[i]) * s;
    const temp = Math.max(0, Math.min(1, (f - this.finStart) / (this.finEnd - this.finStart)));
    return { p: this.curve.getPointAt(Math.max(0, Math.min(1, u))), temp, stage: i, s };
  }
}
const NEAR_OUT = (y) => [7, 21, 35, 49].reduce((a, b) => Math.abs(b - y) < Math.abs(a - y) ? b : a);
// view A path (x-cut): full loop from inlet boss to outlet boss; hero uses xin 0, y0 10, side -1, dir -1
function pathA(xin, y0, side, dir, durs) {
  const xout = xin + dir * 7.7143, yo = NEAR_OUT(y0), xo = side * 1.0;
  const pts = [[0, -20, 31], [0, -20, 26], [0.0, -20, 17.5], [xin * 0.35, -21, 16.6], [xin, -21, 16.0], [xin, -21, 12.0], [xin, -21, 7.4], [xin, y0, 7.4],
    [xin + xo, y0, 4.9], [xin + xo, y0, 4.3], [xin + xo * 0.9, y0, 3.95], [xin + xo * 0.3, y0, 3.5], [xin, y0, 2.4], [xin, y0, 1.6],
    [xin + dir * 1.6, y0, 1.75], [xin + dir * 6.1, y0, 1.75], [xout, y0, 1.9], [xout, y0, 3.4], [xout, y0, 4.3], [xout, y0, 7.4], [xout, yo, 7.4], [xout, yo, 12.0], [xout, yo, 16.0], [xout * 0.5, yo, 16.3]];
  if (yo === 49) pts.push([0, 49, 16.3], [0, 41, 16.6]);
  pts.push([0, 21, 17.5], [0, 21, 24], [0, 21, 31]);
  const d = durs || pts.slice(1).map(() => 1);
  return new FlowPath(pts, d, 13, 16);
}
// view B path (y-cut, in front of the cut face): orifice -> lip -> window -> kerf -> fins -> outlet kerf -> window -> row -> channel
function pathB(xin, side, dir, y) {
  const xout = xin + dir * 7.7143, xo = side * 1.0;
  const pts = [[xin, y, 9.0], [xin + xo, y, 5.0], [xin + xo, y, 4.3], [xin + xo * 0.9, y, 3.95], [xin + xo * 0.3, y, 3.5], [xin, y, 2.4], [xin, y, 1.6], [xin + dir * 1.6, y, 1.75], [xin + dir * 6.1, y, 1.75], [xout, y, 1.9], [xout, y, 3.4], [xout, y, 4.3], [xout, y, 5.5], [xout, y, 9.0]];
  return new FlowPath(pts, pts.slice(1).map(() => 1), 6, 9);
}
const HERO_DURS = [1.4, 1.6, 2.2, 2.3, 1.2, 1.3, 3.5, 1.2, 1.0, 1.2, 1.3, 1.2, 1.2, 2.0, 5.5, 1.5, 1.2, 0.8, 1.4, 1.6, 1.3, 1.6, 1.8, 1.5, 1.6, 1.6]; // sums to ~44 s for xin 0 (yo 21, no spine)
const partGeo = new THREE.SphereGeometry(0.34, 10, 8);
const partMat = new THREE.MeshStandardMaterial({ color: 0xffffff, emissive: 0xffffff, emissiveIntensity: 0.55, metalness: 0.0, roughness: 0.4 });
const PARTS_A = new THREE.InstancedMesh(partGeo, partMat, 520); PARTS_A.visible = false; scene.add(PARTS_A);
const PARTS_B = new THREE.InstancedMesh(partGeo, partMat, 520); PARTS_B.visible = false; scene.add(PARTS_B);
const hero = new THREE.Mesh(new THREE.SphereGeometry(0.95, 18, 14), new THREE.MeshStandardMaterial({ color: 0xffffff, emissive: 0xffffff, emissiveIntensity: 0.8, metalness: 0, roughness: 0.3 })); hero.visible = false; scene.add(hero);
const heroPathA = pathA(0, 10, -1, -1, HERO_DURS);
const heroPathB = pathB(0, -1, -1, 10.6);
const bgA = [], bgB = [];
{ const xins = [-46.2857, -30.8571, -15.4286, 0.0];
  for (let i = 0; i < 64; i++) { const xin = xins[i % 4]; const y0 = -50 + rng() * 100; const dir = xin === 0 ? -1 : (rng() < 0.5 ? -1 : 1); const side = -1; bgA.push({ path: pathA(xin, y0, side, dir), phase: rng(), loop: 14 + rng() * 6 }); }
  const ins = LINES.map((x, i) => [x, KIND[i]]).filter(([, k]) => k === 'in').map(([x]) => x);
  for (let i = 0; i < 64; i++) { const xin = ins[i % ins.length]; const dir = rng() < 0.5 ? -1 : 1; bgB.push({ path: pathB(xin, dir < 0 ? -1 : 1, dir, 10.6 + rng() * 0.3), phase: rng(), loop: 9 + rng() * 4 }); } }
const _m = new THREE.Matrix4(), _q = new THREE.Quaternion(), _s = new THREE.Vector3(1, 1, 1), _c = new THREE.Color();
function updateParticles(inst, list, t, perPath) {
  let k = 0; for (const b of list) { for (let j = 0; j < perPath; j++) { const f = ((t / b.loop) + b.phase + j / perPath) % 1; const r = b.path.at(f); _m.compose(r.p, _q, _s); inst.setMatrixAt(k, _m); _c.copy(COLD).lerp(HOT, r.temp); inst.setColorAt(k, _c); k++; } }
  for (; k < inst.count; k++) { _m.compose(new THREE.Vector3(0, 0, -500), _q, _s); inst.setMatrixAt(k, _m); }
  inst.instanceMatrix.needsUpdate = true; if (inst.instanceColor) inst.instanceColor.needsUpdate = true;
}

// ---------- UI (DOM rebuilt each frame; deterministic) ----------
const dom = document.getElementById('dom'), svg = document.getElementById('svg'), fadeEl = document.getElementById('fade'), zc = document.getElementById('zoning');
const ease = (x) => { x = Math.max(0, Math.min(1, x)); return x * x * (3 - 2 * x); };
const lerp = (a, b, t) => a + (b - a) * t;
const V3 = (a) => new THREE.Vector3(a[0], a[1], a[2]);
const ui = {
  els: [], lines: [],
  clear() { dom.innerHTML = ''; svg.innerHTML = ''; },
  add(cls, html, style, alpha = 1, rise = 0) { const d = document.createElement('div'); d.className = cls; d.innerHTML = html; Object.assign(d.style, style || {}); d.style.opacity = alpha; if (rise) d.style.transform = (d.style.transform || '') + ` translateY(${(1 - alpha) * rise}px)`; dom.appendChild(d); return d; },
  kicker(t, a = 1) { return this.add('kicker', t, {}, a); },
  chapter(t, a = 1) { return this.add('chapter', t, {}, a); },
  wordmark(a = 1) { return this.add('wordmark', 'PRISM-15 Rev A · design review · October 2026 · all performance figures are model predictions', {}, a); },
  caption(t, a = 1, left = false) { return this.add('caption', t, left ? { left: '96px', transform: 'none', maxWidth: '900px', bottom: '100px' } : {}, a, 14); },
  card(title, rows, a = 1, style) { const html = `<h3>${title}</h3>` + rows.map(r => `<div class="row"><span class="k">${r[0]}</span><span class="v ${r[2] || ''}">${r[1]}</span></div>`).join(''); return this.add('card', html, style, a, 18); },
  title(h1, h2, p, a = 1) { return this.add('title', `<h1>${h1}</h1><h2>${h2}</h2>${p ? `<p>${p}</p>` : ''}`, {}, a, 20); },
  big(t, a = 1, style) { return this.add('big', t, style, a, 20); },
  checklist(items, done, a = 1) { return this.add('check', items.map((s, i) => `<div class="${i < done ? 'done' : ''}">${s}</div>`).join(''), {}, a, 10); },
  label(world, text, sub, off, a = 1) { // world: Vector3; off: [dx, dy] screen offset, or 'auto' (side chosen from the anchor's screen half); the box is kept inside the frame
    const v = world.clone().project(camera); if (v.z > 1 || a <= 0.01) return; const x = (v.x + 1) / 2 * W, y = (1 - v.y) / 2 * H;
    const d = this.add('label', text + (sub ? `<small>${sub}</small>` : ''), { left: '0px', top: '0px' }, a);
    let r = d.getBoundingClientRect(); let dx, dy;
    if (off === 'auto' || Array.isArray(off) && off[0] === null) { const dyy = Array.isArray(off) ? off[1] : -80; dx = x < W / 2 ? 70 : -(r.width + 70); dy = dyy; } else { dx = off[0]; dy = off[1]; }
    let lx = Math.max(70, Math.min(W - r.width - 70, x + dx)), ly = Math.max(110, Math.min(H - r.height - 170, y + dy));
    d.style.left = `${lx}px`; d.style.top = `${ly}px`; r = d.getBoundingClientRect();
    const bx = (r.left + r.right) / 2 < x ? r.right : r.left, by = r.top + r.height / 2;
    const ln = document.createElementNS('http://www.w3.org/2000/svg', 'line'); ln.setAttribute('x1', bx); ln.setAttribute('y1', by); ln.setAttribute('x2', x); ln.setAttribute('y2', y); ln.setAttribute('stroke', `rgba(240,138,60,${0.9 * a})`); ln.setAttribute('stroke-width', '2.5'); svg.appendChild(ln);
    const c = document.createElementNS('http://www.w3.org/2000/svg', 'circle'); c.setAttribute('cx', x); c.setAttribute('cy', y); c.setAttribute('r', 6); c.setAttribute('fill', `rgba(240,138,60,${a})`); svg.appendChild(c);
  },
  fade(a) { fadeEl.style.opacity = Math.max(0, Math.min(1, a)); },
};
const appear = (t, t0, dur = 0.6) => ease((t - t0) / dur);
const window_ = (t, t0, t1, f = 0.5) => Math.min(appear(t, t0, f), 1 - appear(t, t1 - f, f)); // fade in at t0, out by t1
const setCam = (pos, look, fov) => { camera.position.copy(pos); camera.lookAt(look); camera.fov = fov; camera.updateProjectionMatrix(); };
const orbit = (t, r, zc, h, a0, w, look, shiftRight = 0) => { const a = a0 + w * t; const right = new THREE.Vector3(-Math.sin(a), Math.cos(a), 0); setCam(new THREE.Vector3(r * Math.cos(a), r * Math.sin(a), h), (look || new THREE.Vector3(0, 0, zc)).clone().add(right.multiplyScalar(shiftRight)), 30); };
const camKeys = (keys, t) => { let i = 0; while (i < keys.length - 2 && t >= keys[i + 1].t) i++; const k0 = keys[i], k1 = keys[i + 1]; const s = ease((t - k0.t) / (k1.t - k0.t)); setCam(V3(k0.pos).lerp(V3(k1.pos), s), V3(k0.look).lerp(V3(k1.look), s), lerp(k0.fov || 30, k1.fov || 30, s)); };
const CHAPTERS = { title: '', benchmark: 'The benchmark', exploded: 'The stack', core: 'The core', grate: 'The grate', flow: 'The coolant path', tie: 'The tie', zoning: 'Zoning', manufacturing: 'Manufacturing', datasheet: 'Predicted datasheet', honest: 'Concessions and programme', closing: '' };

// ---------- scenes ----------
const SC = {};
SC.title = { setup() { resetParts(); setVisible(TTV, false); heat.material.opacity = 0; }, frame(t, d) {
  full.rotation.z = -0.5 + 0.12 * t; const z = 0.5 + 0.5 * ease(t / 6);
  setCam(new THREE.Vector3(120 - 30 * z, -300 + 50 * z, 128 + 16 * z), new THREE.Vector3(-100, 10, 8), 28);
  shadow.material.opacity = 0.9;
  ui.title('PRISM-15 Rev A', 'A copper cold plate designed to beat the CoolIT 15 kW benchmark at its own operating point', 'Conventional manufacturing · one vacuum braze cycle · nothing printed', window_(t, 0.8, d - 0.2, 0.8));
  ui.wordmark(appear(t, 1.5)); } };

SC.benchmark = { setup() { resetParts(); setVisible(TTV, true); }, frame(t, d) {
  orbit(t, 330, 6, 150 + 10 * Math.sin(t * 0.2), -1.1, 0.045, new THREE.Vector3(0, 0, 4), 62);
  ui.kicker('The benchmark'); ui.chapter('02 / 12'); ui.wordmark();
  ui.card('CoolIT 15 kW · tech brief, June 2026', [['Heat load', '15 kW · 4 ceramic heaters'], ['Coolant', '18 LPM PG25 · 45 °C inlet'], ['Average case-to-inlet', '34.4 K · measured'], ['Hottest of 24 thermocouples', '44.2 K · measured'], ['Pressure drop', 'not published · ≈ 22 kPa reconstructed']], window_(t, 1.0, d + 5));
  if (t > 13.5) ui.card('PRISM-15 Rev A · predicted', [['Average, same paste', '31.1 K', 'good'], ['Maximum, same paste', '38.8 K', 'good'], ['Plate pressure drop, 20 mm ports', '7.6 kPa', 'good'], ['Load at 85 °C case, paste / pad', '15.7 / 18.4 kW', 'good'], ['Price per plate at 100k / yr', 'US$165 vs ≈ 126', 'bad']], appear(t, 13.5), { top: '600px' });
  if (t > 22.5) ui.caption('Every PRISM number is a model prediction (±25 % per term) until the first plates are tested', window_(t, 22.5, d), true); } };

const ORDER = ['core', 'grate_land', 'grate_web', 'plenum', 'plenum_frames', 'separator', 'cap', 'boss_in', 'boss_out', 'guard'];
const LABELS = { core: ['Core', 'skived OFE · 360 fins · 15 kerfs · base 0.85 mm'], grate_land: ['Land plate 1.30 mm', '15 windows · 7 recesses · ties every fin tip'], grate_web: ['Meter web 0.40 mm', '756 laser-pierced orifices, graded'], plenum: ['Plenum', 'one 0.8 mm sheet folded into 15 channels'], plenum_frames: ['End frames', 'pitch control, 16 slots'], separator: ['Separator 1.8 mm', '14 inlet + 32 outlet windows'], cap: ['Cap, drawn 1.0 mm', '6 arches · 2 cross domes · skirt lap seam'], boss_in: ['Port bosses', '20 mm bore · brazed in the cap pockets'], guard: ['Guard', '50 µm cup under the inlet dome'] };
SC.exploded = { setup() { resetParts(); setVisible(TTV, false); }, frame(t, d) {
  const t0 = 1.2, step = 2.35, dur = 1.5; full.rotation.z = -0.35 + 0.02 * t;
  ORDER.forEach((n, i) => { const k = ease((t - (t0 + i * step)) / dur); if (M[n]) M[n].position.z = EXPL[n] * 1.25 * k; });
  const prog = ease((t - 2) / 22);
  setCam(new THREE.Vector3(330 - 60 * prog, -270 + 40 * prog, 150 + 110 * prog), new THREE.Vector3(0, 0, 25 + 45 * prog), 30);
  ui.kicker('The stack'); ui.chapter('03 / 12'); ui.wordmark();
  ORDER.forEach((n, i) => { if (!LABELS[n] || n === 'boss_out') return; const a = window_(t, t0 + i * step + 0.5, t0 + i * step + 5.2, 0.45); if (a <= 0) return; const c = centroid(n).add(new THREE.Vector3(0, 0, EXPL[n] * 1.25)); const left = i % 2 === 0; c.x += left ? -58 : 58; c.applyMatrix4(full.matrixWorld); ui.label(c, LABELS[n][0], LABELS[n][1], 'auto', a); });
  if (t > 23) ui.caption('One vacuum braze cycle · every internal joint can only bypass · one external seam at the skirt lap', window_(t, 23, d), true); } };

SC.core = { setup() { resetParts(); setVisible(TTV, false); setVisible(PLATE.filter(n => n !== 'core'), false); }, frame(t, d) {
  camKeys([{ t: 0, pos: [-40, -230, 170], look: [0, 0, 2], fov: 30 }, { t: 7, pos: [-70, -95, 40], look: [-45, -45, 2], fov: 30 }, { t: 12, pos: [-74, -92, 30], look: [-44, -46, 2.0], fov: 28 }, { t: 18, pos: [-20, -120, 60], look: [-10, -20, 2], fov: 30 }, { t: 26, pos: [60, -170, 110], look: [0, 0, 2], fov: 30 }], t);
  const pulse = 0.35 + 0.25 * Math.sin(t * 3.0); kerfHi.children.forEach(m => m.material.opacity = window_(t, 14, 24, 1.0) * pulse);
  ui.kicker('The core'); ui.chapter('04 / 12'); ui.wordmark();
  ui.label(new THREE.Vector3(-40, -40, 2.8), 'Fins 0.15 mm · gaps 0.15 mm · 2.0 mm tall', '360 fins at 0.30 mm pitch, skived from one OFE blank', [null, -190], window_(t, 7.5, 14));
  ui.label(new THREE.Vector3(-54.5, -22, 0.4), 'Base 0.85 mm', 'fly-cut after brazing; 1.0 mm fallback', [null, 70], window_(t, 9.5, 14));
  ui.label(new THREE.Vector3(-15.43, -10, 2.8), '7 feed lines', 'kerfs 0.30 mm wide, 7.714 mm pitch', [-520, -80], window_(t, 15, 23));
  ui.label(new THREE.Vector3(7.71, 12, 2.8), '8 drain lines', 'edge lines at ±54 with half windows', [80, -60], window_(t, 16.5, 23));
  if (t > 20) ui.caption('A kerf under each line lets the coolant enter its fin segment over the full 2 mm height', window_(t, 20, d)); } };

SC.grate = { setup() { resetParts(); setVisible(TTV, false); setVisible(['plenum', 'plenum_frames', 'separator', 'cap', 'boss_in', 'boss_out', 'guard'], false); M.grate_land.position.z = 6; M.grate_web.position.z = 14; }, frame(t, d) {
  camKeys([{ t: 0, pos: [-10, -260, 180], look: [0, 0, 8], fov: 30 }, { t: 8, pos: [-30, -130, 90], look: [-8, -20, 8], fov: 30 }, { t: 15, pos: [-12, -62, 36], look: [-2, -22, 10], fov: 28 }, { t: 24, pos: [6, -40, 26], look: [-1, -18, 16], fov: 26 }, { t: 33, pos: [-60, -200, 150], look: [0, 0, 8], fov: 30 }], t);
  oriGlow.material.opacity = window_(t, 13, 30, 1.0) * (0.55 + 0.35 * Math.sin(t * 4)); oriGlow.position.z = 14;
  ui.kicker('The grate'); ui.chapter('05 / 12'); ui.wordmark();
  ui.label(new THREE.Vector3(-30.86, -30, 2.8 + 6), 'Land plate 1.30 mm', 'window 1.2 mm over every kerf; recess 2.7 × 0.8 mm on the feed lines', [-620, -30], window_(t, 2.5, 12));
  ui.label(new THREE.Vector3(-15.43 - 1.0, -24, 4.5 + 14), 'Meter web 0.40 mm', '756 orifices, 0.50 × 0.99–1.12 mm in five sizes', [60, -90], window_(t, 9, 18));
  ui.label(new THREE.Vector3(-7.71, -20, 4.5 + 14), 'Outlet row', 'balances the two fin segments beside each line', [60, 60], window_(t, 15, 22));
  ui.label(new THREE.Vector3(0 - 0.95, -18, 3.95 + 6), 'Jets land on the lip', '0.75 mm lip; fin-top velocity ≤ 0.5 m/s', [80, -40], window_(t, 24, 31));
  if (t > 11 && t < 23) ui.caption('Orifice areas graded over 1.13 : 1 cancel the plenum pressure profile: flow uniform within ±2.2 % from 9 to 36 LPM', window_(t, 11, 23));
  if (t > 24) ui.caption('The orifices sit 1.3 mm above the braze plane: filler cannot reach them', window_(t, 24, d)); } };

const STAGE_A = ['Inlet boss, 20 mm bore', 'Cross dome → two inlet arches', 'Separator window → plenum channel', 'Along the plenum channel, 0.6 m/s', '', '', '', '', 'Outlet channel → separator window', 'Outlet arches → cross dome', 'Outlet boss'];
SC.flow = {
  setup() { resetParts(); full.visible = false; PARTS_A.visible = true; hero.visible = true; heat.material.opacity = 0.32; },
  teardown() { full.visible = true; secX.visible = false; secY.visible = false; PARTS_A.visible = false; PARTS_B.visible = false; hero.visible = false; heat.material.opacity = 0; },
  frame(t, d) {
    const tA = 1.5, TA = heroPathA.T; const th = t - tA; const fA = th / TA;
    const viewB = th > heroPathA.tWp[8] && th < heroPathA.tWp[19];
    secX.visible = !viewB; secY.visible = viewB; PARTS_A.visible = !viewB; PARTS_B.visible = viewB;
    const r = heroPathA.at(Math.max(0, fA));
    updateParticles(PARTS_A, bgA, t, 3); updateParticles(PARTS_B, bgB, t, 3);
    let hp = r.p.clone(), stage = r.stage;
    if (viewB) { const fB = (th - heroPathA.tWp[8]) / (heroPathA.tWp[19] - heroPathA.tWp[8]); const rb = heroPathB.at(fB); hp = rb.p.clone(); hero.material.color.copy(COLD).lerp(HOT, rb.temp); hero.material.emissive.copy(hero.material.color); }
    else { hero.material.color.copy(COLD).lerp(HOT, r.temp); hero.material.emissive.copy(hero.material.color); }
    hero.position.copy(hp); hero.visible = th > 0 && th < TA; hero.scale.setScalar(viewB ? 0.45 : 1.0); PARTS_B.scale.setScalar(0.55); 
    if (viewB) { const s = (th - heroPathA.tWp[8]) / (heroPathA.tWp[19] - heroPathA.tWp[8]); const close = window_(s, 0.22, 0.80, 0.15); setCam(new THREE.Vector3(hp.x + 3 - 1.5 * close, 10.6 + 30 - 16 * close, hp.z + 8 - 4.2 * close), new THREE.Vector3(hp.x - 1.5, 10, Math.max(1.6, hp.z - 0.4)), 28 - 5 * close); }
    else if (th < 0) setCam(new THREE.Vector3(70, -120, 70), new THREE.Vector3(0, -20, 20), 30);
    else { const late = th > heroPathA.tWp[19]; let off; if (late) off = stage >= 22 ? new THREE.Vector3(34, -46, 40) : new THREE.Vector3(42, -16, 7); else if (stage >= 5) off = new THREE.Vector3(42, -18, 7); else if (stage >= 2) off = new THREE.Vector3(40, -30, 22); else off = new THREE.Vector3(48, -34, 34); setCam(hp.clone().add(off), hp.clone().add(new THREE.Vector3(-2, 0, -0.5)), 30); }
    heat.material.opacity = 0.22 + 0.1 * Math.sin(t * 2.5);
    ui.kicker('The coolant path'); ui.chapter('06 / 12'); ui.wordmark();
    const stageTxt = viewB ? ['Orifice: 1.54 m/s', 'Lands on the lip → window → kerf', 'Fins: 7.7 mm at 0.20 m/s, picking up heat', 'Outlet kerf → window → outlet row'][(() => { const s = (th - heroPathA.tWp[8]) / (heroPathA.tWp[19] - heroPathA.tWp[8]); return s < 0.12 ? 0 : s < 0.34 ? 1 : s < 0.78 ? 2 : 3; })()] : STAGE_A[Math.min(10, stage <= 3 ? stage : stage >= 19 ? (stage >= 24 ? 10 : stage >= 22 ? 9 : 8) : 3)];
    if (hero.visible && stageTxt) ui.label(hp, stageTxt, null, 'auto', 1);
    ui.label(new THREE.Vector3(-30, -30, -0.8), '15 kW · 117 cm² · four heaters', null, [-520, 60], window_(t, 2, 12));
    if (th > heroPathA.tWp[14] + 1 && th < heroPathA.tWp[16] + 2) ui.caption('Every fin segment starts at inlet temperature: 7.7 mm instead of 54 mm along the fins', 1);
    if (th > TA + 0.5) ui.caption('Inlet 45 °C → outlet 57.7 °C at 15 kW · plate pressure drop 7.6 kPa, 81 % inertial', window_(th, TA + 0.5, d - tA));
  } };

const pslab = new THREE.Mesh(new THREE.BoxGeometry(7.0, 0.6, 1.9), new THREE.MeshBasicMaterial({ color: 0x4aa3e8, transparent: true, opacity: 0, depthWrite: false })); pslab.position.set(-3.86, 10.3, 1.85); scene.add(pslab);
SC.tie = { setup() { resetParts(); full.visible = false; secY.visible = true; arrows.visible = true; arrows.clear();
    for (let i = 0; i < 4; i++) { const x = -6.4 + i * 1.7; const a1 = mkArrow(new THREE.Vector3(x, 10.4, 2.3), new THREE.Vector3(0, 0, -1), 0x7fc8f0); a1.scale.setScalar(0.3); const a2 = mkArrow(new THREE.Vector3(x + 0.85, 10.4, 1.35), new THREE.Vector3(0, 0, 1), 0x7fc8f0); a2.scale.setScalar(0.3); } },
  teardown() { full.visible = true; secY.visible = false; arrows.visible = false; pslab.material.opacity = 0; },
  frame(t, d) {
    camKeys([{ t: 0, pos: [-4, 60, 16], look: [-4, 10, 3], fov: 30 }, { t: 6, pos: [-3.6, 26, 6.0], look: [-3.8, 10, 2.4], fov: 24 }, { t: 13, pos: [-3.4, 19, 4.2], look: [-3.7, 10, 1.9], fov: 22 }, { t: 21, pos: [-5, 44, 13], look: [-4, 10, 3], fov: 30 }], t);
    const a = window_(t, 7, 16, 0.8); pslab.material.opacity = 0.28 * a * (0.7 + 0.3 * Math.sin(t * 3)); arrows.children.forEach((m, i) => { m.visible = a > 0.02; m.material.transparent = true; m.material.opacity = a; const up = i % 2 === 1; m.position.z = (up ? 1.35 : 2.3) + (up ? 1 : -1) * 0.18 * (0.5 + 0.5 * Math.sin(t * 3 + i)); });
    ui.kicker('The tie'); ui.chapter('07 / 12'); ui.wordmark();
    ui.label(new THREE.Vector3(-3.0, 10, 2.85), 'Fin tips brazed to the land', '≥ 70 % of every land strip bonded; 12–15 µm silver foil', [80, -110], window_(t, 2.5, 10));
    ui.label(new THREE.Vector3(-5.5, 10, 0.42), 'Base 0.85 mm', 'pressure carried between ties 0.30 mm apart: zero bow', [80, 70], window_(t, 7, 15));
    ui.label(new THREE.Vector3(-1.0, 10, 4.3), 'Orifice above the braze plane', null, [80, -60], window_(t, 11, 17));
    if (t > 14) ui.caption('12 kN of pressure load on the fin field is carried by 5,040 ties, not by the base', window_(t, 14, d)); } };

SC.zoning = { setup() { resetParts(); setVisible(TTV, false); setVisible(PLATE.filter(n => n !== 'grate_web'), false); }, frame(t, d) {
    full.rotation.z = 0.3 * Math.sin(t * 0.25); setCam(new THREE.Vector3(-150, -220, 230), new THREE.Vector3(-20, 10, 4), 26);
    ui.kicker('Zoning'); ui.chapter('08 / 12'); ui.wordmark();
    drawZoning(t, window_(t, 0.8, d + 2, 0.8));
    ui.big('Flow length follows heat flux', appear(t, 0.6), { left: '96px', top: '160px', width: '820px', fontSize: '56px' });
    ui.card('Rule from the 2-D cell model', [['≥ 250 W/cm²', '5–6 mm cells'], ['100–250 W/cm²', '6–8 mm (the 15 kW plate: 7.7)'], ['50–100 W/cm²', '8–12 mm'], ['< 50 W/cm²', '12 mm, bleeds only']], window_(t, 3, d + 2), { left: '96px', right: 'auto', top: '300px', width: '760px' });
    if (t > 11) ui.caption('A new package is a new meter web: a laser file and two to three weeks, not a new die', window_(t, 11, d), true); } };
function drawZoning(t, a) {
  zc.style.display = 'block'; zc.width = 840; const g = zc.getContext('2d'); g.clearRect(0, 0, 840, 840); if (a <= 0) return; g.globalAlpha = a;
  const s = 6.4, cx = 420, cy = 410; const X = x => cx + x * s, Y = y => cy - y * s;
  g.fillStyle = 'rgba(12,15,18,0.82)'; g.strokeStyle = 'rgba(255,255,255,0.14)'; g.lineWidth = 1.5; roundRect(g, 6, 6, 828, 828, 18); g.fill(); g.stroke();
  g.fillStyle = '#d08a5e'; g.font = '600 20px Inter, sans-serif'; g.fillText('PRISM-G EXAMPLE ARTWORK · 110 × 120 mm · 17 LINES', 34, 44);
  g.strokeStyle = 'rgba(255,255,255,0.25)'; g.lineWidth = 1; g.strokeRect(X(-55), Y(60), 110 * s, 120 * s);
  const dies = [[-15, -18.5], [15, -18.5], [-15, 18.5], [15, 18.5]]; const hbm = []; for (const sx of [-1, 1]) for (const cxh of [35.5, 48.5]) for (const cyh of [-21, -7, 7, 21]) hbm.push([sx * cxh, cyh]);
  const reveal = ease((t - 1.5) / 1.5);
  g.fillStyle = `rgba(240,122,44,${0.28 * reveal})`; g.strokeStyle = `rgba(240,160,100,${0.9 * reveal})`; g.lineWidth = 2; dies.forEach(([x, y]) => { g.fillRect(X(x - 13), Y(y + 16.5), 26 * s, 33 * s); g.strokeRect(X(x - 13), Y(y + 16.5), 26 * s, 33 * s); });
  g.fillStyle = `rgba(127,200,240,${0.22 * reveal})`; g.strokeStyle = `rgba(127,200,240,${0.8 * reveal})`; hbm.forEach(([x, y]) => { g.fillRect(X(x - 5.5), Y(y + 6), 11 * s, 12 * s); g.strokeRect(X(x - 5.5), Y(y + 6), 11 * s, 12 * s); });
  const linesOn = ease((t - 4) / 2.0); const seen = {};
  ARTG.forEach(r => { const lx = +r.line_x_mm; if (seen[lx]) return; seen[lx] = r.type; });
  Object.entries(seen).forEach(([lx, ty]) => { g.strokeStyle = ty === 'inlet' ? `rgba(74,163,232,${0.85 * linesOn})` : `rgba(240,138,60,${0.85 * linesOn})`; g.lineWidth = 2; g.beginPath(); g.moveTo(X(+lx), Y(60)); g.lineTo(X(+lx), Y(-60)); g.stroke(); });
  const dotsOn = ease((t - 6) / 2.5); if (dotsOn > 0) { ARTG.forEach(r => { g.fillStyle = r.type === 'inlet' ? `rgba(159,226,255,${0.9 * dotsOn})` : `rgba(255,190,140,${0.7 * dotsOn})`; g.fillRect(X(+r.x_mm) - 1.6, Y(+r.y_mm) - 1.6, 3.2, 3.2); }); }
  g.fillStyle = `rgba(244,241,236,${linesOn})`; g.font = '500 20px Inter, sans-serif'; g.fillText('5.5 mm lines over the dies', X(-33), Y(-62) + 24); g.fillText('11 mm over memory and margin', X(20), Y(-62) + 24);
  g.font = '500 18px Inter, sans-serif'; g.fillStyle = `rgba(201,196,187,${dotsOn})`; g.fillText('4 dies 26 × 33 mm at 350 W/cm² take 88 % of the flow · 16 HBM stacks never sit downstream of a die', 34, 818);
  g.globalAlpha = 1;
}
function roundRect(g, x, y, w, h, r) { g.beginPath(); g.moveTo(x + r, y); g.arcTo(x + w, y, x + w, y + h, r); g.arcTo(x + w, y + h, x, y + h, r); g.arcTo(x, y + h, x, y, r); g.arcTo(x, y, x + w, y, r); g.closePath(); }

const CHECK = ['Helium leak test, dry, every plate (≤ 10⁻⁶ mbar·L/s)', 'Infrared flow screen: no cold line', 'Fly-cut the die face to 0.85 mm, in-line ultrasonic gauge', 'Flush forward and reverse at 25 LPM', 'Proof at 15.5 bar with a 1 µm bulge scan: finds one unbonded strip', 'Pressure drop at 9, 18 and 27 LPM, ±10 %, Cpk ≥ 1.33'];
SC.manufacturing = { setup() { resetParts(); setVisible(TTV, false); }, frame(t, d) {
    const settle = ease((t - 1.0) / 7.5); ORDER.forEach((n, i) => { const k = ease((t - (0.8 + (ORDER.length - 1 - i) * 0.55)) / 1.6); if (M[n]) M[n].position.z = EXPL[n] * 1.6 * (1 - k); });
    full.rotation.z = -0.4 + 0.03 * t; setCam(new THREE.Vector3(260 - 40 * settle, -280, 170 - 30 * settle), new THREE.Vector3(-70, 0, 30 - 15 * settle), 30);
    const glow = window_(t, 9.5, 15, 1.5) * (0.55 + 0.45 * Math.sin(t * 2.2)); PLATE.forEach(n => { if (M[n]) { if (M[n].material.isMeshMatcapMaterial) { M[n].material.color.set(0xffffff).lerp(new THREE.Color(0xff5a14), 0.55 * glow); } else { M[n].material.emissive = new THREE.Color(0xff6a1a); M[n].material.emissiveIntensity = 0.9 * glow; } } });
    ui.kicker('Manufacturing'); ui.chapter('09 / 12'); ui.wordmark();
    if (t < 9.5) ui.caption('The stack goes into one fixture on two alumina pins with photo-etched silver foils between the layers', window_(t, 1.5, 9.5), true);
    if (t >= 9.5 && t < 15.5) ui.card('Vacuum braze, one cycle', [['Temperature', '795 °C, gas quench'], ['Vacuum', '10⁻⁵ mbar'], ['Fixture load', '0.08 MPa, differential-expansion springs'], ['Capacity', '60 plates per load · 5.5 h cycle'], ['Filler', '5.7 g BAg-8 preforms, silver-free route at G1']], window_(t, 9.5, 15.5));
    if (t >= 15.3) { const n = Math.min(CHECK.length, Math.floor((t - 15.3) / 1.45) + 1); ui.checklist(CHECK, n, appear(t, 15.3)); }
  }, teardown() { PLATE.forEach(n => { if (M[n]) { if (M[n].material.isMeshMatcapMaterial) M[n].material.color.set(n === 'grate_land' || n === 'plenum' || n === 'boss_in' || n === 'boss_out' ? 0xeadfd4 : 0xffffff); else M[n].material.emissiveIntensity = 0; } }); } };

SC.datasheet = { setup() { resetParts(); setVisible(TTV, true); arrows.visible = true; arrows.clear(); [[40, 66], [-40, 66], [66, 40], [66, -40], [40, -66], [-40, -66], [-66, 40], [-66, -40]].forEach(([x, y]) => mkArrow(new THREE.Vector3(x, y, 44), new THREE.Vector3(0, 0, -1), 0xf08a3c)); },
  teardown() { arrows.visible = false; },
  frame(t, d) {
    orbit(t, 300, 6, 160, 1.9, 0.035, new THREE.Vector3(0, 0, 6), 58);
    const a = window_(t, 1.5, 9, 0.8); arrows.children.forEach((m, i) => { m.visible = a > 0.02; m.position.z = 44 - 3 * (0.5 + 0.5 * Math.sin(t * 2.5 + i)); m.scale.setScalar(6.0); });
    ui.kicker('Predicted datasheet'); ui.chapter('10 / 12'); ui.wordmark();
    ui.label(new THREE.Vector3(40, 66, 40), '2,011 N through eight spring screws', 'load frame bears on the cap lands, never on the fin ties', 'auto', window_(t, 2, 9));
    ui.card('15 kW · 18 LPM PG25 · 45 °C inlet · 117 cm²', [['Average rise, phase-change pad', '29.2 K', 'good'], ['Maximum rise, phase-change pad', '34.9 K', 'good'], ['Average / maximum, paste', '31.1 / 38.8 K', 'good'], ['Plate pressure drop, 20 mm ports', '7.6 kPa', 'good'], ['Capacity at 85 °C case, pad', '18.4 kW', 'good'], ['Inlet allowed at 15 kW, pad', '50.1 °C', 'good'], ['Height at the bar · plate mass', '20.8 mm · 1.15 kg']], window_(t, 9, d + 2));
    if (t > 18) ui.caption('P10 to P90 on the pad average: 26.7 to 32.4 K · CoolIT measured 34.4 K on paste', window_(t, 18, d)); } };

SC.honest = { setup() { resetParts(); setVisible(TTV, false); }, frame(t, d) {
    full.rotation.z = 0.4 + 0.06 * t; setCam(new THREE.Vector3(240, -260, 120), new THREE.Vector3(0, 0, 8), 30);
    ui.kicker('Concessions and programme'); ui.chapter('11 / 12'); ui.wordmark();
    ui.card('What it does not win', [['Price per plate at 100k / yr', 'US$165 vs ≈ 126 · +31 %', 'bad'], ['Fouling life at equal filtration', 'ships with a 33 µm tray filter', 'bad'], ['Field record', 'none yet', 'bad'], ['Average at ≤ 0.5 LPM / kW, 100 cm², the 4 kW point', 'not claimed', 'bad']], window_(t, 0.8, 11.5), { left: '96px', right: 'auto', width: '760px' });
    if (t > 11) ui.card('The first US$2.3 M buys one answer', [['E1 tie-braze matrix', '24 coupons, 3 routes, 3 fixture loads'], ['Pass', 'every land strip ≥ 70 % bonded; a missed strip seen at proof'], ['Fallback', '1.0 mm base: +0.7 K, still ahead'], ['Gate G1', 'month 3 · Rev A freeze'], ['Public OCP-format result', 'month 12 · 5 plates × 3 re-mounts, independent repeat']], appear(t, 11), { left: '96px', right: 'auto', width: '820px', top: '150px' });
    if (t > 19) ui.caption('Programme US$8.4–10.7 M over 12 months · probability of a decisive pad result at month 12: 0.43', window_(t, 19, d)); } };

SC.closing = { setup() { resetParts(); setVisible(TTV, false); }, frame(t, d) {
    full.rotation.z = -0.5 + 0.1 * t; setCam(new THREE.Vector3(120, -300, 128), new THREE.Vector3(-100, 10, 8), 28);
    ui.title('PRISM-15 Rev A', 'Architecture · design definition · parametric CAD · predicted datasheet · manufacturing route · programme', 'docs/cooling in the design repository · design report, CAD package and review deck', window_(t, 0.6, d - 0.4, 0.8)); } };

// ---------- frame driver ----------
let current = null;
const findScene = (T) => { for (let i = 0; i < TL.scenes.length; i++) { const s = TL.scenes[i]; if (T < s.end || i === TL.scenes.length - 1) return [s, i]; } };
window.renderFrame = (T) => {
  const [s, i] = findScene(T); const t = T - s.start, d = s.end - s.start;
  if (current !== s.id) { if (current && SC[current].teardown) SC[current].teardown(); kerfHi.children.forEach(m => m.material.opacity = 0); oriGlow.material.opacity = 0; oriGlow.position.z = 0; heat.material.opacity = 0; zc.width = 840; zc.style.display = 'none'; SC[s.id].setup(); current = s.id; }
  ui.clear(); full.updateMatrixWorld(true);
  SC[s.id].frame(t, d);
  full.updateMatrixWorld(true);
  renderer.render(scene, camera);
  // scene fades: in over 0.6 s, out over the last 0.5 s (first scene in over 1.2 s, last scene out over 1.5 s)
  const fin = i === 0 ? 1.2 : 0.6, fout = i === TL.scenes.length - 1 ? 1.5 : 0.5;
  ui.fade(Math.max(1 - t / fin, (t - (d - fout)) / fout));
  return s.id;
};
window.ready = true;
