SELECT cluster_3_pop_service
, year
, AVG(prix_ttc_m3) AS moy_prix_ttc_m3
, AVG(tx_conformite_microbiologie) AS moy_microbio
, AVG(tx_conformite_physiochimiques) AS moy_physio
, AVG(IPL_note) AS moy_IPL_note
FROM {{ ref('mart_ag_entite_with_clusters') }}
GROUP BY cluster_3_pop_service, year
ORDER BY cluster_3_pop_service, year