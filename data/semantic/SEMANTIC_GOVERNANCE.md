# EduQuery AI — Governed Semantic Assets Specification

> **Version:** 1.0.0  
> **Folder:** `data/semantic/`  
> **Human Owner / Acceptance Authority:** Muhammad Junaid  
> **Status:** Governed MVP input slice for WS-03/WS-04 interface boundary  

---

## 1. Scope & Source Provenance

All semantic assets in `data/semantic/` are strictly derived from the approved canonical documentation under `docs/06-schema/`:

- `master_schema.md` (SHA-256: `0C4283E76E02801B73E22789CCF87E9008234BD07AB55578B6E901A62FB77959`)
- `semantic_relationship_map.json` (SHA-256: `D7371B5D30EBB5A384B0130B03F1E3397A7B9BBE87BDBD3964753C65A0266815`)
- `semantic_model.json` (SHA-256: `1EC3662EC17100D9D512364C9135E21E866CA76C07FAFD0E2D45A6B03705E13B`)
- `canonical_column_reference.md` (SHA-256: `E4ED4B3DB5CB0015F41F6FEF3F3764AA593B31CB6B757A5F56BCEEC3B077272B`)

---

## 2. Approved 6-Table MVP Slice (`mvp_semantic_slice.json`)

The MVP semantic slice is strictly limited to 6 tables and 4 relationships:

1. **`MARKS`**: Board exam marks & percentages.
2. **`Marks_Internal`**: Internal exam marks & percentages.
3. **`STUDENTS_ROLL`**: Board student enrollment master.
4. **`STUDENTS_ROLL_INTERNAL_EXAM`**: Internal student enrollment master.
5. **`TEACHERS_PROFILE`**: Teacher subject & class teaching assignments.
6. **`STAFF_EMPLOYEE_CARD`**: Staff directory HR master.

### Approved Relationships
- `R02`: `STUDENTS_ROLL` -> `MARKS` (via `ROLLNO`, `SCHOOL`, `YEAR`)
- `R03`: `STUDENTS_ROLL_INTERNAL_EXAM` -> `Marks_Internal` (via `ROLLNO`, `SCHOOL`, `YEAR`, `EXAM`/`EXAMTYPE`)
- `R16`: `STAFF_EMPLOYEE_CARD` -> `TEACHERS_PROFILE` (via `EID`)
- `R14`: `TEACHERS_PROFILE` -> `MARKS` (via `SCHOOL`, `CLASS`, `SUBJECT`/`SUBJECTNAME`, `YEAR`)

---

## 3. Explicit Exclusion List (26 Tables)

The following 26 tables are explicitly excluded from the semantic model, NL2SQL prompt context, and ML feature training:

| # | Excluded Table | Reason |
|---|----------------|--------|
| 1 | `12_25` | Raw import snapshot |
| 2 | `4SCHL` | Ad-hoc student subset |
| 3 | `678_SUB` | Duplicate subject subset |
| 4 | `ctnb810` | Duplicate subject subset |
| 5 | `Ctttt` | Scratch data dump |
| 6 | `mar` | One-off analysis marks dump |
| 7 | `mmm` | Single-school roll dump |
| 8 | `rafia` | Single-school data dump |
| 9 | `MNKRA_UP` | One-school student data |
| 10 | `MNMARKS` | One-school marks data |
| 11 | `marks_with_school_name` | Legacy denormalized marks copy |
| 12 | `MISSED_RSLT_678` | One-time missing results |
| 13 | `PALCEMENT_ATKB` | One-school placement data |
| 14 | `TNS` | Legacy teacher snapshot |
| 15 | `TR` | Raw teacher results dump |
| 16 | `ALL` | Duplicate roll data |
| 17 | `ALLSTD26` | Year-specific student snapshot |
| 18 | `ExamMarksDeletionQueries` | Meta table storing DDL/DML queries |
| 19 | `STUDENTS_ROLL_BKP` | Backup table |
| 20 | `STUDENTS_ROLL_BKP_BEFORE_PROMOTION_27` | Pre-promotion backup |
| 21 | `TEAHCERS_BKP` | Backup table |
| 22 | `HOF_OLD` | Legacy Hall of Fame |
| 23 | `ALL_COMBINED_OLD` | Legacy combined marks |
| 24 | `Marksold` | Legacy marks data |
| 25 | `ALL_COMBINED_FINAL` | Unused legacy table |
| 26 | `SUBJECT_MARKS_EXAM_RUNTIME` | Unused staging table |

---

## 4. Privacy & Data Sovereignty Rules

1. **No Raw Row Exports**: `data/semantic/` contains schema structure, synonyms, metrics, and relationships only. No student marks, student names, or roll numbers are included in semantic input files.
2. **WS-04 MDL Freeze**: Validated semantic inputs are frozen for WS-04. Wren AI MDL configuration will be generated only when WS-04 implementation starts under Muhammad Junaid's direction.
