@echo off
:start
ngrok http 80
timeout /t 3600
goto start
