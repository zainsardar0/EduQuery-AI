import { useEffect, useRef, useState } from 'react'

/**
 * True once, the first time the element crosses into view, and never again —
 * for gating a chart's mount so its own entrance animation plays exactly when
 * the reader scrolls to it, not at page load off-screen.
 */
export function useInViewOnce({ threshold = 0.35 } = {}) {
  const ref = useRef(null)
  const [inView, setInView] = useState(false)

  useEffect(() => {
    const el = ref.current
    if (!el) return

    if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
      setInView(true)
      return
    }

    const observer = new IntersectionObserver(
      (entries) => {
        if (!entries[0].isIntersecting) return
        setInView(true)
        observer.disconnect()
      },
      { threshold },
    )
    observer.observe(el)
    return () => observer.disconnect()
  }, [threshold])

  return [ref, inView]
}
