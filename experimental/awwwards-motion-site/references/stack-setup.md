# Stack Setup — wiring the engine

The two paths. Pick one based on the project (see SKILL.md "Decide the stack first").

---

## Path A — Next.js / React

### Install

```bash
npm i lenis gsap split-type
# Real-time 3D is OPTIONAL and usually NOT needed (see "The centerpiece object" below).
# Only if the object must react to the pointer / be configurable, pick ONE:
# npm i three @react-three/fiber @react-three/drei   # R3F (full control)
# npm i @splinetool/react-spline                       # Spline runtime
```

### The Lenis ↔ GSAP bridge (THE critical piece)

If you skip this, ScrollTrigger and Lenis fight and everything mis-positions. Drive GSAP's ticker
from Lenis and tell ScrollTrigger to update on Lenis scroll.

```tsx
// app/SmoothScroll.tsx  (client component, mount once near the root)
"use client";
import { useEffect } from "react";
import Lenis from "lenis";
import gsap from "gsap";
import { ScrollTrigger } from "gsap/ScrollTrigger";

gsap.registerPlugin(ScrollTrigger);

export default function SmoothScroll({ children }: { children: React.ReactNode }) {
  useEffect(() => {
    if (window.matchMedia("(prefers-reduced-motion: reduce)").matches) return;

    const lenis = new Lenis({ duration: 1.1, smoothWheel: true });
    lenis.on("scroll", ScrollTrigger.update);

    const raf = (time: number) => lenis.raf(time * 1000); // gsap ticker is in seconds
    gsap.ticker.add(raf);
    gsap.ticker.lagSmoothing(0);

    return () => {
      gsap.ticker.remove(raf);
      lenis.destroy();
    };
  }, []);

  return <>{children}</>;
}
```

Wrap your layout/page content in `<SmoothScroll>`. Import `lenis/dist/lenis.css` (or set
`html.lenis,html.lenis body{height:auto}` and `.lenis.lenis-smooth{scroll-behavior:auto!important}`).

### Per-component animations

Use `useGSAP` (from `@gsap/react`, `npm i @gsap/react`) or a plain `useEffect` with a `gsap.context`
scoped to a ref so tweens clean up on unmount. Pattern:

```tsx
const root = useRef<HTMLElement>(null);
useGSAP(() => {
  gsap.from(".reveal-line", {
    yPercent: 110, duration: 1, ease: "expo.out", stagger: 0.06,
  });
}, { scope: root });
```

---

## Path B — Plain single-file HTML (no build)

Hand-back-ready, zero tooling. Use CDN GSAP + Lenis + a Spline embed.

```html
<script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.5/gsap.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.5/ScrollTrigger.min.js"></script>
<script type="module">
  import Lenis from "https://cdn.jsdelivr.net/npm/lenis@1/dist/lenis.mjs";
  gsap.registerPlugin(ScrollTrigger);
  const lenis = new Lenis({ duration: 1.1 });
  lenis.on("scroll", ScrollTrigger.update);
  gsap.ticker.add((t) => lenis.raf(t * 1000));
  gsap.ticker.lagSmoothing(0);
  // ...your tweens
</script>
```

(In Claude.ai artifacts: SplitType via CDN works; Lenis via the esm.sh/jsdelivr module URL.)

---

## The centerpiece object

**Default to a pre-rendered image, not real-time 3D.** The hanging container / floating product look
is almost always a high-quality render that is *moved*, not geometry computed in the browser. This is
lighter, more reliable, easier to art-direct, and indistinguishable from real-time for a non-interactive
hero. Three approaches, in order of preference:

### Option 1 — Single pre-rendered image + scroll transforms (default, what most of these sites do)

1. Get one high-quality render of the object on a transparent background (PNG/WebP). Sources: model it
   in Blender and render once; commission/stock a product render; or generate + clean up an image. Map
   the brand onto it (a texture in Blender, or just composite the logo).
2. Place it in the hero and animate **only `transform`/`opacity`** with GSAP tied to scroll — translate,
   rotate a few degrees, scale, and swing the hook. The render's own lighting carries the depth.

```html
<div class="hero">
  <h1 class="display">Precision</h1>
  <img class="centerpiece" src="/container.webp" alt="" />
  <h1 class="display display--end">Delivery</h1>
</div>
```

```js
// gentle float on load + scroll-driven drift/rotation
gsap.from(".centerpiece", { y: 80, autoAlpha: 0, scale: 0.92, duration: 1.2, ease: "expo.out" });

gsap.to(".centerpiece", {
  yPercent: 18, rotation: 4, ease: "none",
  scrollTrigger: { trigger: ".hero", start: "top top", end: "bottom top", scrub: 1 },
});

// optional: pointer parallax (no 3D needed)
window.addEventListener("mousemove", (e) => {
  const dx = (e.clientX / innerWidth - 0.5);
  const dy = (e.clientY / innerHeight - 0.5);
  gsap.to(".centerpiece", { x: dx * 30, y: dy * 20, rotation: dx * 3, duration: 0.8, ease: "power3.out", overwrite: "auto" });
});
```

The faint "ghost" you sometimes see in screen recordings of these sites is camera motion blur or a
subtle CSS trail — not a model changing. You can fake it with a brief `filter: blur()` during fast
scroll if you want that signature smear.

### Option 2 — Pre-rendered image SEQUENCE scrubbed on a canvas (the "Apple AirPods" rotation)

When you want a genuine-looking full rotation driven by scroll, render the turntable in Blender as
60–120 frames, then flip through them on a `<canvas>` by scroll progress. Still flat pre-rendered
images, still zero WebGL.

```js
const canvas = document.querySelector("#seq");
const ctx = canvas.getContext("2d");
const FRAMES = 90;
const imgs = [];
let loaded = 0;
for (let i = 0; i < FRAMES; i++) {
  const img = new Image();
  img.src = `/seq/container_${String(i).padStart(4, "0")}.webp`;
  img.onload = () => { if (++loaded === 1) draw(0); };
  imgs[i] = img;
}
function draw(i) {
  const img = imgs[Math.round(i)];
  if (img?.complete) ctx.drawImage(img, 0, 0, canvas.width, canvas.height);
}
const state = { frame: 0 };
gsap.to(state, {
  frame: FRAMES - 1, ease: "none",
  scrollTrigger: { trigger: ".hero", start: "top top", end: "+=200%", pin: true, scrub: 1 },
  onUpdate: () => draw(state.frame),
});
```

Keep frames as compressed WebP, preload, and cap canvas resolution (1× retina) to control weight.

### Option 3 — Real-time 3D (only when interactivity demands it)

Use Spline (in-browser modeling, embeddable) or React Three Fiber + a GLB **only** if the object must
react live to the pointer, be configured by the user, or animate beyond what a render can do.

Spline (React): `import Spline from "@splinetool/react-spline"; <Spline scene="https://prod.spline.design/XXXX/scene.splinecode" />`
Spline (HTML): `<script type="module" src="https://unpkg.com/@splinetool/viewer/build/spline-viewer.js"></script>` then `<spline-viewer url="…"></spline-viewer>`

R3F skeleton:

```tsx
import { Canvas } from "@react-three/fiber";
import { useGLTF, Environment, Float } from "@react-three/drei";

function Container() { const { scene } = useGLTF("/container.glb"); return <primitive object={scene} />; }

export default function Hero3D() {
  return (
    <Canvas camera={{ position: [0, 0, 6], fov: 35 }} dpr={[1, 1.75]}>
      <Environment preset="studio" />
      <Float speed={1.2} rotationIntensity={0.4} floatIntensity={0.6}><Container /></Float>
    </Canvas>
  );
}
useGLTF.preload("/container.glb");
```

Pointer/scroll reaction with `useFrame` → see `motion-patterns.md` → "Real-time 3D reaction."
Performance: clamp `dpr`, lazy-mount when in view, static poster on mobile / reduced-motion.