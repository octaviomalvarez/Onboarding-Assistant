# Funcionalidades del MVP

## Estado actual

| Funcionalidad | Estado | Notas |
|---|---|---|
| Asistente conversacional (chat) | Implementado | Soporta mock (sin API key), Anthropic y LM Studio |
| RAG sobre documentación interna | Implementado | ChromaDB + sentence-transformers, umbral de relevancia |
| Documentos de onboarding indexados | Implementado | 7 archivos .md, 31 chunks en `backend/data/docs/` |
| Widget de chat expandible | Implementado | Tamaño normal y expandido desde el header |
| Checklist de onboarding | Implementado | Datos de ejemplo, estado local (sin persistencia aún) |
| Dashboard con progreso | Implementado | Calcula progreso en base al checklist |
| Directorio de contactos | Implementado | Datos de ejemplo |
| Navegación lateral | Implementado | |
| Persistencia de progreso en BD | Pendiente | Siguiente etapa |
| Autenticación Azure AD | Pendiente | Para el piloto |
| Teams Tab | Pendiente | Para el piloto |

## Páginas del frontend

### `/` — Dashboard
Muestra el resumen del progreso del empleado: barra de progreso general, tareas por semana y las próximas tareas pendientes. Acceso rápido al asistente.

### `/checklist` — Checklist
Lista de tareas de las primeras dos semanas, organizadas por semana y categoría (accesos, capacitaciones, administrativo, equipo). El empleado puede marcar tareas como completadas. El estado se guarda localmente en el navegador (sin base de datos aún).

**Categorías:**
- **Accesos:** solicitudes de acceso a herramientas y sistemas
- **Capacitaciones:** cursos obligatorios y recomendados
- **Administrativo:** trámites de RRHH y carga de horas
- **Equipo:** reuniones y presentaciones con el equipo

### `/chat` — Asistente
Interfaz de chat que se conecta al backend. El backend usa RAG para buscar contexto relevante en los documentos de onboarding antes de responder. Soporta tres proveedores de LLM: mock (sin API key), Anthropic Claude y LM Studio. También disponible como widget flotante en todas las páginas.

### `/contactos` — Contactos clave
Directorio con los contactos principales para el onboarding: People Lead, Tech Lead, soporte IT, capacitaciones y accesos.

## Endpoints del backend

| Método | Ruta | Descripción |
|---|---|---|
| GET | `/api/v1/health` | Estado del servidor |
| POST | `/api/v1/chat` | Envía un mensaje al asistente |
| GET | `/api/v1/checklist` | Lista de tareas del onboarding |
| GET | `/api/v1/contacts` | Lista de contactos clave |

Ver Swagger en `http://localhost:8000/docs` con el servidor corriendo.

## Datos de ejemplo vs datos reales

Actualmente toda la información (checklist y contactos) son datos de ejemplo hardcodeados. Cuando el proyecto avance hacia el piloto se van a reemplazar con:
- Datos reales del área/proyecto del empleado
- Información de los sistemas internos de Accenture
- Personalización por rol, seniority y ubicación
