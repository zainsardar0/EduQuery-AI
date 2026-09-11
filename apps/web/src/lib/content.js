/**
 * All page copy lives here.
 *
 * House style, taken from the reference audit: name nouns rather than
 * qualities; no "powerful", "seamless", "robust", "cutting-edge"; no
 * exclamation marks; no italics; body sentences 12–20 words; no paragraph
 * over three sentences.
 */

export const meta = {
  name: 'EduQuery AI',
  wordmark: 'EduQuery.',
  tagline: 'Know your students. Act before the exam.',
  contactEmail: 'hello@eduquery.ai', // TODO: replace with your real address
}

export const hero = {
  eyebrow: 'AI for school networks',
  // Two sentences, deliberately. The full stop buys a beat.
  title: ['Know your students.', 'Act before the exam.'],
  subhead:
    'Every mark, attendance record and exam result across your campuses, in one place you can simply ask questions of.',
  cta: 'Get started',
  proof: 'Built for school networks',
}

export const heroStats = [
  {
    value: 92.32,
    decimals: 2,
    unit: '%',
    label: 'Forecast accuracy',
    note: 'Predicting final grades from midterm results',
  },
  {
    value: 2.4,
    decimals: 1,
    unit: 's',
    label: 'Average answer time',
    note: 'From plain-English question to result',
  },
  {
    value: 12,
    unit: '',
    label: 'Question categories',
    note: 'No query language to learn',
  },
]

/** Scrolls as a marquee. What people actually type — not customer logos. */
export const askedQuestions = [
  'Which schools had the lowest pass rate in Physics?',
  'Show students who missed more than 15 days.',
  'Predict the final result for Roll No. 5522.',
  'Has Class 10 Science declined over three years?',
  'Which teachers are below the board average?',
  'Are there students with missing Midterm marks?',
  'What is the exam schedule for Annual 2026?',
  'Why is Class 10 at Campus B performing poorly?',
]

/** A single-sentence rest beat between the marquee and the argument. */
export const manifesto =
  'EduQuery AI is an academic intelligence platform for school networks. It answers questions about your existing data in plain English, and forecasts which students need help while there is still time to give it.'

export const problems = [
  {
    title: 'Answers need a programmer',
    body: 'Getting a specific answer means someone writes code. That takes days, sometimes weeks.',
    noMore: 'No more waiting on a report request.',
  },
  {
    title: 'Only pre-built reports exist',
    body: 'Most school software ships fixed reports. You cannot ask a question nobody designed in advance.',
    noMore: 'No more questions you are not allowed to ask.',
  },
  {
    title: 'Decision-makers cannot query',
    body: 'Principals and heads of department rarely have the technical skills to interrogate a database.',
    noMore: 'No more depending on one person who knows SQL.',
  },
  {
    title: 'At-risk students surface too late',
    body: 'Struggling students are identified after results are published, when intervention is no longer possible.',
    noMore: 'No more finding out in August.',
  },
]

export const steps = [
  {
    n: '01',
    title: 'You ask a question',
    body: 'Type it the way you would say it to a colleague. No table names, no syntax.',
  },
  {
    n: '02',
    title: 'It reads the question',
    body: 'It resolves which campus, which subject, which session and which students you mean.',
  },
  {
    n: '03',
    title: 'It queries your data',
    body: 'The question becomes a read-only database query. You never see this step.',
  },
  {
    n: '04',
    title: 'It retrieves the records',
    body: 'Marks, attendance, teacher performance, board benchmarks — whatever the question needed.',
  },
  {
    n: '05',
    title: 'You get an answer',
    body: 'A table, a chart or a written summary. Every figure traceable to its source.',
  },
]

/*
  Grouped into three thematic clusters rather than one flat list of twelve —
  each cluster is its own scroll-triggered reveal, so the section reads as
  three considered moves instead of one dense wall of cards.
*/
export const questionGroups = [
  {
    label: 'Everyday lookups',
    items: [
      { type: 'Student lookup', example: 'Show the profile and contact details for Roll No. 12345.' },
      { type: 'Individual results', example: "What were Ali Khan's Mathematics marks in the Midterm?" },
      { type: 'Class performance', example: 'What is the average pass percentage of Class 9 network-wide?' },
      { type: 'Campus comparison', example: 'Which campus had the highest pass rate in English Annual?' },
    ],
  },
  {
    label: 'Oversight and operations',
    items: [
      { type: 'Teacher performance', example: 'List teachers whose students scored below the board average.' },
      { type: 'Board benchmarks', example: 'Which subjects is Campus A consistently below the board average?' },
      { type: 'Attendance tracking', example: 'Which students missed more than 15 days before the final?' },
      { type: 'Exam operations', example: 'What is the exam schedule for the Annual 2026 session?' },
    ],
  },
  {
    label: 'Deeper analysis',
    items: [
      { type: 'Data quality', example: 'Are there any students with missing marks in the Midterm results?' },
      { type: 'Trends over time', example: 'Has Class 10 Science improved or declined over three years?' },
      { type: 'Forecasts', example: 'Predict the likely final result for Roll No. 5522 in Physics.' },
      { type: 'Explanations', example: 'Why is Class 10 at Campus B performing poorly this session?' },
    ],
  },
]

export const predictionInputs = [
  { label: 'Past exam marks', detail: 'How the student performed across previous midterms and annuals.' },
  { label: 'Attendance record', detail: 'Days missed in the run-up to the examination.' },
  { label: 'Class context', detail: 'How the cohort is performing against previous years.' },
  { label: 'Teacher history', detail: 'The subject teacher’s pass rate over prior sessions.' },
  { label: 'Board benchmark gap', detail: 'Whether the campus sits above or below the board average.' },
  { label: 'Trend direction', detail: 'Whether the student is improving, declining or holding steady.' },
]

export const predictionOutputs = [
  { label: 'Predicted range', detail: 'An estimated score band, for example 62–68 percent.' },
  { label: 'Grade band', detail: 'The probable classification from A through F.' },
  { label: 'Pass probability', detail: 'The likelihood of passing, stated as a percentage.' },
  { label: 'At-risk ranking', detail: 'Students ordered by how urgently they need attention.' },
  { label: 'Campus forecast', detail: 'Projected class average and pass rate for planning.' },
  { label: 'Explanation', detail: 'Why the forecast landed where it did, in plain language.' },
]

/** The product surface. Mirrors the module registry in the application. */
export const modules = [
  {
    title: 'Dashboard',
    body: 'Network-wide performance, risk signals and recent activity on one screen.',
    status: 'Live',
  },
  {
    title: 'AI Assistant',
    body: 'Ask in plain English, get tables, charts and written answers back.',
    status: 'Live',
  },
  {
    title: 'Predictions',
    body: 'Exam forecasts with confidence bands, at-risk ranking and explanations.',
    status: 'Live',
  },
  {
    title: 'Students',
    body: 'Profiles, result history, attendance and subject-level breakdowns.',
    status: 'Live',
  },
  {
    title: 'Teachers',
    body: 'Teacher-wise pass rates benchmarked against board averages by subject.',
    status: 'Live',
  },
  {
    title: 'Campuses',
    body: 'League tables, board comparison and subject-level gap analysis.',
    status: 'Live',
  },
  {
    title: 'Attendance',
    body: 'Absence patterns, chronic-absentee tracking and the result correlation.',
    status: 'Live',
  },
  {
    title: 'Analytics',
    body: 'Multi-year trends and cohort comparison saved as reusable views.',
    status: 'Live',
  },
  {
    title: 'Reports',
    body: 'Scheduled and on-demand exports to PDF or Excel with a shareable link.',
    status: 'Live',
  },
]

export const securityLayers = [
  {
    tag: 'Layer 1',
    title: 'Roles and access',
    body: 'A teacher sees their own campus. A principal sees theirs. Nobody sees another campus by accident.',
  },
  {
    tag: 'Layer 2',
    title: 'Database-level rules',
    body: 'The database enforces who may read what. The lock sits inside the vault, not on the front door.',
  },
  {
    tag: 'Layer 3',
    title: 'Sensitive fields excluded',
    body: 'Passwords and one-time codes are removed from the assistant’s view. It cannot expose what it cannot read.',
  },
]

export const securityGuarantees = [
  {
    title: 'Read-only by design',
    body: 'The assistant cannot add, change or delete a record. A window into the data, not a door.',
  },
  {
    title: 'Complete audit trail',
    body: 'Every question, answer and sign-in is recorded. You can review exactly who asked what, and when.',
  },
  {
    title: 'Runs on your infrastructure',
    body: 'Deploy on-premise inside your own network. No student data leaves the building.',
  },
  {
    title: 'Your data stays yours',
    body: 'We do not train models on your records. Export everything at any time.',
  },
]

export const outcomes = [
  {
    title: 'Answers in seconds, not weeks',
    body: 'Questions that needed a report request are answered while you are still in the meeting.',
  },
  {
    title: 'Intervention before the exam',
    body: 'At-risk students surface with weeks to spare, not after results are published.',
  },
  {
    title: 'Evidence, not impression',
    body: 'Teacher and campus performance measured against board benchmarks.',
  },
  {
    title: 'No migration required',
    body: 'It connects to the student database you already run. Nothing to move.',
  },
  {
    title: 'One place for every campus',
    body: 'Network-wide comparison without exporting a spreadsheet from each school.',
  },
  {
    title: 'Deploys in weeks',
    body: 'Connect the database, map the fields, and start asking questions.',
  },
]

export const finalCta = {
  title: 'Ready to stop waiting on reports?',
  body: 'Book a walkthrough on your own data. We will connect a copy of your database and show you real answers to your own questions.',
  cta: 'Book a walkthrough',
}

export const footerColumns = [
  { heading: 'Product', links: ['Overview', 'How it works', 'Forecasting', 'Security'] },
  { heading: 'Company', links: ['About', 'Contact', 'Careers'] },
  { heading: 'Resources', links: ['Documentation', 'Data dictionary', 'Support'] },
  { heading: 'Legal', links: ['Terms', 'Privacy', 'Data processing'] },
]
