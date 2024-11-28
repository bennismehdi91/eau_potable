-- Table des communes => 343796 lignes
SELECT *
FROM {{ ref('stg_datasources__composition_communale_services') }}

-- Tables des entités de gestion avec colonnes catégories => 92730 lignes
SELECT *
from {{ ref('int_ag_IPL_note') }} 

-- nombre de lignes tables Communes 
SELECT
COUNT(*)
FROM {{ ref('stg_datasources__composition_communale_services') }}
WHERE identifiant_sispea_collectivite_via_laquelle_commune_adhere is null
OR identifiant_sispea_collectivite_via_laquelle_commune_adhere = ''

-- Table communes d'origine => identifiant_sispea_collectivite_via_laquelle_commune_adhere,

select * from {{ source('datasources', 'composition_communale_services') }}
 