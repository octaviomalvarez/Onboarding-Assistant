from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import anthropic
import os

router = APIRouter()

SYSTEM_PROMPT = """Sos el asistente de onboarding de Accenture para la torre de Data.
Tu trabajo es ayudar a los nuevos empleados durante sus primeras semanas.
Respondés preguntas sobre tareas, accesos, capacitaciones, contactos y documentación.
Siempre respondés en español, de forma clara y concisa.
Si no sabés algo con certeza, lo decís y sugerís a quién consultar."""


class ChatMessage(BaseModel):
    message: str


class ChatResponse(BaseModel):
    response: str


@router.post("/chat", response_model=ChatResponse)
def chat(body: ChatMessage):
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        raise HTTPException(status_code=500, detail="ANTHROPIC_API_KEY no configurada")

    client = anthropic.Anthropic(api_key=api_key)

    message = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=1024,
        system=SYSTEM_PROMPT,
        messages=[{"role": "user", "content": body.message}],
    )

    return ChatResponse(response=message.content[0].text)
