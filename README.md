# Onboarding Assistant

Asistente digital para nuevos empleados de la torre de Data de Accenture.
Centraliza tareas, accesos, capacitaciones, documentación y contactos clave durante las primeras semanas de incorporación.

## Documentación

| Documento | Descripción |
|---|---|
| [docs/01-arquitectura.md](docs/01-arquitectura.md) | Stack tecnológico, estructura y decisiones de diseño |
| [docs/02-setup-local.md](docs/02-setup-local.md) | Cómo levantar el proyecto en una máquina nueva |
| [docs/03-funcionalidades-mvp.md](docs/03-funcionalidades-mvp.md) | Páginas, endpoints y estado de cada funcionalidad |
| [docs/04-teams-tab.md](docs/04-teams-tab.md) | Cómo publicar la app como Teams Tab |
| [Documentation/](Documentation/) | Boceto original del proyecto (conceptual) |

## Levantar el proyecto (resumen rápido)

```bash
# Backend
cd backend && pip install -e . && uvicorn main:app --reload

# Frontend (en otra terminal)
cd frontend && npm install && npm run dev
```

Ver [docs/02-setup-local.md](docs/02-setup-local.md) para el setup completo.

## Estado actual

- [x] Estructura del proyecto
- [x] Backend FastAPI con endpoints de chat, checklist y contactos
- [x] Frontend Next.js con layout + navegación lateral
- [x] Dashboard con resumen de progreso
- [x] Checklist interactivo (semana 1 y 2)
- [x] Directorio de contactos clave
- [x] Interfaz de chat con el asistente
- [x] Integración con Claude API (requiere API key)
- [x] Teams Tab manifest + scripts de empaquetado
- [ ] RAG sobre documentación interna
- [ ] Checklist personalizado
- [ ] Directorio de contactos
- [ ] Seguimiento de progreso
- [ ] Teams Tab (deploy)
- [ ] Autenticación Azure AD
