from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.db.crud_lead import create_many

SEED = [
    {"id": 1, "name": "Ana Pérez", "location": "Bogota", "budget": 250000},
    {"id": 2, "name": "Luis Gómez", "location": "Medellin", "budget": 180000},
    {"id": 3, "name": "María Ruiz", "location": "Bogota", "budget": 320000},
    {"id": 4, "name": "Carlos López", "location": "Cali", "budget": 150000},
    {"id": 5, "name": "Sofía Ríos", "location": "Bogota", "budget": 450000},
]

def main():
    db: Session = SessionLocal()
    try:
        n = create_many(db, SEED)
        print(f"{n} leads insertados")
    finally:
        db.close()

if __name__ == "__main__":
    main()
