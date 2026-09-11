// Where does each surface ramp cross the "dead band" — the luminance range in
// which neither near-black nor near-white text reaches 4.5:1?
//   dark  #000 needs L >= 0.1750 ; light #fff needs L <= 0.1833  (4.5:1)
// The equal-contrast pivot for pure black/white is L = 0.1791 (4.58:1 both ways).
import { chromium } from 'playwright'

const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium' })
const page = await (await b.newContext()).newPage()
await page.setContent('<div id="probe"></div>')

const ramps = {
  field: ['#f4f5f8', '#34363c'],
  'lift-1': ['#ffffff', '#45474e'],
  'lift-2': ['#f7f8fa', '#3c3e44'],
  'lift-3': ['#e4e7ec', '#2a2c31'],
}

const data = await page.evaluate((ramps) => {
  const cv = document.createElement('canvas')
  cv.width = cv.height = 1
  const ctx = cv.getContext('2d', { willReadFrequently: true })
  const probe = document.getElementById('probe')
  const px = (expr) => {
    probe.style.color = expr
    ctx.clearRect(0, 0, 1, 1)
    ctx.fillStyle = getComputedStyle(probe).color
    ctx.fillRect(0, 0, 1, 1)
    const d = ctx.getImageData(0, 0, 1, 1).data
    return [d[0], d[1], d[2]]
  }
  const out = {}
  for (const [name, [a, z]] of Object.entries(ramps)) {
    out[name] = []
    for (let i = 0; i <= 200; i++) {
      const p = i / 200
      out[name].push([p, px(`color-mix(in oklab, ${a}, ${z} ${(p * 100).toFixed(2)}%)`)])
    }
  }
  return out
}, ramps)

const lum = ([r, g, bl]) => {
  const f = (v) => ((v /= 255), v <= 0.03928 ? v / 12.92 : ((v + 0.055) / 1.055) ** 2.4)
  return 0.2126 * f(r) + 0.7152 * f(g) + 0.0722 * f(bl)
}
const cross = (rows, target) => {
  for (let i = 1; i < rows.length; i++) {
    const a = lum(rows[i - 1][1]),
      c = lum(rows[i][1])
    if (a >= target && c <= target) {
      const t = (a - target) / (a - c)
      return rows[i - 1][0] + t * (rows[i][0] - rows[i - 1][0])
    }
  }
  return NaN
}

for (const [name, rows] of Object.entries(data)) {
  console.log(
    `${name.padEnd(9)} enters band p=${cross(rows, 0.1833).toFixed(4)}  ` +
      `pivot p=${cross(rows, 0.1791).toFixed(4)}  ` +
      `leaves band p=${cross(rows, 0.175).toFixed(4)}`
  )
}
await b.close()
