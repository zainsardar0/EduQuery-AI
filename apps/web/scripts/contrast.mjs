/*
  Measures the colour field's text contrast across the whole scroll range.

  The page darkens continuously from near-white to near-black, so every text
  token has to stay legible on every surface token at every value of --p. The
  tokens are color-mix(in oklab, …) chains, which nothing outside a browser can
  resolve, so this drives a real Chromium: it sets --p / --e / --b / --tp on the
  document, reads the computed colours back, and rasterises each one through a
  1x1 canvas to get true sRGB bytes (getComputedStyle hands back oklab() text,
  which is not parseable as RGB).

  Run the dev server first, then:  node scripts/contrast.mjs

  The p → (e, b, tp) curves below mirror useScrollProgress. They are duplicated
  rather than imported on purpose: this is a check, and a check that shares its
  arithmetic with the thing it checks proves nothing about the arithmetic.
*/
import { chromium } from 'playwright'

const URL = process.env.URL ?? 'http://localhost:5200/'
const PIVOT = 0.6379
const clamp01 = (n) => (n < 0 ? 0 : n > 1 ? 1 : n)
const smootherstep = (t) => {
  const x = clamp01(t)
  return x * x * x * (x * (x * 6 - 15) + 10)
}

const browser = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium' })
const page = await (await browser.newContext({ viewport: { width: 1440, height: 900 } })).newPage()
await page.goto(URL, { waitUntil: 'networkidle' })
// --tp is transitioned on <html>, so a value set and read in the same task
// still reads as the old one. Static contrast is what WCAG measures anyway.
await page.addStyleTag({ content: 'html{transition:none !important}' })

const GROUNDS = ['canvas', 'surface', 'surface-2', 'surface-3']
const TEXTS = ['ink', 'ink-2', 'ink-3', 'positive', 'alert']
/* Pills carry their own ground, so they are checked as pairs rather than
   against the page's surfaces. */
const PAIRS = [
  ['positive', 'positive-wash'],
  ['alert', 'alert-wash'],
  ['on-accent', 'lime'],
  ['lime/ink', 'lime'],
  ['lime/ink-2', 'lime'],
  ['lime/ink-3', 'lime'],
  ['on-btn', 'btn'],
]
const EXTRA = [...new Set(PAIRS.flat())].filter((n) => !n.startsWith('lime/'))

const samples = await page.evaluate(
  ({ grounds, texts, extra, states }) => {
    const cv = document.createElement('canvas')
    cv.width = cv.height = 1
    const ctx = cv.getContext('2d', { willReadFrequently: true })
    const probe = document.createElement('div')
    document.body.appendChild(probe)
    // A second probe scoped inside the accent surface, which re-anchors the
    // ink tokens for its descendants.
    const accent = document.createElement('div')
    accent.className = 'bg-lime'
    const probeAccent = document.createElement('div')
    accent.appendChild(probeAccent)
    document.body.appendChild(accent)
    const pxIn = (el, expr) => {
      el.style.color = expr
      ctx.clearRect(0, 0, 1, 1)
      ctx.fillStyle = getComputedStyle(el).color
      ctx.fillRect(0, 0, 1, 1)
      const d = ctx.getImageData(0, 0, 1, 1).data
      return [d[0], d[1], d[2]]
    }
    const onAccent = (expr) => pxIn(probeAccent, expr)
    const px = (expr) => {
      probe.style.color = expr
      ctx.clearRect(0, 0, 1, 1)
      ctx.fillStyle = getComputedStyle(probe).color
      ctx.fillRect(0, 0, 1, 1)
      const d = ctx.getImageData(0, 0, 1, 1).data
      return [d[0], d[1], d[2]]
    }
    const root = document.documentElement
    const out = []
    for (const s of states) {
      root.style.setProperty('--p', s.p)
      root.style.setProperty('--e', s.e)
      root.style.setProperty('--b', s.b)
      root.style.setProperty('--tp', s.tp)
      const row = { ...s, c: {} }
      for (const n of [...grounds, ...texts, ...extra]) row.c[n] = px(`var(--color-${n})`)
      for (const n of ['ink', 'ink-2', 'ink-3']) row.c['lime/' + n] = onAccent(`var(--color-${n})`)
      out.push(row)
    }
    probe.remove()
    accent.remove()
    for (const k of ['--p', '--e', '--b', '--tp']) root.style.removeProperty(k)
    return out
  },
  {
    grounds: GROUNDS,
    texts: TEXTS,
    extra: EXTRA,
    states: Array.from({ length: 501 }, (_, i) => {
      const p = i / 500
      const d = Math.abs(p - PIVOT)
      return {
        p: p.toFixed(4),
        e: (p < PIVOT
          ? smootherstep((PIVOT - p - 0.028) / 0.09)
          : smootherstep((p - PIVOT - 0.014) / 0.16)
        ).toFixed(4),
        b: (1 - smootherstep((d - 0.03) / 0.42)).toFixed(4),
        tp: p > PIVOT ? 1 : 0,
      }
    }),
  }
)

const lum = ([r, g, b]) => {
  const f = (v) => ((v /= 255), v <= 0.03928 ? v / 12.92 : ((v + 0.055) / 1.055) ** 2.4)
  return 0.2126 * f(r) + 0.7152 * f(g) + 0.0722 * f(b)
}
const ratio = (a, b) => {
  const [hi, lo] = [lum(a), lum(b)].sort((m, n) => n - m)
  return (hi + 0.05) / (lo + 0.05)
}
const hex = (c) => '#' + c.map((v) => v.toString(16).padStart(2, '0')).join('')

/*
  WCAG AA is 4.5:1 for body copy and 3:1 for large text. Every tier is held to
  4.5 here, including ink-3: it is used for 12px uppercase micro-labels, which
  is small text by any reading, so the large-text allowance does not apply.
*/
const FLOOR = { ink: 4.5, 'ink-2': 4.5, 'ink-3': 4.5, positive: 4.5, alert: 4.5 }
const worst = {}
for (const t of TEXTS) worst[t] = { r: Infinity }

for (const row of samples) {
  for (const t of TEXTS) {
    for (const g of GROUNDS) {
      const r = ratio(row.c[t], row.c[g])
      if (r < worst[t].r) worst[t] = { r, g, p: row.p, tp: row.tp, fg: row.c[t], bg: row.c[g] }
    }
  }
}

console.log('field sampled at 501 points, p = 0 … 1\n')
console.log('p       tp  canvas   surface  ink      ink-2    ink-3    | ink/surf ink2/surf ink3/surf')
for (let i = 0; i < samples.length; i += 25) {
  const r = samples[i]
  console.log(
    `${r.p}  ${r.tp}   ${hex(r.c.canvas)}  ${hex(r.c.surface)}  ${hex(r.c.ink)}  ` +
      `${hex(r.c['ink-2'])}  ${hex(r.c['ink-3'])}  | ` +
      [`ink`, `ink-2`, `ink-3`]
        .map((t) => ratio(r.c[t], r.c.surface).toFixed(2).padStart(8))
        .join(' ')
  )
}

console.log('\nworst case over every text token against every ground:')
let ok = true
for (const t of TEXTS) {
  const w = worst[t]
  const pass = w.r >= FLOOR[t]
  ok &&= pass
  console.log(
    `  ${t.padEnd(6)} ${w.r.toFixed(2)}:1  ${hex(w.fg)} on ${hex(w.bg)} (${w.g}) at p=${w.p}` +
      `  — floor ${FLOOR[t]}:1  ${pass ? 'PASS' : 'FAIL'}`
  )
}
console.log('\nself-contained pairs (a token on its own ground):')
for (const [fg, bg] of PAIRS) {
  let w = { r: Infinity }
  for (const row of samples) {
    const r = ratio(row.c[fg], row.c[bg])
    if (r < w.r) w = { r, p: row.p, fg: row.c[fg], bg: row.c[bg] }
  }
  const pass = w.r >= 4.5
  ok &&= pass
  console.log(
    `  ${(fg + ' on ' + bg).padEnd(24)} ${w.r.toFixed(2)}:1  ${hex(w.fg)} on ${hex(w.bg)}` +
      ` at p=${w.p}  ${pass ? 'PASS' : 'FAIL'}`
  )
}

console.log(ok ? '\nEverything clears 4.5:1 at every scroll position.' : '\nFAILED')
await browser.close()
process.exit(ok ? 0 : 1)
