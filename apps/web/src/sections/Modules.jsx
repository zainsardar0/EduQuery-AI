import { LayoutGrid } from 'lucide-react'
import { Section, SectionHead } from '../components/ui'
import { modules } from '../lib/content'

export default function Modules() {
  return (
    <Section id="product" className="py-24 sm:py-32">
      <SectionHead
        icon={LayoutGrid}
        eyebrow="The product"
        title="Nine modules, one set of records."
        lead="Every module reads the same database, so a figure on the dashboard and a figure in a report can never disagree."
      />

      <ul className="mt-16 grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
        {modules.map((m, i) => (
          <li
            key={m.title}
            data-reveal
            className={`card-hover rounded-lg p-7 shadow-card ${
              i === 1 ? 'bg-lime' : 'bg-surface'
            }`}
          >
            <div className="flex items-center justify-between gap-3">
              <h3 className="text-[1.1875rem] text-ink">{m.title}</h3>
              <span
                className={`rounded-full px-2.5 py-1 text-[0.6875rem] font-semibold ${
                  i === 1 ? 'bg-btn text-lime' : 'bg-surface-2 text-ink-2'
                }`}
              >
                {m.status}
              </span>
            </div>
            <p
              className={`mt-3 text-sm leading-relaxed ${i === 1 ? 'text-on-accent/70' : 'text-ink-2'}`}
            >
              {m.body}
            </p>
          </li>
        ))}
      </ul>
    </Section>
  )
}
