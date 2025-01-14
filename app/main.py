# main.py
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.database import engine, Base
from routers import auth, ws
import os

def create_app() -> FastAPI:
    app = FastAPI(title="My WebSocket Auth App")

    # Рекомендуется управлять созданием таблиц через миграции (Alembic),
    # Но если нужно быстро, можешь раскомментировать:
    Base.metadata.create_all(bind=engine)

    # Подключаем роутеры
    app.include_router(auth.router, prefix="/auth", tags=["auth"])
    app.include_router(ws.router, tags=["websockets"])

    this_dir = os.path.dirname(__file__)  # путь к текущей папке (где лежит main.py)
    static_dir = os.path.join(this_dir, "..", "static")  # объединяем путь

    # Монтируем статику по URL /static:
    app.mount("/static", StaticFiles(directory=static_dir), name="static")

    @app.get("/")
    def root():
        return {"message": "Hello from root! Открой /static/index.html для тестового фронтенда."}

    return app

app = create_app()
