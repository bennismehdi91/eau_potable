-- Sélectionner le nombre d'habitant dersservie et le nombre de services par année et par cluster
SELECT year, cluster_3_pop_service, 
sum(nb_habitants_desservis) as sum_nb_habitants_desservis, 
count(distinct(id_sispea_entite_de_gestion)) as count_id_sispea_entite_gestion
FROM {{ ref('int_ad_entite_with_clusters') }}
Group by year, cluster_3_pop_service
ORDER BY year