"""SQLite persistence for sourced government scheme records."""
import sqlite3
from contextlib import contextmanager
from pathlib import Path

DEFAULT_DB = Path(__file__).resolve().parents[1] / "schemes.db"


@contextmanager
def connect(db_path=DEFAULT_DB):
    connection = sqlite3.connect(str(db_path))
    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA foreign_keys = ON")
    try:
        with connection:
            yield connection
    finally:
        connection.close()


def initialize(db_path=DEFAULT_DB):
    with connect(db_path) as db:
        db.execute("""CREATE TABLE IF NOT EXISTS schemes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            department TEXT NOT NULL,
            jurisdiction TEXT NOT NULL,
            category TEXT NOT NULL,
            summary TEXT NOT NULL,
            eligibility TEXT NOT NULL,
            documents TEXT NOT NULL,
            application_steps TEXT NOT NULL,
            official_url TEXT NOT NULL,
            verified_on TEXT NOT NULL,
            min_age INTEGER,
            max_age INTEGER,
            max_income REAL,
            state TEXT,
            occupation TEXT,
            active INTEGER NOT NULL DEFAULT 1,
            created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
        )""")


def list_schemes(db_path=DEFAULT_DB, include_inactive=False):
    with connect(db_path) as db:
        query = "SELECT * FROM schemes"
        if not include_inactive:
            query += " WHERE active = 1"
        query += " ORDER BY name COLLATE NOCASE"
        return [dict(row) for row in db.execute(query)]


def save_scheme(data, db_path=DEFAULT_DB, scheme_id=None):
    fields = ["name", "department", "jurisdiction", "category", "summary", "eligibility",
              "documents", "application_steps", "official_url", "verified_on", "min_age",
              "max_age", "max_income", "state", "occupation", "active"]
    values = [data.get(field) for field in fields]
    with connect(db_path) as db:
        if scheme_id is None:
            marks = ",".join("?" for _ in fields)
            cursor = db.execute(f"INSERT INTO schemes ({','.join(fields)}) VALUES ({marks})", values)
            return cursor.lastrowid
        assignments = ",".join(f"{field} = ?" for field in fields)
        db.execute(f"UPDATE schemes SET {assignments} WHERE id = ?", values + [scheme_id])
        return scheme_id


def set_active(scheme_id, active, db_path=DEFAULT_DB):
    with connect(db_path) as db:
        db.execute("UPDATE schemes SET active = ? WHERE id = ?", (int(active), scheme_id))


def match_profile(scheme, profile):
    """Return (match, reasons); blank profile attributes remain unknown, not failures."""
    reasons = []
    for key, label in (("age", "age"), ("annual_income", "annual income"), ("state", "state"), ("occupation", "occupation")):
        value = profile.get(key)
        if value in (None, ""):
            continue
        if key == "age":
            if scheme.get("min_age") is not None and value < scheme["min_age"]:
                reasons.append(f"Age is below the listed minimum ({scheme['min_age']}).")
            if scheme.get("max_age") is not None and value > scheme["max_age"]:
                reasons.append(f"Age is above the listed maximum ({scheme['max_age']}).")
        elif key == "annual_income" and scheme.get("max_income") is not None and value > scheme["max_income"]:
            reasons.append(f"Income is above the listed limit (₹{scheme['max_income']:,.0f}).")
        elif key in ("state", "occupation") and scheme.get(key) and value.casefold() != scheme[key].casefold():
            reasons.append(f"{label.title()} does not match the listed value ({scheme[key]}).")
    return not reasons, reasons

