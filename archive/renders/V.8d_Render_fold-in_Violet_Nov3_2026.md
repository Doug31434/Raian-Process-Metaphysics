# BWTC render fold-in: violet — Nov 3 2026

**Target**: `claude/bwtc_3d_centers_render.html`. Carries the authority of that file's violet section until spliced in (the render file is too large to retype safely in one pass). Read with the blue and indigo render fold-ins.

**To splice into render.html:**
1. Replace the whole `if (form === 'violet') { … }` block (the early solid petals) with the block below.
2. In the tail, add `form === 'violet'` to the ring-hiding and core-hiding lines and to the depth condition. (Violet's meshes are marked `shaderDepth`; depth is set per petal by color in the block itself.)
3. In `SCALE`, set `violet: 1.0`. `ELEV` stays 30.

**Render:** single pass: `node shoot.js violet && python3 bloom.py violet`.

**Status:** Claude's first draft, sent to Doug November 3 (Doug: "can we do the last energy center"); blob a0dbafb4bfcf277fb073f4b189c5d9bd on the canvas. Doug (Nov 3) first asked for more facets, then ruled: "we should use Ra's words, not mine, and make sure you cite appropriately." The faceted version was withdrawn and the thousand-petaled draft restored (code and image identical to the first draft). Card citations re-verified in Vol. 1 (51.8, 34.15, 15.12, 39.10, 54.30, 47.8, 49.6, 41.16, 49.2); the 49.2 line on the card now quotes Ra's own sentence ("may then yield not only the experience of joy but the comprehension of intelligent infinity which accompanies it"). Awaiting Doug's direction.

**Log line (for the BWTC fold-in).** Violet graphic, first draft (Claude, November 3): a thousand petals of light (70, 160, 290, 480) in four nested crowns, every petal pointing outward in all directions from a radiant core; evenly spaced and steady, for "the least variable" center and "the sum" (51.8); the joy of being as the core's light. No equator ring.


**Correction to carry (Nov 3).** `claude/The Seven BWTCs Under the Eight Categories Nov3 2026.md`, Violet 7a footing, should read: Ra: the experience "of a sacramental, or violet, ray" … "may then yield not only the experience of joy but the comprehension of intelligent infinity which accompanies it" (49.2). The remade chart (artifact WzUkmw67kcNX5e7SgT97Lh, version 2) already carries the corrected wording.

```js
if (form === 'violet') { // "the least variable and is sometimes described in your philosophy as thousand-petaled, as it is the sum of the mind/body/spirit complex distortion totality" (51.8)
  const line = new THREE.Color('#7A3FA8'), hot = new THREE.Color('#A86BD8'), glw = new THREE.Color('#D2B2F0'), white = new THREE.Color('#F7EEFF'), cream = new THREE.Color('#EADFC8');
  // a petal of light: bright edge, soft glowing body, pointed tip
  const pc = document.createElement('canvas'); pc.width = 64; pc.height = 160; const px = pc.getContext('2d');
  const petalPath = () => { px.beginPath(); px.moveTo(32, 156); px.bezierCurveTo(4, 120, 6, 40, 32, 4); px.bezierCurveTo(58, 40, 60, 120, 32, 156); px.closePath(); };
  const body = px.createLinearGradient(0, 156, 0, 4); body.addColorStop(0, 'rgba(255,255,255,0.3)'); body.addColorStop(0.5, 'rgba(255,255,255,0.55)'); body.addColorStop(1, 'rgba(255,255,255,0.85)');
  petalPath(); px.fillStyle = body; px.fill(); px.lineWidth = 4; px.strokeStyle = 'rgba(255,255,255,0.95)'; px.stroke();
  const ptex = new THREE.CanvasTexture(pc);
  const pgeo = new THREE.PlaneGeometry(1, 1); pgeo.translate(0, 0.5, 0);   // base at the origin, petal pointing along +y
  const cdir = camera.position.clone().normalize();
  // a thousand petals in four nested crowns, every one pointing outward from the center: the sum, in all directions
  const CROWNS = [[0.40, 70, 0.16, 0.055, white], [0.66, 160, 0.19, 0.06, white.clone().lerp(glw, 0.5)], [0.93, 290, 0.21, 0.064, glw], [1.18, 480, 0.22, 0.066, hot]];   // [radius, count, length, width, color]
  const dummy = new THREE.Object3D(), yAx = new THREE.Vector3(0,1,0);
  CROWNS.forEach(([R, N, L, W, c], ci) => {
    const inst = new THREE.InstancedMesh(pgeo, new THREE.MeshBasicMaterial({map:ptex, transparent:true, opacity:0.9, depthWrite:false, side:THREE.DoubleSide, color:0xffffff}), N);
    for (let i=0;i<N;i++) {
      const y = 1 - (i+0.5)/N*2, r = Math.sqrt(1-y*y), th = i*Math.PI*(3-Math.sqrt(5)) + ci*0.37;
      const d = new THREE.Vector3(Math.cos(th)*r, y, Math.sin(th)*r);
      dummy.position.copy(d.clone().multiplyScalar(R));
      dummy.quaternion.setFromUnitVectors(yAx, d);
      dummy.rotateY((i*2.399) % Math.PI);   // each petal turned about its own axis, so the crown reads in the round
      dummy.scale.set(W, L, 1); dummy.updateMatrix(); inst.setMatrixAt(i, dummy.matrix);
      const f = (d.dot(cdir) + 1) / 2;   // near = 1, far = 0
      inst.setColorAt(i, cream.clone().lerp(c, 0.55 + 0.45*Math.pow(f, 1.2)));
    }
    inst.userData.shaderDepth = true; G.add(inst);
  });
  // the joy of being: a radiant crown of light at the heart, steady and even
  const cv = document.createElement('canvas'); cv.width = cv.height = 128; const cx = cv.getContext('2d');
  const gr = cx.createRadialGradient(64,64,0,64,64,64); gr.addColorStop(0,'rgba(255,255,255,1)'); gr.addColorStop(0.25,'rgba(255,255,255,0.55)'); gr.addColorStop(0.6,'rgba(255,255,255,0.12)'); gr.addColorStop(1,'rgba(255,255,255,0)');
  cx.fillStyle = gr; cx.fillRect(0,0,128,128); const tex = new THREE.CanvasTexture(cv);
  const spr = (pos, size, c, o) => { const sp = new THREE.Sprite(new THREE.SpriteMaterial({map:tex, color:c, transparent:true, opacity:o, depthWrite:false})); sp.position.copy(pos); sp.scale.setScalar(size); sp.userData.shaderDepth = true; G.add(sp); };
  G.add(new THREE.Mesh(new THREE.SphereGeometry(0.26, 64, 48), new THREE.ShaderMaterial({ transparent:true, depthWrite:false, uniforms:{c:{value:line}, h:{value:white}},
    vertexShader:`varying vec3 vN; varying vec3 vV; void main(){ vec4 mv = modelViewMatrix*vec4(position,1.0); vN = normalize(normalMatrix*normal); vV = normalize(-mv.xyz); gl_Position = projectionMatrix*mv; }`,
    fragmentShader:`uniform vec3 c; uniform vec3 h; varying vec3 vN; varying vec3 vV; void main(){ float f = 1.0 - max(dot(vN,vV),0.0); gl_FragColor = vec4(mix(h, c, f), 0.3 + pow(f,1.3)*0.6);
#include <colorspace_fragment>
}`})));
  G.children[G.children.length-1].userData.shaderDepth = true;
  spr(new THREE.Vector3(), 2.6, glw, 0.55); spr(new THREE.Vector3(), 1.3, white, 0.6); spr(new THREE.Vector3(), 0.55, white, 0.9); spr(new THREE.Vector3(), 0.22, white, 1.0);
}
```
