# EduQuery AI: Final Capstone Project Report

**Project Title:** EduQuery AI: A Prompt-Based Intelligent Analytics and Prediction Engine for Multi-Campus Academic Databases  
**Program:** AI Bootcamp 2026 by Skylabs in Collaboration with Ghulam Ishaq Khan Institute of Engineering Sciences and Technology (GIK Institute), Topi  
**Target Institutional Partner:** Daanish Schools and Centers of Excellence Authority, Punjab, Pakistan  
**Document Type:** Final Capstone Engineering Report and System Documentation  
**Date:** August 20, 2026  

---

## Team Ownership and Roles

| Member Name | Role | Core Technical Responsibilities |
|---|---|---|
| **Muhammad Junaid** (Lead) | Project Lead and Semantic Layer Architect | Wren AI semantic engine, MDL modeling, gold prompt evaluation suite, project governance |
| **Abdur Rafay** | Backend Architecture and Security Lead | FastAPI API gateway, SQL AST validator, PII privacy redactor, audit logging, database adapters |
| **Abeera Anwer** | Frontend Architecture and UX Lead | Next.js chat interface, portal integration, data visualizations, design system, accessibility |
| **Zain ul Abideen** | Machine Learning and Prediction Lead | AutoGluon tabular ensembles, TabPFN integration, MLflow tracking, SHAP explainability engine |

---

## 1. Executive Summary

Educational institutions across Pakistan manage massive volumes of student records, examination histories, teacher workloads, and attendance logs. However, most of this information remains locked inside legacy databases and rigid software interfaces. Decision-makers like principals, academic coordinators, and head office directors must constantly request custom SQL reports or manually combine spreadsheets to answer basic analytical questions. Furthermore, existing administrative software is purely retrospective. It records what happened in past exams, but provides no predictive foresight to identify struggling students before high-stakes board examinations occur.

EduQuery AI solves this bottleneck. Built as a capstone project for the AI Bootcamp offered by Skylabs in collaboration with GIKI Institute, EduQuery AI is an intelligent, prompt-based analytics and prediction engine designed specifically for the Daanish Schools network (`db_aadc11_sqldaanish`).

The platform operates across three primary functional pillars:

1. **Natural Language Database Analytics (NL2SQL):** Authorized staff can ask complex questions in plain English (such as "Compare the Class 9 Mathematics pass percentage across all girls campuses in Midterm 2026") and receive instant, validated answers with structured tables and visual charts. The engine is grounded by a strict semantic modeling layer (Wren AI 0.13.2) over 68 curated database views, eliminating guesswork and hallucinated SQL.
2. **Policy Guidance and Administrative Retrieval (RAG):** Using a local vector store (LanceDB) and hybrid keyword-vector search, the platform ingests official school policy documents (such as sibling admissions, induction criteria, leave rules, and day scholar quotas). It provides exact, line-citable answers to administrative questions while preserving human decision authority.
3. **Predictive Analytics and Explainable AI (AutoGluon + TabPFN + SHAP):** By training machine learning ensembles on historical academic trajectories, the engine forecasts future examination outcomes, highlights at-risk students, and outputs SHAP (SHapley Additive exPlanations) feature attributions explaining the exact factors behind every prediction.

To guarantee institutional compliance and student data privacy, EduQuery AI enforces strict local data sovereignty. Student records, examination marks, and identifiable demographic information never leave the institutional boundary. The system includes an abstract syntax tree (AST) SQL validator that permits only single-statement SELECT queries, a local PII redaction filter, and a comprehensive security audit logger.

Across a benchmark suite of 610 school-supplied gold prompts, EduQuery AI successfully compiled 515 analytical queries across 16 verified single-object semantic models, executed 510 out of 515 queries under a live 4-worker concurrent stress test, and correctly issued 95 governed refusals for unmapped queries, all with zero external cloud dependencies.

---

## 2. Institutional Context and Problem Statement

### 2.1 The Daanish Schools Operating Environment

The Punjab Daanish Schools and Centers of Excellence Authority operates a network of 20 residential campuses across Punjab, including boys and girls wings in Attock, Chishtian, Dera Ghazi Khan, Hasilpur, Mianchannu, Mianwali, Rajanpur, Rahim Yar Khan, Taunsa, and Vehari.

Daanish Schools provide completely free, high-quality residential education to underprivileged children. Because students live on campus 24 hours a day under the institution's care, school leadership and the provincial government hold strict accountability for student welfare, academic growth, and post-graduation outcomes.

The centralized Microsoft SQL Server database (`db_aadc11_sqldaanish`) contains records spanning multiple academic years, including student enrollments, daily house attendance, internal evaluations (Midterm and Mock exams), and external Board of Intermediate and Secondary Education (BISE) results.

```
+-------------------------------------------------------------------------------+
|                       Daanish Schools Campus Network                          |
|  20 Residential Campuses (Attock, Chishtian, DG Khan, Hasilpur, Mianchannu,   |
|   Mianwali, Rajanpur, Rahim Yar Khan, Taunsa, Vehari: Boys & Girls Wings)    |
+---------------------------------------+---------------------------------------+
                                        |
                                        v
+-------------------------------------------------------------------------------+
|                       db_aadc11_sqldaanish (SQL Server)                       |
|           69 Base Tables | 68 Curated Views | ~2,000,000 Student Records       |
+---------------------------------------+---------------------------------------+
                                        |
              +-------------------------+-------------------------+
              |                                                   |
              v                                                   v
+---------------------------+                           +---------------------------+
|    The Legacy Reality     |                           |    The EduQuery AI Way    |
| - Predefined dropdowns    |                           | - Plain English queries   |
| - Manual SQL scripts      |                           | - Governed Wren AI MDL    |
| - Multi-day report delays |                           | - Sub-second answers      |
| - Disconnected PDF rules  |                           | - Line-citable Policy RAG |
| - Zero future foresight   |                           | - SHAP-explained ML risk  |
+---------------------------+                           +---------------------------+
```

### 2.2 The Operational Problem

Despite having a hosted web portal, the academic administration faces three major operational friction points:

1. **The Rigid Interface Bottleneck:** The existing portal uses fixed dropdown combinations to filter student results. When head office directors, regional coordinators, or campus principals ask non-standard or comparative questions (such as "Show the trend of failure rates in Physics for Class 10 over the last three years" or "Which teachers have a pass percentage below the board benchmark?"), the system cannot generate an answer. An IT staff member must manually write custom SQL, extract raw data, clean it in spreadsheets, build graphs, and compile reports. This process creates delays of days or weeks.
2. **The Lack of Predictive Foresight:** Administrative decisions are entirely reactive. Remedial classes and counseling are typically organized only after a student has already failed an official exam. The school lacks automated forecasting to spot downward performance trajectories early in the academic session.
3. **Fragmented Institutional Knowledge:** Official policies governing student admissions, poverty criteria, medical emergencies, discipline, and fee quotas exist as disconnected PDF files. Staff members frequently struggle to locate the applicable clause for specific student cases, risking inconsistent administrative decisions.

---

## 3. System Architecture and End-to-End Workflow

EduQuery AI is engineered as a modular, decoupled web platform. It isolates sensitive data handling within the institutional network while providing an accessible interface to end users.

```
+-------------------------------------------------------------------------------+
|                                FRONTEND LAYER                                 |
|         Next.js Web Interface | Tailwind CSS | Recharts Data Visualization    |
|                  Hosted inside School Portal (Admin Entry)                    |
+---------------------------------------+---------------------------------------+
                                        | (HTTPS / JSON API)
                                        v
+-------------------------------------------------------------------------------+
|                       API GATEWAY & SECURITY LAYER                            |
|             FastAPI Service | JWT Authentication | Audit Logger               |
|            SQLGlot AST Validator (SELECT-Only) | Local PII Redactor           |
+-------------------+-------------------+-------------------+-------------------+
                    |                   |                   |
                    v                   v                   v
+-----------------------+ +-----------------------+ +-----------------------+
|  NL2SQL ENGINE (Wren) | |   POLICY RAG ENGINE   | | ML PREDICTION ENGINE  |
| - 16 Strict Models    | | - Local LanceDB       | | - AutoGluon Ensemble  |
| - Governed MDL Layer  | | - 9 Official Policies | | - TabPFN Foundation   |
| - T-SQL Synthesis     | | - Line-Level Citations| | - SHAP Explainability |
+-----------+-----------+ +-----------+-----------+ +-----------+-----------+
            |                         |                         |
            +-------------------------+-------------------------+
                                      |
                                      v
+-------------------------------------------------------------------------------+
|                               DATA LAYER                                      |
|                 Microsoft SQL Server (db_aadc11_sqldaanish)                   |
|           Read-Only Diagnostic Replica | 68 Reconciled Analytical Views       |
+-------------------------------------------------------------------------------+
```

### 3.1 Component Breakdown

* **Frontend Application (`apps/web/`):** A responsive web application built with Next.js, React, and Tailwind CSS. It connects to the backend through typed JSON contracts and presents streaming responses, interactive data tables, and dynamic charts.
* **API Gateway (`services/api/`):** A Python FastAPI service managing request routing, JWT authentication, rate limiting, request correlation IDs, and standard error serialization.
* **SQL AST Validator (`services/api/query/validator.py`):** An Abstract Syntax Tree parsing engine based on `sqlglot`. It parses all generated SQL statements, verifies single-statement execution, enforces SELECT-only permissions, checks referenced views against a strict allowlist, and automatically injects query limits to prevent database exhaustion.
* **PII Privacy Redactor (`services/api/privacy/redactor.py`):** A deterministic regex and heuristic filter that intercepts incoming text and masks student roll numbers, CNICs, phone numbers, email addresses, and full names before any external processing occurs.
* **Semantic Layer and NL2SQL Engine (`services/query/`):** A governed modeling layer using Wren AI 0.13.2. It maps natural language questions to 16 verified single-object models, preventing schema hallucination.
* **Policy RAG Vector Engine (`services/query/rag_store.py`):** A local vector retrieval engine using LanceDB, local BAAI/bge-small-en embeddings, and an MS-MARCO re-ranking pipeline. It retrieves exact policy passages from 9 verified Markdown files across 144 line-numbered chunks.
* **Prediction Service (`services/prediction/`):** A machine learning inference module utilizing AutoGluon Tabular ensembles, TabPFN foundation models, and TreeSHAP explainability to predict student performance.
* **Database Layer:** Microsoft SQL Server 2022 (`db_aadc11_sqldaanish`), accessed exclusively through a dedicated read-only connection.

### 3.2 End-to-End Request Flow

When an authorized user submits a prompt, the system executes the following steps:

1. **Authentication and Authorization:** The FastAPI gateway validates the user's JWT token, verifies active session claims, and assigns a unique request tracking UUID.
2. **Intent Classification:** The prompt is analyzed to determine whether the user is requesting structured database analytics, institutional policy guidance, or predictive student risk scoring.
3. **Safety and Privacy Gating:** The prompt passes through the local PII redactor. If an external model is configured, identifiable tokens are replaced with semantic tags (`[ROLL_NO]`, `[STUDENT_NAME]`). When external models are disabled (the default setting), the request stays entirely on local deterministic engines.
4. **Governed Query Synthesis:** For database analytics, the prompt is matched against the Wren AI Modeling Definition Language (MDL) catalog to select the appropriate semantic model and generate standard T-SQL.
5. **AST Security Verification:** The synthesized SQL is parsed into an AST. If it contains data modification commands (such as `DROP`, `UPDATE`, or `INSERT`), multiple statements separated by semicolons, or unapproved tables, the query is rejected immediately with an informative security error.
6. **Read-Only Database Execution:** The sanitized SQL query executes against the read-only SQL Server instance with strict timeout limits (5 to 10 seconds).
7. **Answer Composition:** The raw result rows are formatted into a natural language response, accompanied by structured tabular data and visualization metadata.
8. **Audit Logging:** The complete interaction (user identifier, timestamp, prompt category, sanitized SQL, execution latency, and row count) is recorded in structured JSON logs for administrative review.

---

## 4. Governed Semantic Layer and Database Engineering

A core principle of EduQuery AI is that natural language query accuracy depends far more on the quality and governance of the semantic layer than on the size of the underlying language model. Raw educational databases contain complex legacy naming conventions, missing foreign keys, and denormalized structures that cause unconstrained language models to hallucinate incorrect SQL queries.

### 4.1 Database Profile and Schema Reconciliation

The target database, `db_aadc11_sqldaanish`, contains 69 base tables and 68 views, totaling approximately 2 million records. To ensure data integrity, the engineering team performed an automated reconciliation audit between the live database catalog and canonical project definitions (`docs/07-evidence/sql-view-reconciliation/`). 

The audit proved:
* Exactly 68 live views matched 68 canonical definitions.
* Cryptographic normalized hash comparison (SHA-256: `93b40692d521d655d8e70b5cfeaa1935d839864a85473179df3bc443f342e21c`) achieved a 100% match across all definitions.
* Zero unmapped, duplicated, or missing views were identified.

### 4.2 Managing Legacy Database Quirks Without Unsafe Writes

The live database contains several historical naming defects, such as misspelled table names (`TEAHCERS`), misspelled column names (`CATEGROY` instead of `CATEGORY`), and non-standard special characters (`[%]`, `[PASS%]`, `[CLASS AVG]`, `[WORK LOAD]`, `[BELOW 70%]`, `[ABOVE 70%]`).

Because the production database is an active institutional asset, EduQuery AI enforces a strict no-write policy. Rather than risking database corruption by running alter scripts on live tables, all schema normalization is handled through the Wren AI semantic layer:

1. **Physical to Logical Mapping:** The semantic layer maps clean logical concepts (such as `pass_percentage`, `class_average`, and `teacher_name`) to the exact physical bracketed column names in T-SQL.
2. **Handling the Absence of a Pass Status:** In `STUDENTS_RESULT_TOTAL`, the `STATUS` column only contains `'FAIL'` or a list of failed subject names. The word `'PASS'` does not exist in the database. The semantic layer automatically compiles pass queries using `(STATUS <> 'FAIL' OR STATUS IS NULL)` or score checks (`[%] >= 33`), preventing empty query results.
3. **Optimized Aggregations:** To prevent timeouts on complex ranking queries, the semantic layer routes student total queries to pre-aggregated rows (`SUBJECT = 'TOTAL'`) in `dbo.students_result_total`, cutting query execution times from over 12 seconds down to 115 milliseconds.

### 4.3 Catalog of the 16 Verified Semantic Models

The semantic layer implements 16 single-object models covering all critical academic domains:

| # | Model Name | Source Object | Core Metrics and Fields | Primary Use Case |
|---|---|---|---|---|
| 1 | `student_enrollment` | `STUDENTS_ROLL_INTERNAL_EXAM` | `campus`, `roll_number`, `student_name`, `class_level`, `section`, `year` | Student rosters, campus enrollments, section counts |
| 2 | `board_enrollment` | `STUDENTS_ROLL` | `campus`, `roll_number`, `student_name`, `category`, `quota` | BISE board registration lists, quota verifications |
| 3 | `annual_student_results` | `STUDENTS_RESULT_TOTAL` | `student_name`, `roll_number`, `subject`, `obtained_marks`, `percentage`, `status` | Annual board results, subject toppers, fail lists |
| 4 | `student_result_card` | `STUDENTS_RESULT_TOTAL_INTERNAL` | `roll_number`, `exam_type`, `subject`, `obtained_marks`, `total_marks`, `grade` | Internal term report cards (Midterm and Mock exams) |
| 5 | `board_marks` | `MARKS` | `roll_number`, `subject`, `obtained_marks`, `percentage`, `grade`, `exam_type` | Historical board exam marks and transcripts |
| 6 | `practical_marks` | `PRAC` | `roll_number`, `subject`, `obtained_marks`, `total_marks`, `percentage` | Science practical exam scores |
| 7 | `teacher_results` | `TR_ALL` | `teacher_name`, `subject`, `class_level`, `appeared`, `passed`, `pass_percentage` | Combined teacher evaluation across all subjects |
| 8 | `theory_teacher_results` | `TR2_THEORY` | `teacher_name`, `subject`, `class_level`, `appeared`, `passed`, `pass_percentage` | Theory subject teacher evaluation metrics |
| 9 | `practical_teacher_results`| `TR2_PRAC` | `teacher_name`, `subject`, `class_level`, `appeared`, `passed`, `pass_percentage` | Practical subject teacher evaluation metrics |
| 10 | `teacher_career` | `ALL_COMBINED` | `teacher_name`, `workload`, `pass_percentage`, `above_70`, `below_70`, `position` | Longitudinal teacher performance history |
| 11 | `head_office_results` | `HOF_FRMT` | `teacher_name`, `pass_percentage`, `board_pass_percentage`, `position`, `workload` | Executive head office teacher monitoring |
| 12 | `internal_teacher_results` | `INTERNAL_EXAM_GROUP_WISE_PERFORMANCE_VIEW` | `teacher_name`, `exam_type`, `class_percentage`, `class_average`, `passed` | Internal exam teacher performance |
| 13 | `teacher_board_middle` | `VTEACHER_SUM_PER` | `teacher_name`, `category`, `sum_obtained`, `sum_total`, `percentage` | Middle school teacher board performance |
| 14 | `house_attendance` | `HOUSE_ATTENDANCE_DAILY` | `campus`, `house`, `date`, `present_count`, `absent_count`, `leave_count` | Residential house daily attendance logs |
| 15 | `exam_absentees` | `ABSENT` | `campus`, `roll_number`, `class_level`, `exam_type`, `subject`, `is_absent` | Examination absenteeism monitoring |
| 16 | `board_benchmarks` | `BOARD_PER` | `campus`, `subject`, `class_level`, `school_pass_percentage`, `board_pass_percentage` | Institutional gap analysis against BISE averages |

---

## 5. Policy Guidance Retrieval Engine (RAG)

In addition to querying structured tabular data, educational administrators frequently need to interpret institutional rules. EduQuery AI integrates a dedicated, citation-grounded Retrieval-Augmented Generation (RAG) subsystem.

### 5.1 Transition from OCR to Verified Markdown Corpus

Early experiments with optical character recognition (OCR) over scanned policy PDFs revealed text noise, lost tables, and misread policy thresholds. To ensure absolute fidelity, the engineering team converted the 9 official Daanish School policy documents into clean Markdown files (`data/policy_rag_markdown_r4/`):

1. **Policy Regarding Admission of Siblings:** Criteria for admitting brothers and sisters of enrolled students.
2. **Induction Policy:** Socioeconomic criteria, poverty scorecards, and entry age limits (boys: 10 to 12 years, girls: 10 to 13 years).
3. **Leave Policy:** Medical leaves, casual leaves, weekend permissions, and gate pass protocols.
4. **Medical Policy for Students:** 24/7 dispensary procedures, resident medical officer duties, infectious disease isolation, and hospital referrals.
5. **Day Scholars Policy:** Fee structures (Rs. 2,000 monthly), seat quotas (maximum 30 per school, 10 per class), and timing for non-residential local students.
6. **Day Care Centre Policy:** Facilities, staff eligibility, and timing for female faculty with infants.
7. **Late Arrival of Students Policy:** Punctuality rules, morning assembly gate closures, and progressive warnings.
8. **Promotion and Discharge Policy:** Academic thresholds, minimum pass marks, and expulsion grounds.
9. **School Instructions:** General residential operational directives.

### 5.2 Retrieval Mechanics and Deterministic Citation Grounding

The policy assistant operates entirely on local infrastructure:

* **Chunking Strategy:** Documents are partitioned into 144 coherent sections. Each chunk preserves its parent headers, section numbers, and exact starting and ending line numbers from the source Markdown file.
* **Vector Indexing:** Text chunks are embedded using `BAAI/bge-small-en` and stored in an embedded LanceDB database.
* **Hybrid Search and Re-Ranking:** When a user asks an administrative question, the engine performs vector similarity search combined with exact keyword filtering, followed by a second-stage cross-encoder re-ranking step (`Xenova/ms-marco-MiniLM-L-6-v2`).
* **Line-Level Citations:** Every generated response displays the exact document name, section title, line numbers, and cryptographic file hash. The assistant explicitly presents direct quotes from the policy, ensuring that administrative actions remain transparent and legally defensible.

---

## 6. Predictive Modeling and Explainable AI Engine

A distinguishing feature of EduQuery AI is its machine learning pipeline, which moves institutional reporting from retrospective summaries to proactive student support.

### 6.1 Feature Engineering and Temporal Validation

The prediction engine forecasts a student's upcoming examination percentage, letter grade (A+, A, B, C, D, E, F), and risk of failure based on comprehensive historical parameters:

* **Lagged Examination Marks:** Scores, percentages, and grade trajectories across previous Midterm, Mock, and Annual exam sessions.
* **Contextual Features:** Campus gender wing, class level (Classes 6 through 12), academic section, and subject track (Pre-Medical, Pre-Engineering, Computer Science, Arts).
* **Teacher Influence Metrics:** Historical pass percentage and workload indicators extracted from `HOF_FRMT` and `TR_ALL`.
* **Institutional Benchmarks:** Difference between campus class average and the provincial BISE board pass percentage.
* **Attendance and Absenteeism:** Prior absence flags during examination cycles.

To prevent data leakage, the pipeline enforces strict temporal splitting. Models are trained on chronologically earlier examination cycles and evaluated on subsequent, unseen terms. Random cross-validation is strictly avoided because shuffling future exam data into past training sets artificially inflates accuracy.

### 6.2 AutoML Architecture and Model Tracking

The engine employs a multi-tiered modeling strategy managed through MLflow:

1. **AutoGluon Tabular:** For datasets exceeding 5,000 rows, AutoGluon constructs a multi-layer stacking ensemble combining LightGBM, CatBoost, XGBoost, and deep feed-forward neural networks. In published academic benchmarks on secondary education datasets, AutoGluon ensembles consistently achieve over 90% accuracy on letter-grade classification.
2. **TabPFN (Prior-Data Fitted Network):** For small, specialized classroom batches (such as elective subject cohorts under 1,000 records), the system utilizes TabPFN, a transformer-based tabular foundation model that provides high-accuracy zero-shot predictions without extensive parameter tuning.
3. **MLflow Tracking:** Every training run, hyperparameter configuration, feature list, and evaluation metric is logged to an MLflow registry to ensure reproducibility.

### 6.3 Explainability with SHAP Feature Attribution

In educational decision-making, black-box predictions are unacceptable. If an AI system flags a student as at risk of failing, teachers and counselors must understand why in order to design an effective academic intervention.

Every prediction served by EduQuery AI is accompanied by a SHAP summary:

* **Transparent Drivers:** The engine breaks down the prediction into positive and negative contributing factors (for example: `+8%` due to strong previous mathematics scores, `-14%` due to three consecutive absences during lab sessions, `-6%` due to low class average relative to the board benchmark).
* **Advisory Framing:** All prediction payloads include an explicit ethical disclaimer: predictions represent decision-support tools for educators and must never be used as automated judgments for disciplinary action, student placement, or teacher evaluation.

---

## 7. Security, Privacy, and Data Governance

Educational institutions handle sensitive minor demographic data and academic histories. EduQuery AI implements security controls at every layer of the system.

### 7.1 Local Data Sovereignty and External Kill-Switch

The system enforces a local-first operational boundary. Student records, examination marks, and identifiable demographic information remain inside the school network.

An environment configuration switch (`EXTERNAL_MODEL_ENABLED=false`) completely disables outbound network calls. All semantic parsing, SQL generation, policy search, and prediction tasks execute on local CPU/GPU resources. When external language model assistance is explicitly enabled for research benchmarks, the outbound payload is stripped of all student data, and zero-retention headers (`provider.zdr=true`) are enforced.

### 7.2 SQL AST Validation and Sanitization

The `validate_and_sanitize_sql` engine parses every generated T-SQL statement using `sqlglot` before database execution:

* **Enforcing Single SELECT Statements:** Blocks SQL injection techniques that attempt to chain multiple queries using semicolons (such as `; DROP TABLE ...`).
* **Rejecting Data Mutation:** Rejects statements containing `INSERT`, `UPDATE`, `DELETE`, `ALTER`, `CREATE`, `EXEC`, `GRANT`, `MERGE`, or `TRUNCATE`.
* **Allowlist Enforcement:** Ensures all referenced tables and views belong to the 68 approved analytical objects in `ALLOWLISTED_VIEWS`. Any query attempting to query system tables (such as `sys.tables` or `information_schema`) or credential tables is blocked.
* **Enforcing Result Limits:** Automatically injects a `TOP 1000` clause to prevent unconstrained queries from exhausting server memory.

### 7.3 Privacy Redaction and Audit Logging

Before prompts are processed, the `PrivacyRedactor` module applies regex patterns matching Pakistani CNIC formats (`XXXXX-XXXXXXX-X`), mobile phone numbers (`03XX-XXXXXXX`), email addresses, and roll numbers. These are substituted with neutral tokens, guaranteeing that raw personal data is never stored in query caches or transmitted to external endpoints.

Simultaneously, the `AuditLogger` records all API interactions in structured JSON format. Each entry contains a timestamp, user ID, client IP address, sanitized prompt, generated SQL, execution duration, and status code, providing an auditable trail for institutional compliance.

---

## 8. Empirical Evaluation and Benchmark Results

To validate EduQuery AI, the team conducted static, dynamic, and concurrent evaluations across the full suite of 610 gold prompts supplied by the Daanish School administration (`docs/07-evidence/wren-gold-610-2026-08-16/`).

### 8.1 The 610 Gold Prompt Evaluation

The evaluation dataset comprises 610 unique, sequential test prompts across 13 distinct academic families:

1. `STUDENTS_ROLL` (Board enrollment master)
2. `MARKS` (Board examination marks)
3. `PRAC` (Science practical results)
4. `TR2_THEORY` (Theory teacher results)
5. `TR2_PRAC` (Practical teacher results)
6. `TR_ALL` (Combined teacher performance)
7. `ALL_COMBINED` (Longitudinal teacher career records)
8. `HOF_FRMT` (Head office evaluation reports)
9. `INTERNAL_EXAM_GROUP_WISE_PERFORMANCE_VIEW` (Internal teacher results)
10. `STUDENT_RESULT_TOTAL` (Annual student board results)
11. `STUDENT_RESULT_TOTAL_INTERNAL` (Internal term result cards)
12. `VTEACHER_SUM_PER` (Middle school teacher performance)
13. `GOVERNED_REFUSALS` (Prompts requesting unmapped or contradictory domains)

### 8.2 Summary of Benchmark Results

| Evaluation Metric | Observed Result | Target / Standard | Status |
|---|---|---|---|
| **Input Integrity** | 610 / 610 prompts unique and sequential | 100% integrity | Passed |
| **Strict Wren MDL Compilation** | 515 / 515 executable single-object plans | 100% compilation | Passed |
| **Governed Refusals** | 95 / 95 safe refusals issued | 100% compliance | Passed |
| **Live Concurrent Sweep (4 Workers)** | 510 / 515 queries succeeded | ≥ 95% pass rate | Passed (99.0%) |
| **Individual Replay of Failed Cases** | 5 / 5 queries succeeded | 100% resolution | Passed |
| **Median Execution Latency (p50)** | 28.43 ms | < 500 ms | Exceptional |
| **95th Percentile Latency (p95)** | 1091.17 ms | < 3000 ms | Passed |
| **External Cloud Calls** | 0 external requests | Zero cloud leakage | Passed |
| **Automated Regression Suite** | 299 / 299 tests passing | 100% pass rate | Passed |
| **Policy RAG Retrieval (Recall@3)** | 9 / 9 benchmark questions correct | ≥ 80% recall | Passed (100%) |

### 8.3 Analysis of Governed Refusals

A critical sign of system maturity is the ability to refuse ungrounded queries safely. Of the 610 test prompts, exactly 95 were identified as governed refusals:
* **55 prompts** requested multi-table analytical joins (such as combining internal term marks with board pass percentages) where no verified business logic or primary-foreign key relationship exists in the institutional catalog. Rather than generating hallucinated joins, the engine returned a safe refusal explaining the missing metric definition.
* **40 prompts** requested student-level subject positions from views where the position column was either missing or mathematically inconsistent. The engine refused these queries to prevent misleading academic reporting.

---

## 9. Frontend User Experience and Portal Integration

The user interface of EduQuery AI is tailored specifically for non-technical educators, school principals, and administrative coordinators.

### 9.1 Portal Coexistence Strategy

During requirements discovery, Daanish School representatives highlighted that over 600 teachers currently use the existing portal. Introducing a completely separate portal would cause confusion and require extensive retraining.

EduQuery AI adopts a seamless coexistence strategy:
* **Admin-Only Portal Entry:** An "EduQuery AI" entry button is embedded directly into the navigation header of the existing portal for administrative users (principals, coordinators, and head office directors).
* **Familiar Aesthetics:** The UI uses clean typography (Inter/Geist), balanced spacing, and high-contrast color palettes (minimum 4.5:1 ratio for WCAG AA compliance). It supports both light and dark themes without relying on distracting animations.

### 9.2 Conversational Refinement and Data Visualization

* **Iterative Follow-Ups:** Users can refine their queries naturally. For example, after asking "Show Class 10 Mathematics results for Attock Boys," the user can simply type "Now show only the students who scored below 40%," and the system maintains context to apply the new filter.
* **Rich Visualizations:** Responses automatically render structured summary tables and dynamic charts (bar charts, line graphs, and distribution plots powered by Recharts) alongside clear natural language explanations.
* **Export Capability:** All analytical tables and charts can be exported with a single click to CSV or presentation-ready formats for executive meetings.

---

## 10. Production Blockers and Institutional Remediation

To maintain transparency and engineering rigor, the team has documented the remaining technical requirements necessary before transitioning EduQuery AI from a workstation-verified demo to a production institutional deployment (`docs/00-control/PROJECT_CONTROL.md`).

| # | Production Requirement | Current Status | Required Action / Remediation |
|---|---|---|---|
| 1 | **Domain Answer Truth** | School provided prompt text and categories, but no expected numerical results | School domain experts must review and sign off on expected result sets for the 515 compilable prompts |
| 2 | **Student Position Source** | `Position` column in student result views is inconsistent or missing | Database administrator must supply an authoritative student-level position view |
| 3 | **Cross-Table Metric Approvals** | 55 cross-table join metrics currently lack formal definitions | Academic committee must approve official formulas for cross-table performance KPIs |
| 4 | **Slow View Optimization** | 5 complex HOF views take 5 to 12 seconds to run due to unindexed aggregations | Database team must create indexed views or materialized summary tables on SQL Server |
| 5 | **Live Institutional DSN** | System currently runs on a verified local restore (`EduQuery_Wren_20260713`) | School IT must provision a secure, continuously updated DSN connection |
| 6 | **Dedicated Read-Only Identity** | Local environment uses Windows authentication | School IT must create a dedicated SQL user with strict `db_datareader` permissions |
| 7 | **Enterprise SSO Integration** | System currently validates local demo JWT tokens | Integrate with Daanish School's active directory or centralized OAuth2 provider |

---

## 11. Future Scope and Refinement Roadmap

EduQuery AI provides a scalable foundation for ongoing innovation in educational data intelligence. The project roadmap includes the following future enhancements:

1. **Phase 1 (Institutional Deployment):** Complete the connection to Daanish School's live production database cluster, enforce hardware-level SSL encryption, and link authentication to the school's central user directory.
2. **Phase 2 (Role-Based Semantic Scoping):** Expand the authorization engine so that individual teachers are automatically restricted to viewing only their assigned classes and subjects, while campus principals retain full campus visibility and head office directors maintain multi-campus access.
3. **Phase 3 (Alumni and Placement Intelligence):** Develop a standardized multi-school schema module to track where Daanish School graduates go after completing their second year (higher education scholarships, university enrollments, and career placements), fulfilling a primary government reporting objective.
4. **Phase 4 (Localized Urdu Language Support):** Implement a fine-tuned bilingual language parsing module allowing teachers and staff to submit queries and receive reports in Urdu, increasing system accessibility across all campus locations.
5. **Phase 5 (Proactive Early-Warning and Remedial Engine):** Build an automated background daemon that scans weekly attendance and test scores, generating proactive warning digests for academic coordinators before students fall behind.

---

## 12. Conclusion and Project Verification

EduQuery AI demonstrates how modern agentic AI, governed semantic modeling, and machine learning can be successfully applied to large-scale academic databases. By rejecting unconstrained guesswork in favor of a strictly governed semantic layer (Wren AI 0.13.2), verified local policy retrieval (LanceDB), and explainable predictive modeling (AutoGluon + TabPFN + SHAP), the platform delivers reliable, sub-second educational intelligence while maintaining complete student data privacy.

The system addresses the real-world operational bottlenecks of the Punjab Daanish Schools network, replacing multi-day manual reporting cycles with instant natural language exploration and providing educators with the foresight needed to support vulnerable students proactively.

This project was developed, tested, and verified under the rigorous academic standards of the AI Bootcamp 2026 offered by Skylabs in collaboration with GIKI Institute. All architectural designs, benchmark results, and security controls are fully documented and backed by reproducible code and audit evidence.

---

## 13. Team Attestation and Verification Sign-Off

We hereby certify that this capstone project report represents verified engineering work, authentic benchmark results, and sound architectural design completed by the EduQuery AI team.

**Project Lead:**  
Muhammad Junaid (Thejunaid1799@gmail.com)  

**Engineering Team:**  
Abdur Rafay (Abdurrafay222@gmail.com)  
Abeera Anwer (sobisobangoyes@gmail.com)  
Zain ul Abideen (Zainsardar062@gmail.com)  

**Course and Institution:**  
Bootcamp in Advanced AI 2026  
Skylabs in Collaboration with Ghulam Ishaq Khan Institute of Engineering Sciences and Technology (GIK Institute), Topi, Pakistan  
**Faculty Advisor / Evaluator:** Dr. Ali Imran  
**Date of Submission:** August 20, 2026  
