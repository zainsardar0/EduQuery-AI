import { TriangleAlert } from 'lucide-react'
import { Section, SectionHead, Card } from '../components/ui'
import { problems } from '../lib/content'

export default function Problem() {
  return (
    <Section id="problem" className="py-24 sm:py-32">
      <SectionHead
        icon={TriangleAlert}
        eyebrow="The problem"
        title="The data is already there. Nobody can reach it."
        lead="Schools record marks, attendance and teacher performance every day. Almost none of it reaches the people making decisions."
      />

      <div className="mt-16 grid gap-4 sm:grid-cols-2">
        {problems.map((p, i) => (
          <Card key={p.title} data-reveal className="flex flex-col p-8">
            <span className="figure text-[2.5rem] text-line-2">
              {String(i + 1).padStart(2, '0')}
            </span>
            <h3 className="mt-5 text-[1.375rem] text-ink">{p.title}</h3>
            <p className="mt-3 flex-1 text-[0.9375rem] leading-relaxed text-ink-2">{p.body}</p>
            {/* Restate the pain after the benefit. */}
            <p className="mt-6 border-t border-line pt-5 text-sm font-semibold text-ink">
              {p.noMore}
            </p>
          </Card>
        ))}
      </div>
    </Section>
  )
}
