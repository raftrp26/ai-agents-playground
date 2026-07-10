
--Storing the table
CREATE OR REPLACE VIEW hometask_data AS
SELECT *
-- Update the file path below if your local project structure differs from the one used in this solution
FROM read_csv_auto('notebooks/AUTODOC/data_set_da_test.csv');

-- As some sessions cross calendar days, all events in a session are assigned to the day when the session started

-- Defining date of the session

with session_start_time as (
    SELECT
    user
    ,session
    ,min(event_date) as session_start_datetime
    FROM hometask_data
    GROUP BY
    user
    ,session
)

-- More than 5% of users have more than one session per day, so sessions are ranked by user and start date to identify the first daily session

,rank_sessions_by_day_by_user as (
    SELECT
    *
    ,DATE_TRUNC('day', session_start_datetime) as session_start_date
    ,ROW_NUMBER() OVER (PARTITION BY user, DATE_TRUNC('day', session_start_datetime) ORDER BY session_start_datetime ASC) AS session_rank_by_day
    FROM session_start_time
    --LIMIT 300
)

-- Filtering first session of the day

,user_first_session_of_the_day as (
    SELECT DISTINCT
    user
    ,session
    ,session_start_date
    FROM rank_sessions_by_day_by_user
    WHERE session_rank_by_day = 1
)

-- Joining all events from the selected first sessions of the day

,events_first_session_of_the_day as (
    SELECT
    *
    ,CASE
        WHEN event_type = 'page_view' then 0
        ELSE 1
    END AS FLAG_NOT_VIEW
    FROM user_first_session_of_the_day
    LEFT JOIN (
        SELECT DISTINCT
        session
        ,user
        ,event_type
        FROM hometask_data
    ) USING (session, user)
)

-- Counting events per user that are not only pageview

,events_not_pageview as (
    SELECT
    session_start_date
    ,user
    ,sum(FLAG_NOT_VIEW) AS not_view_count
    FROM events_first_session_of_the_day
    GROUP by 
    session_start_date
    ,user
)

-- Counting users that only generated page view events in their first session of each day

SELECT
    session_start_date
    ,count(user) as number_clients_only_pageview
FROM events_not_pageview
WHERE not_view_count = 0
GROUP BY session_start_date
ORDER BY session_start_date;
