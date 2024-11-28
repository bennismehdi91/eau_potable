SELECT *
,  CASE 
    WHEN densite_lineaire_abonnes < 25 THEN '1 - faible'
    WHEN densite_lineaire_abonnes < 50 THEN '2 - intermediaire'
    WHEN densite_lineaire_abonnes >= 50 THEN '3 - fort'
    ELSE 'NA'
  END AS cat_densite
FROM {{ ref('int_all_data_with_clusters') }}