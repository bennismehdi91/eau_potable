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

# Run the query
query_job = client.query(query)

# Get the results
results = query_job.result()

# Extract column names from the schema
columns = [field.name for field in results.schema]

# Convert rows to a list of dictionaries
data = [dict(row.items()) for row in results]

# Create a Pandas DataFrame
results_df = pd.DataFrame(data, columns=columns)

results_df
