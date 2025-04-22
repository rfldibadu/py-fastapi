from sqlmodel import Session, text
from app.db.session import engine  # Adjust if your import path is different


def test_engine_connection():
    try:
        with engine.connect() as connection:
            result = connection.execute(text("SELECT 1")).scalar()
            print("✅ Connected successfully!", result)
    except Exception as e:
        print("❌ Connection failed:", e)

if __name__ == "__main__":
    test_engine_connection()