from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()


class Contact(BaseModel):
    id: str
    name: str
    role: str
    email: str
    area: str


CONTACTS: list[Contact] = [
    Contact(id="1", name="María González", role="People Lead", email="maria.gonzalez@accenture.com", area="Recursos Humanos"),
    Contact(id="2", name="Carlos Ramírez", role="Tech Lead — Data Tower", email="carlos.ramirez@accenture.com", area="Data & Analytics"),
    Contact(id="3", name="Mesa de Ayuda IT", role="Soporte técnico", email="it.support@accenture.com", area="IT"),
    Contact(id="4", name="Laura Méndez", role="Responsable de Capacitaciones", email="laura.mendez@accenture.com", area="Learning & Development"),
    Contact(id="5", name="Diego Torres", role="Responsable de Accesos", email="diego.torres@accenture.com", area="IT Security"),
]


@router.get("/contacts", response_model=list[Contact])
def get_contacts():
    return CONTACTS
