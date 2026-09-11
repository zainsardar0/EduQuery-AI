export default function PageHeader({ eyebrow, title, lead }) {
  return (
    <header>
      <p className="text-xs font-semibold tracking-wide text-ink-3 uppercase">{eyebrow}</p>
      <h1 className="mt-2 text-[1.75rem] text-ink">{title}</h1>
      {lead && <p className="mt-2 max-w-2xl text-sm leading-relaxed text-ink-2">{lead}</p>}
    </header>
  )
}
