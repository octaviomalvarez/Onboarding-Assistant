# Arquitectura del proyecto

## Visión general

El Onboarding Assistant es una aplicación web que se integra como Teams Tab dentro de Microsoft Teams. El empleado la ve dentro de Teams sin necesidad de abrir un browser externo.

```
Teams Tab (frontend embebido)
    │
    └──► FastAPI (backend Python)
              │
              ├──► Claude API (Anthropic) — asistente conversacional
              ├──► ChromaDB — RAG sobre documentación interna
              └──► PostgreSQL — checklist, progreso, usuarios
```

## Stack tecnológico

| Capa | Tecnología | Por qué |
|---|---|---|
| Frontend | Next.js 15 + TypeScript + Tailwind | UI profesional, sin necesitar frontend specialist |
| Backend | FastAPI (Python) | Familiar en equipos de datos, rápido de construir |
| IA / Chat | Claude API (Anthropic) | Mejor modelo para responder sobre docs internas |
| Base de conocimiento | ChromaDB | Vector store local, sin infra extra para el MVP |
| Base de datos | SQLite → PostgreSQL | Simple para empezar, escalable |
| Auth | Microsoft MSAL (Azure AD) | Ecosistema Accenture |
| Deploy | Azure App Service | Cloud corporativo |

## Estructura de carpetas

```
onboarding-assistant/
├── backend/
│   ├── main.py                  # Punto de entrada FastAPI
│   ├── pyproject.toml           # Dependencias Python
│   ├── .env.example             # Variables de entorno (plantilla)
│   ├── api/
│   │   ├── routes/
│   │   │   ├── health.py        # GET /api/v1/health
│   │   │   └── chat.py          # POST /api/v1/chat
│   │   └── models/              # Modelos Pydantic (a agregar)
│   ├── rag/                     # Procesamiento de documentos (a implementar)
│   └── data/
│       └── docs/                # Documentos internos en Markdown
├── frontend/
│   ├── src/
│   │   ├── app/                 # Next.js App Router
│   │   ├── components/
│   │   │   └── Chat.tsx         # Componente de chat
│   │   └── lib/
│   │       └── api.ts           # Cliente HTTP al backend
│   └── package.json
├── docs/                        # Documentación del proyecto
└── Documentation/               # Boceto original del proyecto
```

## Decisiones de diseño

**¿Por qué Teams Tab y no un bot de Teams?**
Una Teams Tab es la app web corriendo embebida dentro de Teams. No requiere Bot Framework ni permisos especiales de admin para desarrollar. El bot de chat se puede agregar en una fase posterior para notificaciones proactivas.

**¿Por qué Claude API y no Azure OpenAI?**
Claude tiene mejor desempeño en tareas de lectura y síntesis de documentación interna. Azure OpenAI se puede considerar si hay restricciones corporativas de Accenture sobre APIs externas.

**¿Por qué ChromaDB y no un servicio de vectores en la nube?**
Para el MVP, ChromaDB corre localmente sin infraestructura adicional. Cuando el proyecto escale se puede migrar a Azure AI Search o Pinecone.
