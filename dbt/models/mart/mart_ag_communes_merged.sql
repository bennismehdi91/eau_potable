SELECT* EXCEPT(id_sispea_entite_gestion_a_laquelle_la_commune_adhere_INT, id_sispea_entite_gestion_a_laquelle_la_commune_adhere)
FROM {{ ref('int_ad_communes_merged') }}