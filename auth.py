"""Authentication and user persistence for the ACORD service.

The original deployment kept this module outside version control.  This
replacement deliberately uses only the Python standard library so a fresh
host can reproduce the service without an opaque auth dependency.
"""

from __future__ import annotations

import base64
import hashlib
import hmac
import json
import os
import secrets
import sqlite3
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


BASE_DIR = Path(__file__).resolve().parent
DB_PATH = Path(os.getenv("ACORD_DB_PATH", BASE_DIR / "data" / "telemetry.db"))
TOKEN_TTL_SECONDS = int(os.getenv("ACORD_TOKEN_TTL_SECONDS", str(7 * 24 * 60 * 60)))
PBKDF2_ITERATIONS = 310_000


def _connect() -> sqlite3.Connection:
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_PATH, timeout=15)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    conn.execute("PRAGMA journal_mode = WAL")
    conn.execute("PRAGMA busy_timeout = 15000")
    return conn


def init_users_db() -> None:
    with _connect() as db:
        db.executescript(
            """
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL UNIQUE COLLATE NOCASE,
                password_hash TEXT NOT NULL,
                email TEXT DEFAULT '',
                display_name TEXT DEFAULT '',
                is_admin INTEGER NOT NULL DEFAULT 0,
                is_active INTEGER NOT NULL DEFAULT 1,
                agency_profile TEXT NOT NULL DEFAULT '{}',
                created_at TEXT NOT NULL,
                last_login TEXT
            );
            CREATE INDEX IF NOT EXISTS idx_users_username ON users(username);
            """
        )


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _password_hash(password: str) -> str:
    salt = secrets.token_bytes(16)
    digest = hashlib.pbkdf2_hmac(
        "sha256", password.encode("utf-8"), salt, PBKDF2_ITERATIONS
    )
    return "pbkdf2_sha256${}${}${}".format(
        PBKDF2_ITERATIONS,
        base64.urlsafe_b64encode(salt).decode("ascii").rstrip("="),
        base64.urlsafe_b64encode(digest).decode("ascii").rstrip("="),
    )


def _password_matches(password: str, encoded: str) -> bool:
    try:
        algorithm, iterations, salt_text, expected_text = encoded.split("$", 3)
        if algorithm != "pbkdf2_sha256":
            return False
        salt = _b64decode(salt_text)
        expected = _b64decode(expected_text)
        actual = hashlib.pbkdf2_hmac(
            "sha256", password.encode("utf-8"), salt, int(iterations)
        )
        return hmac.compare_digest(actual, expected)
    except (TypeError, ValueError):
        return False


def _b64encode(data: bytes) -> str:
    return base64.urlsafe_b64encode(data).decode("ascii").rstrip("=")


def _b64decode(data: str) -> bytes:
    return base64.urlsafe_b64decode(data + "=" * (-len(data) % 4))


def _token_secret() -> bytes:
    secret = os.getenv("ACORD_JWT_SECRET", "")
    if len(secret) < 32:
        raise RuntimeError("ACORD_JWT_SECRET must be at least 32 characters")
    return secret.encode("utf-8")


def _issue_token(user_id: int) -> str:
    now = int(time.time())
    header = _b64encode(json.dumps({"alg": "HS256", "typ": "JWT"}, separators=(",", ":")).encode())
    payload = _b64encode(
        json.dumps(
            {"sub": str(user_id), "iat": now, "exp": now + TOKEN_TTL_SECONDS},
            separators=(",", ":"),
        ).encode()
    )
    signing_input = f"{header}.{payload}".encode("ascii")
    signature = _b64encode(hmac.new(_token_secret(), signing_input, hashlib.sha256).digest())
    return f"{header}.{payload}.{signature}"


def decode_token(token: str) -> dict[str, Any] | None:
    try:
        header, payload, supplied_signature = token.split(".", 2)
        signing_input = f"{header}.{payload}".encode("ascii")
        expected_signature = _b64encode(
            hmac.new(_token_secret(), signing_input, hashlib.sha256).digest()
        )
        if not hmac.compare_digest(expected_signature, supplied_signature):
            return None
        decoded = json.loads(_b64decode(payload))
        if int(decoded.get("exp", 0)) <= int(time.time()):
            return None
        return decoded
    except (RuntimeError, ValueError, json.JSONDecodeError):
        return None


def _public_user(row: sqlite3.Row | None) -> dict[str, Any] | None:
    if not row:
        return None
    user = dict(row)
    user.pop("password_hash", None)
    user["is_admin"] = bool(user.get("is_admin"))
    user["is_active"] = bool(user.get("is_active"))
    try:
        user["agency_profile"] = json.loads(user.get("agency_profile") or "{}")
    except json.JSONDecodeError:
        user["agency_profile"] = {}
    return user


def create_user(
    username: str,
    password: str,
    email: str = "",
    display_name: str = "",
    is_admin: bool = False,
) -> dict[str, Any]:
    username = username.strip()
    if not username or len(password) < 10:
        raise ValueError("Username and a password of at least 10 characters are required")
    try:
        with _connect() as db:
            cursor = db.execute(
                """
                INSERT INTO users
                    (username, password_hash, email, display_name, is_admin, created_at)
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (
                    username,
                    _password_hash(password),
                    email.strip(),
                    display_name.strip(),
                    1 if is_admin else 0,
                    _now(),
                ),
            )
            row = db.execute("SELECT * FROM users WHERE id = ?", (cursor.lastrowid,)).fetchone()
        return _public_user(row) or {}
    except sqlite3.IntegrityError as exc:
        raise ValueError("Username already exists") from exc


def get_user(identifier: str | int) -> dict[str, Any] | None:
    with _connect() as db:
        if str(identifier).isdigit():
            row = db.execute("SELECT * FROM users WHERE id = ?", (int(identifier),)).fetchone()
        else:
            row = db.execute("SELECT * FROM users WHERE username = ?", (str(identifier),)).fetchone()
    return _public_user(row)


def login_user(username: str, password: str) -> dict[str, Any] | None:
    with _connect() as db:
        row = db.execute("SELECT * FROM users WHERE username = ?", (username.strip(),)).fetchone()
        if not row or not row["is_active"] or not _password_matches(password, row["password_hash"]):
            return None
        db.execute("UPDATE users SET last_login = ? WHERE id = ?", (_now(), row["id"]))
        updated = db.execute("SELECT * FROM users WHERE id = ?", (row["id"],)).fetchone()
    return {"token": _issue_token(row["id"]), "user": _public_user(updated)}


def update_user_profile(user_id: str | int, **fields: str) -> None:
    allowed = {key: value.strip() for key, value in fields.items() if key in {"email", "display_name"}}
    if not allowed:
        return
    assignments = ", ".join(f"{key} = ?" for key in allowed)
    with _connect() as db:
        db.execute(
            f"UPDATE users SET {assignments} WHERE id = ?",
            (*allowed.values(), int(user_id)),
        )


def update_agency_profile(user_id: str | int, profile: dict[str, Any]) -> None:
    with _connect() as db:
        db.execute(
            "UPDATE users SET agency_profile = ? WHERE id = ?",
            (json.dumps(profile, separators=(",", ":")), int(user_id)),
        )


def change_password(user_id: str | int, old_password: str, new_password: str) -> bool:
    with _connect() as db:
        row = db.execute("SELECT password_hash FROM users WHERE id = ?", (int(user_id),)).fetchone()
        if not row or not _password_matches(old_password, row["password_hash"]):
            return False
        db.execute(
            "UPDATE users SET password_hash = ? WHERE id = ?",
            (_password_hash(new_password), int(user_id)),
        )
    return True


def admin_list_users() -> list[dict[str, Any]]:
    with _connect() as db:
        rows = db.execute(
            """
            SELECT u.*,
                   COUNT(g.id) AS generation_count
            FROM users u
            LEFT JOIN generations g ON CAST(g.user_id AS TEXT) = CAST(u.id AS TEXT)
            GROUP BY u.id
            ORDER BY u.created_at DESC
            """
        ).fetchall()
    return [_public_user(row) or {} for row in rows]


def admin_reset_password(user_id: str | int, new_password: str) -> None:
    with _connect() as db:
        db.execute(
            "UPDATE users SET password_hash = ? WHERE id = ?",
            (_password_hash(new_password), int(user_id)),
        )


def _toggle(user_id: str | int, column: str) -> None:
    with _connect() as db:
        db.execute(
            f"UPDATE users SET {column} = CASE WHEN {column} = 1 THEN 0 ELSE 1 END WHERE id = ?",
            (int(user_id),),
        )


def admin_toggle_active(user_id: str | int) -> None:
    _toggle(user_id, "is_active")


def admin_toggle_admin(user_id: str | int) -> None:
    _toggle(user_id, "is_admin")


def get_user_certificates(user_id: str | int) -> list[dict[str, Any]]:
    with _connect() as db:
        rows = db.execute(
            """
            SELECT id, timestamp, form_type, insured_name, carrier, cert_holder_name,
                   policy_number, coverages, output_size_bytes, fields_filled, fields_total
            FROM generations
            WHERE CAST(user_id AS TEXT) = ?
            ORDER BY timestamp DESC
            LIMIT 250
            """,
            (str(user_id),),
        ).fetchall()
    result = []
    for row in rows:
        item = dict(row)
        try:
            item["coverages"] = json.loads(item.get("coverages") or "[]")
        except json.JSONDecodeError:
            item["coverages"] = []
        result.append(item)
    return result
