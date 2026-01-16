#The Universal Pokédex - SQLite3 Database

#---------------------------imports----------------------------#
import sqlite3
import hashlib   #use for password hashing
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
            UserID INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
            Username TEXT NOT NULL UNIQUE,
            Password TEXT NOT NULL
            );
    """
    tblDexCreate = """
        CREATE TABLE IF NOT EXISTS tblDex (
            DexID INTEGER NOT NULL PRIMARY KEY,
            Gen INTEGER NOT NULL,
            Version TEXT NOT NULL
            );
    """
    tblMonCreate = """
        CREATE TABLE IF NOT EXISTS tblMon (
            MonID INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
            DexNum INTEGER,
            MonName TEXT,
            Species TEXT,
            Type1 TEXT,
            Type2 TEXT,
            Height REAL,
            Weight REAL,
            BST INTEGER,
            CatchRate INTEGER,
            EggGroups TEXT,
            Gender REAL,
            EggCycle INTEGER,
            Evo TEXT,
            PreEvo TEXT,
            FlavorText TEXT,
            Location TEXT,
            Sprite BLOB
            );
    """
    tblDexMonCreate = """
        CREATE TABLE IF NOT EXISTS tblDexMon (
            DexMonID INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
            DexID INTEGER NOT NULL,
            MonID INTEGER NOT NULL,
            MonGen INTEGER,
            Moves TEXT,
            Ability TEXT,
            CONSTRAINT fkDexID
                FOREIGN KEY (DexID)
                REFERENCES tblDex(DexID),
            CONSTRAINT fkMonID
                FOREIGN KEY (MonID)
                REFERENCES tblMon(MonID)
            );
    """
    tblUserDexMonCreate = """
        CREATE TABLE IF NOT EXISTS tblUserDexMon (
            UserID INTEGER NOT NULL,
            DexMonID INTEGER NOT NULL,
            HP INTEGER,
            Atk INTEGER,
            Def INTEGER,
            SpA INTEGER,
            SpD INTEGER,
            Spe INTEGER,
            CONSTRAINT fkUserID
                FOREIGN KEY (UserID)
                REFERENCES tblUser(UserID),
            CONSTRAINT fkDexMonID
                FOREIGN KEY (DexMonID)
                REFERENCES tblDexMon(DexMonID)
            );
    """

    curs.execute(tblUserCreate)
    curs.execute(tblDexCreate)
    curs.execute(tblMonCreate)
    curs.execute(tblDexMonCreate)
    curs.execute(tblUserDexMonCreate)

    conn.commit()
    conn.close()

#add a user to tblUser
def addUser(username, password):
    hashedPass = hashlib.sha256(password.encode()).hexdigest()
    #connects to database
    conn = sqlite3.connect('TUP.db')
    curs = conn.cursor()

    curs.execute('''
        INSERT INTO tblUser (Username, Password)
        VALUES (?, ?)
        ''',
        (username, hashedPass)
    )

    conn.commit()
    conn.close()

#add a Pokédex to tblDex
def addDex(dexID, gen, version):
    #connects to database
    conn = sqlite3.connect('TUP.db')
    curs = conn.cursor()

    curs.execute('''
        INSERT INTO tblDex (DexID, Gen, Version)
        VALUES (?, ?, ?)
        ''',
        (dexID, gen, version)
    )

    conn.commit()
    conn.close()

#add a Pokémon to tblMon
def addMon(dexNum, monName, species, type1, type2, height, weight, BST, catchRate, eggGroups, gender, eggCycle, evo, preEvo, flavorText, location, sprite):
    #connects to database
    conn = sqlite3.connect('TUP.db')
    curs = conn.cursor()

    curs.execute('''
        INSERT INTO tblMon (DexNum, MonName, Species, Type1, Type2, Height, Weight, BST, CatchRate, EggGroups, Gender, EggCycle, Evo, PreEvo, FlavorText, Location, Sprite)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''',
        (dexNum, monName, species, type1, type2, height, weight, BST, catchRate, eggGroups, gender, eggCycle, evo, preEvo, flavorText, location, sprite)
    )

    conn.commit()
    conn.close()

#add dexMon entry to tblDexMon
def addDexMon(dexID, monID, monGen, moves, ability):
    #connects to database
    conn = sqlite3.connect('TUP.db')
    curs = conn.cursor()

    curs.execute('''
        INSERT INTO tblDexMon (DexID, MonID, MonGen, Moves, Ability)
        VALUES (?, ?, ?, ?, ?)
        ''',
        (dexID, monID, monGen, moves, ability)
    )

    conn.commit()
    conn.close()

#add userDexMon entry to tblUserDexMon
def addUserDexMon(userID, dexMonID, HP, Atk, Def, SpA, SpD, Spe):
    #connects to database
    conn = sqlite3.connect('TUP.db')
    curs = conn.cursor()

    curs.execute('''
        INSERT INTO tblUserDexMon (UserID, DexMonID, HP, Atk, Def, SpA, SpD, Spe)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''',
        (userID, dexMonID, HP, Atk, Def, SpA, SpD, Spe)
    ) 

    conn.commit()
    conn.close()

#searching for Pokémon, returns MonIDs of all appropriate Pokémon
def searchMon(criteria):    
    #criteria is a dictionary of search criteria used for searching/filtering
    #criteria is from:
    #type1, type2, height class, weight class, bst range
    outMonIDs = []

    #connects to database
    conn = sqlite3.connect('TUP.db')
    curs = conn.cursor()
    
    curs.execute('''
        SELECT MonID
        FROM tblMon
        WHERE Type1 = ? AND Type2 = ? 
            AND Height >= ? AND Height < ? 
            AND Weight >= ? AND Weight < ? AND  
            BST >= ? AND BST < ?
    ''',
    (criteria['type1'], criteria['type2'], criteria['heightMin'], criteria['heightMax'], criteria['weightMin'], criteria['weightMax'], criteria['bstMin'], criteria['bstMax']
    ))

    outMonIDs = curs.fetchall()

    conn.commit()
    conn.close()

    return outMonIDs

def returnMon(monID):   #returns the details of a single Pokémon from the database
    #connects to database
    conn = sqlite3.connect('TUP.db')
    curs = conn.cursor()

    curs.execute('''
    SELECT *
    FROM tblMon
    WHERE MonID = ?
    ''',
    (monID,)
    )

    result = curs.fetchone()

    conn.commit()
    conn.close()

    return result

def checkLogin(username, password):
    hashedPass = hashlib.sha256(password.encode()).hexdigest()

    #connects to database
    conn = sqlite3.connect('TUP.db')
    curs = conn.cursor()

    curs.execute('''
        SELECT UserID, Password
        FROM tblUser
        WHERE Username = ?
    ''',
    (username,)
    )

    result = curs.fetchone()
    conn.close()
    
    storedUserID, storedHash = result

    if result is None:
        return False, None

    if storedHash == hashedPass:
        return True, storedUserID
    else:
        return False, None
    


#------------------------------------#
#TUPitems.outMon()