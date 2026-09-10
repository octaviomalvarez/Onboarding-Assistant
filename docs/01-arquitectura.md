# Arquitectura del proyecto

## Visión general

El Onboarding Assistant es una aplicación web que se integra como Teams Tab dentro de Microsoft Teams.

```
Teams Tab (frontend embebido)
    │
    └──► FastAPI (backend Python)
              │
              ├──► LLM Provider (mock / Claude API / LM Studio)
              ├──► ChromaDB + sentence-transformers — RAG
              └──► SQLite (SQLModel) — checklist y progreso
```

## Stack tecnológico

| Capa | Tecnología | Por qué |
|---|---|---|
| Frontend | Next.js 15 + TypeScript + Tailwind CSS 4 | UI profesional, sin necesitar frontend specialist |
| Backend | FastAPI (Python) | Familiar en equipos de datos, rápido de construir |
| IA / Chat | Mock / Claude API / LM Studio | Flexible: funciona sin API key para demo |
| Base de conocimiento | ChromaDB + sentence-transformers | Vector store local, sin infra extra para el MVP |
| Base de datos | SQLite via SQLModel | Simple para empezar, escalable a PostgreSQL |
| Auth | Microsoft MSAL (Azure AD) | Pendiente — para el piloto |
| Deploy | Azure App Service | Cloud corporativo |

## Estructura de carpetas

```
onboarding-assistant/
├── backend/
│   ├── main.py                      # Punto de entrada FastAPI + lifespan
│   ├── database.py                  # Engine SQLite y sesiones
│   ├── models/
│   │   └── checklist.py             # Modelo SQLModel + seed data
│   ├── api/
│   │   └── routes/
│   │       ├── health.py            # GET /api/v1/health
│   │       ├── chat.py              # POST /chat y /chat/stream (SSE)
│   │       ├── checklist.py         # GET + PUT /checklist
│   │       ├── contacts.py          # GET /contacts
│   │       └── admin.py             # GET/POST/DELETE /admin/docs, POST /admin/reindex
│   ├── rag/
│   │   ├── ingest.py                # Carga docs → embeddings → ChromaDB
│   │   ├── retriever.py             # Búsqueda semántica, umbral 0.75
│   │   └── store.py                 # Inicialización de la colección ChromaDB
│   └── data/
│       └── docs/                    # Documentos internos en Markdown
├── frontend/
│   └── src/
│       ├── app/
│       │   ├── page.tsx             # Dashboard
│       │   ├── checklist/page.tsx   # Checklist
│       │   ├── chat/page.tsx        # Chat completo
│       │   ├── contactos/page.tsx   # Directorio
│       │   └── admin/page.tsx       # Panel de administración
│       ├── components/
│       │   ├── Chat.tsx             # Chat full-page
│       │   ├── ChatWidget.tsx       # Widget flotante expandible
│       │   ├── MarkdownMessage.tsx  # Renderizado Markdown + badges de fuente
│       │   ├── Sidebar.tsx          # Navegación lateral
│       │   └── RoleSelector.tsx     # (reservado, sin uso activo)
│       ├── contexts/
│       │   └── RoleContext.tsx      # (reservado, sin uso activo)
│       ├── hooks/
│       │   └── useChatMessages.ts   # Hook compartido para el estado del chat
│       └── lib/
│           ├── api.ts               # Todas las llamadas HTTP al backend
│           ├── types.ts             # Tipos TypeScript compartidos
│           └── useChecklist.ts      # Hook con carga desde API y toggle optimista
├── docs/                            # Documentación del proyecto
└── teams/                           # Manifest y config para Teams Tab
```

## Decisiones de diseño

**¿Por qué SSE en vez de WebSockets para el streaming?**
SSE (Server-Sent Events) es unidireccional y más simple de implementar con FastAPI. Suficiente para el caso de uso de chat donde el cliente envía un mensaje y el servidor responde. WebSockets agregarían complejidad innecesaria.

**¿Por qué SQLite y no PostgreSQL desde el inicio?**
Para el MVP no hay múltiples usuarios concurrentes. SQLite no requiere servidor y el schema ya está definido con SQLModel, por lo que migrar a PostgreSQL solo requiere cambiar la connection string.

**¿Por qué mock provider y no solo Claude API?**
El proyecto se desarrolló sin API key disponible. El mock cubre RAG real (ChromaDB) + keyword matching, suficiente para demo completa sin costos ni dependencias externas.

**¿Por qué react-markdown en vez de `dangerouslySetInnerHTML`?**
Las respuestas del LLM contienen Markdown (tablas, listas, negrita). react-markdown parsea de forma segura y permite aplicar estilos consistentes con el design system.
