from pathlib import Path
from datetime import datetime
import os
import hashlib
import binascii
import csv

ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = ROOT / "data" / "raw"
DATA_DIR.mkdir(parents=True, exist_ok=True)
USERS_FILE = DATA_DIR / "users.csv"

# PBKDF2 params
_ITERATIONS = 100_000
_SALT_BYTES = 16


def _hash_password(password: str, salt: bytes | None = None) -> str:
    if salt is None:
        salt = os.urandom(_SALT_BYTES)
    dk = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt, _ITERATIONS)
    return f"{binascii.hexlify(salt).decode()}${binascii.hexlify(dk).decode()}"


def _verify_password(stored: str, password: str) -> bool:
    try:
        salt_hex, hash_hex = stored.split("$")
        salt = binascii.unhexlify(salt_hex)
        expected = binascii.unhexlify(hash_hex)
        dk = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt, _ITERATIONS)
        return hashlib.compare_digest(dk, expected)
    except Exception:
        return False


def init_user_store():
    """Create a basic users file with a default admin user if it doesn't exist."""
    if not USERS_FILE.exists():
        USERS_FILE.parent.mkdir(parents=True, exist_ok=True)
        with USERS_FILE.open("w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=["username", "password_hash", "role", "created_at"])
            writer.writeheader()
            admin_pw = _hash_password("admin")
            writer.writerow({"username": "admin", "password_hash": admin_pw, "role": "admin", "created_at": datetime.now().isoformat()})


def create_user(username: str, password: str, role: str = "user") -> tuple[bool, str]:
    """Create a new user. Returns (success, message)."""
    init_user_store()
    users = {}
    with USERS_FILE.open("r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            users[row["username"]] = row

    if username in users:
        return False, "User already exists"

    pw_hash = _hash_password(password)
    with USERS_FILE.open("a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["username", "password_hash", "role", "created_at"])
        writer.writerow({"username": username, "password_hash": pw_hash, "role": role, "created_at": datetime.now().isoformat()})

    return True, "User created"


def authenticate(username: str, password: str) -> dict | None:
    """Authenticate a user and return a dict with username and role, or None."""
    init_user_store()
    with USERS_FILE.open("r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row["username"] == username:
                if _verify_password(row["password_hash"], password):
                    return {"username": username, "role": row.get("role", "user")}
                else:
                    return None
    return None


def list_users() -> list[dict]:
    init_user_store()
    out = []
    with USERS_FILE.open("r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            out.append({"username": row["username"], "role": row.get("role", "user"), "created_at": row.get("created_at")})
    return out
