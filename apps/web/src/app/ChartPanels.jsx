import {
  Bar,
  BarChart,
  CartesianGrid,
  Line,
  LineChart,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from 'recharts'
import { TriangleAlert } from 'lucide-react'
import { atRisk, trendData } from '../lib/demoData'
import { Delta, Figure } from '../components/ui'

const axis = { fontSize: 11, fontFamily: 'JetBrains Mono, monospace', fill: '#9AA0A6' }

const tooltipStyle = {
  background: '#0C0D0F',
  border: 'none',
  borderRadius: 12,
  fontSize: 12,
  fontFamily: 'JetBrains Mono, monospace',
  color: '#fff',
  padding: '8px 12px',
}

export function ChartAnswer() {
  return (
    <div className="rounded-lg bg-surface p-6 shadow-card">
      <div className="flex items-center justify-between gap-3">
        <p className="text-[0.9375rem] font-semibold text-ink">Class 10 Science</p>
        <Delta value="−18 pts" positive={false} />
      </div>
      <Figure className="mt-6 text-[2.25rem] text-ink" value="53" unit="%" />
      <p className="mt-1 text-xs text-ink-2">Latest term average, down from 71%</p>
      <div
        className="mt-6 h-48"
        role="img"
        aria-label="Class 10 Science average falling from 71 percent in the 2023 midterm to 53 percent in the 2025 annual"
      >
        <ResponsiveContainer width="100%" height="100%">
          <LineChart data={trendData} margin={{ top: 6, right: 8, bottom: 0, left: -20 }}>
            <CartesianGrid stroke="#E4E7EB" vertical={false} />
            <XAxis dataKey="term" tick={axis} tickLine={false} axisLine={false} />
            <YAxis domain={[40, 80]} tick={axis} tickLine={false} axisLine={false} unit="%" />
            <Tooltip contentStyle={tooltipStyle} formatter={(v) => [`${v}%`, 'Average']} />
            <Line
              type="monotone"
              dataKey="value"
              stroke="#0C0D0F"
              strokeWidth={2.5}
              dot={{ r: 3, fill: '#0C0D0F' }}
              activeDot={{ r: 6, fill: '#D3F84E', stroke: '#0C0D0F', strokeWidth: 2 }}
            />
          </LineChart>
        </ResponsiveContainer>
      </div>
      <p className="mt-4 text-sm leading-relaxed text-ink-2">
        Declining every term since 2023. The steepest drop falls between the 2024 annual and
        the 2025 midterm.
      </p>
    </div>
  )
}

export function AtRiskAnswer() {
  return (
    <div className="rounded-lg bg-surface p-6 shadow-card">
      <div className="flex items-center gap-2.5">
        <span className="flex h-8 w-8 items-center justify-center rounded-full bg-alert-wash">
          <TriangleAlert size={15} className="text-alert" />
        </span>
        <p className="text-[0.9375rem] font-semibold text-ink">At-risk ranking</p>
      </div>
      <div
        className="mt-6 h-52"
        role="img"
        aria-label="Risk scores for four flagged students; Ayesha Noor is highest at 83, then Bilal Ahmed 74, Sana Riaz 71, Hamza Iqbal 62"
      >
        <ResponsiveContainer width="100%" height="100%">
          <BarChart data={atRisk} layout="vertical" margin={{ top: 0, right: 16, bottom: 0, left: 8 }}>
            <CartesianGrid stroke="#E4E7EB" horizontal={false} />
            <XAxis type="number" domain={[0, 100]} tick={axis} tickLine={false} axisLine={false} />
            <YAxis
              type="category"
              dataKey="name"
              tick={axis}
              width={92}
              tickLine={false}
              axisLine={false}
            />
            <Tooltip
              cursor={{ fill: '#F6F7F9' }}
              contentStyle={tooltipStyle}
              formatter={(v, _n, item) => [`${v} risk · band ${item.payload.band}`, 'Score']}
            />
            <Bar dataKey="risk" fill="#0C0D0F" radius={[0, 6, 6, 0]} barSize={18} />
          </BarChart>
        </ResponsiveContainer>
      </div>
      <p className="mt-4 text-sm leading-relaxed text-ink-2">
        Ranked by predicted risk of failing. Each entry carries its own explanation and is
        reviewable by the subject teacher.
      </p>
    </div>
  )
}
