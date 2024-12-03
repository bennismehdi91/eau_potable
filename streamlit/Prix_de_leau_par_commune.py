import streamlit as st
import pandas as pd
from google.cloud import bigquery
import os
import plotly.express as px


credentials = st.secrets["bigquery"]
client = bigquery.Client.from_service_account_info(credentials)

### query to select data and turn it into dataframe

st.header("Prix de l'eau - Suivi de votre commune")

# Input search bar
query = st.text_input("Rechercher votre une commune (nom et/ou code postal)")

file_path = os.path.join(os.path.dirname(__file__), "files/code_cities.csv")
cities = pd.read_csv(file_path, sep=";")

# List of options
options = list(cities["nom_commune_zip"])

# Filter the list based on the query
if query:
    filtered_options = [option for option in options if query.lower() in option.lower()]
else:
    filtered_options = options

# Ensure there's at least one matching option
if not filtered_options:
    st.error("Aucune commune correspondante. Veuillez affiner votre recherche.")
    st.stop()

# Handle single or multiple options
if len(filtered_options) > 1:
    selected_option = st.selectbox("Préciser la localisation :", filtered_options)
else:
    selected_option = filtered_options[0]

# Filter cities and get the INSEE code
cities = cities[cities["nom_commune_zip"] == selected_option]
if cities.empty:
    st.error("Erreur : aucune commune correspondante.")
    st.stop()

code_insee = cities["code_insee_commune_adherente"].iloc[0]

# Query BigQuery
query = f"""
SELECT * 
FROM `eaupotable-442812.dbt_elewagon.mart_cities_final` 
WHERE code_insee_commune_adherente = '{code_insee}'
"""
try:
    query_job = client.query(query)
    results = query_job.result()
    columns = [field.name for field in results.schema]
    data = [dict(row.items()) for row in results]
    df = pd.DataFrame(data, columns=columns)
except Exception as e:
    st.error(f"BigQuery Error: {str(e)}")
    st.stop()

st.subheader("Scorecard")

### Metrics pour la scorecard 2022

###
# nom_entite_de_gestion
# année = year
# Mode de gestion = mode_de_gestion
# Prix TTC m3 en 2022 = prix_ttc_m3
# tx_conformite_microbiologie
# tx_conformite_physiochimiques
# ipl_note
# Nombre d'abonne = nb_abonnes
# conso moyenne par abonne = consommation_moyenne_par_abonne
# lineaire_reseau_hors_branchement

##### Prix
prix = df["prix_ttc_m3"].mean().round(2)
formatted_prix = formatted_mean = f"{prix :.2f} €"

##### Nb Abos
nb_abo = int(df["nb_abonnes"].min())

##### Conso moyenne
mean_conso = int(df.loc[0, "consommation_moyenne_par_abonne"])
formatted_mean = f"{mean_conso} m³"

##### Facture moyenne
facture_moyenne = int((prix * mean_conso))

##### Linéaire réseau
formatted_lin_reseau = df.loc[0, "lineaire_reseau_hors_branchement"]

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
    unsafe_allow_html=True,
)

style_scorecard = "font-size: 40px; font-weight: bold; color: #5C7FCA"

col1, col2, col3 = st.columns([1, 1, 1], vertical_alignment="center")
with col1:

    # Display your metric with custom styling
    st.markdown(
        f"""
        <div class="custom-metric">
            Nombre d'abonnés <br><br> 
            <span style="{style_scorecard}">{nb_abo}</span><br>
        </div>
        """,
        unsafe_allow_html=True,
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
        unsafe_allow_html=True,
    )
with col3:
    # Display your metric with custom styling
    st.markdown(
        f"""
        <div class="custom-metric">
            Consommation moyenne par foyer<br> <span style="{style_scorecard}">{formatted_mean}</span>
        </div>
        """,
        unsafe_allow_html=True,
    )
st.text("")
col1, col2 = st.columns([1, 1], vertical_alignment="center")
with col1:

    # Display your metric with custom styling
    st.markdown(
        f"""
        <div class="custom-metric">
            Facture moyenne <br>annuelle <br> 
            <span style="{style_scorecard}">{facture_moyenne} €</span><br>
        </div>
        """,
        unsafe_allow_html=True,
    )
with col2:
    # Display your metric with custom styling
    st.markdown(
        f"""
        <div class="custom-metric">
            Linéaire réseau <br><br> 
            <span style="{style_scorecard}">{formatted_lin_reseau}</span><br>
        </div>
        """,
        unsafe_allow_html=True,
    )


st.divider()
# Create bar

st.subheader("Evolution du Prix")

df

fig1 = px.line(df, x="year", y="moy_prix_ttc_m3")

# fi2.update
fig1.update_layout(
    # yaxis_range=[1.7, 5],
    yaxis_title="Prix TTC (€ / m³)",
    xaxis_title="Année",
    # plot_bgcolor="white",
    # paper_bgcolor="white",
    xaxis=dict(showgrid=False),
    yaxis=dict(showgrid=False),
)
st.plotly_chart(fig1)

# #####################################################

# query = "SELECT * FROM `eaupotable-442812.dbt_agonternew.mart_ag_group_by_dpt_for_map`"
# query_job = client.query(query)
# results = query_job.result()
# columns = [field.name for field in results.schema]
# data = [dict(row.items()) for row in results]
# df3 = pd.DataFrame(data, columns=columns).sort_values(by="year")


# # Step 2: Load GeoJSON file for French departments
# geojson_url = "https://raw.githubusercontent.com/gregoiredavid/france-geojson/master/departements.geojson"

# # Create the animated choropleth map
# fig2 = px.choropleth(
#     df3,
#     geojson=geojson_url,  # GeoJSON data
#     locations="departement",  # Column in DataFrame linking to GeoJSON properties
#     featureidkey="properties.code",  # Key in GeoJSON properties for regions
#     color="moy_prix_ttc_m3",  # Column to colorize
#     animation_frame="year",  # Column defining animation frames (e.g., years)
#     color_continuous_scale="balance",  # Color scale
#     title="Evolution du prix en France",
#     range_color=[0, 4],  # Dynamic fixed range
# )

# # Update layout for better visuals
# fig2.update_geos(fitbounds="locations", visible=False)

# # Show the map
# st.plotly_chart(fig2)
