from fastapi import APIRouter
from pydantic import BaseModel
from typing import Literal

router = APIRouter()

ChecklistCategory = Literal["accesos", "capacitaciones", "administrativo", "equipo"]


class ChecklistItem(BaseModel):
    id: str
    title: str
    description: str
    category: ChecklistCategory
    week: Literal[1, 2]
    completed: bool
    due_day: int


ITEMS: list[ChecklistItem] = [
    ChecklistItem(id="1", title="Completar formulario de datos personales en MyHR", description="Ingresar a MyHR y completar el perfil con datos de contacto, dirección y documentación.", category="administrativo", week=1, completed=False, due_day=1),
    ChecklistItem(id="2", title="Solicitar acceso a MyTE (carga de horas)", description="Enviar solicitud de acceso a través del portal de herramientas.", category="accesos", week=1, completed=False, due_day=1),
    ChecklistItem(id="3", title="Completar el curso de Code of Business Ethics", description="Curso obligatorio disponible en el portal de capacitaciones. Duración: 45 minutos.", category="capacitaciones", week=1, completed=False, due_day=3),
    ChecklistItem(id="4", title="Reunión de bienvenida con tu People Lead", description="Coordinar fecha y horario con tu People Lead.", category="equipo", week=1, completed=False, due_day=2),
    ChecklistItem(id="5", title="Solicitar acceso a los repositorios del proyecto", description="Pedirle al Tech Lead que te agregue a los repos.", category="accesos", week=1, completed=False, due_day=3),
    ChecklistItem(id="6", title="Configurar VPN corporativa", description="Instalar y configurar el cliente de VPN siguiendo la guía de IT.", category="accesos", week=1, completed=False, due_day=2),
    ChecklistItem(id="7", title="Completar el curso de Data Privacy & Security", description="Capacitación obligatoria para todos los empleados de la torre de Data.", category="capacitaciones", week=2, completed=False, due_day=8),
    ChecklistItem(id="8", title="Cargar tus primeras horas en MyTE", description="Registrar las horas trabajadas de la primera semana.", category="administrativo", week=2, completed=False, due_day=8),
    ChecklistItem(id="9", title="Presentarte con el equipo del proyecto", description="Coordinar una sesión corta de presentación con el equipo completo.", category="equipo", week=2, completed=False, due_day=9),
    ChecklistItem(id="10", title="Solicitar acceso a las herramientas del proyecto", description="Gestionar accesos a Jira, Confluence y ambientes de desarrollo.", category="accesos", week=2, completed=False, due_day=10),
]


@router.get("/checklist", response_model=list[ChecklistItem])
def get_checklist():
    return ITEMS
