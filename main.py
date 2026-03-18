from fastapi.staticfiles import StaticFiles
from fastapi import FastAPI
from sqlmodel import Session, select
from models import engine, Batting, People, Teams, create_db_and_tables
import sqlite3

app = FastAPI()

# Initialize database tables on startup
@app.on_event("startup")
def on_startup():
    try:
        # Create tables using SQLModel
        create_db_and_tables()
        print("✓ Database tables initialized")
    except Exception as e:
        print(f"✗ Error initializing database: {e}")

@app.get("/years")
async def get_years():
    try:
        with Session(engine) as session:
            # Query using raw SQL to ensure compatibility with existing database
            years = session.exec(select(Teams.yearID).distinct().order_by(Teams.yearID)).all()
            
            # If empty, try raw SQL query
            if not years:
                conn = sqlite3.connect("baseball.db")
                cursor = conn.cursor()
                cursor.execute("SELECT DISTINCT yearID FROM teams ORDER BY yearID")
                years = [row[0] for row in cursor.fetchall()]
                conn.close()
            
            return sorted(set(years)) if years else []
    except Exception as e:
        print(f"Error fetching years: {e}")
        # Fallback: try to get years from raw SQL
        try:
            conn = sqlite3.connect("baseball.db")
            cursor = conn.cursor()
            cursor.execute("SELECT DISTINCT yearID FROM teams ORDER BY yearID")
            years = [row[0] for row in cursor.fetchall()]
            conn.close()
            return sorted(set(years)) if years else []
        except Exception as e2:
            print(f"Fallback error: {e2}")
            return []

app.mount("/", StaticFiles(directory="static", html=True), name="static")