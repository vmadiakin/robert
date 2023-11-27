from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from starlette.staticfiles import StaticFiles

from bot import start_bot
import uvicorn

app = FastAPI()

# Подключаем каталог со статическими файлами
app.mount("/static", StaticFiles(directory="static"), name="static")


# Роут для отображения веб-страницы
@app.get("/bots/select_character", response_class=HTMLResponse)
def read_item():
    with open("webpage.html", "r") as file:
        content = file.read()
    return HTMLResponse(content=content)


# Запуск телеграм-бота
async def startup_event():
    await start_bot()


if __name__ == "__main__":
    # Запуск веб-приложения с помощью Uvicorn
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        ssl_keyfile="/app/ssl/privkey.pem",
        ssl_certfile="/app/ssl/fullchain.pem",
    )
