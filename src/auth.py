from datetime import datetime
import binascii
import csv
import hashlib
import hmac
import os
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data" / "raw"
DATA_DIR.mkdir(parents=True, exist_ok=True)
USERS_FILE = DATA_DIR / "users.csv"
USER_FIELDS = ["username", "password_hash", "role", "created_at"]

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
        return hmac.compare_digest(dk, expected)
    except Exception:
        return False


def _public_user(row: dict) -> dict:
    return {
        "username": row.get("username", ""),
        "role": row.get("role") or "user",
        "created_at": row.get("created_at"),
    }


def init_user_store():
    """Create a basic users file with a default admin user if it doesn't exist."""
    if not USERS_FILE.exists():
        USERS_FILE.parent.mkdir(parents=True, exist_ok=True)
        with USERS_FILE.open("w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=USER_FIELDS)
            writer.writeheader()
            admin_pw = _hash_password("admin")
            writer.writerow({"username": "admin", "password_hash": admin_pw, "role": "admin", "created_at": datetime.now().isoformat()})


def load_users() -> list[dict]:
    """Load stored users, including password hashes for internal auth checks."""
    init_user_store()
    users = []
    with USERS_FILE.open("r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            users.append(row)
    return users


def save_users(users: list[dict]) -> None:
    """Persist user records to the local development CSV store."""
    USERS_FILE.parent.mkdir(parents=True, exist_ok=True)
    with USERS_FILE.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=USER_FIELDS)
        writer.writeheader()
        for user in users:
            writer.writerow({field: user.get(field, "") for field in USER_FIELDS})


def user_exists(username: str) -> bool:
    username = username.strip()
    return any(row.get("username") == username for row in load_users())


def register_user(username: str, password: str, role: str = "user") -> tuple[bool, str]:
    """Create a new user. Returns (success, message)."""
    username = username.strip()

    if not username:
        return False, "Username must not be empty."
    if not password:
        return False, "Password must not be empty."
    if len(password) <= 8:
        return False, "Password must be more than 8 characters."
    if user_exists(username):
        return False, "This username is already being used. Please choose another username."

    pw_hash = _hash_password(password)
    users = load_users()
    users.append(
        {
            "username": username,
            "password_hash": pw_hash,
            "role": role or "user",
            "created_at": datetime.now().isoformat(),
        }
    )
    save_users(users)

    return True, "Registration successful. Please sign in."


def authenticate_user(username: str, password: str) -> dict | None:
    """Authenticate a user and return a dict with username and role, or None."""
    username = username.strip()
    for row in load_users():
        if row.get("username") == username and _verify_password(row.get("password_hash", ""), password):
            return _public_user(row)
    return None


def logout_user() -> None:
    """Clear Streamlit authentication state and return to the public home page."""
    import streamlit as st

    st.session_state["authenticated"] = False
    st.session_state["username"] = None
    st.session_state["role"] = "anonymous"
    st.session_state["current_user"] = None
    st.session_state["page"] = "Executive Summary"


def create_user(username: str, password: str, role: str = "user") -> tuple[bool, str]:
    """Backward-compatible alias for older app code."""
    return register_user(username, password, role)


def authenticate(username: str, password: str) -> dict | None:
    """Backward-compatible alias for older app code."""
    return authenticate_user(username, password)


def list_users() -> list[dict]:
    return [_public_user(row) for row in load_users()]
