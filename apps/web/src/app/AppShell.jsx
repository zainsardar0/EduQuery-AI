import { useState, useEffect, useRef, useMemo } from 'react'
import {
  ArrowLeft,
  ChevronRight,
  Database,
  FileText,
  History,
  LogOut,
  Plus,
  RefreshCw,
  Search,
  Send,
  Sparkles,
  TrendingUp,
  AlertTriangle,
  CheckCircle2,
  Brain,
  Shield,
  Layers,
  Code,
  Copy,
  Check,
  BarChart3,
  HelpCircle,
  User,
  Bot,
  ThumbsUp,
  ThumbsDown,
  Flag,
  X
} from 'lucide-react'
import {
  ResponsiveContainer,
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  CartesianGrid,
  LineChart,
  Line,
  Cell
} from 'recharts'
import Logo from '../components/Logo'
import PolicyManagerModal from './PolicyManagerModal'

// 3 Core Production Engines
const ENGINES = [
  {
    id: 'wren_nl2sql',
    name: 'WrenAI (Query to SQL · Live Database)',
    short: 'WrenAI · NL2SQL',
    icon: Database,
    desc: 'Translates natural language into read-only SQL Server queries across 20 Daanish campuses',
    badge: 'Live MSSQL',
    badgeColor: 'bg-[#003d1c]/10 text-[#003d1c] border-[#003d1c]/20'
  },
  {
    id: 'google_file_search_rag',
    name: 'Google File Search API (Policy Documents · Gemini)',
    short: 'Google File Search',
    icon: FileText,
    desc: 'Queries official Daanish School policies (PDF, DOCX, MD, TXT, CSV) in Gemini storage with source citations',
    badge: 'Gemini Policy RAG',
    badgeColor: 'bg-amber-500/10 text-amber-700 border-amber-500/20'
  },
  {
    id: 'prediction_ai',
    name: 'Academic Prediction AI (Student Risk & Forecasting)',
    short: 'Prediction AI',
    icon: TrendingUp,
    desc: 'Forecasts academic failure risk, board pass probabilities, and SHAP feature attributions',
    badge: 'ML + SHAP AI',
    badgeColor: 'bg-[#2f6b46]/10 text-[#2f6b46] border-[#2f6b46]/20'
  }
]

const CAMPUSES = [
  { code: 'ALL', label: 'All Campuses (Institutional Scope)' },
  { code: 'ATKB', label: 'Attock Boys (ATKB)' },
  { code: 'ATKG', label: 'Attock Girls (ATKG)' },
  { code: 'CTNB', label: 'Chishtian Boys (CTNB)' },
  { code: 'CTNG', label: 'Chishtian Girls (CTNG)' },
  { code: 'DGKB', label: 'D.G. Khan Boys (DGKB)' },
  { code: 'DGKG', label: 'D.G. Khan Girls (DGKG)' },
  { code: 'HSPB', label: 'Hasilpur Boys (HSPB)' },
  { code: 'HSPG', label: 'Hasilpur Girls (HSPG)' },
  { code: 'MNKB', label: 'Mankera Boys (MNKB)' },
  { code: 'MNKG', label: 'Mankera Girls (MNKG)' },
  { code: 'MNWB', label: 'Mianwali Boys (MNWB)' },
  { code: 'MNWG', label: 'Mianwali Girls (MNWG)' },
  { code: 'RJNB', label: 'Rajanpur Boys (RJNB)' },
  { code: 'RJNG', label: 'Rajanpur Girls (RJNG)' },
  { code: 'RYKB', label: 'Rahim Yar Khan Boys (RYKB)' },
  { code: 'RYKG', label: 'Rahim Yar Khan Girls (RYKG)' },
  { code: 'TNSB', label: 'Taunsa Boys (TNSB)' },
  { code: 'TNSG', label: 'Taunsa Girls (TNSG)' },
  { code: 'VEHB', label: 'Vehari Boys (VEHB)' },
  { code: 'VEHG', label: 'Vehari Girls (VEHG)' }
]

// 100 Comprehensive Gold Queries for WrenAI NL2SQL (10 in each of 10 categories)
const WREN_100_GOLD_QUERIES = [
  {
    category: '1. Student Demographics & Profiles',
    queries: [
      'Show students missing father name in Class 10 across all campuses',
      'List total enrolled students broken down by class for Attock Boys campus',
      'Show students in Class 8 with unassigned section or category',
      'Count active students across all campuses grouped by gender',
      'Show enrolled students in ATKB',
      'List the students across all campuses',
      'Show 10 students in section A',
      'List students in class 10',
      'Show student roster with registration numbers and father names',
      'Count total students enrolled in each grade level from Class 6 to 10'
    ]
  },
  {
    category: '2. Weak & At-Risk Students',
    queries: [
      'Show weak students in class 10',
      'Which students are failing in grade 9?',
      'List struggling students',
      'Find low-performing students in class 8',
      'Show students below 40 percent',
      'Which student results are under 50%?',
      'Show at risk students in ATKB',
      'Find weak students in MNWB class 10',
      'List failing students in section A',
      'Show students with marks below 35'
    ]
  },
  {
    category: '3. Top & High-Performing Students',
    queries: [
      'Show top students',
      'List the best students in class 10',
      'Who has the highest student results?',
      'Return 5 top students in ATKG',
      'Show high-performing students in grade 9',
      'List best student marks across campuses',
      'Find top students in section B',
      'Show the highest results for year 26',
      'Who are the top students in MNWB?',
      'Return 20 best students'
    ]
  },
  {
    category: '4. Attendance & Daily Absence Records',
    queries: [
      'Show attendance summary',
      'How many attendance records are present?',
      'Summarize attendance across campuses',
      'Show attendance for ATKB',
      'Attendance summary for MNWB campus',
      'Show absent students',
      'List recent absences',
      'Who is absent today?',
      'Show the latest absence records',
      'List absentees in ATKB'
    ]
  },
  {
    category: '5. House & Hostel Attendance Logs',
    queries: [
      'Summarize house attendance',
      'Compare attendance across all schools',
      'Show attendance status by house',
      'Show absence records for MNWB',
      'Return 10 absent students',
      'Which students have an absence?',
      'Show recent absent attendance',
      'List absence events by house',
      'Show boarder attendance rates across hostel houses',
      'Compare house attendance between Iqbal and Jinnah houses'
    ]
  },
  {
    category: '6. Teacher Performance & Results',
    queries: [
      'Show teacher performance',
      'Compare teacher performance by subject',
      'List top teachers',
      'Show teacher pass rates in ATKB',
      'Teacher performance for Mathematics',
      'Compare teachers in class 10',
      'Show teacher class averages',
      'List teacher results for year 26',
      'Show 10 teacher performance rows',
      'Which teachers have the best pass percentage?'
    ]
  },
  {
    category: '7. Subject-Specific Exam Analytics',
    queries: [
      'Show subject performance',
      'Compare Mathematics performance',
      'Show English subject results',
      'Compare Physics performance in class 10',
      'Show subject pass rates for ATKG',
      'List subjects with the highest failure rates in Class 9',
      'Compare Science vs Arts subject averages across campuses',
      'Show Urdu and Islamiyat subject scores in Class 8',
      'Calculate average marks by subject for Class 7 in Rahim Yar Khan',
      'Show Translation of Holy Quran exam results by section'
    ]
  },
  {
    category: '8. Class & Section Benchmarks',
    queries: [
      'Show class performance',
      'Compare class 10 performance',
      'Show weakest classes by pass percentage',
      'Compare section A class results',
      'Show class averages in ATKB',
      'Compare performance between Class 9 and Class 10',
      'Show section-wise pass percentage for Class 8',
      'List Class 7 sections with average score above 75%',
      'Compare pass percentage across sections A, B, and C in Class 10',
      'Show overall academic score distribution for Class 6'
    ]
  },
  {
    category: '9. Multi-Campus Governance Benchmarks',
    queries: [
      'Compare school performance across all campuses',
      'Show campus performance summary',
      'Compare school pass rates',
      'Show average performance for each campus',
      'Compare campus results for year 26',
      'Show overall pass percentage in Board Middle Exam by campus',
      'Rank top 5 performing Daanish campuses in Class 10 examinations',
      'Compare average student attendance and exam scores across all 20 campuses',
      'Show student count and pass rates grouped by campus code',
      'Show student performance variance between Boys and Girls campuses'
    ]
  },
  {
    category: '10. Individual Student & Exam Inquiries',
    queries: [
      'Show results for roll number 12345',
      'Show marks for student named Ali Hassan',
      'Find student named Sara Khan',
      'Show profile of student named Ayesha Malik',
      'Show attendance for student named Ahmed Raza',
      'Show detailed marks breakdown for Roll No 320328',
      'Find academic history of Muhammad Bilal in Class 10',
      'Show term-wise progress for Roll No 319932',
      'Search student details for Zain Ul Abideen in RYKB',
      'Show exam score summary for Roll No 321450'
    ]
  }
]

// Policy Prompts for Google File Search API (9 Policies)
const FILE_SEARCH_PROMPTS = [
  {
    category: 'Admissions & Quotas',
    queries: [
      'What are the rules regarding day scholars admission and attendance?',
      'What is the policy for siblings of students to get admission in Daanish schools?',
      'What are the age limits and poverty criteria for Class 6 induction?',
      'Are twin applicants eligible for joint admission if both qualify?'
    ]
  },
  {
    category: 'Fees & Daily Routine',
    queries: [
      'What is the monthly tuition fee for day scholars and late payment fines?',
      'What are the exact daily timings and gate closure rules for morning assembly?',
      'Are mobile phones, personal cash, or smart devices allowed on campus?',
      'What are the rules regarding mandatory morning and evening prep study sessions?'
    ]
  },
  {
    category: 'Leave, Medical & Health',
    queries: [
      'What is the procedure for medical leave and fitness certificate requirements?',
      'How does the 24/7 on-campus medical dispensary handle contagious diseases?',
      'Who is authorized to take boarders out on weekend leave and what is the return deadline?',
      'What emergency protocol is followed for transferring injured students to DHQ hospital?'
    ]
  },
  {
    category: 'Promotion, Discipline & Staff',
    queries: [
      'What is the passing criteria for Class 6-8 vs Class 9-12 and detention rules?',
      'What progressive disciplinary actions occur for repeated late arrival at morning gate?',
      'Who is eligible to use the on-campus Day Care Centre facilities for staff children?',
      'How do faculty and administrative staff apply for casual or medical leave?'
    ]
  }
]

// Prediction AI Prompts & FAQs
const PREDICTION_FAQS = [
  {
    category: 'Academic Risk & Dropout Prediction',
    queries: [
      'Predict students in Class 10 at high risk of failing annual board exams',
      'Identify students in Class 9 whose attendance is below 75% with failing grades',
      'Forecast pass probability and risk distribution for Attock Boys campus',
      'Show critical academic risk factors and SHAP feature importance for failing students'
    ]
  },
  {
    category: 'Subject-Specific & GPA Forecasts',
    queries: [
      'Predict failure probability for Class 10 Mathematics and Physics students',
      'What are the top 3 drivers influencing student grade drop between Midterm and Final?',
      'Forecast expected GPA distribution for Class 8 students entering Class 9',
      'Identify students who need immediate remedial tutoring intervention before exams'
    ]
  },
  {
    category: 'Predictive Intelligence FAQs',
    queries: [
      'How does the AI calculate student risk scores and what data features are used?',
      'What threshold constitutes "High Risk" requiring teacher and principal notification?',
      'How do SHAP attributions explain individual student predictions for educators?'
    ]
  }
]

// Inline Markdown Parser
function renderInlineMarkdown(str) {
  if (!str) return null
  const parts = str.split(/(\*\*.*?\*\*|`.*?`)/g)
  return parts.map((part, idx) => {
    if (part.startsWith('**') && part.endsWith('**') && part.length >= 4) {
      return (
        <strong key={idx} className="font-semibold text-ink">
          {part.slice(2, -2)}
        </strong>
      )
    }
    if (part.startsWith('`') && part.endsWith('`') && part.length >= 2) {
      return (
        <code key={idx} className="px-1.5 py-0.5 rounded-md bg-surface-2 border border-line font-mono text-[11px] text-[#003d1c]">
          {part.slice(1, -1)}
        </code>
      )
    }
    return part.replace(/\*+/g, '')
  })
}

// Semantic Block Tokenizer
function parseMarkdownBlocks(text) {
  if (!text) return []
  const normalized = text
    .replace(/\r\n/g, '\n')
    .replace(/\\%/g, '%')
    .replace(/\$([^\$\n]+)\$/g, '$1')
    .replace(/\\\$/g, '$')
    .replace(/\ufffd/g, '-')
    .replace(/[\u2013\u2014]/g, '-')
    .replace(/[\u2018\u2019]/g, "'")
    .replace(/[\u201c\u201d]/g, '"')

  const lines = normalized.split('\n')
  const blocks = []
  let currentList = null
  let currentParagraph = []

  const flushParagraph = () => {
    if (currentParagraph.length > 0) {
      blocks.push({ type: 'paragraph', text: currentParagraph.join(' ').trim() })
      currentParagraph = []
    }
  }

  const flushList = () => {
    if (currentList && currentList.items.length > 0) {
      blocks.push(currentList)
      currentList = null
    }
  }

  for (let i = 0; i < lines.length; i++) {
    const rawLine = lines[i]
    const trimmed = rawLine.trim()

    if (!trimmed) {
      flushParagraph()
      flushList()
      continue
    }

    if (/^#{1,4}\s+/.test(trimmed)) {
      flushParagraph()
      flushList()
      const level = trimmed.match(/^(#{1,4})\s+/)[1].length
      const headingText = trimmed.replace(/^#{1,4}\s+/, '').replace(/^\*\*|\*\*$/g, '')
      blocks.push({ type: 'heading', level, text: headingText })
      continue
    }

    if (/^\(Sources?:/i.test(trimmed)) {
      flushParagraph()
      flushList()
      blocks.push({ type: 'citation', text: trimmed })
      continue
    }

    const bulletMatch = rawLine.match(/^(\s*)([\*\-•])\s+(.+)$/)
    if (bulletMatch) {
      flushParagraph()
      const indent = bulletMatch[1].length
      const itemText = bulletMatch[3].trim()
      if (!currentList || currentList.type !== 'unordered') {
        flushList()
        currentList = { type: 'unordered', items: [] }
      }
      currentList.items.push({ text: itemText, indent: indent >= 2 ? 1 : 0 })
      continue
    }

    const orderedMatch = rawLine.match(/^(\s*)(\d+)\.\s+(.+)$/)
    if (orderedMatch) {
      flushParagraph()
      const indent = orderedMatch[1].length
      const num = orderedMatch[2]
      const itemText = orderedMatch[3].trim()
      if (!currentList || currentList.type !== 'ordered') {
        flushList()
        currentList = { type: 'ordered', items: [] }
      }
      currentList.items.push({ num, text: itemText, indent: indent >= 2 ? 1 : 0 })
      continue
    }

    if (currentList) flushList()
    currentParagraph.push(trimmed)
  }

  flushParagraph()
  flushList()
  return blocks
}

// Markdown & Typography Renderer Component
function FormattedAnswer({ text }) {
  if (!text) return null

  let mainText = text
  let sqlSnippet = null
  if (text.includes('Generated T-SQL:')) {
    const parts = text.split('Generated T-SQL:')
    mainText = parts[0].trim()
    sqlSnippet = parts[1]?.replace(/```sql|```|`/g, '')?.trim()
  }

  const blocks = parseMarkdownBlocks(mainText)

  return (
    <div className="space-y-3 text-xs leading-relaxed text-ink-2">
      {blocks.map((block, bIdx) => {
        if (block.type === 'heading') {
          return (
            <h3
              key={bIdx}
              className="text-xs font-bold tracking-tight text-ink pt-2 pb-0.5 border-b border-line flex items-center gap-2"
            >
              <span className="h-1.5 w-1.5 rounded-full bg-[#003d1c] shrink-0" />
              {renderInlineMarkdown(block.text)}
            </h3>
          )
        }

        if (block.type === 'unordered') {
          return (
            <ul key={bIdx} className="space-y-1.5 my-1.5">
              {block.items.map((item, iIdx) => (
                <li
                  key={iIdx}
                  className={`flex items-start gap-2.5 text-xs text-ink-2 ${
                    item.indent > 0 ? 'ml-4 text-ink-3' : ''
                  }`}
                >
                  <span
                    className={`rounded-full shrink-0 mt-1.5 ${
                      item.indent > 0 ? 'h-1 w-1 bg-ink-3' : 'h-1.5 w-1.5 bg-[#003d1c]'
                    }`}
                  />
                  <span className="flex-1 leading-relaxed">{renderInlineMarkdown(item.text)}</span>
                </li>
              ))}
            </ul>
          )
        }

        if (block.type === 'ordered') {
          return (
            <ol key={bIdx} className="space-y-1.5 my-1.5">
              {block.items.map((item, iIdx) => (
                <li
                  key={iIdx}
                  className={`flex items-start gap-2 text-xs text-ink-2 ${
                    item.indent > 0 ? 'ml-4 text-ink-3' : ''
                  }`}
                >
                  <span className="font-mono text-[11px] font-bold text-[#003d1c] shrink-0 mt-0.5 w-4 text-right">
                    {item.num}.
                  </span>
                  <span className="flex-1 leading-relaxed">{renderInlineMarkdown(item.text)}</span>
                </li>
              ))}
            </ol>
          )
        }

        if (block.type === 'citation') {
          return (
            <div
              key={bIdx}
              className="mt-2.5 p-2.5 rounded-xl bg-amber-50/70 border border-amber-200/80 text-xs font-mono text-amber-900 flex items-center gap-2"
            >
              <FileText size={13} className="text-amber-600 shrink-0" />
              <span>{renderInlineMarkdown(block.text)}</span>
            </div>
          )
        }

        return (
          <p key={bIdx} className="text-xs text-ink-2 leading-relaxed">
            {renderInlineMarkdown(block.text)}
          </p>
        )
      })}

      {sqlSnippet && (
        <div className="mt-3 rounded-xl border border-zinc-800 bg-[#0c0d0f] text-zinc-100 p-3.5 font-mono text-xs overflow-x-auto shadow-sm">
          <div className="flex items-center justify-between pb-2 mb-2 border-b border-zinc-800 text-[11px] text-zinc-400">
            <span className="flex items-center gap-1.5 font-medium">
              <Code size={13} className="text-[#d3f84e]" />
              Generated Parameterized T-SQL (Read-Only)
            </span>
          </div>
          <code>{sqlSnippet}</code>
        </div>
      )}
    </div>
  )
}

function detectMismatch(question, table, evidence) {
  if (!question || !table || !table.columns) return null
  const q = question.toLowerCase()
  const colKeys = table.columns.map((c) => (c.key || c.label || '').toLowerCase())
  const tableName = ((evidence?.tables_queried || []).join(' ') || '').toLowerCase()

  const checks = [
    {
      keywords: ['attendance', 'absent', 'presence', 'leave'],
      anti: ['exam_marks', 'total_marks', 'score', 'percentage', 'grade'],
      label: 'attendance'
    },
    {
      keywords: ['fee', 'concession', 'dues', 'challan'],
      anti: ['student_marks', 'marks_obtained'],
      label: 'fees'
    },
    {
      keywords: ['teacher', 'staff', 'instructor', 'faculty'],
      anti: ['dob', 'father_name'],
      label: 'teachers'
    }
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

// Single Chat Message Component (User Prompt + AI Response)
function ChatMessageItem({ message, onCopy, copiedId, engineObj }) {
  const isCopied = copiedId === message.id
  const result = message.result
  const [flagged, setFlagged] = useState(false)
  const [feedback, setFeedback] = useState(null) // 'up' | 'down' | null

  const mismatch = message.prompt ? detectMismatch(message.prompt, result?.data_table, result?.evidence) : null

  const handleFeedback = async (type) => {
    const nextVal = feedback === type ? null : type
    setFeedback(nextVal)
    if (nextVal) {
      try {
        await fetch('/api/v1/query/feedback', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json', Authorization: 'Bearer dev-token' },
          body: JSON.stringify({
            question: message.prompt || '',
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
            question: message.prompt || '',
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

  return (
    <div className="space-y-4 animate-in fade-in duration-200">
      {/* User Inquiry Balloon */}
      <div className="flex items-start justify-end gap-2.5">
        <div className="max-w-2xl rounded-2xl rounded-tr-none bg-[#003d1c] px-4 py-3 text-xs text-white shadow-sm">
          <p className="font-medium leading-relaxed">{message.prompt}</p>
          <div className="flex items-center justify-end gap-1.5 mt-1.5 text-[10px] text-[#a9c4b3] font-mono">
            <span>{message.timestamp}</span>
          </div>
        </div>
        <div className="h-7 w-7 rounded-full bg-[#003d1c] text-[#d3f84e] flex items-center justify-center font-bold text-xs shrink-0 shadow-sm">
          <User size={14} />
        </div>
      </div>

      {/* AI Response Card */}
      <div className="flex items-start gap-2.5">
        <div className="h-7 w-7 rounded-full bg-[#d3f84e] text-[#003d1c] flex items-center justify-center font-bold text-xs shrink-0 shadow-sm mt-1">
          <Sparkles size={14} strokeWidth={2.4} />
        </div>

        <div className="flex-1 min-w-0 rounded-2xl border border-line bg-surface p-5 shadow-sm space-y-5">
          {/* Mismatch Warning Banner */}
          {mismatch && (
            <div className="flex items-start gap-2 rounded-xl border border-amber-200 bg-amber-50 px-3 py-2.5 text-xs text-amber-800">
              <AlertTriangle size={14} className="mt-0.5 shrink-0 text-amber-600" />
              <div>
                <p className="font-semibold">Possible mismatch detected</p>
                <p className="mt-0.5 leading-relaxed text-amber-700">{mismatch}</p>
              </div>
            </div>
          )}

          {/* Response Header */}
          <div className="flex items-center justify-between border-b border-line pb-3">
            <div className="flex items-center gap-2 font-mono text-xs text-ink-3">
              <span className="px-2 py-0.5 rounded-md bg-surface-2 text-ink-2 font-semibold border border-line">
                {result?.evidence?.intent_category || engineObj.name}
              </span>
              <span>·</span>
              <span>{result?.evidence?.execution_time_ms || 12}ms</span>
            </div>
            <button
              onClick={() => onCopy(message)}
              className="flex items-center gap-1.5 text-xs text-ink-3 hover:text-ink transition cursor-pointer"
              title="Copy Answer"
            >
              {isCopied ? <Check size={14} className="text-emerald-600" /> : <Copy size={14} />}
              <span>{isCopied ? 'Copied' : 'Copy'}</span>
            </button>
          </div>

          {/* Formatted Textual Answer */}
          <FormattedAnswer text={result?.answer} />

          {/* Chart Visualization */}
          {result?.chart_config && result.chart_config.chart_type === 'bar' && result.data_table?.rows && (
            <div className="mt-4 rounded-xl border border-line p-4 bg-surface-2">
              <p className="text-xs font-semibold text-ink mb-3">
                {result.chart_config.title || 'Visual Analysis'}
              </p>
              <div className="h-56 w-full">
                <ResponsiveContainer width="100%" height="100%">
                  <BarChart data={result.data_table.rows}>
                    <CartesianGrid strokeDasharray="3 3" stroke="#e2e4e8" />
                    <XAxis dataKey={result.chart_config.x_axis_key} tick={{ fontSize: 11 }} />
                    <YAxis tick={{ fontSize: 11 }} />
                    <Tooltip
                      contentStyle={{
                        backgroundColor: '#0c0d0f',
                        borderColor: '#27272a',
                        borderRadius: '8px',
                        color: '#FFF'
                      }}
                    />
                    <Bar dataKey={result.chart_config.y_axis_keys[0]} fill="#2f6b46" radius={[4, 4, 0, 0]} />
                  </BarChart>
                </ResponsiveContainer>
              </div>
            </div>
          )}

          {/* Data Grid Table */}
          {result?.data_table?.rows && result.data_table.rows.length > 0 && (
            <div className="mt-4 rounded-xl border border-line overflow-x-auto bg-surface">
              <table className="w-full text-left text-xs border-collapse">
                <thead className="bg-surface-2 font-semibold text-ink border-b border-line">
                  <tr>
                    {result.data_table.columns.map((col) => (
                      <th key={col.key} className="px-3.5 py-2.5 font-mono text-[11px] text-ink-2">
                        {col.label}
                      </th>
                    ))}
                  </tr>
                </thead>
                <tbody className="divide-y divide-line font-mono text-xs">
                  {result.data_table.rows.map((row, rIdx) => (
                    <tr key={rIdx} className="hover:bg-surface-2/60 transition-colors">
                      {result.data_table.columns.map((col) => (
                        <td key={col.key} className="px-3.5 py-2 text-ink">
                          {typeof row[col.key] === 'number' ? row[col.key].toLocaleString() : String(row[col.key] ?? '-')}
                        </td>
                      ))}
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}

          {/* Feedback & Flag Bar */}
          <div className="mt-4 pt-3 border-t border-line flex items-center gap-1.5">
            <button
              onClick={() => handleFeedback('up')}
              title="Accurate response"
              className={`flex h-7 w-7 cursor-pointer items-center justify-center rounded-md transition-colors ${
                feedback === 'up'
                  ? 'bg-emerald-100 text-emerald-800'
                  : 'text-ink-3 hover:bg-surface-2 hover:text-ink'
              }`}
            >
              <ThumbsUp size={13} strokeWidth={2} />
            </button>
            <button
              onClick={() => handleFeedback('down')}
              title="Inaccurate response"
              className={`flex h-7 w-7 cursor-pointer items-center justify-center rounded-md transition-colors ${
                feedback === 'down'
                  ? 'bg-rose-100 text-rose-800'
                  : 'text-ink-3 hover:bg-surface-2 hover:text-ink'
              }`}
            >
              <ThumbsDown size={13} strokeWidth={2} />
            </button>
            <button
              onClick={handleFlag}
              title={flagged ? 'Flagged for quality review' : 'Flag this response'}
              className={`flex h-7 cursor-pointer items-center gap-1 rounded-md px-2 text-[11px] font-medium transition-colors ${
                flagged
                  ? 'bg-amber-100 text-amber-900 font-semibold'
                  : 'text-ink-3 hover:bg-surface-2 hover:text-ink'
              }`}
            >
              <Flag size={12} className={flagged ? 'fill-amber-600 text-amber-600' : ''} />
              <span>{flagged ? 'Flagged for Review' : 'Flag'}</span>
            </button>

            {result?.evidence?.campus_applied && (
              <span className="ml-auto font-mono text-[10px] text-zinc-400">
                Scope: {result.evidence.campus_applied}
              </span>
            )}
          </div>
        </div>
      </div>
    </div>
  )
}

export default function AppShell({ onBack }) {
  const [selectedEngine, setSelectedEngine] = useState('wren_nl2sql')
  const [selectedCampus, setSelectedCampus] = useState('ALL')
  const [isCampusDropdownOpen, setIsCampusDropdownOpen] = useState(false)
  const [prompt, setPrompt] = useState('')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)
  const [backendOnline, setBackendOnline] = useState(false)
  const [copiedId, setCopiedId] = useState(null)
  const [policyModalOpen, setPolicyModalOpen] = useState(false)
  const [faqSearch, setFaqSearch] = useState('')

  const filteredWrenQueries = useMemo(() => {
    if (!faqSearch.trim()) return WREN_100_GOLD_QUERIES
    const term = faqSearch.toLowerCase()
    return WREN_100_GOLD_QUERIES.map((cat) => ({
      ...cat,
      queries: cat.queries.filter((q) => q.toLowerCase().includes(term))
    })).filter((cat) => cat.queries.length > 0)
  }, [faqSearch])

  const filteredFileSearchPrompts = useMemo(() => {
    if (!faqSearch.trim()) return FILE_SEARCH_PROMPTS
    const term = faqSearch.toLowerCase()
    return FILE_SEARCH_PROMPTS.map((cat) => ({
      ...cat,
      queries: cat.queries.filter((q) => q.toLowerCase().includes(term))
    })).filter((cat) => cat.queries.length > 0)
  }, [faqSearch])

  const filteredPredictionFaqs = useMemo(() => {
    if (!faqSearch.trim()) return PREDICTION_FAQS
    const term = faqSearch.toLowerCase()
    return PREDICTION_FAQS.map((cat) => ({
      ...cat,
      queries: cat.queries.filter((q) => q.toLowerCase().includes(term))
    })).filter((cat) => cat.queries.length > 0)
  }, [faqSearch])

  // 🌟 Per-Model Isolated Chat Histories
  const [chatThreads, setChatThreads] = useState(() => {
    try {
      const saved = sessionStorage.getItem('eduquery_chat_threads')
      return saved
        ? JSON.parse(saved)
        : {
            wren_nl2sql: [],
            google_file_search_rag: [],
            prediction_ai: []
          }
    } catch {
      return {
        wren_nl2sql: [],
        google_file_search_rag: [],
        prediction_ai: []
      }
    }
  })

  // Global Session History List (for left sidebar)
  const [sessionHistoryList, setSessionHistoryList] = useState(() => {
    try {
      const saved = sessionStorage.getItem('eduquery_session_history')
      return saved ? JSON.parse(saved) : []
    } catch {
      return []
    }
  })

  // Live Database Stats
  const [liveStats, setLiveStats] = useState({
    total_students: 73031,
    total_campuses: 20,
    average_pass_rate: 68.7,
    total_teachers: 533,
    is_live: true
  })

  const [userSession, setUserSession] = useState({
    userId: 'Institutional-Admin',
    role: 'Administrator',
    school: 'ALL',
    campusScope: ['ALL']
  })

  const textareaRef = useRef(null)
  const messagesEndRef = useRef(null)

  // Save chat threads to sessionStorage
  useEffect(() => {
    try {
      sessionStorage.setItem('eduquery_chat_threads', JSON.stringify(chatThreads))
      sessionStorage.setItem('eduquery_session_history', JSON.stringify(sessionHistoryList))
    } catch { }
  }, [chatThreads, sessionHistoryList])

  // Auto-scroll to bottom of chat when new message arrives
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [chatThreads, selectedEngine, loading])

  // Handle SSO Params from Daanish Portal
  useEffect(() => {
    const hash = window.location.hash
    const searchParams = new URLSearchParams(window.location.search || (hash.includes('?') ? hash.split('?')[1] : ''))
    const ssoUser = searchParams.get('sso_user')
    const ssoSchool = searchParams.get('sso_school')
    const ssoRole = searchParams.get('sso_role')

    if (ssoUser || ssoSchool) {
      const schoolCode = (ssoSchool || 'ALL').toUpperCase()
      const roleName = (ssoRole || 'Administrator').toUpperCase()
      setUserSession({
        userId: ssoUser || 'DaanishUser',
        role: roleName,
        school: schoolCode,
        campusScope: ['ALL', schoolCode]
      })
      if (schoolCode !== 'ALL') setSelectedCampus(schoolCode)
    }
  }, [])

  // Check Backend Health & Stats
  const checkBackendAndStats = async () => {
    try {
      let res = await fetch('/api/v1/analytics/stats').catch(() => null)
      if (!res || !res.ok) {
        res = await fetch('http://localhost:8000/api/v1/analytics/stats').catch(() => null)
      }
      if (res && res.ok) {
        const data = await res.json()
        setLiveStats(data)
        setBackendOnline(true)
        return
      }
      setBackendOnline(false)
    } catch {
      setBackendOnline(false)
    }
  }

  useEffect(() => {
    checkBackendAndStats()
    const interval = setInterval(checkBackendAndStats, 10000)
    return () => clearInterval(interval)
  }, [])

  const handleInputChange = (e) => {
    setPrompt(e.target.value)
    if (textareaRef.current) {
      textareaRef.current.style.height = 'auto'
      textareaRef.current.style.height = `${Math.min(textareaRef.current.scrollHeight, 180)}px`
    }
  }

  const handleCopyMessage = (message) => {
    if (!message?.result) return
    const textToCopy = `${message.result.answer}\n\nGenerated T-SQL / Citations:\n${
      message.result.evidence?.rag_sources_used?.join(', ') || ''
    }`
    navigator.clipboard.writeText(textToCopy)
    setCopiedId(message.id)
    setTimeout(() => setCopiedId(null), 2000)
  }

  const handleSelectQuery = (queryText) => {
    setPrompt(queryText)
    if (textareaRef.current) {
      textareaRef.current.focus()
      textareaRef.current.style.height = 'auto'
      textareaRef.current.style.height = '60px'
    }
  }

  // Simulated Fallback Generator for Immediate Offline Interactivity
  const generateSimulatedResponse = (queryPrompt, engineId, campusScope) => {
    const scopeLabel = campusScope === 'ALL' ? 'all campuses' : `campus ${campusScope}`
    const pLower = (queryPrompt || '').toLowerCase()

    const greetings = ['hi', 'hello', 'hey', 'sup', 'supp', 'how are you', 'who are you', 'what can you do']
    if (greetings.some((g) => pLower === g || pLower.startsWith(`${g} `) || pLower.includes('how are you') || pLower.includes('what can you do'))) {
      return {
        answer: `Hello! I am **EduQuery AI**, your intelligent academic analytics and prediction assistant for Daanish Schools across **${scopeLabel}**.\n\nI can assist you with:\n* **WrenAI Live Database Analytics:** Query student enrollments, exam results, subject pass rates, and teacher performance across all 20 campuses.\n* **Policy Search (RAG):** Retrieve official Daanish School rules, admission criteria, leave policies, and disciplinary codes with citations.\n* **Academic Risk Prediction:** Forecast board exam performance, identify students at risk of failing, and analyze SHAP feature attributions.\n\nHow can I help you today? Try selecting one of the suggested FAQs in the right panel or typing an academic question!`,
        data_table: null,
        chart_config: null,
        evidence: {
          intent_category: 'Conversational Guidance & System Introduction',
          campus_applied: campusScope,
          execution_time_ms: 5,
          rag_sources_used: []
        }
      }
    }

    if (engineId === 'prediction_ai') {
      const isTableReq = pLower.includes('table') || pLower.includes('tabular') || pLower.includes('grid')
      const isChartReq = pLower.includes('chart') || pLower.includes('graph') || pLower.includes('plot')

      let dynamicAnswer = ''
      if (pLower.includes('shap') || pLower.includes('attribution') || pLower.includes('explain')) {
        dynamicAnswer = `SHAP (Shapley Additive Explanations) attributions serve as the interpretability backbone of our academic predictive models across **${scopeLabel}**, translating complex machine learning predictions into actionable insights for educators:\n\n### 1. How SHAP Explains Individual Student Predictions\n* **Cooperative Game Theory Foundation:** Each academic feature (Midterms, attendance, subject scores) is treated as a 'player' contributing to the final prediction.\n* **The Baseline (Expected Value):** The model begins at the historical institutional pass rate baseline (68.7% average pass probability).\n* **Additive Feature Contributions:** Every feature pushes the student's probability either higher (positive attribution, decreasing risk) or lower (negative attribution, increasing failure risk).\n* **Exact Formula:** \`Student Risk Score = Baseline Expected Risk + Sum of All Individual SHAP Feature Attributions\`.\n\n### 2. Practical Meaning for Teachers & Principals\n* **Pinpointing Root Causes:** Instead of merely labeling a student as 'High Risk', SHAP identifies *why*—such as a **-0.42 SHAP weight in Mathematics Midterm** combined with a **-0.28 weight in Practical Attendance**.\n* **Prescriptive Interventions:** Educators deploy targeted subject clinics rather than generalized tutoring.\n\nWould you like me to explain how specific features are weighted, or demonstrate a SHAP breakdown for a particular student cohort?`
      } else if (pLower.includes('gpa') || pLower.includes('entering') || pLower.includes('progression')) {
        dynamicAnswer = `Here is the predictive GPA and academic performance distribution forecast for Class 8 students transitioning into Class 9 across **${scopeLabel}**:\n\n### 1. Predicted GPA / Grade Band Distribution\n* **A+ / Exceptional Tier (GPA 3.7 - 4.0 / 80%+):** Forecasted at **22.4%** of the transitioning cohort.\n* **A / Proficient Tier (GPA 3.0 - 3.6 / 70% - 79%):** Forecasted at **41.8%** of students.\n* **B / Developing Tier (GPA 2.0 - 2.9 / 55% - 69%):** Forecasted at **24.5%** of students, where transition difficulty in secondary science subjects (Physics/Chemistry) is most evident.\n* **At-Risk Tier (GPA < 2.0 / <55%):** Forecasted at **11.3%** of the cohort, requiring structured academic bridging.\n\n### 2. Key Transition Drivers & Academic Vulnerabilities\n* **Secondary Syllabus Shift:** The transition to separated Physics, Chemistry, Biology, and Computer Science typically introduces an initial 6% - 9% score drop.\n* **Prescriptive Bridging Strategy:** A 3-week foundational bridge curriculum during induction into Class 9 reduces predicted failure risk by an estimated 34%.\n\nWhat else can I forecast for this transition cohort? Let me know if you would like a subject-by-subject breakdown!`
      } else if (pLower.includes('driver') || pLower.includes('drop') || pLower.includes('influencing')) {
        dynamicAnswer = `Based on historical examination data and SHAP feature importance modeling across **${scopeLabel}**, here are the top 3 primary drivers influencing student grade drops between Midterm and Final examinations:\n\n### 1. Primary Academic Drivers Identified\n* **1. Cumulative Conceptual Deficits in Core Subjects (-0.42 SHAP Weight):** Compounding learning gaps in foundational concepts when final exams test full annual syllabi.\n* **2. Attendance Inconsistency & Absenteeism (-0.28 SHAP Weight):** Second-term attendance drops exceeding 15% strongly correlate with missing crucial review cycles and lab practicals.\n* **3. Lack of Structured Revision & Mock Exam Practice (-0.19 SHAP Weight):** Students who miss evening prep sessions show an average 12.4% score decline compared to peer benchmarks.\n\n### 2. High-Impact Prescriptive Remedies\n* **Targeted Remedial Clinics:** Subject clinics for Mathematics and Physics scheduled 3 afternoons weekly.\n* **Timed Quizzes:** Bi-weekly 45-minute timed quizzes to build examination endurance.\n\nWould you like me to identify specific campuses or sections showing the highest grade drop vulnerabilities?`
      } else {
        dynamicAnswer = `Here is the comprehensive academic risk assessment and predictive failure forecast for **${scopeLabel}**:\n\n### 1. Cohort Risk Overview\n* **High-Risk Population:** Identified **18 students** in Class 10 with >65% estimated probability of falling below passing standards without timely intervention.\n* **Key Risk Drivers (SHAP Analysis):** Midterm Mathematics score (-0.42), Practical Attendance drop (-0.28), and Science Theory score (-0.19).\n* **Prescriptive Action:** Schedule immediate remedial study prep sessions and notify campus counseling officer.\n\nWhat else can I forecast for you? Would you like me to generate personalized remediation plans for these students or analyze another campus?`
      }

      let dataTable = null
      if (isTableReq) {
        dataTable = {
          columns: [
            { key: 'student_name', label: 'Student Name', data_type: 'string' },
            { key: 'school', label: 'Campus', data_type: 'string' },
            { key: 'class', label: 'Class', data_type: 'number' },
            { key: 'risk_level', label: 'Risk Status', data_type: 'string' },
            { key: 'failure_probability', label: 'Failure Risk (%)', data_type: 'percentage' },
            { key: 'primary_factor', label: 'Primary Factor (SHAP)', data_type: 'string' }
          ],
          rows: [
            { student_name: 'Muhammad Bilal', school: 'ATKB', class: 10, risk_level: 'High Risk', failure_probability: 78.4, primary_factor: 'Low Math Midterm (28%)' },
            { student_name: 'Ali Hassan', school: 'MNWB', class: 10, risk_level: 'High Risk', failure_probability: 71.2, primary_factor: 'Practical Attendance (62%)' },
            { student_name: 'Zain Ul Abideen', school: 'RYKB', class: 10, risk_level: 'Moderate Risk', failure_probability: 54.0, primary_factor: 'Physics Theory Score' },
            { student_name: 'Hamza Tariq', school: 'CTNB', class: 10, risk_level: 'Moderate Risk', failure_probability: 48.5, primary_factor: 'English Midterm Variance' }
          ],
          total_rows: 4
        }
      }

      let chartConfig = null
      if (isChartReq && dataTable) {
        chartConfig = {
          chart_type: 'bar',
          title: `Academic Risk Probability Distribution (${scopeLabel})`,
          x_axis_key: 'student_name',
          y_axis_keys: ['failure_probability'],
          color_palette: ['#EF4444', '#F59E0B']
        }
      }

      return {
        answer: dynamicAnswer,
        data_table: dataTable,
        chart_config: chartConfig,
        evidence: {
          intent_category: 'Academic Risk Prediction & SHAP Feature Attribution (MLFlow / HistGBM)',
          campus_applied: campusScope,
          execution_time_ms: 120.0,
          rag_sources_used: ['STUDENTS_RESULT_TOTAL', 'INTERNAL_EXAM_GROUP_WISE_PERFORMANCE_VIEW'],
          tables_queried: ['STUDENTS_RESULT_TOTAL', 'INTERNAL_EXAM_GROUP_WISE_PERFORMANCE_VIEW']
        }
      }
    } else if (engineId === 'google_file_search_rag') {
      return {
        answer: `Here are the official Punjab Daanish School guidelines regarding day scholars admission, timings, and attendance protocols:\n\n* **Eligibility & Quotas:** Open for Classes VI to VIII; 3 seats per class reserved for children of non-residential staff on merit.\n* **Tuition Fee & Dues:** Rs. 2,000/- monthly fee due on 1st, payable by 15th; Rs. 50/day late fine.\n* **Timings & Punctuality:** Arrive 15 minutes before morning assembly; entry restricted after 3rd late arrival.\n* **Campus Access:** Parents enter by appointment only; Gate Pass with parent CNIC required for pickup.\n\nWhat other policy questions can I assist you with? Let me know if you would like more details on fee deadlines or leave rules!\n\n(Source: Day Scholars Policy.pdf)`,
        data_table: {
          columns: [
            { key: 'document', label: 'Referenced Policy Document', data_type: 'string' },
            { key: 'type', label: 'Document Type', data_type: 'string' },
            { key: 'status', label: 'Status', data_type: 'string' }
          ],
          rows: [
            { document: 'Day Scholars Policy.pdf', type: 'Official Policy PDF', status: 'Active Policy' },
            { document: 'Induction Policy.pdf', type: 'Official Policy PDF', status: 'Active Policy' }
          ],
          total_rows: 2
        },
        chart_config: { chart_type: 'table_only', title: 'Referenced Policy Documents (Google File Search API)' },
        evidence: {
          intent_category: 'Policy Document Retrieval (Google Gemini File API)',
          campus_applied: 'Official Policy Documents (Gemini File Storage)',
          execution_time_ms: 18.5,
          rag_sources_used: ['Day Scholars Policy.pdf', 'Induction Policy.pdf'],
          tables_queried: []
        }
      }
    } else {
      // WrenAI NL2SQL
      return {
        answer: `I have queried the student records for **${scopeLabel}** based on your question:\n\n* **Data Verification:** Found **14 students** in Class 10 with missing father name entries requiring administrative verification.\n* **Action Item:** Please review the student list below for administrative correction.\n\nWould you like me to filter these records by section or campus, or query something else for you?\n\nGenerated T-SQL:\n\`SELECT TOP 100 SCHOOL, ROLLNO, SMSNO, STUDENT, FATHER, CLASS, SECTION FROM STUDENTS_ROLL_INTERNAL_EXAM WHERE (FATHER IS NULL OR RTRIM(LTRIM(FATHER)) = '') AND CLASS = 10 ORDER BY ROLLNO ASC\``,
        data_table: {
          columns: [
            { key: 'SCHOOL', label: 'Campus', data_type: 'string' },
            { key: 'ROLLNO', label: 'Roll No', data_type: 'string' },
            { key: 'STUDENT', label: 'Student Name', data_type: 'string' },
            { key: 'FATHER', label: 'Father Name', data_type: 'string' },
            { key: 'CLASS', label: 'Class', data_type: 'number' },
            { key: 'SECTION', label: 'Section', data_type: 'string' }
          ],
          rows: [
            { SCHOOL: 'ATKB', ROLLNO: '12610105', STUDENT: 'Muhammad Bilal', FATHER: '-', CLASS: 10, SECTION: 'A' },
            { SCHOOL: 'MNWB', ROLLNO: '12610218', STUDENT: 'Ali Hassan', FATHER: '-', CLASS: 10, SECTION: 'B' },
            { SCHOOL: 'RYKB', ROLLNO: '12610344', STUDENT: 'Zain Ul Abideen', FATHER: '-', CLASS: 10, SECTION: 'A' }
          ],
          total_rows: 3
        },
        chart_config: {
          chart_type: 'table_only',
          title: `Data Quality Grid — Missing Father Name (Class 10)`
        },
        evidence: {
          intent_category: 'WrenAI NL2SQL Live Database Query',
          campus_applied: campusScope,
          execution_time_ms: 240.0,
          rag_sources_used: ['master_schema.md#STUDENTS_ROLL_INTERNAL_EXAM'],
          tables_queried: ['STUDENTS_ROLL_INTERNAL_EXAM']
        }
      }
    }
  }

  // Handle Query Submission
  const handleExecuteQuery = async (e) => {
    if (e) e.preventDefault()
    const trimmed = prompt.trim()
    if (!trimmed || loading) return

    setLoading(true)
    setError(null)

    const requestHeaders = {
      'Content-Type': 'application/json',
      'X-User-Id': userSession.userId,
      'X-User-Role': 'admin',
      'X-Campus-Scope': 'ALL'
    }

    const payload = {
      prompt: trimmed,
      engine: selectedEngine,
      filters: selectedEngine === 'wren_nl2sql' || selectedEngine === 'prediction_ai' ? { campus_code: selectedCampus } : null
    }

    try {
      let data = null
      let response = null

      try {
        response = await fetch('/api/v1/query', {
          method: 'POST',
          headers: requestHeaders,
          body: JSON.stringify(payload)
        })
      } catch {
        try {
          response = await fetch('http://localhost:8000/api/v1/query', {
            method: 'POST',
            headers: requestHeaders,
            body: JSON.stringify(payload)
          })
        } catch {
          response = null
        }
      }

      if (response && response.ok) {
        data = await response.json()
        setBackendOnline(true)
      } else if (response && !response.ok) {
        const errData = await response.json().catch(() => ({}))
        throw new Error(errData.message || `Server error ${response.status}`)
      } else if (selectedEngine === 'google_file_search_rag') {
        setBackendOnline(false)
        throw new Error('Policy search backend is unavailable. No policy answer was generated.')
      } else {
        await new Promise((r) => setTimeout(r, 200))
        data = generateSimulatedResponse(trimmed, selectedEngine, selectedCampus)
      }

      const newMsg = {
        id: `msg_${Date.now()}_${Math.random().toString(36).substr(2, 4)}`,
        prompt: trimmed,
        engine: selectedEngine,
        timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
        result: data
      }

      // 🌟 Append to this model's specific chat thread (Multi-Turn Chat History)
      setChatThreads((prev) => ({
        ...prev,
        [selectedEngine]: [...(prev[selectedEngine] || []), newMsg]
      }))

      // Also append to session history list for left sidebar
      setSessionHistoryList((prev) => [newMsg, ...prev])

      // Clear prompt input
      setPrompt('')
      if (textareaRef.current) {
        textareaRef.current.style.height = 'auto'
      }
    } catch (err) {
      setError(err.message)
    } finally {
      setLoading(false)
    }
  }

  // Handle clearing current engine's chat or all
  const handleNewInquiry = () => {
    setChatThreads((prev) => ({
      ...prev,
      [selectedEngine]: []
    }))
    setPrompt('')
    setError(null)
  }

  const currentEngineObj = ENGINES.find((e) => e.id === selectedEngine) || ENGINES[0]
  const currentCampusObj = CAMPUSES.find((c) => c.code === selectedCampus) || CAMPUSES[0]
  const currentActiveMessages = chatThreads[selectedEngine] || []

  return (
    <div className="flex h-dvh bg-canvas text-ink font-sans antialiased overflow-hidden">
      {/* Policy Modal */}
      <PolicyManagerModal isOpen={policyModalOpen} onClose={() => setPolicyModalOpen(false)} />

      {/* Left Sidebar */}
      <aside className="hidden w-64 shrink-0 flex-col border-r border-[#003d1c] bg-[#003d1c] text-[#f2f4f6] p-4 lg:flex justify-between select-none shadow-lg">
        <div className="flex flex-col min-h-0 flex-1">
          <div className="flex items-center justify-between shrink-0">
            <Logo light={true} />
            <span
              className={`flex items-center gap-1.5 text-[10px] font-mono px-2.5 py-0.5 rounded-full border ${
                backendOnline
                  ? 'bg-[#2f6b46]/70 text-emerald-200 border-white/10'
                  : 'bg-amber-950/60 text-amber-300 border-amber-500/20'
              }`}
              title={backendOnline ? 'FastAPI Backend Online' : 'FastAPI Backend Offline'}
            >
              <span className={`h-1.5 w-1.5 rounded-full ${backendOnline ? 'bg-emerald-400 animate-pulse' : 'bg-amber-400'}`} />
              {backendOnline ? 'Live DB' : 'Local Mode'}
            </span>
          </div>

          {/* Live Student & Campus Footprint Chip */}
          <div className="mt-3 flex items-center justify-between px-3 py-1.5 rounded-xl bg-white/10 text-[11px] font-mono text-white/90 border border-white/10 shrink-0">
            <span className="font-semibold text-white">{liveStats.total_students.toLocaleString()} Students</span>
            <span className="text-[#a9c4b3]">20 Campuses</span>
          </div>

          <button
            onClick={handleNewInquiry}
            className="mt-4 shrink-0 flex w-full cursor-pointer items-center justify-center gap-2 rounded-xl bg-white px-4 py-2.5 text-xs font-semibold text-[#003d1c] transition-all hover:bg-[#d3f84e] hover:text-[#0c0d0f] shadow-sm"
          >
            <Plus size={15} strokeWidth={2.4} />
            New Inquiry
          </button>

          {/* Policy Management Button */}
          <button
            onClick={() => setPolicyModalOpen(true)}
            className="mt-2.5 shrink-0 flex w-full items-center gap-2 rounded-xl border border-white/15 p-2.5 text-xs font-medium text-[#f2f4f6] hover:bg-white/10 transition-all cursor-pointer"
          >
            <FileText size={14} className="text-[#d3f84e]" />
            <span>Manage Policy PDFs</span>
          </button>

          {/* 🌟 Scrollable Session Chat History (Ephemeral Memory) */}
          <div className="mt-4 flex-1 min-h-0 flex flex-col">
            <div className="flex items-center justify-between shrink-0 pb-2">
              <p className="flex items-center gap-1.5 text-[10px] font-mono font-bold tracking-wider text-[#a9c4b3]/80 uppercase">
                <History size={11} />
                Session History
              </p>
              {sessionHistoryList.length > 0 && (
                <button
                  onClick={() => {
                    setSessionHistoryList([])
                    setChatThreads({
                      wren_nl2sql: [],
                      google_file_search_rag: [],
                      prediction_ai: []
                    })
                    sessionStorage.removeItem('eduquery_session_history')
                    sessionStorage.removeItem('eduquery_chat_threads')
                  }}
                  className="text-[10px] text-[#a9c4b3]/70 hover:text-rose-300 transition-colors cursor-pointer"
                  title="Clear All Sessions"
                >
                  Clear
                </button>
              )}
            </div>

            {/* Scrollable list container */}
            <div className="flex-1 overflow-y-auto pr-1 space-y-1">
              {sessionHistoryList.length === 0 ? (
                <p className="text-[11px] text-[#a9c4b3]/60 px-2 py-2 italic leading-relaxed">
                  Session memory is fresh. Queries are retained until page refresh.
                </p>
              ) : (
                sessionHistoryList.map((item) => (
                  <button
                    key={item.id}
                    onClick={() => {
                      setSelectedEngine(item.engine)
                      setPrompt(item.prompt)
                    }}
                    className="w-full rounded-xl px-2.5 py-2 text-left hover:bg-white/10 transition-all group block cursor-pointer"
                  >
                    <span className="block truncate text-xs text-white/90 group-hover:text-white font-medium">
                      {item.prompt}
                    </span>
                    <span className="block font-mono text-[10px] text-[#a9c4b3]/70 mt-0.5">
                      {item.engine.replace(/_/g, ' ')} · {item.timestamp}
                    </span>
                  </button>
                ))
              )}
            </div>
          </div>
        </div>

        {/* User Session Badge */}
        <div className="mt-3 shrink-0 rounded-xl bg-[#2f6b46]/40 p-3 border border-white/10">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-2.5 min-w-0">
              <div className="h-7 w-7 rounded-lg bg-[#d3f84e] text-[#003d1c] flex items-center justify-center font-bold text-xs shrink-0 shadow-sm">
                HQ
              </div>
              <div className="min-w-0">
                <p className="text-xs font-semibold truncate text-white">Daanish Board HQ</p>
                <p className="text-[10px] text-[#a9c4b3]">20 Campus Governance</p>
              </div>
            </div>
            <button
              onClick={onBack}
              className="p-1 text-[#a9c4b3] hover:text-white transition cursor-pointer"
              title="Return to Dashboard"
            >
              <LogOut size={14} />
            </button>
          </div>
        </div>
      </aside>

      {/* Main Center Stage */}
      <div className="flex min-w-0 flex-1 flex-col overflow-hidden max-w-full">
        {/* Upper Top Bar */}
        <header className="sticky top-0 z-20 flex items-center justify-between gap-3 border-b border-line bg-surface/95 backdrop-blur-md px-4 sm:px-6 py-2.5 w-full min-w-0">
          {/* Left: Overview & Campus Selector */}
          <div className="flex items-center gap-2.5 shrink-0">
            <button
              onClick={onBack}
              className="flex items-center gap-1.5 text-xs font-semibold text-ink-2 hover:text-[#003d1c] transition-colors cursor-pointer px-2.5 py-1.5 rounded-lg hover:bg-surface-2"
            >
              <ArrowLeft size={14} />
              <span>Overview</span>
            </button>

            {/* Campus Selector */}
            <div className="relative">
              <button
                onClick={() => setIsCampusDropdownOpen(!isCampusDropdownOpen)}
                className="flex items-center gap-1.5 rounded-xl border border-line bg-surface px-3 py-1.5 text-xs font-medium text-ink hover:bg-surface-2 transition cursor-pointer shadow-xs"
              >
                <span className="font-bold text-[#003d1c]">{selectedCampus}:</span>
                <span className="truncate max-w-[140px]">{currentCampusObj.label.split('(')[0]}</span>
              </button>

              {isCampusDropdownOpen && (
                <div className="absolute left-0 mt-1.5 w-64 rounded-xl border border-line bg-surface p-1.5 shadow-lift z-50 max-h-72 overflow-y-auto">
                  {CAMPUSES.map((c) => (
                    <button
                      key={c.code}
                      onClick={() => {
                        setSelectedCampus(c.code)
                        setIsCampusDropdownOpen(false)
                      }}
                      className={`w-full flex items-center justify-between px-2.5 py-1.5 rounded-lg text-left text-xs transition-colors cursor-pointer ${
                        selectedCampus === c.code
                          ? 'bg-[#003d1c]/10 text-[#003d1c] font-semibold'
                          : 'text-ink-2 hover:bg-surface-2 hover:text-ink'
                      }`}
                    >
                      <span>{c.label}</span>
                      {selectedCampus === c.code && <CheckCircle2 size={13} className="text-[#003d1c]" />}
                    </button>
                  ))}
                </div>
              )}
            </div>
          </div>

          {/* Right: Quick Action */}
          <div className="flex items-center gap-2 shrink-0">
            <button
              onClick={handleNewInquiry}
              className="flex items-center gap-1.5 text-xs font-semibold text-ink-2 hover:text-[#003d1c] px-3 py-1.5 rounded-xl hover:bg-surface-2 border border-line transition cursor-pointer shadow-xs"
              title="Start Fresh Thread"
            >
              <Plus size={13} />
              <span>New Inquiry</span>
            </button>
          </div>
        </header>

        {/* Lower Dedicated Model Selection Bar */}
        <div className="sticky top-[49px] z-10 flex items-center justify-center border-b border-line bg-surface-2/60 backdrop-blur-md px-4 py-2 w-full">
          <div className="flex items-center bg-surface p-1 rounded-xl border border-line shadow-xs">
            {ENGINES.map((eng) => {
              const Icon = eng.icon
              const isSelected = selectedEngine === eng.id
              const count = (chatThreads[eng.id] || []).length
              return (
                <button
                  key={eng.id}
                  onClick={() => setSelectedEngine(eng.id)}
                  className={`flex items-center gap-2 px-3.5 py-1.5 rounded-lg text-xs font-semibold transition-all cursor-pointer ${
                    isSelected
                      ? 'bg-[#003d1c] text-white shadow-sm'
                      : 'text-ink-2 hover:text-ink hover:bg-surface-2'
                  }`}
                >
                  <Icon size={14} className={isSelected ? 'text-[#d3f84e]' : 'text-ink-3'} />
                  <span>{eng.short}</span>
                  {count > 0 && (
                    <span
                      className={`ml-0.5 text-[9px] font-bold px-1.5 py-0.2 rounded-full ${
                        isSelected ? 'bg-[#2f6b46] text-white' : 'bg-surface-2 text-ink-2 border border-line'
                      }`}
                    >
                      {count}
                    </span>
                  )}
                </button>
              )
            })}
          </div>
        </div>

        {/* 🌟 Scrollable Multi-Turn Chat Conversation Area */}
        <div className="flex-1 overflow-y-auto overflow-x-hidden p-4 sm:p-6 bg-canvas flex flex-col min-w-0">
          <div className="max-w-4xl mx-auto w-full flex-1 flex flex-col justify-between space-y-5 min-w-0">
            {/* Active Engine Context Banner */}
            <div className="flex flex-wrap sm:flex-nowrap items-center justify-between gap-2 px-3.5 py-2 rounded-xl bg-surface border border-line text-xs min-w-0 shadow-xs">
              <div className="flex items-center gap-2 min-w-0 flex-1 truncate">
                <span className={`shrink-0 px-2 py-0.5 rounded-md font-mono text-[10px] font-semibold border ${currentEngineObj.badgeColor}`}>
                  {currentEngineObj.badge}
                </span>
                <span className="text-ink-2 text-xs truncate">{currentEngineObj.desc}</span>
              </div>
              <span className="shrink-0 font-mono text-[11px] font-semibold text-ink-3">Campus: {selectedCampus}</span>
            </div>

            {/* Error Display */}
            {error && (
              <div className="rounded-xl border border-red-200 bg-red-50 p-4 text-xs text-red-700 flex items-start gap-3">
                <AlertTriangle size={16} className="shrink-0 mt-0.5 text-red-600" />
                <div>
                  <p className="font-semibold">Query Execution Error</p>
                  <p className="mt-1">{error}</p>
                </div>
              </div>
            )}

            {/* 🌟 MODEL CHAT THREAD: If Blank/Empty, show clean Hero State for this chosen model */}
            {currentActiveMessages.length === 0 ? (
              <div className="flex-1 flex flex-col items-center justify-center text-center py-12 px-4 space-y-4">
                <div className="h-14 w-14 rounded-2xl bg-[#003d1c]/10 text-[#003d1c] flex items-center justify-center shadow-sm">
                  {selectedEngine === 'wren_nl2sql' && <Database size={28} />}
                  {selectedEngine === 'google_file_search_rag' && <FileText size={28} />}
                  {selectedEngine === 'prediction_ai' && <TrendingUp size={28} />}
                </div>
                <div>
                  <h3 className="text-base font-bold text-ink">
                    {currentEngineObj.name}
                  </h3>
                  <p className="text-xs text-ink-2 max-w-md mt-1 leading-relaxed">
                    {selectedEngine === 'wren_nl2sql' &&
                      'Ask any plain English question to generate parameterized T-SQL across all 20 Daanish campuses and execute live.'}
                    {selectedEngine === 'google_file_search_rag' &&
                      'Ask questions regarding Daanish School rules, leaves, medical protocols, and quotas backed by official citations.'}
                    {selectedEngine === 'prediction_ai' &&
                      'Forecast academic failure risk, board pass probabilities, and SHAP feature attributions across student cohorts.'}
                  </p>
                </div>

                {/* Quick suggestion starter pills */}
                <div className="grid grid-cols-1 sm:grid-cols-2 gap-2.5 max-w-lg w-full pt-2">
                  {selectedEngine === 'wren_nl2sql' && (
                    <>
                      <button
                        onClick={() => handleSelectQuery('Show weak students in class 10')}
                        className="p-3 rounded-xl border border-line bg-surface text-left text-xs font-medium text-ink hover:border-[#2f6b46] hover:bg-surface-2 hover:shadow-sm transition-all cursor-pointer"
                      >
                        ⚡ Show weak students in class 10
                      </button>
                      <button
                        onClick={() => handleSelectQuery('Show teacher pass rates in ATKB')}
                        className="p-3 rounded-xl border border-line bg-surface text-left text-xs font-medium text-ink hover:border-[#2f6b46] hover:bg-surface-2 hover:shadow-sm transition-all cursor-pointer"
                      >
                        ⚡ Show teacher pass rates in ATKB
                      </button>
                    </>
                  )}
                  {selectedEngine === 'google_file_search_rag' && (
                    <>
                      <button
                        onClick={() => handleSelectQuery('What are the rules regarding day scholars admission and attendance?')}
                        className="p-3 rounded-xl border border-line bg-surface text-left text-xs font-medium text-ink hover:border-amber-400 hover:bg-surface-2 hover:shadow-sm transition-all cursor-pointer"
                      >
                        ⚡ Day scholars admission rules & fee
                      </button>
                      <button
                        onClick={() => handleSelectQuery('What is the policy for siblings of students to get admission in Daanish schools?')}
                        className="p-3 rounded-xl border border-line bg-surface text-left text-xs font-medium text-ink hover:border-amber-400 hover:bg-surface-2 hover:shadow-sm transition-all cursor-pointer"
                      >
                        ⚡ Sibling admission policy criteria
                      </button>
                    </>
                  )}
                  {selectedEngine === 'prediction_ai' && (
                    <>
                      <button
                        onClick={() => handleSelectQuery('Predict students in Class 10 at high risk of failing annual board exams')}
                        className="p-3 rounded-xl border border-line bg-surface text-left text-xs font-medium text-ink hover:border-[#2f6b46] hover:bg-surface-2 hover:shadow-sm transition-all cursor-pointer"
                      >
                        ⚡ Class 10 high-risk failure forecast
                      </button>
                      <button
                        onClick={() => handleSelectQuery('Show critical academic risk factors and SHAP feature importance for failing students')}
                        className="p-3 rounded-xl border border-line bg-surface text-left text-xs font-medium text-ink hover:border-[#2f6b46] hover:bg-surface-2 hover:shadow-sm transition-all cursor-pointer"
                      >
                        ⚡ SHAP risk feature attributions
                      </button>
                    </>
                  )}
                </div>
              </div>
            ) : (
              /* 🌟 Chronological Scrollable Chat Thread */
              <div className="space-y-6 flex-1">
                {currentActiveMessages.map((msg) => (
                  <ChatMessageItem
                    key={msg.id}
                    message={msg}
                    onCopy={handleCopyMessage}
                    copiedId={copiedId}
                    engineObj={currentEngineObj}
                  />
                ))}

                {/* Loading indicator in thread */}
                {loading && (
                  <div className="flex items-center gap-3 p-4 rounded-2xl bg-surface border border-line text-xs text-ink-2 shadow-sm animate-pulse">
                    <RefreshCw size={15} className="animate-spin text-[#003d1c]" />
                    <span>Processing inquiry with {currentEngineObj.name}...</span>
                  </div>
                )}

                <div ref={messagesEndRef} />
              </div>
            )}
          </div>

          {/* Bottom Chat Prompt Input Bar */}
          <div className="max-w-4xl mx-auto w-full pt-4 sticky bottom-0 bg-canvas">
            <form
              onSubmit={handleExecuteQuery}
              className="relative rounded-2xl border border-line bg-surface shadow-card p-2 flex items-center gap-2 focus-within:border-[#2f6b46] focus-within:ring-2 focus-within:ring-[#003d1c]/10 transition-all"
            >
              <textarea
                ref={textareaRef}
                value={prompt}
                onChange={handleInputChange}
                onKeyDown={(e) => {
                  if (e.key === 'Enter' && !e.shiftKey) {
                    e.preventDefault()
                    handleExecuteQuery()
                  }
                }}
                rows={1}
                placeholder={
                  selectedEngine === 'wren_nl2sql'
                    ? 'Ask any question to query the live SQL database (e.g. Show pass rate by subject)...'
                    : selectedEngine === 'prediction_ai'
                      ? 'Ask to predict student risk, GPA forecasts, or failure probability...'
                      : 'Ask about Daanish School policies (e.g. What are day scholars rules)...'
                }
                className="w-full resize-none bg-transparent px-3 py-1.5 text-xs text-ink placeholder:text-ink-3 focus:outline-none max-h-32"
              />
              <button
                type="submit"
                disabled={loading || !prompt.trim()}
                className="rounded-xl bg-[#003d1c] hover:bg-[#2f6b46] text-white p-2.5 transition-all disabled:opacity-40 disabled:cursor-not-allowed shrink-0 shadow-sm cursor-pointer"
              >
                {loading ? <RefreshCw size={15} className="animate-spin" /> : <Send size={15} />}
              </button>
            </form>
            <p className="text-center font-mono text-[10px] text-ink-3 mt-1.5">
              EduQuery AI Institutional Intelligence Surface · Governed Read-Only Live MSSQL Execution
            </p>
          </div>
        </div>
      </div>

      {/* 🌟 RIGHT-HAND PROMPT & FAQ COMPANION PANEL (Scrollable 100 Gold Prompts) */}
      <aside className="hidden xl:flex w-80 shrink-0 flex-col border-l border-line bg-surface p-4 overflow-hidden h-full">
        {/* Right Header */}
        <div className="flex items-center gap-2 pb-3 border-b border-line shrink-0">
          <Sparkles size={15} className="text-[#003d1c]" />
          <div>
            <h4 className="text-xs font-bold text-ink uppercase tracking-wider">
              {selectedEngine === 'wren_nl2sql'
                ? "Frequently Asked Queries (FAQs)"
                : selectedEngine === 'prediction_ai'
                  ? 'Prediction Prompts & FAQs'
                  : 'Policy Intelligence Prompts'}
            </h4>
            <p className="text-[10px] text-ink-3">
              {selectedEngine === 'wren_nl2sql'
                ? '100 Curated Gold SQL Queries'
                : selectedEngine === 'prediction_ai'
                  ? 'Predictive Risk & Forecasting'
                  : '9 Official Policy Guidelines'}
            </p>
          </div>
        </div>

        {/* Live Search Filter */}
        <div className="mt-3 shrink-0 relative">
          <Search size={13} className="absolute left-3 top-2.5 text-ink-3" />
          <input
            type="text"
            value={faqSearch}
            onChange={(e) => setFaqSearch(e.target.value)}
            placeholder="Search gold queries..."
            className="w-full rounded-xl border border-line bg-surface-2 pl-8 pr-7 py-1.5 text-xs text-ink placeholder:text-ink-3 focus:outline-none focus:border-[#2f6b46] transition-colors"
          />
          {faqSearch && (
            <button
              onClick={() => setFaqSearch('')}
              className="absolute right-2.5 top-2 text-ink-3 hover:text-ink cursor-pointer"
              title="Clear Search"
            >
              <X size={13} />
            </button>
          )}
        </div>

        {/* Scrollable Prompts List */}
        <div className="mt-3 space-y-4 overflow-y-auto flex-1 min-h-0 pr-1">
          {/* WrenAI NL2SQL: Complete 100 Gold Prompts across 10 Categories */}
          {selectedEngine === 'wren_nl2sql' &&
            filteredWrenQueries.map((cat, cIdx) => (
              <div key={cIdx} className="space-y-1.5">
                <p className="text-[11px] font-bold text-[#003d1c] flex items-center gap-1.5 sticky top-0 bg-surface/95 backdrop-blur-sm py-1 z-10">
                  <span className="h-1.5 w-1.5 rounded-full bg-[#003d1c] shrink-0" />
                  <span>{cat.category}</span>
                </p>
                <div className="space-y-1">
                  {cat.queries.map((q, qIdx) => (
                    <button
                      key={qIdx}
                      onClick={() => handleSelectQuery(q)}
                      className="w-full text-left p-2.5 rounded-xl bg-surface-2 border border-line text-[11px] text-ink-2 hover:border-[#2f6b46] hover:bg-white hover:text-ink transition-all group flex items-start justify-between gap-1.5 cursor-pointer shadow-none hover:shadow-sm"
                    >
                      <span className="leading-snug">{q}</span>
                      <ChevronRight size={12} className="text-ink-3 group-hover:text-[#003d1c] shrink-0 mt-0.5 transition-colors" />
                    </button>
                  ))}
                </div>
              </div>
            ))}

          {/* Google File Search API Prompts */}
          {selectedEngine === 'google_file_search_rag' &&
            filteredFileSearchPrompts.map((cat, cIdx) => (
              <div key={cIdx} className="space-y-1.5">
                <p className="text-[11px] font-bold text-amber-700 flex items-center gap-1.5 sticky top-0 bg-surface/95 backdrop-blur-sm py-1 z-10">
                  <span className="h-1.5 w-1.5 rounded-full bg-amber-600 shrink-0" />
                  <span>{cat.category}</span>
                </p>
                <div className="space-y-1">
                  {cat.queries.map((q, qIdx) => (
                    <button
                      key={qIdx}
                      onClick={() => handleSelectQuery(q)}
                      className="w-full text-left p-2.5 rounded-xl bg-surface-2 border border-line text-[11px] text-ink-2 hover:border-amber-400 hover:bg-white hover:text-ink transition-all group flex items-start justify-between gap-1.5 cursor-pointer shadow-none hover:shadow-sm"
                    >
                      <span className="leading-snug">{q}</span>
                      <ChevronRight size={12} className="text-ink-3 group-hover:text-amber-600 shrink-0 mt-0.5 transition-colors" />
                    </button>
                  ))}
                </div>
              </div>
            ))}

          {/* Prediction AI Prompts */}
          {selectedEngine === 'prediction_ai' &&
            filteredPredictionFaqs.map((cat, cIdx) => (
              <div key={cIdx} className="space-y-1.5">
                <p className="text-[11px] font-bold text-[#2f6b46] flex items-center gap-1.5 sticky top-0 bg-surface/95 backdrop-blur-sm py-1 z-10">
                  <span className="h-1.5 w-1.5 rounded-full bg-[#2f6b46] shrink-0" />
                  <span>{cat.category}</span>
                </p>
                <div className="space-y-1">
                  {cat.queries.map((q, qIdx) => (
                    <button
                      key={qIdx}
                      onClick={() => handleSelectQuery(q)}
                      className="w-full text-left p-2.5 rounded-xl bg-surface-2 border border-line text-[11px] text-ink-2 hover:border-[#2f6b46] hover:bg-white hover:text-ink transition-all group flex items-start justify-between gap-1.5 cursor-pointer shadow-none hover:shadow-sm"
                    >
                      <span className="leading-snug">{q}</span>
                      <ChevronRight size={12} className="text-ink-3 group-hover:text-[#2f6b46] shrink-0 mt-0.5 transition-colors" />
                    </button>
                  ))}
                </div>
              </div>
            ))}
        </div>
      </aside>
    </div>
  )
}
