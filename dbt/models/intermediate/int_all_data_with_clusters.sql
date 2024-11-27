{{ config(
    materialized='table'
) }}

WITH source AS(

SELECT
        departement,
        id_sispea_collectivite,
        nom_collectivite,
        id_sispea_entite_de_gestion,
        nom_entite_de_gestion,
        communes_adherentes_entite_de_gestion,
        pop_entite_de_gestion_sans_double_compte,
        CASE
            WHEN pop_entite_de_gestion_sans_double_compte < 1000 THEN '1- Moins de 1 000'
            WHEN pop_entite_de_gestion_sans_double_compte < 3500 THEN '2- Entre 1 000 à 3 500'
            WHEN pop_entite_de_gestion_sans_double_compte < 10000 THEN '3- Entre 3 500 à 10 000'
            WHEN pop_entite_de_gestion_sans_double_compte < 50000 THEN '4- Entre 10 000 à 50 000'
            WHEN pop_entite_de_gestion_sans_double_compte < 100000 THEN '5- Entre 50 000 à 100 000'
            WHEN pop_entite_de_gestion_sans_double_compte >= 100000 THEN '6- Plus de 100 000'
            ELSE 'NA'
        END AS cluster_pop_entite_gestion,
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
FROM {{ ref('stg_datasources__entite_gestion') }}
WHERE 
    year IN (2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022)
)

SELECT *
FROM source
WHERE
    cluster_pop_entite_gestion <> 'NA'