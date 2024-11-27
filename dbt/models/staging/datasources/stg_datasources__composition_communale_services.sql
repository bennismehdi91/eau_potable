with 

source as (

    select * from {{ source('datasources', 'composition_communale_services') }}

),

renamed as (

    select
        annee,
        nom_commune_adherente,
        identifiant_sispea_commune_adherente,
        code_insee_commune_adherente,
        secteur_desservi,
        population_commune,
        type_dadhesion,
        nom_collectivite_via_laquelle_commune_adhere,
        siren_collectivite_via_laquelle_commune_adhere,
        identifiant_sispea_collectivite_via_laquelle_commune_adhere,
        nom_collectivite_lentite_gestion_laquelle_commune_adhere,
        identifiant_sispea_collectivite_lentite_gestion_laquelle_commune_adhere,
        type_collectivite,
        siren,
        avec_sans_ccspl,
        nom_lentite_gestion_laquelle_commune_adhere,
        identifiant_sispea_lentite_gestion_laquelle_commune_adhere,
        code_uge_eau_potable,
        population_representative,
        competence_lentite_gestion,
        production,
        transfert,
        distribution,
        type_mode_gestion,
        statut_loperateur,
        nom_loperateur,
        date_debut_mode_gestion,
        date_fin_mode_gestion,
        statut_des_donnees_cette_entite_gestion,
        numero_departement_ddt_gestionnaire,
        new_dpt_commune,
        new_dpt_siege_collectivite

    from source

)

select * from renamed
