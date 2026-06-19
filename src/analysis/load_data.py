from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = ROOT / "data" / "raw"


def load_csv(file_name: str) -> pd.DataFrame:
    path = DATA_DIR / file_name
    if not path.exists():
        raise FileNotFoundError(f"Missing file: {path}")
    return pd.read_csv(path)


def load_all_data() -> dict[str, pd.DataFrame]:
    return {
        "attorneys": load_csv("attorneys.csv"),
        "licenses": load_csv("licenses.csv"),
        "cle_records": load_csv("cle_records.csv"),
        "jurisdiction_rules": load_csv("jurisdiction_rules.csv"),
        "matters": load_csv("matters.csv"),
        "matter_assignments": load_csv("matter_assignments.csv"),
    }


if __name__ == "__main__":
    data = load_all_data()
    for name, df in data.items():
        print(f"{name}: {df.shape[0]} rows, {df.shape[1]} columns")