import { lazy, Suspense } from 'react'
import { CloudSun, ArrowDownRight, ArrowUpRight, Minus } from 'lucide-react'
import { Section, SectionHead, Card, Figure, Eyebrow } from '../components/ui'
import { predictionInputs, predictionOutputs } from '../lib/content'

/*
  Recharts is ~376 kB and every other chart on the site already pays for it
  lazily (see AppShell.jsx) rather than in the landing page's main bundle.
  This grid is five charts deep, so it would otherwise be the single biggest
  addition to that bundle — split it the same way.
*/
const PredictionCharts = lazy(() => import('./PredictionCharts'))

function ChartsFallback() {
  return (
    <div
      className="mt-3 h-[38rem] animate-pulse rounded-2xl bg-[#0C0D0F] sm:h-[30rem]"
      aria-hidden="true"
    />
  )
}

export default function Prediction() {
  return (
    <Section id="prediction" className="pb-20 sm:pb-28">
      <SectionHead
        icon={CloudSun}
        eyebrow="The prediction engine"
        title="A weather forecast for exam results."
        lead="A forecast does not guarantee rain. It gives a reliable, evidence-based estimate from patterns — and tells you how confident it is. The prediction engine works the same way, on a student's history rather than the atmosphere."
      />

      <div className="mt-16 grid gap-4 lg:grid-cols-2">
        <Card data-reveal className="p-8 sm:p-10">
          <Eyebrow icon={ArrowDownRight}>What it reads</Eyebrow>
          <ul className="mt-8 space-y-5">
            {predictionInputs.map((f) => (
              <li key={f.label} className="border-b border-line pb-5 last:border-0 last:pb-0">
                <p className="text-[0.9375rem] font-semibold text-ink">{f.label}</p>
                <p className="mt-1.5 text-sm leading-relaxed text-ink-2">{f.detail}</p>
              </li>
            ))}
          </ul>
        </Card>

        <Card data-reveal hover={false} tone="card" className="p-8 sm:p-10">
          <Eyebrow icon={ArrowUpRight}>What it tells you</Eyebrow>
          <ul className="mt-8 space-y-5">
            {predictionOutputs.map((f) => (
              <li key={f.label} className="border-b border-line-2 pb-5 last:border-0 last:pb-0">
                <p className="text-[0.9375rem] font-semibold text-ink">{f.label}</p>
                <p className="mt-1.5 text-sm leading-relaxed text-ink-2">{f.detail}</p>
              </li>
            ))}
          </ul>
        </Card>
      </div>

      <div className="mt-5 grid gap-4 lg:grid-cols-[1.2fr_1fr]">
        <Card data-reveal hover={false} tone="lime" className="p-8 sm:p-10">
          <span className="flex h-10 w-10 items-center justify-center rounded-full bg-ink">
            <Minus size={17} className="text-lime" strokeWidth={2.5} aria-hidden="true" />
          </span>
          <h3 className="mt-6 text-[clamp(1.5rem,2.6vw,2rem)] text-ink">
            No student's grade, promotion or future is ever decided by the AI alone.
          </h3>
          <p className="mt-4 text-[0.9375rem] leading-relaxed text-ink/70">
            Every prediction is labelled as decision support for educators — a tool for
            spotting who needs extra attention. The final judgment always rests with the
            teacher and the administration.
          </p>
        </Card>

        <Card data-reveal className="flex flex-col justify-center p-8 sm:p-10">
          <p className="text-xs font-semibold tracking-wide text-ink-3 uppercase">
            Benchmark accuracy
          </p>
          <Figure className="mt-6 text-[clamp(3rem,6vw,4.25rem)] text-ink" value="92.32" unit="%" />
          <p className="mt-5 text-[0.9375rem] leading-relaxed text-ink-2">
            Achieved by this type of AI in predicting final letter grades from midterm
            scores, in a March 2026 study published in a peer-reviewed international
            educational data mining journal.
          </p>
        </Card>
      </div>

      <Suspense fallback={<ChartsFallback />}>
        <PredictionCharts />
      </Suspense>
    </Section>
  )
}
