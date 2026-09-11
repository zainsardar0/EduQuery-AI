# CAPSTONE PROJECT PROPOSAL

**Project Title**\
**EduQuery AI: A Prompt-Based Intelligent Analytics and Prediction Engine for Multi-Campus Academic Databases**

| | |
|---|---|
| **Proposed Team** | Muhammad Junaid, M. Zain ul Abideen, Abdur Rafay, Abeera Anwer |
| **Course** | Bootcamp — Advanced AI 2026 |
| **Submitted To** | Dr. Ali Imran |
| **Institution** | Ghulam Ishaq Khan Institute of Engineering Sciences and Technology (GIK Institute), Topi |
| **Date** | 27 July 2026 |

### Team Members

| Name | Email | Primary Role |
|---|---|---|
| Muhammad Junaid | Thejunaid1799@gmail.com | NL2SQL Engine & Semantic Layer Lead |
| M. Zain ul Abideen | Zainsardar062@gmail.com | ML Prediction Pipeline & Model Engineering |
| Abdur Rafay | Abdurrafay222@gmail.com | Backend Architecture & API Development |
| Abeera Anwer | sobisobangoyes@gmail.com | Frontend, Visualization & UX Design |

---

## 1. Abstract

Educational institutions store large volumes of student, examination, teacher, attendance, and board-performance data, yet most of this value remains locked behind fixed reports and SQL expertise. This project proposes **EduQuery AI**, a prompt-based artificial intelligence engine that allows authorized users to ask natural-language questions over an existing multi-school academic SQL Server database (`db_aadc11_sqldaanish`) and receive accurate analytical answers. The system will also **predict future examination results** using previous exam parameters such as subject-wise percentages, grades, pass/fail history, class averages, teacher performance indicators, absentee patterns, and board benchmarks.

EduQuery AI is built on three pillars drawn from an evidence-based design philosophy:

1. **Documents as Source of Truth (DOX Framework)** — A governed semantic layer defines every metric, table relationship, and business term in the academic schema. The AI never interprets data from training data alone; it is always grounded in documented schema definitions.
2. **Evidence-Based Adaptation** — Every architectural decision in this proposal is backed by verifiable data: published benchmarks, GitHub repository metrics, and market research — not assumptions.
3. **Production Realism** — The system is designed around "what actually breaks at scale," incorporating mandatory SQL validation, row-level security, explainable predictions, and audit logging from day one.

The outcome will be a practical decision-support application that makes institutional data accessible, actionable, and forward-looking.

**Keywords:** Prompt-based AI, NL2SQL, Educational Analytics, Student Performance Prediction, Machine Learning, Semantic Layer, Explainable AI

---

## 2. Problem Statement and Motivation

School networks already maintain rich data — student rolls, marks, teacher KPIs (`HOF`, `ALL_COMBINED`, `TR`), absentees, exam schedules, and board percentages — but decision-makers cannot freely explore this data in everyday language. New analytical questions usually require developers to write custom SQL or Excel reports, causing delay and under-utilization of historical evidence. Equally important, institutions rarely use prior exam patterns to **forecast** upcoming outcomes, so at-risk students are often identified too late.

### 2.1 Market Context

The AI in Education market validates the demand for this project:

| Metric | Value | Source |
|---|---|---|
| AI in Education Market (2026) | $9.58B – $11.4B | Grand View Research, Precedence Research |
| Projected Growth by 2033 | $57.2B – $136.8B | Multiple analyst firms |
| CAGR | 25.9% – 36.0% | Grand View Research |
| Learning Analytics Segment (2026) | $16.99B | TechNavio |
| Pakistan EdTech Market (2025) | $407.9M | Market Research |
| Pakistan EdTech Projected (2034) | $2,865.2M (23.46% CAGR) | Market Research |

Pakistan's higher-education sector — including institutions like GIK Institute — has massive amounts of siloed academic data but **no local NL2SQL analytics platform**. EduQuery AI would be a first-mover in this rapidly growing market.

### 2.2 Gaps Addressed

**EduQuery AI** addresses three critical gaps:

1. **Accessibility** — non-technical users (teachers, administrators, principals) can query data through natural-language prompts without SQL knowledge.
2. **Flexibility** — ad-hoc questions are answered in real-time without waiting for developers to write new custom reports.
3. **Foresight** — historical exam parameters drive prediction of future results, enabling proactive intervention for at-risk students.

### 2.3 Academic Suitability

The project is academically suitable for Advanced AI because it combines large language models, database systems, machine learning, responsible AI design, and production engineering on a real institutional schema — spanning Weeks 3–8 of the GIKI-SkyLabs AI Bootcamp curriculum (NLP/Transformers, Agentic AI, RAG, MLOps, and Capstone).

---

## 3. Design Philosophy

This proposal is guided by a set of non-negotiable design principles, adapted from an evidence-based AI agent architecture:

### 3.1 DOX Framework — Documents as Source of Truth

The system's accuracy depends entirely on a **governed semantic layer** — a curated, human-authored definition of every table, column, metric, and business term in the academic schema. The AI never generates SQL from training-data guesswork alone; it always consults this documented semantic model.

**Why this matters:** Community consensus from NL2SQL practitioners in 2026 confirms that "accuracy depends more on semantic layer quality than LLM capability" (Reddit, HackerNews, technical forums). Traditional benchmarks (Spider) are insufficient for production; real-world accuracy requires result-set validation against documented ground truth.

### 3.2 Rigor Over Comfort

If a simpler approach produces worse accuracy, we do not keep it. Every technology choice is selected based on published benchmarks and community validation — not familiarity or ease of setup.

### 3.3 Evidence-Based Adaptation

All architectural decisions are backed by verifiable data:
- GitHub repository star counts and activity levels
- Published academic benchmarks (e.g., AutoGluon achieving 92.32% accuracy on student grade prediction)
- Market sizing data from Grand View Research, Precedence Research, and TechNavio
- Community feedback from Reddit, technical forums, and academic publications

### 3.4 Production Realism — "What Actually Breaks at Scale"

Every component is designed with failure modes in mind:
- SQL injection → prevented by SELECT-only validation and AST parsing
- LLM hallucination → mitigated by semantic layer grounding and query template matching
- Data privacy breach → enforced by Row-Level Security (RLS) and PII exclusion
- Model accuracy degradation → detected by continuous gold-prompt evaluation

### 3.5 Skills-Based Modularity

The system is decomposed into independent, replaceable modules (semantic layer, NL2SQL engine, ML prediction service, frontend). Each module can be upgraded, swapped, or scaled independently without affecting the rest of the system.

---

## 4. Proposed Solution

Users will type prompts such as:

- "Show Mathematics marks of Roll 12345 for Midterm Year 26."
- "Compare pass% of all schools in Class 9 English Annual."
- "Which teachers have pass% below board percentage?"
- "Predict Annual percentage of Roll 5522 in Physics from previous exams."
- "Why is Class 10 Science performance declining compared to last year?"

The system will interpret intent, map entities (school, class, section, subject, year, exam type, roll number, teacher), generate a **safe read-only** SQL query or prediction request, execute it against curated analytical views, and return a clear answer with charts, confidence indicators, and explanation.

### 4.1 Core Modules

| # | Module | Responsibility |
|---|---|---|
| 1 | **Authentication & RBAC** | JWT-based login, role-based access (admin, principal, teacher), campus-scoped data isolation |
| 2 | **Semantic Layer (DOX)** | Schema glossary, metric definitions, table relationships — the AI's "source of truth" |
| 3 | **NL2SQL Engine** | Intent classification, entity extraction, schema-aware SQL generation via governed semantic model |
| 4 | **SQL Validator** | SELECT-only enforcement, AST parsing, campus-scope injection, query sanitization |
| 5 | **ML Prediction Service** | AutoML ensemble for future exam outcomes with confidence intervals |
| 6 | **Explainability Engine** | SHAP-based feature importance for every prediction — "why is this student at risk?" |
| 7 | **Answer Composer** | Natural-language response generation, chart rendering, tabular output formatting |
| 8 | **Audit Logger** | Every query, prediction, and access event recorded for compliance and review |

Sensitive credential tables (passwords, OTP logs) will be excluded from the natural-language query surface.

---

## 5. Technology Stack (Research-Backed)

Every technology choice below is justified by published data. No assumptions.

### 5.1 NL2SQL Engine — Wren AI

| Attribute | Value |
|---|---|
| **Repository** | [Canner/WrenAI](https://github.com/Canner/WrenAI) |
| **GitHub Stars** | ~16,500+ ⭐ |
| **License** | Apache 2.0 (permissive, institutional-safe) |
| **SQL Server Support** | ✅ Native connector, read-only |
| **Semantic Layer** | ✅ Built-in Modeling Language (MDL) — maps "teacher pass rate" → actual SQL |
| **Visualization** | ✅ Charts and summaries included |
| **LLM Flexibility** | ✅ OpenAI, Gemini, Ollama (local) — provider-agnostic |
| **Deployment** | ✅ Self-hosted via Docker |

**Why Wren AI:** Community feedback from 2026 confirms that Wren AI is preferred over alternatives (e.g., Vanna AI) for governed, consistent analytics where metric definitions must be standardized across campuses. Its Modeling Language (MDL) enforces a single source of truth — exactly the DOX Framework principle. Vanna AI's primary repository was archived in March 2026, making Wren AI the safer long-term choice.

**Supplementary NL2SQL References:**

| Repository | Stars | Use For |
|---|---|---|
| [defog-ai/sqlcoder](https://github.com/defog-ai/sqlcoder) | 8,000+ | Fine-tuned NL2SQL models for local/private deployment |
| [sqlchat/sqlchat](https://github.com/sqlchat/sqlchat) | 5,800+ | UI reference — proven chat-to-SQL interface (Next.js) |
| [HKUSTDial/NL2SQL_Handbook](https://github.com/HKUSTDial/NL2SQL_Handbook) | 2,000+ | Research reference — latest techniques and benchmarks |

### 5.2 ML Prediction Engine — AutoGluon + SHAP

| Component | Tool | Justification |
|---|---|---|
| **AutoML Framework** | [AutoGluon Tabular](https://github.com/awslabs/autogluon) (8,000+ ⭐, Apache 2.0) | Best-in-class for tabular data; auto-ensembles XGBoost + LightGBM + CatBoost + DNNs |
| **Explainability** | [SHAP](https://github.com/slundberg/shap) (22,000+ ⭐, MIT) | Teachers need to understand *why* a student is predicted to be at-risk |
| **Foundation Model** | [TabPFN](https://github.com/PriorLabs/tabPFN) (2,500+ ⭐, Apache 2.0) | State-of-art zero-shot tabular prediction for datasets <50K rows |
| **Model Tracking** | [MLflow](https://github.com/mlflow/mlflow) (19,000+ ⭐, Apache 2.0) | Version models, track experiments, ensure reproducibility |

**Published Benchmark:** A March 2026 academic study demonstrated AutoGluon achieving **92.32% accuracy** predicting final letter grades from midterm and quiz scores (source: dergipark.org.tr) — directly applicable to EduQuery AI's prediction module.

**Why AutoGluon over raw scikit-learn/XGBoost:**
- AutoGluon automatically ensembles XGBoost + LightGBM + CatBoost + Deep Neural Networks
- Achieves state-of-the-art accuracy with 3 lines of code (`TabularPredictor.fit()`)
- 2026 systematic reviews in Educational Data Mining increasingly favor AutoML over manual model building

**Why SHAP is non-negotiable:**
Predictions without explanations are useless in an educational context. When EduQuery AI predicts "Roll 5522 has a 72% chance of failing Physics," the teacher must know **why** — e.g., "low attendance in weeks 3–5, declining midterm trajectory, class average significantly below board benchmark." SHAP provides this transparency.

### 5.3 API & Backend — Python FastAPI

| Component | Choice | Rationale |
|---|---|---|
| **Framework** | FastAPI | Native async, automatic OpenAPI docs, Pydantic validation |
| **Data Validation** | Pydantic v2 | Strict input schema enforcement before any query or prediction |
| **Server** | Gunicorn + Uvicorn workers | Production-grade concurrent request handling |
| **Containerization** | Docker | Environment consistency across dev, staging, production |

**Why Python-only (not ASP.NET + Python):** Wren AI, AutoGluon, SHAP, MLflow, and the entire ML/NLP ecosystem are Python-native. Adding ASP.NET creates unnecessary inter-process complexity without benefit.

### 5.4 Frontend — React/Next.js

| Component | Choice | Rationale |
|---|---|---|
| **Framework** | Next.js (React) | Server-side rendering, API routes, production-ready |
| **UI Reference** | [SQLChat](https://github.com/sqlchat/sqlchat) | Proven chat-to-SQL interface pattern (5,800+ ⭐) |
| **Charts** | Recharts / Chart.js | Interactive data visualization |
| **Auth** | JWT + Role-Based UI | Campus-scoped views based on user role |

### 5.5 Data Layer — SQL Server (Existing)

| Component | Choice | Rationale |
|---|---|---|
| **Primary Database** | Microsoft SQL Server (existing `db_aadc11_sqldaanish`) | Data already resides here — zero migration risk |
| **Security** | Row-Level Security (RLS) | Database-engine-enforced campus isolation |
| **ML Integration** | SQL Server Machine Learning Services | Optional in-database Python execution for sensitive data |
| **Semantic Views** | Curated analytical views | Clean interface over legacy/backup tables |

### 5.6 LLM Provider Strategy (Flexible)

The architecture is designed to be **LLM-agnostic**. The team will select the optimal provider during Phase 1 based on institutional requirements:

| Option | Provider | Cost | Data Privacy | Latency | Best For |
|---|---|---|---|---|---|
| **A — Cloud** | Azure OpenAI (GPT-4o) | ~$0.01–0.03/query | Data leaves campus | Low | Maximum accuracy, enterprise SLA |
| **B — Hybrid** | Azure OpenAI + local fallback | Moderate | Configurable | Medium | Balance of cost and privacy |
| **C — Local** | Ollama + Llama 3.2 / Qwen2.5 | Free (hardware only) | Data stays on-premise | Higher | Maximum privacy, zero API cost |

Wren AI natively supports all three options. The final choice depends on GIK Institute's data governance policy and available infrastructure.

---

## 6. System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        FRONTEND LAYER                           │
│  Next.js Web App │ Chat Interface │ Dashboard │ Role-Based Auth │
└────────────────────────────┬────────────────────────────────────┘
                             │
┌────────────────────────────▼────────────────────────────────────┐
│                     API GATEWAY (FastAPI)                        │
│                  Intent Router / Auth Middleware                 │
├──────────────┬──────────────────┬───────────────────────────────┤
│              │                  │                               │
│   ┌──────────▼──────────┐  ┌───▼───────────────┐  ┌───────────▼──────┐
│   │  NL2SQL ENGINE      │  │  ML PREDICTION    │  │  EXPLAINABILITY  │
│   │  (Wren AI)          │  │  SERVICE          │  │  ENGINE          │
│   │                     │  │                   │  │                  │
│   │  ├─ Semantic Layer   │  │  ├─ AutoGluon     │  │  ├─ SHAP Values   │
│   │  ├─ Schema Glossary  │  │  ├─ TabPFN        │  │  └─ Feature       │
│   │  ├─ SQL Generator    │  │  ├─ MLflow        │  │     Importance    │
│   │  └─ SQL Validator    │  │  └─ Model Registry│  │                  │
│   │    (SELECT-only)     │  │                   │  │                  │
│   └──────────┬──────────┘  └───┬───────────────┘  └──────────────────┘
│              │                  │
│   ┌──────────▼──────────────────▼───────────────────────────────┐
│   │              DATA LAYER                                      │
│   │  SQL Server (db_aadc11_sqldaanish)                          │
│   │  ├─ Row-Level Security (campus isolation)                    │
│   │  ├─ Curated Analytical Views                                 │
│   │  ├─ Audit Log Tables                                         │
│   │  └─ ML Services (optional in-database Python)                │
│   └─────────────────────────────────────────────────────────────┘
│                                                                  │
│   ┌──────────────────────────────────────────────────────────────┐
│   │              SECURITY & OBSERVABILITY                        │
│   │  ├─ JWT Authentication          ├─ Query Audit Trail         │
│   │  ├─ Role-Based Access Control   ├─ Prediction Logging        │
│   │  └─ PII Exclusion Layer         └─ Performance Monitoring    │
│   └──────────────────────────────────────────────────────────────┘
└─────────────────────────────────────────────────────────────────┘
```

### 6.1 Deployment Options

The Dockerized microservice architecture supports both deployment models:

| Option | Infrastructure | Cost | Scalability | Best For |
|---|---|---|---|---|
| **On-Premise** | GIK Institute servers + Docker | Hardware only | Vertical scaling | Maximum data control |
| **Cloud (Azure)** | Azure App Service + Azure SQL | Pay-as-you-go | Horizontal scaling | Elastic demand |

The final deployment target will be determined during Phase 1 based on institutional policy and available infrastructure.

---

## 7. Scope and Data Domains

The engine will support analytically meaningful questions across the main domains of the provided schema:

| Domain | Example Sources | What Users Can Ask |
|---|---|---|
| Students | `STUDENTS_ROLL`, `ALLSTD26`, profiles | Identity, strength, placement, house/category |
| Marks / Results | `MARKS`, `Marks_Internal`, `MPREV` | Transcripts, grades, fail subjects, trends |
| Class / School analytics | `TR`, `ALL_COMBINED_FINAL`, `GZT_STRENGTH` | Averages, pass%, percentage bands, rankings |
| Teacher performance | `HOF`, `TEAHCERS`, `TR` | Pass%, workload, position vs board |
| Board benchmarks | `BOARD_PER` | Gap between school and board performance |
| Attendance | `ABSENT`, `House_Attendance_Daily` | Absentees and attendance patterns |
| Exam operations | `Exam_Schedule`, marks-entry controls | Dates, deadlines, entry status |
| Prediction | Historical marks + context features | Next-exam % / grade / fail risk |

Legacy/backup tables will be handled through a curated semantic view layer to improve accuracy.

---

## 8. Prompt Capability Summary

Although natural language is open-ended, all meaningful schema-supported questions fall into these prompt families:

**A. Student lookup** — profiles, lists by school/class/section, enrollment counts.\
**B. Individual results** — subject-wise marks, grades, status, report-card style answers.\
**C. Class/section aggregates** — averages, band counts (90–100 … 0–39), top scorers, pass%.\
**D. Cross-school comparison** — rank schools by subject/class performance.\
**E. Teacher analytics** — HOF-style KPIs, workload, board comparison.\
**F. Board benchmark** — subjects/schools below board norms.\
**G. Absenteeism/attendance** — exam absentees and house attendance.\
**H. Exam operations** — schedules, deadlines, marks-entry openness.\
**I. Data-quality checks** — missing marks, incomplete results.\
**J. Trends/diagnostics** — multi-year and multi-exam improvement or decline.\
**K. Prediction** — forecast next exam percentage, grade band, or pass probability.\
**L. Explanation** — "why is performance low?" and remedial focus lists with SHAP-powered feature attribution.

Together, these families cover essentially all practical queries derivable from the schema without requiring users to know SQL.

---

## 9. Future Exam Result Prediction

A central innovation of this project is prediction of future examination outcomes from previous parameters.

### 9.1 Prediction Targets

- Predicted percentage per student per subject
- Grade band classification (A, B, C, D, F)
- Pass/fail probability with confidence interval
- Aggregate forecasts (class average, school-level pass%)
- At-risk student identification with ranked severity

### 9.2 Key Input Features

```
├── Prior obtained marks and percentages across exam types (lagged features)
├── Subject / class / school / section / year context
├── Class averages and student strength (contextual)
├── Teacher historical pass% and workload (from HOF/TR)
├── Board percentage gap (school vs board benchmark)
├── Absentee flags and patterns (from ABSENT table)
├── Performance trajectory (improvement or decline slope over recent exams)
└── Cyclical features (exam type encoding: midterm, annual, etc.)
```

### 9.3 Approach

**Adaptive Model Selection:** The ML pipeline is designed to be data-driven rather than prescriptive:

| Data Volume | Primary Model | Fallback |
|---|---|---|
| < 50,000 rows | TabPFN (zero-shot foundation model) | AutoGluon ensemble |
| ≥ 50,000 rows | AutoGluon `best_quality` ensemble | XGBoost + Optuna tuning |

**Validation Strategy:** Strict temporal splitting — earlier exams train the model, later exams test it. Random train/test splits are explicitly prohibited to prevent data leakage.

**Explainability:** Every prediction is accompanied by SHAP feature attribution, showing which factors (attendance, prior marks, teacher pass%, board gap) contributed most to the prediction. This is mandatory for educational decision-making.

Predictions include confidence indicators and are intended as **decision support for educators**, not automatic academic judgments.

### 9.4 Published Validation

A March 2026 academic study demonstrated AutoGluon achieving **92.32% accuracy** predicting final letter grades from midterm and quiz scores using ensemble methods — directly applicable to EduQuery AI's prediction targets. A separate July 2026 study validated AutoGluon for student dropout prediction on imbalanced educational datasets.

---

## 10. Objectives and Deliverables

### 10.1 Objectives

1. Build a governed semantic model (DOX layer) of the academic schema for AI querying.
2. Implement a prompt engine that answers all 12 prompt families (A–L) above.
3. Deliver a prediction module for future exam outcomes with explainability.
4. Ensure security through read-only access, role-based filters, RLS, and audit logs.
5. Demonstrate measurable accuracy on a gold set of ≥200 academic prompts.
6. Provide SHAP-based explanations for every prediction to support educator decision-making.

### 10.2 Deliverables

| Deliverable | Description |
|---|---|
| **Working Prototype** | Web-based EduQuery AI application (FastAPI + Next.js + Wren AI) |
| **Semantic Layer Documentation** | Schema glossary, metric definitions, MDL configuration |
| **Gold Prompt Set** | ≥200 test prompts with expected answers and evaluation results |
| **Trained Models** | AutoGluon ensemble + TabPFN models with MLflow tracking |
| **Explainability Reports** | Sample SHAP analyses for representative student predictions |
| **Security Audit** | RLS verification, SQL injection test results, PII exclusion proof |
| **Final Report & Demo** | Comprehensive documentation and live demonstration |

---

## 11. Methodology and Timeline

| Phase | Weeks | Focus | Team Lead | Outcome |
|---|---|---|---|---|
| **Phase 1** | 1–2 | Schema study, Wren AI semantic layer setup, LLM provider selection | Junaid | Curated views, glossary, Wren AI connected to SQL Server |
| **Phase 2** | 3–5 | NL2SQL MVP (prompt families A–D) + frontend scaffold | Junaid + Abeera | Core student/marks/school prompts working with chat UI |
| **Phase 3** | 6–7 | Advanced analytics (E–H) + prediction data pipeline | Rafay + Zain | Teacher, board, attendance prompts + ML feature engineering |
| **Phase 4** | 8–10 | ML prediction module (AutoGluon + SHAP) + API integration | Zain + Rafay | Prediction with explainability, MLflow tracking |
| **Phase 5** | 11–12 | Security hardening, gold prompt evaluation, documentation | Full Team | RBAC, audit logs, ≥80% accuracy, final demo |

### 11.1 Team Responsibilities

| Member | Primary Ownership | Secondary Support |
|---|---|---|
| **Muhammad Junaid** | Wren AI semantic layer, NL2SQL engine, schema glossary | SQL validation, LLM integration |
| **M. Zain ul Abideen** | AutoGluon/TabPFN prediction pipeline, SHAP explainability | MLflow tracking, model evaluation |
| **Abdur Rafay** | FastAPI backend, Docker deployment, API gateway | Security (JWT, RLS), audit logging |
| **Abeera Anwer** | Next.js frontend, chat UI, dashboard visualization | Gold prompt set design, UX testing |

---

## 12. Risk Management

Each risk is assessed with severity, probability, and a concrete mitigation strategy:

### 12.1 LLM Hallucination in SQL Generation
- **Severity:** 🔴 Critical | **Probability:** Medium
- **What could go wrong:** The LLM generates syntactically correct but semantically wrong SQL (e.g., confusing `midterm_marks` with `annual_marks`, or joining wrong tables).
- **Mitigation:** Wren AI's Modeling Language (MDL) constrains the LLM to only use pre-defined metric definitions and table relationships. Every generated query passes through an AST validator that enforces SELECT-only syntax and verifies that all referenced columns exist in the semantic model. Additionally, a library of "golden queries" (verified question→SQL pairs) provides few-shot examples that anchor the LLM's output.

### 12.2 Student Data Privacy Breach
- **Severity:** 🔴 Critical | **Probability:** Low
- **What could go wrong:** A user gains access to another campus's student data, or PII (personal identifiable information) leaks into LLM API calls.
- **Mitigation:** Three layers of defense: (1) SQL Server Row-Level Security (RLS) enforces campus-scoped data isolation at the database engine level — even if the application has a bug, the database itself prevents cross-campus queries. (2) A PII exclusion layer strips password hashes, OTP logs, and unnecessary personal identifiers before any data reaches the LLM context window. (3) JWT-based authentication with role claims ensures users only see data appropriate to their role (admin, principal, teacher).

### 12.3 ML Model Accuracy Below Target
- **Severity:** 🟡 Medium | **Probability:** Medium
- **What could go wrong:** The prediction model fails to achieve the ≥80% accuracy target due to insufficient historical data, noisy features, or class imbalance.
- **Mitigation:** AutoGluon's ensemble approach (stacking XGBoost + LightGBM + CatBoost + DNNs) provides inherent robustness. For small datasets, TabPFN's zero-shot foundation model serves as a fallback. Continuous evaluation against a gold prompt set enables early detection of accuracy drift. If accuracy remains below target, the team will implement targeted feature engineering (adding attendance patterns, teacher workload correlations) and expand the training dataset with additional historical years.

### 12.4 SQL Server Version Compatibility
- **Severity:** 🟡 Medium | **Probability:** Medium
- **What could go wrong:** The existing SQL Server instance is version 2016 or older, which reached End of Life in July 2026 and lacks Python ML Services.
- **Mitigation:** Phase 1 includes a SQL Server version assessment. The NL2SQL engine (Wren AI) works with SQL Server 2014+. For the ML prediction service, if the server version is too old for in-database Python, the prediction module will operate as an external FastAPI microservice that connects via read-only ODBC — no server upgrade required for core functionality.

### 12.5 LLM API Cost at Scale
- **Severity:** 🟡 Medium | **Probability:** Low–Medium
- **What could go wrong:** High query volume drives Azure OpenAI API costs beyond budget.
- **Mitigation:** The architecture supports three LLM options (cloud, hybrid, local). If costs escalate, the team can switch to a local model (Ollama + Llama 3.2) with zero API cost. Additionally, Headroom (an open-source LLM context compression proxy at [headroomlabs-ai/headroom](https://github.com/headroomlabs-ai/headroom)) can reduce token usage by 60–95% for database query results, significantly cutting API costs while maintaining accuracy.

### 12.6 NL2SQL Tool Ecosystem Risk
- **Severity:** 🟢 Low | **Probability:** Low
- **What could go wrong:** Wren AI project is abandoned or makes breaking changes.
- **Mitigation:** Wren AI is licensed under Apache 2.0 (permissive, forkable), has 16,500+ GitHub stars, and maintains an active community. If needed, the NL2SQL engine can be replaced with Defog SQLCoder (8,000+ ⭐) or a custom RAG pipeline using LangChain without affecting other system modules, thanks to the skills-based modular architecture.

---

## 13. Evaluation, Ethics, and Importance

### 13.1 Success Metrics

| Metric | Target | Measurement Method |
|---|---|---|
| NL2SQL accuracy | ≥80% acceptable answers | Gold prompt set (≥200 prompts) with human evaluation |
| SQL execution success | ≥95% for validated prompts | Automated testing against expected result sets |
| Prediction accuracy | Better than historical average baseline | Temporal cross-validation on held-out exam data |
| Prediction explainability | 100% of predictions have SHAP output | Automated check — no prediction served without explanation |
| Usability | Usable by non-technical academic staff | User testing with 5+ teachers/administrators |
| Response latency | < 5 seconds for NL2SQL, < 3 seconds for prediction | Automated performance benchmarking |

### 13.2 Ethics and Responsible AI

- **Data Privacy:** Exclude passwords, OTP logs, and unnecessary personal identifiers from AI prompting. Apply campus-scoped access via RLS.
- **Advisory Predictions:** All predictions are explicitly labeled as **decision support for educators**, not automatic academic judgments. No student's grade, placement, or future will be determined by AI alone.
- **Bias Monitoring:** Track prediction accuracy across demographic subgroups (gender, school, section) to detect and address systematic bias.
- **Transparency:** SHAP explanations accompany every prediction, ensuring educators understand the basis for each recommendation.
- **Audit Trail:** Every query, prediction, and data access is logged for institutional compliance and review.

### 13.3 Why This Matters

The system turns an existing institutional database into an interactive AI assistant for academic decision-making — faster reporting, earlier risk detection, fairer teacher/school review against board norms, and evidence-based planning across campuses. For GIK Institute and the broader Pakistan education sector, it demonstrates that AI can be practically deployed to improve educational outcomes without requiring massive infrastructure investment.

---

## 14. Competitive Analysis

| Competitor | Focus | Pricing | EduQuery AI Advantage |
|---|---|---|---|
| Civitas Learning | Higher Ed retention | $50K+/year license | Free/open-source stack, local data control |
| PowerSchool | K-12 comprehensive | Enterprise pricing | Purpose-built for multi-campus Pakistan context |
| BrightBytes | K-12 analytics | SaaS subscription | NL2SQL + prediction (not just dashboards) |
| Querio.ai | General NL2SQL | Enterprise | Education-specific semantic layer |
| Manual SQL/Excel | Current state | Developer time | 10x faster, non-technical user access |

---

## 15. References and Open-Source Stack

### 15.1 Core Technology Repositories

| Repository | Stars | License | Role in EduQuery AI |
|---|---|---|---|
| [Canner/WrenAI](https://github.com/Canner/WrenAI) | 16,500+ | Apache 2.0 | NL2SQL semantic engine |
| [awslabs/autogluon](https://github.com/awslabs/autogluon) | 8,000+ | Apache 2.0 | ML prediction (tabular AutoML) |
| [slundberg/shap](https://github.com/slundberg/shap) | 22,000+ | MIT | Model explainability |
| [mlflow/mlflow](https://github.com/mlflow/mlflow) | 19,000+ | Apache 2.0 | Experiment tracking |
| [sqlchat/sqlchat](https://github.com/sqlchat/sqlchat) | 5,800+ | BSL | UI design reference |
| [defog-ai/sqlcoder](https://github.com/defog-ai/sqlcoder) | 8,000+ | Apache 2.0 | Local NL2SQL model reference |
| [PriorLabs/tabPFN](https://github.com/PriorLabs/tabPFN) | 2,500+ | Apache 2.0 | Tabular foundation model |

### 15.2 Research References

| Resource | Type | Relevance |
|---|---|---|
| [HKUSTDial/NL2SQL_Handbook](https://github.com/HKUSTDial/NL2SQL_Handbook) | Research handbook | Latest NL2SQL techniques and benchmarks |
| [eosphoros-ai/Awesome-Text2SQL](https://github.com/eosphoros-ai/Awesome-Text2SQL) | Curated list | NL2SQL datasets, models, and fine-tuning guides |
| [bigdata-ustc/EduX](https://github.com/bigdata-ustc/EduX) | EDM toolkit | Educational data mining algorithms and datasets |
| AutoGluon Student Grade Prediction Study (2026) | Academic paper | 92.32% accuracy benchmark (dergipark.org.tr) |

### 15.3 Market Data Sources

- Grand View Research — AI in Education Market Report 2026
- Precedence Research — AI in Education Market Forecast 2035
- IMARC Group — Global AI in Education Report
- DataM Intelligence — AI in Education Analysis
- TechNavio — Learning Analytics Market 2026

---

## 16. Conclusion

**EduQuery AI** is a practical Advanced AI capstone that unites prompt-based natural-language querying with educational data analytics and future examination result prediction over a real multi-campus academic schema. It is built on a research-backed technology stack (Wren AI + AutoGluon + SHAP + FastAPI), guided by a design philosophy that prioritizes documented truth, evidence-based decisions, and production realism.

The project is technically rigorous, institutionally useful, and aligned with the learning goals of the Bootcamp — Advanced AI 2026 at GIK Institute, Topi.

---

**Proposed Team:**\
Muhammad Junaid (Thejunaid1799@gmail.com)\
M. Zain ul Abideen (Zainsardar062@gmail.com)\
Abdur Rafay (Abdurrafay222@gmail.com)\
Abeera Anwer (sobisobangoyes@gmail.com)

**Submitted To:** Dr. Ali Imran\
**Institution:** GIK Institute, Topi


