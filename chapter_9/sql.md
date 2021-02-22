# Chapter 9 SQL Sample Code

## sample sql from chapter 1
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

## Grouping
```sql
SELECT
  PageName,
  AVG(ResponseTime)
FROM
  PageLoads
GROUP BY
  PageName
```

```sql
SELECT
  PageName,
  AVG(ResponseTime)
FROM
  PageLoads
GROUP BY
  PageName
ORDER BY
  AVG(ResponseTime) DESC
```

## Star Queries

```sql
SELECT
  A.*,
  B.Name
FROM
  A
JOIN
  B
USING
  (Key)
```

## WITH

```sql
WITH
  Result AS (
  SELECT
    Kind,
    COUNT(*) C
  FROM
    T
  GROUP BY
    Kind)
SELECT
  MAX(C)
FROM
  TableQuery
```

## Inner JOIN
```sql
SELECT
  UserID,
  UserName,
  PetName
FROM
  Users
INNER JOIN
  UserPets
ON
  Users.UserID = UserPets.OwnerID
```

## Subqueries
```sql
SELECT
  Username,
  PhoneNumber,
  NumberOfPets
FROM
  Users
JOIN (
  SELECT
    UserID,
    COUNT(*) NumberOfPets
  FROM
    UserPets
  GROUP BY
    UserID) PetCount
USING
  (UserID)
```

## WITH Clause
```sql
WITH PetCount AS (
  SELECT UserID, COUNT(*) NumberOfPets
  FROM UserPets
  GROUP BY UserID
)
SELECT Username, PhoneNumber, NumberOfPets
FROM Users
JOIN PetCount
  USING (UserID)

```

## UNNEST

```sql
SELECT UserID, PhoneNumber,
(SELECT COUNT(*) FROM UNNEST(UserPets)) PetCount
FROM DW_Users

SELECT UserID, P.PetName
FROM DW_Users
JOIN UNNEST(DW_Users.UserPets) P

SELECT UserPets.PetName FROM DW_Users

```

## Working with Partitions
```sql
SELECT *
FROM IngestionTimePartitionedTable
WHERE _PARTITIONDATE = "2020-01-01"

SELECT * FROM
`bigquery-public-data.ethereum_blockchain.blocks`
WHERE timestamp BETWEEN "2018-07-07T07:00:00Z" AND "2018-07-07T08:00:00Z"
```

```sql
SELECT Department, SUM(Cost) TotalCost
FROM Expenses
GROUP BY Department
HAVING SUM(Cost) > 1000

SELECT Department, SUM(Cost) TotalCost
FROM Expenses
GROUP BY Department
HAVING SUM(Cost) > 1000
GROUP BY ROLLUP(Department)
```

## ARRAY_CONCAT_AGG
```sql
SELECT FORMAT("%T", ARRAY_CONCAT_AGG(x)) AS array_concat_agg
FROM (
 SELECT [1, 2, 3] AS x
 UNION ALL SELECT [4, 5]
 UNION ALL SELECT [6]
)

```

## COUNTIF
```sql
SELECT Department, COUNTIF(Cost > 25)
FROM Expenses
GROUP BY Department
```

## STRING_AGG
```sql
SELECT STRING_AGG(fruit) AS string_agg
FROM UNNEST(["apple", NULL, "pear", "banana", "pear"]) AS fruit
```

## SUM
```sql
SELECT Department, SUM(IF(Cost > 150, Cost, 0))
```
## Bitwise AGGREGATION

```sql
SELECT BIT_AND(x) as bit_and
FROM UNNEST([0xF001, 0x00A1]) as x;

SELECT BIT_OR(x) as bit_or
FROM UNNEST([0xF001, 0x00A1]) as x;

SELECT BIT_XOR(x) AS bit_xor
FROM UNNEST([5678, 1234]) AS x;

SELECT LOGICAL_AND(x) AS logical_and
FROM UNNEST([true, false, true]) AS x;

SELECT LOGICAL_OR(x) AS logical_or
FROM UNNEST([true, false, true]) AS x;
```

## GIS FUNCTION
```sql
SELECT
  zip_code,
  zipcodes.area_land_meters zip_area,
  urban_area_code,
  name,
  cities.area_land_meters metro_area,
  (zipcodes.area_land_meters / cities.area_land_meters) ratio
FROM
  `bigquery-public-data.geo_us_boundaries.zip_codes` AS zipcodes
INNER JOIN
  `bigquery-public-data.utility_us.us_cities_area` cities
ON
  ST_INTERSECTS(zipcodes.zip_code_geom,
    cities.city_geom)
WHERE
  urban_area_code = "51445"
ORDER BY
  6 DESC
```
