SELECT
    departement,
    id_sispea_collectivite 

FROM {{ ref('stg_datasources__entite_gestion') }}