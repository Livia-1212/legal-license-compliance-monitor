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


def get_eligible_cle_attorneys() -> list[dict]:
    """
    Return attorneys who are eligible for CLE record entry.

    An attorney is eligible when:
    - the attorney is actively employed;
    - the attorney has an active license;
    - the license registration expiry date has not passed;
    - the jurisdiction has a configured CLE rule.
    """
    conn = get_connection()

    try:
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT
                    a.attorney_id,
                    a.name,
                    a.email,
                    a.office,
                    a.practice_area,
                    a.employment_status,
                    l.license_id,
                    l.jurisdiction,
                    l.admission_date,
                    l.admission_year,
                    l.license_status,
                    l.registration_expiry,
                    jr.cle_required_hours,
                    jr.registration_cycle
                FROM attorneys AS a
                INNER JOIN licenses AS l
                    ON a.attorney_id = l.attorney_id
                INNER JOIN jurisdiction_rules AS jr
                    ON l.jurisdiction = jr.jurisdiction
                WHERE a.employment_status = 'Active'
                  AND l.license_status = 'Active'
                  AND l.registration_expiry >= CURRENT_DATE
                ORDER BY a.name, l.jurisdiction;
                """
            )

            column_names = [description[0] for description in cur.description]
            rows = cur.fetchall()

            return [
                dict(zip(column_names, row))
                for row in rows
            ]

    finally:
        conn.close()


def get_unassigned_open_matters() -> list[dict]:
    """
    Return open matters that do not yet have an attorney assignment.
    """
    conn = get_connection()

    try:
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT
                    m.matter_id,
                    m.matter_name,
                    m.jurisdiction,
                    m.client,
                    m.revenue,
                    m.matter_type,
                    m.status
                FROM matters AS m
                WHERE LOWER(m.status) = 'open'
                  AND NOT EXISTS (
                      SELECT 1
                      FROM matter_assignments AS ma
                      WHERE ma.matter_id = m.matter_id
                  )
                ORDER BY m.matter_id;
                """
            )

            column_names = [
                description[0]
                for description in cur.description
            ]

            return [
                dict(zip(column_names, row))
                for row in cur.fetchall()
            ]

    finally:
        conn.close()


def get_eligible_attorneys_for_matter(jurisdiction: str) -> list[dict]:
    """
    Return actively employed attorneys with an active, unexpired license
    matching the selected matter's jurisdiction.
    """
    conn = get_connection()

    try:
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT DISTINCT
                    a.attorney_id,
                    a.name,
                    a.email,
                    a.office,
                    a.practice_area,
                    a.employment_status,
                    l.jurisdiction,
                    l.license_status,
                    l.registration_expiry
                FROM attorneys AS a
                INNER JOIN licenses AS l
                    ON a.attorney_id = l.attorney_id
                WHERE a.employment_status = 'Active'
                  AND l.license_status = 'Active'
                  AND l.registration_expiry >= CURRENT_DATE
                  AND UPPER(l.jurisdiction) = UPPER(%s)
                ORDER BY a.name, a.attorney_id;
                """,
                (jurisdiction,),
            )

            column_names = [
                description[0]
                for description in cur.description
            ]

            return [
                dict(zip(column_names, row))
                for row in cur.fetchall()
            ]

    finally:
        conn.close()


def load_matter_directory_with_assignments() -> pd.DataFrame:
    """
    Load matters with their assigned attorney information.

    Unassigned matters return null attorney fields, which the dashboard
    can display as N/A.
    """
    conn = get_connection()

    try:
        query = """
            SELECT
                m.matter_id,
                m.matter_name,
                m.jurisdiction,
                m.client,
                m.revenue,
                m.matter_type,
                m.status,
                a.name AS assigned_attorney,
                ma.attorney_id AS assigned_attorney_id,
                ma.role AS assignment_role,
                ma.assignment_date
            FROM matters AS m
            LEFT JOIN matter_assignments AS ma
                ON m.matter_id = ma.matter_id
            LEFT JOIN attorneys AS a
                ON ma.attorney_id = a.attorney_id
            ORDER BY m.matter_id;
        """

        matter_directory = pd.read_sql_query(query, conn)

        matter_directory["assigned_attorney"] = (
            matter_directory["assigned_attorney"].fillna("N/A")
        )

        matter_directory["assigned_attorney_id"] = (
            matter_directory["assigned_attorney_id"]
            .astype("Int64")
            .astype("string")
            .fillna("N/A")
        )

        matter_directory["assignment_role"] = (
            matter_directory["assignment_role"].fillna("N/A")
        )

        return matter_directory

    finally:
        conn.close()


def create_attorney(attorney_data: dict) -> None:
    """
    Insert a new attorney record into PostgreSQL.
    Attorney ID is auto-generated by PostgreSQL.
    """
    conn = get_connection()

    try:
        with conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO attorneys (
                    name,
                    email,
                    date_of_birth,
                    title,
                    office,
                    practice_area,
                    employment_status
                )
                VALUES (%s, %s, %s, %s, %s, %s, %s);
                """,
                (
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