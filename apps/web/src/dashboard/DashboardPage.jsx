import { useState, useMemo } from 'react'
import {
  AlertTriangle,
  Percent,
  School,
  Target,
  ArrowRight,
  Sparkles,
  BookOpen,
  Users,
  CheckCircle2,
  TrendingUp,
  Search,
  ChevronRight,
  ShieldCheck,
  Building2,
  Menu,
} from 'lucide-react'
import PageHeader from './PageHeader'
import Sidebar from './Sidebar'
import { Delta, Figure } from '../components/ui'
import { ChartAnswer, AtRiskAnswer } from '../app/ChartPanels'
import { PredictionAnswer, TableAnswer } from '../app/AnswerPanels'
import {
  HistoricalPerformanceCard,
  PassProbabilityCard,
  PerformanceTrendCard,
  RiskDonutCard,
  SubjectComparisonCard,
  ShapAttributionCard,
  CampusBenchmarkCard,
} from './DashboardCharts'
import { useReveal } from '../lib/useReveal'
import { networkOverview, campusStats } from '../lib/analyticsData'

function KpiCard({ icon: Icon, label, value, unit, delta, positive, prompt, onAsk, subtitle }) {
  return (
    <div data-reveal className="tile group rounded-2xl p-5 relative flex flex-col justify-between border border-line bg-surface shadow-sm hover:shadow-card transition-all">
      <div>
        <div className="flex items-center justify-between gap-2">
          <span className="flex h-9 w-9 items-center justify-center rounded-xl bg-[#003d1c]/10 text-[#003d1c] shadow-xs">
            <Icon size={17} strokeWidth={2.2} aria-hidden="true" />
          </span>
          {delta && <Delta value={delta} positive={positive} />}
        </div>
        <Figure className="mt-4 text-[1.875rem] font-bold text-ink" value={value} unit={unit} />
        <p className="mt-1 text-xs font-semibold text-ink-2">{label}</p>
        {subtitle && <p className="text-[11px] text-ink-3 mt-0.5">{subtitle}</p>}
      </div>

      {prompt && onAsk && (
        <button
          onClick={() => onAsk(prompt)}
          className="mt-4 flex items-center gap-1 text-[11px] font-semibold text-[#2f6b46] hover:text-[#003d1c] transition-colors cursor-pointer group-hover:translate-x-0.5 transition-transform"
        >
          <Sparkles size={11} className="text-[#003d1c]" />
          <span>Ask AI about this</span>
          <ArrowRight size={11} className="transition-transform group-hover:translate-x-0.5" />
        </button>
      )}
    </div>
  )
}

export default function DashboardPage({ onNavigate }) {
  const kpiReveal = useReveal({ stagger: 50 })
  const chartsReveal = useReveal({ stagger: 50 })
  const [mobileOpen, setMobileOpen] = useState(false)
  const [selectedCampusCode, setSelectedCampusCode] = useState('ALL')
  const [tableSearch, setTableSearch] = useState('')
  const [tableRegionFilter, setTableRegionFilter] = useState('ALL')

  const selectedCampusObj = useMemo(() => {
    if (selectedCampusCode === 'ALL') return null
    return campusStats.find((c) => c.code === selectedCampusCode) || null
  }, [selectedCampusCode])

  const filteredCampusTable = useMemo(() => {
    return campusStats.filter((c) => {
      const matchSearch =
        c.name.toLowerCase().includes(tableSearch.toLowerCase()) ||
        c.code.toLowerCase().includes(tableSearch.toLowerCase()) ||
        c.region.toLowerCase().includes(tableSearch.toLowerCase())
      const matchRegion = tableRegionFilter === 'ALL' || c.region === tableRegionFilter
      return matchSearch && matchRegion
    })
  }, [tableSearch, tableRegionFilter])

  const handleAsk = (prompt) => {
    window.location.hash = '#/app'
  }

  // Dynamic KPI calculations based on campus selection
  const dynamicKpis = useMemo(() => {
    if (selectedCampusObj) {
      return [
        {
          icon: Target,
          label: 'Forecast Accuracy (AUROC)',
          value: '91.8',
          unit: '%',
          delta: '+2.1 pts',
          positive: true,
          subtitle: `${selectedCampusObj.name} ML Model Validation`,
          prompt: `Evaluate 2026 forecast accuracy and SHAP feature importance for ${selectedCampusObj.name}.`
        },
        {
          icon: Percent,
          label: 'Campus Pass Rate',
          value: selectedCampusObj.passRate.toFixed(1),
          unit: '%',
          delta: `${(selectedCampusObj.passRate - networkOverview.averagePassRate) >= 0 ? '+' : ''}${(selectedCampusObj.passRate - networkOverview.averagePassRate).toFixed(1)} pts vs avg`,
          positive: selectedCampusObj.passRate >= networkOverview.averagePassRate,
          subtitle: `Network baseline: ${networkOverview.averagePassRate}%`,
          prompt: `What are the primary subject bottlenecks affecting pass rates in ${selectedCampusObj.name}?`
        },
        {
          icon: AlertTriangle,
          label: 'Students at Risk',
          value: selectedCampusObj.atRisk.toString(),
          unit: '',
          delta: `${Math.round((selectedCampusObj.atRisk / selectedCampusObj.students) * 100)}% of cohort`,
          positive: selectedCampusObj.atRisk < 100,
          subtitle: `Requires immediate academic review`,
          prompt: `Which students are currently at high risk of failing board exams in ${selectedCampusObj.name}?`
        },
        {
          icon: Users,
          label: 'Total Enrolled Students',
          value: selectedCampusObj.students.toLocaleString(),
          unit: '',
          delta: `${selectedCampusObj.teachers} Teachers`,
          positive: true,
          subtitle: `${selectedCampusObj.region} Region · Classes 6-10`,
          prompt: `Show teacher pass rates and student enrollment breakdown for ${selectedCampusObj.name}.`
        },
      ]
    }

    return [
      {
        icon: Target,
        label: 'Forecast Accuracy (AUROC)',
        value: '91.8',
        unit: '%',
        delta: '+2.1 pts YoY',
        positive: true,
        subtitle: 'LightGBM + Calibrated Logistic with SHAP',
        prompt: 'Evaluate model accuracy and SHAP feature importance for 2026 predictions.'
      },
      {
        icon: Percent,
        label: 'Network Pass Rate',
        value: '68.7',
        unit: '%',
        delta: '+3.6 pts vs 2023',
        positive: true,
        subtitle: 'Targeting 74.2% with AI Remediation',
        prompt: 'Which campuses had the lowest pass rate in Physics and Mathematics this year?'
      },
      {
        icon: AlertTriangle,
        label: 'High/Moderate Risk Cohort',
        value: '2,140',
        unit: '',
        delta: '9.8% of Class 10',
        positive: false,
        subtitle: 'Pre-board intervention queue',
        prompt: 'Which Class 10 students are currently at high risk of failing Mathematics across all campuses?'
      },
      {
        icon: School,
        label: 'Verified Enrollment',
        value: '73,031',
        unit: '',
        delta: '20 Campuses',
        positive: true,
        subtitle: '533 Faculty · Governed Read-Only MSSQL',
        prompt: 'Compare pass rates and attendance averages across all 20 Daanish campuses.'
      },
    ]
  }, [selectedCampusObj])

  return (
    <div className="flex h-dvh w-full overflow-hidden bg-canvas text-ink">
      <Sidebar
        route="dashboard"
        onNavigate={(id) => {
          if (id === 'chatbot' || id === 'app') {
            window.location.hash = '#/app'
          } else {
            window.location.hash = '#/dashboard'
          }
        }}
        mobileOpen={mobileOpen}
        onCloseMobile={() => setMobileOpen(false)}
      />

      <div className="flex-1 h-full overflow-y-auto">
        <div className="mx-auto w-full max-w-[86rem] px-6 py-8 sm:px-10 sm:py-10 space-y-8">
          {/* Header & Filter Toolbar */}
          <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 pb-2 border-b border-line">
            <div className="flex items-center gap-3">
              <button
                onClick={() => setMobileOpen(true)}
                className="flex h-9 w-9 items-center justify-center rounded-xl border border-line bg-surface text-ink lg:hidden cursor-pointer"
                aria-label="Open navigation menu"
              >
                <Menu size={18} />
              </button>
              <PageHeader
                eyebrow="Institutional Intelligence · 20 Campuses"
                title="Academic Performance & Predictive Dashboard"
                lead="Multi-campus academic outcomes, STEM subject mastery, explainable risk signals, and board exam forecasts."
              />
            </div>
            <div className="flex items-center gap-3 shrink-0 flex-wrap">
              {/* Campus Switcher Dropdown */}
              <div className="flex items-center gap-2 bg-surface border border-line rounded-xl px-3 py-1.5 shadow-sm">
                <Building2 size={15} className="text-[#003d1c]" />
                <select
                  value={selectedCampusCode}
                  onChange={(e) => setSelectedCampusCode(e.target.value)}
                  className="text-xs font-semibold text-ink bg-transparent focus:outline-none cursor-pointer"
                >
                  <option value="ALL">All 20 Campuses (Network-Wide)</option>
                  {campusStats.map((c) => (
                    <option key={c.code} value={c.code}>
                      {c.name} ({c.code})
                    </option>
                  ))}
                </select>
              </div>

              <button
                onClick={() => {
                  window.location.hash = '#/app'
                }}
                className="flex cursor-pointer items-center gap-2 rounded-xl bg-[#003d1c] hover:bg-[#2f6b46] px-4 py-2 text-xs font-semibold text-white shadow-sm transition-all"
              >
                <Sparkles size={13} className="text-[#d3f84e]" />
                <span>Launch AI Assistant</span>
              </button>
            </div>
          </div>

        {/* Executive Data Storytelling Briefing Banner */}
        <div className="rounded-2xl border border-[#003d1c]/20 bg-[#003d1c]/5 p-5 flex flex-col md:flex-row items-start md:items-center justify-between gap-4">
          <div className="flex items-start gap-3">
            <div className="h-9 w-9 rounded-xl bg-[#003d1c] text-[#d3f84e] flex items-center justify-center shrink-0 mt-0.5 shadow-sm">
              <TrendingUp size={18} />
            </div>
            <div>
              <h3 className="text-xs font-bold uppercase tracking-wider text-[#003d1c]">
                Executive Performance & Governance Synthesis
              </h3>
              <p className="text-xs text-ink-2 mt-1 leading-relaxed max-w-3xl">
                {selectedCampusObj ? (
                  <>
                    <strong className="text-ink font-semibold">{selectedCampusObj.name}</strong> has an active enrollment of{' '}
                    <strong className="text-ink font-semibold">{selectedCampusObj.students.toLocaleString()} students</strong> with a{' '}
                    <strong className="text-ink font-semibold">{selectedCampusObj.passRate}% pass rate</strong>. Sourced live from institutional MSSQL records.
                  </>
                ) : (
                  <>
                    Across <strong className="text-ink font-semibold">73,031 students</strong> and <strong className="text-ink font-semibold">20 campuses</strong>, network pass rate stands at{' '}
                    <strong className="text-ink font-semibold">68.7%</strong> (projected to reach <strong className="text-ink font-semibold">74.2%</strong>). STEM subjects (Physics 58.2% & Mathematics 61.4%) are the primary bottlenecks. Explainable AI (SHAP) reveals pre-board mock scores (41.2%) and attendance regularity (28.4%) account for 70% of risk variance.
                  </>
                )}
              </p>
            </div>
          </div>
          <div className="flex items-center gap-2 font-mono text-[11px] text-[#2f6b46] bg-surface border border-line px-3 py-1.5 rounded-xl shrink-0 shadow-xs">
            <ShieldCheck size={14} className="text-[#003d1c]" />
            <span>MSSQL Live Ingestion · Zero PII Export</span>
          </div>
        </div>

        {/* Top 4 Executive KPI Cards */}
        <div ref={kpiReveal} className="grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
          {dynamicKpis.map((k) => (
            <KpiCard key={k.label} {...k} onAsk={handleAsk} />
          ))}
        </div>

        {/* Visual Analytics & Data Storytelling Grid */}
        <div ref={chartsReveal} className="grid gap-5 lg:grid-cols-3">
          <PerformanceTrendCard />
          <PassProbabilityCard />
          <SubjectComparisonCard />
          <RiskDonutCard />
          <ShapAttributionCard />
          <HistoricalPerformanceCard />
          <CampusBenchmarkCard />
        </div>

        {/* Comprehensive 20-Campus Performance Table */}
        <div className="rounded-2xl border border-line bg-surface p-6 shadow-sm space-y-4">
          <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 pb-3 border-b border-line">
            <div>
              <h3 className="text-sm font-bold text-ink">
                20 Daanish Campuses: Academic Performance & Risk Breakdown
              </h3>
              <p className="text-xs text-ink-3 mt-0.5">
                Live institutional metrics across North, South, Central, and West Punjab zones.
              </p>
            </div>

            <div className="flex items-center gap-2">
              {/* Region Filter */}
              <select
                value={tableRegionFilter}
                onChange={(e) => setTableRegionFilter(e.target.value)}
                className="text-xs rounded-xl border border-line bg-surface-2 px-3 py-1.5 text-ink focus:outline-none focus:border-[#2f6b46]"
              >
                <option value="ALL">All Regions</option>
                <option value="North">North Zone</option>
                <option value="South">South Zone</option>
                <option value="Central">Central Zone</option>
                <option value="West">West Zone</option>
                <option value="South-West">South-West Zone</option>
              </select>

              {/* Search Bar */}
              <div className="relative">
                <Search size={13} className="absolute left-3 top-2.5 text-ink-3" />
                <input
                  type="text"
                  value={tableSearch}
                  onChange={(e) => setTableSearch(e.target.value)}
                  placeholder="Search campus..."
                  className="rounded-xl border border-line bg-surface-2 pl-8 pr-3 py-1.5 text-xs text-ink placeholder:text-ink-3 focus:outline-none focus:border-[#2f6b46]"
                />
              </div>
            </div>
          </div>

          <div className="overflow-x-auto">
            <table className="w-full text-left text-xs border-collapse">
              <thead>
                <tr className="border-b border-line text-[11px] font-bold text-ink-3 uppercase tracking-wider">
                  <th className="py-2.5 px-3">Campus Code</th>
                  <th className="py-2.5 px-3">Campus Name</th>
                  <th className="py-2.5 px-3">Region</th>
                  <th className="py-2.5 px-3 text-right">Students</th>
                  <th className="py-2.5 px-3 text-right">Faculty</th>
                  <th className="py-2.5 px-3 text-right">Pass Rate (%)</th>
                  <th className="py-2.5 px-3 text-right">At-Risk</th>
                  <th className="py-2.5 px-3">Status</th>
                  <th className="py-2.5 px-3 text-right">Action</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-line/60 font-mono">
                {filteredCampusTable.map((c) => (
                  <tr key={c.code} className="hover:bg-surface-2/60 transition-colors">
                    <td className="py-3 px-3 font-bold text-[#003d1c]">{c.code}</td>
                    <td className="py-3 px-3 font-sans font-medium text-ink">{c.name}</td>
                    <td className="py-3 px-3 text-ink-2">{c.region}</td>
                    <td className="py-3 px-3 text-right text-ink">{c.students.toLocaleString()}</td>
                    <td className="py-3 px-3 text-right text-ink-2">{c.teachers}</td>
                    <td className="py-3 px-3 text-right">
                      <div className="flex items-center justify-end gap-2">
                        <span className="font-bold text-ink">{c.passRate.toFixed(1)}%</span>
                        <div className="w-12 bg-surface-3 h-1.5 rounded-full overflow-hidden">
                          <div
                            className={`h-full rounded-full ${
                              c.passRate >= 73 ? 'bg-[#003d1c]' : c.passRate >= 68 ? 'bg-[#2f6b46]' : 'bg-[#e06a3b]'
                            }`}
                            style={{ width: `${Math.min(c.passRate, 100)}%` }}
                          />
                        </div>
                      </div>
                    </td>
                    <td className="py-3 px-3 text-right font-semibold text-rose-600">{c.atRisk}</td>
                    <td className="py-3 px-3 font-sans">
                      <span
                        className={`text-[10px] font-semibold px-2 py-0.5 rounded-full border ${
                          c.status === 'High Performing'
                            ? 'bg-emerald-50 text-emerald-800 border-emerald-200'
                            : c.status === 'Performing'
                              ? 'bg-blue-50 text-blue-800 border-blue-200'
                              : c.status === 'Needs Support'
                                ? 'bg-amber-50 text-amber-800 border-amber-200'
                                : 'bg-rose-50 text-rose-800 border-rose-200'
                        }`}
                      >
                        {c.status}
                      </span>
                    </td>
                    <td className="py-3 px-3 text-right font-sans">
                      <button
                        onClick={() => {
                          window.location.hash = '#/app'
                        }}
                        className="text-[11px] font-semibold text-[#003d1c] hover:text-[#2f6b46] hover:underline cursor-pointer flex items-center justify-end gap-1 ml-auto"
                      >
                        <span>Query</span>
                        <ChevronRight size={12} />
                      </button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>

        {/* Live Structured Evidence & Model Answers Section */}
        <div className="border-t border-line pt-8 space-y-6">
          <div>
            <h3 className="text-xs font-bold uppercase tracking-wider text-ink-3">
              Grounded AI Engine Structured Artifacts
            </h3>
            <p className="text-xs text-ink-2 mt-0.5">
              Multi-model responses executed with governed parameters and live data integrity.
            </p>
          </div>

          <div className="grid gap-5 lg:grid-cols-2">
            <ChartAnswer />
            <AtRiskAnswer />
          </div>

          <div className="space-y-5">
            <PredictionAnswer />
            <TableAnswer />
          </div>
        </div>
      </div>
    </div>
  </div>
  )
}
