# Chapter 5 CLI Code

## copy source to GCS
```bash
gsutil -m cp {source} gs://{bucket}/{location}
```

## show schema for any table
```
bq show --format=prettyjson {dataset.table}
```

## Preprocessing Files
```bash
bq load --project_id="{YOUR_PROJECT}" --autodetect "dataset.gpa_table" ./gpa.
bq show --format=prettyjson {dataset.table}
  "schema": {
    "fields": [
      {
        "mode": "NULLABLE",
        "name": "Author",
        "type": "STRING"
      }, {
        "mode": "NULLABLE",
        "name": "Title",
        "type": "STRING"
      }, {
        "mode": "NULLABLE",
        "name": "LexicalDiversity",
        "type": "FLOAT"
     }
    ]
   }
```

## Delete old table and copy the temoporary table back.
```bash
bq rm {my-project}:dataset.gpa_table
bq cp --project_id={my-project} dataset.gpa_table_temp dataset.gpa_table
bq rm {my-project}:dataset.gpa_table_temp
```

## Loading Files
```bash
bq load --source_format=CSV dataset.table gs://data-bucket/file.csv ./schema.json
bq load --source_format=CSV dataset.table gs://data-bucket/file*.csv ./schema.json
```

##
```bash
ls **/*.csv | sed "s/.*/"&"/" | tr "\n" ","
```
