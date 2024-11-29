import streamlit as st
import pandas as pd
from google.cloud import bigquery
import os
import plotly.express as px

local = True

if local:
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/home/aureliegont/projects/eaupotable-442812-b1a5289718c4.json"
    client = bigquery.Client()
else:
    credentials = st.secrets["bigquery"]
    client = bigquery.Client.from_service_account_info(credentials)


### query to select data and turn it into dataframe
query = "SELECT * FROM eaupotable-442812.dbt_agonternew.mart_ag_evol_prix_qualite_sans_cluster"
query_job = client.query(query)
results = query_job.result()
columns = [field.name for field in results.schema]
data = [dict(row.items()) for row in results]
df = pd.DataFrame(data, columns=columns)




st.header("La gestion administrative serait-elle un axe d'influence sur le prix de l'eau' ?")

st.markdown(
    """
    <style>
    .custom-metric {
        background-color: rgba(0, 123, 255, 0.2); /* Light blue background with 20% opacity */
        padding: 10px; /* Add some padding */
        border-radius: 5px; /* Rounded corners */
        text-align: center; /* Center align text */
        font-size: 1.5rem; /* Adjust font size if needed */
        font-weight: bold; /* Make text bold */
    }
    </style>
    """,
    unsafe_allow_html=True
)
# Display your metric with custom styling
st.markdown(
    f"""
    <div class="custom-metric">
        Prix: {formatted_prix}
    </div>
    """,
    unsafe_allow_html=True
)



