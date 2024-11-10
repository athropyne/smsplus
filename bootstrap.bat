set PROJECT_PATH = C:\work\smsplus\src\services
set API_PATH = %PROJECT_PATH%\api\starter.py
set BOT_PATH = %PROJECT_PATH%\bot.main.py

cd %PROJECT_PATH%\API\
call venv\scripts\activate
start python %API_PATH%

cd %PROJECT_PATH%\API\
call venv\scripts\activate
start celery -A celery_app.worker worker --loglevel=info --pool=solo

cd %PROJECT_PATH%\bot\
call venv\scripts\activate
start python %BOT_PATH%