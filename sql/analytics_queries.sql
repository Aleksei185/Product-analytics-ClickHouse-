-- Создание базы и таблицы

CREATE DATABASE IF NOT EXISTS analytics;

CREATE TABLE IF NOT EXISTS analytics.events (
    event_time DateTime,
    user_id UInt32,
    event_type String,
    page String,
    country String
) ENGINE = MergeTree()
ORDER BY (event_time, user_id);

-- DAU

SELECT
    toDate(event_time) AS day,
    uniq(user_id) AS dau
FROM analytics.events
GROUP BY day
ORDER BY day;

-- Воронка продаж

SELECT
    level,
    count() AS users
FROM (
    SELECT
        user_id,
        windowFunnel(86400)(
            event_time,
            event_type = 'page_view',
            event_type = 'add_to_cart',
            event_type = 'checkout',
            event_type = 'purchase'
        ) AS level
    FROM analytics.events
    GROUP BY user_id
)
GROUP BY level
ORDER BY level;

-- Retention

SELECT
    first_day,
    day_number,
    uniq(user_id) AS users
FROM (
    SELECT
        user_id,
        min(toDate(event_time)) AS first_day,
        toDate(event_time) AS current_day,
        dateDiff('day', min(toDate(event_time)) OVER (PARTITION BY user_id), toDate(event_time)) AS day_number
    FROM analytics.events
    GROUP BY user_id, current_day
)
WHERE day_number <= 7
GROUP BY first_day, day_number
ORDER BY first_day, day_number;
