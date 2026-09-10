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

MOCK_RESPONSES: list[tuple[list[str], str]] = [
    (
        ["primera semana", "qué debo", "qué hacer", "empezar", "primeros días", "comenzar"],
        "Durante tu primera semana tenés que completar estas tareas:\n\n"
        "• **Día 1:** Completar el formulario en MyHR y solicitar acceso a MyTE\n"
        "• **Día 2:** Configurar la VPN y reunirte con tu People Lead\n"
        "• **Día 3:** Completar el curso de Code of Business Ethics y solicitar acceso a los repos\n\n"
        "Podés seguir el progreso de todas estas tareas desde la sección Checklist.",
    ),
    (
        ["acceso", "solicitar acceso", "herramienta", "permiso", "accesos", "portal"],
        "Para solicitar acceso a una herramienta:\n\n"
        "1. Ingresá al portal interno de accesos con tu cuenta corporativa\n"
        "2. Buscá la herramienta que necesitás\n"
        "3. Completá el formulario de justificación de negocio\n"
        "4. El aprobador correspondiente va a recibir una notificación\n\n"
        "El tiempo estándar es de 1 a 3 días hábiles. Si tenés problemas, contactá a **diego.torres@accenture.com**.",
    ),
    (
        ["capacitación", "curso", "training", "obligatorio", "ethics", "privacy", "cobe"],
        "Los cursos obligatorios para los primeros 30 días son:\n\n"
        "• **Code of Business Ethics (COBE)** — 45 min, completarlo antes del Día 3\n"
        "• **Data Privacy & Security** — 60 min, segunda semana\n"
        "• **Information Security Fundamentals** — 30 min\n"
        "• **Workplace Harassment Prevention** — 45 min\n\n"
        "Todos están disponibles en el portal de capacitaciones. Ante dudas, escribile a **laura.mendez@accenture.com**.",
    ),
    (
        ["myte", "horas", "cargar horas", "carga de horas", "timesheet"],
        "MyTE es el sistema para cargar tus horas trabajadas. Tenés que registrarlas diariamente o como mínimo antes del cierre del viernes.\n\n"
        "Si todavía no tenés acceso, solicitalo a través del portal de herramientas o contactá a la **Mesa de Ayuda IT** (it.support@accenture.com). "
        "El tiempo de aprobación es de 1 día hábil.",
    ),
    (
        ["people lead", "quién es", "referente", "rrhh", "recursos humanos", "carrera"],
        "Tu **People Lead** es tu referente de carrera dentro de Accenture. Lo contactás para:\n\n"
        "• Temas de desarrollo profesional y evaluaciones\n"
        "• Inquietudes sobre tu rol o equipo\n"
        "• Consultas de Recursos Humanos\n\n"
        "Podés encontrar su nombre en tu perfil de MyHR. Para este onboarding, tu People Lead es **María González** (maria.gonzalez@accenture.com).",
    ),
    (
        ["tech lead", "repositorio", "repo", "código", "github", "azure devops", "proyecto"],
        "Para acceso a los repositorios del proyecto, pedíselo directamente al **Tech Lead** de tu proyecto por Teams o email. "
        "En la Torre de Data el Tech Lead es **Carlos Ramírez** (carlos.ramirez@accenture.com).\n\n"
        "Los repos pueden estar en GitHub o Azure DevOps dependiendo del proyecto. "
        "El Tech Lead te va a indicar cuál corresponde y te va a agregar al equipo.",
    ),
    (
        ["vpn", "red", "conexión", "remoto", "conectar"],
        "Para configurar la VPN corporativa:\n\n"
        "1. Contactá a la **Mesa de Ayuda IT** (it.support@accenture.com) para que te envíen el instalador\n"
        "2. Seguí la guía de configuración que te van a mandar por email\n"
        "3. Si la solicitud es antes de las 14hs, el acceso se activa el mismo día\n\n"
        "Si tenés algún problema técnico, escribile directamente a soporte IT.",
    ),
    (
        ["azure", "databricks", "power bi", "synapse", "data factory", "herramienta", "stack", "tecnología"],
        "El stack principal de la Torre de Data es:\n\n"
        "**Cloud & Datos:** Azure Data Factory, Databricks, Azure Synapse Analytics, dbt\n"
        "**Visualización:** Power BI, Tableau (en algunos proyectos)\n"
        "**Lenguajes:** Python, SQL, PySpark\n"
        "**Gestión:** Jira / Azure DevOps, Confluence, Teams\n\n"
        "Los accesos a herramientas de Azure requieren aprobación del Tech Lead y en algunos casos del área de Seguridad.",
    ),
    (
        ["evaluación", "desempeño", "performance", "review", "feedback"],
        "Las evaluaciones formales son **semestrales**. Tu People Lead te va a comunicar las fechas exactas.\n\n"
        "Durante el onboarding se hace una revisión informal al primer mes para ver cómo te estás adaptando. "
        "Es un buen momento para plantear dudas o necesidades de soporte.",
    ),
    (
        ["contacto", "a quién", "con quién", "soporte", "ayuda", "duda"],
        "Los contactos clave para tu onboarding son:\n\n"
        "• **People Lead:** María González — maria.gonzalez@accenture.com\n"
        "• **Tech Lead:** Carlos Ramírez — carlos.ramirez@accenture.com\n"
        "• **Mesa de Ayuda IT:** it.support@accenture.com\n"
        "• **Capacitaciones:** Laura Méndez — laura.mendez@accenture.com\n"
        "• **Accesos:** Diego Torres — diego.torres@accenture.com\n\n"
        "También los podés ver todos en la sección **Contactos** de esta app.",
    ),
]

FALLBACK_RESPONSE = (
    "Gracias por tu pregunta. Por el momento no tengo información específica sobre ese tema en mi base de conocimiento.\n\n"
    "Te recomiendo consultar con:\n"
    "• Tu **People Lead** para temas de RRHH y carrera\n"
    "• El **Tech Lead** del proyecto para temas técnicos\n"
    "• La **Mesa de Ayuda IT** (it.support@accenture.com) para accesos y equipamiento"
)


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
            # La primera línea del chunk es el título de la sección
            chunk_lines = "\n".join(content_lines).strip().splitlines()
            if not chunk_lines:
                continue
            title = chunk_lines[0]
            body = "\n".join(chunk_lines[1:]).strip()
            if body:
                parts.append(f"**{title}**\n{body}")
            else:
                parts.append(title)
        if parts:
            return "Encontré esto en la documentación interna:\n\n" + "\n\n".join(parts)

    lower = message.lower()
    for keywords, response in MOCK_RESPONSES:
        if any(kw in lower for kw in keywords):
            return response
    return FALLBACK_RESPONSE


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
    provider = os.getenv("LLM_PROVIDER", "mock").lower()
    user_content, has_context = _build_user_content(body.message)

    if provider == "anthropic":
        response_text = _call_claude(user_content)
    elif provider == "lmstudio":
        response_text = _call_lmstudio(user_content)
    else:
        context = retrieve_context(body.message) if not collection_is_empty() else ""
        response_text = _call_mock(body.message, context=context)

    return ChatResponse(response=response_text, has_context=has_context, provider=provider)
