import os

import pandas as pd
from dotenv import load_dotenv

from src.analysis.load_data import load_all_data
from src.db.repositories import load_all_data_from_db


load_dotenv()


def get_data_source() -> str:
    """
    Return the configured data source.

    Supported values:
    - csv
    - postgres
    """
    return os.getenv("DATA_SOURCE", "csv").lower().strip()


def load_application_data() -> dict[str, pd.DataFrame]:
    """
    Load application data from the configured data source.

    Defaults to CSV for backward compatibility.
    Set DATA_SOURCE=postgres in .env to load from PostgreSQL.
    """
    data_source = get_data_source()

    if data_source == "postgres":
        return load_all_data_from_db()

    if data_source == "csv":
        return load_all_data()

    raise ValueError(
        f"Unsupported DATA_SOURCE: {data_source}. "
        "Expected 'csv' or 'postgres'."
    )
