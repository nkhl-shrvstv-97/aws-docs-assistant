from sqlalchemy import text
from backend.app.db.session import engine, Base
# Import models to ensure they are registered with Base
from backend.app.db.models import DocumentChunk, SessionSummary

def init_database():
    print("Initializing database...")
    try:
        with engine.connect() as conn:
            # Create extension if not exists
            print("Creating vector extension if not exists...")
            conn.execute(text("CREATE EXTENSION IF NOT EXISTS vector;"))
            conn.commit()
        
        print("Creating all tables...")
        Base.metadata.create_all(bind=engine)
        print("Database initialized successfully!")
    except Exception as e:
        print(f"Error initializing database: {e}")

if __name__ == "__main__":
    init_database()
