-- SQL script that creates an index idx_name_first on the
-- table names and the first letter of name

ALTER TABLE names
ADD COLUMN first_alpha CHAR(1);

UPDATE names 
SET first_alpha = LEFT(name, 1);

CREATE INDEX idx_name_first ON names (first_alpha);
