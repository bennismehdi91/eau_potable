--- Correlation entre le Correlation entre prix de l’eau et 
--- taille des services (nombre d’abonné par entité de gestion)

/*      id_sispea_entite_de_gestion AS pk_entite_gestion,
        prix_ttc_m3,
        nb_abonnes,
        year
        
*/

WITH source as (

SELECT * FROM {{ ref('stg_datasources__entite_gestion') }})

SELECT
        id_sispea_entite_de_gestion AS pk_entite_gestion,
        prix_ttc_m3,
        nb_abonnes,
        year
FROM source
WHERE
    prix_ttc_m3 IS NOT NULL 
    AND
    nb_abonnes IS NOT NULL
    AND
    year IN (2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022)
-- ORDER BY year desc