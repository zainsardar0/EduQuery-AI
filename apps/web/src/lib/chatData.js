import { Database, FileText, TrendingUp } from 'lucide-react'

export const chatModes = [
  {
    id: 'wren_nl2sql',
    label: 'Query to SQL (Live Database)',
    short: 'WrenAI · NL2SQL',
    icon: Database,
    badge: 'Live MSSQL',
    badgeClass: 'bg-emerald-50 text-emerald-700 border-emerald-200',
    description: 'Ask questions in plain English to query live student, teacher, and exam records across 20 Daanish campuses.',
    engine_mode: 'wren_nl2sql',
    placeholder: 'Ask about marks, attendance, pass rates, or campus comparisons...',
    faqs: [
      // 1. Student Demographics & Profiles
      { q: 'Show students missing father name in Class 10 across all campuses', category: 'Demographics' },
      { q: 'List total enrolled students broken down by class for Attock Boys campus', category: 'Demographics' },
      { q: 'Show students in Class 8 with unassigned section or category', category: 'Demographics' },
      { q: 'Count active students across all campuses grouped by gender', category: 'Demographics' },
      { q: 'Show enrolled students in ATKB', category: 'Demographics' },
      { q: 'List the students across all campuses', category: 'Demographics' },
      { q: 'Show 10 students in section A', category: 'Demographics' },
      { q: 'List students in class 10', category: 'Demographics' },
      { q: 'Show student roster with registration numbers and father names', category: 'Demographics' },
      { q: 'Count total students enrolled in each grade level from Class 6 to 10', category: 'Demographics' },

      // 2. Weak & At-Risk Students
      { q: 'Show weak students in class 10', category: 'At-Risk' },
      { q: 'Which students are failing in grade 9?', category: 'At-Risk' },
      { q: 'List struggling students', category: 'At-Risk' },
      { q: 'Find low-performing students in class 8', category: 'At-Risk' },
      { q: 'Show students below 40 percent', category: 'At-Risk' },
      { q: 'Which student results are under 50%?', category: 'At-Risk' },
      { q: 'Show at risk students in ATKB', category: 'At-Risk' },
      { q: 'Find weak students in MNWB class 10', category: 'At-Risk' },
      { q: 'List failing students in section A', category: 'At-Risk' },
      { q: 'Show students with marks below 35', category: 'At-Risk' },

      // 3. Top & High-Performing Students
      { q: 'Show top students', category: 'Top Scorers' },
      { q: 'List the best students in class 10', category: 'Top Scorers' },
      { q: 'Who has the highest student results?', category: 'Top Scorers' },
      { q: 'Return 5 top students in ATKG', category: 'Top Scorers' },
      { q: 'Show high-performing students in grade 9', category: 'Top Scorers' },
      { q: 'List best student marks across campuses', category: 'Top Scorers' },
      { q: 'Find top students in section B', category: 'Top Scorers' },
      { q: 'Show the highest results for year 26', category: 'Top Scorers' },
      { q: 'Who are the top students in MNWB?', category: 'Top Scorers' },
      { q: 'Return 20 best students', category: 'Top Scorers' },

      // 4. Attendance & Daily Absence Records
      { q: 'Show attendance summary', category: 'Attendance' },
      { q: 'How many attendance records are present?', category: 'Attendance' },
      { q: 'Summarize attendance across campuses', category: 'Attendance' },
      { q: 'Show attendance for ATKB', category: 'Attendance' },
      { q: 'Attendance summary for MNWB campus', category: 'Attendance' },
      { q: 'Show absent students', category: 'Attendance' },
      { q: 'List recent absences', category: 'Attendance' },
      { q: 'Who is absent today?', category: 'Attendance' },
      { q: 'Show the latest absence records', category: 'Attendance' },
      { q: 'List absentees in ATKB', category: 'Attendance' },

      // 5. House & Hostel Attendance Logs
      { q: 'Summarize house attendance', category: 'Hostel' },
      { q: 'Compare attendance across all schools', category: 'Hostel' },
      { q: 'Show attendance status by house', category: 'Hostel' },
      { q: 'Show absence records for MNWB', category: 'Hostel' },
      { q: 'Return 10 absent students', category: 'Hostel' },
      { q: 'Which students have an absence?', category: 'Hostel' },
      { q: 'Show recent absent attendance', category: 'Hostel' },
      { q: 'List absence events by house', category: 'Hostel' },
      { q: 'Show boarder attendance rates across hostel houses', category: 'Hostel' },
      { q: 'Compare house attendance between Iqbal and Jinnah houses', category: 'Hostel' },

      // 6. Teacher Performance & Results
      { q: 'Show teacher performance', category: 'Teachers' },
      { q: 'Compare teacher performance by subject', category: 'Teachers' },
      { q: 'List top teachers', category: 'Teachers' },
      { q: 'Show teacher pass rates in ATKB', category: 'Teachers' },
      { q: 'Teacher performance for Mathematics', category: 'Teachers' },
      { q: 'Compare teachers in class 10', category: 'Teachers' },
      { q: 'Show teacher class averages', category: 'Teachers' },
      { q: 'List teacher results for year 26', category: 'Teachers' },
      { q: 'Show 10 teacher performance rows', category: 'Teachers' },
      { q: 'Which teachers have the best pass percentage?', category: 'Teachers' },

      // 7. Subject-Specific Exam Analytics
      { q: 'Show subject performance', category: 'Subjects' },
      { q: 'Compare Mathematics performance', category: 'Subjects' },
      { q: 'Show English subject results', category: 'Subjects' },
      { q: 'Compare Physics performance in class 10', category: 'Subjects' },
      { q: 'Show subject pass rates for ATKG', category: 'Subjects' },
      { q: 'List subjects with the highest failure rates in Class 9', category: 'Subjects' },
      { q: 'Compare Science vs Arts subject averages across campuses', category: 'Subjects' },
      { q: 'Show Urdu and Islamiyat subject scores in Class 8', category: 'Subjects' },
      { q: 'Calculate average marks by subject for Class 7 in Rahim Yar Khan', category: 'Subjects' },
      { q: 'Show Translation of Holy Quran exam results by section', category: 'Subjects' },

      // 8. Class & Section Benchmarks
      { q: 'Show class performance', category: 'Classes' },
      { q: 'Compare class 10 performance', category: 'Classes' },
      { q: 'Show weakest classes by pass percentage', category: 'Classes' },
      { q: 'Compare section A class results', category: 'Classes' },
      { q: 'Show class averages in ATKB', category: 'Classes' },
      { q: 'Compare performance between Class 9 and Class 10', category: 'Classes' },
      { q: 'Show section-wise pass percentage for Class 8', category: 'Classes' },
      { q: 'List Class 7 sections with average score above 75%', category: 'Classes' },
      { q: 'Compare pass percentage across sections A, B, and C in Class 10', category: 'Classes' },
      { q: 'Show overall academic score distribution for Class 6', category: 'Classes' },

      // 9. Multi-Campus Governance Benchmarks
      { q: 'Compare school performance across all campuses', category: 'Campuses' },
      { q: 'Show campus performance summary', category: 'Campuses' },
      { q: 'Compare school pass rates', category: 'Campuses' },
      { q: 'Show average performance for each campus', category: 'Campuses' },
      { q: 'Compare campus results for year 26', category: 'Campuses' },
      { q: 'Show overall pass percentage in Board Middle Exam by campus', category: 'Campuses' },
      { q: 'Rank top 5 performing Daanish campuses in Class 10 examinations', category: 'Campuses' },
      { q: 'Compare average student attendance and exam scores across all 20 campuses', category: 'Campuses' },
      { q: 'Show student count and pass rates grouped by campus code', category: 'Campuses' },
      { q: 'Show student performance variance between Boys and Girls campuses', category: 'Campuses' },

      // 10. Individual Student & Exam Inquiries
      { q: 'Show results for roll number 12345', category: 'Students' },
      { q: 'Show marks for student named Ali Hassan', category: 'Students' },
      { q: 'Find student named Sara Khan', category: 'Students' },
      { q: 'Show profile of student named Ayesha Malik', category: 'Students' },
      { q: 'Show attendance for student named Ahmed Raza', category: 'Students' },
      { q: 'Show detailed marks breakdown for Roll No 320328', category: 'Students' },
      { q: 'Find academic history of Muhammad Bilal in Class 10', category: 'Students' },
      { q: 'Show term-wise progress for Roll No 319932', category: 'Students' },
      { q: 'Search student details for Zain Ul Abideen in RYKB', category: 'Students' },
      { q: 'Show exam score summary for Roll No 321450', category: 'Students' }
    ],
    initialMessages: [
      {
        from: 'assistant',
        text: 'Welcome to WrenAI Natural Language Analytics. Ask any question in plain English to query live academic databases across all 20 Daanish School campuses.',
        meta: 'Connected to read-only MSSQL cluster · 68 tables indexed'
      }
    ]
  },
  {
    id: 'google_file_search_rag',
    label: 'Policy Documents (Gemini RAG)',
    short: 'Policy Search',
    icon: FileText,
    badge: 'Gemini Policy RAG',
    badgeClass: 'bg-amber-50 text-amber-700 border-amber-200',
    description: 'Search official Daanish School policies regarding admissions, leave, exams, promotions, and discipline.',
    engine_mode: 'google_file_search_rag',
    placeholder: 'Search rules, admission criteria, leave policies, or disciplinary guidelines...',
    faqs: [
      { q: 'What are the rules regarding day scholars admission and attendance?', category: 'Admissions' },
      { q: 'What is the policy for siblings of students to get admission in Daanish schools?', category: 'Admissions' },
      { q: 'What are the age limits and poverty criteria for Class 6 induction?', category: 'Admissions' },
      { q: 'Are twin applicants eligible for joint admission if both qualify?', category: 'Admissions' },
      { q: 'What are the mandatory promotion and discharge criteria for Class 9?', category: 'Academic Rules' },
      { q: 'What is the minimum passing percentage required in Midterm examinations?', category: 'Academic Rules' },
      { q: 'What are the official regulations for student medical leave and late arrival?', category: 'Leave Policy' },
      { q: 'What procedure is required for long-term absence due to illness?', category: 'Leave Policy' },
      { q: 'How are merit-based scholarships and fee concessions allocated?', category: 'Scholarships' },
      { q: 'What are the code of conduct and disciplinary procedures for hostel students?', category: 'Discipline' },
      { q: 'What constitutes a major disciplinary violation resulting in rustication?', category: 'Discipline' }
    ],
    initialMessages: [
      {
        from: 'assistant',
        text: 'Policy Knowledge Base is online. Ask about any institutional rule, admission requirement, or governance document with strict source citations.',
        meta: 'Google Gemini File Search API · 9 Official Daanish Policy PDFs'
      }
    ]
  },
  {
    id: 'prediction_ai',
    label: 'Academic Predictions (ML & SHAP)',
    short: 'Prediction AI',
    icon: TrendingUp,
    badge: 'ML + SHAP AI',
    badgeClass: 'bg-purple-50 text-purple-700 border-purple-200',
    description: 'Forecast student exam failure risk, board pass probabilities, and inspect explainable SHAP feature weights.',
    engine_mode: 'prediction_ai',
    placeholder: 'Forecast exam outcomes, identify at-risk students, or evaluate SHAP factors...',
    faqs: [
      { q: 'Which Class 10 students are currently at high risk of failing Mathematics?', category: 'Risk Assessment' },
      { q: 'Predict the final exam result for Roll No. 5522 in Physics.', category: 'Individual Forecast' },
      { q: 'Forecast the board exam pass probability for Attock Boys branch in 2026.', category: 'Campus Outlook' },
      { q: 'Show SHAP feature impact breakdown and explain risk attributions.', category: 'Explainability' },
      { q: 'What are the primary drivers influencing grade drops between Midterm and Final exams?', category: 'Risk Drivers' },
      { q: 'Predict GPA distribution for Class 8 students entering Class 9.', category: 'Cohort Progression' },
      { q: 'Analyze the correlation between attendance below 75% and midterm failure.', category: 'Risk Analysis' }
    ],
    initialMessages: [
      {
        from: 'assistant',
        text: 'Academic Predictive Intelligence Engine ready. Forecast student outcomes, calculate failure risks, and inspect underlying SHAP feature drivers.',
        meta: 'CatBoost & Random Forest Inference · MLflow Governance'
      }
    ]
  }
]

export const CAMPUSES = [
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
