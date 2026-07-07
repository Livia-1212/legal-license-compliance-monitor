from pathlib import Path

import pandas as pd
from psycopg2.extras import execute_values

from src.db.connection import get_connection


ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = ROOT / "data" / "raw"


EXPECTED_COLUMNS = {
    "attorneys": [
        "attorney_id",
        "name",
        "email",
        "date_of_birth",
        "title",
        "office",
        "practice_area",
        "employment_status",
    ],
    "licenses": [
        "attorney_id",
        "jurisdiction",
        "admission_date",
        "admission_year",
        "license_status",
        "registration_expiry",
    ],
    "cle_records": [
        "attorney_id",
        "jurisdiction",
        "required_hours",
        "completed_hours",
        "deadline",
    ],
    "jurisdiction_rules": [
        "jurisdiction",
        "cle_required_hours",
        "registration_cycle",
    ],
    "matters": [
        "matter_id",
        "matter_name",
        "jurisdiction",
        "client",
        "revenue",
        "matter_type",
        "status",
    ],
    "matter_assignments": [
        "matter_id",
        "attorney_id",
        "role",
        "assignment_date",
    ],
}


DATE_COLUMNS = {
    "attorneys": ["date_of_birth"],
    "licenses": ["admission_date", "registration_expiry"],
    "cle_records": ["deadline"],
    "matter_assignments": ["assignment_date"],
}


LOAD_ORDER = [
    "jurisdiction_rules",
    "attorneys",
    "licenses",
    "cle_records",
    "matters",
    "matter_assignments",
]


def validate_dataframe(df: pd.DataFrame, dataset_name: str) -> tuple[bool, str]:
    """
    Validate dataframe columns against the expected dataset schema.
    """
    expected = EXPECTED_COLUMNS.get(dataset_name)

    if expected is None:
        return False, f"Unknown dataset: {dataset_name}"

    missing = [column for column in expected if column not in df.columns]
    if missing:
        return False, f"Missing required columns for {dataset_name}: {missing}"

    return True, "OK"


def normalize_dates(df: pd.DataFrame, dataset_name: str) -> pd.DataFrame:
    """
    Convert known date columns to Python date objects.
    Invalid or missing dates are converted to None.
    """
    df = df.copy()

    for column in DATE_COLUMNS.get(dataset_name, []):
        if column in df.columns:
            df[column] = pd.to_datetime(df[column], errors="coerce").dt.date
            df[column] = df[column].where(pd.notnull(df[column]), None)

    return df


def load_csv_dataset(dataset_name: str) -> pd.DataFrame:
    """
    Load and validate one CSV dataset from data/raw.
    """
    csv_path = DATA_DIR / f"{dataset_name}.csv"

    if not csv_path.exists():
        raise FileNotFoundError(f"CSV file not found: {csv_path}")

    df = pd.read_csv(csv_path)

    valid, message = validate_dataframe(df, dataset_name)
    if not valid:
        raise ValueError(message)

    return normalize_dates(df, dataset_name)


def insert_dataframe(conn, table_name: str, df: pd.DataFrame) -> None:
    """
    Insert dataframe rows into a PostgreSQL table.
    """
    if df.empty:
        return

    allowed_tables = set(EXPECTED_COLUMNS.keys())
    if table_name not in allowed_tables:
        raise ValueError(f"Unsupported table name: {table_name}")

    columns = list(EXPECTED_COLUMNS[table_name])
    df = df[columns]

    values = [tuple(row) for row in df.to_numpy()]

    query = f"""
        INSERT INTO {table_name} ({", ".join(columns)})
        VALUES %s
    """

    with conn.cursor() as cursor:
        execute_values(cursor, query, values)


def seed_database_from_csv() -> None:
    """
    Truncate PostgreSQL tables and seed them from data/raw CSV files.
    """
    conn = get_connection()

    try:
        with conn.cursor() as cursor:
            cursor.execute(
                """
                TRUNCATE
                    matter_assignments,
                    cle_records,
                    licenses,
                    matters,
                    attorneys,
                    jurisdiction_rules
                RESTART IDENTITY CASCADE;
                """
            )

        for dataset_name in LOAD_ORDER:
            df = load_csv_dataset(dataset_name)
            insert_dataframe(conn, dataset_name, df)

        conn.commit()
        print("PostgreSQL database seeded successfully from CSV files.")

    except Exception:
        conn.rollback()
        raise

    finally:
        conn.close()


if __name__ == "__main__":
    seed_database_from_csv()
