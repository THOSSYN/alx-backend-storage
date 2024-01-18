-- An SQL script that lists all bands with Glam rock style

SELECT
  band_name,
  COALESCE((YEAR(2022) - MAX(formed)) - (YEAR(2022) - MAX(split)), 0) AS lifespan
FROM
  metal_bands
WHERE
  style = 'Glam rock'
GROUP BY
  band_name
ORDER BY
  lifespan DESC;
