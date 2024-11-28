-- Table communes => 34 796 lignes
SELECT *
FROM {{ ref('stg_datasources__composition_communale') }}

-- Table entité avec clusters => 92 730 lignes
SELECT *
FROM  {{ ref('int_ad_entite_with_clusters') }}

--Combien de lignes par année et par entité pour le fichier communes
SELECT annee,
count(distinct id_sispea_collectivite_via_laquelle_la_commune_adhere) as nb_collectivite_adheree, 
count(distinct id_sispea_entite_gestion_a_laquelle_la_commune_adhere) as nb_entite_gestion, -- c'est la clé à utilier pour merger les tables
FROM {{ ref('stg_datasources__composition_communale') }}
GROUP BY annee
order by annee


-- Combien de collectivité et d'entité de gestion dans le fichier entité
SELECT year,
count(distinct id_sispea_collectivite) as nb_collectivite, 
count(distinct id_sispea_entite_de_gestion) as nb_entite_gestion,
FROM {{ ref('int_ad_entite_with_clusters') }}
GROUP BY year
Order by year

-- 