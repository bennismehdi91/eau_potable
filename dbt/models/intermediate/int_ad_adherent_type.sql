select *
from {{ ref("int_all_data_with_clusters") }}

-- est ce que le la colonne id_sespea_entité de gestion est une clé primaire ? yes
-- c'est bon
select id_sispea_entite_de_gestion, year, count(*) as nb
from {{ ref("int_all_data_with_clusters") }}
group by year, id_sispea_entite_de_gestion
having nb > 1

-- Evolution du nombre de commune solo adhérent à une entité de gestion, il manque la
-- donnée nombre de commune par année
select communes_adherentes_entite_de_gestion, year, count(*) as nb
from {{ ref("int_all_data_with_clusters") }}
group by year, communes_adherentes_entite_de_gestion
having communes_adherentes_entite_de_gestion = 1
