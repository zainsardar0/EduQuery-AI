import { useState, useEffect } from 'react'
import { LayoutDashboard, MessagesSquare, FileText, Database, Shield, X } from 'lucide-react'
import Logo from '../components/Logo'

const NAV = [
  { id: 'dashboard', label: 'Overview Dashboard', icon: LayoutDashboard },
  { id: 'chatbot', label: 'AI Intelligence Assistant', icon: MessagesSquare },
]

export default function Sidebar({ route, onNavigate, mobileOpen, onCloseMobile }) {
  const [online, setOnline] = useState(true)

  useEffect(() => {
    fetch('/health')
      .then((res) => res.ok ? setOnline(true) : setOnline(false))
      .catch(() => setOnline(false))
  }, [])

  return (
    <>
      {/* Mobile Backdrop */}
      {mobileOpen && (
        <div
          className="fixed inset-0 z-40 bg-ink/40 backdrop-blur-xs lg:hidden"
          onClick={onCloseMobile}
          aria-hidden="true"
        />
      )}

      <aside
        className={`fixed inset-y-0 left-0 z-50 flex h-dvh w-64 shrink-0 flex-col bg-panel px-4 py-6 transition-transform duration-300 ease-[cubic-bezier(0.22,1,0.36,1)] lg:sticky lg:top-0 lg:translate-x-0 ${
          mobileOpen ? 'translate-x-0' : '-translate-x-full'
        }`}
      >
        <div className="flex items-center justify-between px-2">
          <Logo light />
          <button
            onClick={onCloseMobile}
            aria-label="Close menu"
            className="press flex h-8 w-8 cursor-pointer items-center justify-center rounded-full text-on-panel-2 hover:bg-panel-2 hover:text-on-panel lg:hidden"
          >
            <X size={16} strokeWidth={2} aria-hidden="true" />
          </button>
        </div>

        <nav className="mt-8 flex flex-col gap-1.5">
          {NAV.map((item) => {
            const active = route === item.id
            const Icon = item.icon
            return (
              <button
                key={item.id}
                onClick={() => {
                  onNavigate(item.id)
                  onCloseMobile?.()
                }}
                aria-current={active ? 'page' : undefined}
                className={`press flex cursor-pointer items-center gap-3 rounded-xl px-3.5 py-2.5 text-left text-sm font-medium transition-all duration-200 ${
                  active
                    ? 'bg-panel-2 text-on-panel shadow-xs'
                    : 'text-on-panel-2 hover:bg-panel-2/50 hover:text-on-panel'
                }`}
              >
                <Icon size={17} strokeWidth={2.2} aria-hidden="true" />
                {item.label}
              </button>
            )
          })}
        </nav>

        {/* Engine Capability Quick Badges */}
        <div className="mt-6 border-t border-panel-line pt-5 px-2">
          <p className="text-[0.625rem] font-semibold uppercase tracking-wider text-on-panel-2/60">
            Active Engines
          </p>
          <div className="mt-2.5 space-y-2 text-xs text-on-panel-2">
            <div className="flex items-center gap-2">
              <span className="h-1.5 w-1.5 rounded-full bg-emerald-400"></span>
              <span className="text-[0.75rem]">WrenAI NL2SQL (Live DB)</span>
            </div>
            <div className="flex items-center gap-2">
              <span className="h-1.5 w-1.5 rounded-full bg-amber-400"></span>
              <span className="text-[0.75rem]">Gemini Policy RAG</span>
            </div>
            <div className="flex items-center gap-2">
              <span className="h-1.5 w-1.5 rounded-full bg-purple-400"></span>
              <span className="text-[0.75rem]">Predictive AI & SHAP</span>
            </div>
          </div>
        </div>

        {/* Audit & Compliance Footer */}
        <div className="mt-auto rounded-xl border border-panel-line bg-panel-2/30 p-3.5">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-1.5">
              <Shield size={13} className="text-emerald-400" />
              <span className="text-xs font-semibold text-on-panel">Governed Audit Trail</span>
            </div>
            <span className={`inline-block h-2 w-2 rounded-full ${online ? 'bg-emerald-400 animate-pulse' : 'bg-rose-400'}`} />
          </div>
          <p className="mt-1.5 text-[0.6875rem] leading-relaxed text-on-panel-2">
            Read-only MSSQL enforcement. No PII or raw student identities leave institutional perimeter.
          </p>
        </div>
      </aside>
    </>
  )
}
