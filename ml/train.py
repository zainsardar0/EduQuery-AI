"""
EduQuery AI — Master Training Orchestrator
============================================
Runs the full pipeline: ETL → Student Model → Teacher Model → Branch Model.
All experiments tracked via MLflow.
"""

import os
import sys
import time
import warnings
from pathlib import Path

import numpy as np
import pandas as pd

warnings.filterwarnings("ignore", category=FutureWarning)
warnings.filterwarnings("ignore", category=UserWarning)

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from ml.etl_pipeline import run_etl, FEATURES_DIR
from ml.mlflow_config import setup_mlflow, REPORTS_DIR
from ml.models.student_model import StudentModel
from ml.models.teacher_model import TeacherModel
from ml.models.branch_model import BranchModel


def main():
    t0 = time.time()

    print("\n" + "█" * 70)
    print("  EduQuery AI — National Prediction Engine")
    print("  3-Tier ML Pipeline: Student → Teacher → Branch")
    print("█" * 70 + "\n")

    # ── Step 0: Setup MLflow ──
    setup_mlflow()

    # ── Step 1: Run ETL Pipeline ──
    print("\n" + "─" * 70)
    print("  STEP 1: ETL Pipeline")
    print("─" * 70)

    student_path = FEATURES_DIR / "student_features.parquet"
    teacher_path = FEATURES_DIR / "teacher_features.parquet"
    branch_path = FEATURES_DIR / "branch_features.parquet"

    if student_path.exists() and teacher_path.exists() and branch_path.exists():
        print("  ✅ Parquet feature files found. Skipping ETL to save time.")
        student_df = pd.read_parquet(student_path)
        teacher_df = pd.read_parquet(teacher_path)
        branch_df = pd.read_parquet(branch_path)
    else:
        # Always re-run ETL to get fresh features
        student_df, teacher_df, branch_df = run_etl()

    # ── Step 2: Train Student Model ──
    print("\n" + "─" * 70)
    print("  STEP 2: Student Annual Marks Prediction Model")
    print("─" * 70)

    student_model = StudentModel(output_dir=str(REPORTS_DIR / "student"))
    student_metrics = student_model.train(student_df)

    print(f"\n  📊 Student Model Results:")
    print(f"     MAE:  {student_metrics.get('mae', 'N/A')}")
    print(f"     RMSE: {student_metrics.get('rmse', 'N/A')}")
    print(f"     R²:   {student_metrics.get('r2', 'N/A')}")
    print(f"     Within ±8%: {student_metrics.get('pct_within_8', 'N/A')}")

    # ── Step 3: Train Teacher Model ──
    print("\n" + "─" * 70)
    print("  STEP 3: Teacher Credibility Score Model")
    print("─" * 70)

    teacher_model = TeacherModel(output_dir=str(REPORTS_DIR / "teacher"))
    teacher_metrics = teacher_model.train(teacher_df)

    print(f"\n  📊 Teacher Model Results:")
    print(f"     MAE:      {teacher_metrics.get('mae', 'N/A')}")
    print(f"     RMSE:     {teacher_metrics.get('rmse', 'N/A')}")
    print(f"     R²:       {teacher_metrics.get('r2', 'N/A')}")
    print(f"     Spearman: {teacher_metrics.get('spearman_rho', 'N/A')}")

    # ── Step 4: Train Branch Model ──
    print("\n" + "─" * 70)
    print("  STEP 4: Branch Reputation Score Model")
    print("─" * 70)

    branch_model = BranchModel(output_dir=str(REPORTS_DIR / "branch"))
    branch_metrics = branch_model.train(branch_df)

    print(f"\n  📊 Branch Model Results:")
    print(f"     MAE:      {branch_metrics.get('mae', 'N/A')}")
    print(f"     RMSE:     {branch_metrics.get('rmse', 'N/A')}")
    print(f"     R²:       {branch_metrics.get('r2', 'N/A')}")
    print(f"     Spearman: {branch_metrics.get('spearman_rho', 'N/A')}")

    # ── Step 5: Generate Analysis Report ──
    print("\n" + "─" * 70)
    print("  STEP 5: Generating Analysis Report")
    print("─" * 70)

    generate_analysis_report(student_df, teacher_df, branch_df,
                             student_metrics, teacher_metrics, branch_metrics,
                             student_model, teacher_model, branch_model)

    elapsed = time.time() - t0
    print("\n" + "█" * 70)
    print(f"  PIPELINE COMPLETE — Total time: {elapsed:.1f}s ({elapsed/60:.1f} min)")
    print("█" * 70)


def generate_analysis_report(student_df, teacher_df, branch_df,
                              student_metrics, teacher_metrics, branch_metrics,
                              student_model, teacher_model, branch_model):
    """Generate comprehensive analysis report."""
    import json

    report_path = REPORTS_DIR / "analysis_report.md"

    # Per-school student performance
    school_analysis = ""
    if hasattr(student_model, "per_school_mae") and student_model.per_school_mae:
        school_analysis = "\n### Per-Campus Student Model MAE\n\n| Campus | MAE (%) | Interpretation |\n|---|---|---|\n"
        for school, mae in sorted(student_model.per_school_mae.items(), key=lambda x: x[1]):
            quality = "🟢 Excellent" if mae < 3.5 else "🟡 Good" if mae < 5 else "🟠 Fair" if mae < 7 else "🔴 Needs Attention"
            school_analysis += f"| {school} | {mae:.2f} | {quality} |\n"

    # Teacher ranking
    teacher_ranking = ""
    if "EID" in teacher_df.columns and "teacher_credibility_score" in teacher_df.columns:
        top_teachers = teacher_df.groupby(["EID", "NAME", "school"]).agg(
            avg_score=("teacher_credibility_score", "mean"),
            records=("teacher_credibility_score", "count"),
        ).reset_index().sort_values("avg_score", ascending=False).head(20)

        teacher_ranking = "\n### Top 20 Teachers by Credibility Score\n\n| Rank | Name | School | Avg Score | Records |\n|---|---|---|---|---|\n"
        for i, (_, row) in enumerate(top_teachers.iterrows(), 1):
            name = row.get("NAME", "N/A")
            if isinstance(name, str) and len(name) > 25:
                name = name[:22] + "..."
            teacher_ranking += f"| {i} | {name} | {row['school']} | {row['avg_score']:.1f} | {row['records']} |\n"

    # Branch ranking
    branch_ranking = ""
    if "school" in branch_df.columns and "branch_reputation_score" in branch_df.columns:
        latest_year = branch_df["year"].max()
        latest = branch_df[branch_df["year"] == latest_year].sort_values(
            "branch_reputation_score", ascending=False
        )
        branch_ranking = f"\n### Branch Ranking (Year {int(latest_year)})\n\n"
        branch_ranking += "| Rank | Campus | Reputation Score | Mean % | Pass Rate | Teacher Avg |\n|---|---|---|---|---|---|\n"
        for i, (_, row) in enumerate(latest.iterrows(), 1):
            branch_ranking += (
                f"| {i} | {row['school']} | {row['branch_reputation_score']:.1f} | "
                f"{row.get('branch_mean_pct', 0):.1f}% | "
                f"{row.get('branch_pass_rate', 0)*100:.1f}% | "
                f"{row.get('branch_teacher_avg_class_avg', 0):.1f} |\n"
            )

    # Data quality summary
    dq_summary = f"""
### Data Quality Summary

| Metric | Value |
|---|---|
| Student feature rows | {len(student_df):,} |
| Teacher feature rows | {len(teacher_df):,} |
| Branch feature rows | {len(branch_df):,} |
| Unique students | {student_df['ROLLNO'].nunique() if 'ROLLNO' in student_df.columns else 'N/A':,} |
| Unique teachers | {teacher_df['EID'].nunique() if 'EID' in teacher_df.columns else 'N/A'} |
| Unique branches | {branch_df['school'].nunique() if 'school' in branch_df.columns else 'N/A'} |
| Student null cols | {student_df.isnull().any().sum()} |
| Target (student) range | {student_df['pct_annual'].min():.1f}% – {student_df['pct_annual'].max():.1f}% |
"""

    report = f"""# EduQuery AI — Analysis Report

Generated: {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M')}

---

## Model Performance Summary

| Model | MAE | RMSE | R² | Additional |
|---|---|---|---|---|
| **Student Marks** | {student_metrics.get('mae', 'N/A')} | {student_metrics.get('rmse', 'N/A')} | {student_metrics.get('r2', 'N/A')} | Within ±8%: {student_metrics.get('pct_within_8', 'N/A')} |
| **Teacher Credibility** | {teacher_metrics.get('mae', 'N/A')} | {teacher_metrics.get('rmse', 'N/A')} | {teacher_metrics.get('r2', 'N/A')} | Spearman ρ: {teacher_metrics.get('spearman_rho', 'N/A')} |
| **Branch Reputation** | {branch_metrics.get('mae', 'N/A')} | {branch_metrics.get('rmse', 'N/A')} | {branch_metrics.get('r2', 'N/A')} | Spearman ρ: {branch_metrics.get('spearman_rho', 'N/A')} |

---

{dq_summary}

---

{school_analysis}

---

{teacher_ranking}

---

{branch_ranking}

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
"""

    report_path.write_text(report, encoding="utf-8")
    print(f"  📝 Report saved: {report_path}")

    # Save metrics as JSON
    metrics_path = REPORTS_DIR / "metrics.json"
    all_metrics = {
        "student": {k: float(v) if isinstance(v, (int, float, np.floating)) else str(v)
                     for k, v in student_metrics.items()},
        "teacher": {k: float(v) if isinstance(v, (int, float, np.floating)) else str(v)
                     for k, v in teacher_metrics.items()},
        "branch": {k: float(v) if isinstance(v, (int, float, np.floating)) else str(v)
                    for k, v in branch_metrics.items()},
    }
    metrics_path.write_text(json.dumps(all_metrics, indent=2), encoding="utf-8")
    print(f"  📝 Metrics saved: {metrics_path}")


if __name__ == "__main__":
    main()
