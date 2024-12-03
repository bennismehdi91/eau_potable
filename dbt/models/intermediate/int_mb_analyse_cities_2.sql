{{ config(
    materialized='table'
) }}

SELECT
*
FROM
{{ ref('int_mb_analyse_cities') }}
