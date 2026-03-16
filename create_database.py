import pandas as pd
import sqlite3
import numpy as np

# Read the CSV files
people_df = pd.read_csv('people.csv')
teams_df = pd.read_csv('teams.csv')
batting_df = pd.read_csv('Batting.csv')

# Connect to database (creates it if it doesn't exist)
conn = sqlite3.connect('baseball.db')
cursor = conn.cursor()

# Disable foreign keys during development (will enable after data insertion)
cursor.execute('PRAGMA foreign_keys = OFF')

# Drop tables if they exist
cursor.execute('DROP TABLE IF EXISTS batting')
cursor.execute('DROP TABLE IF EXISTS teams')
cursor.execute('DROP TABLE IF EXISTS people')

# Create people table
cursor.execute('''
    CREATE TABLE people (
        playerID TEXT PRIMARY KEY,
        ID INTEGER,
        birthYear INTEGER,
        birthMonth INTEGER,
        birthDay INTEGER,
        birthCity TEXT,
        birthCountry TEXT,
        birthState TEXT,
        deathYear REAL,
        deathMonth REAL,
        deathDay REAL,
        deathCountry TEXT,
        deathState TEXT,
        deathCity TEXT,
        nameFirst TEXT,
        nameLast TEXT,
        nameGiven TEXT,
        weight REAL,
        height REAL,
        bats TEXT,
        throws TEXT,
        debut TEXT,
        bbrefID TEXT,
        finalGame TEXT,
        retroID TEXT
    )
''')

# Create teams table
cursor.execute('''
    CREATE TABLE teams (
        yearID INTEGER,
        lgID TEXT,
        teamID TEXT,
        franchID TEXT,
        divID TEXT,
        Rank REAL,
        G INTEGER,
        Ghome REAL,
        W INTEGER,
        L INTEGER,
        DivWin TEXT,
        WCWin TEXT,
        LgWin TEXT,
        WSWin TEXT,
        R INTEGER,
        AB INTEGER,
        H INTEGER,
        "2B" INTEGER,
        "3B" INTEGER,
        HR INTEGER,
        BB INTEGER,
        SO INTEGER,
        SB INTEGER,
        CS INTEGER,
        HBP INTEGER,
        SF INTEGER,
        RA INTEGER,
        ER INTEGER,
        ERA REAL,
        CG INTEGER,
        SHO INTEGER,
        SV INTEGER,
        IPouts INTEGER,
        HA INTEGER,
        HRA INTEGER,
        BBA INTEGER,
        SOA INTEGER,
        E INTEGER,
        DP INTEGER,
        FP REAL,
        name TEXT,
        park TEXT,
        attendance REAL,
        BPF INTEGER,
        PPF INTEGER,
        teamIDBR TEXT,
        teamIDlahman45 TEXT,
        teamIDretro TEXT,
        PRIMARY KEY (yearID, teamID)
    )
''')

# Create batting table
cursor.execute('''
    CREATE TABLE batting (
        playerID TEXT,
        yearID INTEGER,
        stint INTEGER,
        teamID TEXT,
        lgID TEXT,
        G INTEGER,
        AB INTEGER,
        R INTEGER,
        H INTEGER,
        "2B" INTEGER,
        "3B" INTEGER,
        HR INTEGER,
        RBI INTEGER,
        SB INTEGER,
        CS INTEGER,
        BB INTEGER,
        SO INTEGER,
        IBB INTEGER,
        HBP INTEGER,
        SH INTEGER,
        SF INTEGER,
        GIDP INTEGER,
        PRIMARY KEY (playerID, yearID, stint),
        FOREIGN KEY (playerID) REFERENCES people(playerID),
        FOREIGN KEY (yearID, teamID) REFERENCES teams(yearID, teamID)
    )
''')

# Replace NaN with None for proper NULL insertion
people_df = people_df.where(pd.notna(people_df), None)
teams_df = teams_df.where(pd.notna(teams_df), None)
batting_df = batting_df.where(pd.notna(batting_df), None)

# Insert people data
for _, row in people_df.iterrows():
    placeholders = ', '.join(['?' for _ in range(len(row))])
    cursor.execute(f'INSERT INTO people VALUES ({placeholders})', tuple(row))

# Insert teams data
for _, row in teams_df.iterrows():
    placeholders = ', '.join(['?' for _ in range(len(row))])
    cursor.execute(f'INSERT INTO teams VALUES ({placeholders})', tuple(row))

# Insert batting data
for _, row in batting_df.iterrows():
    placeholders = ', '.join(['?' for _ in range(len(row))])
    cursor.execute(f'INSERT INTO batting VALUES ({placeholders})', tuple(row))

conn.commit()

# Re-enable foreign keys for data integrity going forward
cursor.execute('PRAGMA foreign_keys = ON')

conn.close()

print("✓ Database created successfully: baseball.db")
print(f"  - people table: {len(people_df)} rows")
print(f"  - teams table: {len(teams_df)} rows")
print(f"  - batting table: {len(batting_df)} rows")
print("\nSchema:")
print("  - people: Primary key = playerID")
print("  - teams: Primary key = (yearID, teamID)")
print("  - batting: Primary key = (playerID, yearID, stint)")
print("  - batting.playerID → people.playerID")
print("  - batting.(yearID, teamID) → teams.(yearID, teamID)")
