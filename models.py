from typing import Optional, List
from sqlmodel import SQLModel, Field, Relationship, create_engine, Session
from sqlalchemy import ForeignKeyConstraint
import os

# Database connection
DATABASE_URL = "sqlite:///./baseball.db"
engine = create_engine(DATABASE_URL)

def create_db_and_tables():
    """Create all database tables"""
    SQLModel.metadata.create_all(engine)


def get_session():
    """Get a database session"""
    return Session(engine)


class People(SQLModel, table=True):
    """Baseball player information"""
    playerID: str = Field(primary_key=True)
    birthYear: Optional[int] = None
    birthMonth: Optional[int] = None
    birthDay: Optional[int] = None
    birthCity: Optional[str] = None
    birthCountry: Optional[str] = None
    birthState: Optional[str] = None
    deathYear: Optional[float] = None
    deathMonth: Optional[float] = None
    deathDay: Optional[float] = None
    deathCountry: Optional[str] = None
    deathState: Optional[str] = None
    deathCity: Optional[str] = None
    nameFirst: Optional[str] = None
    nameLast: Optional[str] = None
    nameGiven: Optional[str] = None
    weight: Optional[float] = None
    height: Optional[float] = None
    bats: Optional[str] = None
    throws: Optional[str] = None
    debut: Optional[str] = None
    bbrefID: Optional[str] = None
    finalGame: Optional[str] = None
    retroID: Optional[str] = None
    
    # Relationships
    batting_records: List["Batting"] = Relationship(back_populates="player")


class Teams(SQLModel, table=True):
    """Team season information"""
    yearID: int = Field(primary_key=True)
    teamID: str = Field(primary_key=True)
    lgID: Optional[str] = None
    franchID: Optional[str] = None
    divID: Optional[str] = None
    Rank: Optional[float] = None
    G: Optional[int] = None
    Ghome: Optional[float] = None
    W: Optional[int] = None
    L: Optional[int] = None
    DivWin: Optional[str] = None
    WCWin: Optional[str] = None
    LgWin: Optional[str] = None
    WSWin: Optional[str] = None
    R: Optional[int] = None
    AB: Optional[int] = None
    H: Optional[int] = None
    TwoB: Optional[int] = Field(None, alias="2B")
    ThreeB: Optional[int] = Field(None, alias="3B")
    HR: Optional[int] = None
    BB: Optional[int] = None
    SO: Optional[int] = None
    SB: Optional[int] = None
    CS: Optional[int] = None
    HBP: Optional[int] = None
    SF: Optional[int] = None
    RA: Optional[int] = None
    ER: Optional[int] = None
    ERA: Optional[float] = None
    CG: Optional[int] = None
    SHO: Optional[int] = None
    SV: Optional[int] = None
    IPouts: Optional[int] = None
    HA: Optional[int] = None
    HRA: Optional[int] = None
    BBA: Optional[int] = None
    SOA: Optional[int] = None
    E: Optional[int] = None
    DP: Optional[int] = None
    FP: Optional[float] = None
    name: Optional[str] = None
    park: Optional[str] = None
    attendance: Optional[float] = None
    BPF: Optional[int] = None
    PPF: Optional[int] = None
    teamIDBR: Optional[str] = None
    teamIDlahman45: Optional[str] = None
    teamIDretro: Optional[str] = None
    
    # Relationships
    batting_records: List["Batting"] = Relationship(back_populates="team")


class Batting(SQLModel, table=True):
    """Player batting statistics"""
    __table_args__ = (
        ForeignKeyConstraint(['yearID', 'teamID'], ['teams.yearID', 'teams.teamID']),
    )
    
    playerID: str = Field(foreign_key="people.playerID", primary_key=True)
    yearID: int = Field(primary_key=True)
    stint: int = Field(primary_key=True)
    teamID: str = Field(primary_key=False)
    lgID: Optional[str] = None
    G: Optional[int] = None
    AB: Optional[int] = None
    R: Optional[int] = None
    H: Optional[int] = None
    TwoB: Optional[int] = Field(None, alias="2B")
    ThreeB: Optional[int] = Field(None, alias="3B")
    HR: Optional[int] = None
    RBI: Optional[int] = None
    SB: Optional[int] = None
    CS: Optional[int] = None
    BB: Optional[int] = None
    SO: Optional[int] = None
    IBB: Optional[int] = None
    HBP: Optional[int] = None
    SH: Optional[int] = None
    SF: Optional[int] = None
    GIDP: Optional[int] = None
    
    # Relationships
    player: Optional[People] = Relationship(back_populates="batting_records")
    team: Optional[Teams] = Relationship(back_populates="batting_records")
