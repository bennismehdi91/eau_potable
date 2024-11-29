import streamlit as st
import pandas as pd
from google.cloud import bigquery
import os

local = True

if local:
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/home/mehdibennis/projects/lewagon/api_googlebigquery/eaupotable-442812-b1a5289718c4.json"
    client = bigquery.Client()
else:
    credentials = st.secrets["bigquery"]
    client = bigquery.Client.from_service_account_info(credentials)

### query to select data and turn it into dataframe
query = "SELECT * FROM eaupotable-442812.dbt_atorne.marte_at_scorecard_p2"
query_job = client.query(query)
results = query_job.result()
columns = [field.name for field in results.schema]
data = [dict(row.items()) for row in results]
df = pd.DataFrame(data, columns=columns)

"coucou c'est moi"
"Ceci est un streamlit"

df

"""

### scorecard prix_ttc_m3 
prix = df['prix_ttc_m3'].mean().round(2)
formatted_prix = formatted_mean = f"{prix :.2f} €"
formatted_prix

# scorecard nb_abonnes 
formatted_nb_abonnes = (df['nb_abonnes'] / 1_000_000).round(2).astype(str).str.replace(".", ",") + " M"
formatted_nb_abonnes

# scorecard conso_moy_foyer
mean_conso = df['conso_moy_foyer'].mean().round(0)
formatted_mean = f"{mean_conso:.2f} m³"
formatted_mean

# scorecard nb_services 
formatted_nb_services = df['nb_services'].apply(lambda x: f"{x:,}")
formatted_nb_services

# scorecard lineaire_reseau_km' 
formatted_lin_reseau = (df['lineaire_reseau_km'] / 1_000).round(0).astype(str).str.replace(".", ",") + "K km"
formatted_lin_reseau

"""