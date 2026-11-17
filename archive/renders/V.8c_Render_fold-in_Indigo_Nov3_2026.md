# BWTC render fold-in: indigo — Nov 3 2026

**Target**: `claude/bwtc_3d_centers_render.html`. Carries the authority of that file's indigo section until spliced in (the render file is too large to retype safely in one pass).

**To splice into render.html:**
1. Replace the whole `if (form === 'indigo') { … }` block (the early solid triangle) with the block below.
2. In the tail, add `form === 'indigo'` to the ring-hiding and core-hiding lines (as for green and blue) and to the depth condition.
3. In `SCALE`, set `indigo: 1.0`. `ELEV` stays 55 (looking down into the triangle).

**Render:** single-pass method (like orange and green): `node shoot.js indigo && python3 bloom.py indigo`.

**Status:** Claude's first draft, sent to Doug November 3; blob d717e26054d743625a9ba43ff70dd7cb on the canvas. Doug (Nov 3) asked where the triangle came from: Ra's only indigo shape-word is 51.8, "the basic triangular, or three-petaled, shape"; the frame joining the tips was Claude's. Doug: take the triangle lines out. Removed; the three petals carry the triangular shape. Ra's form (51.8, verified Vol. 1) and the meeting in indigo (57.24, verified Vol. 2) checked in session. Awaiting Doug's direction.

**Log line (for the BWTC fold-in).** Indigo graphic, first draft (Claude, November 3; Doug asked "do EC6"): three broad petals of light reaching the membrane, together making the triangular shape (triangle lines removed at Doug's direction); a quiet lattice in each petal for the adept's "more faceted forms"; nested forms growing from a gateway ring at the core; light drawn in from every side to meet there (57.24). No equator ring.

```js
if (form === 'indigo') { // "a more quiet center which has the basic triangular, or three-petaled, shape in many, although some adepts who have balanced the lower energies may create more faceted forms" (51.8)
  const line = new THREE.Color('#3B2E9E'), hot = new THREE.Color('#6E5EE0'), glw = new THREE.Color('#A99EF0'), white = new THREE.Color('#EEEBFF');
  const streamMat = (r, c, o) => new THREE.ShaderMaterial({
    transparent:true, depthWrite:false, side:THREE.DoubleSide,
    uniforms:{ c:{value:c}, o:{value:o}, r:{value:r}, camD:{value:camera.position.length()} },
    vertexShader:`uniform float r; uniform float camD; varying float vF;
      void main(){ vec3 ctr = position - normal * r; vec4 mvc = modelViewMatrix * vec4(ctr, 1.0);
        float t = clamp((mvc.z + camD) / 1.1, -1.0, 1.0); float f = (t + 1.0) * 0.5; vF = f;
        vec3 p = ctr + normal * r * (0.72 + 0.5 * smoothstep(0.0, 1.0, f));
        gl_Position = projectionMatrix * modelViewMatrix * vec4(p, 1.0); }`,
    fragmentShader:`uniform vec3 c; uniform float o; varying float vF;
      void main(){ float a = o * (0.24 + 0.76 * smoothstep(0.0, 1.0, vF));
        vec3 haze = vec3(0.91, 0.85, 0.74); vec3 col = mix(haze, c, 0.58 + 0.42 * smoothstep(0.0, 1.0, vF));
        gl_FragColor = vec4(col, clamp(a, 0.0, 1.0));
        #include <colorspace_fragment>
      }` });
  const layers = [[0.008, white, 1.0], [0.014, hot, 0.7], [0.022, hot, 0.38], [0.034, line, 0.2], [0.05, glw, 0.08]];
  const tube = (pts, k=1, st=1, closed=true) => { const cv = new THREE.CatmullRomCurve3(pts, closed, 'centripetal');
    for (const [r,c,o] of layers) { const m = new THREE.Mesh(new THREE.TubeGeometry(cv, Math.max(80, pts.length*3), r*k, 12, closed), streamMat(r*k, c, o*st)); m.userData.shaderDepth = true; G.add(m); } };
  const cvs = document.createElement('canvas'); cvs.width = cvs.height = 128; const cx = cvs.getContext('2d');
  const gr = cx.createRadialGradient(64,64,0,64,64,64); gr.addColorStop(0,'rgba(255,255,255,1)'); gr.addColorStop(0.25,'rgba(255,255,255,0.55)'); gr.addColorStop(0.6,'rgba(255,255,255,0.12)'); gr.addColorStop(1,'rgba(255,255,255,0)');
  cx.fillStyle = gr; cx.fillRect(0,0,128,128); const tex = new THREE.CanvasTexture(cvs);
  const spr = (pos, size, c, o) => { const sp = new THREE.Sprite(new THREE.SpriteMaterial({map:tex, color:c, transparent:true, opacity:o, depthWrite:false})); sp.position.copy(pos); sp.scale.setScalar(size); G.add(sp); };
  const up = new THREE.Vector3(0,1,0);
  // a petal: from the gateway outward to a point at the membrane, swelling wide, its tip lifting slightly
  const petalPts = (phi, r0, L, w, lift) => { const d = new THREE.Vector3(Math.cos(phi), 0, Math.sin(phi)), q = new THREE.Vector3(-Math.sin(phi), 0, Math.cos(phi)), pts = [];
    const at = (u, side) => d.clone().multiplyScalar(r0 + L*u).add(q.clone().multiplyScalar(side * w * Math.pow(Math.sin(Math.PI*u), 0.8) * (1 - 0.35*u))).add(up.clone().multiplyScalar(lift * Math.sin(Math.PI*u*0.5) * u));
    for (let i=0;i<=48;i++) pts.push(at(i/48, 1)); for (let i=47;i>=1;i--) pts.push(at(i/48, -1));
    return { pts, at, tip: at(1, 0) }; };
  const RT = 1.36;   // petal tips at the membrane
  // nested forms: the smallest born at the gateway, each larger one turned further, out to the full form at the membrane
  const NEST = [[0.42, -0.5, 0.4], [0.7, -0.25, 0.6], [1.0, 0.0, 1.0]];   // [scale, turn, strength]
  for (const [sc, turn, st] of NEST) {
    const k = Math.pow(sc, 0.6), tips = [];
    for (let i=0;i<3;i++) {
      const phi = -Math.PI/2 + turn + i*2*Math.PI/3, P = petalPts(phi, 0.3*sc, (RT-0.3)*sc, 0.56*sc, 0.1*sc);
      tube(P.pts, k, st); tips.push(P.tip);
      spr(P.tip, 0.34*k, glw, 0.5*st); spr(P.tip, 0.12*k, white, 0.95*st);
      if (sc === 1.0) { // the adept's more faceted form, latent within each petal: a quiet lattice of light
        for (const u of [0.32, 0.55, 0.76]) { const a = P.at(u, 1), b = P.at(u, -1); tube([a, a.clone().lerp(b, 0.5).add(up.clone().multiplyScalar(0.03)), b], 0.35, 0.28, false); }
        for (const s of [-0.5, 0.5]) { const pts = []; for (let j=1;j<=14;j++){ const u = 0.12 + j/14*0.8; pts.push(P.at(u, s)); } tube(pts, 0.3, 0.22, false); }
      }
    }
  }
  // wholeness-making: light drawn in from every side, gathering at the gateway (57.24, "meeting in indigo")
  for (let i=0;i<12;i++) {
    const y = 1 - (i+0.5)/12*2, r = Math.sqrt(1-y*y), th = i*Math.PI*(3-Math.sqrt(5));
    const d = new THREE.Vector3(Math.cos(th)*r, y, Math.sin(th)*r), side = d.clone().cross(up).normalize();
    const pts = []; for (let j=0;j<=30;j++){ const u = j/30, rad = 1.36*(1-u) + 0.26*u; pts.push(d.clone().multiplyScalar(rad).add(side.clone().multiplyScalar(0.1*Math.sin(Math.PI*u)))); }
    tube(pts, 0.28, 0.16, false);
  }
  // the gateway: a quiet ring of light around a deep core
  { const pts = []; for (let j=0;j<64;j++){ const a = j/64*2*Math.PI; pts.push(new THREE.Vector3(0.3*Math.cos(a), 0, 0.3*Math.sin(a))); } tube(pts, 0.9, 1.0); }
  G.add(new THREE.Mesh(new THREE.SphereGeometry(0.22, 64, 48), new THREE.ShaderMaterial({ transparent:true, depthWrite:false, uniforms:{c:{value:line}, h:{value:hot}},
    vertexShader:`varying vec3 vN; varying vec3 vV; void main(){ vec4 mv = modelViewMatrix*vec4(position,1.0); vN = normalize(normalMatrix*normal); vV = normalize(-mv.xyz); gl_Position = projectionMatrix*mv; }`,
    fragmentShader:`uniform vec3 c; uniform vec3 h; varying vec3 vN; varying vec3 vV; void main(){ float f = 1.0 - max(dot(vN,vV),0.0); gl_FragColor = vec4(mix(c, h, f), 0.35 + pow(f,1.3)*0.6);
#include <colorspace_fragment>
}`})));
  spr(new THREE.Vector3(), 1.6, glw, 0.4); spr(new THREE.Vector3(), 0.7, hot, 0.6); spr(new THREE.Vector3(), 0.22, white, 0.9);
  G.rotation.set(0.0, Math.PI/6, 0);
}
```
