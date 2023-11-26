# Используем базовый образ Python Slim
FROM python:3.11-slim

# Устанавливаем переменные окружения
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем зависимости
COPY pyproject.toml poetry.lock /app/

# Устанавливаем зависимости
RUN apt-get update && apt-get install -y build-essential
RUN pip install --no-cache-dir poetry
RUN poetry config virtualenvs.create false  # Disable virtualenvs
RUN poetry install --no-dev  # Install dependencies without development dependencies

# Копируем все файлы в рабочую директорию
COPY . /app/

# Загружаем переменные окружения из файла .env
RUN if [ -f .env ]; then export $(cat .env | xargs); fi

# Запускаем приложение
CMD ["bash", "start.sh"]
