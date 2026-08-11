# Onboarding Assistant — Documentación del Proyecto

**Proyecto:** Onboarding Assistant — Torre de Data, Accenture  
**Autor:** Octavio Alvarez  
**Fecha:** Agosto 2026  
**Repositorio:** https://github.com/octaviomalvarez/Onboarding-Assistant

---

## 1. Resumen ejecutivo

El **Onboarding Assistant** es una aplicación interna que centraliza y guía el proceso de incorporación de nuevos empleados en la torre de Data de Accenture. La herramienta reemplaza la dispersión actual de información entre emails, documentos, sistemas y personas, ofreciendo un único punto de acceso con checklist personalizado, documentación centralizada, directorio de contactos y un asistente conversacional inteligente.

El proyecto se encuentra en estado de **MVP funcional**, listo para demo interna. La primera versión está orientada a la torre de Data y puede escalarse a otras áreas.

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
| **Checklist personalizado** | Lista de tareas de las primeras dos semanas con categorías, fechas límite y estado de progreso |
| **Dashboard de progreso** | Visualización del avance general y por semana |
| **Directorio de contactos** | People Lead, Tech Lead, RRHH, soporte IT y más |
| **Asistente conversacional** | Chat con IA que responde preguntas en lenguaje natural basándose en documentación interna |
| **Documentación centralizada** | FAQ, guía de accesos, capacitaciones obligatorias y herramientas del área |

---

## 4. Arquitectura técnica

La solución está construida con tecnologías estándar del mercado, elegidas por su familiaridad en equipos de Data y facilidad de mantenimiento.

```
Microsoft Teams (Teams Tab)
        │
        └── Frontend: Next.js (React)
                │
                └── Backend: FastAPI (Python)
                        │
                        ├── Asistente IA (Claude API / LM Studio)
                        ├── RAG: ChromaDB + sentence-transformers
                        └── Base de datos (SQLite → PostgreSQL)
```

### Stack tecnológico

| Capa | Tecnología | Justificación |
|---|---|---|
| Frontend | Next.js 15 + TypeScript + Tailwind | UI profesional, componentes reutilizables |
| Backend | FastAPI (Python) | Familiar en equipos de Data, alto rendimiento |
| Asistente IA | Claude API (Anthropic) | Mejor modelo para síntesis de documentación interna |
| Base de conocimiento | ChromaDB + sentence-transformers | Búsqueda semántica local, sin infraestructura extra |
| Deploy objetivo | Azure App Service | Ecosistema corporativo Accenture |
| Integración Teams | Teams Tab (manifest) | Embebe la app en Teams sin desarrollo adicional |

### ¿Qué es el RAG?

RAG (Retrieval Augmented Generation) es la técnica que permite que el asistente responda preguntas basándose en documentación interna real, no en conocimiento genérico del modelo de IA.

**Cómo funciona:**
1. Los documentos internos (FAQ, guías, procesos) se cargan al sistema
2. Cuando el empleado hace una pregunta, el sistema busca los fragmentos más relevantes
3. Esos fragmentos se envían junto con la pregunta al modelo de IA
4. El asistente responde con información específica de Accenture

Esto garantiza respuestas precisas, actualizadas y basadas en fuentes internas aprobadas.

---

## 5. Estado actual del MVP

### Funcionalidades implementadas

| Funcionalidad | Estado | Notas |
|---|---|---|
| Dashboard con progreso | ✅ Completo | Sincronizado con el checklist |
| Checklist semana 1 y 2 | ✅ Completo | Persistencia local, categorías, fechas |
| Directorio de contactos | ✅ Completo | Datos de ejemplo |
| Chat widget flotante | ✅ Completo | Visible en todas las pantallas |
| Asistente con respuestas mock | ✅ Completo | Funciona sin dependencias externas |
| Pipeline RAG | ✅ Completo | Listo para conectar con modelo IA real |
| Documentos internos de ejemplo | ✅ Completo | FAQ, accesos, capacitaciones, herramientas |
| Teams Tab manifest | ✅ Completo | Listo para publicar en Teams |
| Repositorio GitHub | ✅ Completo | github.com/octaviomalvarez/Onboarding-Assistant |
| Diseño con branding Accenture | ✅ Completo | Color corporativo #A100FF |

### Lo que funciona hoy en la demo

La aplicación puede demostrarse completamente sin dependencias externas:

- El empleado ve su dashboard con progreso real
- Puede marcar tareas del checklist y el progreso se actualiza en tiempo real
- Puede consultar contactos clave
- El asistente responde preguntas frecuentes de onboarding en lenguaje natural

### Lo que falta para producción

| Componente | Descripción | Prioridad |
|---|---|---|
| API key de IA | Acceso a Claude API o modelo local validado | Alta |
| Autenticación Azure AD | Login con cuenta corporativa Accenture | Alta (antes del piloto) |
| Persistencia en base de datos | El progreso del empleado guardado por usuario | Alta (antes del piloto) |
| Deploy en Azure | URL pública para publicar como Teams Tab | Media |
| Contenido real | Reemplazar documentos de ejemplo con información real de Accenture | Media |

---

## 6. Guía para la demo

### Requisitos previos
- Node.js instalado
- Python 3.11+ instalado
- Repositorio clonado

### Pasos para levantar la demo

**Terminal 1 — Backend:**
```bash
cd backend
python -m venv .venv
.venv\Scripts\activate    # Windows
pip install -e .
uvicorn main:app --reload
```

**Terminal 2 — Frontend:**
```bash
cd frontend
npm install
npm run dev
```

Abrir en el browser: `http://localhost:3000`

### Flujo de demo sugerido

1. **Dashboard:** mostrar la bienvenida personalizada y el panel de progreso con las cards de Semana 1 y Semana 2
2. **Checklist:** navegar a la sección, marcar algunas tareas y volver al dashboard para ver cómo se actualiza el progreso en tiempo real
3. **Contactos:** mostrar el directorio con los contactos clave del onboarding
4. **Asistente:** usar el chat widget (botón flotante abajo a la derecha) y hacer preguntas como:
   - *"¿Qué debo hacer durante mi primera semana?"*
   - *"¿Cómo solicito acceso a una herramienta?"*
   - *"¿Cuáles son los cursos obligatorios?"*
   - *"¿Quién es mi People Lead?"*

---

## 7. Roadmap

### Fase actual — POC (completada)
- MVP funcional con todas las funcionalidades core
- Arquitectura definida y documentada
- Listo para demo interna

### Próxima fase — Piloto
- Integración con modelo de IA real (Claude API o LM Studio)
- Autenticación con Azure AD (cuentas corporativas)
- Persistencia de datos en base de datos (progreso por usuario)
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
├── backend/                  # API Python (FastAPI)
│   ├── api/routes/           # Endpoints: chat, checklist, contactos
│   ├── rag/                  # Pipeline de documentos con IA
│   ├── data/docs/            # Documentación interna (Markdown)
│   └── main.py               # Punto de entrada
├── frontend/                 # Aplicación web (Next.js)
│   └── src/
│       ├── app/              # Páginas: dashboard, checklist, contactos
│       ├── components/       # Sidebar, Chat, ChatWidget
│       └── lib/              # Tipos, datos, hooks
├── teams/                    # Configuración para Microsoft Teams Tab
├── docs/                     # Documentación técnica del proyecto
└── Documentation/            # Documentación conceptual original
```

---

## 9. Equipo y recursos necesarios para el piloto

Para avanzar hacia un piloto real se necesita:

| Recurso | Para qué |
|---|---|
| API key de Claude (Anthropic) o acceso a LM Studio validado | Activar el asistente conversacional con IA real |
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
