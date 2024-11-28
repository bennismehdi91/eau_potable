SELECT 
CASE
    WHEN departement LIKE '0%' THEN SUBSTRING(departement, 2) -- Retirer le 0 si le numéro commence par 0
    ELSE departement                                       -- Sinon garder tel quel
END AS departement
, year
, moy_prix_ttc_m3
, moy_microbio
, moy_physio
, moy_IPL_note
FROM {{ ref('int_ag_group_by_dpt') }}