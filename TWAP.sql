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
    --SUBSTR(txn_tmsp_nanos, 1, 10) AS day, -- select
    cyc_dt AS day,
    --CAST(SUBSTR(txn_tmsp_nanos, 15, 2) AS INT64) AS minute,
    TIMESTAMP_TRUNC(txn_tmsp, MINUTE) AS minute,
    TIMESTAMP_TRUNC(txn_tmsp, HOUR) AS hour_1,
    TIMESTAMP_TRUNC(txn_tmsp, SECOND) AS second
    --CAST(SUBSTR(txn_tmsp_nanos, 18, 2) AS INT64) AS second
  FROM
    `prj-pr-curated-zone-ext-1595.marketdata.t_orderbook_globex_10_lvl_deep`
  WHERE
    cyc_dt IN UNNEST(run_dates)
    AND mrkt_dta_rpt_typ = "TRD"
    AND inst_sym IN UNNEST(run_symbols)
    -- AND hour = 23
    -- Add additional filters as desired
    ),
  weighted AS(
  SELECT
    *,
    CASE
      WHEN LEAD(intervals) OVER symbol_window = intervals THEN TIMESTAMP_DIFF(LEAD(txn_tmsp) OVER symbol_window, txn_tmsp, SECOND)
      ELSE TIMESTAMP_DIFF(LEAD(txn_tmsp) OVER symbol_window, txn_tmsp, SECOND)
  END
    AS weight
  FROM
    full_obr
  WINDOW
    symbol_window AS (
    PARTITION BY
      inst_sym
    ORDER BY
      txn_tmsp_nanos)
    -- Determining weight of each transaction for twap calculation
    )
SELECT
  inst_sym,
  CASE
    WHEN intervals = 'day' THEN CAST(day AS STRING)
    WHEN intervals = 'hour' THEN CAST(hour_1 AS STRING)
    WHEN intervals = 'minute' THEN CAST(minute AS STRING)
  END
  AS interval_value,
  ROUND(SUM(weight*CAST(last_trd_px_fmt AS FLOAT64))/SUM(weight), 2) AS twap
FROM
  weighted
GROUP BY
  inst_sym,
  interval_value
ORDER BY
  inst_sym,
  interval_value