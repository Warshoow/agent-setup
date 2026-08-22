// chapters.ts — scrub config + overlay choreography
// Edit FRAME_COUNT to match what extract-frames.sh printed.

export const FRAME_COUNT = 180; // number of files in /public/frames

// Frames are named frame_0001.avif … frame_NNNN.avif (1-indexed).
// If extract-frames.sh fell back to WebP, change the extension here.
export function frameSrc(i: number): string {
  const n = String(i + 1).padStart(4, "0");
  return `/frames/frame_${n}.avif`;
}

export type Chapter = {
  id: string;
  start: number; // global scroll progress (0..1) where the overlay starts entering
  end: number; // where it starts leaving
  eyebrow?: string; // small line above the title
  title: string; // large display line
  meta?: string[]; // technical annotation labels (rendered monospace)
  align?: "left" | "center";
};

// Pre-filled with the reel's own copy as a working template — replace freely.
export const CHAPTERS: Chapter[] = [
  {
    id: "fall-line",
    start: 0.0,
    end: 0.22,
    eyebrow: "FRONT ELEVATION",
    title: "FALL LINE HOUSE",
    meta: ["CANTILEVER 18.4M", "FIN-03 / LOAD TRANSFER", "WATERFALL EDGE / ALPINE BASIN"],
    align: "left",
  },
  {
    id: "threshold",
    start: 0.26,
    end: 0.48,
    eyebrow: "THE HOUSE OPENS WHERE THE CLIFF FALLS AWAY",
    title: "THRESHOLD / WATER SIDE",
    meta: ["GLASS EDGE / WATER SIDE", "TIMBER CORE 312", "FIN-03 VISIBLE AXIS"],
    align: "left",
  },
  {
    id: "timber",
    start: 0.52,
    end: 0.74,
    eyebrow: "INTERIOR MASS",
    title: "TIMBER CORE",
    meta: ["A WARM LINE HELD INSIDE CONCRETE", "CONCRETE SHELL 420MM", "HEATED TIMBER WALL"],
    align: "left",
  },
  {
    id: "interior",
    start: 0.78,
    end: 1.0,
    eyebrow: "VISIBLE AXIS",
    title: "ENTER INTERIOR STUDY",
    meta: ["FLOOR PLATE / BLACK STONE", "OPEN TERRAIN STUDY"],
    align: "left",
  },
];

// Opacity for one chapter given the global scroll progress.
// Triangular fade with a short ramp at each edge.
export function chapterOpacity(c: Chapter, p: number, fade = 0.05): number {
  if (p < c.start - fade || p > c.end + fade) return 0;
  if (p < c.start) return (p - (c.start - fade)) / fade; // entering
  if (p > c.end) return 1 - (p - c.end) / fade; // leaving
  return 1; // fully visible
}

export const clamp = (v: number, min: number, max: number) =>
  Math.max(min, Math.min(max, v));
