"""
Legacy CSV upload persistence helper.

This module supports the current CSV-backed upload workflow used by streamlit_app.py.
Phase 8 introduces PostgreSQL persistence under src/db/.

Do not add new database logic here.
"""

from pathlib import Path
from datetime import datetime
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = ROOT / "data" / "raw"
BACKUP_DIR = ROOT / "data" / "backups"
BACKUP_DIR.mkdir(parents=True, exist_ok=True)
AUDIT_FILE = BACKUP_DIR / "upload_audit.csv"

# Expected columns for simple validation. Adjust as needed.
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
        "license_status",
        "registration_expiry",
        "license_number",
    ],
    "cle_records": [
        "attorney_id",
        "jurisdiction",
        "required_hours",
        "completed_hours",
        "deadline",
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


def _path_for_dataset(dataset_name: str) -> Path:
    return DATA_DIR / f"{dataset_name}.csv"


def _backup_file(path: Path) -> None:
    if path.exists():
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        dest = BACKUP_DIR / f"{path.stem}_{ts}.csv"
        path.replace(dest)


def validate_dataframe(df: pd.DataFrame, dataset_name: str) -> tuple[bool, str]:
    """Validate uploaded dataframe columns against expected columns for dataset.

    Returns (is_valid, message).
    """
    expected = EXPECTED_COLUMNS.get(dataset_name)
    if expected is None:
        return False, f"Unknown dataset: {dataset_name}"

    missing = [c for c in expected if c not in df.columns]
    if missing:
        return False, f"Missing required columns: {missing}"

    return True, "OK"


def save_uploaded_csv(uploaded_file, dataset_name: str, mode: str = "replace", uploader: str | None = None) -> tuple[bool, str]:
    """Save an uploaded CSV file to the data/raw folder.

    uploaded_file: Streamlit UploadedFile or file-like
    dataset_name: one of the keys in EXPECTED_COLUMNS (without .csv)
    mode: 'replace' or 'append'

    Returns (success, message)
    """
    target = _path_for_dataset(dataset_name)

    try:
        df = pd.read_csv(uploaded_file)
    except Exception as e:
        return False, f"Unable to read uploaded CSV: {e}"

    valid, msg = validate_dataframe(df, dataset_name)
    if not valid:
        return False, msg

    # Ensure directory exists
    DATA_DIR.mkdir(parents=True, exist_ok=True)

    if mode == "replace":
        # backup existing file if present
        if target.exists():
            _backup_file(target)
        try:
            df.to_csv(target, index=False)
        except Exception as e:
            return False, f"Failed to write CSV: {e}"

    elif mode == "append":
        # append to existing dataset, deduplicate by common id where possible
        if target.exists():
            try:
                existing = pd.read_csv(target)
                combined = pd.concat([existing, df], ignore_index=True)
                combined.drop_duplicates(inplace=True)
                _backup_file(target)
                combined.to_csv(target, index=False)
            except Exception as e:
                return False, f"Failed to append CSV: {e}"
        else:
            try:
                df.to_csv(target, index=False)
            except Exception as e:
                return False, f"Failed to write CSV: {e}"

    else:
        return False, f"Unknown mode: {mode}"

    # record audit event
    try:
        audit_row = {
            "timestamp": datetime.now().isoformat(),
            "dataset": dataset_name,
            "uploader": uploader or "",
            "mode": mode,
            "rows": int(len(df)) if hasattr(df, "__len__") else None,
            "filename": target.name,
        }

        # write header if file doesn't exist
        if not AUDIT_FILE.exists():
            import csv

            with AUDIT_FILE.open("w", newline="", encoding="utf-8") as f:
                writer = csv.DictWriter(f, fieldnames=list(audit_row.keys()))
                writer.writeheader()
                writer.writerow(audit_row)
        else:
            import csv

            with AUDIT_FILE.open("a", newline="", encoding="utf-8") as f:
                writer = csv.DictWriter(f, fieldnames=list(audit_row.keys()))
                writer.writerow(audit_row)
    except Exception:
        # don't fail the main upload if audit logging errors
        pass

    return True, "Saved"
