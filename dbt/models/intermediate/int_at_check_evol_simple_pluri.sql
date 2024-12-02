WITH base AS (
    SELECT
        year,
        departement_name,
        COUNT(mode_de_gestion) AS total_mode_gestion,
        CONCAT(year, departement_name) AS key_dpt
    FROM {{ ref("int_at_region_departement") }}
    WHERE mode_de_gestion IS NOT NULL
    GROUP BY year, departement_name, CONCAT(year, departement_name)
)

SELECT
    reg.year,
    reg.departement_name,
    CONCAT(reg.year, reg.departement_name) AS key_dpt,
    reg.mode_de_gestion,
    COUNT(reg.mode_de_gestion) AS split_mode_gestion,
    b.total_mode_gestion,
    ROUND(((COUNT(reg.mode_de_gestion) /b.total_mode_gestion)*100),0) AS percentage
FROM {{ ref("int_at_region_departement") }} reg
LEFT JOIN base b ON b.key_dpt = CONCAT(reg.year, reg.departement_name)
WHERE mode_de_gestion IS NOT NULL 
GROUP BY year, departement_name, mode_de_gestion, total_mode_gestion
ORDER BY departement_name, year