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

CREATE TABLE IF NOT EXISTS calculated_humidity (
    collector_id        INTEGER       NOT NULL
  , calculation_date    TIMESTAMPTZ   NOT NULL
  , humidity_percentage NUMERIC(5,2)  NOT NULL
  , PRIMARY KEY (
        collector_id
      , calculation_date
    )
);

CREATE TABLE IF NOT EXISTS receptor_status (
    update_date       TIMESTAMPTZ NOT NULL PRIMARY KEY
  , records_in_buffer INTEGER     NOT NULL
);