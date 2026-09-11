// Frequently asked questions for the Chatbot page. Answers reuse the same
// house copy voice as the rest of the product: no "powerful", no exclamation
// marks, three sentences at most.

export const faqs = [
  {
    q: 'What can I ask the assistant?',
    a: 'Anything about marks, attendance, exam schedules, teacher performance or campus comparisons — in plain English, the way you would ask a colleague. No table names or query syntax required.',
  },
  {
    q: 'How current is the data it answers from?',
    a: 'Every answer is read live from your student database at the moment you ask. There is no separate copy or export that can drift out of date.',
  },
  {
    q: 'Can it change or delete a record?',
    a: 'No. The assistant is read-only by design — it can retrieve data but has no permission to add, edit or delete anything.',
  },
  {
    q: 'Who can see which students?',
    a: 'Access follows your existing roles. A teacher sees their own campus, a principal sees theirs, and the database enforces this — it is not a setting the assistant could be asked around.',
  },
  {
    q: 'Is every question logged?',
    a: 'Yes. Every question, answer and sign-in is written to an audit trail you can review at any time, showing exactly who asked what and when.',
  },
  {
    q: 'How reliable are the exam predictions?',
    a: 'Forecasts are estimates, not guarantees — each one comes with a confidence band and a plain-language explanation of the factors behind it, so you can judge how much weight to give it.',
  },
  {
    q: 'Does my data leave our infrastructure?',
    a: 'No. The assistant can run on-premise inside your own network, and your records are never used to train a model shared with anyone else.',
  },
]
