import pandas as pd

from src.db.connection import get_connection


TABLES = [
    "attorneys",
    "licenses",
    "cle_records",
    "jurisdiction_rules",
    "matters",
    "matter_assignments",
]


def load_table(table_name: str) -> pd.DataFrame:
    """
    Load one PostgreSQL table into a pandas DataFrame.
    """
    if table_name not in TABLES:
        raise ValueError(f"Unsupported table name: {table_name}")

    conn = get_connection()

    try:
        query = f"SELECT * FROM {table_name};"
        return pd.read_sql_query(query, conn)

    finally:
        conn.close()


def load_all_data_from_db() -> dict[str, pd.DataFrame]:
    """
    Load all core PostgreSQL tables into pandas DataFrames.
    """
    return {table_name: load_table(table_name) for table_name in TABLES}


def create_attorney(attorney_data: dict) -> None:
    """
    Insert a new attorney record into PostgreSQL.
    """
    conn = get_connection()

    try:
        with conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO attorneys (
                    attorney_id,
                    name,
                    email,
                    date_of_birth,
                    title,
                    office,
                    practice_area,
                    employment_status
                )
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s);
                """,
                (
                    attorney_data["attorney_id"],
                    attorney_data["name"],
                    attorney_data["email"],
                    attorney_data["date_of_birth"],
                    attorney_data["title"],
                    attorney_data["office"],
                    attorney_data["practice_area"],
                    attorney_data["employment_status"],
                ),
            )

        conn.commit()

    except Exception:
        conn.rollback()
        raise

    finally:
        conn.close()


def create_license(license_data: dict) -> None:
    """
    Insert a new attorney license record into PostgreSQL.
    """
    conn = get_connection()

    try:
        with conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO licenses (
                    attorney_id,
                    jurisdiction,
                    admission_date,
                    admission_year,
                    license_status,
                    registration_expiry
                )
                VALUES (%s, %s, %s, %s, %s, %s);
                """,
                (
                    license_data["attorney_id"],
                    license_data["jurisdiction"],
                    license_data["admission_date"],
                    license_data["admission_year"],
                    license_data["license_status"],
                    license_data["registration_expiry"],
                ),
            )

        conn.commit()

    except Exception:
        conn.rollback()
        raise

    finally:
        conn.close()


def create_cle_record(cle_data: dict) -> None:
    """
    Insert a new CLE compliance record into PostgreSQL.
    """
    conn = get_connection()

    try:
        with conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO cle_records (
                    attorney_id,
                    jurisdiction,
                    required_hours,
                    completed_hours,
                    deadline
                )
                VALUES (%s, %s, %s, %s, %s);
                """,
                (
                    cle_data["attorney_id"],
                    cle_data["jurisdiction"],
                    cle_data["required_hours"],
                    cle_data["completed_hours"],
                    cle_data["deadline"],
                ),
            )

        conn.commit()

    except Exception:
        conn.rollback()
        raise

    finally:
        conn.close()


def create_matter(matter_data: dict) -> None:
    """
    Insert a new matter record into PostgreSQL.
    """
    conn = get_connection()

    try:
        with conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO matters (
                    matter_id,
                    matter_name,
                    jurisdiction,
                    client,
                    revenue,
                    matter_type,
                    status
                )
                VALUES (%s, %s, %s, %s, %s, %s, %s);
                """,
                (
                    matter_data["matter_id"],
                    matter_data["matter_name"],
                    matter_data["jurisdiction"],
                    matter_data["client"],
                    matter_data["revenue"],
                    matter_data["matter_type"],
                    matter_data["status"],
                ),
            )

        conn.commit()

    except Exception:
        conn.rollback()
        raise

    finally:
        conn.close()


def create_matter_assignment(assignment_data: dict) -> None:
    """
    Insert a new matter assignment record into PostgreSQL.
    """
    conn = get_connection()

    try:
        with conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO matter_assignments (
                    matter_id,
                    attorney_id,
                    role,
                    assignment_date
                )
                VALUES (%s, %s, %s, %s);
                """,
                (
                    assignment_data["matter_id"],
                    assignment_data["attorney_id"],
                    assignment_data["role"],
                    assignment_data["assignment_date"],
                ),
            )

        conn.commit()

    except Exception:
        conn.rollback()
        raise

    finally:
        conn.close()