WITH
    check_cte AS (
        SELECT
            code_insee_commune_adherente
        FROM {{ ref('int_citiesfinal_2') }}
        WHERE annee = '2015' 
          AND cluster_3_pop_service = '1 - moins de 1000'
          AND communes_adherentes_entite_de_gestion = 1
    )
SELECT
    code_insee_commune_adherente, 
    annee, 
    cluster_3_pop_service,
    prix_ttc_m3,
    tx_conformite_microbiologie,
    tx_conformite_physiochimiques,
    communes_adherentes_entite_de_gestion,
    IPL_note,
    CASE
        WHEN communes_adherentes_entite_de_gestion = 1 THEN 'solo'
        WHEN communes_adherentes_entite_de_gestion > 1 THEN 'multi'
        ELSE 'NA'
    END AS solo_multi,
FROM
    {{ ref('int_citiesfinal_2') }}
WHERE
    code_insee_commune_adherente IN (SELECT code_insee_commune_adherente FROM check_cte)
    AND (annee IN ('2016', '2017','2018','2019','2020','2021','2022') OR communes_adherentes_entite_de_gestion = 1)

