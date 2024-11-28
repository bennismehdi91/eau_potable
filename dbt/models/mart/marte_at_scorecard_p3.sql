SELECT 
    year,
    ROUND(AVG(prix_ttc_m3),2) AS prix_ttc_m3,
    ROUND(AVG(tx_conformite_microbiologie),1) AS tx_conformite_microbio,
    ROUND(AVG(tx_conformite_physiochimiques),1) AS tx_conformite_physiochimiques,
    ROUND((AVG(indice_lieaire_perte_reseau)*SUM(lineaire_reseau_hors_branchement))*365,0) AS perte_m3_2022,
FROM {{ ref('int_ad_entite_with_clusters') }}
WHERE year = 2022
GROUP BY year