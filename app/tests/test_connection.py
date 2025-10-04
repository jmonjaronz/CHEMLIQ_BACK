# app/tests/test_connection.py
from sqlalchemy import text
from app.db.session import engine

def test_connection():
    try:
        with engine.connect() as connection:
            result = connection.execute(text("SELECT SYSDATE FROM dual"))
            print("✅ Conexión exitosa:", result.scalar())
    except Exception as e:
        print("❌ Error de conexión:", e)

if __name__ == "__main__":
    test_connection()