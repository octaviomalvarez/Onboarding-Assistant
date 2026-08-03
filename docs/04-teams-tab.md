# Teams Tab — cómo publicar la app en Teams

La app está pensada para correr como una **Teams Tab personal**: el empleado la ve dentro de Teams sin salir a un browser externo.

## Estructura de la carpeta `teams/`

```
teams/
├── manifest.json        ← Configuración de la app para Teams
├── icon-color.png       ← Ícono 192x192 (color)
├── icon-outline.png     ← Ícono 32x32 (outline)
├── generate_icons.py    ← Script para regenerar los íconos
├── package.py           ← Script para generar el zip de deploy
└── onboarding-assistant.zip  ← Generado por package.py (no commitear)
```

## Proceso de deploy

### Paso 1 — Tener la app publicada en una URL pública

Teams no puede cargar `localhost`. La app necesita estar en una URL accesible con HTTPS. Opciones:
- **Azure App Service** (producción)
- **ngrok** (para pruebas rápidas durante desarrollo)

#### Opción desarrollo rápido con ngrok

```bash
# Instalar ngrok desde https://ngrok.com
# Con el frontend corriendo en localhost:3000:
ngrok http 3000
# ngrok devuelve una URL tipo: https://abc123.ngrok.io
```

### Paso 2 — Generar el zip

```bash
python teams/package.py https://TU_URL_AQUI
# Ejemplo: python teams/package.py https://abc123.ngrok.io
# Genera: teams/onboarding-assistant.zip
```

### Paso 3 — Subir a Teams

1. Abrí Microsoft Teams
2. Andá a **Apps** (ícono en la barra lateral izquierda)
3. Hacé clic en **Manage your apps** (abajo a la izquierda)
4. Elegí **Upload an app** → **Upload a custom app**
5. Seleccioná `teams/onboarding-assistant.zip`
6. La app aparece como una tab personal en Teams

> Si no ves la opción de subir apps, el tenant de Accenture puede tener esa función restringida. En ese caso hay que pedirle al admin de Teams que habilite el sideloading o que publique la app en el catálogo interno.

### Paso 4 — Actualizar la app

Cada vez que cambie la URL o la versión:
1. Actualizar `version` en `manifest.json`
2. Ejecutar `python teams/package.py` con la nueva URL
3. En Teams: Apps → Manage your apps → buscar la app → Update

## Consideraciones para producción

- La URL definitiva va a ser la del Azure App Service donde esté deployada la app
- El `id` del manifest (`a3f8c2d1-...`) es único por app — no cambiarlo una vez publicado
- Para publicar en el catálogo interno de Accenture (que todos los empleados puedan instalarla), hay que pasar por el proceso de aprobación del equipo de IT/Teams admin

## Por qué Teams Tab y no Teams Bot

| | Teams Tab | Teams Bot |
|---|---|---|
| Interfaz | App web completa embebida | Solo chat |
| Checklist visual | Sí | No |
| Requiere admin | Solo para publicar | Sí, para registrar el bot |
| Complejidad | Baja | Alta |

El bot de Teams se puede agregar en una fase posterior para enviar recordatorios proactivos al empleado.
