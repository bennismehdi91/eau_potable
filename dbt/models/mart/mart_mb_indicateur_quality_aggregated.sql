SELECT
    cluster_pop_entite_gestion,
    year,
    AVG(tx_conformite_physiochimiques) AS tx_conformite_physiochimiques,
    AVG(tx_conformite_microbiologie) AS tx_conformite_microbiologie,
    AVG(IPL_note) AS IPL_note,
FROM {{ ref('int_ag_IPL_note') }}
GROUP BY
    cluster_pop_entite_gestion,
    year
ORDER BY
    cluster_pop_entite_gestion,
    year