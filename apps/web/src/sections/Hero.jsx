import { useEffect, useState } from 'react'
import { ArrowRight, CircleCheck, CornerDownLeft, Sparkles, TrendingDown } from 'lucide-react'
import { hero, heroStats } from '../lib/content'
import { Button, Delta, Eyebrow, Figure } from '../components/ui'
import { useCountUp, useReveal } from '../lib/useReveal'

const rotating = [
  'Which schools had the lowest pass rate in Physics?',
  'Show students who missed more than 15 days.',
  'Predict the final result for Roll No. 5522.',
  'Has Class 10 Science declined over three years?',
]

function useTypewriter(phrases) {
  const [index, setIndex] = useState(0)
  const [text, setText] = useState('')
  const [deleting, setDeleting] = useState(false)

  useEffect(() => {
    if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
      setText(phrases[0])
      return
    }
    const current = phrases[index % phrases.length]
    const done = text === current
    const delay = deleting ? 16 : done ? 2600 : 34

    const timer = setTimeout(() => {
      if (!deleting && done) return setDeleting(true)
      if (deleting && text === '') {
        setDeleting(false)
        return setIndex((i) => i + 1)
      }
      setText((t) => (deleting ? current.slice(0, t.length - 1) : current.slice(0, t.length + 1)))
    }, delay)

    return () => clearTimeout(timer)
  }, [text, deleting, index, phrases])

  return text
}

function StatCard({ stat }) {
  const decimals = stat.decimals ?? 0
  const [hostRef, valueRef] = useCountUp(stat.value, { decimals })

  return (
    <div ref={hostRef} data-reveal className="card-hover rounded-lg bg-surface p-7 shadow-card">
      <h4 className="text-sm text-ink">{stat.label}</h4>
      <p className="figure mt-8 text-[clamp(2rem,3.4vw,2.75rem)] text-ink">
        <span ref={valueRef}>{stat.value.toFixed(decimals)}</span>
        {stat.unit && <span className="figure-unit">{stat.unit}</span>}
      </p>
      <p className="mt-3 text-sm text-ink-2">{stat.note}</p>
    </div>
  )
}

export default function Hero({ onOpenDemo }) {
  const typed = useTypewriter(rotating)
  const reveal = useReveal({ stagger: 90 })

  return (
    <div id="top">
      <div ref={reveal}>
        {/* Full bleed: no page gutter means no background strip beside the slab. */}
        <div className="glow-sand relative overflow-hidden px-4 pt-24 pb-6 sm:px-6 sm:pt-28 sm:pb-8">
          <div className="mx-auto w-full max-w-[84rem]">
          <div className="grid items-stretch gap-2 sm:gap-3 lg:grid-cols-[1.02fr_1fr]">
            <div className="flex flex-col justify-center rounded-lg bg-surface p-7 sm:p-10 lg:p-12">
              <div data-reveal>
                <Eyebrow icon={Sparkles}>{hero.eyebrow}</Eyebrow>
              </div>

              {/* Each line rises out from behind its own edge, in reading order. */}
              <h1 className="mt-7 text-[clamp(1.9rem,3.3vw,2.85rem)] text-ink">
                {hero.title.map((line) => (
                  <span key={line} data-reveal className="line-mask">
                    <span>{line}</span>
                  </span>
                ))}
              </h1>

              <p data-reveal className="mt-6 max-w-md text-[1.0625rem] leading-[1.62] text-ink-2">
                {hero.subhead}
              </p>

              {/* One CTA in the fold. A single path reads as clarity. */}
              <div data-reveal className="mt-9">
                <Button onClick={onOpenDemo} icon={ArrowRight} className="pl-2.5">
                  {hero.cta}
                </Button>
              </div>

              <p
                data-reveal
                className="mt-9 flex items-center gap-2.5 text-[0.9375rem] text-ink-2"
              >
                <CircleCheck size={19} strokeWidth={1.8} className="shrink-0 text-ink-3" />
                {hero.proof}
              </p>
            </div>

            {/* Product imagery: cards floating directly on the wash. */}
            <div
              data-reveal
              className="relative flex flex-col justify-center gap-3 p-2 sm:p-5 lg:p-7"
            >
              <div className="flex items-center gap-3 rounded-md bg-surface px-4 py-4 shadow-float">
                <span className="h-2 w-2 shrink-0 rounded-full bg-lime" aria-hidden="true" />
                <p className="min-w-0 flex-1 truncate font-mono text-[0.8125rem] text-ink">
                  {typed}
                  <span
                    className="ml-0.5 inline-block h-[1.05em] w-[2px] translate-y-[0.18em] bg-ink"
                    style={{ animation: 'blink-caret 1s steps(1) infinite' }}
                    aria-hidden="true"
                  />
                </p>
                <kbd className="hidden shrink-0 items-center gap-1 rounded-md bg-surface-2 px-2 py-1 font-mono text-[0.6875rem] text-ink-3 sm:flex">
                  <CornerDownLeft size={11} strokeWidth={2.2} />
                </kbd>
              </div>

              <div className="grid gap-3 sm:grid-cols-2">
                <div className="rounded-md bg-surface p-5 shadow-float">
                  <div className="flex items-center justify-between gap-2">
                    <h4 className="text-[0.8125rem] text-ink">Lowest pass rate</h4>
                    <Delta value="−26.6" positive={false} />
                  </div>
                  <Figure className="mt-7 text-[2.25rem] text-ink" value="53.4" unit="%" />
                  <p className="mt-2 text-xs text-ink-2">Campus B · Physics</p>
                </div>

                <div className="rounded-md bg-lime p-5 shadow-float">
                  <div className="flex items-center justify-between gap-2">
                    <h4 className="text-[0.8125rem] text-ink">Flagged early</h4>
                    <TrendingDown size={16} className="text-on-accent/50" aria-hidden="true" />
                  </div>
                  <Figure className="mt-7 text-[2.25rem] text-ink" value="24" unit="students" />
                  <p className="mt-2 text-xs text-on-accent/60">Predicted at risk this term</p>
                </div>
              </div>

              <div className="rounded-md bg-surface-3 p-5 shadow-float">
                <p className="text-[0.8125rem] font-medium text-ink-3">Answered in</p>
                <div className="mt-2 flex flex-wrap items-end justify-between gap-x-4 gap-y-1">
                  <Figure className="text-[2rem] text-ink" value="2.4" unit="s" />
                  <p className="pb-1 text-xs text-ink-3">
                    read-only query · written to the audit log
                  </p>
                </div>
              </div>
            </div>
            </div>
          </div>
        </div>

        <div className="mx-auto w-full max-w-[84rem] px-4 py-3 sm:px-6">
          <div className="grid gap-3 md:grid-cols-3">
            {heroStats.map((s) => (
              <StatCard key={s.label} stat={s} />
            ))}
          </div>
        </div>
      </div>
    </div>
  )
}
