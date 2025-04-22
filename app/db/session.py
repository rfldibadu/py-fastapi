from sqlmodel import SQLModel, create_engine, Session
from app.core.config import get_settings

settings = get_settings()

# ❌ Remove the hardcoded URL
# ✅ Use the value from .env via settings
engine = create_engine(settings.database_url, echo=True)

def get_session():
    with Session(engine) as session:
        yield session
