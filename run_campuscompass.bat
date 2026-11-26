@echo off
title CampusCompass Server
cd /d "%~dp0"
echo Starting CampusCompass on http://localhost:8000 ...
python server.py
pause
