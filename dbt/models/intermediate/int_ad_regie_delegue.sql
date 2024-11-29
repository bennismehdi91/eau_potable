-- Table pour donuts proportion des services Regie/delegues
SELECT mode_de_gestion, 
count(mode_de_gestion) AS nb_services,
FROM {{ ref('mart_ag_entite_with_clusters') }}
Group by mode_de_gestion
HAVING mode_de_gestion = "Régie" OR mode_de_gestion = "Délégation"