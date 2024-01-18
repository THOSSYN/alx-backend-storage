-- An SQL script that creates an index idx_name_first_score
-- on the table names and the first letter of name and the score

ALTER TABLE names
ADD COLUMN first_alpha;

UPDATE name
SET first_alpha = LEFT(name, 1);

CREATE INDEX idx_name_first_score
ON names (first_alpha, score);
