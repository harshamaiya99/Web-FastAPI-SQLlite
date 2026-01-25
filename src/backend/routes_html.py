from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import os

router = APIRouter(tags=["frontend"])

# Setup Templates (Path is relative to this file)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FRONTEND_DIR = os.path.join(BASE_DIR, "frontend")
templates = Jinja2Templates(directory=FRONTEND_DIR)

@router.get("/login.html", response_class=HTMLResponse)
def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@router.get("/home_page.html", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("home_page.html", {"request": request})

@router.get("/accountDetails.html", response_class=HTMLResponse)
def account_details_page(request: Request):
    return templates.TemplateResponse("accountDetails.html", {"request": request})

@router.get("/createAccount.html", response_class=HTMLResponse)
def create_account_page(request: Request):
    return templates.TemplateResponse("createAccount.html", {"request": request})