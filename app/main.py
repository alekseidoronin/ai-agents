import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.database import Base, engine
from app.middleware.error_handler import ErrorHandlerMiddleware
from app.routers import content_plans_router, sales_funnels_router, users_router

logging.basicConfig(
    level=logging.DEBUG if settings.debug else logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="AI Agents Platform",
    description="Платформа для развертывания автономных ИИ-агентов",
    version="0.2.0",
    debug=settings.debug,
)

app.add_middleware(ErrorHandlerMiddleware)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(users_router)
app.include_router(content_plans_router)
app.include_router(sales_funnels_router)


@app.get("/", tags=["system"])
def root():
    return {"status": "ok", "message": "AI Agents Platform is running"}


@app.get("/health", tags=["system"])
def health():
    return {"status": "healthy", "version": "0.2.0"}
