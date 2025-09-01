from sqlalchemy import text
from app.db.session import engine
from app.models.lead import Base

def init():
    Base.metadata.create_all(bind=engine)
    with engine.begin() as conn:
        conn.execute(text("CREATE INDEX IF NOT EXISTS idx_leads_location ON leads (location);"))

if __name__ == "__main__":
    init()
    print("Tablas inicializadas")
