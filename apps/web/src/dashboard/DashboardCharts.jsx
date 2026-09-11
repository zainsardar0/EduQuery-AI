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
import {
  historicalPerformance,
  passProbability,
  performanceTrend,
  riskDistribution,
  subjectComparison,
  shapDrivers,
  campusStats,
} from '../lib/analyticsData'

const axis = { fontSize: 11, fontFamily: 'JetBrains Mono, monospace', fill: '#8A8F94' }
const grid = '#EEF0F3'

function ChartTooltip({ active, payload, label, unit = '%' }) {
  if (!active || !payload?.length) return null
  return (
    <div className="rounded-xl border border-line bg-surface px-3.5 py-2.5 text-xs shadow-lift">
      {label && <p className="font-mono font-semibold text-ink">{label}</p>}
      <div className="mt-1.5 space-y-1">
        {payload.map((p) => (
          <div key={p.dataKey ?? p.name} className="flex items-center gap-2">
            <span
              className="h-2 w-2 shrink-0 rounded-full"
              style={{ background: p.color ?? p.payload?.color ?? '#003d1c' }}
              aria-hidden="true"
            />
            <span className="text-ink-2">{p.name}:</span>
            <span className="font-mono font-semibold text-ink">
              {p.value}
              {unit}
            </span>
          </div>
        ))}
      </div>
    </div>
  )
}

export function PerformanceTrendCard() {
  const [ref, inView] = useInViewOnce()
  return (
    <AnalyticsCard
      className="lg:col-span-2"
      title="Longitudinal Academic Trajectory (2023–2026)"
      description="Network-wide average across 20 Daanish residential campuses"
      insight="Performance has steadily recovered from the 2023 baseline (62.4%) to 68.7% in 2025. The 2026 AI Model projects a 74.2% pass rate with targeted remediation."
    >
      <div
        ref={ref}
        className="h-64"
        role="img"
        aria-label="Multi-term trajectory rising from 62.4% in 2023 to a projected 74.2% in 2026"
      >
        {inView && (
          <ResponsiveContainer width="100%" height="100%">
            <AreaChart data={performanceTrend} margin={{ top: 8, right: 30, bottom: 0, left: -20 }}>
              <defs>
                <linearGradient id="pineTrendFill" x1="0" y1="0" x2="0" y2="1">
                  <stop offset="0%" stopColor="#003d1c" stopOpacity={0.25} />
                  <stop offset="100%" stopColor="#003d1c" stopOpacity={0.01} />
                </linearGradient>
              </defs>
              <CartesianGrid stroke={grid} vertical={false} />
              <XAxis dataKey="stage" tick={axis} tickLine={false} axisLine={false} />
              <YAxis domain={[55, 80]} tick={axis} tickLine={false} axisLine={false} unit="%" />
              <Tooltip content={<ChartTooltip />} cursor={{ stroke: '#E2E4E8' }} />
              <Area
                type="monotone"
                dataKey="score"
                name="Actual / AI Projected Pass Rate"
                stroke="#003d1c"
                strokeWidth={2.5}
                fill="url(#pineTrendFill)"
                dot={{ r: 3.5, fill: '#003d1c', strokeWidth: 0 }}
                activeDot={{ r: 6, fill: '#d3f84e', stroke: '#003d1c', strokeWidth: 2 }}
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

export function PassProbabilityCard() {
  const [ref, inView] = useInViewOnce()
  const size = 148
  const stroke = 12
  const r = (size - stroke) / 2
  const circumference = 2 * Math.PI * r
  const [display, setDisplay] = useState(0)

  useEffect(() => {
    if (!inView) return
    if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
      setDisplay(Math.round(passProbability))
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
      title="Board Pass Confidence"
      description="Calibrated model forecast (Roll No. 5522)"
      insight="Students with >80% pass probability are classified as Low Risk. This student achieved 87.4% confidence following assignment remediation."
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
                <stop offset="0%" stopColor="#003d1c" />
                <stop offset="100%" stopColor="#2f6b46" />
              </linearGradient>
            </defs>
            <circle cx={size / 2} cy={size / 2} r={r} fill="none" stroke="#EEF0F3" strokeWidth={stroke} />
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
            <p className="font-mono text-[1.75rem] font-bold text-ink">{display}%</p>
            <p className="text-[0.6875rem] font-medium text-ink-3">Pass Probability</p>
          </div>
        </div>
      </div>
    </AnalyticsCard>
  )
}

export function SubjectComparisonCard() {
  const [ref, inView] = useInViewOnce()
  return (
    <AnalyticsCard
      title="Subject Mastery vs Board Target"
      description="Current baseline vs AI-projected pass rates"
      insight="Physics (58.2% → 64.0%) and Mathematics (61.4% → 67.2%) represent the primary STEM bottlenecks, requiring targeted intervention."
    >
      <div className="mb-4 flex items-center gap-4 text-xs">
        <span className="flex items-center gap-1.5 text-ink-2">
          <span className="h-2 w-2 rounded-full bg-[#003d1c]" aria-hidden="true" />
          Current Score
        </span>
        <span className="flex items-center gap-1.5 text-ink-2">
          <span className="h-2 w-2 rounded-full bg-[#2f6b46]" aria-hidden="true" />
          AI Projected
        </span>
      </div>
      <div
        ref={ref}
        className="h-56"
        role="img"
        aria-label="Current versus projected pass percentage across six core subjects"
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
              <Tooltip content={<ChartTooltip />} cursor={{ fill: '#F6F7FA' }} />
              <Bar dataKey="current" name="Current Score" fill="#003d1c" radius={[4, 4, 0, 0]} barSize={12} animationDuration={900} />
              <Bar dataKey="predicted" name="AI Projected" fill="#2f6b46" radius={[4, 4, 0, 0]} barSize={12} animationDuration={900} animationBegin={120} />
            </BarChart>
          </ResponsiveContainer>
        )}
      </div>
    </AnalyticsCard>
  )
}

export function RiskDonutCard() {
  const [ref, inView] = useInViewOnce()
  return (
    <AnalyticsCard
      title="Academic Risk Distribution"
      description="73,031 students across 20 campuses"
      insight="68.4% of students are Low Risk, while 9.8% (7,158 students) are High Risk and require immediate academic review."
    >
      <div className="flex flex-col items-center gap-5">
        <div
          ref={ref}
          className="h-32 w-32 shrink-0"
          role="img"
          aria-label="68.4% low risk, 21.8% moderate risk, 9.8% high risk"
        >
          {inView && (
            <ResponsiveContainer width="100%" height="100%">
              <PieChart>
                <Pie
                  data={riskDistribution}
                  dataKey="value"
                  nameKey="name"
                  innerRadius="60%"
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
        <ul className="w-full min-w-0 space-y-2.5">
          {riskDistribution.map((d) => (
            <li key={d.name} className="grid grid-cols-[1fr_auto] items-baseline gap-3 text-xs">
              <span className="flex min-w-0 items-center gap-2 text-ink-2">
                <span className="h-2 w-2 shrink-0 rounded-full" style={{ background: d.color }} aria-hidden="true" />
                <span className="truncate font-medium">{d.name}</span>
              </span>
              <span className="font-mono font-semibold text-ink whitespace-nowrap">{d.value}% ({d.count.toLocaleString()})</span>
            </li>
          ))}
        </ul>
      </div>
    </AnalyticsCard>
  )
}

export function ShapAttributionCard() {
  const [ref, inView] = useInViewOnce()
  return (
    <AnalyticsCard
      title="Explainable AI: Risk Feature Weights (SHAP)"
      description="Statistical drivers of academic failure risk"
      insight="Pre-board mock scores (41.2%) and attendance below 75% (28.4%) account for nearly 70% of total predictive risk variance."
    >
      <div
        ref={ref}
        className="h-56"
        role="img"
        aria-label="SHAP feature importance weights: Mock score 41.2%, Attendance 28.4%, Teacher index 16.5%, Homework 13.9%"
      >
        {inView && (
          <ResponsiveContainer width="100%" height="100%">
            <BarChart
              data={shapDrivers}
              layout="vertical"
              margin={{ top: 4, right: 20, bottom: 0, left: 10 }}
            >
              <CartesianGrid stroke={grid} horizontal={false} />
              <XAxis type="number" domain={[0, 50]} tick={axis} tickLine={false} axisLine={false} unit="%" />
              <YAxis
                type="category"
                dataKey="feature"
                tick={{ ...axis, fontSize: 10 }}
                width={120}
                tickLine={false}
                axisLine={false}
                tickFormatter={(v) => v.split(' ')[0] + ' ' + (v.split(' ')[1] || '')}
              />
              <Tooltip content={<ChartTooltip unit="%" />} cursor={{ fill: '#F6F7FA' }} />
              <Bar dataKey="impact" name="SHAP Importance Weight" fill="#003d1c" radius={[0, 6, 6, 0]} barSize={16}>
                {shapDrivers.map((d, i) => (
                  <Cell key={i} fill={i === 0 ? '#003d1c' : i === 1 ? '#e06a3b' : '#2f6b46'} />
                ))}
              </Bar>
            </BarChart>
          </ResponsiveContainer>
        )}
      </div>
    </AnalyticsCard>
  )
}

export function HistoricalPerformanceCard() {
  const [ref, inView] = useInViewOnce()
  return (
    <AnalyticsCard
      title="Multi-Term Student Pass Volume"
      description="Six terms, 73,031 student cohort"
      insight="Passing student volume increased from 45,571 (62.4%) in 2023 to 50,172 (68.7%) in 2025, driven by institutional academic audits."
    >
      <div
        ref={ref}
        className="h-56"
        role="img"
        aria-label="Student pass volume growing from 45,571 to 50,172 over six terms"
      >
        {inView && (
          <ResponsiveContainer width="100%" height="100%">
            <AreaChart data={historicalPerformance} margin={{ top: 8, right: 8, bottom: 0, left: -10 }}>
              <defs>
                <linearGradient id="historyFill" x1="0" y1="0" x2="0" y2="1">
                  <stop offset="0%" stopColor="#2f6b46" stopOpacity={0.25} />
                  <stop offset="100%" stopColor="#2f6b46" stopOpacity={0.01} />
                </linearGradient>
              </defs>
              <CartesianGrid stroke={grid} vertical={false} />
              <XAxis dataKey="term" tick={{ ...axis, fontSize: 10 }} tickLine={false} axisLine={false} />
              <YAxis domain={[40000, 55000]} tick={axis} tickLine={false} axisLine={false} />
              <Tooltip content={<ChartTooltip unit=" Passed" />} cursor={{ stroke: '#E2E4E8' }} />
              <Area
                type="monotone"
                dataKey="passes"
                name="Passed Students"
                stroke="#2f6b46"
                strokeWidth={2.5}
                fill="url(#historyFill)"
                dot={{ r: 3.5, fill: '#2f6b46', strokeWidth: 0 }}
                activeDot={{ r: 6, fill: '#d3f84e', stroke: '#2f6b46', strokeWidth: 2 }}
                animationDuration={1100}
              />
            </AreaChart>
          </ResponsiveContainer>
        )}
      </div>
    </AnalyticsCard>
  )
}

export function CampusBenchmarkCard() {
  const [ref, inView] = useInViewOnce()
  // Top 8 representative campuses
  const topCampuses = campusStats.slice(0, 8)

  return (
    <AnalyticsCard
      className="lg:col-span-3"
      title="Regional Campus Pass-Rate Benchmarks"
      description="Comparative analysis across North, South, Central, and West zones"
      insight="Attock Girls (77.8%) and Jand Girls (75.1%) lead the network in pass rates, while Fazilpur Boys (61.8%) and Rajanpur Boys (62.4%) require targeted resource allocation."
    >
      <div
        ref={ref}
        className="h-60"
        role="img"
        aria-label="Campus pass rate comparison across representative Daanish campuses"
      >
        {inView && (
          <ResponsiveContainer width="100%" height="100%">
            <BarChart data={topCampuses} margin={{ top: 8, right: 16, bottom: 0, left: -20 }}>
              <CartesianGrid stroke={grid} vertical={false} />
              <XAxis dataKey="code" tick={axis} tickLine={false} axisLine={false} />
              <YAxis domain={[50, 90]} tick={axis} tickLine={false} axisLine={false} unit="%" />
              <Tooltip content={<ChartTooltip />} cursor={{ fill: '#F6F7FA' }} />
              <Bar dataKey="passRate" name="Pass Rate" fill="#003d1c" radius={[4, 4, 0, 0]} barSize={22}>
                {topCampuses.map((c, idx) => (
                  <Cell
                    key={idx}
                    fill={c.passRate >= 73 ? '#003d1c' : c.passRate >= 68 ? '#2f6b46' : '#e06a3b'}
                  />
                ))}
              </Bar>
            </BarChart>
          </ResponsiveContainer>
        )}
      </div>
    </AnalyticsCard>
  )
}
