"use client";

import { useEffect, useRef, useState, useCallback } from "react";
import Lenis from "lenis";
import {
  CHAPTERS,
  FRAME_COUNT,
  frameSrc,
  chapterOpacity,
  clamp,
} from "./chapters";

// How many viewport-heights the cinematic occupies. More = slower, more
// frames between text beats. ~4–6 feels cinematic; tune to taste.
const SCROLL_VH = 5;

export default function ScrollScrubScene() {
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const wrapRef = useRef<HTMLDivElement>(null);
  const framesRef = useRef<HTMLImageElement[]>([]);
  const progressRef = useRef(0);
  const [loaded, setLoaded] = useState(0);
  const [ready, setReady] = useState(false);
  const [progress, setProgress] = useState(0); // throttled, drives overlays
  const [reduced, setReduced] = useState(false);

  // Respect prefers-reduced-motion.
  useEffect(() => {
    const mq = window.matchMedia("(prefers-reduced-motion: reduce)");
    setReduced(mq.matches);
    const on = () => setReduced(mq.matches);
    mq.addEventListener("change", on);
    return () => mq.removeEventListener("change", on);
  }, []);

  // Preload every frame before enabling scroll. Seeking to an undecoded
  // frame is what causes stutter, so we gate on full decode.
  useEffect(() => {
    if (reduced) return;
    let cancelled = false;
    let count = 0;
    const imgs: HTMLImageElement[] = new Array(FRAME_COUNT);
    for (let i = 0; i < FRAME_COUNT; i++) {
      const img = new Image();
      img.decoding = "async";
      img.src = frameSrc(i);
      const done = () => {
        if (cancelled) return;
        count += 1;
        setLoaded(count);
        if (count === FRAME_COUNT) setReady(true);
      };
      img.onload = done;
      img.onerror = done;
      imgs[i] = img;
    }
    framesRef.current = imgs;
    return () => {
      cancelled = true;
    };
  }, [reduced]);

  // Cover-fit draw of one frame to the full canvas.
  const draw = useCallback((index: number) => {
    const canvas = canvasRef.current;
    const img = framesRef.current[index];
    if (!canvas || !img || !img.complete || img.naturalWidth === 0) return;
    const ctx = canvas.getContext("2d");
    if (!ctx) return;
    const dpr = Math.min(window.devicePixelRatio || 1, 2);
    const w = window.innerWidth;
    const h = window.innerHeight;
    if (canvas.width !== Math.round(w * dpr) || canvas.height !== Math.round(h * dpr)) {
      canvas.width = Math.round(w * dpr);
      canvas.height = Math.round(h * dpr);
      canvas.style.width = `${w}px`;
      canvas.style.height = `${h}px`;
    }
    const ir = img.naturalWidth / img.naturalHeight;
    const cr = w / h;
    let dw = w;
    let dh = h;
    let dx = 0;
    let dy = 0;
    if (cr > ir) {
      dh = w / ir;
      dy = (h - dh) / 2;
    } else {
      dw = h * ir;
      dx = (w - dw) / 2;
    }
    ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
    ctx.clearRect(0, 0, w, h);
    ctx.drawImage(img, dx, dy, dw, dh);
  }, []);

  // Lenis smooth scroll + rAF loop mapping scroll → frame → draw.
  useEffect(() => {
    if (reduced || !ready) return;
    const lenis = new Lenis({ lerp: 0.1, smoothWheel: true });
    let raf = 0;
    let lastOverlay = -1;

    const loop = (t: number) => {
      lenis.raf(t);
      const wrap = wrapRef.current;
      if (wrap) {
        const rect = wrap.getBoundingClientRect();
        const scrollable = wrap.offsetHeight - window.innerHeight;
        const p = scrollable > 0 ? clamp(-rect.top / scrollable, 0, 1) : 0;
        progressRef.current = p;
        const frame = Math.min(FRAME_COUNT - 1, Math.round(p * (FRAME_COUNT - 1)));
        draw(frame);
        // Update overlay state only on meaningful change (keeps React cheap).
        if (Math.abs(p - lastOverlay) > 0.004) {
          lastOverlay = p;
          setProgress(p);
        }
      }
      raf = requestAnimationFrame(loop);
    };
    raf = requestAnimationFrame(loop);

    const onResize = () =>
      draw(Math.round(progressRef.current * (FRAME_COUNT - 1)));
    window.addEventListener("resize", onResize);

    return () => {
      cancelAnimationFrame(raf);
      lenis.destroy();
      window.removeEventListener("resize", onResize);
    };
  }, [draw, ready, reduced]);

  // Reduced-motion / no-JS-friendly fallback: stacked static sections.
  if (reduced) {
    return (
      <main className="bg-[#0a0a0a] text-neutral-100">
        <section className="flex min-h-screen items-center justify-center">
          {/* Provide a single hero still at /public/frames/poster.avif */}
          <img
            src="/frames/poster.avif"
            alt=""
            className="absolute inset-0 h-full w-full object-cover opacity-60"
          />
        </section>
        {CHAPTERS.map((c) => (
          <section
            key={c.id}
            className="relative flex min-h-screen flex-col justify-center gap-3 px-8 md:px-16"
          >
            {c.eyebrow && (
              <p className="font-mono text-xs uppercase tracking-[0.25em] text-neutral-400">
                {c.eyebrow}
              </p>
            )}
            <h2 className="text-4xl font-light uppercase tracking-tight md:text-6xl">
              {c.title}
            </h2>
            {c.meta && (
              <ul className="mt-4 space-y-1 font-mono text-[11px] uppercase tracking-widest text-neutral-500">
                {c.meta.map((m) => (
                  <li key={m}>— {m}</li>
                ))}
              </ul>
            )}
          </section>
        ))}
      </main>
    );
  }

  return (
    <div ref={wrapRef} style={{ height: `${SCROLL_VH * 100}vh` }} className="relative bg-[#0a0a0a]">
      {/* Pinned cinematic viewport */}
      <div className="sticky top-0 h-screen w-full overflow-hidden">
        <canvas ref={canvasRef} className="block h-full w-full" />

        {/* Preloader */}
        {!ready && (
          <div className="absolute inset-0 z-20 flex items-center justify-center bg-[#0a0a0a]">
            <p className="font-mono text-xs uppercase tracking-[0.3em] text-neutral-400">
              Loading {Math.round((loaded / FRAME_COUNT) * 100)}%
            </p>
          </div>
        )}

        {/* Chapter overlays */}
        {ready &&
          CHAPTERS.map((c) => {
            const o = chapterOpacity(c, progress);
            if (o <= 0) return null;
            return (
              <div
                key={c.id}
                style={{ opacity: o }}
                className={`pointer-events-none absolute inset-0 z-10 flex flex-col justify-center gap-3 px-8 md:px-16 ${
                  c.align === "center" ? "items-center text-center" : "items-start"
                }`}
              >
                {c.eyebrow && (
                  <p className="font-mono text-[10px] uppercase tracking-[0.3em] text-neutral-300 md:text-xs">
                    {c.eyebrow}
                  </p>
                )}
                <h2 className="max-w-[14ch] text-4xl font-light uppercase leading-none tracking-tight text-white drop-shadow md:text-7xl">
                  {c.title}
                </h2>
                {c.meta && (
                  <ul className="mt-3 space-y-1 font-mono text-[10px] uppercase tracking-[0.2em] text-neutral-300/80 md:text-[11px]">
                    {c.meta.map((m) => (
                      <li key={m}>— {m}</li>
                    ))}
                  </ul>
                )}
              </div>
            );
          })}

        {/* Scroll progress hairline */}
        <div
          className="absolute bottom-0 left-0 z-10 h-px bg-white/70"
          style={{ width: `${progress * 100}%` }}
        />
      </div>
    </div>
  );
}
