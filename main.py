from fastapi.staticfiles import StaticFiles
from fastapi import FastAPI
from sqlmodel import Session, select
from models import Batting, Teams, People, engine, create_db_and_tables
from sqlalchemy import text

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
            select(People.playerID, People.nameFirst, People.nameLast)
            .join(Batting, Batting.playerID == People.playerID)
            .where(Batting.yearID == year, Batting.teamID == teamID)
            .distinct()
            .order_by(People.nameLast, People.nameFirst)
        )
        return [{"playerID": row[0], "first": row[1], "last": row[2]} for row in result.all()]


@app.get("/player/{playerID}")
def get_player_details(playerID: str):
    with Session(engine) as session:
        # player bio
        player = session.exec(select(People).where(People.playerID == playerID)).first()
        if not player:
            return {"error": "Player not found"}

        # batting records (use raw SQL to handle column names like "2B" and "3B")
        sql = text('SELECT yearID, teamID, G, AB, R, H, "2B", "3B", HR, RBI, BB, SO, SB FROM batting WHERE playerID = :pid ORDER BY yearID DESC')
        rows = session.execute(sql, {"pid": playerID}).fetchall()

        batting = []
        for r in rows:
            # r is a tuple-like row: (yearID, teamID, G, AB, R, H, TwoB, ThreeB, HR, RBI, BB, SO, SB)
            # resolve team name if available
            team_name = None
            team_row = session.exec(select(Teams.name).where(Teams.yearID == r[0], Teams.teamID == r[1])).first()
            team_name = team_row if team_row else r[1]

            batting.append({
                "year": r[0],
                "team": team_name,
                "games": r[2],
                "atBats": r[3],
                "runs": r[4],
                "hits": r[5],
                "doubles": r[6],
                "triples": r[7],
                "homeRuns": r[8],
                "rbi": r[9],
                "walks": r[10],
                "strikeouts": r[11],
                "stolenBases": r[12]
            })

        return {
            "playerID": player.playerID,
            "name": f"{player.nameFirst} {player.nameLast}",
            "birthYear": player.birthYear,
            "birthCity": player.birthCity,
            "birthCountry": player.birthCountry,
            "bats": player.bats,
            "throws": player.throws,
            "debut": player.debut,
            "height": player.height,
            "weight": player.weight,
            "battingRecords": batting
        }

app.mount("/", StaticFiles(directory="static", html=True), name="static")