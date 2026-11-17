# Energy center render fold-in: green after Zone 4, and the outer flow membrane for all seven — Nov 7 2026

**Targets**: `claude/bwtc_3d_centers_render.html`, the Render Toolkit, and `claude/Energy Centers Working Definitions Nov7 2026.md` Part IV (the renders). This replaces the earlier version of this file from the same morning (the first Zone 4 lotus draft). Doug ruled the green below as **the green energy center in our rendering** (November 7). It is separate from Zone 4 in the poloidal core model, which is unchanged.

## Doug's direction (November 7)
- **Base.** Green after Zone 4: the bubble's flow. Neighboring zones and thresholds removed; drawn thinner and less zoomed in.
- **Outer membrane.** The outer flow is one hue of green and the inner circulation is another, distinct even where both rise. The downward counterflow (the reverse poloidal flow) leads, but it reads as part of one continuous loop.
- **Lines.** Six times as many outer lines (96), thinner and transparent. The inner loops are thicker, so the inner circulation is clear.
- **Center.** A pearly silver sphere with a soft glow that lights the flow lines. No rays.
- **One vector.** The membrane runs south to north as a single movement, received at the root from the center below and passed on at the neck to the center above. Its gradient runs yellow-green at the bottom, true green at the equator and green-blue at the top.
- **Shape.** An onion: a soft rounded root and a gentle neck, with no pinch to a point. No arrows on the outer flow; the colors carry the movement.
- **All seven.** Every center gets the same membrane, colored by what lies below and above it.
- **Red's input.** Intelligent energy enters below red as white, randomized and unfocused, until it is drawn in.
- **Red's spokes (later the same morning).** Multiply the spokes from the center, keeping the outer points joined. Now 72 spokes on a Fibonacci sphere, each tip joined to its nearest neighbors, thinned in proportion so the whole keeps its weight (`red.html`, Three.js 0.160, layered shell/back/front as in the Toolkit).
- **Red's input, revised.** The light below red is white, rising all around from below in soft waves: unfocused but not random in direction, since all of it moves upward toward the Creator (Ra 59.11, "all light, or prana, is upward spiraling"). Then, at Doug's direction, a hundredfold, since intelligent energy is ubiquitous: 6,400 hair-fine strands (one merged line geometry, additive blending) rising in soft waves from the whole lower field and past the frame's edges, brightening as they gather into the white root, with a soft white glow there.
- **Violet's output.** Doug asked what color to use above violet. **Claude proposed white-gold, gathered into one coherent column.** Red receives light white and scattered; violet returns it white again, now whole. A faint gold matches the Zone 8 jet of the poloidal model. Not yet ruled.

## Ra, and the layers
- **Ra.** "The lotus-shape" (51.8). Green is "the springboard to primary blue" (48.7). "The strong red/orange/yellow triad springboards the entity into the center ray of green" (39.10). The universal light entering at the root "is undifferentiated until it begins its filtering process through the energy centers" (54.27). Violet is the sum (34.16, 51.8), "a resource from which, through indigo, intelligent infinity may be contacted" (54.31).
- **Physics.** The bubble's closed recirculation and its two stagnation points (Poloidal Core Dynamics §7).
- **Doug's reading.** The membrane as each center's toroidal field, receiving from below and passing on above.
- **Claude's proposal.** The white-gold column.
- **Not in Ra.** Ra doesn't describe the centers' fields, the onion or the colors of the flow.

## Settings
- **Green** (`green_center_z4.html`; view with `?ty=0.754&dist=3.6`, add `&bg=14121c` for the dark page). The bubble is from the poloidal core model's constants.
  - Membrane: 96 lines along a smooth onion profile (monotone cubic through control points), color by height (stops at s = −1.5, −0.8, 0, 0.8, 1.6 of ONION_H = 1.3 × half-height), fading at the root and neck.
  - Inner loops: 12 closed loops (rc 0.50, rr 0.38, rv 0.70), lotus greens from 0x3fbf84 (upward leg) to 0x12804b (downward leg), silvered near the center, opacity 0.82, tube 0.024.
  - Center: a pearl shader sphere with two glow sprites.
- **The other six** (`membrane.html?form=red|orange|yellow|blue|indigo|violet`). The same onion and colors, rendered on a transparent ground: root = the color below, equator = the center's own, neck = the color above. Red adds 6,400 hair-fine white strands rising in soft waves from the whole field below and gathered into the root. Violet adds a white-gold column with a glow above the neck.
  - Compositing: each center's form (red, yellow, blue and violet from the November 3 canvas blobs; orange and indigo from the November 7 knot renders) is feathered to a circle, scaled to 560 px, centered on 1000 px, then the membrane is laid over it on the dark page ground (20, 18, 28).

**Used in.** *The Seven in Their Flow* (https://claude.ai/artifact/2yMVGXzQyApmYNVXAETNFg), version 4.

**Rebuild.** Three.js r128 (`npm install three@0.128.0`), served locally, shot with Playwright as in the Toolkit.

## green_center_z4.html

```html
<!doctype html>
<html><head><meta charset="utf-8">
<style>html,body{margin:0;background:#fff}canvas{display:block}</style>
<script src="./node_modules/three/build/three.min.js"></script>
</head><body>
<script>
// Zone 4 (the Queen's Chamber bubble) and its neighbours, lifted from poloidal_core_visualization.html (July 16, 2026
// version) with the same geometry constants and flow construction; tubes and arrows drawn thinner (Doug, Nov 7).
const P = new URLSearchParams(location.search);
const K = +(P.get('k') || 0.45);            // thickness factor for tubes and arrows
const DIST = +(P.get('dist') || 4.2);
const scene = new THREE.Scene(); scene.background = new THREE.Color(P.get('bg') ? '#'+P.get('bg') : '#ffffff');
const camera = new THREE.PerspectiveCamera(45, 1, 0.1, 100);
const renderer = new THREE.WebGLRenderer({antialias:true, preserveDrawingBuffer:true});
renderer.setPixelRatio(1); renderer.setSize(1000, 1000); document.body.appendChild(renderer.domElement);
scene.add(new THREE.AmbientLight(0xffffff, 0.7)); const dl = new THREE.DirectionalLight(0xffffff, 0.5); dl.position.set(5,10,7); scene.add(dl);

const columnRadius = 1.0, columnBottom = -3.0;
const separatrixBaseY = columnBottom - 0.5, separatrixThroatR = columnRadius * 0.9;
const zone2Base = columnBottom + 0.25, zone2Top = zone2Base + 1.50;
const thresh2Base = zone2Top + 0.05, thresh2Top = thresh2Base + 1.354;
const bubbleCenterY = 0.754, bubbleHalfHeight = 0.55, bubbleHalfWidth = columnRadius * 0.82;
const lowerStagY = bubbleCenterY - bubbleHalfHeight, upperStagY = bubbleCenterY + bubbleHalfHeight, bubbleRingVerticalFactor = 0.455;
const threshold3Base = upperStagY + 0.05, threshold3Top = threshold3Base + 0.30;

const makeTube = (points, color, emissive, r, opacity) => {
  const geom = new THREE.TubeGeometry(new THREE.CatmullRomCurve3(points), Math.max(16, points.length*2), r*K, 10, false);
  const o = { color, emissive: emissive !== undefined ? emissive : color, emissiveIntensity: 0.35, roughness: 0.6, metalness: 0.1 };
  if (opacity !== undefined) Object.assign(o, { transparent: true, opacity, depthWrite: false });
  return new THREE.Mesh(geom, new THREE.MeshStandardMaterial(o)); };
const addArrow = (g, pos, dir, color, size) => { size *= K;
  const a = new THREE.Mesh(new THREE.ConeGeometry(size*0.45, size*1.3, 10), new THREE.MeshStandardMaterial({ color, emissive: color, emissiveIntensity: 0.5, roughness: 0.5 }));
  a.position.copy(pos); a.quaternion.copy(new THREE.Quaternion().setFromUnitVectors(new THREE.Vector3(0,1,0), dir.clone().normalize())); g.add(a); };
const arrowsAt = (g, pts, ts, color, size) => ts.forEach(tA => { const i = Math.floor(tA*(pts.length-1)); const d = pts[Math.min(i+1, pts.length-1)].clone().sub(pts[i]); if (d.length() > 1e-5) addArrow(g, pts[i], d, color, size); });

// axis


// ZONE 3 / THRESHOLD 2: the foundation semi-spiral, gathering into the cradle under the bubble
if (P.get('neighbours') === '1') { const G = new THREE.Group(); scene.add(G);
  const DY_COLOR = 0xb8a018, DY_EM = 0x6e5808, DY_CORE = 0xd8c048, DY_CORE_EM = 0x8a6810;
  const base = thresh2Base, top = thresh2Top, h = top - base, loose = 0.5, tight = 2.2;
  const rBase = columnRadius * 0.92, rPinch = columnRadius * 0.18, rCradleRim = bubbleHalfWidth * 0.62, yPinch = base + h*0.85, yCradleRim = lowerStagY - 0.01;
  const phiAt = t => t <= 0.65 ? (t/0.65)*loose*Math.PI*2 : t <= 0.85 ? loose*Math.PI*2 + tight*Math.PI*2*Math.pow((t-0.65)/0.2, 1.6) : (loose+tight)*Math.PI*2;
  const rAt = t => { if (t <= 0.65) { const u = t/0.65; return rBase - (rBase - rPinch*2.2)*Math.pow(u, 1.4); } if (t <= 0.85) { const u = (t-0.65)/0.2, rE = rPinch*2.2; return rE + (rPinch - rE)*Math.pow(u, 1.3); } const u = (t-0.85)/0.15; return rPinch + (rCradleRim - rPinch)*0.5*(1 - Math.cos(u*Math.PI)); };
  const yAt = t => t <= 0.85 ? base + (yPinch - base)*(t/0.85) : yPinch + (yCradleRim - yPinch)*Math.pow((t-0.85)/0.15, 0.7);
  for (let i=0;i<5;i++){ const phi0 = i/5*Math.PI*2, pts = []; for (let k=0;k<120;k++){ const t = k/119; pts.push(new THREE.Vector3(rAt(t)*Math.cos(phi0+phiAt(t)), yAt(t), rAt(t)*Math.sin(phi0+phiAt(t)))); }
    G.add(makeTube(pts, DY_COLOR, DY_EM, 0.040)); arrowsAt(G, pts, [0.10, 0.30, 0.50, 0.70, 0.82, 0.93], DY_COLOR, 0.13); }
  { const pts = []; for (let k=0;k<40;k++) pts.push(new THREE.Vector3(0, yAt(0.35 + 0.57*k/39), 0)); G.add(makeTube(pts, DY_CORE, DY_CORE_EM, 0.018)); }
  const ring = new THREE.Mesh(new THREE.TorusGeometry(rCradleRim, 0.018*K, 8, 64), new THREE.MeshStandardMaterial({ color: DY_CORE, emissive: DY_CORE_EM, emissiveIntensity: 0.35, metalness: 0.2, roughness: 0.55 }));
  ring.rotation.x = Math.PI/2; ring.position.set(0, yCradleRim, 0); G.add(ring); }

// LOWER SHEATH
if (P.get('neighbours') === '1') { const G = new THREE.Group(); scene.add(G); const C = 0xa8822c, E = 0x5a4018; const yb = separatrixBaseY, yt = lowerStagY, hh = yt - yb, R = separatrixThroatR;
  for (let j=0;j<=4;j++){ const y = yb + hh*j/4, rp = []; for (let k=0;k<=48;k++){ const ph = k/48*Math.PI*2; rp.push(new THREE.Vector3(R*Math.cos(ph), y, R*Math.sin(ph))); } G.add(new THREE.Line(new THREE.BufferGeometry().setFromPoints(rp), new THREE.LineBasicMaterial({ color: C, transparent: true, opacity: 0.35 }))); }
  for (let i=0;i<6;i++){ const off = i/6*Math.PI*2, pts = []; for (let k=0;k<50;k++){ const t = k/49; pts.push(new THREE.Vector3(R*Math.cos(off + 0.5*Math.PI*2*t), yb + t*hh, R*Math.sin(off + 0.5*Math.PI*2*t))); }
    G.add(makeTube(pts, C, E, 0.014, 0.55)); arrowsAt(G, pts, [0.25, 0.55, 0.85], C, 0.09); } }

// ZONE 4: the bubble
{ const G = new THREE.Group(); scene.add(G);
  const GOLD = 0x785c18, GOLD_EM = 0x3d2a08, GREEN = 0x3a8a4a, GREEN_EM = 0x1e4a24, GREEN_ARROW = 0x4caa5e;
  // outer flow membrane: one vector, south to north, shaped like an onion: a full bulb tapering smoothly into a soft
  // root below (receiving from the yellow center) and a soft neck above (passing on toward the blue center). No arrows:
  // the colour carries the movement, yellow-green at the root, true green at the equator, green-blue at the neck, blue above.
  const STOPS = [[-1.5, 0xe2d830], [-0.8, 0xa8d838], [0.0, 0x2fb45e], [0.8, 0x1fa8b0], [1.6, 0x3a7fe8]];   // by (y - centre)/H
  const ONION_H = bubbleHalfHeight*1.3, RN = 0.075, RMAX = bubbleHalfWidth + 0.05, STEM = 0.12;
  const colAt = (y) => { const u = (y - bubbleCenterY)/ONION_H; const c = new THREE.Color();
    if (u <= STOPS[0][0]) return c.setHex(STOPS[0][1]); if (u >= STOPS[STOPS.length-1][0]) return c.setHex(STOPS[STOPS.length-1][1]);
    for (let i=0;i<STOPS.length-1;i++){ const [u0,h0] = STOPS[i], [u1,h1] = STOPS[i+1]; if (u <= u1) return c.setHex(h0).lerp(new THREE.Color(h1), (u-u0)/(u1-u0)); } return c; };
  // the onion's outline, drawn through control points (s = (y - centre)/H, r as a fraction of RMAX) and joined smoothly:
  // a rounder base easing into the root, a gentler taper easing into the neck, no corners
  const PROF = [[-1.60, 0.10], [-1.34, 0.105], [-1.17, 0.16], [-1.03, 0.36], [-0.86, 0.62], [-0.62, 0.84], [-0.32, 0.97], [0.0, 1.0],
                [0.30, 0.965], [0.56, 0.84], [0.78, 0.63], [0.97, 0.38], [1.12, 0.20], [1.27, 0.12], [1.45, 0.10], [1.62, 0.10]];
  const profS = PROF.map(p => p[0]), profR = PROF.map(p => p[1]);
  // monotone cubic (Fritsch-Carlson) so the curve passes through every point without overshoot
  const pchip = (() => { const n = profS.length, h = [], d = [], m = new Array(n);
    for (let i=0;i<n-1;i++){ h.push(profS[i+1]-profS[i]); d.push((profR[i+1]-profR[i])/h[i]); }
    m[0] = d[0]; m[n-1] = d[n-2];
    for (let i=1;i<n-1;i++){ if (d[i-1]*d[i] <= 0) m[i] = 0; else { const w1 = 2*h[i]+h[i-1], w2 = h[i]+2*h[i-1]; m[i] = (w1+w2)/(w1/d[i-1] + w2/d[i]); } }
    return (x) => { if (x <= profS[0]) return profR[0]; if (x >= profS[n-1]) return profR[n-1];
      let i = 0; while (x > profS[i+1]) i++; const t = (x - profS[i])/h[i], t2 = t*t, t3 = t2*t;
      return (2*t3-3*t2+1)*profR[i] + (t3-2*t2+t)*h[i]*m[i] + (-2*t3+3*t2)*profR[i+1] + (t3-t2)*h[i]*m[i+1]; }; })();
  const onionR = (y) => RMAX*pchip((y - bubbleCenterY)/ONION_H);
  window.onionR = onionR; window.ONION_H = ONION_H;
  const yBot = bubbleCenterY - 1.60*ONION_H, yTop = bubbleCenterY + 1.62*ONION_H;
  // per-vertex colour and fading alpha (the lines fade out at the root and the neck)
  const fadeMat = (opacity) => new THREE.ShaderMaterial({ transparent: true, depthWrite: false, uniforms: { op: { value: opacity } },
    vertexShader: `attribute vec3 color; attribute float alpha; varying vec3 vC; varying float vA; void main(){ vC = color; vA = alpha; gl_Position = projectionMatrix*modelViewMatrix*vec4(position,1.0); }`,
    fragmentShader: `uniform float op; varying vec3 vC; varying float vA; void main(){ gl_FragColor = vec4(vC, op*vA); }` });
  const memMat = fadeMat(0.46);
  for (let i=0;i<96;i++){ const phi = i/96*Math.PI*2, pts = [];
    for (let k=0;k<=90;k++){ const t = k/90, y = yBot + (yTop - yBot)*t, r = onionR(y), tw = phi + 0.5*THREE.MathUtils.smoothstep(t, 0.12, 0.88);
      pts.push(new THREE.Vector3(r*Math.cos(tw), y, r*Math.sin(tw))); }
    const geom = new THREE.TubeGeometry(new THREE.CatmullRomCurve3(pts), 220, 0.0085*K, 8, false);
    const pos = geom.attributes.position, cols = [], al = [];
    for (let j=0;j<pos.count;j++){ const y = pos.getY(j), c = colAt(y); cols.push(c.r, c.g, c.b);
      al.push(Math.min(THREE.MathUtils.smoothstep(y, yBot, bubbleCenterY - 1.12*ONION_H), 1 - THREE.MathUtils.smoothstep(y, bubbleCenterY + 1.12*ONION_H, yTop))); }
    geom.setAttribute('color', new THREE.Float32BufferAttribute(cols, 3)); geom.setAttribute('alpha', new THREE.Float32BufferAttribute(al, 1));
    G.add(new THREE.Mesh(geom, memMat)); }
  // the inner circulation: its own closed loop in the lotus greens, one continuous line per loop. The downward leg
  // down the centreline (the reverse poloidal flow) leads through a deeper lotus colour and stronger arrows; the
  // upward leg near the wall shades into a lighter lotus green. Translucent, so the silver centre shows through.
  const CTR = new THREE.Vector3(0, bubbleCenterY, 0);
  const DEEP = new THREE.Color(0x12804b), LIGHT = new THREE.Color(0x3fbf84), SILVERED = new THREE.Color(0xeef5f2);
  const rc = bubbleHalfWidth*0.50, rr = bubbleHalfWidth*0.38, rv = bubbleHalfHeight*0.70;
  const loopPt = (phi, la) => new THREE.Vector3((rc + rr*Math.cos(la))*Math.cos(phi), bubbleCenterY - rv*Math.sin(la), (rc + rr*Math.cos(la))*Math.sin(phi));
  const loopMat = new THREE.MeshBasicMaterial({ vertexColors: true, transparent: true, opacity: 0.82, depthWrite: false });
  for (let i=0;i<12;i++){ const phi = i/12*Math.PI*2, pts = [];
    for (let k=0;k<96;k++) pts.push(loopPt(phi, Math.PI/2 - (k/96)*Math.PI*2));   // up the outside, in at the top, down the centre, out at the bottom
    const geom = new THREE.TubeGeometry(new THREE.CatmullRomCurve3(pts, true), 220, 0.024*K, 12, true);
    const pos = geom.attributes.position, cols = [], c = new THREE.Color(), v = new THREE.Vector3();
    for (let j=0;j<pos.count;j++){ v.fromBufferAttribute(pos, j);
      const rad = Math.hypot(v.x, v.z), inner = THREE.MathUtils.clamp((rc + rr*0.6 - rad)/(rr*1.2), 0, 1);   // 1 on the downward leg, 0 on the upward leg
      c.copy(LIGHT).lerp(DEEP, inner);
      const near = Math.pow(Math.max(0, 1 - v.distanceTo(CTR)/0.62), 1.6); c.lerp(SILVERED, near*0.85);              // touched by the silver light near the centre
      cols.push(c.r, c.g, c.b); }
    geom.setAttribute('color', new THREE.Float32BufferAttribute(cols, 3));
    G.add(new THREE.Mesh(geom, loopMat));
    const arrow = (t, size, col) => { const ix = Math.floor(t*pts.length) % pts.length, d = pts[(ix+1) % pts.length].clone().sub(pts[ix]);
      const ar = new THREE.Mesh(new THREE.ConeGeometry(size*K*0.45, size*K*1.3, 12), new THREE.MeshBasicMaterial({ color: col, transparent: true, opacity: 0.85 }));
      ar.position.copy(pts[ix]); ar.quaternion.copy(new THREE.Quaternion().setFromUnitVectors(new THREE.Vector3(0,1,0), d.normalize())); G.add(ar); };
    arrow(0.25, 0.07, 0x6fd3a2);                       // upward leg: one small arrow
    arrow(i % 2 === 0 ? 0.63 : 0.87, 0.095, 0x2fa56d);   // downward leg: one firmer arrow, alternating above and below the centre
  }
  // the centre: a pearly silver sphere, softly glowing; its light falls on the flow lines around it
  { const pearl = new THREE.ShaderMaterial({ uniforms: {}, depthTest: false, transparent: true,
      vertexShader: `varying vec3 vN; varying vec3 vV; void main(){ vec4 mv = modelViewMatrix*vec4(position,1.0); vN = normalize(normalMatrix*normal); vV = normalize(-mv.xyz); gl_Position = projectionMatrix*mv; }`,
      fragmentShader: `varying vec3 vN; varying vec3 vV; void main(){
        float ndv = max(dot(vN, vV), 0.0), rim = pow(1.0 - ndv, 2.2);
        vec3 base = vec3(0.93, 0.94, 0.96);                                   // silver-white body
        vec3 sheen = 0.5 + 0.5*cos(6.2832*(vec3(0.0, 0.33, 0.67) + rim*0.9 + vN.y*0.25));   // nacre: a soft play of rose, green and blue at the edge
        vec3 shade = mix(vec3(0.93,0.945,0.96), vec3(0.62,0.66,0.71), pow(1.0-ndv,1.1));   // silver body, darker toward the limb
        vec3 col = mix(shade, mix(shade, sheen*0.95, 0.38), smoothstep(0.2, 0.9, rim));          // faint nacre only at the edge
        col += vec3(1.0)*pow(max(dot(vN, normalize(vec3(-0.4, 0.6, 0.7))), 0.0), 24.0)*0.35;  // soft highlight
        col = mix(col, vec3(0.97, 0.98, 1.0), 0.06);
        gl_FragColor = vec4(col, 1.0); }` });
    const orb = new THREE.Mesh(new THREE.SphereGeometry(0.09, 64, 48), pearl); orb.position.copy(CTR); orb.renderOrder = 60; G.add(orb);
    const glowTex = (stops) => { const cv = document.createElement('canvas'); cv.width = cv.height = 256; const cx = cv.getContext('2d');
      const gr = cx.createRadialGradient(128,128,0,128,128,128); stops.forEach(([o,c]) => gr.addColorStop(o, c)); cx.fillStyle = gr; cx.fillRect(0,0,256,256); return new THREE.CanvasTexture(cv); };
    // inner glow hugging the pearl, then a wide soft light filling the bubble's heart
    const s1 = new THREE.Sprite(new THREE.SpriteMaterial({ map: glowTex([[0,'rgba(255,255,255,0.85)'],[0.3,'rgba(244,247,251,0.55)'],[1,'rgba(240,244,250,0)']]), transparent: true, depthWrite: false })); s1.position.copy(CTR); s1.scale.setScalar(0.62); s1.renderOrder = 59; s1.material.depthTest = false; G.add(s1);
    const s2 = new THREE.Sprite(new THREE.SpriteMaterial({ map: glowTex([[0,'rgba(250,252,255,0.6)'],[0.4,'rgba(238,244,248,0.28)'],[1,'rgba(238,244,248,0)']]), transparent: true, depthWrite: false })); s2.position.copy(CTR); s2.scale.setScalar(1.35); s2.renderOrder = 58; s2.material.depthTest = false; G.add(s2);
  }
  // stagnation points and the still centre
  const sg = new THREE.SphereGeometry(0.06*0.7, 24, 16), sm = new THREE.MeshStandardMaterial({ color: 0xf0fff6, emissive: 0xc8f5dc, emissiveIntensity: 0.8, roughness: 0.3 });
  for (const y of [lowerStagY, upperStagY]) { const m = new THREE.Mesh(sg, sm); m.position.set(0, y, 0); G.add(m);
    const ring = new THREE.Mesh(new THREE.RingGeometry(0.06, 0.12, 40), new THREE.MeshBasicMaterial({ color: 0xd8f5e4, transparent: true, opacity: 0.55, side: THREE.DoubleSide })); ring.rotation.x = Math.PI/2; ring.position.set(0, y, 0); G.add(ring); }
  
  
  // bubble envelope
  { const nR = 24, nP = 48, v = [], idx = [];
    for (let j=0;j<=nR;j++){ const yl = -1 + 2*j/nR, y = bubbleCenterY + (yl < 0 ? yl*1.12 : yl*1.10)*window.ONION_H, r = Math.max(0, window.onionR(y) - 0.04); for (let i=0;i<=nP;i++){ const ph = i/nP*Math.PI*2; v.push(r*Math.cos(ph), y, r*Math.sin(ph)); } }
    for (let j=0;j<nR;j++) for (let i=0;i<nP;i++){ const a = j*(nP+1)+i, b = a+1, c = a+nP+1, d = c+1; idx.push(a,b,d, a,d,c); }
    const g = new THREE.BufferGeometry(); g.setAttribute('position', new THREE.Float32BufferAttribute(v, 3)); g.setIndex(idx); g.computeVertexNormals();
    scene.add(new THREE.Mesh(g, new THREE.MeshBasicMaterial({ color: 0x8fd6ae, transparent: true, opacity: 0.22, side: THREE.DoubleSide, depthWrite: false }))); } }

// THRESHOLD 3: the wake above the bubble (seeded so the wobble is the same each render)
if (P.get('neighbours') === '1') { const G = new THREE.Group(); scene.add(G);
  const sleeve = new THREE.Mesh(new THREE.CylinderGeometry(columnRadius*0.14, columnRadius*0.20, threshold3Top - threshold3Base, 24, 1, true), new THREE.MeshStandardMaterial({ color: 0x3d2a08, transparent: true, opacity: 0.16, side: THREE.DoubleSide, depthWrite: false }));
  sleeve.position.set(0, (threshold3Base + threshold3Top)/2, 0); G.add(sleeve);
  for (let i=0;i<12;i++){ const phi0 = i/12*Math.PI*2, baseR = columnRadius*(0.35 + 0.45*(i%2 === 0 ? 1 : 0.7)), pts = [];
    for (let k=0;k<40;k++){ const t = k/39, y = threshold3Base + (threshold3Top - threshold3Base)*t, wob = Math.sin(t*Math.PI*2.5 + phi0*0.5)*(0.04 + 0.08*t), kick = t > 0.75 ? (t - 0.75)*0.15 : 0, phi = phi0 + wob, r = baseR + kick*Math.cos(phi0*2), rw = 0.02*Math.sin(t*Math.PI*3 + phi0);
      pts.push(new THREE.Vector3(Math.max(0.1, r + rw)*Math.cos(phi), y, Math.max(0.1, r + rw)*Math.sin(phi))); }
    let color = 0x785c18, em = 0x3d2a08; if (i%4 === 0) { color = 0x8a552e; em = 0x4a2d14; } else if (i%4 === 2) { color = 0x6a4a68; em = 0x3a2638; }
    G.add(makeTube(pts, color, em, 0.015)); arrowsAt(G, pts, [0.3, 0.6, 0.9], color, 0.10); } }

// camera: the model's default angle (azimuth 45 degrees, tilt 9 degrees), aimed at the bubble, pulled back
const az = Math.PI/4, el = THREE.MathUtils.degToRad(+(P.get('el') || 9)), ty = +(P.get('ty') || 0.62);
camera.position.set(DIST*Math.cos(el)*Math.sin(az), ty + DIST*Math.sin(el), DIST*Math.cos(el)*Math.cos(az)); camera.lookAt(0, ty, 0);
renderer.render(scene, camera); document.body.dataset.done = '1';
</script>
</body></html>

```

## membrane.html

```html
<!doctype html>
<html><head><meta charset="utf-8">
<style>html,body{margin:0;background:transparent}canvas{display:block}</style>
<script src="./node_modules/three/build/three.min.js"></script>
</head><body>
<script>
// The outer flow membrane for each energy center, on the pattern of the green center (Doug, Nov 7 2026): an onion of
// fine translucent lines rising south to north, received at the root from the center below and passed on at the neck
// to the center above. Colour by height: the root takes the colour below, the equator the center's own, the neck the
// colour above. Red receives intelligent energy as scattered white strands drawn in; violet passes on white-gold
// (Claude's proposal). Rendered on a transparent ground for compositing over each center's form.
const P = new URLSearchParams(location.search);
const form = P.get('form') || 'red';
const K = 0.45, DIST = 3.6, CY = 0.754, HH = 0.55, HW = 0.82;
const HEX = { white: 0xf4f2ec, red: 0xd2382c, orange: 0xe8802a, yellow: 0xe2c830, green: 0x2fb45e, blue: 0x2f78d8, indigo: 0x5a48c8, violet: 0x9050c0, wgold: 0xfff0c2 };
const ORDER = ['white','red','orange','yellow','green','blue','indigo','violet','wgold'];
const i0 = ORDER.indexOf(form), below = ORDER[i0-1], above = ORDER[i0+1];
const mix = (a, b, t) => new THREE.Color(HEX[a]).lerp(new THREE.Color(HEX[b]), t).getHex();
const STOPS = [[-1.5, HEX[below]], [-0.8, mix(below, form, 0.6)], [0.0, HEX[form]], [0.8, mix(form, above, 0.45)], [1.6, HEX[above]]];

const scene = new THREE.Scene();
const camera = new THREE.PerspectiveCamera(45, 1, 0.1, 100);
const renderer = new THREE.WebGLRenderer({antialias:true, alpha:true, preserveDrawingBuffer:true});
renderer.setPixelRatio(1); renderer.setSize(1000, 1000); renderer.setClearColor(0x000000, 0); document.body.appendChild(renderer.domElement);
const G = new THREE.Group(); scene.add(G);

const ONION_H = HH*1.3, RMAX = HW + 0.05;
const colAt = (y) => { const u = (y - CY)/ONION_H, c = new THREE.Color();
  if (u <= STOPS[0][0]) return c.setHex(STOPS[0][1]); if (u >= STOPS[STOPS.length-1][0]) return c.setHex(STOPS[STOPS.length-1][1]);
  for (let i=0;i<STOPS.length-1;i++){ const [u0,h0] = STOPS[i], [u1,h1] = STOPS[i+1]; if (u <= u1) return c.setHex(h0).lerp(new THREE.Color(h1), (u-u0)/(u1-u0)); } return c; };
const PROF = [[-1.60, 0.10], [-1.34, 0.105], [-1.17, 0.16], [-1.03, 0.36], [-0.86, 0.62], [-0.62, 0.84], [-0.32, 0.97], [0.0, 1.0],
              [0.30, 0.965], [0.56, 0.84], [0.78, 0.63], [0.97, 0.38], [1.12, 0.20], [1.27, 0.12], [1.45, 0.10], [1.62, 0.10]];
const pchip = (() => { const xs = PROF.map(p => p[0]), ys = PROF.map(p => p[1]), n = xs.length, h = [], d = [], m = new Array(n);
  for (let i=0;i<n-1;i++){ h.push(xs[i+1]-xs[i]); d.push((ys[i+1]-ys[i])/h[i]); } m[0] = d[0]; m[n-1] = d[n-2];
  for (let i=1;i<n-1;i++){ if (d[i-1]*d[i] <= 0) m[i] = 0; else { const w1 = 2*h[i]+h[i-1], w2 = h[i]+2*h[i-1]; m[i] = (w1+w2)/(w1/d[i-1] + w2/d[i]); } }
  return (x) => { if (x <= xs[0]) return ys[0]; if (x >= xs[n-1]) return ys[n-1]; let i = 0; while (x > xs[i+1]) i++;
    const t = (x - xs[i])/h[i], t2 = t*t, t3 = t2*t; return (2*t3-3*t2+1)*ys[i] + (t3-2*t2+t)*h[i]*m[i] + (-2*t3+3*t2)*ys[i+1] + (t3-t2)*h[i]*m[i+1]; }; })();
const onionR = (y) => RMAX*pchip((y - CY)/ONION_H);
const yBot = CY - 1.60*ONION_H, yTop = CY + 1.62*ONION_H, yRoot = CY - 1.12*ONION_H, yNeck = CY + 1.12*ONION_H;

const fadeMat = (op) => new THREE.ShaderMaterial({ transparent: true, depthWrite: false, uniforms: { op: { value: op } },
  vertexShader: `attribute vec3 color; attribute float alpha; varying vec3 vC; varying float vA; void main(){ vC = color; vA = alpha; gl_Position = projectionMatrix*modelViewMatrix*vec4(position,1.0); }`,
  fragmentShader: `uniform float op; varying vec3 vC; varying float vA; void main(){ gl_FragColor = vec4(vC, op*vA); }` });
const colouredTube = (pts, r, mat, alphaFn, colFn) => { const geom = new THREE.TubeGeometry(new THREE.CatmullRomCurve3(pts), Math.max(80, pts.length*2), r*K, 8, false);
  const pos = geom.attributes.position, cols = [], al = [], v = new THREE.Vector3();
  for (let j=0;j<pos.count;j++){ v.fromBufferAttribute(pos, j); const c = colFn(v); cols.push(c.r, c.g, c.b); al.push(alphaFn(v)); }
  geom.setAttribute('color', new THREE.Float32BufferAttribute(cols, 3)); geom.setAttribute('alpha', new THREE.Float32BufferAttribute(al, 1));
  G.add(new THREE.Mesh(geom, mat)); };

// the soft ground inside the bulb, tinted the center's own colour
{ const nR = 30, nP = 64, v = [], idx = [];
  for (let j=0;j<=nR;j++){ const yl = -1 + 2*j/nR, y = CY + (yl < 0 ? yl*1.12 : yl*1.10)*ONION_H, r = Math.max(0, onionR(y) - 0.04); for (let i=0;i<=nP;i++){ const ph = i/nP*Math.PI*2; v.push(r*Math.cos(ph), y, r*Math.sin(ph)); } }
  for (let j=0;j<nR;j++) for (let i=0;i<nP;i++){ const a = j*(nP+1)+i, b = a+1, c = a+nP+1, d = c+1; idx.push(a,b,d, a,d,c); }
  const g = new THREE.BufferGeometry(); g.setAttribute('position', new THREE.Float32BufferAttribute(v, 3)); g.setIndex(idx);
  G.add(new THREE.Mesh(g, new THREE.MeshBasicMaterial({ color: new THREE.Color(HEX[form]).lerp(new THREE.Color(0xffffff), 0.55), transparent: true, opacity: 0.10, side: THREE.DoubleSide, depthWrite: false }))); }

// the membrane: 96 fine lines, south to north
const memMat = fadeMat(0.46);
const endFade = (v) => Math.min(THREE.MathUtils.smoothstep(v.y, yBot, yRoot), 1 - THREE.MathUtils.smoothstep(v.y, yNeck, yTop));
for (let i=0;i<96;i++){ const phi = i/96*Math.PI*2, pts = [];
  for (let k=0;k<=90;k++){ const t = k/90, y = yBot + (yTop - yBot)*t, r = onionR(y), tw = phi + 0.5*THREE.MathUtils.smoothstep(t, 0.12, 0.88); pts.push(new THREE.Vector3(r*Math.cos(tw), y, r*Math.sin(tw))); }
  colouredTube(pts, 0.0085, memMat, endFade, v => colAt(v.y)); }

// seeded random, so each render is the same
let seed = 7; const rnd = () => { seed = (seed*16807) % 2147483647; return seed/2147483647; };

if (form === 'red') {
  // intelligent energy, ubiquitous: white light rising from everywhere below in soft waves, a hundredfold (6,400 strands).
  // Unfocused (each strand undulates on its own, arising anywhere) yet not directionless: every one moves upward and is
  // gathered into the root. Ra: "all light, or prana, is upward spiraling" (59.11); it enters "undifferentiated" (54.27).
  // Drawn as hair-fine lines, faint alone, bright where they gather; merged into one geometry.
  const root = new THREE.Vector3(0, yBot + 0.16, 0), RS = onionR(root.y)*0.95, NSTR = +(P.get('nstr') || 6400), NPT = 48;
  const wht = new THREE.Color(0xfbfaf6), warm = new THREE.Color(0xf6e6de);
  const yLow = CY - 1.6, pos = [], cols = [], al = [];
  for (let i=0;i<NSTR;i++){
    const a0 = rnd()*Math.PI*2, r0 = 0.25 + 2.6*Math.sqrt(rnd()), yStart = yLow + (yBot - 0.02 - yLow)*Math.pow(rnd(), 1.1);
    const amp = 0.03 + 0.05*rnd(), waves = 1.2 + 1.6*rnd(), ph = rnd()*Math.PI*2, swirl = 0.3 + 0.4*rnd();
    let prev = null;
    for (let k=0;k<NPT;k++){ const t = k/(NPT-1), y = yStart + (root.y - yStart)*t, g = THREE.MathUtils.smoothstep(t, 0, 1), rr = r0 + (RS - r0)*g, ang = a0 + swirl*t;
      const wob = amp*(1 - g)*Math.sin(ph + t*waves*Math.PI*2);
      const p = new THREE.Vector3(rr*Math.cos(ang) - wob*Math.sin(ang), y + 0.025*Math.sin(ph*1.7 + t*waves*Math.PI), rr*Math.sin(ang) + wob*Math.cos(ang));
      const c = wht.clone().lerp(warm, THREE.MathUtils.smoothstep(t, 0.9, 1.0)), aa = 0.55 + 0.45*Math.pow(t, 2.5);
      if (prev) { pos.push(prev.p.x, prev.p.y, prev.p.z, p.x, p.y, p.z); cols.push(prev.c.r, prev.c.g, prev.c.b, c.r, c.g, c.b); al.push(prev.a, aa); }
      prev = { p, c, a: aa }; } }
  const g = new THREE.BufferGeometry(); g.setAttribute('position', new THREE.Float32BufferAttribute(pos, 3)); g.setAttribute('color', new THREE.Float32BufferAttribute(cols, 3)); g.setAttribute('alpha', new THREE.Float32BufferAttribute(al, 1));
  const m = fadeMat(+(P.get('sop') || 0.16)); m.blending = THREE.AdditiveBlending; G.add(new THREE.LineSegments(g, m));
  // a soft white glow where the light is gathered into the root
  const cv = document.createElement('canvas'); cv.width = cv.height = 128; const cx = cv.getContext('2d');
  const gr = cx.createRadialGradient(64,64,0,64,64,64); gr.addColorStop(0,'rgba(255,255,255,0.8)'); gr.addColorStop(0.35,'rgba(255,250,246,0.3)'); gr.addColorStop(1,'rgba(255,250,246,0)');
  cx.fillStyle = gr; cx.fillRect(0,0,128,128);
  const sp = new THREE.Sprite(new THREE.SpriteMaterial({ map: new THREE.CanvasTexture(cv), transparent: true, depthWrite: false })); sp.position.set(0, root.y - 0.02, 0); sp.scale.set(0.5, 0.4, 1); G.add(sp);
}
if (form === 'violet') {
  // above the neck: white-gold, gathered into one coherent column rising on (Claude's proposal)
  const colMat = fadeMat(0.42);
  for (let i=0;i<24;i++){ const phi = i/24*Math.PI*2, r = 0.05, pts = [];
    for (let k=0;k<=30;k++){ const y = yNeck + (yTop + 0.45 - yNeck)*k/30; pts.push(new THREE.Vector3(r*Math.cos(phi), y, r*Math.sin(phi))); }
    colouredTube(pts, 0.008, colMat, v => 1 - THREE.MathUtils.smoothstep(v.y, yTop + 0.05, yTop + 0.45), () => new THREE.Color(HEX.wgold)); }
  const cv = document.createElement('canvas'); cv.width = cv.height = 128; const cx = cv.getContext('2d');
  const gr = cx.createRadialGradient(64,64,0,64,64,64); gr.addColorStop(0,'rgba(255,246,214,0.85)'); gr.addColorStop(0.4,'rgba(255,240,200,0.3)'); gr.addColorStop(1,'rgba(255,240,200,0)');
  cx.fillStyle = gr; cx.fillRect(0,0,128,128);
  const sp = new THREE.Sprite(new THREE.SpriteMaterial({ map: new THREE.CanvasTexture(cv), transparent: true, depthWrite: false })); sp.position.set(0, yTop + 0.1, 0); sp.scale.set(0.35, 0.7, 1); G.add(sp);
}

const az = Math.PI/4, el = THREE.MathUtils.degToRad(9), ty = CY;
camera.position.set(DIST*Math.cos(el)*Math.sin(az), ty + DIST*Math.sin(el), DIST*Math.cos(el)*Math.cos(az)); camera.lookAt(0, ty, 0);
renderer.render(scene, camera); document.body.dataset.done = '1';
</script>
</body></html>

```

## red.html (72 spokes)

```html
<!doctype html>
<html><head><meta charset="utf-8">
<style>html,body{margin:0;background:transparent}canvas{display:block}</style>
<script type="importmap">{"imports":{"three":"./node_modules/three/build/three.module.js"}}</script>
</head><body>
<script type="module">
// The red energy center from claude/bwtc_3d_centers_render.html (Nov 3), with the spokes multiplied (Doug, Nov 7):
// 72 spokes spread evenly in all directions (Fibonacci sphere), each tip joined to its nearest neighbours, and again small at the core.
import * as THREE from 'three';
const P = new URLSearchParams(location.search);
const NS = +(P.get('n') || 72);
const col = new THREE.Color('#C8352B'), glow = new THREE.Color('#E2574C');
const renderer = new THREE.WebGLRenderer({antialias:true, alpha:true, preserveDrawingBuffer:true});
renderer.setPixelRatio(1); renderer.setSize(1000, 1000); renderer.setClearColor(0x000000, 0);
renderer.outputColorSpace = THREE.SRGBColorSpace; document.body.appendChild(renderer.domElement);
const scene = new THREE.Scene();
const camera = new THREE.PerspectiveCamera(30, 1, 0.1, 100);
const elev = THREE.MathUtils.degToRad(28), dist = 6.2;
camera.position.set(0, Math.sin(elev)*dist, Math.cos(elev)*dist); camera.lookAt(0,0,0);
const halo = new THREE.Mesh(new THREE.SphereGeometry(1.42, 96, 64), new THREE.ShaderMaterial({ transparent:true, depthWrite:false, uniforms:{c:{value:glow}},
  vertexShader:`varying vec3 vN; varying vec3 vV; void main(){ vec4 mv = modelViewMatrix*vec4(position,1.0); vN = normalize(normalMatrix*normal); vV = normalize(-mv.xyz); gl_Position = projectionMatrix*mv; }`,
  fragmentShader:`uniform vec3 c; varying vec3 vN; varying vec3 vV; void main(){ float f = 1.0 - max(dot(vN, vV), 0.0); float a = pow(f, 2.2)*0.85 + 0.06; gl_FragColor = vec4(c, a); }` }));
halo.renderOrder = 10; scene.add(halo);
{ const N = 90, pos = []; for (let i=0;i<N;i++){ const y = 1 - (i+0.5)/N*2, r = Math.sqrt(1-y*y), th = i*Math.PI*(3-Math.sqrt(5)); const d = new THREE.Vector3(Math.cos(th)*r, y, Math.sin(th)*r);
    pos.push(...d.clone().multiplyScalar(1.3).toArray(), ...d.clone().multiplyScalar(1.41).toArray()); }
  const g = new THREE.BufferGeometry(); g.setAttribute('position', new THREE.Float32BufferAttribute(pos,3)); scene.add(new THREE.LineSegments(g, new THREE.LineBasicMaterial({color:glow, transparent:true, opacity:0.45}))); }
const G = new THREE.Group(); scene.add(G);
// directions: Fibonacci sphere
const dirs = []; for (let i=0;i<NS;i++){ const y = 1 - (i+0.5)/NS*2, r = Math.sqrt(1-y*y), th = i*Math.PI*(3-Math.sqrt(5)); dirs.push(new THREE.Vector3(Math.cos(th)*r, y, Math.sin(th)*r)); }
// edges: each tip to its nearest neighbours (an approximate geodesic net)
const edges = new Set(); for (let i=0;i<NS;i++){ const near = dirs.map((d,j) => [d.distanceTo(dirs[i]), j]).filter(x => x[1] !== i).sort((a,b) => a[0]-b[0]).slice(0, 5);
  const dmin = near[0][0]; near.forEach(([d,j]) => { if (d < dmin*1.45) edges.add(i < j ? i+'-'+j : j+'-'+i); }); }
const hot = col.clone().lerp(new THREE.Color('#ff5a3c'), 0.45);
const soft = (c, o) => new THREE.MeshBasicMaterial({color:c, transparent:true, opacity:o, depthWrite:false});
const k = Math.sqrt(24/NS);   // thinner as they multiply, so the whole keeps its weight
const layers = [[0.0055, hot, 0.95], [0.010, hot, 0.38], [0.016, col, 0.22], [0.024, col, 0.13], [0.034, col, 0.075], [0.048, glow, 0.04]];
const beam = (a, b, kk=1) => { const len = a.distanceTo(b), mid = a.clone().add(b).multiplyScalar(0.5), q2 = new THREE.Quaternion().setFromUnitVectors(new THREE.Vector3(0,1,0), b.clone().sub(a).normalize());
  for (const [r,c,o] of layers) { const m = new THREE.Mesh(new THREE.CylinderGeometry(r*kk, r*kk, len, 10, 1, true), soft(c, o)); m.position.copy(mid); m.quaternion.copy(q2); G.add(m); } };
const trunk = (a, b) => { const len = a.distanceTo(b), grp = new THREE.Group(); grp.position.copy(a.clone().add(b).multiplyScalar(0.5)); grp.quaternion.setFromUnitVectors(new THREE.Vector3(0,1,0), b.clone().sub(a).normalize());
  for (const [r,c,o] of layers) { const pts = []; for (let i=0;i<=40;i++){ const u = i/40; pts.push(new THREE.Vector2((r + 0.05*Math.exp(-u*9) + 0.012*Math.exp(-u*3.5))*k*1.15, u*len - len/2)); }
    grp.add(new THREE.Mesh(new THREE.LatheGeometry(pts, 20), new THREE.MeshBasicMaterial({color:c, transparent:true, opacity:o, depthWrite:false, side:THREE.DoubleSide}))); }
  G.add(grp); };
const cv = document.createElement('canvas'); cv.width = cv.height = 128; const cx = cv.getContext('2d');
const gr = cx.createRadialGradient(64,64,0,64,64,64); gr.addColorStop(0,'rgba(255,255,255,1)'); gr.addColorStop(0.25,'rgba(255,255,255,0.55)'); gr.addColorStop(0.6,'rgba(255,255,255,0.12)'); gr.addColorStop(1,'rgba(255,255,255,0)');
cx.fillStyle = gr; cx.fillRect(0,0,128,128); const tex = new THREE.CanvasTexture(cv);
const spr = (pos, size, c, o) => { const sp = new THREE.Sprite(new THREE.SpriteMaterial({map:tex, color:c, transparent:true, opacity:o, depthWrite:false})); sp.position.copy(pos); sp.scale.setScalar(size); G.add(sp); };
const R0 = 0.30, Rin = 0.33, Rout = 0.94;
for (const d of dirs) { trunk(d.clone().multiplyScalar(R0*0.92), d.clone().multiplyScalar(Rout)); spr(d.clone().multiplyScalar(Rout), 0.13*k*1.2, hot, 1.0); spr(d.clone().multiplyScalar(Rout), 0.3*k*1.2, col, 0.5); spr(d.clone().multiplyScalar(Rin), 0.08*k, hot, 0.9); }
for (const e of edges) { const [i,j] = e.split('-').map(Number); beam(dirs[i].clone().multiplyScalar(Rout), dirs[j].clone().multiplyScalar(Rout), k*1.1); beam(dirs[i].clone().multiplyScalar(Rin), dirs[j].clone().multiplyScalar(Rin), 0.45*k); }
G.add(new THREE.Mesh(new THREE.SphereGeometry(R0, 64, 48), new THREE.ShaderMaterial({ transparent:true, depthWrite:false, uniforms:{c:{value:col}, h:{value:hot}},
  vertexShader:`varying vec3 vN; varying vec3 vV; void main(){ vec4 mv = modelViewMatrix*vec4(position,1.0); vN = normalize(normalMatrix*normal); vV = normalize(-mv.xyz); gl_Position = projectionMatrix*mv; }`,
  fragmentShader:`uniform vec3 c; uniform vec3 h; varying vec3 vN; varying vec3 vV; void main(){ float f = 1.0 - max(dot(vN,vV),0.0); vec3 col = mix(h, c, f); gl_FragColor = vec4(col, 0.10 + pow(f,1.4)*0.75); }`})));
spr(new THREE.Vector3(), 1.2, col, 0.35); spr(new THREE.Vector3(), 0.6, hot, 0.55); spr(new THREE.Vector3(), 0.24, hot, 0.9);
G.rotation.set(0.35, 0.5, 0.1); G.scale.multiplyScalar(1.45);
// depth cues and layer split, as in the Nov 3 source
G.updateMatrixWorld(true);
const cdir = camera.position.clone().normalize(), layer = P.get('layer') || 'all', wp = new THREE.Vector3(), R = 1.45*0.94;
for (const ch of [...G.children]) { ch.getWorldPosition(wp); const t = THREE.MathUtils.clamp(wp.dot(cdir)/R, -1, 1), f = (t + 1)/2, isCenter = wp.length() < 0.05;
  if (!isCenter) { ch.traverse(o => { if (o.material && o.material.opacity !== undefined) o.material.opacity *= (0.12 + 0.88*Math.pow(f, 1.7)); });
    if (ch.isSprite) ch.scale.multiplyScalar(0.45 + 0.95*f); else ch.scale.x = ch.scale.z = 0.4 + 1.3*f; }
  if (layer === 'back' && (t >= 0 || isCenter)) ch.visible = false; if (layer === 'front' && t < 0 && !isCenter) ch.visible = false; }
if (layer === 'front' || layer === 'back') scene.children.forEach(o => { if (o !== G) o.visible = false; });
if (layer === 'shell') G.visible = false;
renderer.render(scene, camera); document.body.dataset.done = '1';
</script>
</body></html>

```
