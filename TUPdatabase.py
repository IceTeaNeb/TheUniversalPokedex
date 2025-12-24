#The Universal Pokédex - SQLite3 Database

#---------------------------imports----------------------------#
import sqlite3
import bcrypt   #use for password hashing
import TUPitems

#--------------------------------------------------------------#

#creating database
def createDatabase():
    #connects to database
    conn = sqlite3.connect('TUP.db')
    curs = conn.cursor()

    curs.execute('PRAGMA foreign_keys = ON')

    #creating tables with their attributes and keys
    tblUserCreate = """
        CREATE TABLE IF NOT EXISTS tblUser (
            UserID INT NOT NULL PRIMARY KEY AUTOINCREMENT,
            Username TEXT NOT NULL,
            Password TEXT NOT NULL,
            Salt TEXT NOT NULL
            );
    """
    tblDexCreate = """
        CREATE TABLE IF NOT EXISTS tblDex (
            DexID INT NOT NULL PRIMARY KEY,
            Gen INT NOT NULL,
            Version TEXT NOT NULL,
            );
    """
    tblMonCreate = """
        CREATE TABLE IF NOT EXISTS tblMon (
            MonID INT NOT NULL PRIMARY KEY,
            MonName TEXT,
            Species TEXT,
            Type1 TEXT,
            Type2 TEXT,
            Height REAL,
            Weight REAL,
            BST INT,
            CatchRate INT,
            EggGroups TEXT,
            Gender REAL,
            EggCycle INT,
            Evo TEXT,
            PreEvo TEXT,
            FlavorText TEXT,
            Location TEXT
            );
    """
    tblDexMonCreate = """
        CREATE TABLE IF NOT EXISTS tblDexMon (
            DexMonID INT NOT NULL PRIMARY KEY,
            DexID INT NOT NULL,
            MonID INT NOT NULL,
            MonGen INT,
            Moves TEXT,
            Ability TEXT,
            CONSTRAINT fkDexID
                FOREIGN KEY (DexID)
                REFERENCES tblDex(DexID)
            CONSTRAINT fkMonID
                FOREIGN KEY (MonID)
                REFERENCES tblMon(MonID)
            );
    """
    tblUserDexMonCreate = """
        CREATE TABLE IF NOT EXISTS tblUserDexMon (
            UserID INT NOT NULL,
            DexMonID INT NOT NULL,
            HP INT,
            Atk INT,
            Def INT,
            SpA INT,
            SpD INT,
            Spe INT
            CONSTRAINT fkUserID
                FOREIGN KEY (UserID)
                REFERENCES tblUser(UserID)
            CONSTRAINT fkDexMonID
                FOREIGN KEY (DexMonID)
                REFERENCES tblDexMon(DexMonID)
            );
    """

    cursor.execute(tblUserCreate)
    cursor.execute(tblDexCreate)
    cursor.execute(tblMonCreate)
    cursor.execute(tblDexMonCreate)
    cursor.execute(tblUserDexMonCreate)

    conn.commit()
    conn.close()

#updating database
def updateDatabase():
    pass

#------------------------------------#
TUPitems.outMon()