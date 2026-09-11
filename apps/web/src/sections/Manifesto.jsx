import { manifesto } from '../lib/content'
import { useReveal } from '../lib/useReveal'

/** A deliberate empty beat between the marquee and the argument. */
export default function Manifesto() {
  const reveal = useReveal()

  return (
    <section className="px-3 py-20 sm:px-4 sm:py-28">
      <div ref={reveal} className="mx-auto max-w-4xl px-5 sm:px-8">
        <p
          data-reveal
          className="text-[clamp(1.375rem,2.8vw,2rem)] leading-[1.35] font-medium tracking-[-0.028em] text-ink"
        >
          {manifesto}
        </p>
      </div>
    </section>
  )
}
