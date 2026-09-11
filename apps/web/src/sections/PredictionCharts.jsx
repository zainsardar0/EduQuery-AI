import { useEffect, useState } from 'react'
import {
  Area,
  AreaChart,
  Bar,
  BarChart,
  CartesianGrid,
  Cell,
  Pie,
  PieChart,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from 'recharts'
import { AnalyticsCard } from '../components/AnalyticsCard'
import { useInViewOnce } from '../lib/useInViewOnce'
import { useReveal } from '../lib/useReveal'
import {
  historicalPerformance,
  passProbability,
  performanceTrend,
  riskDistribution,
  subjectComparison,
} from '../lib/analyticsData'

/*
  The only place on the site allowed to carry saturated colour, and even here
  it draws from nothing but the reference accent set (index.css) — sky-deep
  for the prediction line and "current", mauve-deep for "predicted" and the
  historical trend, lime for low risk, peach-deep / peach-deep-2 for medium
  and high risk. The palette has no red; intensity carries what hue would
  otherwise for the risk tiers. Each chart mounts only once it is in view
  (useInViewOnce), so Recharts' own entrance animation plays exactly when the
  reader scrolls to it and never replays on scroll-up.
*/

const axis = { fontSize: 11, fontFamily: 'JetBrains Mono, monospace', fill: '#71767D' }
const grid = 'rgba(255,255,255,0.06)'

function ChartTooltip({ active, payload, label, unit = '%' }) {
  if (!active || !payload?.length) return null
  return (
    <div className="rounded-lg border border-white/10 bg-[#1c1e21]/95 px-3.5 py-2.5 text-xs shadow-[0_12px_32px_rgba(0,0,0,0.5)] backdrop-blur">
      {label && <p className="font-mono text-[#71767D]">{label}</p>}
      <div className="mt-1 space-y-1">
        {payload.map((p) => (
          <div key={p.dataKey ?? p.name} className="flex items-center gap-2">
            <span
              className="h-2 w-2 shrink-0 rounded-full"
              style={{ background: p.color ?? p.payload?.color }}
              aria-hidden="true"
            />
            <span className="text-[#B9BEC4]">{p.name}</span>
            <span className="font-mono font-semibold text-white">
              {p.value}
              {unit}
            </span>
          </div>
        ))}
      </div>
    </div>
  )
}

function PerformanceTrendCard() {
  const [ref, inView] = useInViewOnce()
  return (
    <AnalyticsCard
      className="lg:col-span-2"
      title="Student performance trend"
      description="Roll No. 5522 · Physics, tracked through the term"
      insight="Score has climbed through every checkpoint this term. The predicted final sits four points above the last graded result, in line with the class recovery after the midterm dip."
    >
      <div ref={ref} className="h-64" role="img" aria-label="Score rising from 58 at the midterm to a predicted 68 by the final, five checkpoints tracked through the term">
        {inView && (
          <ResponsiveContainer width="100%" height="100%">
            <AreaChart data={performanceTrend} margin={{ top: 8, right: 44, bottom: 0, left: -20 }}>
              <defs>
                <linearGradient id="trendFill" x1="0" y1="0" x2="0" y2="1">
                  <stop offset="0%" stopColor="var(--color-accent-sky-deep)" stopOpacity={0.35} />
                  <stop offset="100%" stopColor="var(--color-accent-sky-deep)" stopOpacity={0} />
                </linearGradient>
              </defs>
              <CartesianGrid stroke={grid} vertical={false} />
              <XAxis dataKey="stage" tick={axis} tickLine={false} axisLine={false} />
              <YAxis domain={[50, 75]} tick={axis} tickLine={false} axisLine={false} unit="%" />
              <Tooltip content={<ChartTooltip />} cursor={{ stroke: 'rgba(255,255,255,0.12)' }} />
              <Area
                type="monotone"
                dataKey="score"
                name="Score"
                stroke="var(--color-accent-sky-deep)"
                strokeWidth={2.5}
                fill="url(#trendFill)"
                dot={{ r: 3.5, fill: 'var(--color-accent-sky-deep)', strokeWidth: 0 }}
                activeDot={{ r: 6, fill: 'var(--color-accent-sky-deep)', stroke: '#3c3e44', strokeWidth: 2 }}
                animationDuration={1100}
                animationEasing="ease-out"
              />
            </AreaChart>
          </ResponsiveContainer>
        )}
      </div>
    </AnalyticsCard>
  )
}

function PassProbabilityCard() {
  const [ref, inView] = useInViewOnce()
  const size = 148
  const stroke = 12
  const r = (size - stroke) / 2
  const circumference = 2 * Math.PI * r
  const [display, setDisplay] = useState(0)

  useEffect(() => {
    if (!inView) return
    if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
      setDisplay(passProbability)
      return
    }
    const start = performance.now()
    const duration = 1200
    let frame
    const tick = (now) => {
      const t = Math.min((now - start) / duration, 1)
      const eased = t === 1 ? 1 : 1 - Math.pow(2, -10 * t)
      setDisplay(Math.round(passProbability * eased))
      if (t < 1) frame = requestAnimationFrame(tick)
    }
    frame = requestAnimationFrame(tick)
    return () => cancelAnimationFrame(frame)
  }, [inView])

  const offset = circumference * (1 - display / 100)

  return (
    <AnalyticsCard
      title="Pass probability"
      description="Same student, this session"
      insight="Above 80% is treated as low-risk. This student crossed that line after the last assignment was graded."
    >
      <div ref={ref} className="flex items-center justify-center py-2">
        <div
          className="relative"
          style={{ width: size, height: size }}
          role="img"
          aria-label={`${passProbability}% chance of passing`}
        >
          <svg width={size} height={size} className="-rotate-90">
            <defs>
              <linearGradient id="ringGradient" x1="0%" y1="0%" x2="100%" y2="100%">
                <stop offset="0%" stopColor="var(--color-accent-sky-deep)" />
                <stop offset="100%" stopColor="var(--color-lime)" />
              </linearGradient>
            </defs>
            <circle cx={size / 2} cy={size / 2} r={r} fill="none" stroke="rgba(255,255,255,0.08)" strokeWidth={stroke} />
            <circle
              cx={size / 2}
              cy={size / 2}
              r={r}
              fill="none"
              stroke="url(#ringGradient)"
              strokeWidth={stroke}
              strokeLinecap="round"
              strokeDasharray={circumference}
              strokeDashoffset={offset}
              style={{ transition: 'stroke-dashoffset 1200ms cubic-bezier(0.22,1,0.36,1)' }}
            />
          </svg>
          <div className="absolute inset-0 flex flex-col items-center justify-center">
            <p className="font-mono text-[1.75rem] font-semibold text-white">{display}%</p>
            <p className="text-[0.6875rem] text-[#71767D]">chance of passing</p>
          </div>
        </div>
      </div>
    </AnalyticsCard>
  )
}

function SubjectComparisonCard() {
  const [ref, inView] = useInViewOnce()
  return (
    <AnalyticsCard
      title="Subject comparison"
      description="Current vs. predicted, network average"
      insight="Physics and Mathematics carry the widest predicted gain, five points each — the two subjects the midterm audit flagged for extra revision time."
    >
      <div className="mb-4 flex items-center gap-4 text-xs">
        <span className="flex items-center gap-1.5 text-[#B9BEC4]">
          <span className="h-2 w-2 rounded-full bg-accent-sky-deep" aria-hidden="true" />
          Current
        </span>
        <span className="flex items-center gap-1.5 text-[#B9BEC4]">
          <span className="h-2 w-2 rounded-full bg-accent-mauve-deep" aria-hidden="true" />
          Predicted
        </span>
      </div>
      <div
        ref={ref}
        className="h-56"
        role="img"
        aria-label="Current versus predicted pass percentage for five subjects, predicted higher in every case"
      >
        {inView && (
          <ResponsiveContainer width="100%" height="100%">
            <BarChart data={subjectComparison} margin={{ top: 4, right: 4, bottom: 0, left: -24 }} barGap={4}>
              <CartesianGrid stroke={grid} vertical={false} />
              <XAxis
                dataKey="subject"
                tick={{ ...axis, fontSize: 10 }}
                tickLine={false}
                axisLine={false}
                interval={0}
                tickFormatter={(v) => v.slice(0, 4)}
              />
              <YAxis domain={[0, 100]} tick={axis} tickLine={false} axisLine={false} unit="%" />
              <Tooltip content={<ChartTooltip />} cursor={{ fill: 'rgba(255,255,255,0.04)' }} />
              <Bar dataKey="current" name="Current" fill="var(--color-accent-sky-deep)" radius={[6, 6, 0, 0]} barSize={12} animationDuration={900} />
              <Bar dataKey="predicted" name="Predicted" fill="var(--color-accent-mauve-deep)" radius={[6, 6, 0, 0]} barSize={12} animationDuration={900} animationBegin={120} />
            </BarChart>
          </ResponsiveContainer>
        )}
      </div>
    </AnalyticsCard>
  )
}

function RiskDonutCard() {
  const [ref, inView] = useInViewOnce()
  return (
    <AnalyticsCard
      title="Risk distribution"
      description="Network-wide, this session"
      insight="Ten percent of students carry high risk this term, roughly in line with the three-year average of eleven percent."
    >
      <div className="flex items-center gap-6">
        <div
          ref={ref}
          className="h-40 w-40 shrink-0"
          role="img"
          aria-label="68% of students low risk, 22% medium risk, 10% high risk"
        >
          {inView && (
            <ResponsiveContainer width="100%" height="100%">
              <PieChart>
                <Pie
                  data={riskDistribution}
                  dataKey="value"
                  nameKey="name"
                  innerRadius="62%"
                  outerRadius="100%"
                  paddingAngle={3}
                  stroke="none"
                  animationDuration={1000}
                >
                  {riskDistribution.map((d) => (
                    <Cell key={d.name} fill={d.color} />
                  ))}
                </Pie>
                <Tooltip content={<ChartTooltip />} />
              </PieChart>
            </ResponsiveContainer>
          )}
        </div>
        <ul className="flex-1 space-y-2.5">
          {riskDistribution.map((d) => (
            <li key={d.name} className="flex items-center justify-between gap-3 text-xs">
              <span className="flex items-center gap-2 text-[#B9BEC4]">
                <span className="h-2 w-2 shrink-0 rounded-full" style={{ background: d.color }} aria-hidden="true" />
                {d.name}
              </span>
              <span className="font-mono font-semibold text-white">{d.value}%</span>
            </li>
          ))}
        </ul>
      </div>
    </AnalyticsCard>
  )
}

function HistoricalPerformanceCard() {
  const [ref, inView] = useInViewOnce()
  return (
    <AnalyticsCard
      title="Historical performance"
      description="Six terms, network average"
      insight="Growth resumed after the 2024 annual low, gaining six points across the last three terms of comparable history."
    >
      <div ref={ref} className="h-56" role="img" aria-label="Network average falling from 71% to a low of 64% in early 2024, then recovering to 69% by the 2025 annual">
        {inView && (
          <ResponsiveContainer width="100%" height="100%">
            <AreaChart data={historicalPerformance} margin={{ top: 8, right: 8, bottom: 0, left: -20 }}>
              <defs>
                <linearGradient id="historyFill" x1="0" y1="0" x2="0" y2="1">
                  <stop offset="0%" stopColor="var(--color-accent-mauve-deep)" stopOpacity={0.3} />
                  <stop offset="100%" stopColor="var(--color-accent-mauve-deep)" stopOpacity={0} />
                </linearGradient>
              </defs>
              <CartesianGrid stroke={grid} vertical={false} />
              <XAxis dataKey="term" tick={{ ...axis, fontSize: 10 }} tickLine={false} axisLine={false} />
              <YAxis domain={[55, 75]} tick={axis} tickLine={false} axisLine={false} unit="%" />
              <Tooltip content={<ChartTooltip />} cursor={{ stroke: 'rgba(255,255,255,0.12)' }} />
              <Area
                type="monotone"
                dataKey="score"
                name="Average"
                stroke="var(--color-accent-mauve-deep)"
                strokeWidth={2.5}
                fill="url(#historyFill)"
                dot={{ r: 3.5, fill: 'var(--color-accent-mauve-deep)', strokeWidth: 0 }}
                activeDot={{ r: 6, fill: 'var(--color-accent-mauve-deep)', stroke: '#3c3e44', strokeWidth: 2 }}
                animationDuration={1100}
              />
            </AreaChart>
          </ResponsiveContainer>
        )}
      </div>
    </AnalyticsCard>
  )
}

export default function PredictionCharts() {
  const reveal = useReveal({ stagger: 60 })
  return (
    <div ref={reveal} className="mt-8 rounded-2xl bg-[#2a2c31] p-6 sm:p-10">
      <p data-reveal className="text-xs font-semibold tracking-wide text-[#71767D] uppercase">
        Inside the forecast
      </p>
      <h3 data-reveal className="mt-2 text-[clamp(1.375rem,2.4vw,1.75rem)] font-medium text-white">
        The same prediction, five ways.
      </h3>

      <div className="mt-9 grid gap-5 lg:grid-cols-3">
        <PerformanceTrendCard />
        <PassProbabilityCard />
        <SubjectComparisonCard />
        <RiskDonutCard />
        <HistoricalPerformanceCard />
      </div>
    </div>
  )
}
