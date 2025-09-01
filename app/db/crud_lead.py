from typing import Iterable, Sequence
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.models.lead import Lead

def create_many(db: Session, leads: Iterable[dict]) -> int:
    objs = [Lead(**l) for l in leads]
    db.add_all(objs)
    db.commit()
    return len(objs)

def list_filtered(db: Session, location: str | None, min_budget: int | None, max_budget: int | None) -> Sequence[Lead]:
    stmt = select(Lead)
    if location:
        stmt = stmt.where(Lead.location.ilike(location))
    if min_budget is not None:
        stmt = stmt.where(Lead.budget >= min_budget)
    if max_budget is not None:
        stmt = stmt.where(Lead.budget <= max_budget)
    stmt = stmt.order_by(Lead.budget.desc())
    return db.execute(stmt).scalars().all()

def create_one(db: Session, data: dict) -> Lead:
    obj = Lead(**data)
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj
