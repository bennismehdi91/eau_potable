import streamlit as st
from google.cloud import bigquery
import pandas as pd

st.markdown('Test test')

"test test"

st.header('title')

# Initialize the BigQuery client
credentials = st.secrets["bigquery"]

client = bigquery.Client.from_service_account_info(credentials)

# Query BigQuery
query = "SELECT * FROM `eaupotable-442812.dbt_elewagon.mart_mb_correlation_abonnesprice` LIMIT 10"
df = client.query(query).to_dataframe()

