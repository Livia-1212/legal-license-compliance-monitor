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
