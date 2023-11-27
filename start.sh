#!/bin/bash
uvicorn main:app --host 0.0.0.0 --port 8000 --ssl-keyfile /app/ssl/privkey.pem --ssl-certfile /app/ssl/fullchain.pem &
python bot.py
