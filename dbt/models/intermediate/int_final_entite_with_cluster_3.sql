SELECT
CASE
    -- Auvergne-Rhône-Alpes (12 departments)
    WHEN departement IN ("001", "003", "007", "015", "026", "038", "042", "043", "063", "069", "073", "074") THEN "Auvergne-Rhône-Alpes"
    -- Bourgogne-Franche-Comté (8 departments)
    WHEN departement IN ("021", "025", "039", "058", "070", "071", "089", "090") THEN "Bourgogne-Franche-Comté"
    -- Bretagne (4 departments)
    WHEN departement IN ("022", "029", "035", "056") THEN "Bretagne"
    -- Centre-Val de Loire (6 departments)
    WHEN departement IN ("018", "028", "036", "037", "041", "045") THEN "Centre-Val de Loire"
    -- Corse (2 departments)
    WHEN departement IN ("2A0", "2B0") THEN "Corse"
    -- Grand Est (10 departments)
    WHEN departement IN ("008", "010", "051", "052", "054", "055", "057", "067", "068", "088") THEN "Grand Est"
    -- Hauts-de-France (5 departments)
    WHEN departement IN ("002", "059", "060", "062", "080") THEN "Hauts-de-France"
    -- Île-de-France (8 departments)
    WHEN departement IN ("075", "077", "078", "091", "092", "093", "094", "095") THEN "Île-de-France"
    -- Normandie (5 departments)
    WHEN departement IN ("014", "027", "050", "061", "076") THEN "Normandie"
    -- Nouvelle-Aquitaine (12 departments)
    WHEN departement IN ("016", "017", "019", "023", "024", "033", "040", "047", "064", "079", "086", "087") THEN "Nouvelle-Aquitaine"
    -- Occitanie (13 departments)
    WHEN departement IN ("009", "011", "012", "030", "031", "032", "034", "046", "048", "065", "066", "081", "082") THEN "Occitanie"
    -- Pays de la Loire (5 departments)
    WHEN departement IN ("044", "049", "053", "072", "085") THEN "Pays de la Loire"
    -- Provence-Alpes-Côte d'Azur (6 departments)
    WHEN departement IN ("004", "005", "006", "013", "083", "084") THEN "Provence-Alpes-Côte d'Azur"
    -- Overseas Departments (5 departments)
    WHEN departement IN ("971") THEN "Guadeloupe"
    WHEN departement IN ("972") THEN "Martinique"
    WHEN departement IN ("973") THEN "Guyane"
    WHEN departement IN ("974") THEN "Réunion"
    WHEN departement IN ("976") THEN "Mayotte"
    ELSE "Unknown"
END AS region_name,
CASE
    WHEN departement = "001" THEN "Ain"
    WHEN departement = "003" THEN "Allier"
    WHEN departement = "007" THEN "Ardèche"
    WHEN departement = "015" THEN "Cantal"
    WHEN departement = "026" THEN "Drôme"
    WHEN departement = "038" THEN "Isère"
    WHEN departement = "042" THEN "Loire"
    WHEN departement = "043" THEN "Haute-Loire"
    WHEN departement = "063" THEN "Puy-de-Dôme"
    WHEN departement = "069" THEN "Rhône"
    WHEN departement = "073" THEN "Savoie"
    WHEN departement = "074" THEN "Haute-Savoie"
    WHEN departement = "021" THEN "Côte-d'Or"
    WHEN departement = "025" THEN "Doubs"
    WHEN departement = "039" THEN "Jura"
    WHEN departement = "058" THEN "Nièvre"
    WHEN departement = "070" THEN "Haute-Saône"
    WHEN departement = "071" THEN "Saône-et-Loire"
    WHEN departement = "089" THEN "Yonne"
    WHEN departement = "090" THEN "Territoire de Belfort"
    WHEN departement = "022" THEN "Côtes-d'Armor"
    WHEN departement = "029" THEN "Finistère"
    WHEN departement = "035" THEN "Ille-et-Vilaine"
    WHEN departement = "056" THEN "Morbihan"
    WHEN departement = "018" THEN "Cher"
    WHEN departement = "028" THEN "Eure-et-Loir"
    WHEN departement = "036" THEN "Indre"
    WHEN departement = "037" THEN "Indre-et-Loire"
    WHEN departement = "041" THEN "Loir-et-Cher"
    WHEN departement = "045" THEN "Loiret"
    WHEN departement = "2A0" THEN "Corse-du-Sud"
    WHEN departement = "2B0" THEN "Haute-Corse"
    WHEN departement = "008" THEN "Ardennes"
    WHEN departement = "010" THEN "Aube"
    WHEN departement = "051" THEN "Marne"
    WHEN departement = "052" THEN "Haute-Marne"
    WHEN departement = "054" THEN "Meurthe-et-Moselle"
    WHEN departement = "055" THEN "Meuse"
    WHEN departement = "057" THEN "Moselle"
    WHEN departement = "067" THEN "Bas-Rhin"
    WHEN departement = "068" THEN "Haut-Rhin"
    WHEN departement = "088" THEN "Vosges"
    WHEN departement = "002" THEN "Aisne"
    WHEN departement = "059" THEN "Nord"
    WHEN departement = "060" THEN "Oise"
    WHEN departement = "062" THEN "Pas-de-Calais"
    WHEN departement = "080" THEN "Somme"
    WHEN departement = "075" THEN "Paris"
    WHEN departement = "077" THEN "Seine-et-Marne"
    WHEN departement = "078" THEN "Yvelines"
    WHEN departement = "091" THEN "Essonne"
    WHEN departement = "092" THEN "Hauts-de-Seine"
    WHEN departement = "093" THEN "Seine-Saint-Denis"
    WHEN departement = "094" THEN "Val-de-Marne"
    WHEN departement = "095" THEN "Val-d'Oise"
    WHEN departement = "014" THEN "Calvados"
    WHEN departement = "027" THEN "Eure"
    WHEN departement = "050" THEN "Manche"
    WHEN departement = "061" THEN "Orne"
    WHEN departement = "076" THEN "Seine-Maritime"
    WHEN departement = "016" THEN "Charente"
    WHEN departement = "017" THEN "Charente-Maritime"
    WHEN departement = "019" THEN "Corrèze"
    WHEN departement = "023" THEN "Creuse"
    WHEN departement = "024" THEN "Dordogne"
    WHEN departement = "033" THEN "Gironde"
    WHEN departement = "040" THEN "Landes"
    WHEN departement = "047" THEN "Lot-et-Garonne"
    WHEN departement = "064" THEN "Pyrénées-Atlantiques"
    WHEN departement = "079" THEN "Deux-Sèvres"
    WHEN departement = "086" THEN "Vienne"
    WHEN departement = "087" THEN "Haute-Vienne"
    WHEN departement = "009" THEN "Ariège"
    WHEN departement = "011" THEN "Aude"
    WHEN departement = "012" THEN "Aveyron"
    WHEN departement = "030" THEN "Gard"
    WHEN departement = "031" THEN "Haute-Garonne"
    WHEN departement = "032" THEN "Gers"
    WHEN departement = "034" THEN "Hérault"
    WHEN departement = "046" THEN "Lot"
    WHEN departement = "048" THEN "Lozère"
    WHEN departement = "065" THEN "Hautes-Pyrénées"
    WHEN departement = "066" THEN "Pyrénées-Orientales"
    WHEN departement = "081" THEN "Tarn"
    WHEN departement = "082" THEN "Tarn-et-Garonne"
    WHEN departement = "044" THEN "Loire-Atlantique"
    WHEN departement = "049" THEN "Maine-et-Loire"
    WHEN departement = "053" THEN "Mayenne"
    WHEN departement = "072" THEN "Sarthe"
    WHEN departement = "085" THEN "Vendée"
    WHEN departement = "004" THEN "Alpes-de-Haute-Provence"
    WHEN departement = "005" THEN "Hautes-Alpes"
    WHEN departement = "006" THEN "Alpes-Maritimes"
    WHEN departement = "013" THEN "Bouches-du-Rhône"
    WHEN departement = "083" THEN "Var"
    WHEN departement = "084" THEN "Vaucluse"
    ELSE "Unknown"
END AS departement_name,
CASE
    WHEN tx_conformite_microbiologie = 100 THEN 'ok'
    WHEN tx_conformite_microbiologie < 100 THEN 'Under expectation'
    ELSE 'NA'
END AS tx_microbio_cast,
CASE
    WHEN tx_conformite_physiochimiques = 100 THEN 'ok'
    WHEN tx_conformite_physiochimiques < 100 THEN 'Under expectation'
    ELSE 'NA'
END AS tx_physio_cast,
*
FROM {{ ref('int_final_entite_with_cluster_2') }}