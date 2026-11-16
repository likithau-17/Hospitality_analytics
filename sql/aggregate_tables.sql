
USE hospitality_analytics;

DROP TABLE IF EXISTS hospitality_analytics.agg_monthly_hotel_performance;


CREATE TABLE hospitality_analytics.agg_monthly_hotel_performance AS
SELECT
    h.hotel_id,
    h.hotel_name,
    h.location,
    d.year,
    d.month,
    d.month_name,

    SUM(f.is_available) AS available_room_nights,

    SUM(f.is_occupied) AS occupied_room_nights,

    SUM(f.room_revenue) AS total_room_revenue,

    ROUND(
        SUM(f.is_occupied) * 100.0 /
        NULLIF(SUM(f.is_available), 0), 2
    ) AS occupancy_rate,

    ROUND(
        SUM(f.room_revenue) /
        NULLIF(SUM(f.is_occupied), 0), 2
    ) AS ADR,

    ROUND(
        SUM(f.room_revenue) /
        NULLIF(SUM(f.is_available), 0), 2
    ) AS RevPAR

FROM hospitality_analytics.fact_room_night f

JOIN hospitality_analytics.dim_hotel h
    ON f.hotel_id = h.hotel_id

JOIN hospitality_analytics.dim_date d
    ON f.date_id = d.date_id

GROUP BY
    h.hotel_id,
    h.hotel_name,
    h.location,
    d.year,
    d.month,
    d.month_name;

DROP TABLE IF EXISTS hospitality_analytics.agg_monthly_guest_satisfaction;

CREATE TABLE hospitality_analytics.agg_monthly_guest_satisfaction AS
SELECT
    h.hotel_id,
    h.hotel_name,
    h.location,
    d.year,
    d.month,
    d.month_name,
    COUNT(f.feedback_id) AS total_feedback,
    ROUND(AVG(f.satisfaction_rating), 2) AS avg_satisfaction_score
FROM hospitality_analytics.fact_guest_feedback f
JOIN hospitality_analytics.dim_hotel h
    ON f.hotel_id = h.hotel_id
JOIN hospitality_analytics.dim_date d
    ON f.date_id = d.date_id
GROUP BY
    h.hotel_id,
    h.hotel_name,
    h.location,
    d.year,
    d.month,
    d.month_name;


DROP TABLE IF EXISTS hospitality_analytics.agg_annual_employee_turnover;

CREATE TABLE hospitality_analytics.agg_annual_employee_turnover AS

WITH monthly_movements AS (
    SELECT
        h.hotel_id,
        d.year,
        d.month,
        SUM(CASE WHEN f.movement_type = 'JOIN' THEN 1 ELSE 0 END) AS joins_count,
        SUM(CASE WHEN f.movement_type = 'EXIT' THEN 1 ELSE 0 END) AS exits_count
    FROM hospitality_analytics.fact_employee_movement f
    JOIN hospitality_analytics.dim_hotel h
        ON f.hotel_id = h.hotel_id
    JOIN hospitality_analytics.dim_date d
        ON f.date_id = d.date_id
    GROUP BY h.hotel_id, d.year, d.month
),

hotel_months AS (
    SELECT
        h.hotel_id,
        d.year,
        d.month
    FROM hospitality_analytics.dim_hotel h
    CROSS JOIN (
        SELECT DISTINCT year, month
        FROM hospitality_analytics.dim_date
    ) d
),

monthly_headcount AS (
    SELECT
        hm.hotel_id,
        hm.year,
        hm.month,
        COALESCE(mm.joins_count, 0) AS joins_count,
        COALESCE(mm.exits_count, 0) AS exits_count,
        SUM(
            COALESCE(mm.joins_count, 0) -
            COALESCE(mm.exits_count, 0)
        ) OVER (
            PARTITION BY hm.hotel_id
            ORDER BY hm.year, hm.month
        ) AS closing_headcount
    FROM hotel_months hm
    LEFT JOIN monthly_movements mm
        ON hm.hotel_id = mm.hotel_id
        AND hm.year = mm.year
        AND hm.month = mm.month
)

SELECT
    h.hotel_id,
    h.hotel_name,
    h.location,
    mh.year,
    SUM(mh.exits_count) AS total_employee_exits,
    ROUND(AVG(mh.closing_headcount), 2) AS avg_monthly_employee_count,
    ROUND(
        SUM(mh.exits_count) * 100.0 /
        NULLIF(AVG(mh.closing_headcount), 0),
        2
    ) AS employee_turnover_rate
FROM monthly_headcount mh
JOIN hospitality_analytics.dim_hotel h
    ON mh.hotel_id = h.hotel_id
GROUP BY
    h.hotel_id,
    h.hotel_name,
    h.location,
    mh.year;

DROP TABLE IF EXISTS hospitality_analytics.agg_annual_hotel_kpi;

CREATE TABLE hospitality_analytics.agg_annual_hotel_kpi AS

WITH performance AS (
    SELECT
        hotel_id,
        hotel_name,
        location,
        year,
        SUM(available_room_nights) AS available_room_nights,
        SUM(occupied_room_nights) AS occupied_room_nights,
        SUM(total_room_revenue) AS total_room_revenue,
        ROUND(
            SUM(occupied_room_nights) * 100.0 /
            NULLIF(SUM(available_room_nights), 0), 2
        ) AS occupancy_rate,
        ROUND(
            SUM(total_room_revenue) /
            NULLIF(SUM(occupied_room_nights), 0), 2
        ) AS ADR,
        ROUND(
            SUM(total_room_revenue) /
            NULLIF(SUM(available_room_nights), 0), 2
        ) AS RevPAR
    FROM hospitality_analytics.agg_monthly_hotel_performance
    GROUP BY hotel_id, hotel_name, location, year
),

satisfaction AS (
    SELECT
        hotel_id,
        year,
        SUM(total_feedback) AS total_feedback,
        ROUND(
            SUM(avg_satisfaction_score * total_feedback) /
            NULLIF(SUM(total_feedback), 0), 2
        ) AS avg_satisfaction_score
    FROM hospitality_analytics.agg_monthly_guest_satisfaction
    GROUP BY hotel_id, year
)

SELECT
    p.hotel_id,
    p.hotel_name,
    p.location,
    p.year,
    p.occupancy_rate,
    p.ADR,
    p.RevPAR,
    s.total_feedback,
    s.avg_satisfaction_score,
    t.total_employee_exits,
    t.avg_monthly_employee_count,
    t.employee_turnover_rate
FROM performance p
LEFT JOIN satisfaction s
    ON p.hotel_id = s.hotel_id
    AND p.year = s.year
LEFT JOIN hospitality_analytics.agg_annual_employee_turnover t
    ON p.hotel_id = t.hotel_id
    AND p.year = t.year;