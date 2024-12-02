SELECT 
    cluster_3_pop_service,
    CASE
        WHEN indice_lieaire_perte_reseau < 1.5  AND densite_lineaire_abonnes < 25 THEN 4
        WHEN indice_lieaire_perte_reseau < 2.5  AND densite_lineaire_abonnes < 25 THEN 3
        WHEN indice_lieaire_perte_reseau <= 4  AND densite_lineaire_abonnes < 25 THEN 2
        WHEN indice_lieaire_perte_reseau > 4  AND densite_lineaire_abonnes < 25 THEN 1
        WHEN indice_lieaire_perte_reseau < 3  AND densite_lineaire_abonnes < 50 THEN 4
        WHEN indice_lieaire_perte_reseau < 5  AND densite_lineaire_abonnes < 50 THEN 3
        WHEN indice_lieaire_perte_reseau <= 8  AND densite_lineaire_abonnes < 50 THEN 2
        WHEN indice_lieaire_perte_reseau > 8  AND densite_lineaire_abonnes < 50 THEN 1
        WHEN indice_lieaire_perte_reseau < 7  AND densite_lineaire_abonnes >= 50 THEN 4
        WHEN indice_lieaire_perte_reseau < 10  AND densite_lineaire_abonnes >= 50 THEN 3
        WHEN indice_lieaire_perte_reseau <= 15  AND densite_lineaire_abonnes >= 50 THEN 2
        WHEN indice_lieaire_perte_reseau > 15  AND densite_lineaire_abonnes >= 50 THEN 1
        ELSE NULL
    END AS IPL_Note,
    cat_densite,
    departement,
    id_sispea_collectivite,
    nom_collectivite,
    id_sispea_entite_de_gestion,
    CONCAT(year, "_", id_sispea_entite_de_gestion) AS unique_key,
    nom_entite_de_gestion,
    communes_adherentes_entite_de_gestion,
    pop_entite_de_gestion_sans_double_compte,
    mode_de_gestion,
    statut_operateur,
    nom_operateur,
    statut,
    nb_habitants_desservis,
    prix_ttc_m3,
    tx_conformite_microbiologie,
    tx_conformite_physiochimiques,
    indice_lieaire_perte_reseau,
    tx_moyen_renouvellement_reseau,
    indice_protection_ressource,
    nb_abonnes,
    epargne_brute_annuelle,
    lineaire_reseau_hors_branchement,
    densite_lineaire_abonnes,
    ratio_habitant_par_abonne,
    consommation_moyenne_par_abonne,
    year
FROM {{ ref('int_final_entite_with_cluster') }}
WHERE
    cluster_3_pop_service NOT IN ('NA', 'Inconnu')
    AND mode_de_gestion NOT IN ('NA', 'Inconnu')
    AND mode_de_gestion IS NOT NULL
