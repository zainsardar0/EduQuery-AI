# Daanish School — Current System, Client Needs, and Product Expectations

> **Status:** Approved Canonical Requirements Document
> **Purpose:** Convert the meeting transcript into a connected account of how the school works today, what problems it is trying to solve, what it expects from EduQuery AI, and how those expectations relate to the existing project proposal and current architecture.  
> **Authority boundary:** This document forms the basis for MVP scope updates reflecting Daanish School's requirements.

## 1. Evidence and interpretation boundary

This document uses four evidence layers:

1. **Meeting-confirmed:** clearly supported by the recording transcript.
2. **School-stated, not independently verified:** stated by the school-side speaker, but still needs portal, database, document, or management verification.
3. **Existing project baseline:** already present in the proposal, workforce plan, architecture, or governed schema documents; it was not necessarily requested or approved by the school in this meeting.
4. **Open or unclear:** the audio, authority, data, or implementation decision is insufficient for a firm conclusion.

Primary sources:

- [Timestamped Urdu/English ASR transcript](openrouter-transcription/TRANSCRIPTION.md)
- [Flow-corrected English translation](openrouter-transcription/TRANSCRIPT_ENGLISH.md)
- [Machine-readable transcript segments](openrouter-transcription/transcription-segments.json)
- [Original EduQuery AI proposal](../../docs/01-proposal/EduQuery_AI_Proposal.md)
- [Current workforce and MVP plan](../../docs/05-planning/WORKFORCE_PLAN.md)
- [Current architecture baseline](../../docs/05-planning/codebase/ARCHITECTURE.md)
- [Governed schema scope](../../docs/06-schema/master_schema.md)
- [Deferred database improvements](../../docs/06-schema/future_db_changes.md)

The supplied attendee roster is Muhammad Junaid, Abdur Rafay, Abeera, Ali Imran, and Awais, Representative of Daanish School. The transcript does not reliably identify every voice, so requirements are attributed only to the **school side** or **project side**, not to named individuals.

## 2. Executive conclusion

Daanish School already has a hosted, multi-school result portal. The school is **not asking for that portal to be replaced**. Its present system can retrieve predefined result views through dropdowns, show data in a grid, and export a PDF. Its weakness is that every new or unusual question still requires a person to understand the request, construct or adjust a database query, extract the result, add requested fields, and prepare a report, graph, or presentation.

The client wants EduQuery AI to become an **intelligence layer inside the existing user-account flow**. The meeting defines two primary client needs:

1. **Natural-language academic and result analytics:** a user writes the question they actually want answered; the system returns the relevant result and supports refinement of that question.
2. **Policy search and guidance:** a user describes an issue; the system finds the relevant official policy, explains whether and how it applies, and supports handling the matter according to that policy.

The strongest product interpretation is therefore:

> **EduQuery AI should extend Daanish School's existing portal with a secure, account-aware AI assistant that answers governed questions over academic data and official policy documents, produces useful analytical outputs, and reduces the manual work currently required for custom reports.**

The original proposal's NL2SQL, semantic layer, charts, read-only controls, auditability, and multi-campus security directly support this client need. The proposal's prediction engine remains a project and academic commitment, but **prediction was not presented by the school as one of its two main needs in this meeting**. Conversely, policy search was a core meeting requirement but is not presently treated as a first-class must-ship capability in the locked MVP plan. That scope difference requires an explicit project decision.

## 3. Why the school needs the system

### 3.1 Institutional operating context

Daanish School is described as a boarding system in which students remain under the institution's care twenty-four hours a day. The school therefore considers itself responsible for both good and poor student outcomes. The government funds students and expects the institution to explain what happened during and after the students' time in the system.

This creates continuous accountability from school leadership and head office. They ask for changing combinations of evidence, including:

- performance of students from a particular area;
- English performance;
- performance for a division such as Mianwali;
- a school's own performance;
- comparisons with other schools;
- weak students and failures;
- graphs and result presentations;
- teacher and school performance;
- where students went after second year, including university and employment outcomes.

Evidence: `00:00:36.800–00:01:50.280`, `00:14:02.440–00:15:37.860`.

### 3.2 The actual business problem

The database exists, but the present interface only handles combinations anticipated in advance. New questions become a manual reporting exercise:

1. receive the question from head office, a principal, or another stakeholder;
2. identify the required data and filters;
3. write or adjust a database query;
4. retrieve the result;
5. add or change columns when the requester revises the question;
6. prepare the answer, report, graph, or presentation;
7. repeat the process for the next variation.

The client wants to reduce this repeated dependency on technical query preparation without losing control over which school's data a user may access.

Evidence: `00:00:51.600–00:02:05.580`.

## 4. How the school works today

### 4.1 Existing portal and user experience

The current school system is already hosted and used across schools. Each school has an account, and users have their own login/profile. The current portal is primarily based on predefined pages and dropdown combinations.

For student results, users can search using combinations such as:

- student name;
- roll number;
- class;
- subject;
- school;
- percentage.

The portal runs the corresponding SQL retrieval, shows the result in a grid, and allows a PDF download. Similar pages or views exist for teachers and schools.

Evidence: `00:03:32.000–00:05:13.000`.

### 4.2 Current access model

The existing system does not appear to use a formally defined role model. Instead, separate pages were created for different user types. A teacher who logs in is redirected to the teacher page based on the username and password. Administration, examination coordinators, and principals see different pages.

The school-side speaker estimated that approximately 600 teachers currently use the system. Replacing the familiar flow with a substantially different access structure would require significant explanation and retraining. The school therefore treated a visible role-system redesign as optional: do it now if it fits the available time and workload; otherwise retain it for a later update.

This does **not** remove the security need for server-side authorization. It means the new product should preserve the familiar account flow while enforcing permissions behind it.

Evidence: `00:12:30.000–00:13:46.000`.

### 4.3 Result data and how it enters the system

The school-side speaker described the result coverage as follows:

- overall stated coverage: 2017 through 2026;
- 2017–2021: class 9 through second year;
- later years: class 6 through second year;
- classes 6, 7, and 8: internal examinations entered by teachers through their pages;
- higher classes: board results obtained from board sources/websites.

This is **school-stated, not fully verified against the shared database copy**. The project side reported that the shared file appeared to show data from 2022 onward. The school-side speaker said the earlier board data exists and may have been fetched on another machine or omitted because an older file was shared. They agreed to check and resend it.

Evidence: `00:00:00.000–00:00:36.800`, `00:05:24.000–00:06:23.700`.

### 4.4 Syllabus-completion workflow

The portal also contains a more recent syllabus-completion feature. A separate question-paper-generation system already stores class-wise subjects and topics. It was connected to the portal so that teachers can tick the topics taught in class and the relevant principal can see syllabus completion on their screen. The 2026-specific syllabus or marks tables discussed in the meeting support this feature.

This workflow is useful context for EduQuery AI because it shows that the existing portal already integrates separate functions and that principals expect school-level monitoring views.

Evidence: `00:06:23.700–00:07:36.160`.

### 4.5 Policy handling today

The school has multiple official policies, including areas described in the meeting as:

- induction;
- promotion;
- passing out;
- rustication or disciplinary handling;
- admissions;
- class/marks requirements;
- admission criteria;
- quota or marks rules for circumstances such as a deceased parent.

These policies are stored in separate PDF files. Staff currently have difficulty finding the correct policy for a particular issue. The PDFs had not yet been supplied to the project team at the time of the meeting.

Evidence: `00:02:05.580–00:03:30.000`.

### 4.6 Placement and outcome reporting today

The school needs to report where students go after completing second year, including university and employment outcomes. The school-side speaker said there is no current web portal for this function; information is handled through reports.

The governed project schema currently excludes a one-school table named `PALCEMENT_ATKB`. That table is not a sufficient or approved basis for a network-wide placement feature. A governed multi-school data source and ownership process are still required.

Evidence: `00:15:15.160–00:15:43.300`; project anchor: `master_schema.md` excluded-table list.

### 4.7 Current technology and database condition

The meeting supports the following limited conclusions:

- the portal is used on Windows;
- the hosting appears related to ASP.NET or SmartASP.NET, but the exact phrase is unclear;
- the meeting does not provide a reliable SQL Server version answer.

Separately, the current governed schema records SQL Server 2022, compatibility level 160, as verified on 2 August 2026. That is project evidence, not a clear statement from this recording.

The project side raised spelling errors, missing or problematic foreign keys, redundancy, latency, and performance. The school-side speaker agreed that cleanup could be done and expected reduced duplication to improve portal performance. Existing project analysis has already documented examples such as `CATEGROY`, `TEAHCERS`, `SUBJECT_GORUP_YEAR_MARKS_26`, inconsistent data types, absent foreign-key constraints, and scratch/duplicate tables.

However, canonical project governance currently treats database changes as deferred and the AI data path as read-only. The meeting agreement should therefore be treated as support for a controlled cleanup proposal, not permission to modify the live database immediately.

Evidence: `00:07:36.160–00:09:28.000`; project anchors: `future_db_changes.md`, `master_schema.md`, and `ARCHITECTURE.md`.

## 5. How the client wants EduQuery AI to work

### 5.1 Target product position

The AI functionality should be available inside the existing product/account experience. A user should go to the account they already use and find the AI capability there. The meeting does not support launching an unrelated replacement portal or forcing all users through a new operational workflow.

Evidence: `00:13:46.000–00:14:02.440`.

The exact technical integration is still open. It could require changes inside the existing ASP.NET application, a securely linked module, or another account-sharing method. No choice should be made until the current portal source, authentication flow, and deployment access are inspected.

### 5.2 Target academic-query workflow

The intended experience is:

1. the user signs in through the existing account flow;
2. the user writes a natural-language question instead of building a dropdown combination;
3. the system interprets school, class, subject, year, exam, student, teacher, area, comparison, and output intent;
4. the system enforces the user's authorized school and role scope;
5. the system queries only the approved academic data surface;
6. the system returns a clear answer, table, graph, or other required analytical output;
7. the user can refine the prompt to improve or change the result;
8. the request and response are handled safely and audibly enough for institutional review.

Steps 1, 2, 6, and 7 are directly supported by the meeting. Steps 3, 4, 5, and 8 are necessary implementation safeguards from the proposal and current architecture.

### 5.3 Target policy workflow

The intended policy experience is:

1. the user describes an issue in natural language;
2. the system searches only approved Daanish School policy documents;
3. it identifies the relevant policy or policies;
4. it shows the supporting policy section;
5. it explains whether the policy appears applicable and how the matter can be handled under that policy;
6. it clearly distinguishes quoted policy evidence from generated explanation;
7. it leaves the final administrative or disciplinary decision with the authorized human officer.

Steps 1, 3, and 5 are directly stated in the meeting. Steps 2, 4, 6, and 7 are required safeguards so the assistant does not invent policy or become an unauthorized decision-maker.

### 5.4 Expected analytical outputs

The meeting identifies frequent demand for:

- direct answers to custom questions;
- result tables;
- graphs;
- result presentations;
- weak-student lists;
- failure and failure-rate analysis;
- subject performance;
- area and division analysis;
- individual-school analysis;
- cross-school comparisons;
- teacher-performance evidence;
- board-performance comparisons;
- post-second-year placement and outcome information.

The existing proposal already anticipates natural-language answers, tabular output, charts, school comparisons, teacher analytics, board benchmarks, trends, and at-risk-student analysis. Presentation-file generation itself was not defined precisely in either source and needs confirmation: the client may mean presentation-ready charts/data rather than automatic PowerPoint generation.

## 6. Client requirement register

| ID | Requirement or need | Evidence status | Meeting evidence | Project alignment | Decision state |
|---|---|---|---|---|---|
| DS-01 | Users can ask academic/result questions in natural language. | Meeting-confirmed | `00:01:50–00:02:10` | Core proposal NL2SQL objective | Required |
| DS-02 | Users can refine prompts and receive an improved or adjusted result. | Meeting-confirmed | `00:01:55–00:02:05` | Fits conversational query UX | Required |
| DS-03 | The system supports school-specific and cross-school analysis. | Meeting-confirmed | `00:01:24–00:01:50` | Proposal prompt families C and D | Required |
| DS-04 | The query surface supports students, classes, subjects, schools, percentages, years, exams, and relevant result filters. | Meeting-confirmed plus existing portal evidence | `00:04:10–00:04:38` | Matches governed semantic domains | Required; exact vocabulary to validate |
| DS-05 | Outputs support clear answers, tables, graphs, and result-presentation needs. | Meeting-confirmed need | `00:14:02–00:14:13` | Proposal answer composer and charts | Required; exact presentation format open |
| DS-06 | Users can identify weak students, failures, and areas of performance deficiency. | Meeting-confirmed | `00:14:08–00:14:56` | Proposal diagnostics and at-risk analysis | Required |
| DS-07 | The system supports teacher-performance and accountability analysis using approved definitions. | Meeting-confirmed context | `00:14:13–00:14:56` | Proposal teacher analytics | Required, but policy thresholds need formal definitions |
| DS-08 | The system supports geographic and organizational questions such as area/division and school comparisons. | Meeting-confirmed | `00:00:51–00:01:12` | Proposal cross-school analytics | Required |
| DS-09 | The AI capability appears in the existing portal/account flow. | Meeting-confirmed | `00:13:46–00:14:02` | Potential conflict with standalone Vercel UI assumption | Required; integration method open |
| DS-10 | Existing users should not face unnecessary retraining or disruption. | Meeting-confirmed operational constraint | `00:13:11–00:13:46` | Supports incremental integration | Required UX constraint |
| DS-11 | The system searches official policy PDFs from an issue description. | Meeting-confirmed | `00:02:05–00:02:57` | New first-class client requirement | Required; source PDFs missing |
| DS-12 | Policy answers identify the relevant rule and explain how it applies. | Meeting-confirmed | `00:02:35–00:02:57` | Requires governed, citation-backed RAG | Required |
| DS-13 | Access remains scoped to the correct user/school even if the visible pages remain familiar. | Existing portal context plus project safeguard | `00:04:38–00:05:13`, `00:12:30–00:13:46` | Canonical RBAC/campus-security requirement | Required security control |
| DS-14 | Result querying uses the existing live institutional database through a safe integration. | Meeting-confirmed direction | `00:03:32–00:03:52` | Canonical read-only architecture | Required; connection approval open |
| DS-15 | Historical result coverage should include the complete school-approved period. | School-stated, not verified | `00:00:00–00:00:36`, `00:05:30–00:06:23` | Multi-year trends need it | Blocked on complete data |
| DS-16 | Internal results for classes 6–8 and board-result sources are interpreted correctly. | School-stated | `00:00:21–00:00:36` | Requires semantic definitions and source provenance | Required data rule; validate |
| DS-17 | Syllabus-completion data and its relationship to existing tools are understood before using those tables. | Meeting-confirmed current workflow | `00:06:23–00:07:36` | Relevant to schema grounding | Required analysis input, not necessarily MVP feature |
| DS-18 | Database defects and redundancy are assessed and a controlled remediation plan is produced. | Meeting-supported | `00:07:36–00:08:29` | Conflicts with current no-write/read-only boundary if treated as direct implementation | Proposed separate workstream; approval required |
| DS-19 | Visible role redesign may be implemented now only if it does not derail the AI focus; otherwise defer it. | Meeting-confirmed | `00:12:30–00:13:46` | UX-role overhaul optional; backend authorization remains mandatory | Optional UI change |
| DS-20 | Placement/outcome information after second year should become queryable or better managed. | Meeting-confirmed business need | `00:15:15–00:15:37` | Current approved schema lacks a sufficient governed source | Open scope and data dependency |
| DS-21 | The school supplies a list of common or “gold” prompts for validation. | Meeting-confirmed commitment | `00:15:43–00:16:19` | Current project requires at least 200 validated prompts | School list pending |
| DS-22 | The school tests the delivered solution and reports whether it meets its needs. | Meeting-confirmed collaboration goal | `00:11:07–00:11:29` | Fits human acceptance authority | Required acceptance step |
| DS-23 | Portal access and examples of teacher/admin/principal views are provided to the team. | Meeting-confirmed commitment | `00:04:38–00:05:13` | Needed for integration and access mapping | Pending input |
| DS-24 | Policy PDFs are provided to the team. | Meeting-confirmed commitment | `00:03:00–00:03:30` | Required for policy assistant | Pending input |

## 7. Relationship to the existing EduQuery AI proposal

### 7.1 What the meeting confirms

The meeting strongly validates the proposal's central problem and several design choices:

- non-technical users need natural-language access to academic data;
- fixed reports and manual SQL work are too slow for changing questions;
- multi-school and school-specific analytics are both required;
- users need answers, tables, and charts rather than raw SQL;
- the live SQL Server database remains the institutional data source;
- the system needs a governed semantic layer because school, class, subject, exam, teacher, board, and year terms must map consistently;
- existing accounts and school scope matter;
- gold prompts and school-side validation are essential.

### 7.2 What the meeting adds or elevates

The meeting adds or elevates requirements that the present locked MVP does not fully reflect:

1. **Policy search is one of the client's two main requested capabilities.** The current MVP plan limits local RAG mainly to schema, metrics, MDL, and verified examples, while richer policy administration is placed after the demo. At minimum, a citation-backed policy-search slice should be considered for the client MVP once the PDFs arrive.
2. **The AI must fit the existing portal/account flow.** The current architecture assumes a Vercel-hosted Next.js interface. That may still be usable, but the user experience and authentication must feel integrated with the existing school product. The exact integration method is unresolved.
3. **Placement/outcome reporting is a real institutional need.** It is not currently supported by a governed multi-school source.
4. **Database cleanup is desired.** It needs separate authority, migration analysis, backups, application dependency checks, and rollback—not direct changes through the AI project.
5. **The current page-based user model and approximately 600 teachers make change management a product constraint.**

### 7.3 What remains proposal-driven rather than client-confirmed

The following are important current project commitments or engineering choices, but the school did not specifically request or approve them in this meeting:

- future-result prediction;
- AutoGluon, TabPFN, MLflow, and SHAP;
- Wren AI as the selected semantic/NL2SQL product;
- FastAPI and Next.js as the implementation stack;
- Vercel as the browser-interface host;
- GPT 5.6 Luna Pro/OpenRouter as the external model route;
- at least 200 gold prompts;
- exact success targets such as response time and accuracy percentages;
- the precise RLS, JWT, audit, and deployment design.

These remain valid project requirements where already approved. They must not be described as requirements personally stated by the Daanish School representative during this meeting.

### 7.4 Prediction needs explicit positioning

Prediction is central to the submitted proposal and current August 20 plan, but it was not one of the two needs defined by the school-side speaker. The project should therefore present it accurately:

- **Client-defined immediate value:** faster result analytics and policy search.
- **Proposal-defined additional value:** predictive risk and future-result forecasting with explainability.

Prediction should remain advisory. It must not automatically affect grades, teacher contracts, disciplinary action, admission, or placement decisions.

## 8. Recommended product boundary after this meeting

This is the evidence-supported target, subject to Muhammad Junaid's approval:

### Core client layer

- natural-language result and academic analytics;
- school-aware and account-aware access;
- answers, tables, charts, and export-ready outputs;
- common diagnostic questions for weak students, failures, subjects, teachers, schools, divisions, and comparisons;
- follow-up/refinement of questions;
- citation-backed search over approved Daanish School policies;
- integration with the existing account experience;
- evaluation against school-supplied gold prompts.

### Existing proposal layer

- governed semantic model;
- safe read-only SQL generation and validation;
- auditability and campus isolation;
- English-only MVP under the current approved plan;
- prediction and SHAP as an additional proposal deliverable, not a substitute for the two client-defined needs.

### Separate or conditional work

- live database cleanup and schema migration;
- full role-system redesign;
- placement/outcome portal and data collection;
- automatic PowerPoint generation;
- multilingual/Urdu product support;
- commercial or payment arrangements;
- formal collaboration letter/certificate terms.

## 9. Inputs the school still needs to provide

| Input | Why it is needed | Meeting evidence | Current state |
|---|---|---|---|
| Official policy PDFs | Build and validate the policy assistant | `00:03:00–00:03:30` | Received; processing into Headroom Vector DB |
| Existing portal access/sign-in | Inspect actual workflow and integration points | `00:04:38–00:05:02` | Received; access granted |
| Teacher-page example | Map teacher capabilities and scope | `00:05:02–00:05:07` | Received |
| Admin/exam-coordinator/principal examples | Map page-level access and user journeys | `00:05:07–00:05:13` | Received |
| Complete 2017–2021 result data or proof of location | Validate stated historical coverage | `00:05:30–00:06:23` | Missing from the copy discussed in the meeting |
| School's common/gold prompt list | Define acceptance questions and expected outputs | `00:15:43–00:16:19` | Promised |
| Exact portal hosting and authentication details | Choose a safe integration method | `00:08:30–00:09:28` | Partly unclear |
| Official school/management approval for database changes | Separate authorized cleanup from read-only AI access | `00:07:36–00:08:29` | Representative support heard; formal authority unverified |
| Placement/outcome data source and ownership process | Make post-second-year outcomes reliable and maintainable | `00:15:15–00:15:37` | No current web portal; governed source unresolved |
| Formal metric definitions | Prevent ambiguous calculations for failure, weakness, performance, and teacher accountability | `00:14:02–00:15:15` | Context supplied; authoritative thresholds not supplied |

## 10. Acceptance model implied by the discussion

The meeting describes the school as a validator of the solution. A defensible acceptance process would be:

1. the school supplies its common questions and expected interpretations;
2. the team converts them into replayable gold prompts without changing their business meaning;
3. the school confirms the expected filters, calculations, and result sets;
4. the system is tested against those questions using authorized data;
5. policy questions are tested only after the official PDFs are supplied;
6. every policy answer shows its supporting source section;
7. school/account access boundaries are tested for allowed and denied cases;
8. the school records whether the solution meets its needs;
9. unresolved or incorrect cases remain visible rather than being counted as successful.

The current project target of at least 200 prompts can be built by expanding the school's seed list, but the school or its delegated domain reviewers must own the correctness of expected answers.

## 11. Collaboration and non-functional outcomes discussed

The meeting also discussed collaboration between Daanish School, the students/team, and GIKI. The source suggests that:

- Daanish School would test and validate the delivered solution;
- an official acknowledgement, appreciation letter, or certificate could help the team demonstrate its work;
- the collaboration could be presented as work done with or for a government-linked institution;
- group communication would be used for follow-up questions and coordination.

Evidence: `00:10:00–00:12:22`, `00:16:24–00:16:40`.

The audio is too unclear to establish the exact issuer, wording, approval process, financial arrangement, or legal status of any certificate/letter. None of those should be treated as agreed until confirmed in writing.

## 12. Unresolved points that must not be guessed

| Topic | What is known | What remains unresolved |
|---|---|---|
| Speaker identity | Attendee roster is known | Which named person said each line |
| Historical data | School says 2017–2026 exists | Exact tables/files and completeness for 2017–2021 |
| Hosting | Windows and an ASP.NET-related host are mentioned | Exact host, application framework, topology, and access |
| Role design | Current system uses separate pages; visible redesign is optional | Current authorization rules, account claims, and future role model |
| Policy corpus | Policies exist as PDFs | Files, versions, approval status, effective dates, and access rules |
| Database cleanup | Representative agreed cleanup can be done | Formal change authority, downtime, dependencies, rollback, and scope |
| Placement | Government asks for outcomes; no portal exists | Data source, fields, update owner, privacy, and whether it is in the MVP |
| Presentations | Result presentations are frequently requested | Whether the product must generate PowerPoint files or only presentation-ready charts/data |
| Teacher salary | A range sounding like 170–180 is mentioned | Currency, unit, and exact statement |
| Teacher contract consequence | Strict performance consequences are described | Exact threshold, policy, and consequence |
| Government cost per child | A figure sounding like 50 lakh over seven years is mentioned | Exact amount, accounting basis, and whether it is a reportable metric |
| Formal recognition | Letter/certificate and collaboration are discussed | Exact commitment, issuer, wording, and timing |
| Financial arrangement | The source appears to defer financial discussion | Exact meaning and any commercial terms |
| Final closing remark | Board/class-result work is mentioned | Exact event and timing |

The salary, contract, and per-child-cost statements are contextual explanations of accountability. They must not be encoded as system rules or reported as verified institutional policy until the official policy/metric source is supplied.

## 13. Complete meeting traceability

| Recording time | Discussion | Reliable conclusion |
|---|---|---|
| `00:00:00–00:00:36` | Result years, classes, internal and board sources | Claimed 2017–2026 coverage; classes 6–8 internal; higher classes board-based |
| `00:00:36–00:02:05` | Boarding responsibility, government/head-office questions, manual query work | Ad-hoc reporting is slow and repetitive; natural-language querying is the first need |
| `00:02:05–00:02:59` | School policies and issue handling | Policy search/guidance is the second need |
| `00:03:00–00:03:32` | Missing policy material | School will send separate policy PDFs |
| `00:03:32–00:05:24` | Existing hosted portal | Accounts, dropdowns, grid, PDF, and page examples; portal access promised |
| `00:05:24–00:06:23` | Historical-data mismatch | Shared copy may omit 2017–2021; school says data exists and will check/send |
| `00:06:23–00:07:36` | 2026 syllabus/marks tables | Connected syllabus-completion and question-paper-generation workflow |
| `00:07:36–00:08:29` | Spelling, foreign keys, redundancy, performance | School supports cleanup; controlled authority and migration scope still required |
| `00:08:30–00:09:28` | SQL/OS/hosting | Windows confirmed; ASP.NET-related host phrase unclear; exact stack incomplete |
| `00:09:30–00:09:59` | Garbled management/role discussion | No firm requirement can be extracted safely |
| `00:10:00–00:11:59` | Collaboration, validation, recognition | School validation and possible official acknowledgement discussed; exact terms unclear |
| `00:12:00–00:12:30` | Group coordination | Follow-up through a shared group; Rafay invited to ask questions |
| `00:12:30–00:13:46` | Current access and future roles | Separate pages, not formal roles; about 600 teachers; role redesign optional if costly |
| `00:13:46–00:14:02` | Product integration | AI should appear inside the existing product/account flow |
| `00:14:02–00:15:43` | Common analytics and accountability | Graphs, presentations, weak students, failures, deficiencies, and placement/outcomes are important |
| `00:15:43–00:16:24` | Gold prompts | School agrees to provide a fuller list of common questions |
| `00:16:24–00:16:44` | Closing | Continue questions in the group; final timing remark is unclear |

## 14. Updated goal for validation

> Build EduQuery AI as a secure, English-first intelligence layer within Daanish School's existing account experience. It should allow authorized staff to ask natural-language questions over governed academic/result data, refine those questions, and receive accurate answers, tables, charts, and diagnostic outputs. It should also search approved school policy PDFs, cite the relevant provisions, and explain their applicability without replacing human authority. The system must preserve school/account boundaries, avoid unsafe database writes, and be validated against questions and expected answers supplied or approved by Daanish School. Predictive analytics remains an additional proposal deliverable, while database cleanup, role redesign, placement tracking, and formal collaboration terms require separate scope or approval.

## 15. Decisions Made (August 12, 2026)

Muhammad Junaid and the project team have resolved the following:

1. **Policy Search MVP:** The policy-search capability IS included in the August MVP. The official policy PDFs have been received and are being processed into the Headroom vector database.
2. **Frontend Integration:** The integration with the existing Daanish School portal will be handled via a redirect button on the main existing portal to the Eduquery AI page. Initially, this feature is restricted to users who already have admin access to all data (e.g., school principals, admins, higher-level faculty).
3. **Prediction Engine:** The prediction engine (AutoGluon/TabPFN/SHAP) remains firmly implemented in the MVP alongside the Policy Search RAG.
4. **Wren AI:** The semantic layer and NL2SQL pipeline will utilize Wren AI as planned.
