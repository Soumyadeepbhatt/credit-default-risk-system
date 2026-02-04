from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from .routes import router as api_router
from ..db.database import engine, Base
import os

# Create DB Tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Credit Default Risk System")

# Mount API
app.include_router(api_router, prefix="/api")

# Frontend Templates
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
template_dir = os.path.join(base_dir, "frontend", "templates")
templates = Jinja2Templates(directory=template_dir)

@app.get("/")
def dashboard(request: Request):
    return templates.TemplateResponse("dashboard.html", {"request": request})

@app.get("/application")
def application_form(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/login")
def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@app.get("/register")
def register_page(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})
