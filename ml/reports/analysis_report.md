# EduQuery AI — Analysis Report

Generated: 2026-08-15 17:39

---

## Model Performance Summary

| Model | MAE | RMSE | R² | Additional |
|---|---|---|---|---|
| **Student Marks** | 6.334816936992567 | 9.851057295691293 | 0.5480207960101763 | Within ±8%: 74.31559315260108 |
| **Teacher Credibility** | 1.039119275452518 | 1.3487936984588222 | 0.989607974704494 | Spearman ρ: 0.9861317796491758 |
| **Branch Reputation** | 3.479227968171836 | 4.864593226096064 | 0.510950124905436 | Spearman ρ: 0.48631608608361815 |

---


### Data Quality Summary

| Metric | Value |
|---|---|
| Student feature rows | 105,091 |
| Teacher feature rows | 62,169 |
| Branch feature rows | 88 |
| Unique students | 6,292 |
| Unique teachers | 767 |
| Unique branches | 21 |
| Student null cols | 19 |
| Target (student) range | 0.0% – 100.0% |


---


### Per-Campus Student Model MAE

| Campus | MAE (%) | Interpretation |
|---|---|---|
| HSPB | 4.82 | 🟡 Good |
| MNWG | 5.06 | 🟠 Fair |
| DGKG | 5.34 | 🟠 Fair |
| RYKG | 5.40 | 🟠 Fair |
| VEHG | 5.46 | 🟠 Fair |
| RYKB | 5.66 | 🟠 Fair |
| RJNG | 5.89 | 🟠 Fair |
| CTNG | 6.25 | 🟠 Fair |
| HSPG | 6.26 | 🟠 Fair |
| DGKB | 6.27 | 🟠 Fair |
| ATKG | 6.75 | 🟠 Fair |
| CTNB | 6.86 | 🟠 Fair |
| RJNB | 6.90 | 🟠 Fair |
| TNSB | 7.13 | 🔴 Needs Attention |
| MNKB | 7.23 | 🔴 Needs Attention |
| VEHB | 7.24 | 🔴 Needs Attention |
| ATKB | 7.56 | 🔴 Needs Attention |
| MNWB | 7.85 | 🔴 Needs Attention |
| MNKG | 7.85 | 🔴 Needs Attention |
| TNSG | 8.63 | 🔴 Needs Attention |
| UNKNOWN | 29.14 | 🔴 Needs Attention |


---


### Top 20 Teachers by Credibility Score

| Rank | Name | School | Avg Score | Records |
|---|---|---|---|---|
| 1 | ABDUL SAMAD | DGKB | 98.7 | 4 |
| 2 | KHADIJA-TUL- KUBRA | HSPG | 98.4 | 2 |
| 3 | Affifa noureen | MNWG | 98.4 | 4 |
| 4 | TASLEEM FATIMA | MNWG | 98.4 | 6 |
| 5 | HAFIZ MUNIR AHMAD | HSPB | 98.2 | 4 |
| 6 | AZEEM KHALID | HSPB | 97.9 | 12 |
| 7 | FARHAT FIRDOUS | CTNG | 97.4 | 2 |
| 8 | BILAL ATTA MUHAMMAD SA... | HSPB | 97.4 | 36 |
| 9 | Mr Abdul Rauf | RYKB | 97.3 | 4 |
| 10 | MAFIA PARVEEN | VEHG | 97.3 | 10 |
| 11 | SADIA ASGHAR | CTNG | 97.3 | 409 |
| 12 | Mr Imran Hayder | RYKB | 97.2 | 74 |
| 13 | Mr Fayyaz Mehmood Bukhari | RYKB | 97.1 | 16 |
| 14 | ABDUL REHMAN | HSPB | 96.8 | 117 |
| 15 | Mr Daanish Ali | RYKB | 96.7 | 3 |
| 16 | FIRDOS PARVEEN | VEHG | 96.3 | 25 |
| 17 | MR MUHAMMAD ABU BAKAR | RYKB | 96.3 | 88 |
| 18 | FIRDOUS | VEHG | 96.3 | 255 |
| 19 | Mr Adnan Altaf | RYKB | 96.1 | 32 |
| 20 | FIRDOUS PARVEEN | VEHG | 96.0 | 133 |


---


### Branch Ranking (Year 26)

| Rank | Campus | Reputation Score | Mean % | Pass Rate | Teacher Avg |
|---|---|---|---|---|---|
| 1 | HSPB | 86.8 | 92.0% | 100.0% | 94.6 |
| 2 | MNWG | 85.5 | 90.4% | 99.8% | 92.1 |
| 3 | DGKG | 85.2 | 89.2% | 100.0% | 90.8 |
| 4 | RYKB | 84.3 | 88.2% | 100.0% | 89.5 |
| 5 | HSPG | 83.9 | 87.7% | 100.0% | 89.0 |
| 6 | VEHB | 83.2 | 85.7% | 99.8% | 87.4 |
| 7 | CTNG | 83.1 | 87.6% | 98.9% | 88.9 |
| 8 | RYKG | 83.0 | 87.0% | 99.7% | 87.6 |
| 9 | VEHG | 82.0 | 85.2% | 99.5% | 86.1 |
| 10 | RJNB | 81.1 | 84.4% | 99.7% | 85.8 |
| 11 | CTNB | 80.7 | 83.9% | 99.0% | 85.2 |
| 12 | DGKB | 80.5 | 83.0% | 99.5% | 83.8 |
| 13 | MNWB | 80.1 | 82.4% | 99.6% | 81.7 |
| 14 | ATKG | 80.0 | 83.2% | 99.2% | 83.5 |
| 15 | RJNG | 79.8 | 82.9% | 99.4% | 83.8 |
| 16 | TNSB | 79.6 | 82.1% | 98.8% | 82.5 |
| 17 | MNKB | 78.5 | 81.1% | 99.7% | 81.1 |
| 18 | ATKB | 77.5 | 79.8% | 99.6% | 81.7 |
| 19 | MNKG | 76.4 | 79.4% | 99.4% | 79.4 |
| 20 | TNSG | 70.2 | 72.6% | 95.2% | 72.7 |


---

## Feature Engineering Notes

- **32 student features** from 8 source tables (Marks_Internal, STUDENTS_ROLL_INTERNAL_EXAM, TR_ALL, HOF, BOARD_PER, PRAC, House_Attendance_Daily, TEACHERS_INTERNAL_EXAM)
- **25 teacher features** from 4 source tables (TR, HOF, HOF_OLD, BOARD_PER)
- **30 branch features** from 7 source tables (MARKS, STUDENTS_ROLL, TR, HOF, HOF_OLD, BOARD_PER, GZT_STRENGTH)
- All subject names canonicalized to 14 standard subjects
- All school codes cleaned and standardized to 20 campuses
- Score percentages recalculated and capped to [0, 100]
- Missing mock scores imputed with group medians + indicator flags
- Teacher performance linked via composite key: SCHOOL + CLASS + SECTION + SUBJECT
