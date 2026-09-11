/*
  Environmental lighting, not content. A single decorative loop, fixed to the
  viewport so no wrapper has to be sized or positioned to match the page's
  actual pixel geometry — visibility is entirely controlled by --video-op
  (see useScrollProgress.js), which fades it in as the hero ends, holds it
  through Marquee, and fades it out before Problem. Never in the hero itself,
  never behind the headline or the product mockup — by the time it is visible
  at all, both are already above the fold and behind the reader.

  `armed` (lifted to App.jsx, flipped by a sentinel placed in normal document
  flow right where the hero ends) delays mounting the <video> — and so
  fetching it — until the reader is actually approaching its visible window,
  rather than during the hero's own paint.
*/
export default function AmbientVideo({ armed }) {
  return (
    <div
      aria-hidden="true"
      className="pointer-events-none fixed inset-0 -z-10 overflow-hidden"
      style={{
        opacity: 'calc(var(--video-op, 0) * 0.5)',
        maskImage: 'radial-gradient(68% 62% at 50% 40%, black, transparent 80%)',
        WebkitMaskImage: 'radial-gradient(68% 62% at 50% 40%, black, transparent 80%)',
        willChange: 'opacity',
      }}
    >
      {armed && (
        <video
          className="absolute top-1/2 left-1/2 h-[130vh] w-[130vw] object-cover"
          style={{ filter: 'blur(32px) saturate(1.15)', transform: 'translate(-50%, -50%) scale(1.1)' }}
          src="/ambient-loop.mp4"
          autoPlay
          muted
          loop
          playsInline
          preload="none"
        />
      )}
    </div>
  )
}
