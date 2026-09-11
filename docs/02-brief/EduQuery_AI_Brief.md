# EduQuery AI

## A Prompt-Based Intelligent Analytics and Prediction Engine for Multi-Campus Academic Databases

**Strategic Executive Brief for University Leadership**

| | |
|---|---|
| Submitted to | Dr. Ali Imran; Office of the Prorector / Rector |
| Prepared by | Muhammad Junaid; M. Zain ul Abideen; Abdur Rafay; Abeera Anwer |
| Programme | Bootcamp — Advanced AI 2026 |
| Date | Updated 3 August 2026 |

## Executive Overview

Modern educational networks accumulate extensive operational data across student enrolments, academic examinations, teacher key performance indicators, daily attendance and standardized board outcomes. Institutional decision-makers nevertheless face friction when extracting timely strategic insights because traditional data structures require developer intervention or static reports.

EduQuery AI transforms static database assets into an interactive decision-support engine. It combines a natural-language query interface with machine-learning prediction pipelines so university leadership, Deans and academic administrators can query multi-campus databases using familiar academic terminology and receive analytical summaries, trend visualizations and early-warning student-performance forecasts.

The core engineering stack is open source, but infrastructure and OpenRouter usage are operational costs that require measurement and approval. The proposal's 92.3% predictive figure is an external research benchmark, while EduQuery AI must report its own leakage-safe results. The broader product vision covers 12 institutional analytical domains and prioritizes institutional control of student data.

The August 20 release is now locked as an English-only working MVP. It includes Next.js, FastAPI and Wren AI; semantic-layer documentation; evaluated gold prompts; Optuna-tuned LightGBM, CatBoost, and HistGBM models with TreeSHAP tracked in MLflow; representative SHAP explanations; verified empirical accuracy (74.32% of predictions within ±8% margin, MAE 6.33%) as a realistic first-year baseline given missing historical mock data in remote campuses; security evidence; and the final report/live demonstration.

## 1. Institutional Context and Strategic Value

### 1.1 Strategic Alignment and Purpose

EduQuery AI introduces a governed prompt-based analytics layer over existing institutional database infrastructure. It establishes three capabilities:

- **Democratized data access:** Leadership and academic heads can conduct ad-hoc exploration without waiting for custom SQL development.
- **Forward-looking foresight:** Management moves from post-exam review toward earlier intervention using predictive models.
- **Governed metric consistency:** Institutional definitions such as pass percentage and teacher-performance indexes remain consistent across campuses.

### 1.2 Operational Transformation

| Dimension | Traditional workflow | EduQuery AI platform |
|---|---|---|
| Query mechanism | Static reports or developer-coded SQL requests | Natural-language prompts grounded in governed schema terms |
| Turnaround | Days or weeks depending on technical availability | Targeted near-real-time query and chart composition |
| Analytical horizon | Historical post-facto evaluation | Historical diagnostics plus predictive forecasting |
| Student support | At-risk identification after final results | Earlier risk detection with explainable indicators |
| Data sovereignty | Manual spreadsheet exports across silos | Governed execution with database-level access controls |

**Strategic takeaway:** EduQuery AI does not replace institutional databases or academic authority. It provides an intelligent layer that makes existing data more accessible, consistent and actionable.

## 2. System Architecture and Governed Semantic Layer

### 2.1 Architecture Overview

| Tier | Component | Institutional role |
|---|---|---|
| Presentation | Next.js web portal on Vercel | English responsive chat interface, charts and role-scoped dashboards; no protected server-side processing on Vercel |
| Institutional gateway | FastAPI inside the institution | Authentication, authorization, intent routing, redaction, validation, audit and response composition |
| Analytics and NL2SQL | Institution-hosted Wren AI plus local RAG | Uses governed MDL, schema glossary, metric definitions and approved examples to produce validated query plans |
| External model assistance | GPT 5.6 Luna Pro through OpenRouter | Receives only locally de-identified intent/schema context; never student identities, rows, marks, results or predictions |
| Prediction | Institution-hosted Optuna-tuned LightGBM/CatBoost/HistGBM tournament with TreeSHAP and MLflow tracking | Produces measured performance forecasts, empirical accuracy baselines and feature attribution |
| Data and governance | SQL Server `db_aadc11_sqldaanish` | Authoritative academic database with read-only access and row-level controls |

### 2.2 Documents as Source of Truth

The Documents-as-Source-of-Truth framework addresses hallucination and metric inconsistency. The AI does not guess table structures or formulas from generic model knowledge. Prompts are interpreted through a curated semantic model that defines approved tables, relationships, metrics, joins and campus-security parameters before any query reaches the database.

Generated queries must pass schema grounding, allowlisting, Abstract Syntax Tree validation, parameterization, scope enforcement, row limits and read-only database permissions.

## 3. Institutional Analytical Domains

| Domain | Representative question |
|---|---|
| Student lookup and profile | Retrieve enrolment profile, house assignment and academic status for a roll number |
| Individual transcript analytics | Display subject marks and historical trajectory across examinations |
| Class and section aggregates | Generate averages, pass percentages and grade distributions |
| Cross-campus comparison | Rank schools by subject or class performance |
| Faculty performance KPIs | Identify sections performing below approved board benchmarks |
| Board benchmarking | Compare institutional subject results against `BOARD_PER` metrics |
| Attendance and absenteeism | Identify students whose absence exceeds an approved threshold |
| Exam operations | Display schedules, deadlines and marks-entry completion status |
| Audit and data quality | Detect missing marks and incomplete result records |
| Multi-year trends | Analyse improvement or decline across exams and years |
| Predictive result forecast | Forecast percentage, grade band and pass probability |
| Explainable risk attribution | Identify the factors contributing to academic-risk predictions |

## 4. Predictive Intelligence and Explainable AI

### 4.1 Prediction Engine

The active prediction pipeline implements an Optuna-tuned tournament evaluating LightGBM, XGBoost, CatBoost, and HistGradientBoosting regressors across 105,091 student-subject instances, evaluated with Leave-One-School-Out (LOSO) cross-validation across all 21 school splits. The empirical evaluation achieves a Mean Absolute Error (MAE) of 6.33%, an RMSE of 9.85%, and 74.32% of all predictions falling within a strict ±8% tolerance margin (with top campuses reaching 4.82% MAE in HSPB and 5.06% MAE in MNWG).

### 4.2 Input Features

- Historical marks, percentages and formative mock trajectories (Mid-Dec, Mock 1–4).
- Attendance and absentee patterns.
- Class averages, section size, teacher historical pass rates, and teacher position percentiles.
- Difference between campus performance and board benchmarks (`BOARD_PER`).

### 4.3 Explainability

TreeSHAP (Tree Shapley Additive Explanations) attribution is implemented to show how factors such as attendance, formative mock trends, teacher context, and board benchmark gaps influence each student's forecast. Predictions are advisory decision support only; they must never automatically determine a student's grade, placement, or disciplinary outcome.

The verified empirical baseline for EduQuery AI is 74.32% within ±8% margin (MAE 6.33%), establishing a realistic and defensible institutional first-year baseline given missing formative records in newer and remote campuses.

## 5. Data Governance, Security and On-Premise Control

### 5.1 Defence in Depth

| Boundary | Control | Outcome |
|---|---|---|
| Access control | Institutional authentication, RBAC and campus-scoped authorization | Users access only approved functions and records |
| Database isolation | Least-privilege read-only SQL identity and SQL Server Row-Level Security where supported | Cross-campus and write access are blocked at the data layer |
| AI privacy boundary | PII exclusion, approved semantic surface, prompt/result redaction and SQL validation | Sensitive tables and fields are excluded from model context and query execution |
| Accountability | Tamper-resistant audit events for requests, decisions, generated SQL and outcomes | Administrators can investigate access and failures |

### 5.2 Deployment Sovereignty

The approved MVP uses a split deployment. Vercel hosts the Next.js interface and static assets. FastAPI, Wren AI, local RAG, SQL Server connectivity, model inference, MLflow, SHAP and audit services remain inside the institution. The browser connects through an institution-approved HTTPS/VPN gateway without routing protected prompts through Vercel server functions or analytics.

OpenRouter is an external processor even when zero-data-retention controls are enabled. Therefore local redaction/tokenization runs before every request; the external model receives de-identified schema/intent context only. Student identities, roll numbers, marks, returned rows, predictions and protected prompts never leave the institution. If that exclusion cannot be proven, the external call is blocked.

## 6. Implementation Roadmap and Team Allocation

### 6.1 Product Roadmap

| Phase | Focus | Institutional deliverable |
|---|---|---|
| 1 | Schema engineering and semantic modelling | Curated analytical views and governed glossary |
| 2 | NL2SQL engine and web portal | Working prompt flows for core academic domains |
| 3 | Advanced analytics and feature pipelines | Teacher, attendance and board-comparison analytics |
| 4 | Prediction and explainability | Validated model, explanation output and model records |
| 5 | Security, evaluation and operational readiness | Access-control verification, gold prompts, performance testing and deployment runbook |

The August 20, 2026 workforce plan defines the immediate parallel delivery sequence. Multilingual capability, beginning with Urdu, follows after acceptance of the English MVP.

### 6.2 Team Ownership

| Team member | Primary ownership | Secondary support |
|---|---|---|
| Muhammad Junaid | NL2SQL engine and governed semantic layer | Schema glossary and SQL validation |
| M. Zain ul Abideen | Prediction pipeline and explainability | Experiment tracking and model evaluation |
| Abdur Rafay | FastAPI backend and deployment architecture | Authentication, authorization, RLS and audit logging |
| Abeera Anwer | Next.js portal, visualization and UX | Gold-prompt UX and dashboard evaluation |

Codex acts as Workforce and Planner across architecture, task allocation, integration, quality and release readiness. Antigravity executes bounded implementation packets under the relevant human stream owner.

## 7. Deliverables and Leadership FAQ

### 7.1 Deliverables

| Category | Deliverable |
|---|---|
| Software | Containerized EduQuery AI web application with Next.js and FastAPI |
| Semantic governance | Approved schema glossary, metric definitions and relationships |
| Evaluation | At least 200 versioned gold prompts with expected answers, actual results and measured query accuracy |
| Prediction | Historical baseline, AutoGluon ensemble and TabPFN artifacts with MLflow tracking, adaptive selection and representative SHAP output |
| Security | Threat model, RLS verification, access-control tests, SQL-injection results, outbound-payload inspection and PII-exclusion proof |
| Operations | Deployment configuration, monitoring, backup/recovery and support runbook |
| Documentation | Technical documentation, stakeholder brief and live demonstration materials |

### 7.2 Leadership FAQ

**Does this require proprietary software licensing?**

The proposed core stack uses open-source frameworks. Infrastructure, model-provider and operational costs still require measurement and approval.

**How is student privacy protected?**

Through institution-hosted authorization, a least-privilege read-only database identity, row-level controls, PII exclusion, query validation, redacted logging and fail-closed outbound redaction. Vercel hosts only the interface; OpenRouter receives only de-identified schema/intent context.

**What infrastructure is required?**

Vercel hosts the interface. Institutional infrastructure runs FastAPI, Wren AI, RAG, SQL connectivity, MLflow and prediction/explainability services. CPU/GPU and storage requirements must be measured against the actual AutoGluon/TabPFN workloads and expected concurrency.

**Does the platform replace teachers or administrators?**

No. It provides analytics and predictive decision support. Human educators retain complete academic authority.
