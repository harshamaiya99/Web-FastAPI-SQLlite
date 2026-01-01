from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
import sqlite3
import os

app = FastAPI()

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
templates = Jinja2Templates(directory=os.path.join(BASE_DIR, "frontend"))

# Database
conn = sqlite3.connect(os.path.join(BASE_DIR, "database.db"), check_same_thread=False)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS accounts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    email TEXT
)
""")
conn.commit()


class Account(BaseModel):
    name: str
    email: str


class AccountUpdate(BaseModel):
    name: str
    email: str


@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


# CREATE
@app.post("/accounts")
def create_account(account: Account):
    cursor.execute(
        "INSERT INTO accounts (name, email) VALUES (?, ?)",
        (account.name, account.email)
    )
    conn.commit()
    return {"message": "Account created successfully"}


# READ
@app.get("/accounts")
def get_accounts():
    cursor.execute("SELECT * FROM accounts")
    rows = cursor.fetchall()
    return [
        {"id": r[0], "name": r[1], "email": r[2]}
        for r in rows
    ]


# UPDATE
@app.put("/accounts/{account_id}")
def update_account(account_id: int, account: AccountUpdate):
    cursor.execute(
        "UPDATE accounts SET name=?, email=? WHERE id=?",
        (account.name, account.email, account_id)
    )
    conn.commit()
    return {"message": "Account updated successfully"}


# DELETE
@app.delete("/accounts/{account_id}")
def delete_account(account_id: int):
    cursor.execute("DELETE FROM accounts WHERE id=?", (account_id,))
    conn.commit()
    return {"message": "Account deleted successfully"}
