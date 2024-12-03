SELECT
        CONCAT(cc.annee,"_",cc.id_sispea_entite_gestion_a_laquelle_la_commune_adhere) AS unique_key,
        cc.annee,
        cc.nom_commune_adherente,
        cc.id_sispea_commune_adherente,
        cc.code_insee_commune_adherente,
        cc.id_sispea_collectivite_via_laquelle_la_commune_adhere,
        cc.id_sispea_entite_gestion_a_laquelle_la_commune_adhere,
        cc.new_dpt_commune,
        cities.zip_code,
        cities.label,
        cities.latitude,
        cities.longitude,
        cities.department_name,
        cities.department_number,
        cities.region_geojson_name
FROM {{ ref('stg_datasources__composition_communale') }} AS cc
LEFT JOIN {{ ref('stg_datasources__cities') }} AS cities ON cc.code_insee_commune_adherente = cities.insee_code
WHERE annee BETWEEN '2015' AND '2022'
