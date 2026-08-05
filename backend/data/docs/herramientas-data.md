# Herramientas de la Torre de Data

## Stack tecnológico principal

La Torre de Data de Accenture trabaja principalmente con las siguientes tecnologías:

**Cloud**
- Microsoft Azure (plataforma principal)
- AWS (en algunos proyectos de clientes)
- Google Cloud Platform (en algunos proyectos de clientes)

**Ingeniería de datos**
- Azure Data Factory — orquestación y pipelines ETL/ELT
- Databricks — procesamiento distribuido con Spark
- Azure Synapse Analytics — data warehouse y analytics
- dbt — transformaciones SQL con control de versiones
- Apache Airflow — orquestación de workflows (proyectos legacy)

**Analytics y visualización**
- Power BI — visualización y reportes para clientes
- Tableau — en algunos proyectos de clientes
- Looker — en algunos proyectos de clientes

**Lenguajes y herramientas de desarrollo**
- Python — lenguaje principal para data engineering y ML
- SQL — para transformaciones y consultas
- PySpark — para procesamiento distribuido en Databricks
- Git — control de versiones (GitHub o Azure DevOps según proyecto)

**Colaboración y gestión**
- Microsoft Teams — comunicación del equipo
- Confluence — documentación técnica
- Jira / Azure DevOps Boards — gestión de tareas y sprints
- SharePoint — documentación corporativa

## Configuración del entorno local

Para la mayoría de los proyectos en la Torre de Data necesitás tener instalado:

1. **Python 3.10 o superior** con entornos virtuales (venv o conda)
2. **Git** con acceso a los repositorios del proyecto
3. **VS Code** o PyCharm como IDE (VS Code es el más usado en el equipo)
4. **Azure CLI** para interactuar con servicios de Azure
5. **Databricks CLI** si el proyecto usa Databricks

## Repositorios y código

El código de los proyectos vive en GitHub (proyectos internos) o Azure DevOps (proyectos de clientes). Para acceder necesitás que el Tech Lead del proyecto te agregue al repositorio correspondiente.

La convención de branching más usada en el equipo es GitFlow o trunk-based development según el proyecto.

## Comunicación del equipo

- Los canales de Teams del proyecto son el principal medio de comunicación
- Usamos reuniones de standup diario (15 minutos) la mayoría de los proyectos
- Las decisiones técnicas importantes se documentan en Confluence
- Para preguntas rápidas, Teams es más rápido que el email

## ¿A quién le pregunto si tengo dudas técnicas?

- **Tu Tech Lead** — primer contacto para dudas del proyecto
- **Tu Buddy** — si fue asignado, es tu referente informal para preguntas del día a día
- **Canales de Teams de la Torre de Data** — para preguntas generales de tecnología
- **Tu People Lead** — para temas de carrera y desarrollo profesional
