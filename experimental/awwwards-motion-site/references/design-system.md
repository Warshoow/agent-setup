# Design System — the "look"

Read this first, every build. This is what separates the result from generic AI output.

## Palette (one accent, ruthlessly)

```css
:root {
  --paper: #F4F1EC;   /* warm off-white base — NOT pure #fff */
  --ink:   #0A0A0A;   /* near-black for type */
  --accent:#FF3D00;   /* the single saturated accent (orange-red here) */
  --paper-pure: #ffffff; /* sparingly, for cards/containers that must pop off paper */
  --line:  rgba(10,10,10,0.12); /* hairline dividers */
}
```

Rules:
- Exactly **one** accent. Use it for: CTAs, the 3D object's branding, oversized numbers, a full-bleed
  section background, hover states. Never introduce a second hue.
- The base is a *warm* neutral, not stark white — it reads premium and editorial.
- Big accent moments (a whole orange section) work *because* the rest is restrained.
- Want a different identity? Swap `--accent` only (electric blue `#1A39FF`, acid green `#C6FF00`,
  vermillion `#FF3D00`). Keep paper+ink. The system holds.

## Typography (the hero)

Pick a tight grotesque. Good choices:
- Paid: PP Neue Montreal, TWK Everett, Söhne, Neue Haas Grotesk, Helvetica Now Display.
- Free (load via Fontshare/local): **General Sans**, **Geist**, **Clash Grotesk** (more characterful),
  Space Grotesk only if nothing else (overused — avoid converging on it).
- A mono for labels/tags: Geist Mono, JetBrains Mono, or the grotesque in uppercase + tracking.

Type ramp (display-dominant):

```css
:root {
  --step--1: clamp(0.83rem, 0.78rem + 0.2vw, 0.94rem); /* small label / mono */
  --step-0:  clamp(1rem, 0.95rem + 0.3vw, 1.18rem);    /* body */
  --step-3:  clamp(2.2rem, 1.6rem + 3vw, 4rem);         /* section heading */
  --display: clamp(4rem, 8vw + 1rem, 14rem);           /* hero words */
}

.display {
  font-size: var(--display);
  line-height: 0.88;
  letter-spacing: -0.03em;   /* tight tracking is essential */
  font-weight: 600;
  text-wrap: balance;
}
.label {                      /* editorial mono accents: "01  MISSION", "FEATURED PROJECTS" */
  font-size: var(--step--1);
  text-transform: uppercase;
  letter-spacing: 0.18em;
}
```

Layout moves with type:
- Hero words **bleed off the canvas edges** (negative margins / `overflow: hidden` on the section).
- **Layered hero (signature):** pin two giant display words to opposite diagonal corners (top-left +
  bottom-right) and place the centerpiece image ON TOP so it overlaps/occludes them. The overlap is
  the effect — depth from z-index, not 3D. (Code: `motion-patterns.md` #8.)
- **Full-bleed accent panels:** entire sections in the accent color with large CENTERED display copy
  that reveals word-by-word on scroll; these often scroll up to *cover* the previous section (sticky
  stacking). (#10, #11.)
- **Annotation callouts:** in product/mission sections, label the centerpiece with mono micro-labels
  on short leader lines that animate in (Guaranteed Security, On-time Delivery…). (#12.)
- A rotating circular badge ("watch showreel") and a small testimonial card with a portrait are common
  supporting hero elements.
- Oversized **numbers** (01 / 02 / 03 / 04) as structural anchors in lists and stacks.
- Pair a giant black word with a smaller-but-still-large word in another position (e.g. "Precision"
  top-left, "Delivery" bottom-right with the 3D object between them) — diagonal reading flow.

## Layout & composition

- 12-col mental grid, but **break it on purpose**: overlap the centerpiece across columns, push labels
  to the far margins, let a heading run wider than its container.
- **Asymmetry over centering.** Centered everything = template energy.
- Generous negative space in editorial sections; controlled density in data sections (stats, tags).
- Pill/tag clusters (rounded, hairline border, mono text) scattered as texture — see image refs:
  "LOGISTICS SOLUTION", "ADVANCED TRACKING".
- Sticky/oversized footer with the brand name set as the largest type on the page.

## Motion principles

- **Smooth scroll (Lenis) is the floor**, not a feature.
- One orchestrated **load reveal**: staggered lines of the hero heading + the 3D object easing in.
- A few **scroll set-pieces**, each with a clear job (see `motion-patterns.md`):
  marquee → pinned card stack → clip-path photo reveal → cursor-preview services list.
- Easing: never linear. Defaults — `expo.out` / `power4.out` for entrances,
  `power2.inOut` for state changes, custom `cubic-bezier(0.16, 1, 0.3, 1)` for "premium" snaps.
- Durations: entrances 0.8–1.2s, micro-states 0.3–0.5s. Stagger 0.04–0.08s between siblings.
- Hover: scale 1.02–1.04, accent fill sweeps, magnetic buttons (pointer-follow with lerp).

## Imagery & 3D

- Photography is high-contrast, real-world, slightly cinematic (the worker on the loading dock).
  Treat it inside **clipped polygon/parallelogram masks**, never plain rectangles.
- The 3D centerpiece: clean geometry, studio lighting, the brand mark mapped onto it, one slow
  idle rotation + pointer parallax. A hanging rig (hook + cables) sells the "logistics" story —
  but the pattern generalizes to any floating product.

## Accessibility / restraint

- Maintain contrast: ink-on-paper and paper-on-accent both pass. Don't put accent text on paper at
  small sizes (low contrast).
- `prefers-reduced-motion`: kill Lenis + scroll tweens, show final states, freeze 3D to a poster.
- Keep real semantic HTML under the spectacle — headings, landmarks, focus states.