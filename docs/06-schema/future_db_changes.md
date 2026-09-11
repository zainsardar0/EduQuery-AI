# EduQuery AI — Future Database Changes

> These are optional database improvements that would enhance schema quality but are NOT required for the current project phase. They are deferred and will only be implemented if the school management approves them.

**Status:** Listed for future consideration — NO action taken.

---

## Priority 1: High Impact, Low Risk

### 1.1 Add a `Schools` Master Dimension Table

**Problem:** School is a repeated free-text string (`nvarchar` varying from 10 to 255 chars) across every table. No school IDs, addresses, regions, or metadata exist.

**Proposed Change:**
```sql
CREATE TABLE dbo.Schools (
    SchoolID    INT IDENTITY(1,1) PRIMARY KEY,
    SchoolCode  VARCHAR(10) NOT NULL UNIQUE, -- e.g., 'ATKB', 'MNWB'
    SchoolName  NVARCHAR(200) NOT NULL,       -- Full name
    Gender      CHAR(1) NOT NULL,             -- 'B' or 'G'
    City        NVARCHAR(100) NULL,
    Region      NVARCHAR(100) NULL,
    IsActive    BIT NOT NULL DEFAULT 1,
    CreatedAt   DATETIME NOT NULL DEFAULT GETDATE()
);
```

**Benefit:** Enables proper school dimension for analytics, eliminates string matching, supports school metadata in NLP queries.

**Risk:** Low — additive only, no existing tables modified.

---

### 1.2 Fix the `CATEGROY` Typo

**Affected tables:** `STUDENTS_ROLL`, `TR_ALL`, `TR`

**Proposed Change:**
```sql
-- STUDENTS_ROLL
EXEC sp_rename 'dbo.STUDENTS_ROLL.CATEGROY', 'CATEGORY', 'COLUMN';
-- TR_ALL
EXEC sp_rename 'dbo.TR_ALL.CATEGROY', 'CATEGORY', 'COLUMN';
-- TR
EXEC sp_rename 'dbo.TR.CATEGROY', 'CATEGORY', 'COLUMN';
```

**Risk:** Medium — any application code or views referencing `CATEGROY` will break. Requires audit of all views and stored procedures first.

---

### 1.3 Fix the `TEAHCERS` Table Name Typo

**Proposed Change:**
```sql
EXEC sp_rename 'dbo.TEAHCERS', 'TEACHERS';
EXEC sp_rename 'dbo.TEAHCERS_BKP', 'TEACHERS_BKP';
```

**Risk:** Medium — same as above. Application code and views referencing old name will break.

---

### 1.4 Fix the `SUBJECT_GORUP_YEAR_MARKS_26` Table Name Typo

**Proposed Change:**
```sql
EXEC sp_rename 'dbo.SUBJECT_GORUP_YEAR_MARKS_26', 'SUBJECT_GROUP_YEAR_MARKS_26';
```

**Risk:** Low-Medium — check for references first.

---

## Priority 2: Medium Impact

### 2.0 Repair Gold-Prompt Reporting Views

- Correct `STUDENTS_RESULT_TOTAL_INTERNAL` so `STRING_AGG` uses an `nvarchar(max)` input and cannot exceed the 8,000-byte limit.
- Optimize or materialize broad scans over `HOF_FRMT` and `INTERNAL_EXAM_GROUP_WISE_PERFORMANCE_VIEW`; current restore timings reach roughly 5–12 seconds and fail under concurrent load.
- Provide or correct the student-level subject-position source. The live `School_Ind_Pos_SUB` view contains school aggregates only and cannot support merit-list prompts.

These changes require school database-owner approval and a replay of the 610-prompt concurrency benchmark.

### 2.1 Add Foreign Key Constraints

**Problem:** No FK constraints exist in the entire database. Data integrity relies entirely on application logic.

**Proposed changes (examples):**
```sql
-- Link teacher marks entries to teacher profiles
ALTER TABLE dbo.SUBJECT_MARKS_EXAM_RUNTIME
ADD CONSTRAINT FK_SMER_Teacher
FOREIGN KEY (EID) REFERENCES dbo.TEACHERS_PROFILE(EID);

-- Link student answers to questions
ALTER TABLE dbo.StudentAnswers
ADD CONSTRAINT FK_SA_Question
FOREIGN KEY (QuestionID) REFERENCES dbo.Questions(QuestionID);

-- Link quiz questions to quiz subjects
ALTER TABLE dbo.Questions
ADD CONSTRAINT FK_Q_Subject
FOREIGN KEY (SubjectID) REFERENCES dbo.Subjects_Quiz(SubjectID);
```

**Benefit:** Improves data integrity; enables the NLP model to auto-discover join paths.

**Risk:** High — existing data may violate FK constraints. Requires data cleanup before constraint creation.

---

### 2.2 Standardize `CLASS` Data Type

**Problem:** `CLASS` is `varchar(20)` in some tables, `int` in others, `float` in imported tables, `tinyint` in ALLSCHOOLS26, `smallint` in SUBJECT_GROUP_YEAR_MARKS.

**Proposed standard:** `INT NOT NULL` (or `TINYINT` for storage efficiency since classes are 1-12).

**Risk:** High — requires data migration and view/procedure updates.

---

### 2.3 Standardize `EID` Data Type

**Problem:** `EID` is `int` in production tables, `float` in legacy imported tables.

**Proposed standard:** `INT NOT NULL`.

**Risk:** Medium — only affects legacy tables.

---

### 2.4 Standardize `YEAR` Data Type

**Problem:** `YEAR` is `int` in production tables, `float` in legacy tables, `tinyint` in ALLSCHOOLS26, `smallint` in some config tables, `varchar(2)` in SUBJECT_GORUP_YEAR_MARKS_26.

**Proposed standard:** `SMALLINT NOT NULL` (academic year 22-30 fits in smallint).

**Risk:** Medium — requires view updates.

---

## Priority 3: Nice-to-Have

### 3.1 Add an `AcademicYears` Dimension Table

```sql
CREATE TABLE dbo.AcademicYears (
    YearCode    SMALLINT PRIMARY KEY, -- 22, 23, 24, 25, 26
    YearLabel   VARCHAR(10) NOT NULL, -- '2022', '2023' etc.
    StartDate   DATE NULL,
    EndDate     DATE NULL,
    IsCurrent   BIT NOT NULL DEFAULT 0
);
```

### 3.2 Add Student Demographics

Currently no DOB, gender, or contact information is part of the approved semantic scope. An ad-hoc import contains some of this data, but it must remain outside all training-bound artifacts.

### 3.3 Consolidate Exam Schedule Tables

Merge `Exam_Schedule` and `Exam_Schedule_26` into a single table, using YEAR to distinguish.

### 3.4 Clean Up Scratch Tables

Drop the ~27 scratch/temp tables after confirming no active application references.

### 3.5 Add Audit Tables for EduQuery AI

New tables for the AI system:
```sql
CREATE TABLE dbo.EduQuery_QueryAuditLog (
    LogID           INT IDENTITY(1,1) PRIMARY KEY,
    UserEID         INT NOT NULL,
    UserRole        NVARCHAR(50) NOT NULL,
    UserSchool      NVARCHAR(150) NOT NULL,
    NaturalLanguage NVARCHAR(MAX) NOT NULL,
    GeneratedSQL    NVARCHAR(MAX) NOT NULL,
    WasExecuted     BIT NOT NULL DEFAULT 0,
    WasBlocked      BIT NOT NULL DEFAULT 0,
    BlockReason     NVARCHAR(500) NULL,
    ExecutionTimeMs INT NULL,
    RowsReturned    INT NULL,
    CreatedAt       DATETIME NOT NULL DEFAULT GETDATE()
);

CREATE TABLE dbo.EduQuery_PredictionAuditLog (
    LogID           INT IDENTITY(1,1) PRIMARY KEY,
    UserEID         INT NOT NULL,
    PredictionType  NVARCHAR(100) NOT NULL,
    InputFeatures   NVARCHAR(MAX) NULL,
    PredictionResult NVARCHAR(MAX) NULL,
    ConfidenceScore FLOAT NULL,
    ModelVersion    NVARCHAR(50) NULL,
    CreatedAt       DATETIME NOT NULL DEFAULT GETDATE()
);
```

---

## Decision Log

| # | Change | Decision | Decided By | Date |
|---|--------|----------|------------|------|
| 1 | All changes in this file | Deferred to future | User (Muhammad Junaid) | 2026-08-02 |
