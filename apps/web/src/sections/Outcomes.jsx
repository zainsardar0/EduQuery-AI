import { Target } from 'lucide-react'
import { Section, SectionHead } from '../components/ui'
import { outcomes } from '../lib/content'

export default function Outcomes() {
  return (
    <Section id="outcomes" className="pb-28 sm:pb-36">
      <SectionHead
        icon={Target}
        eyebrow="Outcomes"
        title="What changes in the first term."
        lead="Not capabilities. The things your staff stop doing, and the students they reach in time."
      />

      <ul className="mt-16 grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
        {outcomes.map((v, i) => (
          <li
            key={v.title}
            data-reveal
            className={`relative rounded-lg p-7 ${i === 1 ? 'card-hover bg-lime' : 'tile'}`}
          >
            {/* A restrained dot on two cards — the same reference palette as
                everywhere else on the page, used at the smallest possible
                dose so the grid stays mostly neutral. */}
            {(i === 3 || i === 4) && (
              <span
                className={`absolute top-7 right-7 h-2.5 w-2.5 rounded-full ${
                  i === 3 ? 'bg-accent-peach' : 'bg-accent-sky'
                }`}
                aria-hidden="true"
              />
            )}
            <span className={`figure text-[1.75rem] ${i === 1 ? 'text-on-accent/30' : 'text-ink-3/50'}`}>
              {String(i + 1).padStart(2, '0')}
            </span>
            <h3 className={`mt-4 text-[1.25rem] ${i === 1 ? 'text-on-accent' : 'text-ink'}`}>
              {v.title}
            </h3>
            <p
              className={`mt-3 text-sm leading-relaxed ${
                i === 1 ? 'text-on-accent/70' : 'text-ink-2'
              }`}
            >
              {v.body}
            </p>
          </li>
        ))}
      </ul>
    </Section>
  )
}
