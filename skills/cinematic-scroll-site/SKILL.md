---
name: cinematic-scroll-site
description: Build scroll-driven cinematic websites where scrolling scrubs through a pre-rendered camera flythrough (the technique behind Apple product pages and "architectural studio" sites — a moving camera through a 3D house/scene with text that fades in at scroll milestones). Use this skill whenever the user wants a "scroll cinematic", "scrollytelling", "scroll-scrub", "camera moves on scroll", "Apple-style scroll", "immersive landing page", "3D-looking website" driven by scroll, or shows a reel/video of a website where scrolling moves through a scene. Trigger even if the user only describes the effect ("the site goes inside the house as you scroll") without naming the technique. NOT for ordinary parallax or for genuinely interactive real-time 3D (see the R3F variant note for that).
---

# Cinematic Scroll Site

Build the "luxury scroll cinematic": as the user scrolls, a pre-rendered camera flythrough plays forward/backward, and editorial typography fades in at scroll milestones. Stack: **Next.js (App Router) + Lenis (smooth scroll) + `<canvas>` frame-scrub + Tailwind**.

## The one thing to understand first

These sites are **almost never real-time 3D**. They are a single pre-rendered video (Blender render or AI-generated flythrough) that is *scrubbed* by scroll position. The "camera moving through the house" is just the video advancing. This is why they look photoreal and run smoothly on a phone — the GPU isn't computing 3D, it's drawing one image per frame.

So the work splits cleanly:
- **Footage** = the asset the user supplies or generates (the hard/creative part). See `references/footage-pipeline.md`.
- **The web build** = a known, repeatable pattern (this skill).

Do not reach for Three.js / React Three Fiber unless the user explicitly needs *interactive* real-time 3D (clicking objects, free-orbit camera, live state). For a fixed cinematic path, frame-scrub is smoother, lighter, more photoreal, and far less code. The R3F variant is noted at the end for the rare case it's warranted.

## Choose the scrub technique

Two ways to scrub. Default to **canvas frame-sequence** — it is what makes these sites buttery.

| | Canvas frame-sequence (default) | Video `currentTime` |
|---|---|---|
| Smoothness | Excellent (no seek jank) | Janky unless GOP=1 encoding |
| Payload | Heavier (N images) | Lighter (one video) |
| iOS Safari | Reliable | Needs `muted` + `playsinline` + wake hack |
| Best for | Hero flythroughs ≤ ~12s | Long sequences, bandwidth-critical |

Use frame-sequence for the hero unless the user flags strict bandwidth limits. If they do, read the video-scrub fallback in `references/footage-pipeline.md`.

## Build steps

Work in this order. The footage can be a placeholder while you build the mechanics.

1. **Scaffold** a Next.js App Router + Tailwind project. Install `lenis`. (`gsap` only if the user wants complex multi-track timelines — the reference works without it.)
2. **Prepare frames.** Run `scripts/extract-frames.sh <video.mp4>` to produce `public/frames/frame_0001.avif …`. It prints the frame count.
3. **Wire the config.** Copy `assets/chapters.ts`. Set `FRAME_COUNT` to the printed number. Define `CHAPTERS` — each chapter is a scroll range `[start,end]` (0→1) with an eyebrow, title, and technical `meta` labels. The reel's own labels (`FALL LINE HOUSE` / `CANTILEVER 18.4M`, `THRESHOLD / WATER SIDE`, `TIMBER CORE`) are pre-filled as a working example; replace with the user's content.
4. **Drop in the scrubber.** Copy `assets/ScrollScrubScene.tsx`. It preloads frames, runs Lenis, maps scroll progress to a frame, draws to a `<canvas>`, and renders the chapter overlays. Render it as the page (it owns the tall scroll container).
5. **Style the overlays** per `references/design-language.md` — thin uppercase display type, monospace technical annotations, heavy negative space. This editorial layer is what sells the "studio" feel as much as the footage.
6. **Add the loading gate.** Show a minimal preloader with the load percentage until frames are ready (the component exposes it). A flythrough that stutters because frames aren't decoded ruins the effect.

## Performance & accessibility — non-negotiable for this effect

- **Encode to AVIF** (WebP fallback). Frame sequences are the whole payload; a poorly encoded set is multiple hundred MB and will not load on mobile. Target a few hundred KB per frame max, fewer frames (24–30fps source → keep 1 in 2 if needed).
- **Cover-fit the draw** so it fills any viewport without distortion (the reference does this).
- **`prefers-reduced-motion`**: fall back to a single hero still + normal native scroll with the text laid out as stacked sections. The reference includes this branch — keep it.
- **Mobile**: ship a smaller-width frame set, or fall back to the video-scrub approach, or to the reduced-motion layout. Don't push a 1920px frame set to phones.
- **Preload strategy**: decode frames before enabling scroll; never seek to an undecoded frame.

## Reference files

- `references/footage-pipeline.md` — how to *get* the flythrough: AI video gen prompting, Blender camera-path rendering, Spline, the `ffmpeg`/AVIF pipeline, and the video-`currentTime` fallback implementation.
- `references/design-language.md` — the editorial-architectural aesthetic: type, annotation system, layout, color, motion of the text layer.
- `assets/ScrollScrubScene.tsx` — the canvas frame-scrub component (Lenis + cover-fit draw + overlays + reduced-motion + preloader).
- `assets/chapters.ts` — frame count + chapter/overlay choreography config and opacity curve.
- `scripts/extract-frames.sh` — `ffmpeg` frame extraction + AVIF/WebP encoding; prints `FRAME_COUNT`.

## The real-time 3D variant (only if interactivity is required)

If the user genuinely needs interactive 3D (orbit, hover/click objects, live data in the scene), use **React Three Fiber** + `@react-three/drei` (`ScrollControls`, `useScroll`) and animate the camera along a `CatmullRomCurve3` path driven by scroll offset, importing a `.glb` scene. This is much heavier (asset budget, draw calls, lighting bake) and rarely matches the photorealism of a Blender/AI render. Reach for it only when the fixed-path frame-scrub can't express the requirement.
