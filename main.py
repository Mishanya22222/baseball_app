from fastapi.staticfiles import StaticFiles
from fastapi import FastAPI
from sqlmodel import Session, select
from models import Batting, Teams, People, engine, create_db_and_tables

# Initialize database
create_db_and_tables()

app = FastAPI()


@app.get("/years")
def get_years():
    with Session(engine) as session:
        result = session.exec(select(Teams.yearID).distinct().order_by(Teams.yearID))
        return result.all()

@app.get("/teams")
def get_teams(year: int):
    with Session(engine) as session:
        result = session.exec(select(Teams.teamID, Teams.name).where(Teams.yearID == year).order_by(Teams.name))
        return [{'teamID': row[0], 'name': row[1]} for row in result.all()]


@app.get("/players")
def get_players(year: int, teamID: str):
    with Session(engine) as session:
        result = session.exec(
            select(People.nameFirst, People.nameLast)
            .join(Batting, Batting.playerID == People.playerID)
            .where(Batting.yearID == year, Batting.teamID == teamID)
            .distinct()
            .order_by(People.nameLast, People.nameFirst)
        )
        return [{"first": row[0], "last": row[1]} for row in result.all()]

app.mount("/", StaticFiles(directory="static", html=True), name="static")