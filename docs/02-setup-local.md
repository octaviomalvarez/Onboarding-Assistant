# Setup local — primeros pasos

Esta guía permite levantar el proyecto en una máquina nueva desde cero.

## Requisitos previos

- Python 3.11 o superior
- Node.js 18 o superior
- Una API key de Anthropic (`ANTHROPIC_API_KEY`)

## 1. Clonar el repositorio

```bash
git clone <url-del-repo>
cd onboarding-assistant
```

## 2. Configurar el backend

```bash
cd backend

# Crear entorno virtual
python -m venv .venv

# Activar el entorno (Windows)
.venv\Scripts\activate

# Activar el entorno (Mac/Linux)
source .venv/bin/activate

# Instalar dependencias
pip install -e .

# Configurar variables de entorno
copy .env.example .env
# Editá .env y completá ANTHROPIC_API_KEY con tu clave
```

## 3. Levantar el backend

```bash
# Desde la carpeta backend, con el entorno activado
uvicorn main:app --reload --port 8000
```

Verificar que funciona:
- `http://localhost:8000/` → debe devolver `{"message": "Onboarding Assistant API", "version": "0.1.0"}`
- `http://localhost:8000/api/v1/health` → debe devolver `{"status": "ok"}`
- `http://localhost:8000/docs` → Swagger UI con todos los endpoints

## 4. Configurar el frontend

```bash
cd ../frontend

# Instalar dependencias
npm install

# Configurar variables de entorno
copy .env.local.example .env.local
# El archivo ya tiene los valores correctos para desarrollo local
```

## 5. Levantar el frontend

```bash
npm run dev
```

Abrir `http://localhost:3000` en el browser.

## 6. Probar el flujo completo

Con los dos servicios corriendo:
1. Abrí `http://localhost:3000`
2. Escribí una pregunta en el chat, por ejemplo: *"¿Qué debo hacer durante mi primera semana?"*
3. El frontend llama al backend en `localhost:8000/api/v1/chat`
4. El backend llama a Claude API y devuelve la respuesta

## Estructura de puertos

| Servicio | Puerto local |
|---|---|
| Backend (FastAPI) | 8000 |
| Frontend (Next.js) | 3000 |

## Solución de problemas comunes

**Error: ANTHROPIC_API_KEY no configurada**
→ Verificar que el archivo `backend/.env` existe y tiene la clave completa.

**Error de CORS**
→ Verificar que `ALLOWED_ORIGINS=http://localhost:3000` está en `backend/.env`.

**El frontend no conecta con el backend**
→ Verificar que el backend está corriendo en el puerto 8000 y que `frontend/.env.local` tiene `NEXT_PUBLIC_API_URL=http://localhost:8000`.
