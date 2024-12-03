SELECT *
FROM {{ ref('int_citiesfinal_3') }}
WHERE
    prix_ttc_m3 IS NOT NULL
    OR tx_conformite_microbiologie IS NOT NULL
    OR tx_conformite_physiochimiques IS NOT NULL