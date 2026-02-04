@echo off
echo Installing dependencies...
pip install -r requirements.txt
echo.
echo Starting Credit Risk System...
uvicorn src.api.main:app --reload
pause
