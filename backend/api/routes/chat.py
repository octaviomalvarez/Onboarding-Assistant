from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import anthropic
import os

from rag.retriever import retrieve_context
from rag.store import collection_is_empty

router = APIRouter()

SYSTEM_PROMPT = """Sos el asistente de onboarding de Accenture para la torre de Data.
Tu trabajo es ayudar a los nuevos empleados durante sus primeras semanas.
Respondés preguntas sobre tareas, accesos, capacitaciones, contactos y documentación.
Siempre respondés en español, de forma clara y concisa.
Cuando uses información del contexto provisto, respondé basándote en esa información.
Si no sabés algo con certeza, lo decís y sugerís a quién consultar."""


class ChatMessage(BaseModel):
    message: str


class ChatResponse(BaseModel):
    response: str
    has_context: bool = False


@router.post("/chat", response_model=ChatResponse)
def chat(body: ChatMessage):
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        raise HTTPException(status_code=500, detail="ANTHROPIC_API_KEY no configurada")

    # Buscar contexto relevante en los documentos internos
    context = retrieve_context(body.message) if not collection_is_empty() else ""
    has_context = bool(context)

    if has_context:
        user_content = f"""Usá la siguiente información interna de Accenture para responder.
Si la información no alcanza para responder con certeza, decilo claramente.

INFORMACIÓN RELEVANTE:
{context}

PREGUNTA:
{body.message}"""
    else:
        user_content = body.message

    client = anthropic.Anthropic(api_key=api_key)
    message = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=1024,
        system=SYSTEM_PROMPT,
        messages=[{"role": "user", "content": user_content}],
    )

    return ChatResponse(response=message.content[0].text, has_context=has_context)
