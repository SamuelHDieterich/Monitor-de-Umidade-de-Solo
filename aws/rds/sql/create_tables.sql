DROP TABLE IF EXISTS
    collector_status
  , collector_record
  , calculated_humidity
  , receptor_status
;


CREATE TABLE IF NOT EXISTS collector_status (
    collector_id  INTEGER       NOT NULL
  , start_date    TIMESTAMPTZ   NOT NULL
  , end_date      TIMESTAMPTZ   NULL
  , crop          VARCHAR(255)  NOT NULL
  , PRIMARY KEY (
        collector_id
      , start_date
    )
);

CREATE TABLE IF NOT EXISTS collector_record (
    collector_id    INTEGER     NOT NULL
  , collection_date TIMESTAMPTZ NOT NULL
  , read_humidity   INTEGER     NOT NULL
  , PRIMARY KEY (
        collector_id
      , collection_date
    )
);

CREATE OR REPLACE VIEW calculated_humidity AS
SELECT
    collector_id
  , collection_date AS calculation_date
  -- Dry (0%) - 65535
  -- Wet (100%) - 23429
  -- a + (x-min(x))(b-a)/(max(x)-min(x))
  , CAST(LEAST(100 * (65535 - CAST(read_humidity AS FLOAT)) / 42106, 100.0) AS NUMERIC(5,2)) AS humidity_percentage 
FROM collector_record
;

CREATE TABLE IF NOT EXISTS receptor_status (
    update_date       TIMESTAMPTZ NOT NULL PRIMARY KEY
  , records_in_buffer INTEGER     NOT NULL
);