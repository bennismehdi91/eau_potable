import streamlit as st
import pandas as pd
from google.cloud import bigquery
import os
import plotly.express as px
import plotly.graph_objects as go


local = False

if local:
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = (
        "/home/mehdibennis/projects/lewagon/api_googlebigquery/eaupotable-442812-b1a5289718c4.json"
    )
    client = bigquery.Client()
else:
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
SELECT * FROM `eaupotable-442812.dbt_elewagon.mart_cities_aggregated_MB`
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


st.subheader("Scorecard en 2022")


df_2022 = df[df["year"] == 2022]

if df_2022.empty:
    f"Pas de données en 2022 pour {selected_option}"
else:
    prix = df_2022["prix_ttc_m3"].mean()
    abonnes = int(df_2022["nb_abonnes"].mean())
    conso_moyenne = int(df_2022["consommation_moyenne_par_abonne"].mean())
    facture_moyenne = int((prix * conso_moyenne))
    lineaire = int(df_2022["lineaire_reseau_hors_branchement"].mean())
    nom_entite = df_2022["nom_entite_de_gestion"].max()
    mode_de_gestion = df_2022["mode_de_gestion"].max()

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
                Nom de l'entité de gestion : <span style="font-weight:bold;color: #5C7FCA ">{nom_entite}</span><br><br>
                Type de gestion : <span style="font-weight:bold;color: #5C7FCA ">{mode_de_gestion}</span>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with col2:

        # Display your metric with custom styling
        st.markdown(
            f"""
            <div class="custom-metric">
                Nombre d'abonnés <br><br> 
                <span style="{style_scorecard}">{abonnes}</span><br>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with col3:
        # Display your metric with custom styling
        st.markdown(
            f"""
            <div class="custom-metric">
                Prix ttc m3<br><br>
                <span style="{style_scorecard}">{prix} €</span>
            </div>
            """,
            unsafe_allow_html=True,
        )
    st.text("")
    col1, col2, col3 = st.columns([1, 1, 1], vertical_alignment="center")
    with col1:
        # Display your metric with custom styling
        st.markdown(
            f"""
            <div class="custom-metric">
                Consommation moyenne par foyer<br> <span style="{style_scorecard}">{conso_moyenne}</span>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with col2:

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
    with col3:
        # Display your metric with custom styling
        st.markdown(
            f"""
            <div class="custom-metric">
                Linéaire réseau <br><br> 
                <span style="{style_scorecard}">{lineaire} kms</span><br>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.divider()
    # Create bar

st.subheader("Evolution du Prix")

tcd = pd.pivot_table(
    df,
    index="year",
    values=[
        "prix_ttc_m3",
        "tx_conformite_microbiologie",
        "tx_conformite_physiochimiques",
        "ipl_note",
    ],
    aggfunc="mean",
).reset_index()

tcd["prix_ttc_m3"] = tcd["prix_ttc_m3"].round(2)

if tcd.empty:
    f"Pas de données pour {selected_option}"
else:

    fig1 = px.line(
        tcd,
        x="year",
        y="prix_ttc_m3",
        text="prix_ttc_m3",
    )
    fig1.update_traces(textposition="top center")
    fig1.update_layout(
        yaxis_range=[tcd["prix_ttc_m3"].min() - 0.5, tcd["prix_ttc_m3"].max() + 0.5],
        yaxis_title="Prix TTC (€ / m³)",
        xaxis_title="Année",
        # plot_bgcolor="white",
        # paper_bgcolor="white",
        xaxis=dict(showgrid=False),
        yaxis=dict(showgrid=False),
    )
    st.plotly_chart(fig1)

    st.subheader("Indicateurs qualité")

    # Create dual-axis plot
    fig2 = go.Figure()

    # Add first trace
    fig2.add_trace(
        go.Scatter(
            x=tcd["year"],
            y=tcd["tx_conformite_microbiologie"],
            name="Microbiologie",
            yaxis="y1",
            line=dict(color="blue"),
        )
    )

    # Add second trace
    fig2.add_trace(
        go.Scatter(
            x=tcd["year"],
            y=tcd["tx_conformite_physiochimiques"],
            name="Physiochimiques",
            yaxis="y2",
            line=dict(color="green"),
        )
    )

    # Define y-axes
    fig2.update_layout(
        title="Microbiologie vs Physiochimiques",
        xaxis=dict(title="Années"),
        yaxis=dict(
            title="Microbiologie",
            titlefont=dict(color="blue"),
            tickfont=dict(color="blue"),
            range=[tcd["tx_conformite_physiochimiques"].min() - 3, 100],
        ),
        yaxis2=dict(
            title="Physiochimiques",
            titlefont=dict(color="green"),
            tickfont=dict(color="green"),
            range=[tcd["tx_conformite_microbiologie"].min() - 3, 100],
            overlaying="y",
            side="right",
        ),
    )

    st.plotly_chart(fig2)

    fig3 = px.line(
        tcd,
        x="year",
        y="ipl_note",
        title="Indice de Perte Linéaire",
    )
    fig3.update_traces(textposition="top center")
    fig3.update_layout(
        yaxis_range=[tcd["ipl_note"].min() - 0.5, tcd["ipl_note"].max() + 0.5],
        yaxis_title="Indice de Perte Linéaire (fuites)",
        xaxis_title="Année",
        # plot_bgcolor="white",
        # paper_bgcolor="white",
        xaxis=dict(showgrid=False),
        yaxis=dict(showgrid=False),
    )
    st.plotly_chart(fig3)
