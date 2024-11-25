with 

source as (

    select * from {{ source('Test_Upload', 'test') }}

),

renamed as (

    select
        int64_field_0,
        dpt,
        id,
        nom,
        type,
        siren,
        insee,
        communes,
        ccspl

    from source

)

select * from renamed
