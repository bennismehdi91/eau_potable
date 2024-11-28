SELECT *
FROM {{ ref('int_all_data_with_clusters') }}
WHERE year = 2022

-- check prix ttc
SELECT 
ROUND(MAX(prix_ttc_m3),2) AS max_price,
ROUND(AVG(prix_ttc_m3),2) AS avg_price,
ROUND(MIN(prix_ttc_m3),2) AS min_price
FROM {{ ref('int_all_data_with_clusters') }}
WHERE year = 2022;

-- check répartition des niveaux de prix
SELECT  
    COUNT(CASE WHEN prix_ttc_m3 <1 THEN 1 END) AS under_1,
    COUNT(CASE WHEN prix_ttc_m3 BETWEEN 1 AND 2 THEN 1 END) AS between_1_and_2,
    COUNT(CASE WHEN prix_ttc_m3 BETWEEN 2 AND 3 THEN 1 END) AS between_2_and_3,
    COUNT(CASE WHEN prix_ttc_m3 BETWEEN 3 AND 4 THEN 1 END) AS between_3_and_4,
    COUNT(CASE WHEN prix_ttc_m3 BETWEEN 4 AND 5 THEN 1 END) AS between_4_and_5,
    COUNT(CASE WHEN prix_ttc_m3 >5 THEN 1 END) AS over_5
FROM {{ ref('int_all_data_with_clusters') }}
WHERE year = 2022

    SELECT
    COUNT(CASE WHEN tx_conformite_microbiologie = 100 THEN 1 END) AS ok_micro,
    COUNT(CASE WHEN tx_conformite_microbiologie < 100 THEN 1 END) AS pas_ok_micro,
    COUNT(CASE WHEN tx_conformite_physiochimiques = 100 THEN 1 END) AS ok_physio,
    COUNT(CASE WHEN tx_conformite_physiochimiques  < 100 THEN 1 END) AS pas_ok_physio
    FROM {{ ref('int_all_data_with_clusters') }}
    WHERE year = 2022