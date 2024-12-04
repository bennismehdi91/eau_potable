import streamlit as st
import pandas as pd
import numpy as np
from google.cloud import bigquery
import os
import plotly.express as px
import plotly.graph_objects as go


credentials = st.secrets["bigquery"]
client = bigquery.Client.from_service_account_info(credentials)

### query to select data and turn it into dataframe
image = os.path.join(os.path.dirname(__file__), "files/logo.png")

col1, col2, col3 = st.columns([1, 1, 1], vertical_alignment="center")
with col2:
    st.image(image)

st.header("Prix de l'eau - Suivi de votre commune")

file_path = os.path.join(os.path.dirname(__file__), "files/code_cities.csv")
cities = pd.read_csv(file_path, sep=";")

# Input search bar
query = st.text_input("Rechercher votre une commune (nom et/ou code postal)")

# List of options
options = list(cities["nom_commune_zip"])

# Filter the list based on the query
if query:
    filtered_options = [option for option in options if query.lower() in option.lower()]
else:
    filtered_options = [options[15566]]

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

name = cities["nom_commune_adherente"].iloc[0]

st.subheader(f"Scorecard en 2022 : {name}")

df_2022 = df[df["year"] == 2022]

if df_2022.empty:
    "Données 2022 non déclarées par la commune"
else:
    prix = (
        df_2022["prix_ttc_m3"].mean()
        if not np.isnan(df_2022["prix_ttc_m3"].mean())
        else 0
    )
    abonnes = (
        int(df_2022["nb_abonnes"].mean())
        if not np.isnan(df_2022["nb_abonnes"].mean())
        else 0
    )
    conso_moyenne = (
        int(df_2022["consommation_moyenne_par_abonne"].mean())
        if not np.isnan(df_2022["consommation_moyenne_par_abonne"].mean())
        else 0
    )
    facture_moyenne = (
        int((prix * conso_moyenne)) if not np.isnan(prix * conso_moyenne) else 0
    )
    lineaire = (
        int(df_2022["lineaire_reseau_hors_branchement"].mean())
        if not np.isnan(df_2022["lineaire_reseau_hors_branchement"].mean())
        else 0
    )
    nom_entite = (
        df_2022["nom_entite_de_gestion"].max()
        if df_2022["nom_entite_de_gestion"].notna().any()
        else "Information non déclarée"
    )
    mode_de_gestion = (
        df_2022["mode_de_gestion"].max()
        if df_2022["mode_de_gestion"].notna().any()
        else "Information non déclarée"
    )

    st.markdown(
        """
        <style>
        .custom-metric {
            background-color: rgba(211, 211, 211, 0.30);
            padding: 10px; 
            border-radius: 5px; 
            text-align: center;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    style_scorecard = "font-size: 40px; font-weight: bold; color: #0072F0"

    info_missing = (
        "<span style='font-weight: bold; color: #0072F0'> Information manquante</span>"
    )
    col1, col2, col3 = st.columns([1, 1, 1], vertical_alignment="center")
    with col1:

        # Display your metric with custom styling
        st.markdown(
            f"""
            <div class="custom-metric">
                Nom de l'entité de gestion : <span style="font-weight:bold;color: #0072F0 ">{nom_entite}</span><br><br>
                Mode de gestion : <span style="font-weight:bold;color: #0072F0 ">{mode_de_gestion}</span>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with col2:
        if abonnes != 0:
            st.markdown(
                f"""
                <div class="custom-metric">
                    Nombre d'abonnés <br><br> 
                    <span style="{style_scorecard}">{abonnes}</span><br>
                </div>
                """,
                unsafe_allow_html=True,
            )
        else:
            st.markdown(
                f"""
                <div class="custom-metric">
                    Nombre d'abonnés <br><br> 
                   {info_missing}<br><br>
                </div>
                """,
                unsafe_allow_html=True,
            )
    with col3:
        if prix != 0:
            st.markdown(
                f"""
                <div class="custom-metric">
                    Prix ttc m3<br><br>
                    <span style="{style_scorecard}">{prix} €</span>
                </div>
                """,
                unsafe_allow_html=True,
            )
        else:
            st.markdown(
                f"""
                <div class="custom-metric">
                    Prix ttc m3 <br><br> 
                   {info_missing}<br><br>
                </div>
                """,
                unsafe_allow_html=True,
            )
    st.text("")
    col1, col2, col3 = st.columns([1, 1, 1], vertical_alignment="center")
    with col1:
        if conso_moyenne != 0:
            st.markdown(
                f"""
                <div class="custom-metric">
                    Consommation moyenne par foyer<br> <span style="{style_scorecard}">{conso_moyenne}</span>
                </div>
                """,
                unsafe_allow_html=True,
            )
        else:
            st.markdown(
                f"""
                <div class="custom-metric">
                    Consommation moyenne par foyer<br> 
                   {info_missing}<br><br>
                </div>
                """,
                unsafe_allow_html=True,
            )
    with col2:

        if facture_moyenne != 0:
            st.markdown(
                f"""
                <div class="custom-metric">
                    Facture moyenne <br>annuelle <br> 
                    <span style="{style_scorecard}">{facture_moyenne} €</span><br>
                </div>
                """,
                unsafe_allow_html=True,
            )
        else:
            st.markdown(
                f"""
                <div class="custom-metric">
                    Facture moyenne <br>annuelle<br> 
                   {info_missing}<br><br>
                </div>
                """,
                unsafe_allow_html=True,
            )
    with col3:
        if lineaire != 0:
            st.markdown(
                f"""
                <div class="custom-metric">
                    Linéaire réseau <br><br> 
                    <span style="{style_scorecard}">{lineaire} kms</span><br>
                </div>
                """,
                unsafe_allow_html=True,
            )
        else:
            st.markdown(
                f"""
                <div class="custom-metric">
                    Linéaire réseau<br><br> 
                   {info_missing}<br><br>
                </div>
                """,
                unsafe_allow_html=True,
            )


st.divider()

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

if df.empty:
    f"Pas de données pour {selected_option}"
else:
    fig1 = px.line(
        tcd,
        x="year",
        y="prix_ttc_m3",
        text="prix_ttc_m3",
    )
    fig1.update_traces(textposition="top center", line=dict(color="#0072F0"))
    fig1.update_layout(
        yaxis_range=[tcd["prix_ttc_m3"].min() - 0.5, tcd["prix_ttc_m3"].max() + 0.5],
        yaxis_title="Prix TTC (€ / m³)",
        xaxis_title="Année",
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
            line=dict(color="#0072F0"),
        )
    )

    # Add second trace
    fig2.add_trace(
        go.Scatter(
            x=tcd["year"],
            y=tcd["tx_conformite_physiochimiques"],
            name="Physiochimiques",
            yaxis="y2",
            line=dict(color="#F06292"),
        )
    )

    min_micro = tcd["tx_conformite_microbiologie"].min()
    min_physio = tcd["tx_conformite_physiochimiques"].min()
    if min_micro < min_physio:
        min_scale = min_micro - 5
    else:
        min_scale = min_physio - 5

    # Define y-axes
    fig2.update_layout(
        title="Microbiologie vs Physiochimiques",
        xaxis=dict(title="Années"),
        yaxis=dict(
            title="Microbiologie & Physiochimiques",
            range=[min_scale, 102],
        ),
        yaxis2=dict(
            range=[min_scale, 102],
            overlaying="y",
        ),
    )

    st.plotly_chart(fig2)

    fig3 = px.line(
        tcd,
        x="year",
        y="ipl_note",
        title="Indice de Perte Linéaire",
        text="ipl_note",
    )

    fig3.update_traces(textposition="top center", line=dict(color="#0072F0"))
    fig3.update_layout(
        yaxis_range=[tcd["ipl_note"].min() - 0.5, tcd["ipl_note"].max() + 0.5],
        yaxis_title="Indice de Perte Linéaire (fuites)",
        xaxis_title="Année",
        xaxis=dict(showgrid=False),
        yaxis=dict(showgrid=False),
    )
    st.plotly_chart(fig3)
