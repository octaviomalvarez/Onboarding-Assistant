# RAG — Asistente con documentación interna

## Qué es el RAG y por qué lo usamos

RAG (Retrieval Augmented Generation) permite que el asistente responda preguntas basándose en documentación interna real, en lugar de usar solo el conocimiento general del modelo de lenguaje.

Sin RAG: el asistente responde de forma genérica.
Con RAG: el asistente responde con información específica de Accenture — procesos, contactos, herramientas y procedimientos reales.

## Cómo funciona el pipeline

```
Pregunta del empleado
    │
    ▼
Embedding de la pregunta (sentence-transformers, local)
    │
    ▼
Búsqueda de chunks similares en ChromaDB
    │
    ▼
Top 3 chunks más relevantes
    │
    ▼
Prompt: system + contexto + pregunta → Claude API
    │
    ▼
Respuesta basada en documentación interna
```

## Estructura de archivos

```
backend/
├── data/
│   └── docs/                    ← Documentos fuente en Markdown
│       ├── faq.md
│       ├── accesos.md
│       ├── capacitaciones.md
│       └── herramientas-data.md
├── rag/
│   ├── loader.py                ← Lee y chunksea los .md
│   ├── store.py                 ← Configura ChromaDB + embeddings
│   ├── retriever.py             ← Busca chunks relevantes
│   └── ingest.py                ← Script para indexar documentos
└── chroma_db/                   ← Base de datos vectorial (generada, no en git)
```

## Cómo indexar los documentos

Antes de usar el asistente con RAG, hay que indexar los documentos:

```bash
cd backend
# Con el entorno virtual activado:
python -m rag.ingest
```

La primera vez descarga el modelo de embeddings (~420MB). Las siguientes veces es instantáneo.

Hay que volver a correr este script cada vez que se agregue o modifique un documento en `data/docs/`.

## Cómo agregar documentación nueva

1. Crear un archivo `.md` en `backend/data/docs/`
2. Usar `##` para separar secciones (cada sección se convierte en un chunk)
3. Correr `python -m rag.ingest`

Ejemplo de estructura recomendada:

```markdown
# Título del documento

## Pregunta o sección 1

Contenido de la sección...

## Pregunta o sección 2

Contenido de la sección...
```

## Modelo de embeddings

Usamos `paraphrase-multilingual-MiniLM-L12-v2` de sentence-transformers:
- Multilingüe (español incluido)
- Corre 100% local, sin API key
- ~420MB, se descarga automáticamente la primera vez
- Buena calidad para búsqueda semántica en este dominio

## Limitaciones actuales

- Los documentos son de ejemplo — deben reemplazarse con información real de Accenture
- ChromaDB corre local (en el servidor). Para producción migrar a Azure AI Search o similar
- No hay historial de conversación — cada pregunta es independiente
