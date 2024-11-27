SELECT *
,  CASE 
    WHEN IPL_classement = 'bon' THEN 4
    WHEN IPL_classement = 'acceptable' THEN 3
    WHEN IPL_classement = 'mediocre' THEN 2
    WHEN IPL_classement = 'mauvais' THEN 1
    ELSE 0
  END AS IPL_note
FROM {{ ref('int_ag_appreciation_IPL') }}