from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlmodel import Session, select
from typing import Literal

from database import get_session
from models.checklist import ChecklistItemDB, SEED_ITEMS

router = APIRouter()

ChecklistCategory = Literal["accesos", "capacitaciones", "administrativo", "equipo"]


class ChecklistItemResponse(BaseModel):
    id: str
    title: str
    description: str
    category: ChecklistCategory
    week: Literal[1, 2]
    completed: bool
    dueDay: int
    roles: str = ""

    model_config = {"populate_by_name": True}


class ChecklistUpdate(BaseModel):
    completed: bool


@router.get("/checklist", response_model=list[ChecklistItemResponse])
def get_checklist(role: str | None = None, session: Session = Depends(get_session)):
    items = session.exec(select(ChecklistItemDB)).all()
    if not items:
        for seed in SEED_ITEMS:
            session.add(ChecklistItemDB(**seed))
        session.commit()
        items = session.exec(select(ChecklistItemDB)).all()

    if role:
        items = [i for i in items if not i.roles or role in i.roles.split(",")]

    return [
        ChecklistItemResponse(
            id=i.id,
            title=i.title,
            description=i.description,
            category=i.category,
            week=i.week,
            completed=i.completed,
            dueDay=i.due_day,
            roles=i.roles,
        )
        for i in items
    ]


@router.put("/checklist/{item_id}", response_model=ChecklistItemResponse)
def update_checklist_item(item_id: str, body: ChecklistUpdate, session: Session = Depends(get_session)):
    item = session.get(ChecklistItemDB, item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item no encontrado")
    item.completed = body.completed
    session.add(item)
    session.commit()
    session.refresh(item)
    return ChecklistItemResponse(
        id=item.id,
        title=item.title,
        description=item.description,
        category=item.category,
        week=item.week,
        completed=item.completed,
        dueDay=item.due_day,
        roles=item.roles,
    )
