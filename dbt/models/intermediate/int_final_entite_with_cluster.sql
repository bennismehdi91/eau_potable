SELECT
    CASE 
        WHEN pop_entite_de_gestion_sans_double_compte < 1000 THEN '1 - moins de 1000'
        WHEN pop_entite_de_gestion_sans_double_compte < 50000 THEN '2 - moins de 50000'
        WHEN pop_entite_de_gestion_sans_double_compte >= 50000 THEN '3 - plus de 50000'
        ELSE 'NA' 
        END AS cluster_3_pop_service ,

    CASE 
        WHEN densite_lineaire_abonnes < 25 THEN '1 - faible'
        WHEN densite_lineaire_abonnes < 50 THEN '2 - intermediaire'
        WHEN densite_lineaire_abonnes >= 50 THEN '3 - fort'
        ELSE 'NA'
    END AS cat_densite,
    departement,
    id_sispea_collectivite,
    nom_collectivite,
    id_sispea_entite_de_gestion,
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
FROM
{{ ref('stg_datasources__entite_gestion') }}
WHERE year in (2015,2016,2017,2018,2019,2020,2021,2022)