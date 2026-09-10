from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from typing import Literal
import asyncio
import json
import os

from rag.retriever import retrieve_context
from rag.store import collection_is_empty

router = APIRouter()

MAX_HISTORY = 10

SYSTEM_PROMPT = """Sos el asistente de onboarding de Accenture para la torre de Data.
Tu trabajo es ayudar a los nuevos empleados durante sus primeras semanas.
Respondés preguntas sobre tareas, accesos, capacitaciones, contactos y documentación.
Siempre respondés en español, de forma clara y concisa.
Cuando uses información del contexto provisto, respondé basándote en esa información.
Si no sabés algo con certeza, lo decís y sugerís a quién consultar."""

MOCK_RESPONSES: list[tuple[list[str], str]] = [
    (
        ["primera semana", "qué debo", "qué hacer", "empezar", "primeros días", "comenzar", "primer dia", "día 1"],
        "Durante tu primera semana tenés que completar estas tareas:\n\n"
        "- **Día 1:** Completar el formulario en MyHR y solicitar acceso a MyTE\n"
        "- **Día 2:** Configurar la VPN y reunirte con tu People Lead\n"
        "- **Día 3:** Completar el curso de Code of Business Ethics y solicitar acceso a los repos\n\n"
        "Podés seguir el progreso de todas estas tareas desde la sección **Checklist**.",
    ),
    (
        ["acceso", "solicitar acceso", "herramienta", "permiso", "accesos", "portal"],
        "Para solicitar acceso a una herramienta:\n\n"
        "1. Ingresá al portal interno de accesos con tu cuenta corporativa\n"
        "2. Buscá la herramienta que necesitás\n"
        "3. Completá el formulario de justificación de negocio\n"
        "4. El aprobador correspondiente va a recibir una notificación\n\n"
        "El tiempo estándar es de **1 a 3 días hábiles**. Si tenés problemas, contactá a diego.torres@accenture.com.",
    ),
    (
        ["capacitación", "curso", "training", "obligatorio", "ethics", "privacy", "cobe"],
        "Los cursos obligatorios para los primeros 30 días son:\n\n"
        "| Curso | Duración | Plazo |\n"
        "|---|---|---|\n"
        "| Code of Business Ethics (COBE) | 45 min | Día 3 |\n"
        "| Data Privacy & Security | 60 min | Semana 2 |\n"
        "| Information Security Fundamentals | 30 min | Semana 2 |\n"
        "| Workplace Harassment Prevention | 45 min | Mes 1 |\n\n"
        "Todos disponibles en el portal de capacitaciones. Dudas: laura.mendez@accenture.com.",
    ),
    (
        ["myte", "horas", "cargar horas", "carga de horas", "timesheet"],
        "**MyTE** es el sistema para cargar tus horas trabajadas. Tenés que registrarlas como mínimo antes del cierre del viernes.\n\n"
        "Si todavía no tenés acceso, solicitalo a través del portal o contactá a la Mesa de Ayuda IT (it.support@accenture.com). "
        "El tiempo de aprobación es de **1 día hábil**.",
    ),
    (
        ["people lead", "quién es", "referente", "rrhh", "recursos humanos", "carrera"],
        "Tu **People Lead** es tu referente de carrera dentro de Accenture. Lo contactás para:\n\n"
        "- Temas de desarrollo profesional y evaluaciones\n"
        "- Inquietudes sobre tu rol o equipo\n"
        "- Consultas de Recursos Humanos\n\n"
        "Para este onboarding, tu People Lead es **María González** — maria.gonzalez@accenture.com.",
    ),
    (
        ["tech lead", "repositorio", "repo", "código", "github", "azure devops", "proyecto"],
        "Para acceso a los repositorios, pedíselo directamente al **Tech Lead** de tu proyecto por Teams o email.\n\n"
        "En la Torre de Data el Tech Lead es **Carlos Ramírez** — carlos.ramirez@accenture.com.\n\n"
        "Los repos pueden estar en GitHub o Azure DevOps según el proyecto.",
    ),
    (
        ["vpn", "red", "conexión", "remoto", "conectar"],
        "Para configurar la VPN corporativa:\n\n"
        "1. Contactá a la **Mesa de Ayuda IT** (it.support@accenture.com) para el instalador\n"
        "2. Seguí la guía de configuración que te mandan por email\n"
        "3. Si la solicitud entra antes de las 14hs, el acceso se activa el mismo día",
    ),
    (
        ["azure", "databricks", "power bi", "synapse", "data factory", "stack", "tecnología", "herramientas"],
        "El stack principal de la Torre de Data:\n\n"
        "**Cloud & Datos:** Azure Data Factory · Databricks · Synapse Analytics · dbt\n\n"
        "**Visualización:** Power BI · Tableau\n\n"
        "**Lenguajes:** Python · SQL · PySpark\n\n"
        "**Gestión:** Jira / Azure DevOps · Confluence · Teams\n\n"
        "Los accesos a Azure requieren aprobación del Tech Lead y en algunos casos de Seguridad.",
    ),
    (
        ["evaluación", "desempeño", "performance", "review", "feedback"],
        "Las evaluaciones formales son **semestrales**. Tu People Lead te va a comunicar las fechas exactas.\n\n"
        "Durante el onboarding se hace una revisión informal al **primer mes** para ver cómo te estás adaptando.",
    ),
    (
        ["contacto", "a quién", "con quién", "soporte", "ayuda", "duda", "comunicar"],
        "Los contactos clave para tu onboarding:\n\n"
        "| Rol | Nombre | Email |\n"
        "|---|---|---|\n"
        "| People Lead | María González | maria.gonzalez@accenture.com |\n"
        "| Tech Lead | Carlos Ramírez | carlos.ramirez@accenture.com |\n"
        "| Mesa IT | — | it.support@accenture.com |\n"
        "| Capacitaciones | Laura Méndez | laura.mendez@accenture.com |\n"
        "| Accesos | Diego Torres | diego.torres@accenture.com |\n\n"
        "También los podés ver en la sección **Contactos** de esta app.",
    ),
    (
        ["buddy", "mentor", "referente informal", "guía"],
        "El **Buddy** es un colega asignado informalmente para ayudarte durante el onboarding. "
        "Es el primer contacto para dudas del día a día.\n\n"
        "Si no te fue asignado uno, consultale a tu People Lead o al Tech Lead del proyecto.",
    ),
    (
        ["teams", "microsoft", "outlook", "email", "calendar", "reunión"],
        "Para configurar tu cuenta de Microsoft 365 (Teams, Outlook, SharePoint):\n\n"
        "1. Accedé al link de activación que te llega por email el primer día\n"
        "2. Si no lo recibís, contactá a la Mesa de Ayuda IT — it.support@accenture.com\n\n"
        "Teams es el canal principal de comunicación del equipo.",
    ),
    (
        ["beneficio", "obra social", "seguro", "sueldo", "payroll", "liquidación", "vacaciones", "licencia"],
        "Para consultas sobre beneficios, obra social, sueldo y licencias, el canal es tu **People Lead** "
        "(maria.gonzalez@accenture.com).\n\n"
        "También podés encontrar información en el portal de RRHH accediendo con tu cuenta corporativa.",
    ),
]

FALLBACK_RESPONSE = (
    "Por el momento no tengo información específica sobre ese tema en la documentación de onboarding.\n\n"
    "Te recomiendo consultar con:\n"
    "- Tu **People Lead** para temas de RRHH y carrera\n"
    "- El **Tech Lead** del proyecto para temas técnicos\n"
    "- La **Mesa de Ayuda IT** (it.support@accenture.com) para accesos y equipamiento"
)


class HistoryEntry(BaseModel):
    role: Literal["user", "assistant"]
    content: str


class ChatMessage(BaseModel):
    message: str
    history: list[HistoryEntry] = []
    role: str | None = None


class ChatResponse(BaseModel):
    response: str
    has_context: bool = False
    provider: str = ""
    sources: list[str] = []


def _get_context(message: str) -> tuple[str, list[str], bool]:
    if collection_is_empty():
        return "", [], False
    context, sources = retrieve_context(message)
    return context, sources, bool(context)


def _call_mock(message: str, context: str = "") -> str:
    if context:
        sections = context.split("\n\n---\n\n")
        parts = []
        for section in sections:
            lines = section.strip().splitlines()
            content_lines = [
                l for l in lines
                if not l.startswith("[Fuente:") and not l.startswith("[Título:")
            ]
            chunk_lines = "\n".join(content_lines).strip().splitlines()
            if not chunk_lines:
                continue
            title = chunk_lines[0]
            body = "\n".join(chunk_lines[1:]).strip()
            if body:
                parts.append(f"**{title}**\n\n{body}")
            else:
                parts.append(title)
        if parts:
            return "Encontré esto en la documentación interna:\n\n" + "\n\n---\n\n".join(parts)

    lower = message.lower()
    for keywords, response in MOCK_RESPONSES:
        if any(kw in lower for kw in keywords):
            return response
    return FALLBACK_RESPONSE


def _build_messages(message: str, context: str, history: list[HistoryEntry]) -> list[dict]:
    msgs = [{"role": h.role, "content": h.content} for h in history[-MAX_HISTORY:]]
    user_content = message
    if context:
        user_content = (
            f"Usá la siguiente información interna para responder:\n\n{context}\n\nPREGUNTA: {message}"
        )
    msgs.append({"role": "user", "content": user_content})
    return msgs


def _call_lmstudio(message: str, context: str, history: list[HistoryEntry]) -> str:
    from openai import OpenAI
    base_url = os.getenv("LMSTUDIO_URL", "http://localhost:1234/v1")
    client = OpenAI(base_url=base_url, api_key="lm-studio")
    response = client.chat.completions.create(
        model="local-model",
        messages=[{"role": "system", "content": SYSTEM_PROMPT}] + _build_messages(message, context, history),
        max_tokens=1024,
    )
    return response.choices[0].message.content


def _call_claude(message: str, context: str, history: list[HistoryEntry]) -> str:
    import anthropic
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        raise HTTPException(status_code=500, detail="ANTHROPIC_API_KEY no configurada")
    client = anthropic.Anthropic(api_key=api_key)
    result = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=1024,
        system=SYSTEM_PROMPT,
        messages=_build_messages(message, context, history),
    )
    return result.content[0].text


@router.post("/chat", response_model=ChatResponse)
def chat(body: ChatMessage):
    provider = os.getenv("LLM_PROVIDER", "mock").lower()
    context, sources, has_context = _get_context(body.message)

    if provider == "anthropic":
        response_text = _call_claude(body.message, context, body.history)
    elif provider == "lmstudio":
        response_text = _call_lmstudio(body.message, context, body.history)
    else:
        response_text = _call_mock(body.message, context=context)

    return ChatResponse(response=response_text, has_context=has_context, provider=provider, sources=sources)


async def _stream_mock(text: str):
    words = text.split(" ")
    for i, word in enumerate(words):
        chunk = word if i == len(words) - 1 else word + " "
        yield chunk
        await asyncio.sleep(0.03)


async def _stream_claude(message: str, context: str, history: list[HistoryEntry]):
    import anthropic
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        raise HTTPException(status_code=500, detail="ANTHROPIC_API_KEY no configurada")
    client = anthropic.Anthropic(api_key=api_key)
    with client.messages.stream(
        model="claude-sonnet-4-6",
        max_tokens=1024,
        system=SYSTEM_PROMPT,
        messages=_build_messages(message, context, history),
    ) as stream:
        for text in stream.text_stream:
            yield text


async def _stream_lmstudio(message: str, context: str, history: list[HistoryEntry]):
    from openai import OpenAI
    base_url = os.getenv("LMSTUDIO_URL", "http://localhost:1234/v1")
    client = OpenAI(base_url=base_url, api_key="lm-studio")
    stream = client.chat.completions.create(
        model="local-model",
        messages=[{"role": "system", "content": SYSTEM_PROMPT}] + _build_messages(message, context, history),
        max_tokens=1024,
        stream=True,
    )
    for chunk in stream:
        delta = chunk.choices[0].delta.content
        if delta:
            yield delta


@router.post("/chat/stream")
async def chat_stream(body: ChatMessage):
    provider = os.getenv("LLM_PROVIDER", "mock").lower()
    context, sources, has_context = await asyncio.to_thread(_get_context, body.message)

    async def event_generator():
        try:
            if provider == "anthropic":
                gen = _stream_claude(body.message, context, body.history)
            elif provider == "lmstudio":
                gen = _stream_lmstudio(body.message, context, body.history)
            else:
                text = _call_mock(body.message, context=context)
                gen = _stream_mock(text)

            async for chunk in gen:
                yield f"data: {json.dumps({'chunk': chunk})}\n\n"

            done_payload = json.dumps({"done": True, "has_context": has_context, "sources": sources})
            yield f"data: {done_payload}\n\n"
        except Exception as e:
            yield f"data: {json.dumps({'error': str(e)})}\n\n"

    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
        headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no"},
    )
