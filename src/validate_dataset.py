import pandas as pd
from pathlib import Path

DATA_DIR = Path("data")

required_files = [
    "departments.csv",
    "academic_requirements.csv",
    "course_categories.csv",
    "student_advice_rules.csv",
    "sources.csv",
]

def check_file_exists():
    for file in required_files:
        path = DATA_DIR / file
        if not path.exists():
            raise FileNotFoundError(f"Missing file: {path}")
    print("All required files exist.")

def check_academic_requirements():
    df = pd.read_csv(DATA_DIR / "academic_requirements.csv")

    required_columns = [
        "requirement_id",
        "department_id",
        "admission_year",
        "student_type",
        "requirement_type",
        "title_ja",
        "title_en",
        "detail_ja",
        "detail_en",
        "primary_contact_ja",
        "primary_contact_en",
        "source_id",
        "confidence",
        "last_verified",
    ]

    missing = [col for col in required_columns if col not in df.columns]
    if missing:
        raise ValueError(f"Missing columns in academic_requirements.csv: {missing}")

    allowed_confidence = {"high", "medium", "low"}
    invalid_confidence = set(df["confidence"]) - allowed_confidence
    if invalid_confidence:
        raise ValueError(f"Invalid confidence values: {invalid_confidence}")

    print(f"academic_requirements.csv OK: {len(df)} records")

def check_source_ids():
    req = pd.read_csv(DATA_DIR / "academic_requirements.csv")
    sources = pd.read_csv(DATA_DIR / "sources.csv")

    valid_sources = set(sources["source_id"])
    used_sources = set(req["source_id"])

    missing_sources = used_sources - valid_sources
    if missing_sources:
        raise ValueError(f"Source IDs not found in sources.csv: {missing_sources}")

    print("Source ID check OK.")

if __name__ == "__main__":
    check_file_exists()
    check_academic_requirements()
    check_source_ids()
    print("Dataset validation completed.")