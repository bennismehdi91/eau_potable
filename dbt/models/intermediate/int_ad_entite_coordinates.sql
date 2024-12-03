with
    entite_coordinates as (
        select
            id_sispea_entite_de_gestion,
            avg(latitude) as latitude_entite,
            avg(longitude) as longitude_entite,
        from {{ ref("mart_cities_final") }}
        where annee = "2022"
        group by id_sispea_entite_de_gestion
    )

select entite_tab.*, coordinates.* except (id_sispea_entite_de_gestion),
concat(latitude_entite,',',longitude_entite) as lat_long,
from {{ ref("mart_entite_final") }} as entite_tab
left join
    entite_coordinates as coordinates
    on coordinates.id_sispea_entite_de_gestion = entite_tab.id_sispea_entite_de_gestion
where year = 2022

