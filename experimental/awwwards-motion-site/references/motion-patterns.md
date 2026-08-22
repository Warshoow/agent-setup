# Motion Patterns — the signature effects

Each is the GSAP/JS core. Adapt selectors/markup. All assume the Lenis↔GSAP bridge from
`stack-setup.md` is already mounted. Always register `gsap.registerPlugin(ScrollTrigger)`.

---

## 1. Staggered text reveal (hero load + on scroll)

Split into lines, mask each line, slide up with stagger. SplitType does the splitting.

```js
import SplitType from "split-type";

const split = new SplitType(".display", { types: "lines" });
// wrap each line in an overflow:hidden mask
split.lines.forEach((l) => {
  const wrap = document.createElement("span");
  wrap.style.cssText = "display:block;overflow:hidden;";
  l.parentNode.insertBefore(wrap, l);
  wrap.appendChild(l);
});

gsap.from(split.lines, {
  yPercent: 115,
  duration: 1.1,
  ease: "expo.out",
  stagger: 0.08,
  // for on-scroll instead of on-load, add:
  // scrollTrigger: { trigger: ".display", start: "top 80%" }
});
```

Re-run `SplitType` on resize (debounced) or lines break wrong.

---

## 2. Velocity-skewed marquee (the duplicated "We bring logistics…" band)

Two identical tracks for a seamless loop; scroll velocity adds a skew/speed kick.

```html
<div class="marquee"><div class="track"><span>WE BRING LOGISTICS WITH FLAIR&nbsp;</span>
<span>WE BRING LOGISTICS WITH FLAIR&nbsp;</span></div></div>
```

```css
.marquee { overflow: hidden; white-space: nowrap; }
.track { display: inline-flex; will-change: transform; }
```

```js
const track = document.querySelector(".track");
// base loop
const loop = gsap.to(track, { xPercent: -50, repeat: -1, duration: 18, ease: "none" });
// scroll velocity → speed up + skew
ScrollTrigger.create({
  onUpdate: (self) => {
    const v = self.getVelocity();
    loop.timeScale(gsap.utils.clamp(0.3, 4, 1 + Math.abs(v) / 1500));
    gsap.to(track, { skewX: gsap.utils.clamp(-12, 12, v / -250), duration: 0.4, overwrite: "auto" });
  },
});
```

---

## 3. Pinned card stack (images 3/4 — 01/02/03/04 cards peel as you scroll)

Pin the section, drive a timeline by scroll, bring each card up and scale the previous down.

```html
<section class="stack">
  <div class="card">01 — Shipping Details</div>
  <div class="card">02 — Tracking</div>
  <div class="card">03 — Cargo</div>
  <div class="card">04 — Logistics Scheduling</div>
</section>
```

```css
.stack { position: relative; height: 100vh; }
.card { position: absolute; inset: 0; margin: auto; will-change: transform; }
```

```js
const cards = gsap.utils.toArray(".card");
gsap.set(cards, { yPercent: (i) => i * 4, scale: (i) => 1 - i * 0.04, transformOrigin: "top center" });

const tl = gsap.timeline({
  scrollTrigger: {
    trigger: ".stack",
    start: "top top",
    end: () => "+=" + window.innerHeight * cards.length,
    pin: true,
    scrub: 1,
  },
});
cards.forEach((card, i) => {
  if (i === 0) return;
  tl.fromTo(card, { yPercent: 100, scale: 0.95 }, { yPercent: i * 4, scale: 1 - i * 0.04, ease: "power2.out" }, i - 1)
    .to(cards[i - 1], { scale: 0.92, filter: "brightness(0.85)", ease: "power2.out" }, i - 1);
});
```

A vertical **scroll-progress timeline** (the red markers on the right in the refs):

```js
gsap.to(".progress-fill", {
  scaleY: 1, transformOrigin: "top",
  scrollTrigger: { trigger: ".stack", start: "top top", end: () => "+=" + window.innerHeight * cards.length, scrub: true },
});
```

---

## 4. Clip-path polygon reveal (images 5/6 — the worker photo opens as a parallelogram)

Animate `clip-path` points on scroll so the image "opens" from a slanted shape.

```css
.reveal-media { clip-path: polygon(20% 30%, 80% 30%, 80% 70%, 20% 70%); will-change: clip-path; }
```

```js
gsap.to(".reveal-media", {
  clipPath: "polygon(0% 0%, 100% 0%, 100% 100%, 0% 100%)",
  ease: "power3.inOut",
  scrollTrigger: { trigger: ".reveal-media", start: "top 75%", end: "top 30%", scrub: 1 },
});
```

For the angled/diagonal version in the refs, keep a slant in the final state, e.g.
`polygon(0% 8%, 100% 0%, 100% 92%, 0% 100%)`. Pair with a subtle `scale: 1.08 → 1` on the inner
`<img>` for a parallax push.

---

## 5. Services list with cursor-following preview (image 2 — Global Freight / Express Delivery…)

Hovering a row shows a thumbnail that chases the cursor with lerp; row text shifts in accent.

```js
const preview = document.querySelector(".preview"); // fixed/absolute img holder
let tx = 0, ty = 0, x = 0, y = 0;

window.addEventListener("mousemove", (e) => { tx = e.clientX; ty = e.clientY; });
gsap.ticker.add(() => {
  x += (tx - x) * 0.12; y += (ty - y) * 0.12;            // lerp = trailing feel
  gsap.set(preview, { x, y });
});

document.querySelectorAll(".service-row").forEach((row) => {
  const src = row.dataset.img;
  row.addEventListener("mouseenter", () => {
    preview.querySelector("img").src = src;
    gsap.to(preview, { autoAlpha: 1, scale: 1, duration: 0.4, ease: "power3.out" });
    gsap.to(row, { color: "var(--accent)", x: 16, duration: 0.4, ease: "power3.out" });
  });
  row.addEventListener("mouseleave", () => {
    gsap.to(preview, { autoAlpha: 0, scale: 0.8, duration: 0.3 });
    gsap.to(row, { color: "var(--ink)", x: 0, duration: 0.4 });
  });
});
```

Disable on touch (no hover) — show the thumbnails inline instead.

---

## 6. Magnetic CTA button (the "Let's get your cargo →" / "Talk to us" buttons)

```js
document.querySelectorAll(".magnetic").forEach((btn) => {
  btn.addEventListener("mousemove", (e) => {
    const r = btn.getBoundingClientRect();
    gsap.to(btn, { x: (e.clientX - (r.left + r.width / 2)) * 0.3, y: (e.clientY - (r.top + r.height / 2)) * 0.4, duration: 0.6, ease: "power3.out" });
  });
  btn.addEventListener("mouseleave", () => gsap.to(btn, { x: 0, y: 0, duration: 0.6, ease: "elastic.out(1, 0.4)" }));
});
```

---

## 7. Centerpiece reaction (default: pre-rendered image; optional: real-time 3D)

**Default — pre-rendered image.** The centerpiece is almost always a flat high-quality render moved
with `transform`s, NOT real-time 3D. The scroll-drift + load-float + pointer-parallax code for that
lives in `stack-setup.md` → "The centerpiece object" (Option 1). Use that for this site's look.

**Optional — real-time 3D reaction (R3F).** Only when the object must respond live to the pointer.
Inside the `<Canvas>` from `stack-setup.md`, lerp rotation toward pointer + scroll progress:

```tsx
import { useFrame, useThree } from "@react-three/fiber";
import { useRef } from "react";
import * as THREE from "three";

function Container() {
  const ref = useRef<THREE.Group>(null!);
  const { pointer } = useThree();
  useFrame((_, dt) => {
    // idle spin + pointer parallax
    ref.current.rotation.y += dt * 0.15;
    ref.current.rotation.x = THREE.MathUtils.damp(ref.current.rotation.x, pointer.y * 0.2, 4, dt);
    ref.current.position.y = THREE.MathUtils.damp(ref.current.position.y, pointer.x * 0.1, 4, dt);
  });
  // <primitive> the GLB here, or build the container from boxes
  return <group ref={ref}>{/* ... */}</group>;
}
```

To couple it to page scroll, read Lenis progress into a ref (`lenis.on("scroll", e => progress.current = e.progress)`)
and use it inside `useFrame` to drive rotation/position — keep it `damp`ed so it stays smooth.

---

## 8. Hero with layered occlusion (type framed by, and behind, the centerpiece)

The signature hero composition: two huge display words pinned to opposite diagonal corners
(top-left + bottom-right), and the centerpiece image sits ON TOP, overlapping/occluding the
type. Depth comes from z-index layering, not 3D.

```html
<header class="hero">
  <h1 class="display tl">Precision</h1>
  <img class="centerpiece" src="/container.webp" alt="" />  <!-- z-index ABOVE the type -->
  <h1 class="display br">Delivery</h1>
</header>
```

```css
.hero{position:relative;min-height:100vh;overflow:hidden}
.display{position:absolute;z-index:1;font-size:clamp(4rem,15vw,16rem);line-height:.82}
.tl{top:12vh;left:3vw}.br{bottom:8vh;right:3vw}
.centerpiece{position:absolute;z-index:2;left:50%;top:50%;transform:translate(-50%,-50%);width:min(58vw,820px)}
```

The two words must be large enough that the centerpiece visibly covers part of them — that overlap is
the whole effect. Add the scroll-drift + pointer-parallax from `stack-setup.md` Option 1 to the
centerpiece. Supporting hero elements seen on these sites: a rotating circular "watch showreel" badge
(see pattern 11), a testimonial card with a portrait, and a stat stack (99% / 4.9 / 100+).

## 9. Preloader — column wipe reveal

Full-screen accent panel split into N vertical columns that retract (usually upward) at staggered
times, revealing the site. A centered logo sits on top and fades/scales out.

```html
<div class="preloader">
  <div class="cols"><i></i><i></i><i></i><i></i></div>
  <div class="pl-logo">FLUX. <small>ENHANCED LOGISTICS</small></div>
</div>
```

```css
.preloader{position:fixed;inset:0;z-index:999;pointer-events:none}
.cols{position:absolute;inset:0;display:flex}
.cols i{flex:1;background:var(--accent);transform-origin:top}
.pl-logo{position:absolute;inset:0;display:grid;place-content:center;color:#fff;z-index:1}
```

```js
const tl = gsap.timeline();
tl.to(".pl-logo", { autoAlpha: 0, scale: .9, duration: .5, ease: "power2.in", delay: .8 })
  .to(".cols i", { scaleY: 0, duration: .9, ease: "expo.inOut", stagger: .08 }, "-=.2")
  .set(".preloader", { display: "none" });
// run the hero load reveal AFTER the wipe (chain it or use tl.add at the end)
```

Disable / shorten under reduced-motion (just hide the preloader instantly).

## 10. Sticky panel-cover transition (the orange "About" panel rises over the hero)

The previous section stays pinned while the next, full-bleed accent section scrolls up and covers it.
Cheapest robust version: make the hero `position: sticky; top: 0`, and let the next section sit above
it in the stacking order so it naturally scrolls over.

```css
.hero{position:sticky;top:0;height:100vh}
.about{position:relative;z-index:5;background:var(--accent);color:var(--paper);min-height:100vh}
```

That's it — normal document flow does the covering because `.about` paints after the sticky hero.
For a parallax kick, drift the hero contents slightly as it gets covered:

```js
gsap.to(".hero .display", { yPercent: -12, ease: "none",
  scrollTrigger: { trigger: ".about", start: "top bottom", end: "top top", scrub: 1 } });
```

## 11. Scroll-linked word-by-word opacity reveal (the centered About copy)

Big centered statement where each word goes from faded to solid as you scroll through it.

```js
const split = new SplitType(".about-copy", { types: "words" });
gsap.set(split.words, { opacity: .18 });
gsap.to(split.words, {
  opacity: 1, ease: "none", stagger: 1,
  scrollTrigger: { trigger: ".about-copy", start: "top 75%", end: "bottom 55%", scrub: true },
});
```

## 12. Annotation callouts around the centerpiece (Mission section)

Feature labels that fade/slide in around the object with short leader lines, on enter. Position them
absolutely relative to the centerpiece wrapper; animate `autoAlpha` + a small offset, stagger them.

```html
<div class="annotated">
  <img class="centerpiece" src="/container-orange.webp" alt="" />
  <span class="note n1">Guaranteed Security</span>
  <span class="note n2">On-time Delivery</span>
  <span class="note n3">Real-time Tracking</span>
  <span class="note n4">24/7 Support</span>
</div>
```

```css
.annotated{position:relative}
.note{position:absolute;font-family:ui-monospace,monospace;font-size:.7rem;letter-spacing:.1em;
  padding-left:1.4rem}
.note::before{content:"";position:absolute;left:0;top:50%;width:1rem;height:1px;background:var(--accent)}
.n1{top:18%;left:2%}.n2{top:24%;right:2%}.n3{bottom:30%;left:2%}.n4{bottom:14%;right:14%}
```

```js
gsap.from(".note", {
  autoAlpha: 0, x: (i) => (i % 2 ? 20 : -20), duration: .6, ease: "power3.out", stagger: .12,
  scrollTrigger: { trigger: ".annotated", start: "top 60%" },
});
```

## 13. Angular / brand-shaped clip-path reveal (refines pattern 4)

Same scroll-scrubbed `clip-path` idea, but the resting and final shapes are ANGULAR with a brand
notch (e.g. a zigzag corner), not a plain rectangle — that's what makes it read as "designed."

```css
/* closed: tight slanted hexagon. final: full-bleed but keeps a zigzag notch bottom-right */
.reveal-media{ clip-path: polygon(18% 22%, 82% 14%, 82% 78%, 18% 86%); }
```

```js
gsap.to(".reveal-media", {
  clipPath: "polygon(0% 0%, 100% 0%, 100% 80%, 88% 80%, 88% 100%, 0% 100%)", /* zigzag notch */
  ease: "power3.inOut",
  scrollTrigger: { trigger: ".reveal-media", start: "top 75%", end: "top 25%", scrub: 1 },
});
```

---

## 14. Cursor spotlight color/state reveal (hero — recolor the object under the pointer)

Signature interaction: the object sits in its base color (e.g. white); a second copy in the accent
color is stacked on top, masked to a radial circle that **follows the pointer**. Only the area under
the cursor shows the accent. It reverts as the pointer moves away — purely interactive, non-destructive.

```html
<div class="spotlight">
  <div class="layer base"><!-- white object (img or svg) --></div>
  <div class="layer accent"><!-- same object, accent-colored --></div>
</div>
```

```css
.spotlight{position:relative}
.spotlight .layer{position:absolute;inset:0}
.spotlight .accent{
  -webkit-mask-image:radial-gradient(circle var(--r,0px) at var(--mx,50%) var(--my,50%),#000 62%,transparent 70%);
          mask-image:radial-gradient(circle var(--r,0px) at var(--mx,50%) var(--my,50%),#000 62%,transparent 70%);
}
```

```js
const el = document.querySelector(".spotlight");
const acc = el.querySelector(".accent");
const set = (p,v)=>acc.style.setProperty(p,v);
el.addEventListener("pointermove",(e)=>{ const r=el.getBoundingClientRect();
  // gsap.to for smoothing is nicer than raw set:
  gsap.to(acc,{ "--mx":(e.clientX-r.left)+"px","--my":(e.clientY-r.top)+"px","--r":"140px",duration:.4,ease:"power3.out" });
});
el.addEventListener("pointerleave",()=> gsap.to(acc,{ "--r":"0px",duration:.5,ease:"power3.out" }));
```

Works the same whether the layers are `<img>` renders (white vs accent version) or two SVGs. Disable
under reduced-motion / touch (no hover): just show the base.

## 15. Object-silhouette image mask that grows to fullscreen (pinned)

The object's silhouette becomes the clip mask for an image: the image appears *in the shape of the
object*, centered and modest, then on scroll scales up — the clip morphing toward a full rectangle —
until the image fills the viewport.

```css
.grow{height:100vh;display:grid;place-items:center;overflow:hidden}
.grow-media{width:min(48vw,640px);aspect-ratio:3/2;will-change:transform,clip-path;
  /* container-ish silhouette */
  clip-path:polygon(8% 22%,92% 12%,92% 78%,8% 88%);}
.grow-media img{width:100%;height:100%;object-fit:cover}
```

```js
gsap.fromTo(".grow-media",
  { scale:.6 },
  { scale:2.2, clipPath:"polygon(0% 0%,100% 0%,100% 100%,0% 100%)", ease:"power2.inOut",
    scrollTrigger:{ trigger:".grow", start:"top top", end:"+=140%", pin:true, scrub:1 } });
```

Tune `scale` end so the media covers the viewport at the morph's end. Chain pattern 16 onto the tail of
this pinned scrub so cards appear once the image is full-bleed.

## 16. Messy scattered card stack (piled, off to one side of the image)

Cards heaped toward one edge, overlapping with **random** rotations and offsets — like an untidy hand
of cards spilling past the corner, not a clean stack. Keep each card's random transform; animate them
in with stagger.

```js
const cards = gsap.utils.toArray(".scatter .card");
cards.forEach((c,i)=>{
  gsap.set(c,{ rotation:gsap.utils.random(-16,16), x:gsap.utils.random(-40,40),
               y:i*-16+gsap.utils.random(-12,12), zIndex:i });
});
gsap.from(cards,{ autoAlpha:0, y:140, rotation:0, duration:.7, ease:"power3.out", stagger:.12,
  scrollTrigger:{ trigger:".scatter", start:"top 65%" } });
```

Position the `.scatter` wrapper absolutely over one side of the image (e.g. `right:6%;bottom:8%`) so the
pile is excentred and a few corners overflow the frame.

## 17. Footer built from the object's shapes

The object (or its brand mark) becomes the footer's structural backdrop: oversized, low-contrast,
bleeding off-canvas, with the wordmark / nav composed over its forms. Treat the object as decor, not a
hero — derive the footer's geometry from it (the zigzag mark as a giant background cut, the container
as a band).

```css
footer{position:relative;overflow:hidden;background:var(--ink);color:var(--paper)}
footer .object-bg{position:absolute;right:-8%;bottom:-12%;width:70%;opacity:.10;pointer-events:none}
footer .wordmark{position:relative;z-index:1;font-family:var(--display-font);font-size:clamp(5rem,22vw,20rem)}
```

```js
gsap.to("footer .object-bg",{ yPercent:-12, ease:"none",
  scrollTrigger:{ trigger:"footer", start:"top bottom", end:"bottom bottom", scrub:1 } });
```

---

## 18. Persistent choreographed object (ONE fixed object across the whole page)

The most important structural insight: the centerpiece is **a single element**, `position: fixed`,
that stays on screen and is animated through every section by scroll — NOT a separate copy per
section. It travels the whole page (recoloring, scaling, gaining annotations, becoming an image mask)
and only disappears (fades to transparent) near the bottom.

Architecture:
- One fixed `.stage` holds the object; give it a z-index *between* the section text and the opaque
  panels. Sections that should REVEAL it are transparent; sections that should HIDE it (the accent
  About panel, the footer) have solid backgrounds and a higher z-index so they cover the fixed object
  as they scroll past.
- Drive the object with per-section ScrollTriggers (scrub) targeting that one fixed element. Chain
  their from/to values so scale/colour are continuous across the boundaries (e.g. mission `scale 1→1.06`,
  grow `scale 1.06→2.8`).

```css
.stage{position:fixed;inset:0;z-index:3;display:grid;place-items:center;pointer-events:none}
.obj{pointer-events:auto;will-change:transform}      /* the single persistent object */
.hero-words{z-index:2}                                 /* behind the object → occlusion */
.about,.services,footer{position:relative;z-index:5}   /* solid bg → cover the fixed object */
.hero,.mission,.grow{background:transparent}           /* let the fixed object show through */
```

```js
// recolor white→accent as the About panel covers it
gsap.to(".obj .accent", { "--r":"1200px", ease:"none",
  scrollTrigger:{ trigger:".about", start:"top 80%", end:"top top", scrub:1 } });
// slight zoom + annotations during mission
gsap.timeline({ scrollTrigger:{ trigger:".mission", start:"top center", end:"bottom top", scrub:1 } })
  .fromTo(".obj", { scale:1 }, { scale:1.06, ease:"none" }, 0)
  .fromTo(".note", { autoAlpha:0 }, { autoAlpha:1 }, 0).to(".note", { autoAlpha:0 }, .8);
// becomes an image mask, grows to fullscreen, then the whole stage fades (transparent toward bottom)
gsap.timeline({ scrollTrigger:{ trigger:".grow", start:"top bottom", end:"bottom bottom", scrub:1 } })
  .to(".obj .svg-layers", { autoAlpha:0 }, 0).to(".obj .photo", { autoAlpha:1 }, 0)
  .fromTo(".obj", { scale:1.06 }, { scale:2.8, ease:"power2.inOut" }, 0)
  .to(".obj .photo", { clipPath:"polygon(0 0,100% 0,100% 100%,0 100%)" }, 0)
  .to(".stage", { autoAlpha:0 }, .85);
```

This single-object model is what makes the whole page feel like one continuous piece rather than a
stack of unrelated sections. Build the fixed object first, then layer the sections around it.

---

## Easing cheat-sheet

- Entrances: `expo.out`, `power4.out`.
- Scrub set-pieces: `power2.inOut` / `power3.inOut`.
- Snappy premium: `cubic-bezier(0.16, 1, 0.3, 1)` (CSS) ≈ `expo.out`.
- Bounce-back on magnetic release: `elastic.out(1, 0.4)`.
- Never `linear` except continuous marquees.

## Reduced motion

Guard everything: `if (matchMedia("(prefers-reduced-motion: reduce)").matches) return;` before
building tweens; render final states statically and freeze the 3D to a poster.