import { useState } from 'react'
import {
  ArrowLeft,
  ArrowRight,
  GraduationCap,
  Lock,
  MessageSquareText,
  ShieldCheck,
  TrendingUp,
  Users,
} from 'lucide-react'
import Logo from '../components/Logo'
import { FloatingField } from './FloatingField'
import { useReveal } from '../lib/useReveal'
import { meta } from '../lib/content'

/*
  The entrance to the product, not a marketing band — so it does not ride the
  scroll field. useScrollProgress is inactive on this route (see App.jsx),
  which leaves every token at its light-mode value; the left panel is the one
  deliberately fixed-dark surface, an immersive still rather than a section of
  the page.
*/

const features = [
  { icon: MessageSquareText, text: 'Ask academic questions in natural language.' },
  { icon: TrendingUp, text: 'Predict student performance using AI.' },
  { icon: ShieldCheck, text: 'Explore institutional analytics securely.' },
  { icon: Users, text: 'Role-based access for teachers, principals and administrators.' },
]

const roles = ['Teacher', 'Principal', 'Administrator', 'IT Staff']

const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/

export default function LoginPage({ onBack, onSignedIn }) {
  const reveal = useReveal({ stagger: 70 })
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [remember, setRemember] = useState(true)
  const [errors, setErrors] = useState({})
  const [status, setStatus] = useState('idle') // idle | loading | success

  const submit = (e) => {
    e.preventDefault()
    if (status === 'loading') return

    const next = {}
    if (!emailPattern.test(email)) next.email = 'Enter a valid institutional email address.'
    if (password.length < 8) next.password = 'Password must be at least 8 characters.'
    setErrors(next)
    if (Object.keys(next).length) return

    setStatus('loading')
    // No backend in this mockup — the delay and the redirect are what a real
    // sign-in would do, not a fabricated success. See the docs before wiring
    // this to a real auth provider.
    window.setTimeout(() => {
      setStatus('success')
      window.setTimeout(() => onSignedIn?.(), 500)
    }, 900)
  }

  return (
    <div ref={reveal} className="min-h-screen bg-canvas lg:flex">
      {/* Left: immersive, dark, fixed. Hidden below lg per the responsive spec. */}
      <div className="relative hidden overflow-hidden bg-[#0a0a0a] lg:flex lg:w-[55%] lg:items-center lg:justify-center">
        <div className="auth-orb h-[28rem] w-[28rem] bg-accent-sky/25" style={{ top: '-6rem', left: '-4rem' }} />
        <div
          className="auth-orb h-[24rem] w-[24rem] bg-accent-peach/20"
          style={{ bottom: '-4rem', right: '-2rem', animationDelay: '-7s' }}
        />
        <div
          className="auth-orb h-[20rem] w-[20rem] bg-accent-mauve/20"
          style={{ top: '40%', left: '50%', animationDelay: '-14s' }}
        />
        <div
          className="pointer-events-none absolute inset-0"
          style={{
            backgroundImage:
              'radial-gradient(rgba(255,255,255,0.08) 1px, transparent 1px)',
            backgroundSize: '28px 28px',
            maskImage: 'radial-gradient(ellipse at center, black, transparent 75%)',
          }}
          aria-hidden="true"
        />
        <div className="pointer-events-none absolute inset-0 bg-gradient-to-b from-black/10 via-black/40 to-black/70" />

        <div
          data-reveal
          className="relative m-10 w-full max-w-md rounded-2xl border border-white/10 bg-white/[0.04] p-10 shadow-[0_32px_80px_-24px_rgba(0,0,0,0.6)] backdrop-blur-2xl"
        >
          <Logo light />
          <h1 className="mt-8 text-[1.75rem] font-medium text-white">Welcome to EduQuery AI</h1>
          <p className="mt-3 text-[0.9375rem] leading-relaxed text-white/60">
            Secure access to intelligent educational analytics, AI-powered insights, and
            predictive academic reporting.
          </p>

          <ul className="mt-8 space-y-4">
            {features.map((f) => (
              <li key={f.text} className="flex items-start gap-3">
                <span className="flex h-8 w-8 shrink-0 items-center justify-center rounded-full bg-white/[0.06] text-accent-sky">
                  <f.icon size={15} strokeWidth={2} aria-hidden="true" />
                </span>
                <span className="mt-1.5 text-sm leading-relaxed text-white/70">{f.text}</span>
              </li>
            ))}
          </ul>

          <p className="mt-9 flex items-center gap-2 border-t border-white/10 pt-6 text-xs text-white/45">
            <Lock size={13} strokeWidth={2} aria-hidden="true" />
            Protected with enterprise-grade authentication and role-based access control.
          </p>
        </div>
      </div>

      {/*
        Right: the auth card, light theme. It used to be form controls sitting
        directly on bg-canvas with no container of their own — reads as an
        unfinished page next to the immersive left panel rather than a
        composed one. A soft ambient tint plus an actual elevated card (the
        same shadow-lift/border-line vocabulary the rest of the site uses)
        gives it the weight the left panel already has.
      */}
      <div className="relative flex flex-1 items-center justify-center overflow-hidden px-6 py-14 sm:px-10">
        <div
          className="pointer-events-none absolute -top-24 -right-24 h-96 w-96 rounded-full bg-accent-sky/25 blur-3xl"
          aria-hidden="true"
        />
        <div
          className="pointer-events-none absolute -bottom-32 -left-16 h-80 w-80 rounded-full bg-accent-peach/20 blur-3xl"
          aria-hidden="true"
        />

        <div data-reveal className="relative w-full max-w-[460px]">
          <button
            onClick={onBack}
            className="press mb-7 inline-flex cursor-pointer items-center gap-1.5 text-sm font-medium text-ink-2 transition-colors hover:text-ink"
          >
            <ArrowLeft size={15} strokeWidth={2.2} aria-hidden="true" />
            Back to site
          </button>

          <div className="mb-7 lg:hidden">
            <Logo />
          </div>

          <div className="rounded-2xl border border-line bg-surface p-9 shadow-lift sm:p-11">
            <span className="block h-9 w-1 rounded-full bg-accent-sky-deep" aria-hidden="true" />
            <h2 className="mt-5 text-[2rem] tracking-[-0.02em] text-ink">Welcome back</h2>
            <p className="mt-2.5 text-[0.9375rem] leading-relaxed text-ink-2">
              Sign in to continue to your institutional dashboard.
            </p>

            <form onSubmit={submit} noValidate className="mt-9 space-y-5">
              <FloatingField
                id="email"
                label="Institution email"
                type="email"
                autoComplete="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                error={errors.email}
                disabled={status !== 'idle'}
              />
              <FloatingField
                id="password"
                label="Password"
                type="password"
                autoComplete="current-password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                error={errors.password}
                disabled={status !== 'idle'}
              />

              <div className="flex items-center justify-between pt-1">
                <label className="flex cursor-pointer items-center gap-2.5 text-sm text-ink-2">
                  <input
                    type="checkbox"
                    checked={remember}
                    onChange={(e) => setRemember(e.target.checked)}
                    className="h-4 w-4 rounded border-line-2 text-accent-sky-deep accent-accent-sky-deep focus-visible:outline-2 focus-visible:outline-accent-sky-deep"
                  />
                  Remember me
                </label>
                <a
                  href={`mailto:${meta.contactEmail}?subject=${encodeURIComponent('Password reset request')}`}
                  className="text-sm font-medium text-accent-sky-deep hover:underline"
                >
                  Forgot password?
                </a>
              </div>

              <button
                type="submit"
                disabled={status !== 'idle'}
                className="press flex w-full cursor-pointer items-center justify-center gap-2 rounded-full bg-accent-sky-deep py-3.5 text-[0.9375rem] font-semibold text-white shadow-[0_1px_2px_rgba(58,133,217,0.1),0_16px_32px_-12px_rgba(58,133,217,0.45)] transition-all duration-200 hover:bg-accent-sky-deep-2 disabled:cursor-not-allowed disabled:opacity-80"
              >
                {status === 'idle' && (
                  <>
                    Sign in
                    <ArrowRight size={15} strokeWidth={2.4} aria-hidden="true" />
                  </>
                )}
                {status === 'loading' && (
                  <>
                    <span
                      className="h-4 w-4 animate-spin rounded-full border-2 border-white/30 border-t-white"
                      aria-hidden="true"
                    />
                    Signing in
                  </>
                )}
                {status === 'success' && 'Signed in'}
              </button>

              <a
                href={`mailto:${meta.contactEmail}?subject=${encodeURIComponent('Request access to EduQuery AI')}`}
                className="press block w-full cursor-pointer rounded-full border border-line-2 py-3.5 text-center text-[0.9375rem] font-semibold text-ink transition-colors hover:bg-surface-2"
              >
                Request access
              </a>
            </form>

            <p className="mt-7 text-center text-[0.8125rem] leading-relaxed text-ink-3">
              Need help accessing your account?{' '}
              <span className="text-ink-2">Contact your institution's administrator or IT support.</span>
            </p>
          </div>

          <div className="mt-7 rounded-2xl border border-line bg-surface-2 p-6">
            <p className="flex items-center gap-2 text-xs font-semibold tracking-wide text-ink-3 uppercase">
              <GraduationCap size={13} strokeWidth={2} aria-hidden="true" />
              Authorized roles
            </p>
            <div className="mt-3 flex flex-wrap gap-2">
              {roles.map((r) => (
                <span
                  key={r}
                  className="rounded-full border border-line-2 bg-surface px-3 py-1.5 text-xs font-medium text-ink-2"
                >
                  {r}
                </span>
              ))}
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}
