# init_db.py
from sqlmodel import SQLModel
from app.db.session import engine
from app.models import items, purchases

def init_db():
    SQLModel.metadata.create_all(engine)
    print("✅ Tables created!")

if __name__ == "__main__":
    init_db()