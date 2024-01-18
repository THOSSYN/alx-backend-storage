-- A SQL script that creates a stored procedure AddBonus
-- that adds a new correction for a student

DELIMITER //

CREATE
PROCEDURE AddBonus(
	IN user_id_param INT,
	IN project_name VARCHAR(255),
	IN score_param INT
)
BEGIN
  DECLARE proj_id INT;

  SELECT id INTO proj_id
  FROM projects
  WHERE name = project_name;

  IF proj_id IS NULL THEN
    INSERT INTO projects (name)
    VALUES (project_name);
    
    SET proj_id = LAST_INSERT_ID();
  END IF;

  INSERT INTO corrections (user_id, project_id, score)
  VALUES(user_id_param, proj_id, score_param);

  SELECT user_id_param, project_name;
END;
//

DELIMITER ;
