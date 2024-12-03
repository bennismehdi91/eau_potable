{{ config(materialized="table") }}

with
    base as (
        select
            year,
            departement_name,
            count(mode_de_gestion) as total_mode_gestion,
            concat(year, departement_name) as key_dpt
        from {{ ref("int_at_region_departement") }}
        where mode_de_gestion is not null
        group by year, departement_name, concat(year, departement_name)
    )

select
    reg.year,
    reg.departement_name,
    concat(reg.year, reg.departement_name) as key_dpt,
    reg.mode_de_gestion,
    count(reg.mode_de_gestion) as split_mode_gestion,
    b.total_mode_gestion,
    round(((count(reg.mode_de_gestion) / b.total_mode_gestion) * 100), 0) as percentage,
    lag(round((count(reg.mode_de_gestion) * 100.0 / b.total_mode_gestion), 0)) over (
        partition by reg.departement_name, reg.mode_de_gestion order by reg.year
    ) as prev_percentage,
    round(
        (
            (
                round((count(reg.mode_de_gestion) * 100.0 / b.total_mode_gestion), 0)
                - lag(
                    round(
                        (count(reg.mode_de_gestion) * 100.0 / b.total_mode_gestion), 0
                    )
                ) over (
                    partition by reg.departement_name, reg.mode_de_gestion
                    order by reg.year
                )
            ) / nullif(
                lag(
                    round(
                        (count(reg.mode_de_gestion) * 100.0 / b.total_mode_gestion), 0
                    )
                ) over (
                    partition by reg.departement_name, reg.mode_de_gestion
                    order by reg.year
                ),
                0
            )
        )
        * 100,
        2
    ) as percentage_change
from {{ ref("int_at_region_departement") }} reg
left join base b on b.key_dpt = concat(reg.year, reg.departement_name)
where mode_de_gestion is not null
group by year, departement_name, mode_de_gestion, total_mode_gestion
order by departement_name, year
