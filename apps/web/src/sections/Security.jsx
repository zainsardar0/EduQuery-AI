import { ShieldCheck } from 'lucide-react'
import { Section, SectionHead, Card } from '../components/ui'
import { securityLayers, securityGuarantees } from '../lib/content'

export default function Security() {
  return (
    <Section id="security" className="py-24 sm:py-32">
      <SectionHead
        icon={ShieldCheck}
        eyebrow="Security"
        title="Three locks, and none of them are on the door."
        lead="Student privacy is enforced by the database itself, so it holds even if the application above it is wrong."
      />

      <div className="mt-16 grid gap-4 lg:grid-cols-3">
        {securityLayers.map((l, i) => (
          <Card
            key={l.tag}
            data-reveal
            hover={false}
            tone={i === 1 ? 'lime' : 'card'}
            className="p-8"
          >
            <span
              className={`inline-flex rounded-full px-3 py-1.5 text-xs font-semibold ${
                i === 1
                  ? 'bg-btn text-lime'
                  : i === 0
                    ? 'bg-accent-mauve text-[#0c0d0f]'
                    : 'bg-accent-sky text-[#0c0d0f]'
              }`}
            >
              {l.tag}
            </span>
            <h3 className="mt-6 text-[1.375rem] text-ink">{l.title}</h3>
            <p
              className={`mt-3 text-[0.9375rem] leading-relaxed ${
                i === 1 ? 'text-on-accent/70' : 'text-ink-2'
              }`}
            >
              {l.body}
            </p>
          </Card>
        ))}
      </div>

      <div className="mt-5 grid gap-4 sm:grid-cols-2">
        {securityGuarantees.map((g) => (
          <Card key={g.title} data-reveal hover={false} tone="card" className="p-8">
            <h3 className="text-[1.375rem] text-ink">{g.title}</h3>
            <p className="mt-3 text-[0.9375rem] leading-relaxed text-ink-2">{g.body}</p>
          </Card>
        ))}
      </div>
    </Section>
  )
}
