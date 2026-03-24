from fastapi import FastAPI

from app.config import settings
from app.database import Base, engine
from app.routers import content_plans

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="AI Agents Platform",
    description="Платформа для развертывания автономных ИИ-агентов",
    version="0.1.0",
    debug=settings.debug,
)

app.include_router(content_plans.router)


@app.get("/")
def root():
    return {"status": "ok", "message": "AI Agents Platform is running"}


@app.get("/health")
def health():
    return {"status": "healthy"}
