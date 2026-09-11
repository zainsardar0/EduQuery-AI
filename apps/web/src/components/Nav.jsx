import { useEffect, useState } from 'react'
import { ArrowRight, Menu, X } from 'lucide-react'
import Logo from './Logo'

/* Every label a single common word. No "Solutions", no "Platform". */
const links = [
  { href: '#product', label: 'Product' },
  { href: '#prediction', label: 'Forecasting' },
  { href: '#outcomes', label: 'Outcomes' },
  { href: '#security', label: 'Security' },
]

export default function Nav({ onOpenDemo }) {
  const [scrolled, setScrolled] = useState(false)
  const [open, setOpen] = useState(false)

  useEffect(() => {
    const onScroll = () => setScrolled(window.scrollY > 20)
    onScroll()
    window.addEventListener('scroll', onScroll, { passive: true })
    return () => window.removeEventListener('scroll', onScroll)
  }, [])

  useEffect(() => {
    document.body.style.overflow = open ? 'hidden' : ''
    return () => {
      document.body.style.overflow = ''
    }
  }, [open])

  return (
    <div className="pointer-events-none sticky top-0 z-50 px-3 pt-3 sm:px-4 sm:pt-4">
      <header
        className={`pointer-events-auto mx-auto flex w-full max-w-[84rem] items-center justify-between gap-4 rounded-full bg-surface py-2.5 pr-2.5 pl-5 transition-shadow duration-500 ease-[cubic-bezier(0.16,1,0.3,1)] sm:pl-6 ${
          scrolled ? 'shadow-lift' : 'shadow-card'
        }`}
      >
        <a href="#top" aria-label="EduQuery AI, back to top" className="rounded-full">
          <Logo />
        </a>

        <nav className="hidden items-center gap-1 lg:flex" aria-label="Primary">
          {links.map((l) => (
            <a
              key={l.href}
              href={l.href}
              className="rounded-full px-4 py-2 text-[0.9375rem] font-medium text-ink-2 transition-colors duration-300 ease-[cubic-bezier(0.16,1,0.3,1)] hover:bg-surface-2 hover:text-ink"
            >
              {l.label}
            </a>
          ))}
        </nav>

        <div className="flex items-center gap-2">
          <a
            href="#/login"
            className="hidden rounded-full px-4 py-2 text-[0.9375rem] font-medium text-ink-2 transition-colors duration-300 ease-[cubic-bezier(0.16,1,0.3,1)] hover:bg-surface-2 hover:text-ink sm:inline-flex"
          >
            Sign in
          </a>
          <button
            onClick={onOpenDemo}
            aria-label="Get started"
            className="press group hidden cursor-pointer items-center gap-2.5 rounded-full bg-btn py-2 pr-5 pl-2 text-[0.9375rem] font-semibold text-on-btn transition-all duration-300 ease-[cubic-bezier(0.16,1,0.3,1)] hover:opacity-90 sm:inline-flex"
          >
            <span className="flex h-8 w-8 items-center justify-center rounded-full bg-lime text-on-accent transition-transform duration-500 ease-[cubic-bezier(0.22,1,0.36,1)] group-hover:translate-x-0.5">
              <ArrowRight size={15} strokeWidth={2.4} aria-hidden="true" />
            </span>
            <span className="roll" aria-hidden="true">
              <span>Get started</span>
              <span>Get started</span>
            </span>
          </button>

          <button
            onClick={() => setOpen((v) => !v)}
            className="press flex h-11 w-11 cursor-pointer items-center justify-center rounded-full bg-surface-2 text-ink lg:hidden"
            aria-label={open ? 'Close menu' : 'Open menu'}
            aria-expanded={open}
          >
            {open ? <X size={18} /> : <Menu size={18} />}
          </button>
        </div>
      </header>

      {open && (
        <nav
          className="pointer-events-auto mx-auto mt-2 w-full max-w-[84rem] rounded-lg bg-surface p-3 shadow-lift lg:hidden"
          aria-label="Mobile"
        >
          {links.map((l) => (
            <a
              key={l.href}
              href={l.href}
              onClick={() => setOpen(false)}
              className="block rounded-md px-4 py-3.5 text-base font-medium text-ink-2 hover:bg-surface-2 hover:text-ink"
            >
              {l.label}
            </a>
          ))}
          <a
            href="#/login"
            onClick={() => setOpen(false)}
            className="block rounded-md px-4 py-3.5 text-base font-medium text-ink-2 hover:bg-surface-2 hover:text-ink"
          >
            Sign in
          </a>
          <button
            onClick={() => {
              setOpen(false)
              onOpenDemo()
            }}
            className="press mt-2 w-full cursor-pointer rounded-full bg-btn px-5 py-3.5 text-[0.9375rem] font-semibold text-on-btn"
          >
            Get started
          </button>
        </nav>
      )}
    </div>
  )
}
