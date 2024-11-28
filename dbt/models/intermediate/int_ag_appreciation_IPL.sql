SELECT *
     , CASE
         WHEN indice_lieaire_perte_reseau < 1.5  AND densite_lineaire_abonnes < 25 THEN 'bon'
         WHEN indice_lieaire_perte_reseau < 2.5  AND densite_lineaire_abonnes < 25 THEN 'acceptable'
         WHEN indice_lieaire_perte_reseau <= 4  AND densite_lineaire_abonnes < 25 THEN 'mediocre'
         WHEN indice_lieaire_perte_reseau > 4  AND densite_lineaire_abonnes < 25 THEN 'mauvais'
         WHEN indice_lieaire_perte_reseau < 3  AND densite_lineaire_abonnes < 50 THEN 'bon'
         WHEN indice_lieaire_perte_reseau < 5  AND densite_lineaire_abonnes < 50 THEN 'acceptable'
         WHEN indice_lieaire_perte_reseau <= 8  AND densite_lineaire_abonnes < 50 THEN 'mediocre'
         WHEN indice_lieaire_perte_reseau > 8  AND densite_lineaire_abonnes < 50 THEN 'mauvais'
         WHEN indice_lieaire_perte_reseau < 7  AND densite_lineaire_abonnes >= 50 THEN 'bon'
         WHEN indice_lieaire_perte_reseau < 10  AND densite_lineaire_abonnes >= 50 THEN 'acceptable'
         WHEN indice_lieaire_perte_reseau <= 15  AND densite_lineaire_abonnes >= 50 THEN 'mediocre'
         WHEN indice_lieaire_perte_reseau > 15  AND densite_lineaire_abonnes >= 50 THEN 'mauvais'
         ELSE 'NA'
       END AS IPL_classement
FROM {{ ref('int_ag_add_cat_densite') }}