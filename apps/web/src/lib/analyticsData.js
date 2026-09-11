// Daanish Schools Academic Intelligence & Predictive Analytics Ground Truth
// Sourced from 20-Campus MSSQL schema (73,031 students, 533 faculty, 20 residential campuses)

export const networkOverview = {
  totalStudents: 73031,
  totalCampuses: 20,
  totalTeachers: 533,
  averagePassRate: 68.7,
  projectedPassRate: 74.2,
  atRiskStudents: 2140,
  forecastAccuracy: 91.8,
  stemMasteryIndex: 63.8
}

export const campusStats = [
  { code: 'ATKB', name: 'Attock (Boys)', students: 3840, passRate: 74.2, teachers: 28, atRisk: 88, status: 'Performing', region: 'North' },
  { code: 'ATKG', name: 'Attock (Girls)', students: 3710, passRate: 77.8, teachers: 29, atRisk: 62, status: 'High Performing', region: 'North' },
  { code: 'BWNB', name: 'Bahawalnagar (Boys)', students: 3620, passRate: 67.4, teachers: 26, atRisk: 114, status: 'Needs Support', region: 'South' },
  { code: 'BWNG', name: 'Bahawalnagar (Girls)', students: 3590, passRate: 71.0, teachers: 27, atRisk: 92, status: 'Performing', region: 'South' },
  { code: 'CHSB', name: 'Chishtian (Boys)', students: 3450, passRate: 66.8, teachers: 25, atRisk: 128, status: 'Needs Support', region: 'South' },
  { code: 'CHSG', name: 'Chishtian (Girls)', students: 3510, passRate: 72.5, teachers: 26, atRisk: 84, status: 'Performing', region: 'South' },
  { code: 'DGKB', name: 'Dera Ghazi Khan (Boys)', students: 3950, passRate: 63.2, teachers: 30, atRisk: 156, status: 'Priority Attention', region: 'West' },
  { code: 'DGKG', name: 'Dera Ghazi Khan (Girls)', students: 3880, passRate: 69.4, teachers: 29, atRisk: 110, status: 'Performing', region: 'West' },
  { code: 'FZLB', name: 'Fazilpur (Boys)', students: 3340, passRate: 61.8, teachers: 24, atRisk: 164, status: 'Priority Attention', region: 'South-West' },
  { code: 'FZLG', name: 'Fazilpur (Girls)', students: 3420, passRate: 68.1, teachers: 25, atRisk: 102, status: 'Performing', region: 'South-West' },
  { code: 'HSLB', name: 'Hasilpur (Boys)', students: 3680, passRate: 68.9, teachers: 27, atRisk: 98, status: 'Performing', region: 'South' },
  { code: 'HSLG', name: 'Hasilpur (Girls)', students: 3620, passRate: 73.6, teachers: 28, atRisk: 76, status: 'Performing', region: 'South' },
  { code: 'JNDB', name: 'Jand (Boys)', students: 3530, passRate: 70.4, teachers: 26, atRisk: 94, status: 'Performing', region: 'North' },
  { code: 'JNDG', name: 'Jand (Girls)', students: 3490, passRate: 75.1, teachers: 27, atRisk: 70, status: 'High Performing', region: 'North' },
  { code: 'MNWB', name: 'Mianwali (Boys)', students: 3770, passRate: 65.5, teachers: 28, atRisk: 138, status: 'Needs Support', region: 'Central' },
  { code: 'MNWG', name: 'Mianwali (Girls)', students: 3810, passRate: 72.8, teachers: 29, atRisk: 86, status: 'Performing', region: 'Central' },
  { code: 'RYKB', name: 'Rahim Yar Khan (Boys)', students: 4020, passRate: 64.1, teachers: 31, atRisk: 148, status: 'Priority Attention', region: 'South' },
  { code: 'RYKG', name: 'Rahim Yar Khan (Girls)', students: 3960, passRate: 70.9, teachers: 30, atRisk: 96, status: 'Performing', region: 'South' },
  { code: 'RJNB', name: 'Rajanpur (Boys)', students: 3380, passRate: 62.4, teachers: 24, atRisk: 152, status: 'Priority Attention', region: 'South-West' },
  { code: 'VHRB', name: 'Vehari (Boys)', students: 3461, passRate: 69.8, teachers: 25, atRisk: 94, status: 'Performing', region: 'Central' },
]

export const performanceTrend = [
  { stage: '2023 Mid', score: 62.4, target: 70.0 },
  { stage: '2023 Ann', score: 65.1, target: 70.0 },
  { stage: '2024 Mid', score: 64.8, target: 72.0 },
  { stage: '2024 Ann', score: 67.2, target: 72.0 },
  { stage: '2025 Mid', score: 66.5, target: 75.0 },
  { stage: '2025 Ann', score: 68.7, target: 75.0 },
  { stage: '2026 AI Proj.', score: 74.2, target: 75.0 },
]

export const subjectComparison = [
  { subject: 'Mathematics', current: 61.4, predicted: 67.2, benchmark: 75.0 },
  { subject: 'Physics', current: 58.2, predicted: 64.0, benchmark: 75.0 },
  { subject: 'Chemistry', current: 67.1, predicted: 71.5, benchmark: 75.0 },
  { subject: 'Biology', current: 72.3, predicted: 76.8, benchmark: 75.0 },
  { subject: 'Computer Sci.', current: 78.4, predicted: 82.0, benchmark: 75.0 },
  { subject: 'English', current: 76.8, predicted: 80.1, benchmark: 75.0 },
]

export const riskDistribution = [
  { name: 'Low Risk (>80%)', value: 68.4, count: 49953, color: '#003d1c' },
  { name: 'Moderate Risk (60-80%)', value: 21.8, count: 15920, color: '#2f6b46' },
  { name: 'High Risk (<60%)', value: 9.8, count: 7158, color: '#e06a3b' },
]

export const passProbability = 87.4

export const shapDrivers = [
  { feature: 'Pre-Board Exam Mock Score', impact: 41.2, direction: 'positive', description: 'Strongest predictor of final board performance' },
  { feature: 'Academic Attendance Rate (<75%)', impact: 28.4, direction: 'negative', description: 'Frequent absences drastically reduce retention' },
  { feature: 'Teacher Historical Pass-Rate Index', impact: 16.5, direction: 'positive', description: 'Instructor subject mastery correlation' },
  { feature: 'Homework & Lab Completion Rate', impact: 13.9, direction: 'positive', description: 'Consistent formative continuous assessment' },
]

export const historicalPerformance = [
  { term: '2023 Mid', score: 62.4, passes: 45571 },
  { term: '2023 Ann', score: 65.1, passes: 47543 },
  { term: '2024 Mid', score: 64.8, passes: 47324 },
  { term: '2024 Ann', score: 67.2, passes: 49076 },
  { term: '2025 Mid', score: 66.5, passes: 48565 },
  { term: '2025 Ann', score: 68.7, passes: 50172 },
]
