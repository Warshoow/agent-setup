# Design language — the "architectural studio" editorial layer

The footage carries the photorealism; the *typography* carries the credibility. The look in these reels is a specific genre: technical/architectural editorial. Get this layer right and even mediocre footage reads as premium.

## Type

- **Display:** a thin/light weight, **uppercase**, tight tracking, large (`text-6xl`–`text-8xl`). Think drawing-sheet titles, not marketing headlines. A light grotesque (Neue Haas, Helvetica Now Light, Suisse Int'l) or a high-contrast light serif both work. Keep weight low — heaviness kills the look.
- **Annotations / meta:** **monospace**, tiny (`text-[10px]`–`text-xs`), wide letter-spacing (`tracking-[0.2em]`–`[0.3em]`), muted color. These are the `CANTILEVER 18.4M`, `FIN-03 / LOAD TRANSFER` labels — they imitate construction-drawing callouts and do most of the "studio" work.
- Pair exactly two faces (one display, one mono). No more.

## The annotation system (the signature move)

Treat text like a technical drawing, not a webpage:
- Prefix meta lines with `—` or `/` or coordinate-like codes (`01`, `FIN-03`, `SIDE CONTEXT`).
- Use slashes as separators: `THRESHOLD / WATER SIDE`, `GLASS EDGE / WATER SIDE`.
- Scatter small corner labels (top-right sheet number, bottom-left index) that stay fixed while the cinematic moves — sells the "live document" feel.
- Numbers with units (`18.4M`, `420MM`, `312`) read as engineering, not copywriting.

## Layout

- Heavy **negative space** — text occupies one corner/edge, the image breathes.
- Left-aligned, vertically centered is the default; reserve centered for a single title beat.
- Constrain title width (`max-w-[14ch]`) so long titles wrap like a stacked sheet header.
- A thin scroll-progress hairline along an edge reinforces the "instrument" aesthetic.

## Color

- Near-black background (`#0a0a0a`), off-white text. Avoid pure `#000`/`#fff`.
- Let the footage supply all the warmth (timber glow, daylight). UI stays neutral/monochrome.
- One restrained accent at most (a warm hairline), never a saturated brand color.

## Motion of the text layer

- **Fade only**, or fade + a few-pixel rise. No bounce, no slide-from-side, no spring. Restraint = luxury.
- Triangular opacity per chapter (see `chapterOpacity`): enter, hold, leave — synced to scroll, not to time.
- Optional: a 1–2px blur-to-sharp on entry for the cinematic feel.
- The cinematic does the dramatic movement; the text must stay calm or the composition fights itself.

## Anti-patterns

- Bold/heavy display weights. Drop shadows beyond a faint one for legibility. Rounded corners. Gradients on text. Multiple accent colors. Slide/zoom text transitions. Emoji. Any of these breaks the genre instantly.
