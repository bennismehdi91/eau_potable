-- Recode : ajouter une colonne avec 3 catégories en fonction de la taille du service : 1 - moins de 1000, 2 - moins de 50000, 3 - plus de 50 000
SELECT *,
    CASE 
        WHEN pop_entite_de_gestion_sans_double_compte < 1000 THEN '1 - moins de 1000'
        WHEN pop_entite_de_gestion_sans_double_compte < 50000 THEN '2 - moins de 50000'
        ELSE '3 - plus de 50000' 
        END AS cluster_3_pop_service
from {{ ref('int_ag_IPL_note') }} 