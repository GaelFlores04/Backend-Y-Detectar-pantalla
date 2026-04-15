import time
import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text
from app.database import engine, Base
from app.routers import sessions, activity
from fastapi.staticfiles import StaticFiles

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def wait_for_db(retries=10, delay=3):
    for i in range(retries):
        try:
            with engine.connect() as conn:
                conn.execute(text("SELECT 1"))
            logger.info("Base de datos lista.")
            return
        except Exception as e:
            logger.warning(f"Esperando base de datos... intento {i+1}/{retries}")
            time.sleep(delay)
    raise Exception("No se pudo conectar a la base de datos.")

wait_for_db()
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Focus Tracker API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(sessions.router)
app.include_router(activity.router)
app.mount("/", StaticFiles(directory="frontend", html=True), name="frontend")

@app.get("/health")
def health():
    return {"status": "ok"}