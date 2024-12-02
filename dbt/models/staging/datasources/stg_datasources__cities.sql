with 

source as (

    select * from {{ source('datasources', 'cities') }}

),

renamed as (

    select
        insee_code,
        city_code,
        zip_code,
        label,
        latitude,
        longitude,
        department_name,
        department_number,
        region_name,
        region_geojson_name

    from source

)

select * from renamed
