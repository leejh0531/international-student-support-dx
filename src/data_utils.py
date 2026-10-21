"""Data loading and query logic shared by the UI and dataset checks."""
from pathlib import Path

import pandas as pd

DATA_DIR = Path(__file__).resolve().parents[1] / "data"
REQUIRED_COLUMNS = {
    "faculty_summary.csv": "faculty_id faculty_ja faculty_en department_count campus_ja campus_en source_id last_verified",
    "departments.csv": "department_id faculty_id faculty_ja faculty_en department_ja department_en campus_ja campus_en source_id last_verified",
    "academic_requirements.csv": "requirement_id department_id admission_year student_type requirement_type stage title_ja title_en detail_ja detail_en primary_contact_ja primary_contact_en source_id confidence last_verified",
    "support_categories.csv": "category_id category_ja category_en owner_type primary_contact_ja primary_contact_en official_check_required notes_ja notes_en",
    "support_faq.csv": "faq_id category_id question_ja question_en answer_ja answer_en contact_ja contact_en source_type confidence last_verified",
    "sources.csv": "source_id source_name source_type source_url access_level last_verified notes",
}


def load_table(name: str, data_dir: Path = DATA_DIR) -> pd.DataFrame:
    frame = pd.read_csv(data_dir / name, dtype=str, keep_default_na=False)
    missing = set(REQUIRED_COLUMNS[name].split()) - set(frame.columns)
    if missing:
        raise ValueError(f"{name}: missing columns: {', '.join(sorted(missing))}")
    if name == "faculty_summary.csv":
        frame["department_count"] = pd.to_numeric(frame["department_count"], errors="raise")
    return frame


def search_faq(frame: pd.DataFrame, keyword: str) -> pd.DataFrame:
    if not keyword:
        return frame.copy()
    mask = pd.Series(False, index=frame.index)
    for column in ("question_ja", "question_en", "answer_ja", "answer_en", "category_id"):
        mask |= frame[column].astype("string").str.contains(keyword, case=False, na=False, regex=False)
    return frame.loc[mask].copy()


def filter_requirements(frame: pd.DataFrame, departments: pd.DataFrame,
                        department: str = "all", student_type: str = "all",
                        requirement_type: str = "all", stage: str = "all",
                        admission_year: str = "all") -> pd.DataFrame:
    result = frame.copy()
    if department != "all":
        applicable = {department}
        if not departments.empty:
            faculty_ids = departments.loc[departments["department_id"] == department, "faculty_id"]
            applicable.update("all_" + str(f) for f in faculty_ids.dropna() if str(f))
        result = result[result["department_id"].isin(applicable)]
    for column, selected in (("student_type", student_type), ("requirement_type", requirement_type),
                             ("stage", stage), ("admission_year", admission_year)):
        if selected != "all":
            result = result[result[column].astype(str) == str(selected)]
    return result


def validate_dataset(data_dir: Path = DATA_DIR) -> dict[str, pd.DataFrame]:
    tables = {name: load_table(name, data_dir) for name in REQUIRED_COLUMNS}
    ids = {
        "faculty_summary.csv": "faculty_id", "departments.csv": "department_id",
        "academic_requirements.csv": "requirement_id", "support_categories.csv": "category_id",
        "support_faq.csv": "faq_id", "sources.csv": "source_id",
    }
    for name, key in ids.items():
        values = tables[name][key].str.strip()
        if values.eq("").any() or values.duplicated().any():
            raise ValueError(f"{name}: blank or duplicate {key}")
    faculties = set(tables["faculty_summary.csv"]["faculty_id"])
    departments = tables["departments.csv"]
    if not set(departments["faculty_id"]) <= faculties:
        raise ValueError("departments.csv: unknown faculty_id")
    valid_departments = set(departments["department_id"]) | {"all_" + f for f in faculties}
    if not set(tables["academic_requirements.csv"]["department_id"]) <= valid_departments:
        raise ValueError("academic_requirements.csv: unknown department/faculty scope")
    categories = set(tables["support_categories.csv"]["category_id"])
    if not set(tables["support_faq.csv"]["category_id"]) <= categories:
        raise ValueError("support_faq.csv: unknown category_id")
    sources = set(tables["sources.csv"]["source_id"])
    for name in ("faculty_summary.csv", "departments.csv", "academic_requirements.csv"):
        if not set(tables[name]["source_id"]) <= sources:
            raise ValueError(f"{name}: unknown source_id")
    for name in ("academic_requirements.csv", "support_faq.csv"):
        if not set(tables[name]["confidence"]) <= {"high", "medium", "low"}:
            raise ValueError(f"{name}: invalid confidence label")
    return tables
