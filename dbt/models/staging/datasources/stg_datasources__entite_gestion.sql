with 

source as (

    select * from {{ source('datasources', 'entite_gestion') }}

),

renamed as (

    select
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

    from source

)

select * from renamed
