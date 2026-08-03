from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os

from api.routes import chat, health, checklist, contacts

load_dotenv()

app = FastAPI(
    title="Onboarding Assistant API",
    description="Backend del asistente de onboarding para nuevos empleados de Accenture",
    version="0.1.0",
)

allowed_origins = os.getenv("ALLOWED_ORIGINS", "http://localhost:3000").split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health.router, prefix="/api/v1", tags=["health"])
app.include_router(chat.router, prefix="/api/v1", tags=["chat"])
app.include_router(checklist.router, prefix="/api/v1", tags=["checklist"])
app.include_router(contacts.router, prefix="/api/v1", tags=["contacts"])


@app.get("/")
def root():
    return {"message": "Onboarding Assistant API", "version": "0.1.0"}
