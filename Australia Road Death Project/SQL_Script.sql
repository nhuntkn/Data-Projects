CREATE OR REPLACE TABLE `project-de05ea45-0c4e-455c-806.aus_road_deaths_data_engineering.vw_fatality_counts_by_dimensions` AS (
SELECT 
    -- Dimensions from Date
    d.time_of_day,
    d.holiday_flag,
    d.weekend_flag,
    d.month,
    d.year,

    -- Dimensions from Location
    l.state,
    l.national_road_type,
    l.national_remoteness_areas_2021,

    -- Dimensions from Person
    p.road_user,
    p.gender,
    p.age_group,

    -- Dimensions from Scenario
    s.crash_type,
    s.speed_limit,
    s.bus_involvement,
    s.heavy_rigid_truck_involvement,
    s.articulated_truck_involvement,

    -- The Metric (The actual count)
    f.age,
    COUNT(f.crash_id) AS fatality_count

FROM `project-de05ea45-0c4e-455c-806.aus_road_deaths_data_engineering.fact_fatalities` f
LEFT JOIN `project-de05ea45-0c4e-455c-806.aus_road_deaths_data_engineering.dim_date` d 
    ON f.date_id = d.date_id
LEFT JOIN `project-de05ea45-0c4e-455c-806.aus_road_deaths_data_engineering.dim_location` l 
    ON f.location_id = l.location_id
LEFT JOIN `project-de05ea45-0c4e-455c-806.aus_road_deaths_data_engineering.dim_person` p 
    ON f.person_id = p.person_id
LEFT JOIN `project-de05ea45-0c4e-455c-806.aus_road_deaths_data_engineering.dim_scenario` s 
    ON f.scenario_id = s.scenario_id

-- Grouping by every dimension column listed above (Columns 1 through 15)
GROUP BY 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16

);

-- ANALYSES QUESTIONS
-- Find the top 10 sa4_name_2021 based on the number of fatalities.

SELECT 
    l.sa4_name_2021,
    COUNT(f.crash_id) AS fatality_count
FROM `project-de05ea45-0c4e-455c-806.aus_road_deaths_data_engineering.fact_fatalities` f
JOIN `project-de05ea45-0c4e-455c-806.aus_road_deaths_data_engineering.dim_location` l ON f.location_id = l.location_id
GROUP BY 1
ORDER BY fatality_count DESC
LIMIT 10;

-- Find the time of day when pedestrians or pedal cyclists are most likely to be in danger.

SELECT 
  p.road_user,
  d.time_of_day,
  COUNT(f.crash_id) AS fatality_count
FROM `project-de05ea45-0c4e-455c-806.aus_road_deaths_data_engineering.fact_fatalities` f
JOIN `project-de05ea45-0c4e-455c-806.aus_road_deaths_data_engineering.dim_person` p ON p.person_id = f.person_id
JOIN `project-de05ea45-0c4e-455c-806.aus_road_deaths_data_engineering.dim_date` d ON d.date_id = f.date_id
WHERE p.road_user = 'Pedestrian'
OR p.road_user = 'Pedal cyclist'
GROUP BY 1, 2
ORDER BY fatality_count DESC;

-- Find national remoteness areas that have high fatality numbers.

SELECT 
  l.national_remoteness_areas_2021,
  COUNT(f.crash_id) AS fatality_count
FROM `project-de05ea45-0c4e-455c-806.aus_road_deaths_data_engineering.fact_fatalities` f
JOIN `project-de05ea45-0c4e-455c-806.aus_road_deaths_data_engineering.dim_location` l ON l.location_id = f.location_id
JOIN `project-de05ea45-0c4e-455c-806.aus_road_deaths_data_engineering.dim_scenario` s ON s.scenario_id = f.scenario_id
JOIN `project-de05ea45-0c4e-455c-806.aus_road_deaths_data_engineering.dim_person` p ON p.person_id = f.person_id
WHERE s.speed_limit >= 100
GROUP BY 1
ORDER BY fatality_count DESC, 1;