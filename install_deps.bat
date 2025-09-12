@echo off
echo Installing Python dependencies...
py -m pip install fastapi
py -m pip install uvicorn
py -m pip install jinja2
py -m pip install python-multipart
py -m pip install python-dotenv
py -m pip install sendgrid
echo Installation complete!
pause
