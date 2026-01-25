import sqlite3
import os
from passlib.context import CryptContext
from dotenv import load_dotenv

# Load environment variables from .env file (looks in root or current dir)
load_dotenv()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "database.db")

# Setup hashing for seeding (creating default users)
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_connection():
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    # --- 1. Accounts Table ---
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS accounts (
        account_id TEXT PRIMARY KEY,
        account_holder_name TEXT NOT NULL,
        dob TEXT NOT NULL,
        gender TEXT NOT NULL,
        email TEXT NOT NULL,
        phone TEXT NOT NULL,
        address TEXT NOT NULL,
        zip_code TEXT NOT NULL,
        account_type TEXT NOT NULL,
        balance REAL NOT NULL DEFAULT 0.0,
        date_opened TEXT NOT NULL,
        status TEXT NOT NULL DEFAULT 'Active',
        services TEXT,
        marketing_opt_in BOOLEAN NOT NULL DEFAULT 0,
        agreed_to_terms BOOLEAN NOT NULL DEFAULT 0
    )
    """)

    # --- 2. Users Table ---
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        username TEXT PRIMARY KEY,
        hashed_password TEXT NOT NULL,
        role TEXT NOT NULL
    )
    """)

    # --- 3. Seed Default Users ---
    # Fetch Credentials from .env
    clerk_user = os.getenv("CLERK_USERNAME")
    clerk_pass = os.getenv("CLERK_PASSWORD")

    manager_user = os.getenv("MANAGER_USERNAME")
    manager_pass = os.getenv("MANAGER_PASSWORD")

    # Hash passwords
    clerk_hash = pwd_context.hash(clerk_pass)
    manager_hash = pwd_context.hash(manager_pass)

    # Insert Users
    cursor.execute("INSERT OR IGNORE INTO users (username, hashed_password, role) VALUES (?, ?, ?)",
                   (clerk_user, clerk_hash, "clerk"))

    cursor.execute("INSERT OR IGNORE INTO users (username, hashed_password, role) VALUES (?, ?, ?)",
                   (manager_user, manager_hash, "manager"))

    conn.commit()
    conn.close()
    print("Database initialized successfully.")


if __name__ == "__main__":
    init_db()