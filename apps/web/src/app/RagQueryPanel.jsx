import { useState } from 'react'

export default function RagQueryPanel() {
  const [query, setQuery] = useState('What is the leave policy for boarders?')
  const [loading, setLoading] = useState(false)
  const [answer, setAnswer] = useState('')
  const [sources, setSources] = useState([])
  const [error, setError] = useState(null)

  const runQuery = async () => {
    setLoading(true)
    setError(null)
    setAnswer('')
    setSources([])
    try {
      const res = await fetch('/rag/query', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ query, top_k: 5 }),
      })
      if (!res.ok) throw new Error(`Server returned ${res.status}`)
      const data = await res.json()
      setAnswer(data.answer || '')
      setSources(data.sources || [])
    } catch (err) {
      setError(err.message)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="rounded-lg bg-surface p-4 shadow-card">
      <h3 className="mb-3 text-sm font-semibold">Policy RAG</h3>
      <textarea
        value={query}
        onChange={(e) => setQuery(e.target.value)}
        rows={3}
        className="w-full rounded-md border p-2 text-sm"
      />
      <div className="mt-3 flex items-center gap-2">
        <button
          onClick={runQuery}
          disabled={loading}
          className="press rounded-full bg-ink px-4 py-2 text-white"
        >
          {loading ? 'Running...' : 'Run'}
        </button>
        {error && <span className="text-xs text-alert">{error}</span>}
      </div>

      {answer && (
        <div className="mt-4">
          <h4 className="text-sm font-semibold">Answer</h4>
          <div className="mt-2 whitespace-pre-wrap text-sm text-ink-2">{answer}</div>
        </div>
      )}

      {sources.length > 0 && (
        <div className="mt-4">
          <h4 className="text-sm font-semibold">Sources</h4>
          <ul className="mt-2 space-y-2 text-sm text-ink-3">
            {sources.map((s, i) => (
              <li key={i}>
                <div className="font-mono">{s.source}</div>
                <div className="text-xs">score: {Number(s.score).toFixed(3)}</div>
              </li>
            ))}
          </ul>
        </div>
      )}
    </div>
  )
}
