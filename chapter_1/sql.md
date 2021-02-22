# Chapter 1 SQL Sample Code 

```sql
SELECT
  spc_common AS species,
  COUNT(*) number_of_trees,
FROM
  `bigquery-public-data.new_york.tree_census_2015`
WHERE
  spc_common != ""
  AND health = "Good"
GROUP BY
  spc_common,
  health
ORDER BY
  number_of_trees DESC
LIMIT
  10
```

```sql
SELECT
  name
FROM
  fruit
WHERE
  shape = "round"
```
