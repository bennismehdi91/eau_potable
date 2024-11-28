SELECT 
    year,
    ROUND(AVG(prix_ttc_m3),2) AS prix_ttc_m3,
    SUM(nb_abonnes) AS nb_abonnes,
    ROUND(AVG(consommation_moyenne_par_abonne),0) AS conso_moy_foyer,
    COUNT(DISTINCT id_sispea_entite_de_gestion) AS nb_services,
    ROUND(SUM(lineaire_reseau_hors_branchement),0) AS lineaire_reseau_km
FROM {{ ref('int_ad_entite_with_clusters') }}
WHERE year = 2022
GROUP BY year