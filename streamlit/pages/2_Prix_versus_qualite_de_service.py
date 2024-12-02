import streamlit as st
import pandas as pd
from google.cloud import bigquery
import os
import plotly.express as px
import plotly.graph_objects as go

local = True

if local:
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/home/aureliegont/projects/eaupotable-442812-b1a5289718c4.json"
    client = bigquery.Client()
else:
    credentials = st.secrets["bigquery"]
    client = bigquery.Client.from_service_account_info(credentials)


### query to select data and turn it into dataframe
query = "SELECT * FROM eaupotable-442812.dbt_atorne.marte_at_scorecard_p3"
query_job = client.query(query)
results = query_job.result()
columns = [field.name for field in results.schema]
data = [dict(row.items()) for row in results]
df = pd.DataFrame(data, columns=columns)

#titre de la page sur la qualité versus prix
st.header("La qualité serait-elle un axe d'influence sur le prix de l'eau ?")
st.subheader('Les données de 2022')

### prix de l'eau en 2022
prix_2022 = float(df['prix_ttc_m3'])

### indice microbio en 2022
micro_2022 = float(df['tx_conformite_microbio'])

### indice physio en 2022
physio_2022 = float(df['tx_conformite_physiochimiques'])

### indice IPL
lostwater_2022 = df['perte_m3_2022']/1000000000
lostwater_2022_round=float(lostwater_2022.round(2))

### create background of the scorecard
st.markdown(
    """
    <style>
    .custom-metric {
        background-color: rgba(211, 211, 211, 0.30); /* Light blue background with 20% opacity */
        padding: 10px; /* Add some padding */
        border-radius: 5px; /* Rounded corners */
        text-align: center; /* Center align text */
    }
    </style>
    """,
    unsafe_allow_html=True
)
style_scorecard = "font-size: 40px; font-weight: bold; color: #5C7FCA"
col1, col2, col3 , col4 = st.columns([1, 1, 1, 1], vertical_alignment="center")


with col1:
# Display your metric with custom styling
    st.markdown(
        f"""
        <div class="custom-metric">
            Prix moyen<br>(€)<br>
            <span style="{style_scorecard}">{prix_2022}</span>
        </div>
        """,
        unsafe_allow_html=True
    )

with col2:
# Display your metric with custom styling
    st.markdown(
        f"""
        <div class="custom-metric">
            Indice microbiologique (%)<br>
            <span style="{style_scorecard}">{micro_2022}</span>
        </div>
        """,
        unsafe_allow_html=True
    )

with col3:
# Display your metric with custom styling
    st.markdown(
        f"""
        <div class="custom-metric">
            Indice physiochimique (%)<br>
            <span style="{style_scorecard}">{physio_2022}</span>
        </div>
        """,
        unsafe_allow_html=True
    )

with col4:
# Display your metric with custom styling
    st.markdown(
        f"""
        <div class="custom-metric">
            Perte d'eau <br>(en milliard de Litre)<br>
            <span style="{style_scorecard}">{lostwater_2022_round}</span>
        </div>
        """,
        unsafe_allow_html=True
    )


### create background the call out
st.markdown(
    """
    <style>
    .callout {
        background-color: rgba(175, 253, 242, 0.50); /* yellow background with 20% opacity */
        padding: 10px; /* Add some padding */
        border-radius: 5px; /* Rounded corners */
        text-align: center; /* Center align text */
    }
    </style>
    """,
    unsafe_allow_html=True
)

col1, col2 = st.columns([1,6], vertical_alignment="center")


with col1:
# Display a icon
    st.markdown(
        f"""
        <div class="callout">
            loremispum
        </div>
        """,
        unsafe_allow_html=True
    )

with col2:
# Display a icon
    st.markdown(
        f"""
        <div class="callout"><br>
            my name is stupid 
            <br>
        </div>
        """,
        unsafe_allow_html=True
    )



st.subheader('Quelle évolution de ses indicateurs en fonction du temps ?')

# Query Bigquery
query = "SELECT * FROM `eaupotable-442812.dbt_agonternew.mart_ag_evol_prix_qualite_sans_cluster`"
query_job = client.query(query)
results = query_job.result()
columns = [field.name for field in results.schema]
data = [dict(row.items()) for row in results]
df_qualite = pd.DataFrame(data, columns=columns)

# Créer le graphique combiné
fig = go.Figure()

# Ajouter les lignes pour moy_microbio et moy_physio
fig.add_trace(go.Scatter(x=df_qualite["year"], y=df_qualite["moy_microbio"],
                         mode="lines+markers", name="moy_microbio",
                         line=dict(color="blue")))
fig.add_trace(go.Scatter(x=df_qualite["year"], y=df_qualite["moy_physio"],
                         mode="lines+markers", name="moy_physio",
                         line=dict(color="green")))

# Ajouter le bar chart pour moy_IPL_note avec un axe Y secondaire
fig.add_trace(go.Bar(x=df_qualite["year"], y=df_qualite["moy_IPL_note"],
                     name="moy_IPL_note", marker=dict(color="rgba(255, 100, 100, 0.7)"),
                     yaxis="y2"))

# Mettre à jour les axes
fig.update_layout(
    title="Évolution des indices de qualité et des moyennes IPL",
    xaxis=dict(title="Année"),
    yaxis=dict(
        title="Indices moy_microbio et moy_physio",
        titlefont=dict(color="blue"),
        tickfont=dict(color="blue"),
        range=[80, 100]  # Adapter aux valeurs
    ),
    yaxis2=dict(
        title="Indice moy_IPL_note",
        titlefont=dict(color="red"),
        tickfont=dict(color="red"),
        overlaying="y",  # Superposer sur l'axe principal
        side="right",    # Positionner à droite
        range=[0, 3]  # Adapter aux valeurs
    ),
    legend=dict(title="Indicateurs", x=0.5, y=1.1, orientation="h"),
    barmode="overlay"  # Les barres superposées
)

# Afficher le graphique
st.plotly_chart(fig)