# Footage pipeline — getting the flythrough

The web build is the easy half. The footage is where the look is won or lost. You need **one continuous camera move** through the scene (a dolly/orbit, no cuts), 6–12s, that reads well played forward *and* backward (scroll goes both ways).

## Option A — AI video generation (fastest, no 3D skills, the "with AI" angle)

Tools: Kling, Runway Gen-4, Google Veo, Sora, Hailuo/MiniMax, Luma.

Prompting principles for a usable scrub clip:
- **One slow, continuous camera move.** Ask explicitly for a single uninterrupted dolly or push-in: "slow continuous forward dolly through a minimalist concrete-and-timber house, no cuts, locked cinematic move, steady speed." Cuts and rapid action scrub badly.
- **Steady speed, no people, no fast motion.** Moving subjects look broken when scrubbed backward. Keep it architectural and still.
- **Loop-friendly framing** if you want seamless reverse.
- Generate several takes; pick the one with the most even motion. Expect to stitch/trim in any editor (or `ffmpeg`) to get a clean in/out.
- Upscale if needed before frame extraction so 1920px frames stay sharp.

Limitation: you don't fully control the exact camera path. For a precise "enter through this door, turn here" sequence, use Blender.

## Option B — Blender (full control, highest quality)

1. Model or import the scene (or buy a `.blend` / `.glb` archviz asset).
2. Add a camera, animate it along a path: add a Bézier/NURBS path, give the camera a **Follow Path** constraint, keyframe the path's *Evaluation Time* for the move. Ease in/out for a cinematic feel.
3. Lighting: an HDRI plus a few area lights gets you the soft archviz look. Use Cycles for photoreal, Eevee for speed.
4. Render an **image sequence** (PNG) directly — you can skip video entirely and feed these straight into the encode step. Match the frame count you want on the web (e.g. 180 frames = 6s at 30fps).
5. Keep resolution at your target web width (1920 wide is plenty; 1280 for a lighter mobile set).

## Option C — Spline (real-time-ish, lighter, in-browser editor)

Spline lets you build a 3D scene in a visual editor and either export a web runtime or render a camera animation. Good middle ground if you want some real-time interactivity without writing R3F. Heavier on the client than frame-scrub; lighter to author than Blender.

## The encode step (all options converge here)

Use `scripts/extract-frames.sh`:

```bash
./scripts/extract-frames.sh flythrough.mp4 30 1920
```

It extracts frames and encodes **AVIF** (best size/quality), with WebP fallback. It prints the `FRAME_COUNT` for `chapters.ts`.

If you rendered an image sequence from Blender, you can skip extraction and just encode:

```bash
# place rendered PNGs in public/frames as frame_0001.png …, then:
for f in public/frames/frame_*.png; do avifenc --min 20 --max 30 -s 6 "$f" "${f%.png}.avif" && rm "$f"; done
```

### Budget sanity check

Frame sequences ARE the payload. A 180-frame set at ~250KB/frame ≈ 45MB — fine over good connections with a preloader, heavy on mobile. Levers:
- Fewer frames (24fps, or drop 1 in 2 — scrubbing tolerates lower frame counts well).
- Lower width for a mobile set (serve via `frameSrc` switching on viewport).
- Tighter AVIF quality (`--max 35`).

## Fallback: video `currentTime` scrubbing (bandwidth-critical)

Instead of frames, scrub the video itself. Lighter payload, but seeking is janky unless the video is encoded with **every frame a keyframe** (GOP=1):

```bash
ffmpeg -i flythrough.mp4 -vf "fps=30,scale=1920:-2" \
  -c:v libx264 -x264opts keyint=1 -preset slow -crf 20 -an \
  -movflags +faststart public/scrub.mp4
```

Then, instead of preloading images, set `video.currentTime = progress * video.duration` inside the Lenis rAF loop. iOS requires the `<video>` to be `muted`, `playsInline`, and "woken" with a `play()` then immediate `pause()` on first user interaction, or seeking is ignored. Frame-scrub avoids all of this — prefer it unless payload is the hard constraint.
