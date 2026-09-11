import { useEffect, useRef, useState } from 'react'
import {
  ArrowUp,
  ChevronDown,
  CircleHelp,
  Database,
  FileText,
  TrendingUp,
  Sparkles,
  Copy,
  Check,
  Code2,
  Table as TableIcon,
  BarChart3,
  Layers,
  FileUp,
  Trash2,
  AlertCircle,
  Building2,
  RefreshCw,
  Flag,
  AlertTriangle,
  ThumbsUp,
  ThumbsDown,
  Search
} from 'lucide-react'
import {
  ResponsiveContainer,
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  CartesianGrid,
  Cell
} from 'recharts'
import { chatModes, CAMPUSES } from '../lib/chatData'
import PolicyManagerModal from '../app/PolicyManagerModal'

function ModeSwitcher({ mode, onChange }) {
  const [open, setOpen] = useState(false)
  const ref = useRef(null)

  useEffect(() => {
    if (!open) return
    const onPointerDown = (e) => {
      if (!ref.current?.contains(e.target)) setOpen(false)
    }
    const onKeyDown = (e) => {
      if (e.key === 'Escape') setOpen(false)
    }
    document.addEventListener('pointerdown', onPointerDown)
    document.addEventListener('keydown', onKeyDown)
    return () => {
      document.removeEventListener('pointerdown', onPointerDown)
      document.removeEventListener('keydown', onKeyDown)
    }
  }, [open])

  return (
    <div ref={ref} className="relative inline-block">
      {open && (
        <ul
          role="listbox"
          className="absolute top-[calc(100%+8px)] left-0 z-30 w-80 max-w-[min(20rem,calc(100vw-2.5rem))] overflow-hidden rounded-xl border border-line bg-surface p-1.5 shadow-lift"
        >
          {chatModes.map((m) => {
            const Icon = m.icon
            const active = m.id === mode.id
            return (
              <li key={m.id}>
                <button
                  role="option"
                  aria-selected={active}
                  onClick={() => {
                    onChange(m)
                    setOpen(false)
                  }}
                  className={`flex w-full cursor-pointer items-start gap-3 rounded-lg px-3 py-2.5 text-left transition-colors duration-150 ${
                    active ? 'bg-surface-2' : 'hover:bg-surface-2'
                  }`}
                >
                  <span className={`mt-0.5 flex h-7 w-7 shrink-0 items-center justify-center rounded-lg border ${m.badgeClass}`}>
                    <Icon size={14} strokeWidth={2.2} />
                  </span>
                  <div className="min-w-0 flex-1">
                    <div className="flex items-center gap-2">
                      <p className="text-sm font-semibold text-ink">{m.label}</p>
                    </div>
                    <p className="mt-0.5 text-xs leading-relaxed text-ink-2 line-clamp-2">{m.description}</p>
                  </div>
                </button>
              </li>
            )
          })}
        </ul>
      )}

      <button
        type="button"
        onClick={() => setOpen((v) => !v)}
        aria-haspopup="listbox"
        aria-expanded={open}
        className="press flex cursor-pointer items-center gap-2 rounded-lg border border-line bg-surface px-3 py-1.5 text-sm font-semibold text-ink shadow-xs transition-colors duration-200 hover:border-line-2 hover:bg-surface-2"
      >
        <span className={`flex h-5 w-5 items-center justify-center rounded-md border ${mode.badgeClass}`}>
          <mode.icon size={11} strokeWidth={2.4} />
        </span>
        {mode.label}
        <ChevronDown
          size={14}
          strokeWidth={2.2}
          className={`text-ink-3 transition-transform duration-200 ${open ? 'rotate-180' : ''}`}
          aria-hidden="true"
        />
      </button>
    </div>
  )
}

function CampusPicker({ selectedCampus, onChange }) {
  const [open, setOpen] = useState(false)
  const ref = useRef(null)

  useEffect(() => {
    if (!open) return
    const onPointerDown = (e) => {
      if (!ref.current?.contains(e.target)) setOpen(false)
    }
    document.addEventListener('pointerdown', onPointerDown)
    return () => document.removeEventListener('pointerdown', onPointerDown)
  }, [open])

  const currentLabel = CAMPUSES.find((c) => c.code === selectedCampus)?.label || 'All Campuses'

  return (
    <div ref={ref} className="relative inline-block">
      {open && (
        <div className="absolute top-[calc(100%+8px)] right-0 z-30 max-h-72 w-64 overflow-y-auto rounded-xl border border-line bg-surface p-1 shadow-lift">
          {CAMPUSES.map((c) => (
            <button
              key={c.code}
              onClick={() => {
                onChange(c.code)
                setOpen(false)
              }}
              className={`flex w-full cursor-pointer items-center justify-between rounded-lg px-3 py-2 text-left text-xs font-medium transition-colors ${
                selectedCampus === c.code ? 'bg-panel-2 text-white' : 'text-ink-2 hover:bg-surface-2 hover:text-ink'
              }`}
            >
              <span>{c.label}</span>
              {selectedCampus === c.code && <Check size={13} strokeWidth={2.5} />}
            </button>
          ))}
        </div>
      )}

      <button
        onClick={() => setOpen((v) => !v)}
        className="press flex cursor-pointer items-center gap-1.5 rounded-lg border border-line bg-surface px-2.5 py-1.5 text-xs font-medium text-ink-2 transition-colors hover:border-line-2 hover:text-ink"
      >
        <Building2 size={13} className="text-ink-3" />
        <span className="max-w-[130px] truncate sm:max-w-none">{currentLabel}</span>
        <ChevronDown size={12} className="text-ink-3" />
      </button>
    </div>
  )
}

function FaqList({ faqs, onAsk }) {
  const [filter, setFilter] = useState('')
  const [selectedCategory, setSelectedCategory] = useState('ALL')

  const categories = ['ALL', ...Array.from(new Set(faqs.map((f) => f.category)))]

  const filteredFaqs = faqs.filter((f) => {
    const matchesCategory = selectedCategory === 'ALL' || f.category === selectedCategory
    const matchesSearch = !filter || f.q.toLowerCase().includes(filter.toLowerCase()) || f.category.toLowerCase().includes(filter.toLowerCase())
    return matchesCategory && matchesSearch
  })

  return (
    <div className="flex flex-col">
      <div className="flex items-center justify-between mb-2.5">
        <p className="flex items-center gap-1.5 text-xs font-semibold tracking-wide text-ink-3 uppercase">
          <CircleHelp size={13} strokeWidth={2} aria-hidden="true" />
          Frequently Asked Queries ({faqs.length})
        </p>
      </div>

      {/* Search Filter */}
      {faqs.length > 6 && (
        <div className="relative mb-2.5">
          <Search size={12} className="absolute left-2.5 top-1/2 -translate-y-1/2 text-ink-3 pointer-events-none" />
          <input
            type="text"
            value={filter}
            onChange={(e) => setFilter(e.target.value)}
            placeholder="Search FAQs..."
            className="w-full rounded-lg border border-line bg-surface-2 py-1.5 pl-7 pr-2.5 text-xs text-ink placeholder:text-ink-3 focus:border-panel-2 focus:bg-surface focus:outline-none"
          />
        </div>
      )}

      {/* Category Pills */}
      {categories.length > 2 && (
        <div className="flex flex-wrap gap-1 mb-2.5 max-h-20 overflow-y-auto">
          {categories.map((cat) => (
            <button
              key={cat}
              onClick={() => setSelectedCategory(cat)}
              className={`px-2 py-0.5 rounded-full text-[0.625rem] font-semibold transition-colors cursor-pointer ${
                selectedCategory === cat
                  ? 'bg-panel text-white'
                  : 'bg-surface-2 text-ink-3 hover:bg-surface-3 hover:text-ink'
              }`}
            >
              {cat}
            </button>
          ))}
        </div>
      )}

      <ul className="space-y-1.5 max-h-[calc(100vh-280px)] overflow-y-auto pr-1">
        {filteredFaqs.slice(0, 30).map((f) => (
          <li key={f.q}>
            <button
              onClick={() => onAsk(f.q)}
              className="press group w-full cursor-pointer rounded-lg border border-transparent p-2.5 text-left text-xs font-medium text-ink-2 transition-all duration-150 hover:border-line hover:bg-surface hover:text-ink hover:shadow-xs"
            >
              <div className="flex items-center justify-between gap-1 mb-1">
                <span className="rounded bg-surface-3 px-1.5 py-0.5 text-[0.625rem] font-semibold text-ink-3 uppercase">
                  {f.category}
                </span>
                <Sparkles size={11} className="text-ink-3 opacity-0 transition-opacity group-hover:opacity-100" />
              </div>
              <p className="line-clamp-2 leading-relaxed">{f.q}</p>
            </button>
          </li>
        ))}
        {filteredFaqs.length === 0 && (
          <li className="py-4 text-center text-xs text-ink-3">
            No queries match your search.
          </li>
        )}
      </ul>
    </div>
  )
}

function SqlViewer({ sql }) {
  const [copied, setCopied] = useState(false)
  const [open, setOpen] = useState(false)

  const copySql = () => {
    navigator.clipboard.writeText(sql)
    setCopied(true)
    setTimeout(() => setCopied(false), 2000)
  }

  return (
    <div className="mt-3 rounded-lg border border-line bg-surface-2 overflow-hidden text-xs">
      <button
        type="button"
        onClick={() => setOpen(!open)}
        className="flex w-full cursor-pointer items-center justify-between px-3 py-2 text-ink-2 hover:bg-surface-3 transition-colors"
      >
        <span className="flex items-center gap-1.5 font-mono text-[0.6875rem] font-semibold text-ink">
          <Code2 size={13} className="text-ink-3" />
          Generated SQL Server Query
        </span>
        <ChevronDown size={13} className={`text-ink-3 transition-transform ${open ? 'rotate-180' : ''}`} />
      </button>

      {open && (
        <div className="border-t border-line bg-[#0c0d0f] p-3 text-white">
          <div className="flex items-center justify-between mb-2 pb-1 border-b border-white/10">
            <span className="font-mono text-[0.625rem] text-white/50">T-SQL Read-Only Statement</span>
            <button
              onClick={copySql}
              className="flex items-center gap-1 text-[0.625rem] font-mono text-white/70 hover:text-white transition-colors cursor-pointer"
            >
              {copied ? <Check size={11} className="text-emerald-400" /> : <Copy size={11} />}
              {copied ? 'Copied' : 'Copy'}
            </button>
          </div>
          <pre className="overflow-x-auto font-mono text-[0.75rem] leading-relaxed text-emerald-300">
            <code>{sql}</code>
          </pre>
        </div>
      )}
    </div>
  )
}

function DataTableViewer({ table }) {
  if (!table || !table.rows || table.rows.length === 0) return null
  const columns = table.columns || Object.keys(table.rows[0]).map((k) => ({ key: k, label: k }))

  return (
    <div className="mt-4 overflow-hidden rounded-xl border border-line bg-surface shadow-card">
      <div className="flex items-center justify-between border-b border-line bg-surface-2 px-4 py-2.5">
        <span className="flex items-center gap-1.5 text-xs font-semibold text-ink">
          <TableIcon size={13} className="text-ink-3" />
          Query Results Table
        </span>
        <span className="font-mono text-[0.6875rem] text-ink-3 tabular">
          {table.total_rows || table.rows.length} rows returned
        </span>
      </div>
      <div className="max-h-64 overflow-x-auto overflow-y-auto">
        <table className="w-full min-w-[32rem] text-left text-xs">
          <thead className="sticky top-0 bg-surface-2 border-b border-line">
            <tr>
              {columns.map((c) => (
                <th key={c.key} className="px-3.5 py-2 font-semibold text-ink-3 uppercase tracking-wider text-[0.6875rem]">
                  {c.label || c.key}
                </th>
              ))}
            </tr>
          </thead>
          <tbody className="divide-y divide-line">
            {table.rows.map((row, i) => (
              <tr key={i} className="hover:bg-surface-2/70 transition-colors">
                {columns.map((c) => {
                  const val = row[c.key]
                  const isNum = typeof val === 'number'
                  return (
                    <td key={c.key} className={`px-3.5 py-2.5 text-ink-2 ${isNum ? 'tabular font-mono text-ink' : ''}`}>
                      {val !== null && val !== undefined ? String(val) : '—'}
                    </td>
                  )
                })}
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  )
}

function ChartViewer({ config, data }) {
  if (!config || !data || data.length === 0) return null
  const xKey = config.x_axis_key || Object.keys(data[0])[0]
  const yKeys = config.y_axis_keys || [Object.keys(data[0])[1]]
  const yKey = yKeys[0]

  return (
    <div className="mt-4 rounded-xl border border-line bg-surface p-4 shadow-card">
      <div className="flex items-center gap-2 mb-3">
        <BarChart3 size={14} className="text-ink-3" />
        <p className="text-xs font-semibold text-ink">{config.title || 'Visual Summary'}</p>
      </div>
      <div className="h-44 w-full">
        <ResponsiveContainer width="100%" height="100%">
          <BarChart data={data.slice(0, 10)} margin={{ top: 5, right: 10, left: -20, bottom: 0 }}>
            <CartesianGrid stroke="#e2e4e8" vertical={false} />
            <XAxis dataKey={xKey} tick={{ fontSize: 10, fill: '#585a5d' }} tickLine={false} axisLine={false} />
            <YAxis tick={{ fontSize: 10, fill: '#585a5d' }} tickLine={false} axisLine={false} />
            <Tooltip
              contentStyle={{
                backgroundColor: '#0c0d0f',
                border: 'none',
                borderRadius: '8px',
                color: '#fff',
                fontSize: '11px',
                fontFamily: 'JetBrains Mono, monospace'
              }}
            />
            <Bar dataKey={yKey} fill="var(--color-panel-2)" radius={[4, 4, 0, 0]} />
          </BarChart>
        </ResponsiveContainer>
      </div>
    </div>
  )
}

function PolicySources({ sources }) {
  if (!sources || sources.length === 0) return null
  return (
    <div className="mt-3 flex flex-wrap items-center gap-1.5">
      <span className="text-[0.6875rem] font-semibold text-ink-3 uppercase tracking-wider mr-1">Sources:</span>
      {sources.map((s, idx) => (
        <span
          key={idx}
          className="inline-flex items-center gap-1 rounded-md border border-amber-200 bg-amber-50 px-2 py-1 text-[0.6875rem] font-medium text-amber-800"
        >
          <FileText size={11} className="text-amber-600" />
          {s}
        </span>
      ))}
    </div>
  )
}

/**
 * Lightweight markdown → HTML for AI assistant responses.
 * Handles: **bold**, *italic*, `inline code`, bullet lines (• or *),
 * numbered lists, and paragraph breaks. No dependency needed.
 */
function renderMd(text) {
  if (!text) return ''
  const escaped = text
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')

  return escaped
    // code spans first (protect from bold/italic)
    .replace(/`([^`]+)`/g, '<code class="rounded bg-surface-2 px-1.5 py-0.5 font-mono text-[0.8125rem] text-ink">$1</code>')
    // bold (non-greedy to handle adjacent **groups**)
    .replace(/\*\*(.+?)\*\*/g, '<strong class="font-semibold text-ink">$1</strong>')
    // italic
    .replace(/(?<!\*)\*([^*]+)\*(?!\*)/g, '<em>$1</em>')
    // bullet lines: • or leading * or -
    .replace(/^[•\-\*]\s+(.+)$/gm, '<li class="ml-4 list-disc list-outside">$1</li>')
    // numbered list lines: 1. 2. etc.
    .replace(/^\d+\.\s+(.+)$/gm, '<li class="ml-4 list-decimal list-outside">$1</li>')
    // paragraph breaks (double newline)
    .replace(/\n{2,}/g, '</p><p class="mt-2">')
    // single newlines
    .replace(/\n/g, '<br/>')
}

/**
 * Detect when the user's question topic doesn't match the returned data.
 * e.g. question about "attendance" but result table has marks columns.
 */
function detectMismatch(question, table, evidence) {
  if (!question || !table?.columns) return null

  const q = question.toLowerCase()
  const colKeys = table.columns.map((c) => (c.key || c.label || '').toLowerCase()).join(' ')
  const tableName = (evidence?.tables_queried || []).join(' ').toLowerCase()

  const checks = [
    { keywords: ['attendance', 'absent', 'present', 'leave'], anti: ['obtained', 'total', '%', 'marks', 'result'], label: 'attendance' },
    { keywords: ['fee', 'payment', 'dues', 'challan'], anti: ['obtained', 'subject', 'result'], label: 'fee records' },
    { keywords: ['teacher', 'faculty', 'staff'], anti: ['father', 'rollno', 'smsno'], label: 'teacher data' },
  ]

  for (const check of checks) {
    const asked = check.keywords.some((k) => q.includes(k))
    const gotWrong = check.anti.some((a) => colKeys.includes(a) || tableName.includes('result'))
    if (asked && gotWrong) {
      return `This question asked about ${check.label}, but the engine returned exam result records instead. The database may not have a dedicated ${check.label} table.`
    }
  }
  return null
}

function ChatTurn({ turn, question }) {
  const isUser = turn.from === 'user'
  const [flagged, setFlagged] = useState(false)
  const [feedback, setFeedback] = useState(null) // 'up' | 'down' | null

  const handleFeedback = async (type) => {
    const nextVal = feedback === type ? null : type
    setFeedback(nextVal)
    if (nextVal) {
      try {
        await fetch('/api/v1/query/feedback', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json', Authorization: 'Bearer dev-token' },
          body: JSON.stringify({
            question: question || '',
            feedback_type: nextVal,
            flagged: false
          })
        })
      } catch (e) {
        // silent fallback
      }
    }
  }

  const handleFlag = async () => {
    const nextVal = !flagged
    setFlagged(nextVal)
    if (nextVal) {
      try {
        await fetch('/api/v1/query/flag', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json', Authorization: 'Bearer dev-token' },
          body: JSON.stringify({
            question: question || '',
            feedback_type: 'flag',
            flagged: true,
            details: 'Flagged by user for review'
          })
        })
      } catch (e) {
        // silent fallback
      }
    }
  }

  if (isUser) {
    return (
      <div className="flex justify-end">
        <div className="max-w-[80%] rounded-2xl rounded-tr-sm bg-ink px-4 py-3 text-sm leading-relaxed text-white shadow-sm">
          {turn.text}
        </div>
      </div>
    )
  }

  const mismatch = question ? detectMismatch(question, turn.table, turn.evidence) : null

  return (
    <div className="flex items-start gap-3">
      <span className="mt-1 flex h-7 w-7 shrink-0 items-center justify-center rounded-full bg-lime text-on-accent shadow-xs">
        <Sparkles size={13} strokeWidth={2.4} aria-hidden="true" />
      </span>
      <div className="min-w-0 max-w-[90%] flex-1">
        {/* Mismatch Warning Banner */}
        {mismatch && (
          <div className="mb-3 flex items-start gap-2 rounded-lg border border-amber-200 bg-amber-50 px-3 py-2.5 text-xs text-amber-800">
            <AlertTriangle size={14} className="mt-0.5 shrink-0 text-amber-600" />
            <div>
              <p className="font-semibold">Possible mismatch detected</p>
              <p className="mt-0.5 leading-relaxed text-amber-700">{mismatch}</p>
            </div>
          </div>
        )}

        <div
          className="prose-chat text-sm leading-relaxed text-ink-2 [&_strong]:text-ink [&_li]:my-0.5 [&_code]:text-[0.8125rem]"
          dangerouslySetInnerHTML={{ __html: renderMd(turn.text) }}
        />

        {turn.sql && <SqlViewer sql={turn.sql} />}
        {turn.sources && <PolicySources sources={turn.sources} />}
        {turn.table && <DataTableViewer table={turn.table} />}
        {turn.chartConfig && turn.table?.rows && <ChartViewer config={turn.chartConfig} data={turn.table.rows} />}

        {/* Feedback & Flag bar */}
        <div className="mt-3 flex items-center gap-1">
          <button
            onClick={() => handleFeedback('up')}
            title="Accurate response"
            className={`flex h-7 w-7 cursor-pointer items-center justify-center rounded-md transition-colors ${
              feedback === 'up' ? 'bg-emerald-100 text-emerald-700' : 'text-ink-3 hover:bg-surface-2 hover:text-ink-2'
            }`}
          >
            <ThumbsUp size={13} strokeWidth={2} />
          </button>
          <button
            onClick={() => handleFeedback('down')}
            title="Inaccurate response"
            className={`flex h-7 w-7 cursor-pointer items-center justify-center rounded-md transition-colors ${
              feedback === 'down' ? 'bg-rose-100 text-rose-700' : 'text-ink-3 hover:bg-surface-2 hover:text-ink-2'
            }`}
          >
            <ThumbsDown size={13} strokeWidth={2} />
          </button>
          <button
            onClick={handleFlag}
            title={flagged ? 'Flagged for review' : 'Flag this response'}
            className={`flex h-7 cursor-pointer items-center gap-1 rounded-md px-1.5 text-[0.6875rem] font-medium transition-colors ${
              flagged ? 'bg-amber-100 text-amber-700' : 'text-ink-3 hover:bg-surface-2 hover:text-ink-2'
            }`}
          >
            <Flag size={12} strokeWidth={2} />
            {flagged && <span>Flagged</span>}
          </button>

          {turn.meta && (
            <span className="ml-auto font-mono text-[0.6875rem] text-ink-3">
              {turn.meta}
            </span>
          )}
        </div>
      </div>
    </div>
  )
}

export default function ChatbotPage() {
  const [mode, setMode] = useState(chatModes[0])
  const [campus, setCampus] = useState('ALL')
  const [threads, setThreads] = useState(() => ({
    wren_nl2sql: chatModes[0].initialMessages,
    google_file_search_rag: chatModes[1].initialMessages,
    prediction_ai: chatModes[2].initialMessages
  }))
  const [draft, setDraft] = useState('')
  const [loading, setLoading] = useState(false)
  const [policyModalOpen, setPolicyModalOpen] = useState(false)
  const scrollRef = useRef(null)

  const currentThread = threads[mode.id] || []

  useEffect(() => {
    scrollRef.current?.scrollTo({ top: scrollRef.current.scrollHeight, behavior: 'smooth' })
  }, [currentThread, loading])

  /**
   * Client-side guardrail: reject profanity, gibberish, greetings, and
   * non-academic input before it reaches the backend or returns PII.
   */
  const validateQuery = (text) => {
    const lower = text.toLowerCase().replace(/[^a-z0-9\s]/g, ' ')
    const words = lower.split(/\s+/).filter(Boolean)

    // Block profanity / slurs
    const blocked = [
      'bitch', 'fuck', 'shit', 'ass', 'damn', 'dick', 'pussy', 'cunt',
      'bastard', 'whore', 'slut', 'nigga', 'nigger', 'faggot', 'retard',
      'stfu', 'gtfo', 'lmao', 'lmfao', 'wtf', 'wth'
    ]
    if (blocked.some((w) => words.includes(w))) {
      return 'This assistant handles academic queries only. Please ask about student records, exam results, attendance, policies, or predictions.'
    }

    // Conversational & Odd Request Failsafe (e.g. "how are you", "supp ?", "hello")
    const greetings = [
      'hi', 'hello', 'hey', 'sup', 'supp', 'yo', 'whatsup', 'wassup',
      'howdy', 'hola', 'bye', 'goodbye', 'thanks', 'thank', 'ok', 'okay',
      'cool', 'nice', 'lol', 'haha', 'hmm', 'bruh', 'bro', 'dude'
    ]
    const chatPhrases = [
      'how are you', 'who are you', 'what can you do', 'what are you', 'help me',
      'how does this work', 'good morning', 'good evening', 'good afternoon'
    ]
    if (
      chatPhrases.some((p) => lower.includes(p)) ||
      (words.length <= 3 && words.every((w) => greetings.includes(w) || w.length <= 2))
    ) {
      return 'Hello! I am **EduQuery AI**, your intelligent academic analytics and prediction assistant for Daanish Schools. Ask me about student results, attendance records, policy documents, or exam predictions across all 20 campuses.'
    }

    // Minimum signal check
    if (text.trim().length < 2) {
      return 'Please enter a complete question about academic data, policies, or predictions.'
    }

    return null // valid for backend execution
  }

  const submitQuery = async (promptText) => {
    const textToSend = (promptText || draft).trim()
    if (!textToSend || loading) return

    setDraft('')
    const userMessage = { from: 'user', text: textToSend }

    setThreads((prev) => ({
      ...prev,
      [mode.id]: [...(prev[mode.id] || []), userMessage]
    }))

    // Guardrail: reject before network round-trip
    const rejection = validateQuery(textToSend)
    if (rejection) {
      const isGreeting = rejection.includes('EduQuery AI')
      setThreads((prev) => ({
        ...prev,
        [mode.id]: [
          ...(prev[mode.id] || []),
          {
            from: 'assistant',
            text: rejection,
            meta: isGreeting ? 'Conversational Guidance' : 'Input Guardrail'
          }
        ]
      }))
      return
    }

    setLoading(true)

    try {
      const res = await fetch('/api/v1/query', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          Authorization: 'Bearer dev-token'
        },
        body: JSON.stringify({
          prompt: textToSend,
          engine: mode.engine_mode,
          filters: {
            campus_code: campus
          }
        })
      })

      const data = await res.json()

      if (!res.ok || data.success === false) {
        const errMsg = data.message || 'The engine could not process this request.'
        const assistantError = {
          from: 'assistant',
          text: `⚠️ Query Notice: ${errMsg}`,
          meta: `Error ${data.error_code || 'RESPONSE_ERROR'}`
        }
        setThreads((prev) => ({
          ...prev,
          [mode.id]: [...(prev[mode.id] || []), assistantError]
        }))
        return
      }

      // Extract generated SQL if present in text or evidence
      let generatedSql = null
      const sqlMatch = data.answer.match(/`+(?:sql|tsql)?\s*(SELECT[\s\S]*?)`+/i)
      if (sqlMatch) {
        generatedSql = sqlMatch[1].trim()
      }

      const assistantReply = {
        from: 'assistant',
        text: data.answer.replace(/`+(?:sql|tsql)?\s*(SELECT[\s\S]*?)`+/i, '').trim(),
        sql: generatedSql,
        sources: data.evidence?.rag_sources_used || [],
        table: data.data_table,
        chartConfig: data.chart_config,
        evidence: data.evidence,
        question: textToSend,
        meta: `Executed in ${data.evidence?.execution_time_ms ? `${data.evidence.execution_time_ms}ms` : 'sub-second'} · Scope: ${data.evidence?.campus_applied || campus}`
      }

      setThreads((prev) => ({
        ...prev,
        [mode.id]: [...(prev[mode.id] || []), assistantReply]
      }))
    } catch (err) {
      setThreads((prev) => ({
        ...prev,
        [mode.id]: [
          ...(prev[mode.id] || []),
          {
            from: 'assistant',
            text: 'Unable to reach the backend service. Ensure the FastAPI server is running on port 8000.',
            meta: 'Network Connection Error'
          }
        ]
      }))
    } finally {
      setLoading(false)
    }
  }

  const clearThread = () => {
    setThreads((prev) => ({
      ...prev,
      [mode.id]: mode.initialMessages
    }))
  }

  return (
    <div className="flex h-full flex-col bg-canvas">
      {/* Top Engine & Scope Bar */}
      <div className="flex flex-wrap items-center justify-between gap-3 border-b border-line bg-surface px-6 py-3.5 sm:px-10">
        <div className="flex items-center gap-3">
          <ModeSwitcher mode={mode} onChange={setMode} />
          <CampusPicker selectedCampus={campus} onChange={setCampus} />
        </div>

        <div className="flex items-center gap-2">
          {mode.id === 'google_file_search_rag' && (
            <button
              onClick={() => setPolicyModalOpen(true)}
              className="press flex cursor-pointer items-center gap-1.5 rounded-lg border border-amber-200 bg-amber-50/70 px-3 py-1.5 text-xs font-semibold text-amber-800 transition-colors hover:bg-amber-100"
            >
              <FileUp size={13} className="text-amber-700" />
              Manage Policy Docs
            </button>
          )}

          <button
            onClick={clearThread}
            title="Clear current thread"
            className="press flex h-8 w-8 cursor-pointer items-center justify-center rounded-lg text-ink-3 transition-colors hover:bg-surface-2 hover:text-ink"
          >
            <Trash2 size={15} />
          </button>
        </div>
      </div>

      <div className="flex min-h-0 flex-1 flex-col lg:flex-row">
        {/* Main Conversation Thread */}
        <div className="flex min-w-0 min-h-0 flex-1 flex-col">
          <div ref={scrollRef} className="min-h-0 flex-1 overflow-y-auto">
            <div className="mx-auto w-full max-w-3xl px-6 pt-8 pb-8 sm:px-10">
              <div className="mb-6 lg:hidden">
                <FaqList faqs={mode.faqs} onAsk={submitQuery} />
              </div>

              <div className="space-y-6">
                {currentThread.map((m, i) => (
                  <ChatTurn
                    key={i}
                    turn={m}
                    question={m.question || (m.from === 'assistant' && i > 0 ? currentThread[i - 1]?.text : null)}
                  />
                ))}

                {loading && (
                  <div className="flex items-center gap-3 text-xs text-ink-3">
                    <span className="flex h-7 w-7 items-center justify-center rounded-full bg-surface text-ink-2 shadow-xs animate-spin">
                      <RefreshCw size={13} />
                    </span>
                    <span className="font-mono">Processing request through {mode.short}...</span>
                  </div>
                )}
              </div>
            </div>
          </div>

          {/* Composer */}
          <div className="border-t border-line bg-surface/50 backdrop-blur-sm px-6 py-4 sm:px-10">
            <form
              onSubmit={(e) => {
                e.preventDefault()
                submitQuery()
              }}
              className="mx-auto w-full max-w-3xl"
            >
              <div className="flex items-center gap-2 rounded-3xl border border-line-2 bg-surface p-1.5 shadow-sm transition-all duration-200 focus-within:border-ink/30 focus-within:shadow-md">
                <input
                  value={draft}
                  onChange={(e) => setDraft(e.target.value)}
                  placeholder={mode.placeholder}
                  disabled={loading}
                  className="min-w-0 flex-1 bg-transparent px-3 py-1.5 text-sm text-ink outline-none placeholder:text-ink-3 disabled:opacity-50"
                />
                <button
                  type="submit"
                  disabled={!draft.trim() || loading}
                  className="press flex h-9 w-9 shrink-0 cursor-pointer items-center justify-center rounded-full bg-ink text-white transition-all duration-200 hover:opacity-90 disabled:cursor-not-allowed disabled:opacity-25 shadow-xs"
                  aria-label="Send query"
                >
                  <ArrowUp size={16} strokeWidth={2.5} />
                </button>
              </div>
            </form>
          </div>
        </div>

        {/* Desktop FAQs & Guidance */}
        <aside className="hidden w-84 shrink-0 overflow-y-auto border-l border-line bg-surface-2/40 px-6 py-8 lg:block">
          <FaqList faqs={mode.faqs} onAsk={submitQuery} />
        </aside>
      </div>

      {/* Policy Management Modal */}
      {policyModalOpen && (
        <PolicyManagerModal isOpen={policyModalOpen} onClose={() => setPolicyModalOpen(false)} />
      )}
    </div>
  )
}
