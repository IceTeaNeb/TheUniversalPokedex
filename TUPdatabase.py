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
            SpriteURL TEXT
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

#migrate database schema
def migrateDatabase():
    conn = sqlite3.connect('TUP.db')
    curs = conn.cursor()
    
    # Check if SpriteURL column exists in tblMon
    curs.execute("PRAGMA table_info(tblMon)")
    columns = [column[1] for column in curs.fetchall()]
    
    if 'SpriteURL' not in columns:
        curs.execute('ALTER TABLE tblMon ADD COLUMN SpriteURL TEXT')
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
        INSERT INTO tblMon (DexNum, MonName, Species, Type1, Type2, Height, Weight, BST, CatchRate, EggGroups, Gender, EggCycle, Evo, PreEvo, FlavorText, Location, SpriteURL)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''',
        (dexNum, monName, species, type1, type2, height, weight, BST, catchRate, eggGroups, gender, eggCycle, evo, preEvo, flavorText, location, sprite)
    )

    monID = curs.lastrowid

    conn.commit()
    conn.close()

    return monID

#add dexMon entry to tblDexMon, also returns dexMonID
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

    dexMonID = curs.lastrowid

    conn.commit()
    conn.close()

    return dexMonID

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

def addMonFull(userID, dexID, monGen, monData, moves="", ability="", stats=None):
    #monData is dictionary with keys:
    #dexNum, monName, species, type1, type2, height, weight, bst, catchRate, 
    #eggGroups, gender, eggCycle, evo, preEvo, flavorText, location, spriteURL

    #stats is dictionary with keys:
    #HP, Atk, Def, SpA, SpD, Spe

    monID = getMonIDByDexNum(monData["dexNum"])

    if monID is None:
        addMon(
            monData["dexNum"], monData["monName"], monData["species"], monData["type1"],
            monData["type2"], monData["height"], monData["weight"], monData["bst"],
            monData["catchRate"], monData["eggGroups"], monData["gender"], monData["eggCycle"],
            monData["evo"], monData["preEvo"], monData["flavorText"], monData["location"],
            monData["spriteURL"],
        )
        monID = getMonIDByDexNum(monData["dexNum"])

    dexMonID = addDexMon(dexID, monID, monGen, moves, ability)

    if stats is None:
        stats = {'HP': None, 'Atk': None, 'Def': None, 'SpA': None, 'SpD': None, 'Spe': None}
    
    addUserDexMon(userID, dexMonID, stats['HP'], stats['Atk'], stats['Def'], stats['SpA'], stats['SpD'], stats['Spe'])

    return monID, dexMonID


#searching for Pokémon that match search/filter
def searchMonsForButtons(criteria):    
    #criteria is a dictionary of search criteria used for searching/filtering
    #criteria is from:
    #type1, type2, height class, weight class, bst range

    #connects to database
    conn = sqlite3.connect('TUP.db')
    curs = conn.cursor()

    #list for each part of WHERE in sql
    partsWHERE = []
    #list for holding values for ? placeholders
    parameters = []

    #name criteria
    if criteria.get('name'):
        partsWHERE.append('MonName LIKE ?') #LIKE is for partial matching
        parameters.append(f"%{criteria['name']}%")
    
    #type1 criteria
    if criteria.get('type1'):
        partsWHERE.append('Type1 = ?')
        parameters.append(criteria['type1'])

    #type2 criteria
    if criteria.get('type2'):
        partsWHERE.append('Type2 = ?')
        parameters.append(criteria['type2'])

    #bstMin criteria
    if criteria.get('bstMin') is not None:
        partsWHERE.append('BST >= ?')
        parameters.append(criteria['bstMin'])
    
    #bstMax criteria
    if criteria.get('bstMax') is not None:
        partsWHERE.append('BST <= ?')
        parameters.append(criteria['bstMax'])

    #heightMin criteria
    if criteria.get('heightMin') is not None:
        partsWHERE.append('Height >= ?')
        parameters.append(criteria['heightMin'])
    
    #heightMax criteria
    if criteria.get('heightMax') is not None:
        partsWHERE.append('Height <= ?')
        parameters.append(criteria['heightMax'])

    #weightMin criteria
    if criteria.get('weightMin') is not None:
        partsWHERE.append('Weight >= ?')
        parameters.append(criteria['weightMin'])

    #weightMax criteria
    if criteria.get('weightMax') is not None:
        partsWHERE.append('Weight <= ?')
        parameters.append(criteria['weightMax'])

    sqlWHERE = ''
    if partsWHERE:
        sqlWHERE = 'WHERE ' + ' AND '.join(partsWHERE)
    
    curs.execute(f'''
            SELECT MonID, MonName, SpriteURL
            FROM tblMon
            {sqlWHERE}
            ORDER BY DexNum
            LIMIT 200
            ''',
            parameters
            )
    rows = curs.fetchall()

    conn.close()

    return rows

def searchDexMonsForButtons(dexID, criteria):    
    #connects to database
    conn = sqlite3.connect('TUP.db')
    curs = conn.cursor()

    #list for each part of WHERE in sql
    partsWHERE = ["dm.DexID = ?"]
    #list for holding values for ? placeholders
    parameters = [dexID]

    #name criteria
    if criteria.get('name'):
        partsWHERE.append('m.MonName LIKE ?') #LIKE is for partial matching
        parameters.append(f"%{criteria['name']}%")
    
    #type1 criteria
    if criteria.get('type1'):
        partsWHERE.append('m.Type1 = ?')
        parameters.append(criteria['type1'])

    #type2 criteria
    if criteria.get('type2'):
        partsWHERE.append('m.Type2 = ?')
        parameters.append(criteria['type2'])

    #bstMin criteria
    if criteria.get('bstMin') is not None:
        partsWHERE.append('m.BST >= ?')
        parameters.append(criteria['bstMin'])
    
    #bstMax criteria
    if criteria.get('bstMax') is not None:
        partsWHERE.append('m.BST <= ?')
        parameters.append(criteria['bstMax'])

    #heightMin criteria
    if criteria.get('heightMin') is not None:
        partsWHERE.append('m.Height >= ?')
        parameters.append(criteria['heightMin'])
    
    #heightMax criteria
    if criteria.get('heightMax') is not None:
        partsWHERE.append('m.Height <= ?')
        parameters.append(criteria['heightMax'])

    #weightMin criteria
    if criteria.get('weightMin') is not None:
        partsWHERE.append('m.Weight >= ?')
        parameters.append(criteria['weightMin'])

    #weightMax criteria
    if criteria.get('weightMax') is not None:
        partsWHERE.append('m.Weight <= ?')
        parameters.append(criteria['weightMax'])

    sqlWHERE = ''
    if partsWHERE:
        sqlWHERE = 'WHERE ' + ' AND '.join(partsWHERE)
    
    curs.execute(f'''
            SELECT dm.DexMonID, m.MonName, m.SpriteURL
            FROM tblDexMon dm
            JOIN tblMon m ON m.MonID = dm.MonID
            {sqlWHERE}
            ORDER BY m.DexNum
            LIMIT 200
            ''',
            parameters
            )
    rows = curs.fetchall()

    conn.close()

    return rows

def returnMon(monID):   #returns the details of a single Pokémon from the database
    #connects to database
    conn = sqlite3.connect('TUP.db')
    conn.row_factory = sqlite3.Row
    curs = conn.cursor()

    curs.execute('''
        SELECT *
        FROM tblMon
        WHERE MonID = ?
    ''',
    (monID,)
    )

    row = curs.fetchone()

    conn.close()

    if row:
        return dict(row)
    else:
        return None

def returnDexMon(dexMonID):
    #connects to database
    conn = sqlite3.connect('TUP.db')
    conn.row_factory = sqlite3.Row
    curs = conn.cursor()   

    curs.execute('''
        SELECT dm.DexMonID, dm.DexID, dm.MonID, dm.MonGen, dm.Moves, dm.Ability, m.*
        FROM tblDexMon dm
        JOIN tblMon m ON m.MonID = dm.MonID
        WHERE dm.DexMonID = ?
    ''',
    (dexMonID,)
    )

    row = curs.fetchone()

    conn.close()

    if row:
        return dict(row)
    else:
        return None
    
def getMonIDByDexNum(dexNum):
    #connects to database
    conn = sqlite3.connect('TUP.db')
    curs = conn.cursor()

    curs.execute('''
        SELECT MonID
        FROM tblMon
        WHERE DexNum = ?
    ''',
    (dexNum,)
    )

    row = curs.fetchone()

    conn.close()

    if row:
        return row[0]
    else:
        return None

def deleteMon(dexMonID): #deletes an entered Pokémon from the database
    #connects to database
    conn = sqlite3.connect('TUP.db')
    curs = conn.cursor()

    curs.execute('''
        DELETE FROM tblUserDexMon
        WHERE DexMonID = ?
    ''',
    (dexMonID,)
    )

    curs.execute('''
        DELETE FROM tblDexMon
        WHERE DexMonID = ?
    ''',
    (dexMonID,)
    )

    conn.commit()
    conn.close()

def ensureDexExists(dexID, gen, version="Default"):
    #connects to database
    conn = sqlite3.connect('TUP.db')
    curs = conn.cursor()

    curs.execute('''
        SELECT 1
        FROM tblDex
        WHERE DexID = ?
    ''',
    (dexID,)
    )

    exists = curs.fetchone()

    if not exists:
        curs.execute('''
            INSERT INTO tblDex (DexID, Gen, Version)
            VALUES (?, ?, ?)
        ''',
        (dexID, gen, version),
        )
    
    conn.commit()
    conn.close()

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

    if result is None:
        return False, None
    
    storedUserID, storedHash = result

    if storedHash == hashedPass:
        return True, storedUserID
    else:
        return False, None
    


#------------------------------------#
#TUPitems.outMon()