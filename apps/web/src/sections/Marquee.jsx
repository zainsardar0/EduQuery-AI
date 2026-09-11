import { askedQuestions } from '../lib/content'

/**
 * Duplicated once so the track is always at least twice the widest viewport,
 * then translated by exactly -50% — any rounding error shows as a stutter
 * once per cycle. Constant linear velocity: easing would imply an animator.
 */
export default function Marquee() {
  const items = [...askedQuestions, ...askedQuestions]

  return (
    <section aria-label="Example questions" className="py-16 sm:py-20">
      <p className="mb-8 text-center text-sm text-ink-3">What people ask it</p>
      <div className="marquee overflow-hidden">
        <ul className="marquee-track flex w-max gap-3">
          {items.map((q, i) => (
            <li
              key={`${q}-${i}`}
              aria-hidden={i >= askedQuestions.length ? 'true' : undefined}
              className="shrink-0 rounded-full border border-line bg-surface px-6 py-3.5 font-mono text-[0.8125rem] text-ink-2"
            >
              {q}
            </li>
          ))}
        </ul>
      </div>
    </section>
  )
}
