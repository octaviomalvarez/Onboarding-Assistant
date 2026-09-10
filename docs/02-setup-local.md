# Setup local — primeros pasos

Esta guía permite levantar el proyecto en una máquina nueva desde cero.

## Requisitos previos

- Python 3.11 o superior
- Node.js 18 o superior
- API key de Anthropic (`ANTHROPIC_API_KEY`) — **opcional**, el proveedor mock no la requiere

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

# Instalar dependencias core
pip install fastapi "uvicorn[standard]" python-dotenv pydantic httpx chromadb sentence-transformers
```

> Si querés usar Claude como LLM también instalá: `pip install anthropic`

## 3. Indexar los documentos de onboarding (RAG)

```bash
# Desde la carpeta backend, con el entorno activado
python -m rag.ingest
```

Esto carga los documentos de `data/docs/` en ChromaDB. La primera vez descarga el modelo de embeddings (~100 MB). Corré este comando cada vez que modifiques o agregues archivos en `data/docs/`.

## 4. Levantar el backend

```bash
# Proveedor mock (sin API key, para demo)
LLM_PROVIDER=mock uvicorn main:app --reload --port 8000

# Proveedor Claude (requiere ANTHROPIC_API_KEY)
ANTHROPIC_API_KEY=sk-... LLM_PROVIDER=anthropic uvicorn main:app --reload --port 8000
```

En Windows PowerShell:
```powershell
$env:PYTHONPATH = "."
$env:LLM_PROVIDER = "mock"
python -m uvicorn main:app --reload --port 8000
```

Verificar que funciona:
- `http://localhost:8000/` → `{"message": "Onboarding Assistant API", "version": "0.1.0"}`
- `http://localhost:8000/api/v1/health` → `{"status": "ok"}`
- `http://localhost:8000/docs` → Swagger UI

## 5. Configurar el frontend

```bash
cd ../frontend

# Instalar dependencias
npm install
```

## 6. Levantar el frontend

```bash
npm run dev
```

Abrir `http://localhost:3000` en el browser.

## 7. Probar el flujo completo

Con los dos servicios corriendo:
1. Abrí `http://localhost:3000`
2. Usá el widget flotante o la sección Asistente
3. Preguntá algo como: *"¿Qué debo hacer durante mi primera semana?"*
4. El frontend llama al backend → el backend busca en ChromaDB → devuelve la respuesta con contexto de los docs

## Proveedores de LLM disponibles

| Variable `LLM_PROVIDER` | Descripción | Requiere |
|---|---|---|
| `mock` (default) | Respuestas basadas en RAG + keyword matching | Nada |
| `anthropic` | Claude via Anthropic API | `ANTHROPIC_API_KEY` |
| `lmstudio` | Modelo local via LM Studio | LM Studio corriendo en puerto 1234 |

## Agregar documentos al asistente

1. Crear un archivo `.md` en `backend/data/docs/`
2. Correr `python -m rag.ingest` desde la carpeta `backend`

## Estructura de puertos

| Servicio | Puerto local |
|---|---|
| Backend (FastAPI) | 8000 |
| Frontend (Next.js) | 3000 |

## Solución de problemas comunes

**El frontend arranca en puerto 3001 en lugar de 3000**
→ Hay otro proceso usando el puerto 3000. En PowerShell: `Get-NetTCPConnection -LocalPort 3000 | ForEach-Object { Stop-Process -Id $_.OwningProcess -Force }`

**Error de CORS**
→ El frontend debe correr en el mismo puerto que `ALLOWED_ORIGINS` en el backend (por defecto `http://localhost:3000`).

**El asistente siempre responde con keyword matching (ignora los docs)**
→ Los documentos no están indexados. Correr `python -m rag.ingest` desde la carpeta `backend`.

**El frontend no conecta con el backend**
→ Verificar que el backend está corriendo en el puerto 8000 y que `NEXT_PUBLIC_API_URL=http://localhost:8000` en `frontend/.env.local`.
