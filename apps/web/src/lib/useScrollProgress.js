import { useEffect } from 'react'

/**
 * Drives the page's single continuous colour field.
 *
 * There are no light sections and no dark sections. There is one field whose
 * colour evolves with scroll position, and every band simply sits on whatever
 * that colour currently is. This hook publishes the progress; the stylesheet
 * turns it into colour by redefining the design tokens themselves, so every
 * existing utility follows automatically. The long note in index.css explains
 * what each variable is for — this file only says how they are computed.
 */

const clamp01 = (n) => (n < 0 ? 0 : n > 1 ? 1 : n)

/* Zero first AND second derivative at both ends. Plain smoothstep leaves a
   perceptible knee where the ramp meets the flat colour at either end. */
const smootherstep = (t) => {
  const x = clamp01(t)
  return x * x * x * (x * (x * 6 - 15) + 10)
}

/*
  The field's own ramp — color-mix(in oklab, #f4f5f8, #34363c p%) — passes
  relative luminance 0.179 at p = 0.6379. That is the luminance where pure
  black and pure white are equally legible (4.58:1 each), so it is where the
  text has to change poles. Recompute this if either field endpoint moves:
  scripts/pivot.mjs prints it.
*/
const PIVOT = 0.6379

/*
  The entry and exit edges of the mesa — deliberately narrow. Any continuous
  blend between an off-white and a charcoal has to pass through the full grey
  continuum in between; that is arithmetic, not a tuning choice, and no width
  here makes it stop being true. What width DOES control is how long that
  continuum stays on screen. At 0.05 the field is fully dark by raw ≈ 0.07 —
  the pivot crossing (where the field is genuinely grey, see PIVOT above)
  lands at raw ≈ 0.05, roughly a third of the page's earlier timing — so a
  normal scroll gesture crosses the whole grey range in a handful of frames.
  It reads as a decisive blend rather than a fade specifically because it is
  short, not because the grey has been removed; grey pixels are still what
  briefly render, just briefly. Exit mirrors it, ending at EXIT_END so the
  reader is back in daylight before the footer, not still mid-fade there.
*/
const ENTRY_HOLD = 0.02
const ENTRY_WIDTH = 0.05
const EXIT_END = 0.985
const EXIT_WIDTH = 0.05

/*
  Elevation holds at zero across the pivot, then returns — much later on the
  dark side than on the light one. That asymmetry is not taste: a card is
  lighter than the field, and on a dark ground a lighter surface is the one
  that fails first, so elevation has to wait until the field is deep enough to
  carry it. The numbers are the ones scripts/contrast.mjs stops complaining at.
*/
const HOLD_LIGHT = 0.028
const RISE_LIGHT = 0.09
const HOLD_DARK = 0.014
const RISE_DARK = 0.16

/*
  Contrast boost: full within 0.03 of the pivot, with a long gentle skirt.
  It has to be long. A mid-grey ground caps the total contrast available to
  ALL text at about 7.5:1, so the three text tiers cannot each hold 4.5:1 out
  there unless they converge — the boost is what closes the gaps as the budget
  shrinks, and re-opens them at both ends where there is room again.
*/
const BOOST_HOLD = 0.03
const BOOST_RISE = 0.42

/* Dead zone for the text flip. Wide enough that a hand resting on a trackpad
   cannot oscillate the polarity, narrow enough that both edges are still
   inside the band where either pole clears 4.5:1. */
const SNAP = 0.004

/*
  The ambient video's own visibility window — a trapezoid, independent of the
  colour pivot on purpose. The pivot is a single narrow instant (arithmetic:
  where the field's luminance crosses 0.179); the video's job is narrative,
  "the reader is leaving the hero and entering the dark experience", which is
  a broader FEEL rather than a point. Tying it to --e would mean it is almost
  fully faded by the time it is actually on screen, since the pivot crossing
  now lands within the hero's own scroll range (see ENTRY_WIDTH above) — long
  before the video's layer, sitting below Marquee, ever scrolls into view.
  This window is tuned by hand to the page's actual geometry (scripts/*.mjs
  measurements): fade in as the hero ends, hold through Marquee and the start
  of Manifesto, fade out before Problem.
*/
const VIDEO_IN_START = 0.05
const VIDEO_IN_END = 0.09
const VIDEO_OUT_START = 0.14
const VIDEO_OUT_END = 0.19

export function useScrollProgress(active = true) {
  useEffect(() => {
    const root = document.documentElement

    const clear = () => {
      for (const k of ['--p', '--e', '--b', '--tp', '--video-op']) root.style.removeProperty(k)
    }

    if (!active) {
      clear()
      return
    }

    let polarity = 0

    const update = () => {
      const max = root.scrollHeight - window.innerHeight
      // Measure from the middle of the viewport: the colour should answer to
      // what the reader is looking at, not to where the page edge happens to be.
      const raw =
        max > 0 ? clamp01((window.scrollY + window.innerHeight * 0.5) / (max + window.innerHeight)) : 0

      /*
        A mesa, not a ramp: light → dark quickly, hold dark through the whole
        middle of the page, then light again before the page ends. Two
        independent smootherstep edges, combined with min() — early on the
        rise edge is the binding constraint (0 → 1), for the entire middle
        both edges are past 1 so p pins at 1, and near the end the fall edge
        becomes binding (1 → 0). Nothing about the pivot/elevation/boost logic
        below cares which direction p is moving — it is pure position, not
        velocity — so the exact same crossing behaviour that used to happen
        once, going into dark, now happens a second time, symmetrically,
        coming back out of it.
      */
      const riseEdge = smootherstep((raw - ENTRY_HOLD) / ENTRY_WIDTH)
      const fallEdge = smootherstep((EXIT_END - raw) / EXIT_WIDTH)
      const p = Math.min(riseEdge, fallEdge)

      // Elevation collapses onto the field across the pivot, so every surface
      // crosses it at the same instant rather than one after another.
      const e =
        p < PIVOT
          ? smootherstep((PIVOT - p - HOLD_LIGHT) / RISE_LIGHT)
          : smootherstep((p - PIVOT - HOLD_DARK) / RISE_DARK)

      // Ink opens to true black / true white where the ground is least
      // forgiving, and secondary copy closes up to full ink strength.
      const b = 1 - smootherstep((Math.abs(p - PIVOT) - BOOST_HOLD) / BOOST_RISE)

      // Discrete, with hysteresis. A crossfade here would pass through 1:1 —
      // see the topology note in index.css.
      if (p > PIVOT + SNAP) polarity = 1
      else if (p < PIVOT - SNAP) polarity = 0

      const videoIn = smootherstep((raw - VIDEO_IN_START) / (VIDEO_IN_END - VIDEO_IN_START))
      const videoOut = 1 - smootherstep((raw - VIDEO_OUT_START) / (VIDEO_OUT_END - VIDEO_OUT_START))
      const videoOp = Math.min(videoIn, videoOut)

      root.style.setProperty('--p', p.toFixed(4))
      root.style.setProperty('--e', e.toFixed(4))
      root.style.setProperty('--b', b.toFixed(4))
      root.style.setProperty('--tp', polarity)
      root.style.setProperty('--video-op', videoOp.toFixed(4))
    }

    let frame = 0
    const onScroll = () => {
      if (frame) return
      frame = requestAnimationFrame(() => {
        frame = 0
        update()
      })
    }

    update()
    window.addEventListener('scroll', onScroll, { passive: true })
    window.addEventListener('resize', onScroll)
    // Reveals change document height as they fire, which moves the denominator.
    const ro = new ResizeObserver(onScroll)
    ro.observe(document.body)

    return () => {
      cancelAnimationFrame(frame)
      window.removeEventListener('scroll', onScroll)
      window.removeEventListener('resize', onScroll)
      ro.disconnect()
      clear()
    }
  }, [active])
}
