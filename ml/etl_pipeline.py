"""
EduQuery AI — ETL Pipeline
===========================
Extracts, cleans, and engineers features from the SQLite database
into 3 Parquet feature stores: student, teacher, branch.

Ground truth: all data comes from sqldaanish.sqlite (69 tables).
"""

import os
import sqlite3
import warnings
from pathlib import Path
from typing import Optional

import numpy as np
import pandas as pd

warnings.filterwarnings("ignore", category=FutureWarning)

# ──────────────────────────────────────────────────────────────
# Constants
# ──────────────────────────────────────────────────────────────
PROJECT_ROOT = Path(__file__).resolve().parent.parent
DB_PATH = PROJECT_ROOT / "data" / "extracted_db" / "sqldaanish.sqlite"
FEATURES_DIR = PROJECT_ROOT / "ml" / "features"

STEM_SUBJECTS = {"MATHEMATICS", "PHYSICS", "CHEMISTRY", "BIOLOGY", "COMPUTER SCIENCE", "GENERAL SCIENCE"}
LANGUAGE_SUBJECTS = {"ENGLISH", "URDU"}
HUMANITIES_SUBJECTS = {"ISLAMIYAT", "ISLAMIC EDUCATION", "TRANSLATION OF THE HOLY QURAN",
                       "PAKISTAN STUDIES", "SOCIAL STUDIES", "ARTS"}

# Subject canonical mapping — handles casing and trailing-space variants
SUBJECT_MAP = {
    "Biology": "BIOLOGY", "Chemistry": "CHEMISTRY", "Physics": "PHYSICS",
    "Urdu": "URDU", "Social Studies": "SOCIAL STUDIES",
    "GENERAL SCIENCE ": "GENERAL SCIENCE", "SOCIAL STUDIES ": "SOCIAL STUDIES",
    "TRANSLATION OF THE HOLY Quran": "TRANSLATION OF THE HOLY QURAN",
    "TRANSLATION OF THE HOLY QURAN ": "TRANSLATION OF THE HOLY QURAN",
    "CHEMISTRY ": "CHEMISTRY", "URDU  ": "URDU",
    "Islamic Education": "ISLAMIC EDUCATION", "Islamiyat": "ISLAMIYAT",
    "TRANSLATION OF THE HOLLY QURAN": "TRANSLATION OF THE HOLY QURAN",
    "TRANSALTION OF THE HOLY QURAN": "TRANSLATION OF THE HOLY QURAN",
    "Tarjma Tul Quran": "TRANSLATION OF THE HOLY QURAN",
    "AL QURAN": "TRANSLATION OF THE HOLY QURAN",
    "IST": "ISLAMIYAT", "ISLAMIC STUDIES": "ISLAMIYAT",
    "MATH": "MATHEMATICS", "COMPUTER": "COMPUTER SCIENCE",
    "G.SCIENCE": "GENERAL SCIENCE", "ENG": "ENGLISH",
    "History and Geography": "SOCIAL STUDIES",
    "FINE ARTS": "ARTS",
}

SCHOOL_STRIP = {"RJNB ": "RJNB", "MNKG ": "MNKG", "atkb": "ATKB", "CNTG": "CTNG"}

CAMPUS_CITY = {
    "ATKB": "ATK", "ATKG": "ATK", "CTNB": "CTN", "CTNG": "CTN",
    "DGKB": "DGK", "DGKG": "DGK", "HSPB": "HSP", "HSPG": "HSP",
    "MNWB": "MNW", "MNWG": "MNW", "RJNB": "RJN", "RJNG": "RJN",
    "RYKB": "RYK", "RYKG": "RYK", "VEHB": "VEH", "VEHG": "VEH",
    "TNSB": "TNS", "TNSG": "TNS", "MNKB": "MNK", "MNKG": "MNK",
}


def _conn() -> sqlite3.Connection:
    """Open a read-only connection to the database."""
    return sqlite3.connect(f"file:{DB_PATH}?mode=ro", uri=True)


def _clean_str_col(s: pd.Series) -> pd.Series:
    """Strip whitespace and uppercase a string column."""
    return s.astype(str).str.strip().str.upper().replace({"NAN": np.nan, "NONE": np.nan, "": np.nan, "\\X00": np.nan})


def _clean_subject(s: pd.Series) -> pd.Series:
    """Canonicalize subject names."""
    out = s.copy()
    for raw, canon in SUBJECT_MAP.items():
        out = out.replace(raw, canon)
    out = out.str.strip().str.upper()
    out = out.replace({"": np.nan, "NAN": np.nan})
    return out


def _clean_school(s: pd.Series) -> pd.Series:
    """Canonicalize school codes."""
    out = s.str.strip()
    for raw, canon in SCHOOL_STRIP.items():
        out = out.replace(raw, canon)
    return out.str.upper()


def _clean_section(s: pd.Series) -> pd.Series:
    """Canonicalize section names."""
    return s.str.strip().str.upper().replace({"": np.nan, "\\X00": np.nan, "NAN": np.nan})


def _clean_status(s: pd.Series) -> pd.Series:
    """Map all status variants → binary PASS/FAIL."""
    mapping = {
        "PASS": "PASS", "Pass": "PASS", "PASS*": "PASS",
        "FAIL": "FAIL", "Fail": "FAIL",
        "LESS THAN 40%": "FAIL", "LESS THAN 33%": "FAIL",
        "LESS THAN 33% MARKS": "FAIL", "Less than 33%": "FAIL",
        "Missing": np.nan, "PNDG": np.nan, "": np.nan, "\\X00": np.nan,
    }
    return s.map(mapping)


# ──────────────────────────────────────────────────────────────
# Step 1: Load & Clean Core Tables
# ──────────────────────────────────────────────────────────────

def load_marks_internal() -> pd.DataFrame:
    """Load Marks_Internal — formative + annual exams, Year 26–27."""
    print("  [ETL] Loading Marks_Internal ...")
    with _conn() as conn:
        df = pd.read_sql("SELECT * FROM Marks_Internal", conn)

    df.columns = [c.strip() for c in df.columns]

    # Drop pending and class-test placeholder rows
    df = df[~df["STATUS"].isin(["PNDG", "\\x00"])].copy()
    df = df[df["EXAMTYPE"] != "CLASSTEST_1"].copy()

    # Clean columns
    df["SUBJECT"] = _clean_subject(df["SUBJECT"])
    df["EXAMTYPE"] = df["EXAMTYPE"].str.strip().str.upper()

    # Recalculate percentage and cap
    df["TOTAL"] = pd.to_numeric(df["TOTAL"], errors="coerce")
    df["OBTAINED"] = pd.to_numeric(df["OBTAINED"], errors="coerce")
    df["clean_pct"] = (df["OBTAINED"] / df["TOTAL"] * 100.0).clip(0.0, 100.0)
    df["is_zero_score"] = (df["clean_pct"] == 0.0).astype(int)

    df["CLASS"] = pd.to_numeric(df["CLASS"], errors="coerce")
    df["YEAR"] = pd.to_numeric(df["YEAR"], errors="coerce")
    df["ROLLNO"] = df["ROLLNO"].astype(str).str.strip()

    # Filter to Year 26 (primary training year)
    df = df[df["YEAR"] == 26].copy()
    df = df.dropna(subset=["SUBJECT", "ROLLNO", "CLASS"])

    print(f"    → {len(df):,} rows after cleaning (Year 26)")
    return df


def load_marks() -> pd.DataFrame:
    """Load MARKS — annual board results, Years 22–26."""
    print("  [ETL] Loading MARKS ...")
    with _conn() as conn:
        df = pd.read_sql("SELECT * FROM MARKS", conn)

    # Drop ghost rows
    df["YEAR"] = pd.to_numeric(df["YEAR"], errors="coerce")
    df = df.dropna(subset=["YEAR"]).copy()

    df["SUBJECT"] = _clean_subject(df["SUBJECT"])
    df["STATUS"] = _clean_status(df["STATUS"])
    df["OBTAINED"] = pd.to_numeric(df["OBTAINED"], errors="coerce")
    df["TOTAL"] = pd.to_numeric(df["TOTAL"], errors="coerce")
    df["clean_pct"] = (df["OBTAINED"] / df["TOTAL"] * 100.0).clip(0.0, 100.0)
    df["CLASS"] = pd.to_numeric(df["CLASS"], errors="coerce")
    df["ROLLNO"] = df["ROLLNO"].astype(str).str.strip().str.replace(r"\.0$", "", regex=True)

    # Deduplicate: keep latest ID per (ROLLNO, SUBJECT, YEAR)
    df = df.sort_values("ID", ascending=False).drop_duplicates(
        subset=["ROLLNO", "SUBJECT", "YEAR"], keep="first"
    )

    df = df.dropna(subset=["SUBJECT", "ROLLNO", "CLASS"])
    print(f"    → {len(df):,} rows after cleaning")
    return df


def load_students_roll_internal() -> pd.DataFrame:
    """Load STUDENTS_ROLL_INTERNAL_EXAM — student demographics for Year 26."""
    print("  [ETL] Loading STUDENTS_ROLL_INTERNAL_EXAM ...")
    with _conn() as conn:
        df = pd.read_sql("SELECT * FROM STUDENTS_ROLL_INTERNAL_EXAM", conn)

    df["YEAR"] = pd.to_numeric(df["YEAR"], errors="coerce")
    df = df[df["YEAR"] == 26].copy()

    df["SCHOOL"] = _clean_school(df["SCHOOL"].astype(str))
    df["SECTION"] = _clean_section(df["SECTION"].astype(str))
    df["CATEGORY"] = df["CATEGORY"].astype(str).str.strip().str.upper().replace(
        {"\\X00": np.nan, "S ": "S", "NAN": np.nan}
    )
    df["ROLLNO"] = df["ROLLNO"].astype(str).str.strip()
    df["SMSNO"] = df["SMSNO"].astype(str).str.strip()
    df["CLASS"] = df["CLASS"].astype(str).str.strip()
    df["HOUSE"] = df["HOUSE"].astype(str).str.strip().str.upper().replace({"\\X00": np.nan, "NAN": np.nan})
    df["GROUP"] = df["GROUP"].astype(str).str.strip().str.upper().replace({"\\X00": np.nan, "NAN": np.nan})

    # Deduplicate: one row per ROLLNO (take first by EXAM=MID_DEC if possible)
    df = df.sort_values("EXAM").drop_duplicates(subset=["ROLLNO"], keep="first")

    print(f"    → {len(df):,} students loaded")
    return df[["ROLLNO", "SCHOOL", "SECTION", "CATEGORY", "CLASS", "GROUP", "HOUSE", "SMSNO"]]


def load_students_roll() -> pd.DataFrame:
    """Load STUDENTS_ROLL — full roster with SMSNO bridging, all years."""
    print("  [ETL] Loading STUDENTS_ROLL ...")
    with _conn() as conn:
        df = pd.read_sql("SELECT * FROM STUDENTS_ROLL", conn)

    df["SCHOOL"] = _clean_school(df["SCHOOL"].astype(str))
    df["SECTION"] = _clean_section(df["SECTION"].astype(str))
    df["YEAR"] = pd.to_numeric(df["YEAR"], errors="coerce")
    df["CLASS"] = pd.to_numeric(df["CLASS"], errors="coerce")
    df["ROLLNO"] = df["ROLLNO"].astype(str).str.strip().str.replace(r"\.0$", "", regex=True)
    df["SMSNO"] = df["SMSNO"].astype(str).str.strip()
    df["CATEGROY"] = df["CATEGROY"].astype(str).str.strip().str.upper().replace(
        {"\\X00": np.nan, "S ": "S"}
    )

    print(f"    → {len(df):,} rows loaded")
    return df


def load_tr() -> pd.DataFrame:
    """Load TR — teacher result records with performance metrics."""
    print("  [ETL] Loading TR ...")
    with _conn() as conn:
        df = pd.read_sql("SELECT * FROM TR", conn)

    df["SCHOOL"] = _clean_school(df["SCHOOL"].astype(str))
    df["SUBJECT"] = _clean_subject(df["SUBJECT"])
    df["SECTION"] = _clean_section(df["SECTION"].astype(str))
    df["Year"] = pd.to_numeric(df["Year"], errors="coerce")
    df["CLASS"] = pd.to_numeric(df["CLASS"], errors="coerce")
    df["EID"] = pd.to_numeric(df["EID"], errors="coerce")

    for col in ["STRENGTH", "Count_90_100", "Count_80_90", "Count_70_80",
                "Count_60_70", "Count_50_60", "Count_40_50", "Count_0_39",
                "APPEARED", "PASSED"]:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    df["PASS%"] = pd.to_numeric(df["PASS%"], errors="coerce")
    df["CLASS AVG"] = pd.to_numeric(df["CLASS AVG"], errors="coerce")

    df = df.dropna(subset=["SUBJECT", "SCHOOL", "Year", "CLASS", "EID"])
    print(f"    → {len(df):,} rows loaded")
    return df


def load_tr_all() -> pd.DataFrame:
    """Load TR_ALL — aggregated teacher results (ANNUAL, ALL category)."""
    print("  [ETL] Loading TR_ALL ...")
    with _conn() as conn:
        df = pd.read_sql("SELECT * FROM TR_ALL", conn)

    df["SCHOOL"] = _clean_school(df["SCHOOL"].astype(str))
    df["SUBJECT"] = _clean_subject(df["SUBJECT"])
    df["SECTION"] = _clean_section(df["SECTION"].astype(str))
    df["Year"] = pd.to_numeric(df["Year"], errors="coerce")
    df["CLASS"] = pd.to_numeric(df["CLASS"], errors="coerce")
    df["EID"] = pd.to_numeric(df["EID"], errors="coerce")
    df["PASS%"] = pd.to_numeric(df["PASS%"], errors="coerce")
    df["CLASS AVG"] = pd.to_numeric(df["CLASS AVG"], errors="coerce")

    for col in ["STRENGTH", "Count_90_100", "Count_80_90", "Count_70_80",
                "Count_60_70", "Count_50_60", "Count_40_50", "Count_0_39",
                "APPEARED", "PASSED"]:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    df = df.dropna(subset=["SUBJECT", "SCHOOL", "Year", "CLASS", "EID"])
    print(f"    → {len(df):,} rows loaded")
    return df


def load_hof() -> pd.DataFrame:
    """Load HOF — teacher Hall of Fame with position rankings."""
    print("  [ETL] Loading HOF ...")
    with _conn() as conn:
        df = pd.read_sql("SELECT * FROM HOF", conn)

    df["SCHOOL"] = _clean_school(df["SCHOOL"].astype(str))
    df["SUBJECT"] = _clean_subject(df["SUBJECT"])
    df["Year"] = pd.to_numeric(df["Year"], errors="coerce")
    df["EID"] = pd.to_numeric(df["EID"], errors="coerce")
    df["Position"] = pd.to_numeric(df["Position"], errors="coerce")
    df["TOTAL_POSITIONS"] = pd.to_numeric(df["TOTAL_POSITIONS"], errors="coerce")
    df["WORK LOAD"] = pd.to_numeric(df["WORK LOAD"], errors="coerce")
    df["CLASS AVG"] = pd.to_numeric(df["CLASS AVG"], errors="coerce")
    df["PASS%"] = pd.to_numeric(df["PASS%"], errors="coerce")
    df["APPEARED"] = pd.to_numeric(df["APPEARED"], errors="coerce")
    df["PASSED"] = pd.to_numeric(df["PASSED"], errors="coerce")

    # Extract CLASS and SECTION from "CLASS/SECTION" column (e.g., "8/A")
    if "CLASS/SECTION" in df.columns:
        split = df["CLASS/SECTION"].astype(str).str.strip().str.split("/", n=1, expand=True)
        df["CLASS"] = pd.to_numeric(split[0], errors="coerce")
        df["SECTION"] = _clean_section(split[1]) if split.shape[1] > 1 else np.nan

    df = df.dropna(subset=["SUBJECT", "SCHOOL", "Year", "EID"])
    print(f"    → {len(df):,} rows loaded")
    return df


def load_hof_old() -> pd.DataFrame:
    """Load HOF_OLD — older hall of fame data."""
    print("  [ETL] Loading HOF_OLD ...")
    with _conn() as conn:
        df = pd.read_sql("SELECT * FROM HOF_OLD", conn)

    df["SCHOOL"] = _clean_school(df["SCHOOL"].astype(str))
    df["SUBJECT"] = _clean_subject(df["SUBJECT"])
    df["Year"] = pd.to_numeric(df["Year"], errors="coerce")
    df["EID"] = pd.to_numeric(df["EID"], errors="coerce")
    df["Position"] = pd.to_numeric(df["Position"], errors="coerce")
    df["TOTAL_POSITIONS"] = pd.to_numeric(df["TOTAL_POSITIONS"], errors="coerce")
    df["WORK LOAD"] = pd.to_numeric(df["WORK LOAD"], errors="coerce")
    df["CLASS AVG"] = pd.to_numeric(df["CLASS AVG"], errors="coerce")
    df["PASS%"] = pd.to_numeric(df["PASS%"], errors="coerce")
    df["APPEARED"] = pd.to_numeric(df["APPEARED"], errors="coerce")
    df["PASSED"] = pd.to_numeric(df["PASSED"], errors="coerce")

    if "CLASS/SECTION" in df.columns:
        split = df["CLASS/SECTION"].astype(str).str.strip().str.split("/", n=1, expand=True)
        df["CLASS"] = pd.to_numeric(split[0], errors="coerce")
        df["SECTION"] = _clean_section(split[1]) if split.shape[1] > 1 else np.nan

    df = df.dropna(subset=["SUBJECT", "SCHOOL", "Year", "EID"])
    print(f"    → {len(df):,} rows loaded")
    return df


def load_teachers_internal() -> pd.DataFrame:
    """Load TEACHERS_INTERNAL_EXAM — teacher→class/section/subject/exam mapping."""
    print("  [ETL] Loading TEACHERS_INTERNAL_EXAM ...")
    with _conn() as conn:
        df = pd.read_sql("SELECT * FROM TEACHERS_INTERNAL_EXAM", conn)

    df["SCHOOL"] = _clean_school(df["SCHOOL"].astype(str))
    df["SUBJECT"] = _clean_subject(df["SUBJECT"])
    df["SECTION"] = _clean_section(df["SECTION"].astype(str))
    df["CLASS"] = pd.to_numeric(df["CLASS"], errors="coerce")
    df["YEAR"] = pd.to_numeric(df["YEAR"], errors="coerce")
    df["EID"] = pd.to_numeric(df["EID"], errors="coerce")

    df = df[df["YEAR"] == 26].copy()
    df = df.dropna(subset=["SUBJECT", "SCHOOL", "CLASS", "EID"])
    df = df.drop_duplicates(subset=["EID", "SCHOOL", "CLASS", "SECTION", "SUBJECT"])

    print(f"    → {len(df):,} rows loaded")
    return df


def load_board_per() -> pd.DataFrame:
    """Load BOARD_PER — board benchmark percentages."""
    print("  [ETL] Loading BOARD_PER ...")
    with _conn() as conn:
        df = pd.read_sql("SELECT * FROM BOARD_PER", conn)

    df["SUBJECT"] = _clean_subject(df["SUBJECT"])
    df["BOARD"] = pd.to_numeric(df["BOARD"], errors="coerce")
    df["YEAR"] = pd.to_numeric(df["YEAR"], errors="coerce")
    df["CLASS"] = pd.to_numeric(df["CLASS"], errors="coerce")

    # Aggregate: mean board % by SUBJECT + CLASS (across years)
    board_agg = df.groupby(["SUBJECT", "CLASS"])["BOARD"].mean().reset_index()
    board_agg.rename(columns={"BOARD": "board_benchmark_pct"}, inplace=True)
    print(f"    → {len(board_agg):,} subject-class benchmarks")
    return board_agg


def load_prac() -> pd.DataFrame:
    """Load PRAC — practical exam marks."""
    print("  [ETL] Loading PRAC ...")
    with _conn() as conn:
        df = pd.read_sql("SELECT * FROM PRAC", conn)

    df["SUBJECT"] = _clean_subject(df["SUBJECT"])
    df["OBTAINED"] = pd.to_numeric(df["OBTAINED"], errors="coerce")
    df["TOTAL"] = pd.to_numeric(df["TOTAL"], errors="coerce")
    df["prac_pct"] = (df["OBTAINED"] / df["TOTAL"] * 100.0).clip(0.0, 100.0)
    df["ROLLNO"] = df["ROLLNO"].astype(str).str.strip().str.replace(r"\.0$", "", regex=True)
    df["YEAR"] = pd.to_numeric(df["YEAR"], errors="coerce")
    df["CLASS"] = pd.to_numeric(df["CLASS"], errors="coerce")

    # Take latest per student-subject-year
    df = df.sort_values("ID", ascending=False).drop_duplicates(
        subset=["ROLLNO", "SUBJECT", "YEAR"], keep="first"
    )
    print(f"    → {len(df):,} rows loaded")
    return df[["ROLLNO", "SUBJECT", "YEAR", "CLASS", "prac_pct"]]


def load_attendance() -> pd.DataFrame:
    """Load House_Attendance_Daily — hostel attendance records."""
    print("  [ETL] Loading House_Attendance_Daily ...")
    with _conn() as conn:
        df = pd.read_sql("SELECT * FROM House_Attendance_Daily", conn)

    df["SMSNO"] = df["SMSNO"].astype(str).str.strip()
    df["Status"] = df["Status"].astype(str).str.strip().str.upper()
    df["School"] = _clean_school(df["School"].astype(str))

    # Aggregate per student
    att_agg = df.groupby("SMSNO").agg(
        total_days=("Status", "count"),
        present_days=("Status", lambda x: (x == "P").sum()),
        absent_days=("Status", lambda x: (x == "A").sum()),
        leave_days=("Status", lambda x: (x == "L").sum()),
    ).reset_index()

    att_agg["attendance_pct"] = (att_agg["present_days"] / att_agg["total_days"] * 100.0).clip(0.0, 100.0)
    att_agg["attendance_available"] = 1

    print(f"    → {len(att_agg):,} students with attendance data")
    return att_agg[["SMSNO", "attendance_pct", "absent_days", "attendance_available"]]


def load_gzt_strength() -> pd.DataFrame:
    """Load GZT_STRENGTH — gazette enrollment and pass counts."""
    print("  [ETL] Loading GZT_STRENGTH ...")
    with _conn() as conn:
        df = pd.read_sql("SELECT * FROM GZT_STRENGTH", conn)

    df["school"] = _clean_school(df["school"].astype(str))
    df["year"] = pd.to_numeric(df["year"], errors="coerce")
    df["count"] = pd.to_numeric(df["count"], errors="coerce")
    df["PASS"] = pd.to_numeric(df["PASS"], errors="coerce")
    df["class"] = pd.to_numeric(df["class"], errors="coerce")

    print(f"    → {len(df):,} rows loaded")
    return df


def load_teahcers() -> pd.DataFrame:
    """Load TEAHCERS — teacher assignments with strength."""
    print("  [ETL] Loading TEAHCERS ...")
    with _conn() as conn:
        df = pd.read_sql("SELECT * FROM TEAHCERS", conn)

    df["SCHOOL"] = _clean_school(df["SCHOOL"].astype(str))
    df["SUBJECT"] = _clean_subject(df["SUBJECT"])
    df["SECTION"] = _clean_section(df["SECTION"].astype(str))
    df["CLASS"] = pd.to_numeric(df["CLASS"], errors="coerce")
    df["YEAR"] = pd.to_numeric(df["YEAR"], errors="coerce")
    df["EID"] = pd.to_numeric(df["EID"], errors="coerce")
    df["STRENGTH"] = pd.to_numeric(df["STRENGTH"], errors="coerce")

    df = df.dropna(subset=["SUBJECT", "SCHOOL", "YEAR", "CLASS", "EID"])
    print(f"    → {len(df):,} rows loaded")
    return df


# ──────────────────────────────────────────────────────────────
# Step 2: Build Student Feature Store
# ──────────────────────────────────────────────────────────────

def build_student_features() -> pd.DataFrame:
    """
    Build the student feature matrix from raw database tables.

    Grain: one row per (student ROLLNO, SUBJECT) for Year 26.
    Target: pct_annual (annual exam percentage).
    """
    print("\n[PHASE 1] Building Student Feature Store ...\n")

    mi = load_marks_internal()
    students = load_students_roll_internal()
    tr_all = load_tr_all()
    hof = load_hof()
    board = load_board_per()
    prac = load_prac()
    attendance = load_attendance()
    teachers_ie = load_teachers_internal()

    # ── 2a. Pivot formative exams to wide format ──
    print("\n  [ETL] Pivoting formative exams to wide format ...")

    # Separate annual (target) from formative (features)
    annual = mi[mi["EXAMTYPE"] == "ANNUAL"][["ROLLNO", "SUBJECT", "CLASS", "clean_pct"]].copy()
    annual.rename(columns={"clean_pct": "pct_annual"}, inplace=True)
    annual = annual.drop_duplicates(subset=["ROLLNO", "SUBJECT"], keep="first")

    formative = mi[mi["EXAMTYPE"] != "ANNUAL"].copy()

    # Pivot formative exams
    exam_types = ["MID_DEC", "MOCK1", "MOCK2", "MOCK3", "MOCK4"]
    pivoted = formative[formative["EXAMTYPE"].isin(exam_types)].pivot_table(
        index=["ROLLNO", "SUBJECT", "CLASS"],
        columns="EXAMTYPE",
        values="clean_pct",
        aggfunc="mean",
    ).reset_index()

    # Rename pivot columns
    rename_map = {et: f"pct_{et.lower()}" for et in exam_types}
    pivoted.rename(columns=rename_map, inplace=True)

    # Merge target onto formative features
    df = pivoted.merge(annual, on=["ROLLNO", "SUBJECT", "CLASS"], how="inner")
    print(f"    → {len(df):,} student-subject rows with both formative and annual data")

    # ── 2b. Compute formative-derived & cross-subject features ──
    print("  [ETL] Computing formative-derived and cross-subject features ...")
    mock_cols = ["pct_mock1", "pct_mock2", "pct_mock3", "pct_mock4"]

    df["mock_mean"] = df[mock_cols].mean(axis=1, skipna=True)
    df["mock_std"] = df[mock_cols].std(axis=1, skipna=True)

    # Mock slope: (latest - earliest) / span
    first_mock = df[mock_cols].apply(lambda row: row.dropna().iloc[0] if row.dropna().shape[0] > 0 else np.nan, axis=1)
    last_mock = df[mock_cols].apply(lambda row: row.dropna().iloc[-1] if row.dropna().shape[0] > 0 else np.nan, axis=1)
    n_mocks = df[mock_cols].notna().sum(axis=1)
    df["mock_slope"] = np.where(n_mocks > 1, (last_mock - first_mock) / (n_mocks - 1), 0.0)

    df["mid_to_mock1_delta"] = df["pct_mock1"] - df["pct_mid_dec"]
    df["mock_improving"] = (df["mock_slope"] > 0).astype(int)
    df["num_formative_exams"] = df[["pct_mid_dec"] + mock_cols].notna().sum(axis=1)
    df["is_zero_in_any_mock"] = (df[mock_cols].eq(0.0).any(axis=1)).astype(int)

    # Cross-subject GPA in Midterm
    mid_only = formative[formative["EXAMTYPE"] == "MID_DEC"]
    gpa_df = mid_only.groupby("ROLLNO")["clean_pct"].agg(
        student_overall_midterm_mean="mean",
        student_subject_count="count"
    ).reset_index()
    df = df.merge(gpa_df, on="ROLLNO", how="left")
    df["student_overall_midterm_mean"] = df["student_overall_midterm_mean"].fillna(df["pct_mid_dec"])
    df["student_subject_delta_to_gpa"] = df["pct_mid_dec"] - df["student_overall_midterm_mean"]

    # Exponential recency weighted mock score (Mock4: 0.40, Mock3: 0.30, Mock2: 0.20, Mock1: 0.10)
    df["mock_exponential_recency_score"] = (
        0.40 * df["pct_mock4"].fillna(df["pct_mid_dec"])
        + 0.30 * df["pct_mock3"].fillna(df["pct_mid_dec"])
        + 0.20 * df["pct_mock2"].fillna(df["pct_mid_dec"])
        + 0.10 * df["pct_mock1"].fillna(df["pct_mid_dec"])
    )

    # Formative completeness indicators
    df["has_mock1"] = df["pct_mock1"].notna().astype(int)
    df["has_mock2"] = df["pct_mock2"].notna().astype(int)
    df["has_mock3"] = df["pct_mock3"].notna().astype(int)
    df["has_mock4"] = df["pct_mock4"].notna().astype(int)
    df["formative_completeness_ratio"] = (df["has_mock1"] + df["has_mock2"] + df["has_mock3"] + df["has_mock4"]) / 4.0

    # ── 2c. Join student demographics ──
    print("  [ETL] Joining student demographics ...")
    df = df.merge(students, on="ROLLNO", how="left", suffixes=("", "_stu"))

    # Use the joined CLASS if original is missing
    if "CLASS_stu" in df.columns:
        df["CLASS"] = df["CLASS"].fillna(df["CLASS_stu"])
        df.drop(columns=["CLASS_stu"], inplace=True, errors="ignore")

    # Clean up class
    df["class_grade"] = pd.to_numeric(df["CLASS"], errors="coerce")

    # Derived demographic features
    df["section_merit_ordinal"] = df["SECTION"].map({"A": 4, "B": 3, "C": 2, "D": 1}).fillna(2)
    df["is_stem_subject"] = df["SUBJECT"].isin(STEM_SUBJECTS).astype(int)
    df["is_language_subject"] = df["SUBJECT"].isin(LANGUAGE_SUBJECTS).astype(int)
    df["is_middle_school"] = df["class_grade"].between(6, 8).astype(int)
    df["is_matric"] = df["class_grade"].between(9, 10).astype(int)
    df["is_hssc"] = df["class_grade"].between(11, 12).astype(int)

    # ── 2d. Join teacher performance metrics ──
    print("  [ETL] Joining teacher performance metrics ...")

    # First, map each student-subject to a teacher via TEACHERS_INTERNAL_EXAM
    teacher_map = teachers_ie[["EID", "SCHOOL", "CLASS", "SECTION", "SUBJECT"]].drop_duplicates()
    teacher_map["CLASS"] = teacher_map["CLASS"].astype(float)

    df["CLASS_float"] = df["class_grade"].astype(float)
    df = df.merge(
        teacher_map,
        left_on=["SCHOOL", "CLASS_float", "SECTION", "SUBJECT"],
        right_on=["SCHOOL", "CLASS", "SECTION", "SUBJECT"],
        how="left",
        suffixes=("", "_teacher"),
    )
    if "CLASS_teacher" in df.columns:
        df.drop(columns=["CLASS_teacher"], inplace=True, errors="ignore")
    df.drop(columns=["CLASS_float"], inplace=True, errors="ignore")

    # Get teacher metrics from TR_ALL (Year 26, ANNUAL)
    tr_metrics = tr_all[["EID", "SCHOOL", "SUBJECT", "CLASS", "SECTION", "PASS%", "CLASS AVG"]].copy()
    tr_metrics.rename(columns={"PASS%": "teacher_pass_pct", "CLASS AVG": "teacher_class_avg"}, inplace=True)
    tr_metrics["CLASS"] = tr_metrics["CLASS"].astype(float)

    df = df.merge(
        tr_metrics,
        left_on=["EID", "SCHOOL", "SUBJECT", "class_grade", "SECTION"],
        right_on=["EID", "SCHOOL", "SUBJECT", "CLASS", "SECTION"],
        how="left",
        suffixes=("", "_tr"),
    )
    if "CLASS_tr" in df.columns:
        df.drop(columns=["CLASS_tr"], inplace=True, errors="ignore")

    # Get teacher position from HOF
    hof_metrics = hof[hof["Year"] == 26][["EID", "SCHOOL", "SUBJECT", "CLASS", "Position", "TOTAL_POSITIONS"]].copy()
    hof_metrics["teacher_position_percentile"] = (
        1.0 - hof_metrics["Position"] / hof_metrics["TOTAL_POSITIONS"]
    ).clip(0.0, 1.0) * 100.0
    hof_metrics["CLASS"] = hof_metrics["CLASS"].astype(float)

    # Aggregate per teacher-subject (mean across sections)
    hof_agg = hof_metrics.groupby(["EID", "SCHOOL", "SUBJECT"]).agg(
        teacher_position_percentile=("teacher_position_percentile", "mean"),
    ).reset_index()

    df = df.merge(hof_agg, on=["EID", "SCHOOL", "SUBJECT"], how="left")

    # ── 2e. Join board benchmarks ──
    print("  [ETL] Joining board benchmarks ...")
    df = df.merge(board, on=["SUBJECT", "CLASS"], how="left", suffixes=("", "_board"))

    # ── 2f. Join practical marks ──
    print("  [ETL] Joining practical marks ...")
    # Use the most recent practical marks available for this student
    prac_latest = prac.sort_values("YEAR", ascending=False).drop_duplicates(
        subset=["ROLLNO", "SUBJECT"], keep="first"
    )
    df = df.merge(
        prac_latest[["ROLLNO", "SUBJECT", "prac_pct"]],
        on=["ROLLNO", "SUBJECT"],
        how="left",
    )

    # ── 2g. Join attendance ──
    print("  [ETL] Joining attendance data ...")
    df = df.merge(attendance, on="SMSNO", how="left")
    df["attendance_available"] = df["attendance_available"].fillna(0).astype(int)
    df["attendance_pct"] = df["attendance_pct"].fillna(df["attendance_pct"].median())

    # ── 2h. Rename for model consumption ──
    df.rename(columns={
        "SCHOOL": "school",
        "SECTION": "section",
        "CATEGORY": "category",
        "GROUP": "group",
        "HOUSE": "house",
        "SUBJECT": "subject",
    }, inplace=True)

    # Final feature selection
    feature_cols = [
        # Formative exam scores
        "pct_mid_dec", "pct_mock1", "pct_mock2", "pct_mock3", "pct_mock4",
        "mock_mean", "mock_std", "mock_slope", "mid_to_mock1_delta",
        "mock_improving", "num_formative_exams", "is_zero_in_any_mock",
        "student_overall_midterm_mean", "student_subject_delta_to_gpa",
        "mock_exponential_recency_score", "formative_completeness_ratio",
        "has_mock1", "has_mock2", "has_mock3", "has_mock4",
        # Demographics
        "school", "class_grade", "section", "section_merit_ordinal",
        "category", "group", "house", "subject",
        # Subject flags
        "is_stem_subject", "is_language_subject",
        # Stage flags
        "is_middle_school", "is_matric", "is_hssc",
        # Teacher metrics
        "teacher_class_avg", "teacher_pass_pct", "teacher_position_percentile",
        # Board and practical
        "board_benchmark_pct", "prac_pct",
        # Attendance
        "attendance_pct", "attendance_available",
        # Target
        "pct_annual",
        # IDs (kept for analysis, dropped before training)
        "ROLLNO", "EID",
    ]

    # Only keep columns that exist
    existing_cols = [c for c in feature_cols if c in df.columns]
    df = df[existing_cols].copy()

    print(f"\n  ✅ Student features: {len(df):,} rows × {len(df.columns)} columns")
    print(f"     Schools: {df['school'].nunique()} | Subjects: {df['subject'].nunique()}")
    print(f"     Target range: {df['pct_annual'].min():.1f}% – {df['pct_annual'].max():.1f}%")
    print(f"     Target mean: {df['pct_annual'].mean():.1f}% | median: {df['pct_annual'].median():.1f}%")
    print(f"     Null counts:\n{df.isnull().sum()[df.isnull().sum() > 0].to_string()}")

    return df


# ──────────────────────────────────────────────────────────────
# Step 3: Build Teacher Feature Store
# ──────────────────────────────────────────────────────────────

def build_teacher_features() -> pd.DataFrame:
    """
    Build teacher feature matrix.

    Grain: one row per (EID, SCHOOL, SUBJECT, CLASS, SECTION, Year).
    Target: teacher_credibility_score (composite).
    """
    print("\n[PHASE 2] Building Teacher Feature Store ...\n")

    tr = load_tr()
    tr_all = load_tr_all()
    hof = load_hof()
    hof_old = load_hof_old()
    board = load_board_per()

    # Use TR as the base (38,937 rows, Years 22-26)
    # Also incorporate TR_ALL which has the same structure
    # TR already has all the score distributions and performance metrics

    df = tr.copy()

    # ── 3a. Core features from TR ──
    df.rename(columns={
        "SCHOOL": "school",
        "SUBJECT": "subject",
        "SECTION": "section",
        "Year": "year",
        "STRENGTH": "strength",
        "Count_90_100": "count_90_100",
        "Count_80_90": "count_80_90",
        "Count_70_80": "count_70_80",
        "Count_60_70": "count_60_70",
        "Count_50_60": "count_50_60",
        "Count_40_50": "count_40_50",
        "Count_0_39": "count_0_39",
        "APPEARED": "appeared",
        "PASSED": "passed",
        "PASS%": "pass_pct",
        "CLASS AVG": "class_avg",
        "CLASS": "class_grade",
    }, inplace=True)

    # Derived features
    df["appeared_strength_ratio"] = (df["appeared"] / df["strength"].replace(0, np.nan)).clip(0, 2)
    df["above_70_pct"] = (
        (df["count_90_100"].fillna(0) + df["count_80_90"].fillna(0) + df["count_70_80"].fillna(0))
        / df["appeared"].replace(0, np.nan)
    ).clip(0, 1)
    df["below_40_pct"] = (df["count_0_39"].fillna(0) / df["appeared"].replace(0, np.nan)).clip(0, 1)
    df["is_stem_subject"] = df["subject"].isin(STEM_SUBJECTS).astype(int)

    # ── 3b. Join HOF position data ──
    print("  [ETL] Joining HOF position data ...")
    # Combine HOF and HOF_OLD
    hof_combined = pd.concat([hof, hof_old], ignore_index=True)
    hof_combined["position_percentile"] = (
        1.0 - hof_combined["Position"] / hof_combined["TOTAL_POSITIONS"]
    ).clip(0.0, 1.0) * 100.0

    hof_agg = hof_combined.groupby(["EID", "SCHOOL", "SUBJECT", "Year"]).agg(
        work_load=("WORK LOAD", "first"),
        position_percentile=("position_percentile", "mean"),
    ).reset_index()
    hof_agg.rename(columns={"SCHOOL": "school", "SUBJECT": "subject", "Year": "year"}, inplace=True)

    df = df.merge(hof_agg, on=["EID", "school", "subject", "year"], how="left")

    # ── 3c. Compute teacher-level aggregate features ──
    print("  [ETL] Computing teacher-level aggregate features ...")

    # Total classes taught per teacher per year
    classes_per_year = df.groupby(["EID", "year"]).size().reset_index(name="total_classes_taught")
    df = df.merge(classes_per_year, on=["EID", "year"], how="left")

    # Years of data per teacher
    years_data = df.groupby("EID")["year"].nunique().reset_index(name="years_of_data")
    df = df.merge(years_data, on="EID", how="left")

    # Previous year class avg (self-lag)
    df = df.sort_values(["EID", "school", "subject", "class_grade", "section", "year"])
    prev = df[["EID", "school", "subject", "class_grade", "section", "year", "class_avg"]].copy()
    prev["year"] = prev["year"] + 1
    prev.rename(columns={"class_avg": "prev_year_class_avg"}, inplace=True)
    df = df.merge(prev, on=["EID", "school", "subject", "class_grade", "section", "year"], how="left")

    # Class avg trend (slope across years per teacher-subject)
    trend = df.groupby(["EID", "subject"]).apply(
        lambda g: pd.Series({
            "class_avg_trend": np.polyfit(g["year"].values, g["class_avg"].values, 1)[0]
            if len(g) >= 2 and g["class_avg"].notna().sum() >= 2 else 0.0
        }),
        include_groups=False,
    ).reset_index()
    df = df.merge(trend, on=["EID", "subject"], how="left")

    # ── 3d. Join board benchmark for context ──
    print("  [ETL] Joining board benchmark ...")
    board_by_subj = board.groupby("SUBJECT")["board_benchmark_pct"].mean().reset_index()
    board_by_subj.rename(columns={"SUBJECT": "subject"}, inplace=True)

    # Mean school performance vs board
    school_avg = df.groupby(["school", "subject"])["class_avg"].mean().reset_index(name="school_mean_avg")
    school_avg = school_avg.merge(board_by_subj, on="subject", how="left")
    school_avg["school_mean_board_delta"] = school_avg["school_mean_avg"] - school_avg["board_benchmark_pct"].fillna(
        school_avg["school_mean_avg"])
    df = df.merge(school_avg[["school", "subject", "school_mean_board_delta"]], on=["school", "subject"], how="left")

    # ── 3e. Compute target: teacher_credibility_score ──
    print("  [ETL] Computing teacher credibility score ...")
    df["teacher_credibility_score"] = (
        0.35 * df["class_avg"].fillna(0)
        + 0.25 * df["pass_pct"].fillna(0)
        + 0.20 * df["above_70_pct"].fillna(0) * 100
        + 0.10 * df["position_percentile"].fillna(50)
        + 0.10 * df["class_avg"].fillna(0)  # value-added proxy (using raw class_avg as fallback)
    )

    # Final feature selection
    feature_cols = [
        "subject", "school", "section", "class_grade", "year",
        "strength", "appeared", "appeared_strength_ratio",
        "count_90_100", "count_80_90", "count_70_80", "count_60_70",
        "count_50_60", "count_40_50", "count_0_39",
        "pass_pct", "above_70_pct", "below_40_pct",
        "is_stem_subject",
        "work_load", "total_classes_taught", "years_of_data",
        "prev_year_class_avg", "class_avg_trend",
        "school_mean_board_delta",
        "teacher_credibility_score",
        "EID", "NAME", "class_avg",  # kept for analysis
    ]
    existing_cols = [c for c in feature_cols if c in df.columns]
    df = df[existing_cols].copy()

    print(f"\n  ✅ Teacher features: {len(df):,} rows × {len(df.columns)} columns")
    print(f"     Unique teachers: {df['EID'].nunique()} | Schools: {df['school'].nunique()}")
    print(f"     Target range: {df['teacher_credibility_score'].min():.1f} – {df['teacher_credibility_score'].max():.1f}")
    print(f"     Target mean: {df['teacher_credibility_score'].mean():.1f}")

    return df


# ──────────────────────────────────────────────────────────────
# Step 4: Build Branch Feature Store
# ──────────────────────────────────────────────────────────────

def build_branch_features() -> pd.DataFrame:
    """
    Build branch-level feature matrix.

    Grain: one row per (SCHOOL, YEAR).
    Target: branch_reputation_score (composite).
    """
    print("\n[PHASE 3] Building Branch Feature Store ...\n")

    marks = load_marks()
    students = load_students_roll()
    tr = load_tr()
    hof = load_hof()
    hof_old = load_hof_old()
    board = load_board_per()
    gzt = load_gzt_strength()

    # We need SCHOOL on marks — join from marks_with_school_name or students_roll
    print("  [ETL] Adding SCHOOL to MARKS via marks_with_school_name ...")
    with _conn() as conn:
        mwsn = pd.read_sql("SELECT ID, SCHOOL, SECTION FROM marks_with_school_name", conn)
    mwsn["SCHOOL"] = _clean_school(mwsn["SCHOOL"].astype(str))

    # Join school to marks via ID
    marks = marks.merge(mwsn[["ID", "SCHOOL"]], on="ID", how="left")

    # For marks without school (Year 26 entries not in mwsn), try via STUDENTS_ROLL
    missing_school = marks["SCHOOL"].isna()
    if missing_school.sum() > 0:
        sr_map = students[["ROLLNO", "SCHOOL", "YEAR"]].drop_duplicates(subset=["ROLLNO", "YEAR"])
        marks_missing = marks[missing_school].drop(columns=["SCHOOL"])
        marks_missing = marks_missing.merge(
            sr_map, on=["ROLLNO", "YEAR"], how="left"
        )
        marks.loc[missing_school, "SCHOOL"] = marks_missing["SCHOOL"].values

    marks = marks.dropna(subset=["SCHOOL"])
    marks["SCHOOL"] = _clean_school(marks["SCHOOL"])
    print(f"    → {len(marks):,} marks with school assignment")

    # ── 4a. Student performance aggregation per branch-year ──
    print("  [ETL] Aggregating student marks per branch-year ...")
    branch_marks = marks.groupby(["SCHOOL", "YEAR"]).agg(
        branch_mean_pct=("clean_pct", "mean"),
        branch_median_pct=("clean_pct", "median"),
        branch_std_pct=("clean_pct", "std"),
        branch_total_records=("clean_pct", "count"),
        branch_pass_count=("STATUS", lambda x: (x == "PASS").sum()),
    ).reset_index()

    branch_marks["branch_pass_rate"] = (
        branch_marks["branch_pass_count"] / branch_marks["branch_total_records"]
    ).clip(0, 1)
    branch_marks["branch_fail_rate"] = 1 - branch_marks["branch_pass_rate"]

    # Score bands
    bands = marks.groupby(["SCHOOL", "YEAR"]).apply(
        lambda g: pd.Series({
            "branch_above_70_pct": (g["clean_pct"] >= 70).mean(),
            "branch_below_40_pct": (g["clean_pct"] < 40).mean(),
        }),
        include_groups=False,
    ).reset_index()
    branch_marks = branch_marks.merge(bands, on=["SCHOOL", "YEAR"], how="left")

    # Per-subject averages
    for subj, col_name in [("MATHEMATICS", "branch_math_avg"), ("ENGLISH", "branch_eng_avg"),
                           ("GENERAL SCIENCE", "branch_sci_avg"), ("URDU", "branch_urdu_avg")]:
        subj_avg = marks[marks["SUBJECT"] == subj].groupby(["SCHOOL", "YEAR"])["clean_pct"].mean().reset_index(
            name=col_name)
        branch_marks = branch_marks.merge(subj_avg, on=["SCHOOL", "YEAR"], how="left")

    # STEM and humanities averages
    stem_avg = marks[marks["SUBJECT"].isin(STEM_SUBJECTS)].groupby(
        ["SCHOOL", "YEAR"])["clean_pct"].mean().reset_index(name="branch_stem_avg")
    hum_avg = marks[marks["SUBJECT"].isin(HUMANITIES_SUBJECTS)].groupby(
        ["SCHOOL", "YEAR"])["clean_pct"].mean().reset_index(name="branch_humanities_avg")
    branch_marks = branch_marks.merge(stem_avg, on=["SCHOOL", "YEAR"], how="left")
    branch_marks = branch_marks.merge(hum_avg, on=["SCHOOL", "YEAR"], how="left")
    branch_marks["branch_stem_humanities_gap"] = (
        branch_marks["branch_stem_avg"].fillna(0) - branch_marks["branch_humanities_avg"].fillna(0)
    )

    df = branch_marks.copy()

    # ── 4b. Student demographics per branch-year ──
    print("  [ETL] Computing branch demographics ...")
    stu_demo = students.groupby(["SCHOOL", "YEAR"]).agg(
        branch_total_students=("ID", "count"),
        boarder_count=("CATEGROY", lambda x: (x == "B").sum()),
        scholar_count=("CATEGROY", lambda x: (x == "S").sum()),
        ds_count=("CATEGROY", lambda x: (x == "DS").sum()),
    ).reset_index()
    stu_demo["branch_boarder_pct"] = stu_demo["boarder_count"] / stu_demo["branch_total_students"].replace(0, np.nan)
    stu_demo["branch_scholar_pct"] = stu_demo["scholar_count"] / stu_demo["branch_total_students"].replace(0, np.nan)
    stu_demo["branch_ds_pct"] = stu_demo["ds_count"] / stu_demo["branch_total_students"].replace(0, np.nan)

    # Class distribution
    class_dist = students.groupby(["SCHOOL", "YEAR"]).apply(
        lambda g: pd.Series({
            "branch_middle_pct": g["CLASS"].between(6, 8).mean(),
            "branch_matric_pct": g["CLASS"].between(9, 10).mean(),
            "branch_hssc_pct": g["CLASS"].between(11, 12).mean(),
        }),
        include_groups=False,
    ).reset_index()
    stu_demo = stu_demo.merge(class_dist, on=["SCHOOL", "YEAR"], how="left")

    df = df.merge(
        stu_demo[["SCHOOL", "YEAR", "branch_total_students", "branch_boarder_pct",
                   "branch_scholar_pct", "branch_ds_pct", "branch_middle_pct",
                   "branch_matric_pct", "branch_hssc_pct"]],
        on=["SCHOOL", "YEAR"], how="left"
    )

    # ── 4c. Teacher quality per branch-year ──
    print("  [ETL] Aggregating teacher quality per branch ...")
    # Filter TR to CATEGROY == 'ALL' (if column exists) or use all rows
    tr_clean = tr.copy()
    if "CATEGROY" in tr_clean.columns:
        tr_all_cat = tr_clean[tr_clean["CATEGROY"].astype(str).str.strip().str.upper() == "ALL"]
        if len(tr_all_cat) > len(tr_clean) * 0.3:
            tr_clean = tr_all_cat

    teacher_agg = tr_clean.groupby(["SCHOOL", "Year"]).agg(
        branch_teacher_avg_class_avg=("CLASS AVG", "mean"),
        branch_teacher_avg_pass_pct=("PASS%", "mean"),
        branch_teacher_count=("EID", "nunique"),
    ).reset_index()
    teacher_agg.rename(columns={"Year": "YEAR"}, inplace=True)

    df = df.merge(teacher_agg, on=["SCHOOL", "YEAR"], how="left")

    # Top teacher percentage from HOF
    hof_all = pd.concat([hof, hof_old], ignore_index=True)
    hof_all["is_top_quarter"] = (hof_all["Position"] <= hof_all["TOTAL_POSITIONS"] * 0.25).astype(int)
    hof_branch = hof_all.groupby(["SCHOOL", "Year"]).agg(
        total_hof_entries=("EID", "count"),
        top_quarter_count=("is_top_quarter", "sum"),
    ).reset_index()
    hof_branch["branch_top_teacher_pct"] = (
        hof_branch["top_quarter_count"] / hof_branch["total_hof_entries"].replace(0, np.nan)
    ).clip(0, 1)
    hof_branch.rename(columns={"Year": "YEAR"}, inplace=True)

    df = df.merge(hof_branch[["SCHOOL", "YEAR", "branch_top_teacher_pct"]], on=["SCHOOL", "YEAR"], how="left")

    # ── 4d. Board benchmark comparison ──
    print("  [ETL] Computing board benchmark comparison ...")
    board_overall = board.groupby("SUBJECT")["board_benchmark_pct"].mean()
    board_mean = board_overall.mean()
    df["branch_vs_board_delta"] = df["branch_mean_pct"] - board_mean

    # ── 4e. Gazette strength ──
    print("  [ETL] Joining gazette strength ...")
    gzt_branch = gzt.groupby(["school", "year"]).agg(
        branch_gazette_strength=("count", "sum"),
    ).reset_index()
    gzt_branch.rename(columns={"school": "SCHOOL", "year": "YEAR"}, inplace=True)
    df = df.merge(gzt_branch, on=["SCHOOL", "YEAR"], how="left")

    # ── 4f. Previous year reputation (lagged target) ──
    print("  [ETL] Computing previous year reputation ...")
    df["branch_gender"] = df["SCHOOL"].str[-1].map({"B": 0, "G": 1}).fillna(-1).astype(int)
    df["branch_city"] = df["SCHOOL"].map(CAMPUS_CITY).fillna("OTHER")

    # Compute reputation score
    df["branch_reputation_score"] = (
        0.30 * df["branch_mean_pct"].fillna(0)
        + 0.20 * df["branch_pass_rate"].fillna(0) * 100
        + 0.15 * df["branch_above_70_pct"].fillna(0) * 100
        + 0.15 * df["branch_teacher_avg_class_avg"].fillna(0)
        + 0.10 * df["branch_vs_board_delta"].fillna(0).clip(-20, 20) + 10  # normalize delta
        + 0.10 * df["branch_gazette_strength"].fillna(0).clip(0, 500) / 5  # normalize strength
    )

    # Lag: previous year reputation
    prev_rep = df[["SCHOOL", "YEAR", "branch_reputation_score"]].copy()
    prev_rep["YEAR"] = prev_rep["YEAR"] + 1
    prev_rep.rename(columns={"branch_reputation_score": "branch_prev_year_reputation"}, inplace=True)
    df = df.merge(prev_rep, on=["SCHOOL", "YEAR"], how="left")

    # Rename for consistency
    df.rename(columns={"SCHOOL": "school", "YEAR": "year"}, inplace=True)

    print(f"\n  ✅ Branch features: {len(df):,} rows × {len(df.columns)} columns")
    print(f"     Schools: {df['school'].nunique()} | Years: {df['year'].nunique()}")
    print(f"     Target range: {df['branch_reputation_score'].min():.1f} – {df['branch_reputation_score'].max():.1f}")
    print(f"     Target mean: {df['branch_reputation_score'].mean():.1f}")

    return df


def build_subject_features() -> pd.DataFrame:
    """
    Build subject-level feature matrix.
    Grain: one row per (SUBJECT, CLASS, SCHOOL).
    Target: subject_annual_pass_pct and board_alignment_gap.
    """
    print("\n[PHASE 4] Building Subject Feature Store ...\n")
    mi = load_marks_internal()
    board = load_board_per()

    # Aggregate subject performance across internal exams
    subj_agg = mi.groupby(["SUBJECT", "CLASS", "SCHOOL"]).agg(
        subject_avg_pct=("clean_pct", "mean"),
        subject_std_pct=("clean_pct", "std"),
        total_students=("clean_pct", "count"),
        pass_count=("STATUS", lambda x: (x == "PASS").sum()),
    ).reset_index()

    subj_agg["subject_annual_pass_pct"] = (subj_agg["pass_count"] / subj_agg["total_students"] * 100.0).clip(0.0, 100.0)
    subj_agg = subj_agg.merge(board, on=["SUBJECT", "CLASS"], how="left")
    subj_agg["board_benchmark_pct"] = subj_agg["board_benchmark_pct"].fillna(subj_agg["subject_avg_pct"])
    subj_agg["board_alignment_gap"] = subj_agg["subject_avg_pct"] - subj_agg["board_benchmark_pct"]
    subj_agg["is_stem_subject"] = subj_agg["SUBJECT"].isin(STEM_SUBJECTS).astype(int)
    subj_agg["is_language_subject"] = subj_agg["SUBJECT"].isin(LANGUAGE_SUBJECTS).astype(int)

    subj_agg.rename(columns={
        "SUBJECT": "subject",
        "CLASS": "class_grade",
        "SCHOOL": "school"
    }, inplace=True)

    print(f"\n  ✅ Subject features: {len(subj_agg):,} rows × {len(subj_agg.columns)} columns")
    return subj_agg


# ──────────────────────────────────────────────────────────────
# Main: Run Full ETL
# ──────────────────────────────────────────────────────────────

def run_etl() -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """
    Execute the complete ETL pipeline across all 4 tiers.

    Returns:
        (student_df, teacher_df, branch_df, subject_df)
    """
    print("=" * 70)
    print("  EduQuery AI — 4-Tier ETL Pipeline")
    print("=" * 70)
    print(f"  Database: {DB_PATH}")
    print(f"  Output:   {FEATURES_DIR}")
    print("=" * 70)

    FEATURES_DIR.mkdir(parents=True, exist_ok=True)

    # Build feature stores
    student_df = build_student_features()
    teacher_df = build_teacher_features()
    branch_df = build_branch_features()
    subject_df = build_subject_features()

    # Save to Parquet
    student_path = FEATURES_DIR / "student_features.parquet"
    teacher_path = FEATURES_DIR / "teacher_features.parquet"
    branch_path = FEATURES_DIR / "branch_features.parquet"
    subject_path = FEATURES_DIR / "subject_features.parquet"

    student_df.to_parquet(student_path, index=False, engine="pyarrow")
    teacher_df.to_parquet(teacher_path, index=False, engine="pyarrow")
    branch_df.to_parquet(branch_path, index=False, engine="pyarrow")
    subject_df.to_parquet(subject_path, index=False, engine="pyarrow")

    print("\n" + "=" * 70)
    print("  ETL COMPLETE (4 Tiers)")
    print("=" * 70)
    print(f"  Student features: {student_path} ({len(student_df):,} rows)")
    print(f"  Teacher features: {teacher_path} ({len(teacher_df):,} rows)")
    print(f"  Branch features:  {branch_path} ({len(branch_df):,} rows)")
    print(f"  Subject features: {subject_path} ({len(subject_df):,} rows)")
    print("=" * 70)

    return student_df, teacher_df, branch_df, subject_df


if __name__ == "__main__":
    run_etl()
