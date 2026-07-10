CREATE OR REPLACE VIEW hometask_data AS
SELECT *
-- Review and update the CSV file path if needed before running the script.
FROM read_csv_auto('notebooks/AUTODOC/data_set_da_test.csv');


WITH cart_events AS (
    SELECT
        session,
        product,
        COUNT(*) AS add_to_cart_count
    FROM hometask_data
    WHERE event_type = 'add_to_cart'
      AND product IS NOT NULL
      AND product <> 0
    GROUP BY
        session,
        product
)

SELECT
    session,
    product,
    add_to_cart_count
FROM cart_events
WHERE add_to_cart_count >= 4
ORDER BY add_to_cart_count DESC;