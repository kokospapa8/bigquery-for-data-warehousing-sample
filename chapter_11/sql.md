# Chapter 11 SQL Sample Code
```sql
SELECT SKU, COUNT(*), SUM(Price) FROM `{project.dataset.sales}` --replace this with table you created
WHERE SKU = "1001" -- the green tea SKU
AND Date BETWEEN "2020-06-27" AND "2020-06-28"
GROUP BY SKU
```
