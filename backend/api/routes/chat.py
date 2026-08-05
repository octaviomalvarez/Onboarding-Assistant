from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
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
    provider: str = ""


def _build_user_content(message: str) -> tuple[str, bool]:
    context = retrieve_context(message) if not collection_is_empty() else ""
    has_context = bool(context)

    if has_context:
        content = f"""Usá la siguiente información interna de Accenture para responder.
Si la información no alcanza para responder con certeza, decilo claramente.

INFORMACIÓN RELEVANTE:
{context}

PREGUNTA:
{message}"""
    else:
        content = message

    return content, has_context


def _call_lmstudio(user_content: str) -> str:
    from openai import OpenAI

    base_url = os.getenv("LMSTUDIO_URL", "http://localhost:1234/v1")
    client = OpenAI(base_url=base_url, api_key="lm-studio")

    response = client.chat.completions.create(
        model="local-model",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_content},
        ],
        max_tokens=1024,
    )
    return response.choices[0].message.content


def _call_claude(user_content: str) -> str:
    import anthropic

    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        raise HTTPException(status_code=500, detail="ANTHROPIC_API_KEY no configurada")

    client = anthropic.Anthropic(api_key=api_key)
    message = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=1024,
        system=SYSTEM_PROMPT,
        messages=[{"role": "user", "content": user_content}],
    )
    return message.content[0].text


@router.post("/chat", response_model=ChatResponse)
def chat(body: ChatMessage):
    provider = os.getenv("LLM_PROVIDER", "lmstudio").lower()
    user_content, has_context = _build_user_content(body.message)

    if provider == "anthropic":
        response_text = _call_claude(user_content)
    else:
        response_text = _call_lmstudio(user_content)

    return ChatResponse(response=response_text, has_context=has_context, provider=provider)
