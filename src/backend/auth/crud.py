from typing import Optional
from database import get_connection
from auth.schemas import UserInDB

def get_user_by_username(username: str) -> Optional[UserInDB]:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username=?", (username,))
    row = cursor.fetchone()
    conn.close()

    if row:
        return UserInDB(**dict(row))
    return None