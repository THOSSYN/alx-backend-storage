-- Write a SQL script that creates a stored procedure
-- ComputeAverageWeightedScoreForUsers that computes and
-- store the average weighted score for all students.

DELIMITER //

CREATE PROCEDURE ComputeAverageWeightedScoreForUsers()
BEGIN
  DECLARE done INT DEFAULT FALSE;
  DECLARE user_id_param INT;
  DECLARE total_wgt_avg DECIMAL(10, 4);

  DECLARE user_cursor CURSOR FOR SELECT id FROM users;

  DECLARE CONTINUE HANDLER FOR NOT FOUND SET done = TRUE;

  OPEN user_cursor;

  begin_loop: 
  REPEAT
    FETCH user_cursor INTO user_id_param;
    IF NOT done THEN
      SELECT SUM(c.score * p.weight) / SUM(p.weight) INTO total_wgt_avg
      FROM corrections c
      JOIN projects p ON c.project_id = p.id
      WHERE c.user_id = user_id_param;
  
      UPDATE users
      SET average_score = total_wgt_avg
      WHERE id = user_id_param;
    END IF;
  UNTIL done
  END REPEAT;
END;
//

DELIMITER ;
