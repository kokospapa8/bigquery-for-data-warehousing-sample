# Chapter 19 SQL Sample Code
## K-Means Clustering
### Creating the Model
```sql
CREATE OR REPLACE MODEL `<project_id>.<dataset>.metkmeans`
OPTIONS(model_type="kmeans", num_clusters=5) AS
SELECT
department,
object_begin_date,
object_end_date,
classification,
artist_alpha_sort
FROM `bigquery-public-data.the_met.objects`
WHERE object_begin_date < 2025 and object_end_date < 2025
```
### Prediction
```sql
SELECT
  *
FROM
  ML.PREDICT( MODEL `<project_id>.<dataset>.metkmeans`,
    (
    SELECT
      "Painting" department,
      1641 object_begin_date,
      1641 object_end_date,
      "Prints" classification,
      "Rembrandt van Rijn" artist_alpha_sort,
      ) )

```

## Data classification
### Create Transformed View for Training
```sql
CREATE OR REPLACE VIEW
  `<project_id>.<dataset>.qml_nhtsa_2015_view` AS
SELECT
  a.consecutive_number,
  a.county,
  a.type_of_intersection,
  a.light_condition,
  a.atmospheric_conditions_1,
  a.hour_of_crash,
  a.functional_system,
  a.related_factors_crash_level_1 related_factors,
  CASE
    WHEN a.hour_of_ems_arrival_at_hospital BETWEEN 0 AND 23 AND a.hour_of_ems_arrival_at_hospital - a.hour_of_crash > 0 THEN a.hour_of_ems_arrival_at_hospital - a.hour_of_crash
  ELSE
  NULL
END
  delay_to_hospital,
  CASE
    WHEN a.hour_of_arrival_at_scene BETWEEN 0 AND 23 AND a.hour_of_arrival_at_scene - a.hour_of_crash > 0 THEN a.hour_of_arrival_at_scene - a.hour_of_crash
  ELSE
  NULL
END
  delay_to_scene,
  p.age,
  p.person_type,
  p.seating_position,
  CASE p.restraint_system_helmet_use
    WHEN 0 THEN 0
    WHEN 1 THEN 0.33
    WHEN 2 THEN 0.67
    WHEN 3 THEN 1.0
  ELSE
  0.5
END
  restraint,
  CASE
    WHEN p.injury_severity IN (4) THEN 1
  ELSE
  0
END
  survived,
  CASE
    WHEN p.rollover IN ("", "NO Rollover") THEN 0
  ELSE
  1
END
  rollover,
  CASE
    WHEN p.air_bag_deployed BETWEEN 1 AND 9 THEN 1
  ELSE
  0
END
  airbag,
  CASE
    WHEN p.police_reported_alcohol_involvement LIKE ("%Yes%") THEN 1
  ELSE
  0
END
  alcohol,
  CASE
    WHEN p.police_reported_drug_involvement LIKE ("%Yes%") THEN 1
  ELSE
  0
END
  drugs,
  p.related_factors_person_level1,
  v.travel_speed,
  CASE
    WHEN v.speeding_related LIKE ("%Yes%") THEN 1
  ELSE
  0
END
  speeding_related,
  v.extent_of_damage,
  v.body_type body_type,
  v.vehicle_removal,
  CASE
    WHEN v.manner_of_collision > 11 THEN 11
  ELSE
  v.manner_of_collision
END
  manner_of_collision,
  CASE
    WHEN v.roadway_surface_condition > 11 THEN 8
  ELSE
  v.roadway_surface_condition
END
  roadway_surface_condition,
  CASE
    WHEN v.first_harmful_event < 90 THEN v.first_harmful_event
  ELSE
  0
END
  first_harmful_event,
  CASE
    WHEN v.most_harmful_event < 90 THEN v.most_harmful_event
  ELSE
  0
END
  most_harmful_event,
FROM
  `bigquery-public-data.nhtsa_traffic_fatalities.accident_2015` a
LEFT OUTER JOIN
  `bigquery-public-data.nhtsa_traffic_fatalities.vehicle_2015` v
USING
  (consecutive_number)
LEFT OUTER JOIN
  `bigquery-public-data.nhtsa_traffic_fatalities.person_2015` p
USING
  (consecutive_number)
```

### Create Model
```sql
CREATE OR REPLACE MODEL
  `<project_id>.<dataset>.bqml_nhtsa_2015` TRANSFORM ( county,
    type_of_intersection,
    light_condition,
    atmospheric_conditions_1,
    ML.QUANTILE_BUCKETIZE(hour_of_crash,
      6) OVER() bucketized_hour,
    ML.BUCKETIZE(functional_system,
      [1, 4, 7]) functional_system,
    related_factors,
    ML.STANDARD_SCALER(delay_to_hospital) OVER() delay_to_hospital,
    ML.STANDARD_SCALER(delay_to_scene) OVER() delay_to_scene,
    ML.QUANTILE_BUCKETIZE(age,
      5) OVER() bucketized_age,
    ML.BUCKETIZE(person_type,
      [1, 6, 9]) person_type,
    ML.BUCKETIZE(seating_position,
      [0, 10, 11, 21, 31, 40]) seating_position,
    restraint,
    rollover,
    airbag,
    alcohol,
    drugs,
    related_factors_person_level1,
    ML.QUANTILE_BUCKETIZE(travel_speed,
      10) OVER() travel_speed,
    speeding_related,
    ML.BUCKETIZE(body_type,
      [0, 10, 20, 30, 40, 50, 60, 80, 90, 91, 92, 93, 94, 95, 96, 97] ) body_type,
    vehicle_removal,
    manner_of_collision,
    roadway_surface_condition,
    first_harmful_event,
    most_harmful_event,
    survived ) OPTIONS (model_type="logistic_reg",
    input_label_cols=["survived"]) AS
SELECT
  * EXCEPT (consecutive_number)
FROM
  `bqml_nhtsa_2015_view`

```
### Create View for 2016 data
```sql
CREATE OR REPLACE VIEW `<project_id>.<dataset>.bqml_nhtsa_2016_view`
...(중략)...
FROM `bigquery-public-data.nhtsa_traffic_fatalities.accident_2016` a
LEFT OUTER JOIN `bigquery-public-data.nhtsa_traffic_fatalities.vehicle_2016` v
USING (consecutive_number)
LEFT OUTER JOIN `bigquery-public-data.nhtsa_traffic_fatalities.person_2016` p
USING (consecutive_number)

```
### Prediction against 2016 data
```sql
SELECT confusion, COUNT(confusion), COUNT(confusion)/ANY_VALUE(total)
FROM
(
SELECT CASE
  WHEN survived = 1 and predicted_survived = 0 THEN 1
  WHEN survived = 1 and predicted_survived = 1 THEN 2
  WHEN survived = 0 and predicted_survived = 1 THEN 3
  WHEN survived = 0 and predicted_survived = 0 THEN 4
  END confusion,
  CASE WHEN survived = 1 THEN 58613 -- total survivors
  WHEN survived = 0 THEN 105087 -- total fatalities
  END total
FROM
  ML.PREDICT(MODEL `<project_id>.<dataset>.bqml_nhtsa_2015`,
  (SELECT * FROM `<project_id>.<dataset>.'bqml_nhtsa_2016_view`),
  STRUCT(0.2805 AS threshold))
  )
GROUP BY confusion;
```
