import { ArrowDownRight, ArrowUpRight, Minus } from 'lucide-react'
import { passRateQuery, prediction } from '../lib/demoData'
import { Figure } from '../components/ui'

export function TableAnswer() {
  return (
    <div className="overflow-hidden rounded-lg bg-surface shadow-card">
      <div className="flex flex-wrap items-center justify-between gap-2 px-6 py-5">
        <p className="text-[0.9375rem] font-semibold text-ink">Pass rate by school</p>
        <span className="font-mono text-[0.6875rem] text-ink-3">
          {passRateQuery.meta.rows} rows · {passRateQuery.meta.seconds}
        </span>
      </div>
      <div className="overflow-x-auto">
        <table className="w-full min-w-[34rem] text-left text-sm">
          <thead>
            <tr className="bg-surface-2">
              {passRateQuery.columns.map((c, i) => (
                <th
                  key={c}
                  scope="col"
                  className={`px-6 py-3 text-xs font-semibold tracking-wide text-ink-3 uppercase ${
                    i > 1 ? 'text-right' : ''
                  }`}
                >
                  {c}
                </th>
              ))}
            </tr>
          </thead>
          <tbody className="divide-y divide-line">
            {passRateQuery.rows.map((r) => (
              <tr
                key={r[0]}
                className="transition-colors duration-300 ease-[cubic-bezier(0.16,1,0.3,1)] hover:bg-surface-2"
              >
                <td className="px-6 py-4 font-medium text-ink">{r[0]}</td>
                <td className="px-6 py-4 text-ink-2">{r[1]}</td>
                <td className="px-6 py-4 text-right text-ink-2">{r[2]}</td>
                <td className="px-6 py-4 text-right text-ink-2">{r[3]}</td>
                <td className="px-6 py-4 text-right">
                  <span
                    className={`tabular font-semibold ${
                      r[4] < 60 ? 'text-alert' : r[4] < 75 ? 'text-ink' : 'text-positive'
                    }`}
                  >
                    {r[4].toFixed(1)}%
                  </span>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
      <p className="bg-surface-2 px-6 py-5 text-sm leading-relaxed text-ink-2">
        {passRateQuery.summary}
      </p>
    </div>
  )
}

function DriverIcon({ direction }) {
  if (direction === 'up') return <ArrowUpRight size={14} className="text-positive" />
  if (direction === 'down') return <ArrowDownRight size={14} className="text-alert" />
  return <Minus size={14} className="text-ink-3" />
}

export function PredictionAnswer() {
  const p = prediction
  return (
    <div className="overflow-hidden rounded-lg bg-surface shadow-card">
      <div className="bg-lime px-6 py-5">
        <div className="flex flex-wrap items-center justify-between gap-2">
          <p className="text-[0.9375rem] font-semibold text-ink">Forecast — not a decision</p>
          <span className="rounded-full bg-ink/10 px-2.5 py-1 text-xs font-semibold text-ink">
            {p.confidence} confidence
          </span>
        </div>
      </div>

      <div className="grid gap-8 p-6 sm:grid-cols-2 sm:p-8">
        <div>
          <p className="font-mono text-xs text-ink-2">
            Roll No. {p.roll} · {p.student}
          </p>
          <p className="mt-1 text-sm text-ink-2">
            {p.subject} — {p.exam}
          </p>
          <Figure className="mt-7 text-[clamp(2.5rem,6vw,3.25rem)] text-ink" value={p.range} />
          <div className="mt-5 flex flex-wrap items-center gap-2">
            <span className="rounded-full bg-surface-2 px-3 py-1.5 text-xs font-semibold text-ink">
              Band {p.band}
            </span>
            <span className="rounded-full bg-positive-wash px-3 py-1.5 text-xs font-semibold text-positive">
              {p.passProbability}% chance of passing
            </span>
          </div>
          <div className="mt-6">
            <div className="h-2.5 overflow-hidden rounded-full bg-surface-3">
              <div
                className="h-full rounded-full bg-ink transition-[width] duration-1000 ease-[cubic-bezier(0.16,1,0.3,1)]"
                style={{ width: `${p.passProbability}%` }}
              />
            </div>
          </div>
        </div>

        <div>
          <p className="text-xs font-semibold tracking-wide text-ink-3 uppercase">Why</p>
          <ul className="mt-5 space-y-3">
            {p.drivers.map((d) => (
              <li
                key={d.label}
                className="flex items-center justify-between gap-3 border-b border-line pb-3 text-sm last:border-0"
              >
                <span className="flex items-center gap-2 text-ink-2">
                  <DriverIcon direction={d.direction} />
                  {d.label}
                </span>
                <span className="tabular text-xs font-semibold text-ink">{d.value}</span>
              </li>
            ))}
          </ul>
        </div>
      </div>

      <p className="bg-surface-2 px-6 py-5 text-sm leading-relaxed text-ink-2 sm:px-8">
        {p.explanation}
      </p>
    </div>
  )
}
