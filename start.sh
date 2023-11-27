#!/bin/bash

# Запуск сервера и ожидание его завершения
uvicorn main:app --host 0.0.0.0 --port 8000 --ssl-keyfile /app/ssl/privkey.pem --ssl-certfile /app/ssl/fullchain.pem &
UVICORN_PID=$!

# Подождать, пока сервер полностью запустится (например, 5 секунд)
sleep 5

# Запуск bot.py
python bot.py &
BOT_PID=$!

# Запуск database.py
python database.py
DATABASE_PID=$!

# Ожидание завершения всех процессов
wait $UVICORN_PID
wait $BOT_PID
wait $DATABASE_PID
