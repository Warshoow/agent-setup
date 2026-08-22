#!/usr/bin/env bash
# Extract frames from a flythrough video and encode them for scroll-scrubbing.
#
# Usage:
#   ./extract-frames.sh input.mp4 [fps] [width]
#   ./extract-frames.sh flythrough.mp4 30 1920
#
# Output: public/frames/frame_0001.avif … (or .webp fallback)
# Prints the FRAME_COUNT to paste into chapters.ts.
#
# Requires: ffmpeg. Optional: avifenc (libavif) for best compression,
# else falls back to cwebp, else keeps PNG.

set -euo pipefail

IN="${1:?Usage: ./extract-frames.sh input.mp4 [fps] [width]}"
FPS="${2:-30}"
WIDTH="${3:-1920}"
OUT="public/frames"

mkdir -p "$OUT"
rm -f "$OUT"/frame_*.png "$OUT"/frame_*.avif "$OUT"/frame_*.webp 2>/dev/null || true

echo "→ Extracting frames at ${FPS}fps, width ${WIDTH}px …"
ffmpeg -loglevel error -i "$IN" \
  -vf "fps=${FPS},scale=${WIDTH}:-2:flags=lanczos" \
  "$OUT/frame_%04d.png"

# Keep a poster for the reduced-motion fallback.
cp "$OUT/frame_0001.png" "$OUT/poster.png" 2>/dev/null || true

EXT="png"
if command -v avifenc >/dev/null 2>&1; then
  echo "→ Encoding AVIF (avifenc) …"
  for f in "$OUT"/frame_*.png "$OUT"/poster.png; do
    [ -e "$f" ] || continue
    avifenc --min 20 --max 30 -s 6 "$f" "${f%.png}.avif" >/dev/null 2>&1
    rm "$f"
  done
  EXT="avif"
elif command -v cwebp >/dev/null 2>&1; then
  echo "→ avifenc not found; encoding WebP (cwebp) …"
  echo "  NOTE: change the extension in chapters.ts frameSrc() to .webp"
  for f in "$OUT"/frame_*.png "$OUT"/poster.png; do
    [ -e "$f" ] || continue
    cwebp -quiet -q 80 "$f" -o "${f%.png}.webp"
    rm "$f"
  done
  EXT="webp"
else
  echo "→ No AVIF/WebP encoder found; keeping PNG (large)."
  echo "  Install libavif or webp tools, or re-run. Update chapters.ts to .png."
fi

COUNT=$(ls "$OUT"/frame_*."$EXT" 2>/dev/null | wc -l | tr -d ' ')
echo ""
echo "✓ Done. $COUNT frames in $OUT (.$EXT)"
echo "  → Set  FRAME_COUNT = $COUNT  in chapters.ts"
[ "$EXT" != "avif" ] && echo "  → Set the extension in frameSrc() to .$EXT"
