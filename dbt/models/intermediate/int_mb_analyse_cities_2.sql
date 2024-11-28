{{ config(
    materialized='table'
) }}

SELECT
*
FROM
{{ ref('int_mb_analyse_cities') }}
WHERE
    annee IS NOT NULL AND
    code_insee_commune_adherente IS NOT NULL AND
    avg_prix_ttc_m3 IS NOT NULL AND
    avg_tx_conformite_microbiologie IS NOT NULL AND
    avg_tx_conformite_physiochimiques IS NOT NULL AND
    solo_multi IS NOT NULL AND
    IPL_note IS NOT NULL AND
    cluster_3_pop_service IS NOT NULL