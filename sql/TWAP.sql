DECLARE
  intervals STRING;
DECLARE
  run_dates ARRAY <DATE>;
DECLARE
  run_symbols ARRAY <STRING>;
  --Parameters:
  -----------------------------------------------------------------
SET
  intervals = "hour"; -- Desired granularity (accepted values ['day', 'hour', 'minute'])
SET
  run_dates = [DATE("2024-08-12"), DATE("2024-08-13")]; -- Desired dates of interest
SET
  run_symbols = ["ESU4"]; -- Desired symbols
  -----------------------------------------------------------------
WITH
  full_obr AS(
  SELECT
    *,
    cycle_date AS day,
    TIMESTAMP_TRUNC(transaction_ts, MINUTE) AS minute,
    TIMESTAMP_TRUNC(transaction_ts, HOUR) AS hour,
    TIMESTAMP_TRUNC(transaction_ts, SECOND) AS second
  FROM
    `customersProject.prod_cme_globex_10_level_order_book.v_orderbook_10_lvl_futuresandoptions`
  WHERE
    cycle_date IN UNNEST(run_dates)
    AND rpt_type = "TRD"
    AND globex_sym IN UNNEST(run_symbols)
    -- Add additional filters as desired
    ),
  weighted AS(
  SELECT
    *,
    CASE
      WHEN LEAD(intervals) OVER symbol_window = intervals THEN TIMESTAMP_DIFF(LEAD(transaction_ts) OVER symbol_window, transaction_ts, SECOND)
      ELSE TIMESTAMP_DIFF(LEAD(transaction_ts) OVER symbol_window, transaction_ts, SECOND)
  END
    AS weight
  FROM
    full_obr
  WINDOW
    symbol_window AS (
    PARTITION BY
      globex_sym
    ORDER BY
      transaction_ts)
    -- Determining weight of each transaction for twap calculation
    )
SELECT
  globex_sym,
  CASE
    WHEN intervals = 'day' THEN CAST(day AS STRING)
    WHEN intervals = 'hour' THEN CAST(hour AS STRING)
    WHEN intervals = 'minute' THEN CAST(minute AS STRING)
  END
  AS interval_value,
  ROUND(SUM(weight*CAST(last_trade_px AS FLOAT64))/SUM(weight), 2) AS twap
FROM
  weighted
GROUP BY
  globex_sym,
  interval_value
ORDER BY
  globex_sym,
  interval_value