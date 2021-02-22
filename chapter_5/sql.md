# Chapter 5 SQL Sample Code

## Create table using subquery from `gpa_table`

```sql
CREATE TABLE
  dataset.gpa_table_temp ( LastName STRING NOT NULL,
    FirstName STRING NOT NULL,
    GPA NUMERIC,
    EnrollmentDate DATE NOT NULL,
    ExpectedGraduationYear INT64 NOT NULL ) AS
SELECT
  string_field_0,
  string_field_1,
  SAFE_CAST(int64_field_2 AS NUMERIC),
  date_field_3,
  EXTRACT(YEAR
  FROM
    date_field_3) + 4
FROM
  dataset.gpa_table
```

## Query from CloudSQL using `EXTERNAL_QUERY`
```sql
SELECT
  *
FROM
  EXTERNAL_QUERY("{project_id.US.conntectID}",
    "SELECT * FROM INFORMATION_SCHEMA.TABLES;");
```

```sql
SELECT
  CONCAT("[", GROUP_CONCAT(field SEPARATOR ", "), "]")
FROM (
  SELECT
    JSON_UNQUOTE(JSON_OBJECT("name",
        COLUMN_NAME,
        "mode",
        CASE IS_NULLABLE
          WHEN "YES" THEN "NULLABLE"
        ELSE
        "REQUIRED"
      END
        ,
        "type",
        CASE DATA_TYPE
          WHEN "TINYINT" THEN "INT64"
          WHEN "SMALLINT" THEN "INT64"
          WHEN "MEDIUMINT" THEN "INT64"
          WHEN "LARGEINT" THEN "INT64"
          WHEN "BIGINT" THEN "INT64"
          WHEN "DECIMAL" THEN "NUMERIC"
          WHEN "FLOAT" THEN "FLOAT64"WHEN "DOUBLE" THEN "FLOAT64"
          WHEN "CHAR" THEN "STRING"
          WHEN "VARCHAR" THEN "STRING"
          WHEN "TINYTEXT" THEN "STRING"
          WHEN "TEXT" THEN "STRING"
          WHEN "MEDIUMTEXT" THEN "STRING"
          WHEN "LONGTEXT" THEN "STRING"
          WHEN "BINARY" THEN "BYTES"
          WHEN "VARBINARY" THEN "BYTES"
          WHEN "DATE" THEN "DATE"
          WHEN "TIME" THEN "TIME"
          WHEN "DATETIME" THEN "DATETIME"
          WHEN "TIMESTAMP" THEN "TIMESTAMP"
        ELSE
        "!!UNKNOWN!!"
      END
        )) field
  FROM
    INFORMATION_SCHEMA.COLUMNS
  WHERE
    TABLE_NAME="gpa"
  ORDER BY
    ORDINAL_POSITION) R;
```
