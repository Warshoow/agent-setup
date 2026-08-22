---
name: awwwards-motion-site
description: >-
  Build bold, editorial, award-winning ("Awwwards-style") marketing/landing sites with a single
  vivid accent color, oversized grotesque typography, scroll-driven motion (smooth scroll + pinned
  sections + clip-path reveals + marquees) and a 3D centerpiece object. Use this skill WHENEVER the
  user wants to recreate a high-end agency/studio/concept website, a "designer reel" look, a logistics
  or product landing page with hanging/floating 3D objects, scroll animations, big type, or asks to
  reproduce a slick site they saw on Instagram/Awwwards/Dribbble — even if they don't name the
  technique. Covers the full stack (Next.js or plain HTML + Lenis + GSAP ScrollTrigger + R3F/Spline)
  and the design system needed to avoid generic AI aesthetics.
---

# Awwwards-style Motion Site

Recreate the bold, editorial, scroll-driven aesthetic of high-end agency/concept sites: a single
saturated accent on a neutral paper/ink base, oversized tight grotesque type that bleeds off the
canvas, a 3D object as the hero centerpiece, and meticulously timed scroll motion (smooth scroll,
pinned card stacks, clip-path photo reveals, velocity-skewed marquees, cursor-following previews).

This is a **design + engineering** skill. The look fails if you treat it as "a few animations on a
normal page." The motion, the type scale, and the restraint of the palette ARE the design. Commit
fully or it reads as generic.

## When this applies

Trigger for requests like: "recreate this site," "make an Awwwards-style landing," "agency/studio
homepage," "logistics/shipping site with 3D containers," "scroll animations like [reel]," "big bold
type + smooth scroll," "hero with a floating 3D product."

## Decide the stack first (1 question max)

Pick based on what the user already has — don't over-ask:

- **React / Next.js project** → Lenis + GSAP ScrollTrigger + SplitType.
- **Plain HTML/CSS/JS or unknown** → single-file HTML + Lenis + GSAP from CDN (no build step, easiest to hand back).
- **The centerpiece object** (the hanging container / floating product): default to a **pre-rendered
  image**, NOT real-time 3D. Most of these "3D-looking" sites are not WebGL — they animate a high-quality
  render (a transparent PNG made in Blender, or a stock/AI render) with CSS/GSAP transforms. The depth
  comes from the render's lighting, not from geometry in the browser. Only reach for real-time
  Spline/R3F when the object must respond to the pointer or be configurable. See
  `references/stack-setup.md` → "The centerpiece object" for the three approaches in order.

Then read the references as needed (don't load all upfront):

- `references/design-system.md` — palette, type ramp, spacing, layout rules, the "look." **Read this first, every time** — it's what stops the output looking generic.
- `references/stack-setup.md` — install + wire Lenis ↔ GSAP, project skeleton, Spline vs R3F setup.
- `references/motion-patterns.md` — copy-adaptable code for each signature effect (text reveal, marquee, pinned card stack, clip-path reveal, cursor preview list, hanging 3D object).

## Non-negotiable design rules (summary — full detail in design-system.md)

1. **One accent, ruthlessly.** A single saturated color (e.g. `#FF3D00`) on paper (`#F4F1EC`) and ink
   (`#0A0A0A`). No second accent. No gradients-on-white AI cliché.
2. **Type is the hero.** A tight grotesque (PP Neue Montreal, TWK Everett, Söhne; free: General Sans,
   Geist). Display sizes are *huge* (`clamp(4rem, 12vw, 14rem)`), tracking negative
   (`letter-spacing: -0.03em`), line-height ~0.9. Let words bleed past the viewport edge.
3. **A centerpiece object**, not decoration. ONE memorable object (the hanging container, a floating
   product) that **persists across the whole page** — a single `position: fixed` element choreographed
   by scroll (recolor, scale, annotate, become an image mask), NOT a separate copy per section. It only
   fades out near the bottom. Almost always a **pre-rendered image**, not real-time 3D. See #18.
4. **Smooth scroll is mandatory.** Lenis. The whole feel collapses without it.
5. **Motion = a few big orchestrated moments**, not scattered micro-interactions. Hero reveal →
   pinned stack → clip-path reveal → marquee. Each one deliberate, with custom easing
   (`expo.out`, `power4.out`, or a custom cubic-bezier), never linear.
6. **Asymmetry & grid-breaking.** Overlap layers, diagonal flow, oversized numbers (01/02/03),
   labels in mono/uppercase with letter-spacing as editorial accents.

## Build order

1. Set up the stack + Lenis/GSAP bridge (`stack-setup.md`).
2. Lock the design tokens (CSS variables from `design-system.md`) and load the font BEFORE building
   sections — the type scale drives every layout decision.
3. Build the **single persistent fixed object** FIRST (#18) — it lives in its own fixed stage and is
   choreographed across every section. Then build sections around it: hero with **layered occlusion**
   (huge display words pinned to opposite diagonal corners, the object on top overlapping them) +
   supporting elements (rotating showreel badge, testimonial card, stat stack) + a load reveal (#8).
4. Add scroll sections one at a time, testing scroll feel after each. The full observed sequence on
   these sites:
   1. **Preloader** — accent columns that slide up off-screen to reveal the site (#9).
   2. **Hero** — moderate-sized centered object (big but still readable) + two display words placed
      offset/diagonal; an **interactive cursor spotlight that recolors the object** under the pointer
      (base white → accent), non-destructive (#14).
   3. **Accent panel covers the hero** (#10) with large-but-coherent CTA copy + button; the object's
      resting color flips from white to accent across this moment.
   4. **Clean section** — just the object, a slight zoom-in, with **annotation callouts** on leader
      lines (#12).
   5. **Pinned grow** — the object's silhouette **masks an image**; on scroll the shaped image scales
      up to fullscreen (#15), then **messy scattered cards** pile onto one side of it (#16).
   6. **Services "lines"** — a list of rows with a **cursor-following image preview** on hover (#5).
   7. **Footer built from the object** — the object as oversized low-contrast decor, its forms
      structuring the footer (#17).
   A velocity marquee (#2), neat pinned card stack (#3), and word-by-word reveal (#11) are optional
   extras — add only if the brief calls for them.
5. Pass on easing/timing and responsiveness last (collapse the giant type gracefully, swap pin/cover
   sections for simpler reveals on mobile, lazy-load / static-poster the centerpiece on small screens).

## Quality bar

- No `Inter`/`Roboto`/`Arial`/system-font display type. No purple-on-white. No evenly distributed
  rainbow palette. No linear easings. No default browser scroll.
- Every animation has an intentional easing curve and a reason to exist.
- The centerpiece must not jank: if it's a pre-rendered image, optimize it (WebP/AVIF, sized right) and
  animate only `transform`/`opacity`. If it's real-time 3D, clamp DPR, lazy-init, and provide a static
  fallback.
- Respect `prefers-reduced-motion`: disable Lenis + heavy scroll tweens, keep content readable.

## Common pitfalls

- Forgetting to drive GSAP's ticker from Lenis's `raf` → ScrollTrigger fights the smooth scroll and
  positions go wrong. See the bridge in `stack-setup.md`.
- Type too small. If it looks "reasonable," it's too small — push display sizes harder.
- Too many colors creep in. Audit: paper, ink, accent. That's it (plus pure white/black sparingly).
- Reaching for WebGL/Spline/R3F when a pre-rendered image + transforms would look identical and run
  far lighter. Most "3D" agency sites are pre-rendered. Use real-time 3D only for pointer interaction.
- 3D over-modeled (when you DO go real-time). A clean low-poly object with good lighting and one slow
  rotation beats a heavy scene.