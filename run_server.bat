@echo off
echo Starting Credit Risk System using .venv...
.venv\Scripts\python.exe -m uvicorn src.api.main:app --reload
pause
