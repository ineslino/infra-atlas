/* globe.js — Interactive 3D globe for infraatlas.dev
   Requires THREE (three.min.js) to be loaded as a global before this script.
   Self-contained IIFE, no build step, no imports.
*/
(function () {
  'use strict';

  /* ── Guards ──────────────────────────────────────────────────── */
  if (typeof THREE === 'undefined') return;
  if (document.getElementById('ia-globe')) return; // already mounted

  // WebGL check
  (function () {
    try {
      var c = document.createElement('canvas');
      if (!(c.getContext('webgl') || c.getContext('experimental-webgl'))) throw 0;
    } catch (e) {
      document.documentElement.classList.add('ia-no-webgl');
      return false;
    }
    return true;
  })() || function () { return; }();

  if (document.documentElement.classList.contains('ia-no-webgl')) return;

  /* ── Preferences & capabilities ──────────────────────────────── */
  var RM     = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var MOBILE = window.innerWidth <= 768;
  var DPR    = Math.min(window.devicePixelRatio || 1, MOBILE ? 1.5 : 2.0);

  /* ── Region data (AWS regions, desktop: 14, mobile: 8) ─────────── */
  var REGIONS_ALL = [
    { lat:  38.9, lng:  -77.5 }, // 0  us-east-1      (N. Virginia)
    { lat:  45.8, lng: -119.7 }, // 1  us-west-2      (Oregon)
    { lat:  53.3, lng:   -6.3 }, // 2  eu-west-1      (Ireland)
    { lat:  50.1, lng:    8.7 }, // 3  eu-central-1   (Frankfurt)
    { lat:   1.3, lng:  103.8 }, // 4  ap-southeast-1 (Singapore)
    { lat:  35.7, lng:  139.7 }, // 5  ap-northeast-1 (Tokyo)
    { lat:  19.1, lng:   72.9 }, // 6  ap-south-1     (Mumbai)
    { lat: -33.9, lng:  151.2 }, // 7  ap-southeast-2 (Sydney)
    { lat:  51.5, lng:   -0.1 }, // 8  eu-west-2      (London)
    { lat:  40.4, lng:  -82.9 }, // 9  us-east-2      (Ohio)
    { lat: -23.5, lng:  -46.6 }, // 10 sa-east-1      (São Paulo)
    { lat:  45.5, lng:  -73.6 }, // 11 ca-central-1   (Montreal)
    { lat:  37.5, lng:  126.9 }, // 12 ap-northeast-2 (Seoul)
    { lat:  59.3, lng:   18.1 }  // 13 eu-north-1     (Stockholm)
  ];

  var ARC_PAIRS_ALL = [
    [0, 8],   // us-east-1  → London
    [1, 5],   // us-west-2  → Tokyo
    [2, 4],   // eu-west-1  → Singapore
    [3, 6],   // eu-central-1 → Mumbai
    [0, 10],  // us-east-1  → São Paulo
    [4, 7]    // Singapore  → Sydney
  ];

  var regions  = MOBILE ? REGIONS_ALL.slice(0, 8)     : REGIONS_ALL;
  var arcPairs = MOBILE ? ARC_PAIRS_ALL.slice(0, 3)   : ARC_PAIRS_ALL;

  /* ── Helpers ─────────────────────────────────────────────────── */
  function ll2v(lat, lng, r) {
    var phi   = (90 - lat) * (Math.PI / 180);
    var theta = (lng + 180) * (Math.PI / 180);
    return new THREE.Vector3(
      -r * Math.sin(phi) * Math.cos(theta),
       r * Math.cos(phi),
       r * Math.sin(phi) * Math.sin(theta)
    );
  }

  function buildArcPoints(r1, r2, segs) {
    var ALT = 0.30;
    var a   = ll2v(r1.lat, r1.lng, 1);
    var b   = ll2v(r2.lat, r2.lng, 1);
    var pts = [];
    for (var i = 0; i <= segs; i++) {
      var t = i / segs;
      var p = a.clone().lerp(b, t).normalize();
      pts.push(p.multiplyScalar(1.0 * (1 + ALT * Math.sin(t * Math.PI))));
    }
    return pts;
  }

  /* ── Canvas + renderer ───────────────────────────────────────── */
  var W = window.innerWidth, H = window.innerHeight;

  var canvas = document.createElement('canvas');
  canvas.id  = 'ia-globe';
  canvas.setAttribute('aria-hidden', 'true');
  canvas.setAttribute('role', 'presentation');
  canvas.style.cssText =
    'position:fixed;inset:0;width:100vw;height:100vh;' +
    'z-index:0;pointer-events:none;' +
    'opacity:1;transition:opacity 0.5s ease;';
  document.body.prepend(canvas);

  var renderer = new THREE.WebGLRenderer({ canvas: canvas, antialias: !MOBILE, alpha: true });
  renderer.setPixelRatio(DPR);
  renderer.setSize(W, H);
  renderer.setClearColor(0x000000, 0);

  /* ── Scene + camera ──────────────────────────────────────────── */
  var scene  = new THREE.Scene();
  var camera = new THREE.PerspectiveCamera(45, W / H, 0.1, 100);
  camera.position.z = 2.85;

  /* ── Globe group (all 3D objects live here for unified rotation) */
  var globe = new THREE.Group();
  globe.rotation.x = -0.12;
  globe.rotation.y = -0.28;
  scene.add(globe);

  /* ── Lights ──────────────────────────────────────────────────── */
  scene.add(new THREE.AmbientLight(0xffffff, 0.6));
  var sun = new THREE.DirectionalLight(0xffffff, 0.65);
  sun.position.set(5, 3, 5);
  scene.add(sun);

  /* ── Globe surface ───────────────────────────────────────────── */
  globe.add(new THREE.Mesh(
    new THREE.SphereGeometry(1.0, 64, 64),
    new THREE.MeshPhongMaterial({
      color:     0x0c0b0e,
      emissive:  0x040305,
      specular:  0x1a1520,
      shininess: 12
    })
  ));

  /* ── Atmosphere glow (FrontSide additive shader) ─────────────── */
  globe.add(new THREE.Mesh(
    new THREE.SphereGeometry(1.15, 64, 64),
    new THREE.ShaderMaterial({
      uniforms: { uColor: { value: new THREE.Color('#FF7849') } },
      vertexShader: [
        'varying vec3 vNormal;',
        'void main(){',
        '  vNormal=normalize(normalMatrix*normal);',
        '  gl_Position=projectionMatrix*modelViewMatrix*vec4(position,1.0);',
        '}'
      ].join('\n'),
      fragmentShader: [
        'uniform vec3 uColor;',
        'varying vec3 vNormal;',
        'void main(){',
        // Edge glow: max strength at limb (dot≈0), zero at dead-center (dot≈1)
        '  float edge=1.0-abs(dot(vNormal,vec3(0.0,0.0,1.0)));',
        '  float i=pow(edge,2.5)*0.55;',
        '  gl_FragColor=vec4(uColor,i);',
        '}'
      ].join('\n'),
      side:        THREE.FrontSide,
      blending:    THREE.AdditiveBlending,
      transparent: true,
      depthWrite:  false
    })
  ));

  /* ── Grid lines ──────────────────────────────────────────────── */
  var gridMat = new THREE.LineBasicMaterial({ color: 0x2b2420, transparent: true, opacity: 0.5 });

  // Latitude lines at -60°, -30°, 0°, 30°, 60°
  [-60, -30, 0, 30, 60].forEach(function (lat) {
    var pts = [], phi = (90 - lat) * Math.PI / 180;
    var yr = Math.cos(phi), xr = Math.sin(phi);
    for (var i = 0; i <= 64; i++) {
      var a = (i / 64) * 2 * Math.PI;
      pts.push(new THREE.Vector3(xr * Math.cos(a), yr, xr * Math.sin(a)));
    }
    globe.add(new THREE.Line(new THREE.BufferGeometry().setFromPoints(pts), gridMat));
  });

  // Longitude lines every 30°
  for (var li = 0; li < 12; li++) {
    var lon = li * 30 * Math.PI / 180, lpts = [];
    for (var si = 0; si <= 64; si++) {
      var th = (si / 64) * Math.PI;
      lpts.push(new THREE.Vector3(
        Math.sin(th) * Math.cos(lon),
        Math.cos(th),
        Math.sin(th) * Math.sin(lon)
      ));
    }
    globe.add(new THREE.Line(new THREE.BufferGeometry().setFromPoints(lpts), gridMat));
  }

  /* ── Region nodes + pulsing rings ───────────────────────────── */
  var nodeDotGeo = new THREE.SphereGeometry(0.012, 8, 8);
  var nodeDotMat = new THREE.MeshBasicMaterial({ color: new THREE.Color('#FF7849') });
  var pulseList  = [];
  var Z_UP       = new THREE.Vector3(0, 0, 1);

  regions.forEach(function (reg) {
    var pos = ll2v(reg.lat, reg.lng, 1.001);

    // Dot on surface
    var dot = new THREE.Mesh(nodeDotGeo, nodeDotMat);
    dot.position.copy(pos);
    globe.add(dot);

    // Pulsing ring — only when motion is allowed
    if (!RM) {
      var ring = new THREE.Mesh(
        new THREE.RingGeometry(0.018, 0.024, 32),
        new THREE.MeshBasicMaterial({
          color: new THREE.Color('#FF7849'),
          transparent: true,
          opacity: 0.55,
          side: THREE.DoubleSide
        })
      );
      ring.position.copy(pos);
      // Orient ring so its plane is tangent to the sphere surface
      ring.quaternion.setFromUnitVectors(Z_UP, pos.clone().normalize());
      globe.add(ring);
      pulseList.push({ mesh: ring, t: Math.random() });
    }
  });

  /* ── Arcs ────────────────────────────────────────────────────── */
  var ARC_SEGS = MOBILE ? 60 : 80;
  var arcList  = [];

  if (!RM) {
    arcPairs.forEach(function (pair, idx) {
      var r1 = regions[pair[0]], r2 = regions[pair[1]];
      if (!r1 || !r2) return;

      var pts = buildArcPoints(r1, r2, ARC_SEGS);
      var geo = new THREE.BufferGeometry().setFromPoints(pts);
      geo.setDrawRange(0, 0);

      var line = new THREE.Line(geo, new THREE.LineBasicMaterial({
        color: new THREE.Color('#FF7849'), transparent: true, opacity: 0.65
      }));
      globe.add(line);

      // Head: white dot that travels along the arc front
      var head = new THREE.Mesh(
        new THREE.SphereGeometry(0.007, 6, 6),
        new THREE.MeshBasicMaterial({ color: 0xffffff })
      );
      head.visible = false;
      globe.add(head);

      arcList.push({
        geo:   geo,
        head:  head,
        pts:   pts,
        // Negative drawLen = pre-delay; stagger starts by arc index
        drawLen: -(idx * 22 + 12),
        speed:   0.40 + Math.random() * 0.25
      });
    });
  }

  /* ── Drag interaction ────────────────────────────────────────── */
  var drag = { on: false, x: 0, y: 0, vx: 0, vy: 0 };

  document.addEventListener('pointerdown', function (e) {
    // Only engage inside the hero viewport area
    var hero = document.querySelector('.hero');
    if (!hero) return;
    if (e.clientY > hero.getBoundingClientRect().bottom) return;
    // Ignore interactive elements
    var el = e.target;
    while (el) {
      if (el.matches && el.matches('a,button,input,select,textarea,[role="button"]')) return;
      el = el.parentElement;
    }
    if (e.pointerType === 'mouse' && e.button !== 0) return;
    drag.on = true;
    drag.x  = e.clientX;
    drag.y  = e.clientY;
    drag.vx = drag.vy = 0;
    e.preventDefault();
  }, { passive: false });

  document.addEventListener('pointermove', function (e) {
    if (!drag.on) return;
    drag.vx = (e.clientX - drag.x) * 0.0032;
    drag.vy = (e.clientY - drag.y) * 0.0032;
    globe.rotation.y += drag.vx;
    globe.rotation.x = Math.max(-1.1, Math.min(0.5, globe.rotation.x + drag.vy));
    drag.x = e.clientX;
    drag.y = e.clientY;
  });

  document.addEventListener('pointerup',     function () { drag.on = false; });
  document.addEventListener('pointercancel', function () { drag.on = false; });

  /* ── Pause / resume ──────────────────────────────────────────── */
  var paused = false;
  var raf    = null;

  function startLoop() {
    if (raf || paused || document.hidden) return;
    raf = requestAnimationFrame(step);
  }

  function stopLoop() {
    if (raf) { cancelAnimationFrame(raf); raf = null; }
  }

  document.addEventListener('visibilitychange', function () {
    if (document.hidden) { stopLoop(); }
    else { startLoop(); }
  });

  /* ── Scroll fade — IntersectionObserver on .hero ─────────────── */
  function setupScrollFade() {
    var hero = document.querySelector('.hero');
    if (!hero) return;

    // 21 thresholds → smooth opacity ramp
    var thresholds = [];
    for (var i = 0; i <= 20; i++) thresholds.push(i / 20);

    new IntersectionObserver(function (entries) {
      var ratio = entries[0].intersectionRatio;
      canvas.style.opacity = String(ratio);

      if (ratio === 0) {
        paused = true;
        stopLoop();
      } else if (paused) {
        paused = false;
        startLoop();
      }
    }, { threshold: thresholds }).observe(hero);
  }

  /* ── Resize ──────────────────────────────────────────────────── */
  window.addEventListener('resize', function () {
    W = window.innerWidth;
    H = window.innerHeight;
    camera.aspect = W / H;
    camera.updateProjectionMatrix();
    renderer.setSize(W, H);
  });

  /* ── Animation step ──────────────────────────────────────────── */
  function step() {
    raf = requestAnimationFrame(step);

    // Auto-rotate (slow, CCW from above)
    if (!drag.on && !RM) {
      globe.rotation.y += 0.00048;
    }

    // Inertia decay after drag
    if (!drag.on) {
      drag.vx *= 0.90;
      drag.vy *= 0.90;
      if (Math.abs(drag.vx) > 0.00005 || Math.abs(drag.vy) > 0.00005) {
        globe.rotation.y += drag.vx;
        globe.rotation.x = Math.max(-1.1, Math.min(0.5, globe.rotation.x + drag.vy));
      }
    }

    // Pulsing rings
    for (var pi = 0; pi < pulseList.length; pi++) {
      var p = pulseList[pi];
      p.t = (p.t + 0.007) % 1.0;
      var s = 1 + p.t * 2.4;
      p.mesh.scale.set(s, s, 1);
      p.mesh.material.opacity = (1 - p.t) * 0.55;
    }

    // Arc draw-range animation
    for (var ai = 0; ai < arcList.length; ai++) {
      var arc = arcList[ai];
      arc.drawLen += arc.speed;

      if (arc.drawLen < 0) {
        // Pre-delay phase — nothing drawn yet
        arc.geo.setDrawRange(0, 0);
        arc.head.visible = false;
        continue;
      }

      var maxPts = arc.pts.length;

      // Past end — reset with a random cooldown
      if (arc.drawLen > maxPts + 16) {
        arc.drawLen = -(18 + Math.random() * 28);
        arc.geo.setDrawRange(0, 0);
        arc.head.visible = false;
        continue;
      }

      var drawCount = Math.min(Math.floor(arc.drawLen), maxPts);
      arc.geo.setDrawRange(0, drawCount);

      // White head dot follows the leading edge
      if (drawCount > 1 && drawCount < maxPts) {
        arc.head.position.copy(arc.pts[drawCount - 1]);
        arc.head.visible = true;
      } else {
        arc.head.visible = false;
      }
    }

    renderer.render(scene, camera);
  }

  /* ── Init ────────────────────────────────────────────────────── */
  function init() {
    setupScrollFade();
    startLoop();
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }

})();
