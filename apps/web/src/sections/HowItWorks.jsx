import { Workflow, Lock, ScrollText } from 'lucide-react'
import { Section, SectionHead, Card } from '../components/ui'
import { steps } from '../lib/content'

export default function HowItWorks() {
  return (
    <Section id="how" className="py-24 sm:py-32">
      <SectionHead
        icon={Workflow}
        eyebrow="How it works"
        title="Five steps. Three seconds. No query language."
        lead="Your staff need no training beyond knowing what they want to find out."
        align="center"
      />

      <ol className="mt-16 grid gap-4 md:grid-cols-3 lg:grid-cols-5">
        {steps.map((s, i) => (
          <li
            key={s.n}
            data-reveal
            className={`card-hover rounded-lg p-7 shadow-card ${
              i === 4 ? 'bg-lime' : 'bg-surface-2'
            }`}
          >
            <span
              className={`flex h-9 w-9 items-center justify-center rounded-full text-[0.8125rem] font-semibold ${
                i === 4 ? 'bg-btn text-lime' : 'bg-surface text-ink'
              }`}
            >
              {s.n}
            </span>
            <h3 className="mt-6 text-[1.1875rem] text-ink">{s.title}</h3>
            <p className={`mt-3 text-sm leading-relaxed ${i === 4 ? 'text-on-accent/70' : 'text-ink-2'}`}>
              {s.body}
            </p>
          </li>
        ))}
      </ol>

      <div className="mt-5 grid gap-4 sm:grid-cols-2">
        <Card data-reveal hover={false} tone="card" className="p-8">
          <span className="flex h-10 w-10 items-center justify-center rounded-full bg-accent-sky">
            <Lock size={17} className="text-[#0c0d0f]" strokeWidth={2} aria-hidden="true" />
          </span>
          <h3 className="mt-6 text-[1.375rem] text-ink">It cannot change anything</h3>
          <p className="mt-3 text-[0.9375rem] leading-relaxed text-ink-2">
            The assistant reads. It cannot add, delete or modify a record — a window into
            your data warehouse, not a door.
          </p>
        </Card>

        <Card data-reveal hover={false} tone="card" className="p-8">
          <span className="flex h-10 w-10 items-center justify-center rounded-full bg-surface-3">
            <ScrollText size={17} className="text-lime" strokeWidth={2} aria-hidden="true" />
          </span>
          <h3 className="mt-6 text-[1.375rem] text-ink">Everything is logged</h3>
          <p className="mt-3 text-[0.9375rem] leading-relaxed text-ink-2">
            Every question and answer is written to an audit trail, so you always know who
            asked what, and when.
          </p>
        </Card>
      </div>
    </Section>
  )
}
