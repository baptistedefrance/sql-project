ATTACH DATABASE 'tpb2.db' AS source_db;

ATTACH DATABASE 'migration.db' AS cible_db;

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




