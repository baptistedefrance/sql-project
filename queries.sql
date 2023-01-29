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
GROUP BY Employee_Data.Gender;



