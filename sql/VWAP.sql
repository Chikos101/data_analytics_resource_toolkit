DECLARE intervals STRING;
DECLARE run_dates ARRAY <DATE>;
DECLARE run_symbols ARRAY <STRING>;

--Parameters:
-----------------------------------------------------------------
SET intervals = "minute"; -- Desired granularity (acceted values ['day', 'hour', 'minute'])
SET run_dates = [DATE("2024-08-11"), DATE("2024-08-12"), DATE("2024-08-13")]; -- Desired dates of interest
SET run_symbols = ["ESU4"]; -- Desired symbols
-----------------------------------------------------------------
WITH full_obr AS(
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
)
SELECT
  globex_sym,
  CASE
    WHEN intervals = 'day' THEN CAST(day AS STRING)
    WHEN intervals = 'hour' THEN CAST(hour AS STRING)
    WHEN intervals = 'minute' THEN CAST(minute AS STRING)
  END AS interval_value,
  ROUND(SUM(CAST(last_trade_px AS FLOAT64)*last_trd_qty)/SUM(last_trd_qty), 2) AS vwap 
FROM
  full_obr
GROUP BY globex_sym, interval_value
ORDER BY globex_sym, interval_value
