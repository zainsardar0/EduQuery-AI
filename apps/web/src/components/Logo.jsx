export function Mark({ className = 'h-9 w-9', light = false }) {
  return (
    <svg viewBox="0 0 36 36" className={className} aria-hidden="true">
      <rect width="36" height="36" rx="18" fill={light ? '#FFFFFF' : '#0C0D0F'} />
      <circle cx="13.5" cy="18" r="4.2" fill={light ? '#0C0D0F' : '#FFFFFF'} />
      <circle cx="23.5" cy="18" r="4.2" fill="#D3F84E" />
    </svg>
  )
}

export default function Logo({ light = false, className = '' }) {
  return (
    <span className={`flex items-center gap-2.5 ${className}`}>
      <Mark light={light} className="h-8 w-8 shrink-0" />
      <span
        className={`text-[1.0625rem] font-bold tracking-[-0.03em] ${
          light ? 'text-white' : 'text-ink'
        }`}
      >
        EduQuery
      </span>
    </span>
  )
}
