with 

source as (

    select * from {{ source('datasources', 'composition_communale') }}

),

renamed as (

    select
        annee,
        nom_commune_adherente,
        id_sispea_commune_adherente,
        code_insee_commune_adherente,
        id_sispea_collectivite_via_laquelle_la_commune_adhere,
        id_sispea_entite_gestion_a_laquelle_la_commune_adhere,
        new_dpt_commune

    from source

)

select * from renamed
