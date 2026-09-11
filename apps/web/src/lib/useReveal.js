import { useEffect, useRef } from 'react'

/**
 * Reveals an element (and optionally its children, staggered) when it scrolls
 * into view. Elements carry `.reveal` and gain `.is-in`; children opt in with
 * a `data-reveal` attribute.
 *
 * Nothing is hidden when the user prefers reduced motion, and nothing is
 * hidden without JS — `.reveal` is only applied by this hook.
 *
 * `selector` exists for nesting: a `Section` already sweeps every
 * `[data-reveal]` under it once, on mount. A group that wants its OWN
 * independent stagger and its own "only once this group is in view" timing
 * — rather than being caught in the section's single flat sweep and
 * overwritten with a much later delay — opts its children into a different
 * attribute instead, so the two observers never touch the same elements.
 */
export function useReveal({ stagger = 80, selector = '[data-reveal]' } = {}) {
  const ref = useRef(null)

  useEffect(() => {
    const root = ref.current
    if (!root) return

    if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) return

    const targets = root.matches(selector) ? [root] : Array.from(root.querySelectorAll(selector))
    if (!targets.length) return

    targets.forEach((el, i) => {
      // .line-mask brings its own hidden state; everything else gets .reveal.
      if (!el.classList.contains('line-mask')) el.classList.add('reveal')
      el.style.setProperty('--reveal-delay', `${i * stagger}ms`)
    })

    /*
      Fire when the element's top reaches ~85% of viewport height, so the
      motion finishes exactly as the element settles into reading position.
      Triggering at 100% runs it off-screen; at 50% the user watches it sit
      still and then perform.
    */
    const observer = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (!entry.isIntersecting) return
          entry.target.classList.add('is-in')
          observer.unobserve(entry.target) // play once, never on scroll-up
        })
      },
      { threshold: 0, rootMargin: '0px 0px -15% 0px' },
    )

    targets.forEach((el) => observer.observe(el))
    return () => observer.disconnect()
  }, [stagger, selector])

  return ref
}

/** Counts a number up once it enters view. Returns [ref, displayValue]. */
export function useCountUp(target, { duration = 1400, decimals = 0 } = {}) {
  const ref = useRef(null)
  const valueRef = useRef(null)

  useEffect(() => {
    const el = ref.current
    const out = valueRef.current
    if (!el || !out) return

    const settle = () => {
      out.textContent = target.toFixed(decimals)
    }

    if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
      settle()
      return
    }

    let frame
    const observer = new IntersectionObserver(
      (entries) => {
        if (!entries[0].isIntersecting) return
        observer.disconnect()
        const start = performance.now()
        const tick = (now) => {
          const p = Math.min((now - start) / duration, 1)
          // expo.out, matching the CSS easing
          const eased = p === 1 ? 1 : 1 - Math.pow(2, -10 * p)
          out.textContent = (target * eased).toFixed(decimals)
          if (p < 1) frame = requestAnimationFrame(tick)
        }
        frame = requestAnimationFrame(tick)
      },
      { threshold: 0.4 },
    )

    observer.observe(el)
    return () => {
      observer.disconnect()
      cancelAnimationFrame(frame)
    }
  }, [target, duration, decimals])

  return [ref, valueRef]
}
