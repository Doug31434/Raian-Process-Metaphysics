# Energy center render fold-in: orange and indigo knots in the toroidal flow — Nov 7 2026

**Targets**: `claude/bwtc_3d_centers_render.html` (orange and indigo sections) and the Render Toolkit. Alternatives to the November 3 renders, made at Doug's direction; they don't replace them on the Design canvas unless Doug says so. This file replaces its own earlier versions of the same morning (the ajna-arranged flat petals, then propellers). The propeller source is kept below as an alternative.

**Doug (November 7).**
- The Gaelic-knot orange (the chart's triquetra) "is closer to what I want."
- Render the large sphere more like the toroidal flow.
- Let the sixth center follow the second center's pattern, with indigo's lobes in the ajna arrangement: one straight down at 6 o'clock, and two perpendicular to it at 3 and 9, mirroring each other.
- Every energy center shows its toroidal flow as the circle, present but faint, and reads in 3-D, like a still shot of something spinning too fast to see.

**How the knot is built (current: `knot.html`, `?form=orange|indigo`).**
- *Arcs.* One continuous thread through three lobes. Each arc joins two lobe tips (radius 1.3596) and bows toward the third, passing inside the center at 0.4977 toward the third tip. The over-and-under runs as z = 0.62 sin 2πs along each arc.
- *Orange.* With evenly spaced tips (330°, 210°, 90°) this reproduces the chart's TRIQ triquetra exactly: semicircles on each chord.
- *Indigo.* Tips at 0°, 180° and 270° give Doug's ajna arrangement.
- *Styling.* The chart's nested knots (scales 0.30/0.47/0.68/1.0, turned −0.66/−0.44/−0.22/0), the stream shader and the layer stack are carried over.
- *Toroidal flow.* Faint helical streamlines on two nested horn tori around the knot's spin axis (R0 0.69/b 0.69 ×16 at opacity 0.2; R0 0.66/b 0.42 ×10 at 0.11), one swirl per poloidal circuit (Hill–Moffatt, physics document §3). These replace the equator ring.
- *View.* The chart's orange camera (elevation 22°, distance 6.2, fov 30) and tilt (−0.42 about x), so indigo's side lobes stay level.
- *Finish.* Bloom (Toolkit bloom.py), then composite over a radially shaded sphere fill (orange 214,92,28; indigo 52,40,191) of radius 439 px.

**Used in.** The artifact *Two Triangles, One Star* (https://claude.ai/artifact/A9ECgBJicn9enYBUMPRMws), version 6.

**Rebuild.** Save the file beside `node_modules/three` (0.160.0), serve on port 8765, and shoot each form with the Toolkit's Playwright method.

## knot.html (current)

```html
<!doctype html>
<html><head><meta charset="utf-8">
<style>html,body{margin:0;background:transparent}canvas{display:block}</style>
<script type="importmap">{"imports":{"three":"./node_modules/three/build/three.module.js"}}</script>
</head><body>
<script type="module">
import * as THREE from 'three';
const P = new URLSearchParams(location.search);
const form = P.get('form') || 'orange';
const SIZE = 1000;
const F = {
  orange: {c:'#D2721E', g:'#EE9447', hot:'#ffb04a', field:'#FFD0A0', tips:[330, 210, 90]},   // the chart's triquetra: lobes at 12, 4 and 8 o'clock
  indigo: {c:'#5546C0', g:'#7C6EE0', hot:'#CFC8FF', field:'#C9C2FF', tips:[0, 180, 270]}     // Doug: lobes at 6 o'clock, and 3 and 9, mirrored (ajna)
}[form];
const col = new THREE.Color(F.c), glow = new THREE.Color(F.g), hot = col.clone().lerp(new THREE.Color(F.hot), 0.5);

const renderer = new THREE.WebGLRenderer({antialias:true, alpha:true, preserveDrawingBuffer:true});
renderer.setPixelRatio(1); renderer.setSize(SIZE, SIZE); renderer.setClearColor(0x000000, 0);
renderer.outputColorSpace = THREE.SRGBColorSpace;
document.body.appendChild(renderer.domElement);
const scene = new THREE.Scene();
const camera = new THREE.PerspectiveCamera(30, 1, 0.1, 100);
const elev = THREE.MathUtils.degToRad(22), dist = 6.2;   // the chart's orange camera
camera.position.set(0, Math.sin(elev)*dist, Math.cos(elev)*dist); camera.lookAt(0,0,0);

// the sphere: the outer surface of the toroidal field, faint
const halo = new THREE.Mesh(new THREE.SphereGeometry(1.42, 96, 64), new THREE.ShaderMaterial({
  transparent:true, depthWrite:false, uniforms:{c:{value:glow}},
  vertexShader:`varying vec3 vN; varying vec3 vV; void main(){ vec4 mv = modelViewMatrix*vec4(position,1.0); vN = normalize(normalMatrix*normal); vV = normalize(-mv.xyz); gl_Position = projectionMatrix*mv; }`,
  fragmentShader:`uniform vec3 c; varying vec3 vN; varying vec3 vV; void main(){ float f = 1.0 - max(dot(vN, vV), 0.0); gl_FragColor = vec4(c, pow(f, 2.2)*0.85 + 0.06); }`}));
halo.renderOrder = 10; scene.add(halo);
{ const N = 90, pos = [];
  for (let i=0;i<N;i++){ const y = 1 - (i+0.5)/N*2, r = Math.sqrt(1-y*y), th = i*Math.PI*(3-Math.sqrt(5)); const d = new THREE.Vector3(Math.cos(th)*r, y, Math.sin(th)*r);
    pos.push(...d.clone().multiplyScalar(1.3).toArray(), ...d.clone().multiplyScalar(1.41).toArray()); }
  const g = new THREE.BufferGeometry(); g.setAttribute('position', new THREE.Float32BufferAttribute(pos,3));
  scene.add(new THREE.LineSegments(g, new THREE.LineBasicMaterial({color:glow, transparent:true, opacity:0.4}))); }

const G = new THREE.Group(); scene.add(G);   // local frame: the knot lies in x–y; its spin axis is z

// the toroidal flow: faint helical streamlines on nested horn tori around the spin axis (one swirl per poloidal circuit)
const fieldMat = (o) => new THREE.ShaderMaterial({ transparent:true, depthWrite:false,
  uniforms:{c:{value:new THREE.Color(F.field)}, o:{value:o}, camD:{value:dist}},
  vertexShader:`uniform float camD; varying float vF; void main(){ vec4 mv = modelViewMatrix*vec4(position,1.0); vF = clamp((mv.z + camD)/1.4*0.5+0.5, 0.0, 1.0); gl_Position = projectionMatrix*mv; }`,
  fragmentShader:`uniform vec3 c; uniform float o; varying float vF; void main(){ gl_FragColor = vec4(c, o*(0.2 + 0.8*vF));
#include <colorspace_fragment>
}`});
for (const [R0, b, n, o] of [[0.69, 0.69, 16, 0.2], [0.66, 0.42, 10, 0.11]]) {
  for (let i=0;i<n;i++) { const phi0 = i*2*Math.PI/n, pts = [];
    for (let k=0;k<=360;k++){ const t = k/360*2*Math.PI, phi = phi0 + t, rr = R0 + b*Math.cos(t); pts.push(new THREE.Vector3(rr*Math.cos(phi), rr*Math.sin(phi), b*Math.sin(t))); }
    G.add(new THREE.Mesh(new THREE.TubeGeometry(new THREE.CatmullRomCurve3(pts, true), 360, 0.0065, 6, true), fieldMat(o))); }
}

// the knot: one continuous thread through three lobes. Each arc joins two lobe tips and bows toward the third, passing
// inside the centre (apex at 0.4977 toward the third tip) and over then under (z = 0.62 sin 2πs). This is the
// chart's triquetra exactly when the tips are evenly spaced; with Doug's indigo tips it becomes the ajna arrangement.
const RT = 1.3596, APX = 0.4977, ZA = 0.62;
const v2 = deg => new THREE.Vector2(Math.cos(THREE.MathUtils.degToRad(deg)), Math.sin(THREE.MathUtils.degToRad(deg)));
const circ3 = (a, b, c) => { const d = 2*(a.x*(b.y-c.y) + b.x*(c.y-a.y) + c.x*(a.y-b.y));
  const ux = ((a.lengthSq())*(b.y-c.y) + (b.lengthSq())*(c.y-a.y) + (c.lengthSq())*(a.y-b.y))/d;
  const uy = ((a.lengthSq())*(c.x-b.x) + (b.lengthSq())*(a.x-c.x) + (c.lengthSq())*(b.x-a.x))/d; return new THREE.Vector2(ux, uy); };
const knotPts = [];
const T = F.tips;
for (let k=0;k<3;k++) {
  const A = v2(T[k]).multiplyScalar(RT), B = v2(T[(k+1)%3]).multiplyScalar(RT), M = v2(T[(k+2)%3]).multiplyScalar(APX);
  const O = circ3(A, M, B), r = A.distanceTo(O);
  const ang = p => Math.atan2(p.y - O.y, p.x - O.x);
  let a0 = ang(A), am = ang(M), a1 = ang(B);
  // sweep from A to B through M
  const norm = x => ((x % (2*Math.PI)) + 2*Math.PI) % (2*Math.PI);
  let sweep = norm(a1 - a0); if (norm(am - a0) > sweep) sweep = sweep - 2*Math.PI;
  const N = 220;
  for (let i=0;i<N;i++){ const s = i/N, a = a0 + sweep*s; knotPts.push(new THREE.Vector3(O.x + r*Math.cos(a), O.y + r*Math.sin(a), ZA*Math.sin(2*Math.PI*s))); }
}
const pts = knotPts;
const streamMat = (r, c, o, pulse) => new THREE.ShaderMaterial({
  transparent:true, depthWrite:false, side:THREE.DoubleSide,
  uniforms:{ c:{value:c}, o:{value:o}, r:{value:r}, pulse:{value:pulse}, camD:{value:camera.position.length()} },
  vertexShader:`uniform float r; uniform float camD; varying float vF; varying float vU;
    void main(){ vec3 ctr = position - normal * r; vec4 mvc = modelViewMatrix * vec4(ctr, 1.0);
      float t = clamp((mvc.z + camD) / 0.9, -1.0, 1.0); float f = (t + 1.0) * 0.5;
      vec3 p = ctr + normal * r * (0.72 + 0.5 * smoothstep(0.0, 1.0, f)); vF = f; vU = uv.x;
      gl_Position = projectionMatrix * modelViewMatrix * vec4(p, 1.0); }`,
  fragmentShader:`uniform vec3 c; uniform float o; uniform float pulse; varying float vF; varying float vU;
    void main(){ float s = fract(vU * 21.0); float comet = smoothstep(0.0, 0.08, s) * (1.0 - smoothstep(0.08, 0.85, s));
      float b = mix(1.0, 0.62 + 0.55 * comet, pulse); float a = o * (0.24 + 0.76 * smoothstep(0.0, 1.0, vF)) * b;
      vec3 haze = vec3(0.91, 0.85, 0.74); vec3 col = mix(haze, c, 0.58 + 0.42 * smoothstep(0.0, 1.0, vF));
      gl_FragColor = vec4(col, clamp(a, 0.0, 1.0));
      #include <colorspace_fragment>
    }` });
const layers = [[0.017, hot, 1.0, 1.0], [0.03, hot, 0.45, 0.8], [0.05, col, 0.24, 0.5], [0.075, col, 0.13, 0.3], [0.105, col, 0.07, 0.0], [0.14, glow, 0.035, 0.0]];
// nested knots spiralling out of the core, each smaller one turned further (as in the chart's orange)
const NEST = [[0.30, -0.66, 0.50], [0.47, -0.44, 0.64], [0.68, -0.22, 0.80], [1.0, 0.0, 1.0]];
for (const [sc, turn, str] of NEST) {
  const cs = Math.cos(turn), sn = Math.sin(turn);
  const p2 = pts.map(q => new THREE.Vector3((q.x*cs - q.y*sn)*sc, (q.x*sn + q.y*cs)*sc, q.z*sc));
  const cv2 = new THREE.CatmullRomCurve3(p2, true, 'centripetal'), w = Math.pow(sc, 0.6);
  for (const [r, c, o, pl] of layers) G.add(new THREE.Mesh(new THREE.TubeGeometry(cv2, 900, r*w, 20, true), streamMat(r*w, c, o*str, pl)));
}
// ethereal centre
const cv = document.createElement('canvas'); cv.width = cv.height = 128; const cx = cv.getContext('2d');
const gr = cx.createRadialGradient(64,64,0,64,64,64); gr.addColorStop(0,'rgba(255,255,255,1)'); gr.addColorStop(0.25,'rgba(255,255,255,0.55)'); gr.addColorStop(0.6,'rgba(255,255,255,0.12)'); gr.addColorStop(1,'rgba(255,255,255,0)');
cx.fillStyle = gr; cx.fillRect(0,0,128,128); const tex = new THREE.CanvasTexture(cv);
const spr = (pos, size, c, o) => { const sp = new THREE.Sprite(new THREE.SpriteMaterial({map:tex, color:c, transparent:true, opacity:o, depthWrite:false})); sp.position.copy(pos); sp.scale.setScalar(size); G.add(sp); };
G.add(new THREE.Mesh(new THREE.SphereGeometry(0.24, 64, 48), new THREE.ShaderMaterial({ transparent:true, depthWrite:false, uniforms:{c:{value:col}, h:{value:hot}},
  vertexShader:`varying vec3 vN; varying vec3 vV; void main(){ vec4 mv = modelViewMatrix*vec4(position,1.0); vN = normalize(normalMatrix*normal); vV = normalize(-mv.xyz); gl_Position = projectionMatrix*mv; }`,
  fragmentShader:`uniform vec3 c; uniform vec3 h; varying vec3 vN; varying vec3 vV; void main(){ float f = 1.0 - max(dot(vN,vV),0.0); gl_FragColor = vec4(mix(h, c, f), 0.10 + pow(f,1.4)*0.75); }`})));
spr(new THREE.Vector3(), 1.0, col, 0.35); spr(new THREE.Vector3(), 0.5, hot, 0.55); spr(new THREE.Vector3(), 0.2, hot, 0.9);
G.rotation.set(-0.42, 0.0, 0);   // the chart's orange tilt
renderer.render(scene, camera);
document.body.dataset.done = '1';
</script>
</body></html>

```

## prop.html (alternative: three-bladed propellers caught still, eye-level camera, group turned 0.55 rad about the vertical)

```html
<!doctype html>
<html><head><meta charset="utf-8">
<style>html,body{margin:0;background:transparent}canvas{display:block}</style>
<script type="importmap">{"imports":{"three":"./node_modules/three/build/three.module.js"}}</script>
</head><body>
<script type="module">
import * as THREE from 'three';
const P = new URLSearchParams(location.search);
const form = P.get('form') || 'indigo';
const SIZE = 1000;
const C = {
  orange: {blade:'#F08A3C', edge:'#FFD2A8', deep:'#B4500F', glow:'#FFB070', field:'#FFC48C', dirs:[90, 210, 330], wid:[0.42, 0.42, 0.42]},
  indigo: {blade:'#7A6CF0', edge:'#E4E0FF', deep:'#3B2E9E', glow:'#B0A6FF', field:'#C2BAFF', dirs:[270, 0, 180], wid:[0.5, 0.55, 0.55]}
}[form];

const renderer = new THREE.WebGLRenderer({antialias:true, alpha:true, preserveDrawingBuffer:true});
renderer.setPixelRatio(1); renderer.setSize(SIZE, SIZE); renderer.setClearColor(0x000000, 0);
renderer.outputColorSpace = THREE.SRGBColorSpace;
document.body.appendChild(renderer.domElement);
const scene = new THREE.Scene();
const camera = new THREE.PerspectiveCamera(30, 1, 0.1, 100);
const elev = 0, dist = 6.2;
camera.position.set(0, Math.sin(elev)*dist, Math.cos(elev)*dist); camera.lookAt(0,0,0);
scene.add(new THREE.HemisphereLight(0xffffff, 0x302040, 0.9));
const key = new THREE.DirectionalLight(0xffffff, 2.4); key.position.set(3, 4, 5); scene.add(key);
const rim = new THREE.DirectionalLight(new THREE.Color(C.glow), 1.6); rim.position.set(-4, -1, -3); scene.add(rim);
const core = new THREE.PointLight(new THREE.Color(C.glow), 3.0, 3); scene.add(core);

// the sphere: the toroidal field's outer surface, faint
const halo = new THREE.Mesh(new THREE.SphereGeometry(1.42, 96, 64), new THREE.ShaderMaterial({
  transparent:true, depthWrite:false, uniforms:{c:{value:new THREE.Color(C.field)}},
  vertexShader:`varying vec3 vN; varying vec3 vV; void main(){ vec4 mv = modelViewMatrix*vec4(position,1.0); vN = normalize(normalMatrix*normal); vV = normalize(-mv.xyz); gl_Position = projectionMatrix*mv; }`,
  fragmentShader:`uniform vec3 c; varying vec3 vN; varying vec3 vV; void main(){ float f = 1.0 - max(dot(vN, vV), 0.0); gl_FragColor = vec4(c, pow(f, 2.4)*0.7 + 0.03); }`}));
halo.renderOrder = 10; scene.add(halo);

const G = new THREE.Group(); scene.add(G);   // local frame: spin axis = +z (toward the viewer before the turn)

// faint toroidal flow: helical streamlines wound on nested horn tori around the spin axis
const fieldMat = (o) => new THREE.ShaderMaterial({ transparent:true, depthWrite:false,
  uniforms:{c:{value:new THREE.Color(C.field)}, o:{value:o}, camD:{value:dist}},
  vertexShader:`uniform float camD; varying float vF; void main(){ vec4 mv = modelViewMatrix*vec4(position,1.0); vF = clamp((mv.z + camD)/1.4*0.5+0.5, 0.0, 1.0); gl_Position = projectionMatrix*mv; }`,
  fragmentShader:`uniform vec3 c; uniform float o; varying float vF; void main(){ gl_FragColor = vec4(c, o*(0.25 + 0.75*vF));
#include <colorspace_fragment>
}`});
for (const [R0, b, n, o] of [[0.68, 0.68, 14, 0.17], [0.66, 0.42, 10, 0.1]]) {
  for (let i=0;i<n;i++) {
    const phi0 = i*2*Math.PI/n, pts = [];
    for (let k=0;k<=360;k++){ const t = k/360*2*Math.PI, phi = phi0 + t;   // one swirl per poloidal circuit
      const rr = R0 + b*Math.cos(t); pts.push(new THREE.Vector3(rr*Math.cos(phi), rr*Math.sin(phi), b*Math.sin(t))); }
    G.add(new THREE.Mesh(new THREE.TubeGeometry(new THREE.CatmullRomCurve3(pts, true), 360, 0.006, 6, true), fieldMat(o)));
  }
}

// a blade: a pitched, cambered leaf of light running from the hub to the membrane, twisting less toward the tip
const bladeMat = new THREE.MeshStandardMaterial({ color:new THREE.Color(C.blade), emissive:new THREE.Color(C.deep), emissiveIntensity:0.55,
  roughness:0.32, metalness:0.12, transparent:true, opacity:0.9, side:THREE.DoubleSide });
const edgeMat = (o, r) => new THREE.MeshBasicMaterial({ color:new THREE.Color(C.edge), transparent:true, opacity:o, depthWrite:false });
const blade = (deg, wmax) => {
  const phi = THREE.MathUtils.degToRad(deg), d = new THREE.Vector3(Math.cos(phi), Math.sin(phi), 0), q = new THREE.Vector3(-Math.sin(phi), Math.cos(phi), 0), z = new THREE.Vector3(0,0,1);
  const r0 = 0.2, R = 1.3, NU = 60, NV = 24;
  const at = (u, v) => { const r = r0 + (R - r0)*u, w = wmax*Math.pow(Math.sin(Math.PI*Math.min(u*1.02, 1)), 0.75)*(1 - 0.3*u) + 0.06*(1-u);
    const th = 0.95 - 0.6*u;   // pitch: steep at the root, flatter at the tip
    const c = q.clone().multiplyScalar(Math.cos(th)).add(z.clone().multiplyScalar(Math.sin(th)));
    const n = q.clone().multiplyScalar(-Math.sin(th)).add(z.clone().multiplyScalar(Math.cos(th)));
    return d.clone().multiplyScalar(r).add(c.multiplyScalar(v*w)).add(n.multiplyScalar(0.12*w*(1 - v*v))); };
  const pos = [], idx = [];
  for (let i=0;i<=NU;i++) for (let j=0;j<=NV;j++){ const p = at(i/NU, -1 + 2*j/NV); pos.push(p.x, p.y, p.z); }
  for (let i=0;i<NU;i++) for (let j=0;j<NV;j++){ const a = i*(NV+1)+j, b = a+NV+1; idx.push(a, b, a+1, b, b+1, a+1); }
  const g = new THREE.BufferGeometry(); g.setAttribute('position', new THREE.Float32BufferAttribute(pos, 3)); g.setIndex(idx); g.computeVertexNormals();
  G.add(new THREE.Mesh(g, bladeMat));
  // glowing rim of the blade
  const rimPts = []; for (let i=0;i<=NU;i++) rimPts.push(at(i/NU, 1)); for (let i=NU;i>=0;i--) rimPts.push(at(i/NU, -1));
  const cv = new THREE.CatmullRomCurve3(rimPts, true);
  for (const [r, o] of [[0.007, 1.0], [0.016, 0.35], [0.03, 0.12]]) G.add(new THREE.Mesh(new THREE.TubeGeometry(cv, 400, r, 8, true), edgeMat(o)));
  // midrib
  const rib = []; for (let i=1;i<=NU;i++) rib.push(at(i/NU, 0));
  G.add(new THREE.Mesh(new THREE.TubeGeometry(new THREE.CatmullRomCurve3(rib), 120, 0.006, 6), edgeMat(0.55)));
  if (form === 'indigo') {   // the adept's more faceted form, latent: a quiet lattice on each blade
    for (const u of [0.35, 0.58, 0.8]) { const row = []; for (let j=0;j<=20;j++) row.push(at(u, -1 + j/10)); G.add(new THREE.Mesh(new THREE.TubeGeometry(new THREE.CatmullRomCurve3(row), 60, 0.004, 6), edgeMat(0.4))); }
  }
};
C.dirs.forEach((deg, i) => blade(deg, C.wid[i]));
// hub
G.add(new THREE.Mesh(new THREE.SphereGeometry(0.21, 64, 48), new THREE.MeshStandardMaterial({ color:new THREE.Color(C.edge), emissive:new THREE.Color(C.glow), emissiveIntensity:0.9, roughness:0.2, metalness:0.2 })));
const cvs = document.createElement('canvas'); cvs.width = cvs.height = 128; const cx = cvs.getContext('2d');
const gr = cx.createRadialGradient(64,64,0,64,64,64); gr.addColorStop(0,'rgba(255,255,255,1)'); gr.addColorStop(0.3,'rgba(255,255,255,0.45)'); gr.addColorStop(1,'rgba(255,255,255,0)');
cx.fillStyle = gr; cx.fillRect(0,0,128,128);
const sp = new THREE.Sprite(new THREE.SpriteMaterial({map:new THREE.CanvasTexture(cvs), color:new THREE.Color(C.glow), transparent:true, opacity:0.75, depthWrite:false})); sp.scale.setScalar(1.0); G.add(sp);

G.rotation.set(0, 0.55, 0);   // a three-quarter view about the vertical: the up/down blade stays true to its hour
renderer.render(scene, camera);
document.body.dataset.done = '1';
</script>
</body></html>

```
