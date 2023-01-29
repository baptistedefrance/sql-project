import sqlite3

def show_duplicates(db, table):
 conn = sqlite3.connect('{}'.format(db))
 cursor = conn.cursor()
 table_name = "{}".format(table)
 cursor.execute("SELECT * FROM {}".format(table_name))
 rows = cursor.fetchall()
 unique_values = set()
 duplicates = set()
 for row in rows:
     if row in unique_values:
         duplicates.add(row)
     else:
         unique_values.add(row)
 print("Les doublons dans la table {} sont :".format(table_name), duplicates)
 conn.close()

def information_database(db):
 conn = sqlite3.connect('{}'.format(db))
 cursor = conn.cursor()
 cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
 tables = cursor.fetchall()
 print("Number of tables:", len(tables)-1)
 for table in tables:
     if table[0] != 'sqlite_sequence':
      print("Table name:", table[0])
 conn.close()
 menu()

def migration(db1, db2):
 conn = sqlite3.connect(db1)
 c = conn.cursor()
 c.executescript('''
 
ATTACH DATABASE '{}' AS source_db;
ATTACH DATABASE '{}' AS cible_db;

INSERT INTO cible_db.Place(Name, Address, City)
SELECT PlaceName, Address, City
FROM source_db.Tournament;

INSERT INTO cible_db.Game(Name) SELECT Name FROM source_db.Game;

INSERT INTO cible_db.Employee_Data(Firstname, Lastname, Age, Wage, Gender)
SELECT Firstname, Lastname, Age, Wage, Gender FROM source_db.Staff;

INSERT INTO cible_db.Employee_Data(Firstname, Lastname, Age, Wage, Gender)
SELECT Firstname, Lastname, Age, Wage, Gender FROM source_db.Player;

INSERT INTO cible_db.Employee_Data(Firstname, Lastname, Age, Wage, Gender)
SELECT Firstname, Lastname, Age, Wage, Gender FROM source_db.Coach;

INSERT INTO cible_db.Tournament(IdPlace, IdGame, Date, Duration)
SELECT cible_db.Place.IdPlace, cible_db.Game.IdGame, Date, Duration
FROM source_db.Tournament, cible_db.Game, cible_db.Place 
WHERE source_db.Tournament.PlaceName = cible_db.Place.Name 
AND source_db.Tournament.IdGame = cible_db.Game.IdGame;

INSERT INTO cible_db.staff(IdEmployeeData)
SELECT cible_db.Employee_Data.IdEmployee
FROM source_db.Staff, cible_db.Employee_Data
WHERE source_db.Staff.Lastname = cible_db.Employee_Data.Lastname;

INSERT INTO cible_db.player(IdEmployeeData, IdGame, Ranking)
SELECT  cible_db.Employee_Data.IdEmployee, cible_db.Game.IdGame, source_db.Player.Ranking
FROM source_db.Player, cible_db.Employee_Data, cible_db.Game
WHERE source_db.Player.IdGame = cible_db.Game.IdGame
AND source_db.Player.Lastname = cible_db.Employee_Data.Lastname
GROUP BY source_db.Player.IdPlayer;

INSERT INTO cible_db.Coach(IdGame, LicenseDate, IdEmployeeData)
SELECT cible_db.Game.IdGame, source_db.Coach.LicenseDate, cible_db.Employee_Data.IdEmployee
FROM cible_db.Game, source_db.Coach, cible_db.Employee_Data
WHERE source_db.Coach.IdGame = cible_db.Game.IdGame
AND source_db.Coach.Lastname = cible_db.Employee_Data.Lastname;

DETACH DATABASE source_db;
DETACH DATABASE cible_db;
'''.format(db1,db2))

 conn.commit()
 c.close()
 conn.close()
 menu()
 

def schema(db1):
 conn = sqlite3.connect(db1)
 c = conn.cursor()
 c.execute('''CREATE TABLE IF NOT EXISTS Place(
   IdPlace INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
   Name VARCHAR2(30),
   Address VARCHAR2(30),
   City VARCHAR2(30)
)''')

 c.execute('''CREATE TABLE IF NOT EXISTS Tournament(
    IdPlace INTEGER NOT NULL,
    IdGame INTEGER NOT NULL,
    IdTournament INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    Duration INTEGER,
    Date VARCHAR2(30) NOT NULL,
    FOREIGN KEY(IdPlace) REFERENCES Place(IdPlace),
    FOREIGN KEY(IdGame) REFERENCES Game(IdGame)
)''')

 c.execute('''CREATE TABLE IF NOT EXISTS Game(
    IdGame INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    Name VARCHAR2(30)
)''')

 c.execute('''CREATE TABLE IF NOT EXISTS Employee_Data(
    IdEmployee INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    Lastname VARCHAR2(30),
    Firstname VARCHAR2(30),
    Gender VARCHAR2(30),
    Age INTEGER,
    Wage INTEGER
)''')

 c.execute('''CREATE TABLE IF NOT EXISTS Staff(
    IdStaff INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    idEmployeeData INTEGER NOT NULL,
    FOREIGN KEY(idEmployeeData) REFERENCES Employee_Data(IdEmployee)
)''')

 c.execute('''CREATE TABLE IF NOT EXISTS Player(
    IdPlayer INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    Ranking INTEGER,
    IdGame INTEGER NOT NULL,
    IdEmployeeData INTEGER NOT NULL,
    FOREIGN KEY(IdGame) REFERENCES Game(IdGame),
    FOREIGN KEY(IdEmployeeData) REFERENCES Employee_Data(IdEmployee)
)''')

 c.execute('''CREATE TABLE IF NOT EXISTS Coach(
    IdCoach INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    IdGame INTEGER NOT NULL,
    LicenseDate VARCHAR2(30),
    idEmployeeData INTEGER NOT NULL,
    FOREIGN KEY(idEmployeeData) REFERENCES Employee_Data(IdEmployee),
    FOREIGN KEY(IdGame) REFERENCES Game(IdGame)
)''')
 
 conn.commit()
 c.close()
 conn.close()
 menu()


def show_information(db1):
 conn = sqlite3.connect(db1)
 c = conn.cursor()
 c.executescript('''
SELECT * FROM Tournament INNER JOIN Game ON
Tournament.IdGame = Game.IdGame WHERE Game.Name = 'Tekken 7';

SELECT AVG(Employee_Data.Wage) FROM Employee_Data INNER JOIN Player
ON Employee_Data.IdEmployee = Player.IdEmployeeData
INNER JOIN Game ON Player.IdGame = Game.IdGame
WHERE Game.Name = 'Tekken 7';

SELECT * FROM Tournament INNER JOIN Place ON
Tournament.IdPlace = Place.IdPlace;

SELECT * FROM Tournament INNER JOIN Place ON
Tournament.IdPlace = Place.IdPlace
WHERE Place.Name = 'Arenes';

SELECT COUNT(Employee_Data.IdEmployee) FROM Employee_Data  INNER JOIN Player
ON Employee_Data.IdEmployee = Player.IdEmployeeData
GROUP BY Employee_Data.Gender;''')
 conn.commit()
 c.close()
 conn.close()
 menu()


def delete(db1):
 conn = sqlite3.connect(db1)
 c = conn.cursor()
 c.executescript('''
DROP TABLE IF EXISTS Game;

DROP TABLE IF EXISTS Tournament;

DROP TABLE IF EXISTS Place;

DROP TABLE IF EXISTS Employee_Data;


DROP TABLE IF EXISTS Staff;

DROP TABLE IF EXISTS Player;

DROP TABLE IF EXISTS Coach;''')
 conn.commit()
 c.close()
 conn.close()
 menu()


def add_table(db1, name_table, row1, type_row1, row2, type_row2, row3, type_row3, row4, type_row4):
 conn = sqlite3.connect(db1)
 c = conn.cursor()
 c.executescript('''CREATE TABLE IF NOT EXISTS {}(
   {} {},
   {} {},
   {} {},
   {} {}
);'''.format(name_table, row1, type_row1, row2, type_row2, row3, type_row3, row4, type_row4))
 conn.commit()
 c.close()
 conn.close()

def create_database(db1):
 myFile = open(db1+".db", "w+")
 myFile.close()
 menu()
 
 

def menu():
    print("Welcome on SQL_MIGRATION_B2 Menu !")
    print("Please, select an option : ")
    print("1/ Create schema")
    print("2/ Transfert DATABASE")
    print("3/ List some information")
    print("4/ Delete all")
    print("5/ See all database")
    print("6/ Add a table in the schema")
    print("7/ Create a database")
    print("8/ Show Duplicates")
    choix = int(input("Please select an option : "))
    if choix == 1:
        db1 = input("Please, choose the name of your DB : ")
        print("The name of your database is "+db1)
        schema(db1)
    if choix == 2:
        db1 = input("Please, choose the name of your 1st DB : ")
        print("The name of your 1st database is "+db1)
        db2 = input("Please, choose the name of your 2st DB : ")
        print("The name of your 1st database is "+db2)
        migration(db1, db2)
    if choix == 3:
        db1 = input("Please, choose the name of your DB : ")
        print("The name of your database is "+db1)
        show_information(db1)
    if choix == 4:
        db1 = input("Please, choose the name of your DB : ")
        print("The name of your database is "+db1)
        delete(db1)
    if choix == 5:
        db = input("Please, choose the name of your DB : ")
        print("The name of your database is "+db)
        information_database(db)
    if choix == 6:
        db1 = input("Please, choose the name of your DB : ")
        print("The name of your database is "+db1)
        name_table = input("Please select the name of you new table : ")
        row1 = input("Please select the name of your 1st row : ")
        type_row1 = input("Please select the type of your 1st row : ")
        row2 = input("Please select the name of your 2st row : ")
        type_row2 = input("Please select the type of your 2nd row : ")
        row3 = input("Please select the name of your 3rd row : ")
        type_row3 = input("Please select the type of your 3rd row : ")
        row4 = input("Please select the name of your 4th row : ")
        type_row4 = input("Please select the type of your 4th row : ")
        add_table(db1, name_table, row1, type_row1, row2, type_row2, row3, type_row3, row4, type_row4)
    if choix == 7:
        db1 = input("Please, choose the name of your DB : ")
        create_database(db1)
    if choix == 8:
        db = input("Please, choose the name of your DB : ")
        row1 = input("Please select the name of the table : ")
        show_duplicates(db, row1)
def main():
    menu()
main()