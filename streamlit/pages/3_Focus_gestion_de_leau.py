import streamlit as st ## pour récupérer streamlit
import pandas as pd # always need pandas
from google.cloud import bigquery # pour se connecter à bigQuery et récupérer les tables préparée
import os # pour s'autentifier à Google Cloud Plateform
import plotly.express as px # bibli pour graph

local = True # pour avoir un visuel streamlit sur son pc

if local:
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/home/agathedubly/projects/eaupotable-442812-b1a5289718c4.json"
    client = bigquery.Client()
else:
    credentials = st.secrets["bigquery"]
    client = bigquery.Client.from_service_account_info(credentials)


#Ajouter un titre
st.title("Comment se structure la gestion de l'eau en France ?")

""

st.subheader("Les services d'eau se concentrent et se professionnalisent")

query = "SELECT * FROM `eaupotable-442812.dbt_adubly.mart_ad_histo_categ_services`"
query_job = client.query(query)
results = query_job.result()
columns = [field.name for field in results.schema]
data = [dict(row.items()) for row in results]
df = pd.DataFrame(data, columns=columns)



fig = px.bar(df,
             x='year',
             y=['count_id_sispea_entite_gestion'], 
             color='cluster_3_pop_service',
             title='Somme de count_id_sispea_entite_gestion par année et par cluster',
             labels={'count_id_sispea_entite_gestion': 'Somme de count_id_sispea_entite_gestion',
                     'year': 'Année',
                     'cluster_3_pop_service': 'Cluster'})
st.plotly_chart(fig)


st.divider()

col1, col2, col3 = st.columns([1,1,1])

with col1:
    client = bigquery.Client()
    query = "SELECT * FROM eaupotable-442812.dbt_adubly.mart_ad_regie_delegue"
    query_job = client.query(query)
    results = query_job.result()
    columns = [field.name for field in results.schema]
    data = [dict(row.items()) for row in results]
    df_donnets1 = pd.DataFrame(data, columns=columns)
    
    fig = px.pie(
        df_donnets1,
        names="mode_de_gestion",
        values="nb_services",
        title="Répartition des services par mode de gestion",
        labels={"mode_de_gestion": "Mode de gestion"}
    )

    # Ajouter les étiquettes en pourcentage
    fig.update_traces(textinfo="percent+label")

    # Affichage du graphique
    st.plotly_chart(fig)

with col2: 
    "Population desservie par service categ 1, categ 2, categ 3"
with col3:
    "A réfléchir"
