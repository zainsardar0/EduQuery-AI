// Daanish Schools Institutional Query Benchmarks & Structured Evidence Sample Data

export const passRateQuery = {
  question: 'Which campuses had the lowest pass rate in Physics this year?',
  meta: { rows: 5, seconds: '0.42s', source: 'MSSQL Live DB · 20 Campuses · Academic Results' },
  columns: ['Campus Code', 'Campus Name', 'Region', 'Students Sat', 'Passed', 'Pass Rate (%)'],
  rows: [
    ['FZLB', 'Fazilpur (Boys)', 'South-West', 184, 114, 61.8],
    ['RJNB', 'Rajanpur (Boys)', 'South-West', 196, 122, 62.4],
    ['DGKB', 'Dera Ghazi Khan (Boys)', 'West', 242, 153, 63.2],
    ['RYKB', 'Rahim Yar Khan (Boys)', 'South', 255, 163, 64.1],
    ['MNWB', 'Mianwali (Boys)', 'Central', 218, 143, 65.5],
  ],
  summary:
    'Five campuses fall below the 68.7% network average in Physics. Fazilpur (Boys) exhibits the largest STEM bottleneck (61.8%) and has been flagged for dedicated mobile lab remediation.',
}

export const trendData = [
  { term: '2023 Mid', value: 62.4 },
  { term: '2023 Ann', value: 65.1 },
  { term: '2024 Mid', value: 64.8 },
  { term: '2024 Ann', value: 67.2 },
  { term: '2025 Mid', value: 66.5 },
  { term: '2025 Ann', value: 68.7 },
]

export const prediction = {
  roll: '5522',
  student: 'Hamza Iqbal',
  subject: 'Physics',
  exam: 'Annual Board 2026',
  range: '64–70%',
  band: 'C',
  passProbability: 87.4,
  confidence: 'High (91.8% AUROC Model)',
  drivers: [
    { label: 'Pre-Board Mock score', value: '68%', direction: 'neutral' },
    { label: 'Attendance regularity', value: '88% (Satisfactory)', direction: 'up' },
    { label: 'Class average trend', value: '+3.2 pts YoY', direction: 'up' },
    { label: 'Teacher pass rate index', value: '82.4%', direction: 'up' },
  ],
  explanation:
    'Forecast generated from a 68% pre-board score, 88% term attendance, and continuous assignment completion. The instructor historical pass index of 82.4% provides additional lift. Model confidence is 91.8% based on LightGBM cross-validation with SHAP feature weights.',
}

export const atRisk = [
  { roll: '5522', name: 'Hamza Iqbal', campus: 'ATKB', subject: 'Physics', risk: 62, band: 'Moderate' },
  { roll: '4108', name: 'Sana Riaz', campus: 'BWNG', subject: 'Mathematics', risk: 71, band: 'Moderate' },
  { roll: '6731', name: 'Bilal Ahmed', campus: 'DGKB', subject: 'Chemistry', risk: 74, band: 'High' },
  { roll: '3390', name: 'Ayesha Noor', campus: 'FZLG', subject: 'Physics', risk: 83, band: 'High' },
]

export const suggestedQuestions = [
  'Which campuses had the lowest pass rate in Physics this year?',
  'Show students in Class 10 who missed more than 15 days of classes.',
  'Predict the final board exam result for Roll No. 5522 in Physics.',
  'Compare pass rates across all 20 Daanish campuses for Class 10 Mathematics.',
]

export const history = [
  { label: 'Class 10 Mathematics pass rate, all 20 campuses', time: '2m ago' },
  { label: 'Fazilpur Boys vs Girls Physics comparison', time: '14m ago' },
  { label: 'Day scholars fee and admission policy check', time: '1h ago' },
  { label: 'Class 9 predictive risk failure cohort', time: 'Yesterday' },
]
