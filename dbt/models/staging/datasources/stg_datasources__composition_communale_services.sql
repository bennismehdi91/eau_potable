with 

source as (

    select * from {{ source('datasources', 'composition_communale_services') }}

),

renamed as (

    select
        annee,
        nom_commune_adherente,
        identifiant_sispea_commune_adherente,
        population_commune,
        identifiant_sispea_collectivite_via_laquelle_commune_adhere,

    from source

)

select * from renamed
