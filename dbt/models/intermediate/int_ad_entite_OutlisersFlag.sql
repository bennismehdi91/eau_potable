
WITH flag_tab AS(
SELECT
    region_name,
    departement_name,
    cluster_3_pop_service,
    departement,
    id_sispea_entite_de_gestion,
    nom_entite_de_gestion,
    pop_entite_de_gestion_sans_double_compte,
    mode_de_gestion,
    prix_ttc_m3,
    tx_conformite_microbiologie,
    tx_conformite_physiochimiques,
    ipl_note,
    latitude_entite,
    longitude_entite,
    lat_long,
    CASE 
        WHEN prix_ttc_m3 < 1.78 THEN 1
        WHEN prix_ttc_m3 >= 1.78 THEN 0
        ELSE null
    END AS prix_note,
    CASE 
        WHEN tx_conformite_microbiologie < 99 THEN 1
        WHEN tx_conformite_microbiologie >= 99 THEN 0
        ELSE null
    END AS tx_micro_note,
        CASE 
        WHEN tx_conformite_physiochimiques < 99 THEN 1
        WHEN tx_conformite_physiochimiques >= 99 THEN 0
        ELSE null
    END AS tx_physio_note,
            CASE 
        WHEN ipl_note <= 3 THEN 1
        WHEN ipl_note > 3 THEN 0
        ELSE null
    END AS ipl_flag_note,
FROM {{ ref("int_ad_entite_coordinates") }}
)

SELECT flag_tab.*,
prix_note+tx_micro_note+tx_physio_note+ipl_flag_note as total_note,
FROM flag_tab
