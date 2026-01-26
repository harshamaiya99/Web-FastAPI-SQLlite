import json
import sqlite3
from typing import Optional, Dict, Any
from database import get_connection


def delete_expired_keys():
    """
    Deletes any keys older than 24 hours using SQLite native time functions.
    """
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM idempotency_keys WHERE created_at < datetime('now', '-24 hours')")
    conn.commit()
    conn.close()


def get_idempotency_key(key: str) -> Optional[Dict[str, Any]]:
    """
    Fetches the response ONLY if the key exists AND is fresh (created within last 24h).
    """
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT response_json 
        FROM idempotency_keys 
        WHERE key=? 
          AND created_at > datetime('now', '-24 hours')
    """, (key,))

    row = cursor.fetchone()
    conn.close()

    if row:
        return json.loads(row["response_json"])
    return None


def save_idempotency_key(key: str, response_data: Dict[str, Any]) -> None:
    """
    Saves a response to the database and cleans up old keys.
    """
    # 1. Clean up old keys first
    delete_expired_keys()

    # 2. Insert/Replace the new key
    conn = get_connection()
    cursor = conn.cursor()

    response_json = json.dumps(response_data)

    try:
        cursor.execute(
            "INSERT OR REPLACE INTO idempotency_keys (key, response_json, created_at) VALUES (?, ?, datetime('now'))",
            (key, response_json)
        )
        conn.commit()
    except sqlite3.Error as e:
        print(f"Error saving idempotency key: {e}")
    finally:
        conn.close()