SELECT * FROM {{ ref('stg_datasources__entite_gestion') }}


-- colonnes dont j'ai besoin pour l'analyse 
SELECT departement, id_sispea_collectivite, communes_adherentes_entite_de_gestion, pop_entite_de_gestion_sans_double_compte
FROM {{ ref('stg_datasources__entite_gestion') }}



-- ajouter une colonne avec le % de commune adhérant seule sur le total de commune 

SELECT year,
sum(communes_adherentes_entite_de_gestion) AS qte_communes, 
FROM {{ ref('stg_datasources__entite_gestion') }}
Group by year 
Order by year

SELECT id_sispea_collectivite, year,
    CASE   
        WHEN communes_adherentes_entite_de_gestion = 1 THEN 1
        ELSE 0 
    END AS commune_solo
FROM {{ ref('stg_datasources__entite_gestion') }}


-- Objectif calculer le poids des données manquantes en terme de population représentée => les données sont complétées pour 52% de la population
WITH NullPricetab AS (
SELECT id_sispea_entite_de_gestion, 
pop_entite_de_gestion_sans_double_compte,
    CASE 
        WHEN prix_ttc_m3 > 1 THEN 1
        ELSE 0
    END AS NullPrice
FROM {{ ref('stg_datasources__entite_gestion') }}
)

SELECT NullPrice,
sum(pop_entite_de_gestion_sans_double_compte)
FROM NullPricetab
GROUP BY NullPrice

