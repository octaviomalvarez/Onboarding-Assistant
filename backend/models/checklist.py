from sqlmodel import SQLModel, Field
from typing import Literal

ChecklistCategory = Literal["accesos", "capacitaciones", "administrativo", "equipo"]


class ChecklistItemDB(SQLModel, table=True):
    __tablename__ = "checklist_items"

    id: str = Field(primary_key=True)
    title: str
    description: str
    category: str
    week: int
    completed: bool = False
    due_day: int
    roles: str = ""


SEED_ITEMS = [
    {"id": "1", "title": "Completar el formulario de datos personales en MyHR", "description": "Ingresar a MyHR y completar el perfil con datos de contacto, dirección y documentación.", "category": "administrativo", "week": 1, "completed": False, "due_day": 1, "roles": ""},
    {"id": "2", "title": "Solicitar acceso a MyTE (carga de horas)", "description": "Enviar solicitud de acceso a través del portal de herramientas. El tiempo de aprobación es de 1-2 días hábiles.", "category": "accesos", "week": 1, "completed": False, "due_day": 1, "roles": ""},
    {"id": "3", "title": "Completar el curso de Code of Business Ethics", "description": "Curso obligatorio disponible en el portal de capacitaciones. Duración aproximada: 45 minutos.", "category": "capacitaciones", "week": 1, "completed": False, "due_day": 3, "roles": ""},
    {"id": "4", "title": "Reunión de bienvenida con tu People Lead", "description": "Coordinar fecha y horario con tu People Lead para la reunión de incorporación.", "category": "equipo", "week": 1, "completed": False, "due_day": 2, "roles": ""},
    {"id": "5", "title": "Solicitar acceso a los repositorios del proyecto", "description": "Pedirle al Tech Lead del proyecto que te agregue a los repos de GitHub/Azure DevOps.", "category": "accesos", "week": 1, "completed": False, "due_day": 3, "roles": "Data Engineer,Data Scientist,Senior,Lead"},
    {"id": "6", "title": "Configurar VPN corporativa", "description": "Instalar y configurar el cliente de VPN siguiendo la guía de IT. Contactar a soporte si hay problemas.", "category": "accesos", "week": 1, "completed": False, "due_day": 2, "roles": ""},
    {"id": "7", "title": "Completar el curso de Data Privacy & Security", "description": "Capacitación obligatoria para todos los empleados de la torre de Data.", "category": "capacitaciones", "week": 2, "completed": False, "due_day": 8, "roles": ""},
    {"id": "8", "title": "Cargar tus primeras horas en MyTE", "description": "Registrar las horas trabajadas de la primera semana antes del cierre del viernes.", "category": "administrativo", "week": 2, "completed": False, "due_day": 8, "roles": ""},
    {"id": "9", "title": "Presentarte con el equipo del proyecto", "description": "Coordinar una sesión corta de presentación con el equipo completo del proyecto asignado.", "category": "equipo", "week": 2, "completed": False, "due_day": 9, "roles": ""},
    {"id": "10", "title": "Solicitar acceso a las herramientas del proyecto", "description": "Gestionar accesos a las herramientas específicas del proyecto (Jira, Confluence, ambientes de desarrollo).", "category": "accesos", "week": 2, "completed": False, "due_day": 10, "roles": ""},
    {"id": "11", "title": "Configurar entorno local de desarrollo", "description": "Instalar Python 3.10+, Git, VS Code/PyCharm, Azure CLI y Databricks CLI según la guía técnica.", "category": "accesos", "week": 1, "completed": False, "due_day": 3, "roles": "Data Engineer,Data Scientist"},
    {"id": "12", "title": "Revisión técnica inicial con el Tech Lead", "description": "Reunión técnica para entender la arquitectura del proyecto y el stack de herramientas.", "category": "equipo", "week": 1, "completed": False, "due_day": 3, "roles": "Data Engineer,Data Scientist,Senior,Lead"},
]
