# Chapter 13 SQL Sample Code
## ROW_NUMBER
```sql
SELECT
ShoeType, Color,
ROW_NUMBER() OVER (PARTITION BY ShoeType ORDER BY Price DESC)
FROM Products
```

## Navigation Functions
```sql

SELECT A.ID, A.Name, B.Name NameTwoEarlier
FROM A
JOIN A AS B
ON (A.ID - 2) = B.ID

SELECT ID, Name, LAG(Name) NameTwoEarlier
FROM A
OVER (ORDER BY ID ROW 2 PRECEDING)
```

## Aggregate Analytic Functions
```sql
WITH
  numbers AS (
  SELECT
    *
  FROM
    UNNEST(GENERATE_ARRAY(1, 100)) AS num)
SELECT
  num,
  AVG(num) OVER (ROWS BETWEEN 2 PRECEDING AND CURRENT ROW) MovingAverage,
  SUM(num) OVER (ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) RunningTotal
FROM
  numbers
```

## IF/THEN/ELSEIF/ELSE/END IF
```sql
-- 필요한 변수를 선언한다
DECLARE DIE1, DIE2, TOTAL INT64;

-- 결과를 넣을 문자열을 선언한다
DECLARE RESULT STRING;

-- 두 개의 난수를 생성하고 변수를 설정한다. 둘의 합을 구한다
SET (DIE1, DIE2) = (CAST(FLOOR(RAND() * 6) + 1 AS INT64), CAST(FLOOR(RAND() * 6) + 1 AS INT64));
SET TOTAL = DIE1 + DIE2;

-- if 블록으로 특별한 결과를 확인하고 결과를 설정한다
IF (DIE1 = 1 AND DIE2 = 1) THEN SET RESULT = "Snake eyes.";
ELSEIF (DIE1 = 6 AND DIE2 = 6) THEN SET RESULT = "Boxcars.";
ELSEIF (DIE1 = 4 AND DIE2 = 4) THEN SET RESULT = "Hard eight.";
ELSE SET RESULT = "Nothing special.";
END IF;

-- 결과를 사용자에게 반환한다
SELECT FORMAT("You rolled %d and %d for a total of %d. %s", DIE1, DIE2, TOTAL, RESULT);
```

## LOOP/END LOOP
```sql
DECLARE I INT64 DEFAULT 0;
DECLARE R ARRAY<INT64> DEFAULT [];
LOOP
  SET I = I + 1;
  SET R = ARRAY_CONCAT(R, [I]);
  IF I > 9 THEN LEAVE;
END IF;
END LOOP;
SELECT * FROM UNNEST(R);

SELECT * FROM UNNEST(GENERATE_ARRAY(1,10))
```

## WHILE/DO/END WHILE
```sql
DECLARE I INT64 DEFAULT 0;
DECLARE R ARRAY<INT64> DEFAULT [];
WHILE I < 10 DO
  SET I = I + 1;
  SET R = ARRAY_CONCAT(R, [I]);
END WHILE;
SELECT * FROM UNNEST(R);
```

## Exception Handling
```sql
BEGIN
SELECT 1/0; -- 0 으로 나누기 오류
EXCEPTION WHEN ERROR THEN
SELECT "What are you even doing there.";
END
```

## Stored Procedures
```sql
CREATE OR REPLACE PROCEDURE wbq.GetRandomNumber(IN Maximum INT64, OUT Answer INT64)
BEGIN
 SET Answer = CAST((SELECT FLOOR((RAND() * Maximum) + 1)) AS INT64);
END;
DECLARE Answer INT64 DEFAULT 0;
CALL wbq.GetRandomNumber(10, Answer);
SELECT Answer;
```
## User-Defined Function
```sql
CREATE OR REPLACE FUNCTION dataset.AddFive(input INT64) AS (input+5);
SELECT dataset.AddFive(10);
CREATE OR REPLACE FUNCTION wbq.AddFive(input ANY TYPE) AS (input+5);
```
## User-Defined Aggregate functions
```sql
CREATE OR REPLACE FUNCTION fake_avg(input ANY TYPE)
AS ((SELECT AVG(x) FROM UNNEST(input) x));

SELECT fake_avg(ARRAY_AGG(x)) FROM input;
```

## JavaScript User-Defined Functions
```sql
CREATE OR REPLACE FUNCTION wbq.AddFiveJS(x FLOAT64)
RETURNS FLOAT64
LANGUAGE js AS """
 return x+5;
""";

CREATE TEMP FUNCTION
  externalLibraryJSFunction(x STRING)
  RETURNS STRING
  LANGUAGE js OPTIONS (library=["gs://{some.js}",
    ...]) AS """
    return externalFunction(x);
  """;
```

## Materizlized Views
```sql
CREATE MATERIALIZED VIEW `{project.dataset.mview}`
  AS SELECT ... FROM `{project.dataset.table}` ... GROUP BY ...

```
