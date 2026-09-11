import { useReveal } from '../lib/useReveal'

/**
 * A section has no colour of its own — not a light one, not a dark one, and
 * not a raised one either. It sits on the page's continuous colour field and
 * shows whatever the field currently is. A full-bleed background here would
 * put a hard horizontal edge across the page and turn the band back into a
 * "section", which is the whole thing this design is built to avoid.
 *
 * Separation between bands comes from vertical rhythm and from the cards
 * inside them, never from the band's own fill.
 */
export function Section({ id, children, className = '' }) {
  const reveal = useReveal()

  return (
    <section id={id} className={className}>
      <div ref={reveal} className="mx-auto w-full max-w-[84rem] px-5 sm:px-8 lg:px-14">
        {children}
      </div>
    </section>
  )
}

export function Eyebrow({ icon: Icon, children, className = '' }) {
  return (
    <span className={`eyebrow w-fit self-start ${className}`}>
      {Icon && (
        <span className="flex h-5 w-5 items-center justify-center rounded-full bg-surface">
          <Icon size={12} strokeWidth={2} aria-hidden="true" />
        </span>
      )}
      {children}
    </span>
  )
}

/** Every section is the same three-part shape: eyebrow, H2, one paragraph. */
export function SectionHead({ icon, eyebrow, title, lead, align = 'left', className = '' }) {
  const centered = align === 'center'
  return (
    <header
      data-reveal
      className={`${centered ? 'mx-auto max-w-3xl text-center' : 'max-w-3xl'} ${className}`}
    >
      {eyebrow && (
        <Eyebrow icon={icon} className={centered ? 'mx-auto self-center' : ''}>
          {eyebrow}
        </Eyebrow>
      )}
      <h2 className="mt-6 text-[clamp(2rem,4.2vw,3rem)] text-ink">
        {title}
      </h2>
      {lead && (
        <p
          className={`mt-5 text-[1.0625rem] leading-[1.62] text-ink-2 ${
            centered ? 'mx-auto max-w-2xl' : ''
          }`}
        >
          {lead}
        </p>
      )}
    </header>
  )
}

/**
 * Background comes from `tone`, never from className — two competing bg-*
 * utilities would be resolved by stylesheet order rather than by intent.
 *
 * Elevation, not lightness. Each of these says how far off the field the
 * surface sits, and the field decides what that means at this scroll position.
 */
const cardTones = {
  card: 'bg-surface', // the default: a card standing on the field
  panel: 'bg-surface-2', // a panel nested inside a card
  sunk: 'bg-surface-3', // a well cut into the field
  lime: 'bg-lime',
}

export function Card({
  children,
  className = '',
  hover = true,
  tone = 'card',
  as: Tag = 'div',
  ...props
}) {
  return (
    <Tag
      className={`rounded-lg shadow-card ${cardTones[tone] ?? cardTones.card} ${hover ? 'card-hover' : ''} ${className}`}
      {...props}
    >
      {children}
    </Tag>
  )
}

/**
 * The label is rendered twice so it can roll on hover. Both copies carry the
 * same string, so screen readers get one accessible name via aria-label and
 * the duplicate is hidden from the tree.
 */
export function Button({
  as: Tag = 'button',
  variant = 'dark',
  className = '',
  children,
  icon: Icon,
  ...props
}) {
  const base =
    'group press inline-flex cursor-pointer items-center justify-center gap-2.5 rounded-full text-[0.9375rem] font-semibold transition-colors duration-200 ease-[cubic-bezier(0.4,0,0.2,1)]'
  /*
    No `onDark` variant. `dark` is bg-btn / text-on-btn, which is already the
    inverse of the field at every scroll position — there is no separate dark
    ground for it to answer to.
  */
  const variants = {
    dark: 'bg-btn text-on-btn hover:opacity-90 py-3.5 px-7',
    lime: 'bg-lime text-on-accent hover:bg-lime-2 py-3.5 px-7',
    outline: 'border border-line-2 text-ink hover:bg-surface-2 py-3.5 px-7',
  }

  return (
    <Tag
      className={`${base} ${variants[variant]} ${className}`}
      aria-label={typeof children === 'string' ? children : undefined}
      {...props}
    >
      {Icon && (
        <span className="flex h-8 w-8 items-center justify-center rounded-full bg-lime text-on-accent transition-transform duration-500 ease-[cubic-bezier(0.22,1,0.36,1)] group-hover:translate-x-0.5">
          <Icon size={15} strokeWidth={2.4} aria-hidden="true" />
        </span>
      )}
      <span className="roll" aria-hidden={typeof children === 'string' ? 'true' : undefined}>
        <span>{children}</span>
        <span>{children}</span>
      </span>
    </Tag>
  )
}

/** Big numeral with a small grey unit riding alongside it. */
export function Figure({ value, unit, className = '', numeralRef }) {
  return (
    <p className={`figure ${className}`}>
      <span ref={numeralRef}>{value}</span>
      {unit && <span className="figure-unit">{unit}</span>}
    </p>
  )
}

export function Delta({ value, positive = true }) {
  return (
    <span
      className={`inline-flex items-center rounded-full px-2.5 py-1 text-xs font-semibold ${
        positive ? 'bg-positive-wash text-positive' : 'bg-alert-wash text-alert'
      }`}
    >
      {value}
    </span>
  )
}
