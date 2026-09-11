import { ArrowRight } from 'lucide-react'
import { Button } from './ui'
import { finalCta, footerColumns, meta } from '../lib/content'
import { useReveal } from '../lib/useReveal'

export default function Footer({ onOpenDemo }) {
  const reveal = useReveal()

  return (
    <footer id="contact">
      <div ref={reveal}>
        {/* Second type peak: the page closes at the altitude it opened. */}
        <div data-reveal className="glow-sand px-4 pt-6 pb-32 sm:px-6 sm:pt-8 sm:pb-36">
          <div className="mx-auto max-w-[84rem] rounded-lg bg-surface px-6 py-20 text-center sm:px-12 sm:py-28">
            <h2 className="mx-auto max-w-3xl text-[clamp(2rem,4.6vw,3.25rem)] text-ink">
              {finalCta.title}
            </h2>
            <p className="mx-auto mt-6 max-w-xl text-[1.0625rem] leading-[1.62] text-ink-2">
              {finalCta.body}
            </p>
            <div className="mt-10 flex justify-center">
              <Button onClick={onOpenDemo} icon={ArrowRight} className="pl-2.5">
                {finalCta.cta}
              </Button>
            </div>
          </div>
        </div>

      </div>

      {/* Sits on the colour field like every other band. By here the field is
          at its darkest, so the colophon simply reads as dark. */}
      <div className="px-6 pt-16 pb-14 sm:px-12 sm:pt-20 sm:pb-16">
        <div className="mx-auto w-full max-w-[84rem]">
          <div className="grid gap-12 lg:grid-cols-[1.2fr_2fr]">
            {/* Wordmark at hero scale, so the page ends rather than trails off. */}
            <p className="text-[clamp(2.5rem,5vw,3.75rem)] leading-none font-medium tracking-[-0.04em] text-ink">
              {meta.wordmark}
            </p>

            <div className="grid gap-8 sm:grid-cols-2 lg:grid-cols-4">
              {footerColumns.map((col) => (
                <div key={col.heading}>
                  <p className="text-xs font-semibold tracking-wide text-ink-3 uppercase">
                    {col.heading}
                  </p>
                  <ul className="mt-4 space-y-2.5">
                    {col.links.map((l) => (
                      <li key={l}>
                        <a
                          href="#top"
                          className="text-sm text-ink-2 transition-colors duration-200 hover:text-ink"
                        >
                          {l}
                        </a>
                      </li>
                    ))}
                  </ul>
                </div>
              ))}
            </div>
          </div>

          <div className="mt-14 flex flex-col gap-3 border-t border-line pt-8 text-xs text-ink-3 sm:flex-row sm:items-center sm:justify-between">
            <p>
              © {new Date().getFullYear()} {meta.name}. All rights reserved.
            </p>
            <a
              href={`mailto:${meta.contactEmail}`}
              className="transition-colors duration-200 hover:text-ink"
            >
              {meta.contactEmail}
            </a>
          </div>
        </div>
      </div>
    </footer>
  )
}
