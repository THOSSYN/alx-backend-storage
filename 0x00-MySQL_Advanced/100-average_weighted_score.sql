-- An SQL script that creates a stored procedure
-- ComputeAverageWeightedScoreForUser that computes and
-- store the average weighted score for a student.

DELIMITER //

CREATE PROCEDURE ComputeAverageWeightedScoreForUser(IN user_id_param INT)
BEGIN
  DECLARE wgt_score DECIMAL(10, 2);

  SELECT SUM(c.score * p.weight) / SUM(p.weight) INTO wgt_score
  FROM corrections c
  JOIN projects p ON c.project_id = p.id
  WHERE c.user_id = user_id_param;

  UPDATE users
  SET average_score = wgt_score
  WHERE id = user_id_param;
END; //

DELIMITER ;
