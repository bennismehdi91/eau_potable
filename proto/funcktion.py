import pandas as pd
from google.cloud import bigquery


def get_query (select_query : str) -> pd.DataFrame :
    """
    get data from a table from BigQuery
    """
    client = bigquery.Client()
    query = select_query
    query_job = client.query(query)
    results = query_job.result()
    columns = [field.name for field in results.schema]
    data = [dict(row.items()) for row in results]
    df = pd.DataFrame(data, columns=columns)

    return df