import { MessageSquareText } from 'lucide-react'
import { Section, SectionHead } from '../components/ui'
import { questionGroups } from '../lib/content'
import { useReveal } from '../lib/useReveal'

/*
  A twelve-item grid used to sit in one block — every card fired its stagger
  at once, the moment the section's top crossed into view, so the reader met
  all twelve simultaneously. Three independent groups mean three separate
  IntersectionObservers: a group's four cards animate only once THAT group
  reaches reading position, giving each cluster room to be looked at on its
  own rather than all of them competing for attention together.

  Colour runs by COLUMN rather than by group, so all four reference-palette
  swatches (sky, peach, mauve, lime) appear in every row instead of three of
  them being reserved and one held back — the same identity-not-decoration
  logic as before, just read down a column instead of across a group. The
  featured Forecasts card keeps its full lime fill regardless of which column
  it lands in: that treatment marks it as the exception (the AI's own
  reasoning surfacing), not a fifth colour.
*/
const ACCENTS = [
  {
    tab: 'bg-accent-sky',
    blob: 'bg-accent-sky',
    glow: 'hover:shadow-[0_28px_52px_-30px_var(--color-accent-sky)]',
  },
  {
    tab: 'bg-accent-peach',
    blob: 'bg-accent-peach',
    glow: 'hover:shadow-[0_28px_52px_-30px_var(--color-accent-peach)]',
  },
  {
    tab: 'bg-accent-mauve',
    blob: 'bg-accent-mauve',
    glow: 'hover:shadow-[0_28px_52px_-30px_var(--color-accent-mauve)]',
  },
  {
    tab: 'bg-lime',
    blob: 'bg-lime',
    glow: 'hover:shadow-[0_28px_52px_-30px_var(--color-lime)]',
  },
]

function QuestionGroup({ label, items, offset }) {
  const reveal = useReveal({ stagger: 70, selector: '[data-reveal-group]' })

  return (
    <div ref={reveal} className={offset === 0 ? '' : 'mt-16 sm:mt-20'}>
      <p data-reveal-group className="text-xs font-semibold tracking-wide text-ink-3 uppercase">
        {label}
      </p>
      <ul className="mt-6 grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
        {items.map((q, i) => {
          const n = offset + i
          const featured = n === 10
          const accent = ACCENTS[i]
          return (
            <li
              key={q.type}
              data-reveal-group
              className={`group relative overflow-hidden rounded-lg p-7 ${
                featured ? 'card-hover bg-lime' : `tile tile-float ${accent.glow}`
              }`}
            >
              {!featured && (
                <>
                  <span
                    className={`pointer-events-none absolute -top-9 -left-9 z-0 h-28 w-28 rounded-full opacity-0 blur-2xl transition-opacity duration-500 ease-out group-hover:opacity-25 ${accent.blob}`}
                    aria-hidden="true"
                  />
                  <span
                    className={`absolute top-0 left-7 z-0 h-1 w-8 rounded-b-full transition-[width] duration-300 ease-out group-hover:w-14 ${accent.tab}`}
                    aria-hidden="true"
                  />
                </>
              )}
              <div className="relative z-10">
                <div className="flex items-center justify-between gap-3">
                  <h3
                    className={`text-[0.9375rem] font-semibold ${featured ? 'text-on-accent' : 'text-ink'}`}
                  >
                    {q.type}
                  </h3>
                  <span className={`figure text-sm ${featured ? 'text-on-accent/35' : 'text-ink-3/50'}`}>
                    {String(n + 1).padStart(2, '0')}
                  </span>
                </div>
                <p
                  className={`mt-4 font-mono text-[0.8125rem] leading-relaxed ${
                    featured ? 'text-on-accent/70' : 'text-ink-2'
                  }`}
                >
                  {q.example}
                </p>
              </div>
            </li>
          )
        })}
      </ul>
    </div>
  )
}

export default function QuestionTypes() {
  return (
    <Section id="questions" className="pb-24 sm:pb-32">
      <SectionHead
        icon={MessageSquareText}
        eyebrow="What you can ask"
        title="Twelve kinds of question. One way of asking."
        lead="You never need the technical name of a table or a column. You type the question the way you would say it out loud."
        align="center"
      />

      <div className="mt-20">
        {questionGroups.map((g, gi) => (
          <QuestionGroup
            key={g.label}
            label={g.label}
            items={g.items}
            offset={gi * questionGroups[0].items.length}
          />
        ))}
      </div>

      <p className="mx-auto mt-16 max-w-2xl text-center text-[0.9375rem] leading-relaxed text-ink-3">
        The AI handles every piece of technical translation behind the scenes. If it cannot
        answer confidently, it says so rather than guessing.
      </p>
    </Section>
  )
}
