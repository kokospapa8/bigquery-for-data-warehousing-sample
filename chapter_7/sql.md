# Chapter 7 SQL Sample Code
## Dataflow SQL sample

```sql
SELECT
  TUMBLE_START("INTERVAL 1 MINUTE"),
  t.Name,
  SUM(Price) TotalSales
FROM
  bigquery.TABLE.`{PROJECT}`.{DATASET}.Products t
INNER JOIN
  pubsub.topic.`{PROJECT}`.`NewSales` d
USING
  (SKU)
GROUP BY
  TUMBLE(d.event_timestamp,
    "INTERVAL 1 MINUTE"),
  Name
```
