-- convertir la colonne en int
WITH communes AS (
SELECT *,
CAST(id_sispea_entite_gestion_a_laquelle_la_commune_adhere AS INT) as id_sispea_entite_gestion_a_laquelle_la_commune_adhere_INT
FROM {{ ref('stg_datasources__composition_communale') }}
)
-- merge tables
SELECT*
FROM communes 
LEFT JOIN {{ ref('mart_ag_entite_with_clusters') }}
ON id_sispea_entite_gestion_a_laquelle_la_commune_adhere_INT=id_sispea_entite_de_gestion