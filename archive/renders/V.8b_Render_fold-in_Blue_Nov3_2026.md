# BWTC render fold-in: blue — Nov 3 2026

**Target**: `claude/bwtc_3d_centers_render.html`. Carries the authority of that file's blue section until spliced in. The render file is too large to retype safely in one pass (the orange TRIQ array), so the new blue code lands here first.

**To splice into render.html:**
1. Replace the whole `if (form === 'blue') { … }` block (the early solid gem) with the block below.
2. In the tail, change the two green-only lines to `if (form === 'green' || form === 'blue')` (blue hides the equator ring and the 0.09 core, like green).
3. In `SCALE`, set `blue: 1.0`.
4. Add `form === 'blue'` to the depth condition.

**Render:** layered method (like red and yellow): `node shoot_layers.js blue && python3 composite.py blue`.

**Status:** Claude's first draft, sent to Doug November 3; blob a2d481f58b311132d2eea1a626686324 on the canvas. Doug (Nov 3): bring the facets to the edge of the outer sphere — outer gem radius now 1.40, at the membrane. Doug (Nov 3): facets at the edge approved ("good"); center sphere made a little more prominent (radius 0.34, stronger glow). Awaiting Doug's direction.

```js
if (form === 'blue') { // "capable of having perhaps one hundred facets and capable of great flashing brilliance" (51.8): a gem of light, 92 facets, light pouring out through them
  const line = new THREE.Color('#2462B0'), hot = new THREE.Color('#4E9BEA'), glw = new THREE.Color('#9CC8F5'), white = new THREE.Color('#EAF4FF');
  const soft = (c, o) => new THREE.MeshBasicMaterial({color:c, transparent:true, opacity:o, depthWrite:false, side:THREE.DoubleSide});
  const layersThin = [[0.0032, white, 0.95], [0.0065, hot, 0.45], [0.011, line, 0.2], [0.018, line, 0.1], [0.028, glw, 0.05]];
  const beam = (a, b, k=1, st=1) => { const len = a.distanceTo(b), grp = new THREE.Group();
    grp.position.copy(a.clone().add(b).multiplyScalar(0.5)); grp.quaternion.setFromUnitVectors(new THREE.Vector3(0,1,0), b.clone().sub(a).normalize());
    for (const [r,c,o] of layersThin) grp.add(new THREE.Mesh(new THREE.CylinderGeometry(r*k, r*k, len, 8, 1, true), soft(c, o*st)));
    G.add(grp); };
  const cv = document.createElement('canvas'); cv.width = cv.height = 128; const cx = cv.getContext('2d');
  const gr = cx.createRadialGradient(64,64,0,64,64,64); gr.addColorStop(0,'rgba(255,255,255,1)'); gr.addColorStop(0.25,'rgba(255,255,255,0.55)'); gr.addColorStop(0.6,'rgba(255,255,255,0.12)'); gr.addColorStop(1,'rgba(255,255,255,0)');
  cx.fillStyle = gr; cx.fillRect(0,0,128,128); const tex = new THREE.CanvasTexture(cv);
  const spr = (pos, size, c, o) => { const sp = new THREE.Sprite(new THREE.SpriteMaterial({map:tex, color:c, transparent:true, opacity:o, depthWrite:false})); sp.position.copy(pos); sp.scale.setScalar(size); G.add(sp); return sp; };
  // a flash: a four-pointed glint, the way a cut stone throws light
  const cf = document.createElement('canvas'); cf.width = cf.height = 256; const fx = cf.getContext('2d');
  const fg = fx.createRadialGradient(128,128,0,128,128,128); fg.addColorStop(0,'rgba(255,255,255,1)'); fg.addColorStop(0.12,'rgba(255,255,255,0.5)'); fg.addColorStop(0.4,'rgba(255,255,255,0.06)'); fg.addColorStop(1,'rgba(255,255,255,0)');
  fx.fillStyle = fg; fx.fillRect(0,0,256,256);
  for (const [w, L, al] of [[3, 128, 0.95], [7, 100, 0.35]]) { fx.save(); fx.translate(128,128);
    for (const ang of [0, Math.PI/2, Math.PI/4, -Math.PI/4]) { fx.rotate(ang); const s = (ang === 0 || ang === Math.PI/2) ? 1 : 0.45; const lg = fx.createLinearGradient(-L*s,0,L*s,0); lg.addColorStop(0,'rgba(255,255,255,0)'); lg.addColorStop(0.5,`rgba(255,255,255,${al})`); lg.addColorStop(1,'rgba(255,255,255,0)'); fx.fillStyle = lg; fx.fillRect(-L*s, -w/2, 2*L*s, w); fx.rotate(-ang); }
    fx.restore(); }
  const ftex = new THREE.CanvasTexture(cf);
  const flash = (pos, size, c, o) => { const sp = new THREE.Sprite(new THREE.SpriteMaterial({map:ftex, color:c, transparent:true, opacity:o, depthWrite:false})); sp.position.copy(pos); sp.scale.setScalar(size); G.add(sp); };
  // the facets: the dual of a frequency-3 geodesic sphere (92 faces: 12 pentagons, 80 hexagons)
  const geo = new THREE.IcosahedronGeometry(1, 2), pa = geo.attributes.position;
  const verts = [], key = v => v.toArray().map(x => x.toFixed(4)).join(','), vid = new Map(), tris = [];
  for (let i=0;i<pa.count;i+=3) { const t = []; for (let j=0;j<3;j++){ const v = new THREE.Vector3().fromBufferAttribute(pa, i+j).normalize(), k = key(v); if (!vid.has(k)) { vid.set(k, verts.length); verts.push(v); } t.push(vid.get(k)); } tris.push(t); }
  const cents = tris.map(t => verts[t[0]].clone().add(verts[t[1]]).add(verts[t[2]]).normalize());
  const edgeMap = new Map(); tris.forEach((t, ti) => { for (let j=0;j<3;j++){ const a = Math.min(t[j], t[(j+1)%3]), b = Math.max(t[j], t[(j+1)%3]), k = a+'_'+b; (edgeMap.get(k) || edgeMap.set(k, []).get(k)).push(ti); } });
  const dualEdges = [...edgeMap.values()].filter(v => v.length === 2);
  const faces = verts.map((v, vi) => { const ts = []; tris.forEach((t, ti) => { if (t.includes(vi)) ts.push(ti); });
    const u = new THREE.Vector3(0,1,0); if (Math.abs(v.y) > 0.9) u.set(1,0,0); const e1 = u.clone().cross(v).normalize(), e2 = v.clone().cross(e1);
    ts.sort((a, b) => { const pa = cents[a].clone().sub(v), pb = cents[b].clone().sub(v); return Math.atan2(pa.dot(e2), pa.dot(e1)) - Math.atan2(pb.dot(e2), pb.dot(e1)); });
    return { n: v, ring: ts }; });
  let seed = 7; const rnd = () => (seed = (seed * 16807) % 2147483647) / 2147483647;
  const RL = 1.40, axis = new THREE.Vector3(0.25, 1, 0.15).normalize();
  // nested gems: the smallest born at the core's surface, each larger one turned further, out to the full stone at the membrane
  const NEST = [[0.34, -0.8, 0.38], [0.62, -0.4, 0.55], [1.0, 0.0, 1.0]];   // [scale, turn, strength]
  for (const [sc, turn, st] of NEST) {
    const T = v => v.clone().applyAxisAngle(axis, turn).multiplyScalar(sc * RL), k = Math.pow(sc, 0.55);
    for (const [a, b] of dualEdges) beam(T(cents[a]), T(cents[b]), k, st);
    for (const c of cents) spr(T(c), 0.06*k, hot, 0.8*st);
    if (sc === 1.0) {
      // facet planes: faint, each catching a different amount of light; a few blaze
      for (const f of faces) {
        const pts = f.ring.map(ti => T(cents[ti])), ctr = T(f.n.clone().multiplyScalar(0.985)); const lit = rnd();
        const pos = []; for (let i=0;i<pts.length;i++){ const p = pts[i], q = pts[(i+1)%pts.length]; pos.push(...ctr.toArray(), ...p.toArray(), ...q.toArray()); }
        const g = new THREE.BufferGeometry(); g.setAttribute('position', new THREE.Float32BufferAttribute(pos, 3)); g.translate(-ctr.x, -ctr.y, -ctr.z);
        const grp = new THREE.Group(); grp.add(new THREE.Mesh(g, soft(lit > 0.8 ? white : (lit > 0.5 ? glw : hot), lit > 0.8 ? 0.42 : 0.03 + 0.14*lit)));
        grp.position.copy(ctr); grp.userData.noScale = true; G.add(grp);
      }
      // outward radiance: light streaming from the core through each facet
      for (const f of faces) { const a = T(f.n.clone().multiplyScalar(0.3)), b = T(f.n.clone().multiplyScalar(0.97)); beam(a, b, 0.5, 0.4); }
      // great flashing brilliance: glints on a scatter of facets
      seed = 31; for (const f of faces) { if (rnd() < 0.24) { const p = T(f.n.clone().multiplyScalar(1.0)), s = 0.32 + 0.5*rnd(); flash(p, s, white, 1.0); spr(p, s*0.6, hot, 0.55); spr(p, 0.08, white, 1.0); } }
    }
  }
  // inner radiance: a luminous core
  G.add(new THREE.Mesh(new THREE.SphereGeometry(0.34, 64, 48), new THREE.ShaderMaterial({ transparent:true, depthWrite:false, uniforms:{c:{value:line}, h:{value:hot}},
    vertexShader:`varying vec3 vN; varying vec3 vV; void main(){ vec4 mv = modelViewMatrix*vec4(position,1.0); vN = normalize(normalMatrix*normal); vV = normalize(-mv.xyz); gl_Position = projectionMatrix*mv; }`,
    fragmentShader:`uniform vec3 c; uniform vec3 h; varying vec3 vN; varying vec3 vV; void main(){ float f = 1.0 - max(dot(vN,vV),0.0); gl_FragColor = vec4(mix(h, c, f), 0.16 + pow(f,1.3)*0.78);
#include <colorspace_fragment>
}`})));
  spr(new THREE.Vector3(), 2.2, glw, 0.5); spr(new THREE.Vector3(), 1.2, hot, 0.7); spr(new THREE.Vector3(), 0.6, hot, 0.95); spr(new THREE.Vector3(), 0.3, white, 1.0); spr(new THREE.Vector3(), 0.14, white, 1.0);
  G.rotation.set(0.3, 0.45, 0.06);
}
```
