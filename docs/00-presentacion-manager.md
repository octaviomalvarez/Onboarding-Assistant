# Onboarding Assistant — Documentación del Proyecto

**Proyecto:** Onboarding Assistant — Torre de Data, Accenture  
**Autor:** Octavio Alvarez  
**Fecha:** Septiembre 2026  
**Repositorio:** https://github.com/octaviomalvarez/Onboarding-Assistant

---

## 1. Resumen ejecutivo

El **Onboarding Assistant** es una aplicación interna que centraliza y guía el proceso de incorporación de nuevos empleados en la torre de Data de Accenture. La herramienta reemplaza la dispersión actual de información entre emails, documentos, sistemas y personas, ofreciendo un único punto de acceso con checklist interactivo, documentación centralizada, directorio de contactos y un asistente conversacional inteligente.

El proyecto se encuentra en estado de **MVP funcional avanzado**, listo para demo interna y con la mayoría de las funcionalidades core implementadas. La primera versión está orientada a la torre de Data y puede escalarse a otras áreas.

---

## 2. Problema identificado

El proceso de incorporación actual presenta las siguientes fricciones:

- La información está distribuida en múltiples plataformas (email, SharePoint, Confluence, Teams, documentos sueltos)
- No hay claridad sobre qué tareas completar, en qué orden y con qué urgencia
- Las demoras en accesos impactan directamente en el tiempo hasta que el empleado puede operar
- Managers y People Leads reciben consultas repetitivas que consumen tiempo de valor
- La experiencia varía significativamente según el equipo o proyecto de asignación
- No hay visibilidad del progreso de incorporación para los responsables

**Consecuencia:** el nuevo empleado tarda más tiempo en estar operativo, y los managers invierten horas en soporte que podría automatizarse.

---

## 3. Solución propuesta

Una aplicación web accesible directamente desde **Microsoft Teams** (como Teams Tab) que ofrece:

| Funcionalidad | Descripción |
|---|---|
| **Checklist interactivo** | Lista de tareas de las primeras dos semanas con categorías, fechas límite y estado de progreso persistido en base de datos |
| **Dashboard de progreso** | Visualización del avance general y por semana, sincronizado en tiempo real |
| **Directorio de contactos** | People Lead, Tech Lead, RRHH, soporte IT y más |
| **Asistente conversacional** | Chat con IA que responde preguntas en lenguaje natural con streaming en tiempo real, basado en documentación interna |
| **Documentación centralizada** | FAQ, guía de accesos, capacitaciones obligatorias y herramientas del área |
| **Panel de administración** | Permite subir, eliminar y re-indexar documentos de conocimiento sin tocar el servidor |

---

## 4. Arquitectura técnica

```
Microsoft Teams (Teams Tab)
        │
        └── Frontend: Next.js (React)
                │
                └── Backend: FastAPI (Python)
                        │
                        ├── Asistente IA (Claude API / LM Studio / Mock)
                        ├── RAG: ChromaDB + sentence-transformers
                        └── Base de datos: SQLite (→ PostgreSQL en producción)
```

### Stack tecnológico

| Capa | Tecnología | Justificación |
|---|---|---|
| Frontend | Next.js 15 + TypeScript + Tailwind | UI profesional, componentes reutilizables |
| Backend | FastAPI (Python) | Familiar en equipos de Data, alto rendimiento |
| Asistente IA | Mock / Claude API / LM Studio | Funciona sin API key para demo; preparado para producción |
| Base de conocimiento | ChromaDB + sentence-transformers | Búsqueda semántica local, sin infraestructura extra |
| Base de datos | SQLite via SQLModel | Sin servidor; migración a PostgreSQL con un cambio de config |
| Deploy objetivo | Azure App Service | Ecosistema corporativo Accenture |
| Integración Teams | Teams Tab (manifest + headers CSP) | Embebe la app en Teams sin desarrollo adicional |

### ¿Qué es el RAG?

RAG (Retrieval Augmented Generation) es la técnica que permite que el asistente responda preguntas basándose en documentación interna real, no en conocimiento genérico del modelo de IA.

**Cómo funciona:**
1. Los documentos internos (FAQ, guías, procesos) se cargan al sistema
2. Cuando el empleado hace una pregunta, el sistema busca los fragmentos más relevantes por similitud semántica
3. Esos fragmentos se envían junto con la pregunta al modelo de IA
4. El asistente responde con información específica de Accenture e indica la fuente

Esto garantiza respuestas precisas, actualizadas y basadas en fuentes internas aprobadas.

---

## 5. Estado actual del MVP

### Funcionalidades implementadas

| Funcionalidad | Estado | Notas |
|---|---|---|
| Dashboard con progreso | ✅ Completo | Sincronizado con el checklist en tiempo real |
| Checklist semana 1 y 2 | ✅ Completo | Persistido en SQLite, toggle via API |
| Directorio de contactos | ✅ Completo | Datos de ejemplo |
| Chat widget flotante expandible | ✅ Completo | Visible en todas las pantallas |
| Asistente con streaming en tiempo real | ✅ Completo | Efecto de escritura vía SSE |
| Renderizado Markdown en respuestas | ✅ Completo | Tablas, listas, negrita, código |
| Indicadores de fuente en respuestas | ✅ Completo | Muestra el documento origen |
| Historial de conversación | ✅ Completo | Los últimos 10 mensajes se envían al LLM |
| Pipeline RAG | ✅ Completo | Búsqueda semántica en 7 documentos, 31 chunks |
| Panel de administración de docs | ✅ Completo | Upload, delete, re-index desde la UI |
| Teams Tab manifest | ✅ Completo | Listo para publicar en Teams |
| Diseño con branding Accenture | ✅ Completo | Color corporativo #A100FF |
| Repositorio GitHub | ✅ Completo | github.com/octaviomalvarez/Onboarding-Assistant |
| Autenticación Azure AD | ⏳ Pendiente | Para el piloto |

### Lo que funciona hoy en la demo

La aplicación puede demostrarse completamente sin dependencias externas (sin API key, sin base de datos externa):

- El empleado ve su dashboard con progreso real
- Puede marcar tareas del checklist y el progreso se actualiza en tiempo real
- Puede consultar contactos clave
- El asistente responde preguntas frecuentes en lenguaje natural con efecto de escritura, cita los documentos fuente y renderiza Markdown
- El administrador puede subir nuevos documentos y re-indexar sin tocar el servidor

### Lo que falta para producción

| Componente | Descripción | Prioridad |
|---|---|---|
| API key de IA | Acceso a Claude API o modelo local validado | Alta |
| Autenticación Azure AD | Login con cuenta corporativa Accenture | Alta (antes del piloto) |
| Deploy en Azure | URL pública para publicar como Teams Tab | Media |
| Contenido real | Reemplazar documentos de ejemplo con información real de Accenture | Media |
| Panel de manager | Visibilidad del progreso del equipo | Baja |

---

## 6. Guía para la demo

### Requisitos previos
- Node.js instalado
- Python 3.11+ instalado
- Repositorio clonado

### Pasos para levantar la demo

**Terminal 1 — Backend (Windows PowerShell):**
```powershell
$env:PYTHONPATH = "<ruta-al-repo>\backend"
& ".\backend\.venv\Scripts\python.exe" -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

**Terminal 2 — Frontend:**
```bash
cd frontend
npm install
npm run dev
```

Abrir en el browser: `http://localhost:3000`

### Flujo de demo sugerido

1. **Dashboard:** mostrar la bienvenida y el panel de progreso con las cards de Semana 1 y Semana 2
2. **Checklist:** navegar, marcar algunas tareas y volver al dashboard para ver cómo se actualiza el progreso
3. **Contactos:** mostrar el directorio con los contactos clave
4. **Asistente:** usar el chat (botón flotante o sección `/chat`) con preguntas como:
   - *"¿Qué debo hacer durante mi primera semana?"*
   - *"¿Cómo solicito acceso a una herramienta?"*
   - *"¿Cuáles son los cursos obligatorios?"*
   - *"¿Cuál es el stack de herramientas del área?"*
5. **Admin:** mostrar el panel `/admin`, subir un documento `.md` y re-indexar

---

## 7. Roadmap

### Fase actual — POC/MVP (completada)
- MVP funcional con todas las funcionalidades core
- Streaming SSE, Markdown, RAG, persistencia en SQLite
- Panel de administración de documentos
- Arquitectura definida y documentada
- Listo para demo interna

### Próxima fase — Piloto
- Integración con modelo de IA real (Claude API o modelo local validado)
- Autenticación con Azure AD (cuentas corporativas)
- Deploy en Azure App Service
- Publicación como Teams Tab en el tenant de Accenture
- Reemplazo de contenido de ejemplo con información real

### Fase futura — Producción
- Extensión a otras torres y áreas
- Integración con sistemas internos (MyHR, MyTE, portal de accesos)
- Panel para managers con visibilidad del progreso del equipo
- Notificaciones proactivas vía Teams Bot
- Métricas de uso y satisfacción

---

## 8. Estructura del repositorio

```
Onboarding-Assistant/
├── backend/                     # API Python (FastAPI)
│   ├── main.py                  # Punto de entrada
│   ├── database.py              # SQLite engine
│   ├── models/checklist.py      # Modelo SQLModel + seed data
│   ├── api/routes/              # Endpoints: chat, checklist, contactos, admin
│   ├── rag/                     # Pipeline RAG: ingest, retriever, store
│   └── data/docs/               # Documentación interna (Markdown)
├── frontend/                    # Aplicación web (Next.js)
│   └── src/
│       ├── app/                 # Páginas: dashboard, checklist, chat, contactos, admin
│       ├── components/          # Sidebar, Chat, ChatWidget, MarkdownMessage
│       ├── hooks/               # useChatMessages
│       └── lib/                 # api.ts, types.ts, useChecklist.ts
├── teams/                       # Manifest y config para Microsoft Teams Tab
├── docs/                        # Documentación técnica del proyecto
└── Documentation/               # Documentación conceptual original
```

---

## 9. Equipo y recursos necesarios para el piloto

| Recurso | Para qué |
|---|---|
| API key de Claude (Anthropic) o acceso a LM Studio validado | Activar el asistente con IA real |
| Acceso a Azure para deploy | Publicar la aplicación en una URL pública |
| Aprobación de IT/Teams admin | Publicar la app como Teams Tab en el tenant corporativo |
| Colaborador (desarrollador o analista) | Incorporar contenido real y soporte al piloto |
| Grupo piloto de usuarios | 5-10 nuevos empleados de la torre de Data |

---

## 10. Contacto

**Octavio Alvarez**  
Torre de Data — Accenture  
octavio.alvarez@accenture.com  
Repositorio: https://github.com/octaviomalvarez/Onboarding-Assistant
