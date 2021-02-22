from google.cloud import bigquery
client = bigquery.Client()

def process_incoming_file(data, context):
  # TODO: create table with follwing schema
  # StoreID:STRING,SKU:STRING,Date:DATE,Price:NUMERIC
  table_name = "{project.dataste.sales}"
  uri = "gs://{bucket}/{file}".format(bucket=data["bucket"], file=data["name"])
  job_config = bigquery.LoadJobConfig(
    schema=[
      bigquery.SchemaField("StoreID", "STRING"),
      bigquery.SchemaField("SKU", "STRING"),
      bigquery.SchemaField("Date", "DATE"),
      bigquery.SchemaField("Price", "NUMERIC")
    ],
    skip_leading_rows = 1,
    time_partitioning = bigquery.TimePartitioning(
      type_=bigquery.TimePartitioningType.DAY,
      field="Date"
    )
  )
  job = client.load_table_from_uri(uri, table_name, job_config=job_config)
  job.result()

  table = client.get_table(table_name)
  print("Loaded {rows} rows from file {uri}".format(rows=table.num_rows, uri=uri))
