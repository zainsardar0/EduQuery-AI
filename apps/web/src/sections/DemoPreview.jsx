import { ArrowRight, MonitorPlay } from 'lucide-react'
import { Section, SectionHead, Button } from '../components/ui'
import { PredictionAnswer, TableAnswer } from '../app/AnswerPanels'

export default function DemoPreview({ onOpenDemo }) {
  return (
    <Section id="demo" className="py-24 sm:py-32">
      <SectionHead
        icon={MonitorPlay}
        eyebrow="The interface"
        title="This is what an answer looks like."
        lead="One input box, and whatever form the answer needs — a table, a chart, a forecast with its reasoning attached. Nothing else competing for attention."
        align="center"
      />

      <div className="glow-sand mt-14 rounded-xl p-3 sm:p-5">
        <div className="grid gap-3 lg:grid-cols-2">
          <div data-reveal className="min-w-0">
            <TableAnswer />
          </div>
          <div data-reveal className="min-w-0">
            <PredictionAnswer />
          </div>
        </div>
      </div>

      <div className="mt-10 flex flex-col items-center gap-4 text-center">
        <Button onClick={onOpenDemo} className="group pr-6 pl-2">
          <span className="flex h-9 w-9 items-center justify-center rounded-full bg-lime text-ink transition-transform duration-500 ease-[cubic-bezier(0.16,1,0.3,1)] group-hover:translate-x-0.5">
            <ArrowRight size={16} strokeWidth={2.4} />
          </span>
          Open the full interface
        </Button>
        <p className="text-sm text-ink-3">
          Interface mockup with illustrative data — not real student records.
        </p>
      </div>
    </Section>
  )
}
