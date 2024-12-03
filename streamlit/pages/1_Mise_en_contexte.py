import streamlit as st
import pandas as pd
from google.cloud import bigquery
import os
import plotly.express as px

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

st.header('Mise en contexte')
st.subheader('Scorecard')

### Metrics pour la scorecard 2022

##### Prix
prix = df['prix_ttc_m3'].mean().round(2)
formatted_prix = formatted_mean = f"{prix :.2f} €"

##### Nb Abos
nb_abo = df['nb_abonnes'].min() / 1000000
nb_abo2 = nb_abo.round(1)

##### Conso moyenne
mean_conso = int(df.loc[0, 'conso_moy_foyer'])
formatted_mean = f"{mean_conso} m³"

##### Facture moyenne
facture_moyenne = int((prix * mean_conso))

##### Nb services
formatted_nb_services = df.loc[0, 'nb_services']/1000

##### Linéaire réseau
formatted_lin_reseau = df.loc[0, 'lineaire_reseau_km'] / 1000

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

col1, col2, col3 = st.columns([1, 1, 1], vertical_alignment="center")
with col1:

    # Display your metric with custom styling
    st.markdown(
        f"""
        <div class="custom-metric">
            Nombre d'abonnés <br>(en millions)<br> 
            <span style="{style_scorecard}">{nb_abo2}</span><br>
        </div>
        """,
        unsafe_allow_html=True
    )
with col2:
        # Display your metric with custom styling
    st.markdown(
        f"""
        <div class="custom-metric">
            Prix ttc m3<br><br>
            <span style="{style_scorecard}">{formatted_prix}</span>
        </div>
        """,
        unsafe_allow_html=True
    )
with col3:
        # Display your metric with custom styling
    st.markdown(
        f"""
        <div class="custom-metric">
            Consommation moyenne par foyer<br> <span style="{style_scorecard}">{formatted_mean}</span>
        </div>
        """,
        unsafe_allow_html=True
    )
st.text('')
col1, col2, col3 = st.columns([1, 1, 1], vertical_alignment="center")
with col1:

    # Display your metric with custom styling
    st.markdown(
        f"""
        <div class="custom-metric">
            Facture moyenne <br>annuelle <br> 
            <span style="{style_scorecard}">{facture_moyenne} €</span><br>
        </div>
        """,
        unsafe_allow_html=True
    )
with col2:
        # Display your metric with custom styling
    st.markdown(
        f"""
        <div class="custom-metric">
            Linéaire réseau <br>(en milliers de kms)<br> 
            <span style="{style_scorecard}">{formatted_lin_reseau}</span><br>
        </div>
        """,
        unsafe_allow_html=True
    )
with col3:
        # Display your metric with custom styling
    st.markdown(
        f"""
        <div class="custom-metric">
            Nombre de services<br><br>
            <span style="{style_scorecard}">{formatted_nb_services}</span>
        </div>
        """,
        unsafe_allow_html=True
    )



query = "SELECT * FROM `eaupotable-442812.dbt_agonternew.mart_ag_evol_prix_qualite_sans_cluster`"
query_job = client.query(query)
results = query_job.result()
columns = [field.name for field in results.schema]
data = [dict(row.items()) for row in results]
df2 = pd.DataFrame(data, columns=columns)

### le retravail du prix df
df2['formatted_price'] = df2['moy_prix_ttc_m3'].apply(lambda x: f"{x:.2f} €")

st.divider()
#Create bar
fig = px.bar(
    df2,
    x="year",
    y="moy_prix_ttc_m3",
    title= "Evolution du prix de l'eau", 
    text='formatted_price')


#fi2.update
fig.update_layout(
    yaxis_range=[1.7, 2.5],
    yaxis_title="Prix TTC (€ / m³)",
    xaxis_title="Année",
    #plot_bgcolor="white",
    #paper_bgcolor="white",
    xaxis=dict(showgrid=False),
    yaxis=dict(showgrid=False)
    )
st.plotly_chart(fig)

#####################################################

query = "SELECT * FROM `eaupotable-442812.dbt_agonternew.mart_ag_group_by_dpt_for_map`"
query_job = client.query(query)
results = query_job.result()
columns = [field.name for field in results.schema]
data = [dict(row.items()) for row in results]
df3 = pd.DataFrame(data, columns=columns).sort_values(by="year")


# Step 2: Load GeoJSON file for French departments
geojson_url = "https://raw.githubusercontent.com/gregoiredavid/france-geojson/master/departements.geojson"

# Create the animated choropleth map
fig2 = px.choropleth(
    df3,
    geojson=geojson_url,        # GeoJSON data
    locations="departement",     # Column in DataFrame linking to GeoJSON properties
    featureidkey="properties.code",  # Key in GeoJSON properties for regions
    color="moy_prix_ttc_m3",               # Column to colorize
    animation_frame="year",      # Column defining animation frames (e.g., years)
    color_continuous_scale="balance",  # Color scale
    title="Evolution du prix en France",
    range_color=[0, 4],  # Dynamic fixed range
)

# Update layout for better visuals
fig2.update_geos(
    fitbounds="locations",
    visible=False)

# Show the map
st.plotly_chart(fig2)