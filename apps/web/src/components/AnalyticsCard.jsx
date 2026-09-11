/**
 * Premium chart card used across the Institutional Analytics and Prediction dashboard.
 * Styled with crisp borders, white surface container, subtle elevation, and actionable AI insight banner.
 */
export function AnalyticsCard({ title, description, insight, className = '', children }) {
  return (
    <div
      data-reveal
      className={`analytics-card rounded-2xl border border-line bg-surface p-6 shadow-sm transition-[transform,box-shadow,border-color] duration-300 ease-[cubic-bezier(0.22,1,0.36,1)] hover:-translate-y-0.5 hover:shadow-card sm:p-7 flex flex-col justify-between ${className}`}
    >
      <div>
        <h4 className="text-[1rem] font-bold text-ink tracking-tight">{title}</h4>
        {description && <p className="mt-1 text-xs leading-relaxed text-ink-3">{description}</p>}
        <div className="mt-5">{children}</div>
      </div>
      {insight && (
        <div className="mt-5 rounded-xl border border-[#003d1c]/15 bg-[#003d1c]/5 p-3 text-xs leading-relaxed text-ink-2">
          <span className="font-bold text-[#003d1c] mr-1">AI Intelligence Brief —</span>
          {insight}
        </div>
      )}
    </div>
  )
}
