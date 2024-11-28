{{ config(
    materialized='table'
) }}

WITH base_data AS (
    SELECT
        year,
        cluster_pop_entite_gestion,
        prix_ttc_m3
    FROM {{ ref('int_all_data_with_clusters') }}
),

quartiles AS (
    SELECT 
        year,
        cluster_pop_entite_gestion,
        PERCENTILE_CONT(prix_ttc_m3, 0.25) OVER (PARTITION BY cluster_pop_entite_gestion) AS Q1,
        PERCENTILE_CONT(prix_ttc_m3, 0.5) OVER (PARTITION BY cluster_pop_entite_gestion) AS Median,
        PERCENTILE_CONT(prix_ttc_m3, 0.75) OVER (PARTITION BY cluster_pop_entite_gestion) AS Q3,
        MIN(prix_ttc_m3) OVER (PARTITION BY cluster_pop_entite_gestion) AS Minimum,
        MAX(prix_ttc_m3) OVER (PARTITION BY cluster_pop_entite_gestion) AS Maximum
    FROM base_data
)

SELECT DISTINCT
    year,
    cluster_pop_entite_gestion,
    Q1,
    Median,
    Q3,
    Minimum,
    Maximum
FROM quartiles