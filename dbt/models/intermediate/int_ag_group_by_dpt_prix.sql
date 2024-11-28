SELECT departement
, year
, AVG(prix_ttc_m3) AS moy_prix_ttc_m3
FROM {{ ref('mart_ag_indicateur_quality') }}
GROUP BY departement, year
ORDER BY departement, year