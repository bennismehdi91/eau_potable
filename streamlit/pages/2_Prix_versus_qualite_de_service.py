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