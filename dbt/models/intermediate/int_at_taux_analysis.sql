{{ config(
    materialized='table'
) }}

SELECT *,
CASE 
    WHEN tx_conformite_microbiologie = 100 THEN 'ok'
    WHEN tx_conformite_microbiologie < 100 THEN 'Under expectation'
    ELSE 'NA'
END AS tx_microbio_cast,
CASE    
    WHEN tx_conformite_physiochimiques = 100 THEN 'ok'
    WHEN tx_conformite_physiochimiques < 100 THEN 'Under expectation'
    ELSE 'NA'
END AS tx_physio_cast,
FROM {{ ref('int_all_data_with_clusters') }}
WHERE year = 2022