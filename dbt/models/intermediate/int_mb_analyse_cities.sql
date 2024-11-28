WITH
    source AS (
        SELECT 
            code_insee_commune_adherente, 
            annee, 
            cluster_3_pop_service,
            prix_ttc_m3,
            tx_conformite_microbiologie,
            tx_conformite_physiochimiques,
            communes_adherentes_entite_de_gestion,
            IPL_note
        FROM {{ ref('mart_ag_communes_merged') }}
    ), 
    check_cte AS (
        SELECT
            code_insee_commune_adherente
        FROM source
        WHERE annee = '2015' 
          AND cluster_3_pop_service = '1 - moins de 1000'
          AND communes_adherentes_entite_de_gestion = 1
    )
SELECT
    annee,
    code_insee_commune_adherente,
    AVG(prix_ttc_m3) AS avg_prix_ttc_m3,
    AVG(tx_conformite_microbiologie) AS avg_tx_conformite_microbiologie,
    AVG(tx_conformite_physiochimiques) AS avg_tx_conformite_physiochimiques,
    AVG(IPL_note) AS IPL_note,
    CASE
        WHEN communes_adherentes_entite_de_gestion = 1 THEN 'solo'
        WHEN communes_adherentes_entite_de_gestion > 1 THEN 'multi'
        ELSE 'NA'
    END AS solo_multi,
FROM
    source
WHERE
    code_insee_commune_adherente IN (SELECT code_insee_commune_adherente FROM check_cte)
GROUP BY
    annee, code_insee_commune_adherente, communes_adherentes_entite_de_gestion