import streamlit as st
from google.cloud import bigquery
import pandas as pd

st.markdown('Test test')

"test test"

st.header('title')

# Initialize the BigQuery client
credentials = st.secrets["bigquery"]

client = bigquery.Client.from_service_account_info(credentials)

query = "SELECT * FROM eaupotable-442812.dbt_elewagon.mart_mb_indicateur_quality_aggregated"

query_job = client.query(query)

results = query_job.result()

columns = [field.name for field in results.schema]

data = [dict(row.items()) for row in results]

results_df = pd.DataFrame(data, columns=columns)

import plotly.express as px

fig = px.line(
    results_df,
    x="year",          # X-axis: Year
    y="IPL_note",         # Y-axis: Value
    color="cluster_pop_entite_gestion",     # Different lines for each group
    title="Evolution de l'IPL par année"
)

fig.add_shape(
    type="rect",
    x0=results_df["year"].min(), x1=results_df["year"].max(),
    y0=0, y1=1,
    fillcolor="red",
    opacity=0.1,
    line_width=0
)

fig.add_shape(
    type="rect",
    x0=results_df["year"].min(), x1=results_df["year"].max(),
    y0=1, y1=2,
    fillcolor="yellow",
    opacity=0.1,
    line_width=0
)

fig.add_shape(
    type="rect",
    x0=results_df["year"].min(), x1=results_df["year"].max(),
    y0=2, y1=3,
    fillcolor="green",
    opacity=0.1,
    line_width=0
)

fig2 = px.line(
    results_df,
    x="year",          # X-axis: Year
    y="tx_conformite_physiochimiques",         # Y-axis: Value
    color="cluster_pop_entite_gestion",     # Different lines for each group
    title="Evolution du taux de conformité physiochimiques"
)

fig3 = px.line(
    results_df,
    x="year",          # X-axis: Year
    y="tx_conformite_microbiologie",         # Y-axis: Value
    color="cluster_pop_entite_gestion",     # Different lines for each group
    title="Evolution du taux de conformité microbiologique"
)


# Display the chart
st.plotly_chart(fig)
st.plotly_chart(fig2)
st.plotly_chart(fig3)