CREATE TABLE DIM_CRYPTO (
    crypto_id INT PRIMARY KEY,
    coin_gecko_id STRING,
    symbol STRING,
    name STRING,
    market_cap_rank INT
);

CREATE TABLE DIM_DATE (
    date_id INT PRIMARY KEY,
    full_date DATE,
    year INT,
    quarter INT,
    month INT,
    week INT,
    day INT
);

CREATE TABLE DIM_TIME (
    time_id INT PRIMARY KEY,
    hour INT,
    minute INT
);

CREATE TABLE FACT_CRYPTO_MARKET (
    fact_id INT AUTOINCREMENT,
    crypto_id INT,
    date_id INT,
    time_id INT,
    current_price FLOAT,
    high_24h FLOAT,
    low_24h FLOAT,
    total_volume FLOAT,
    market_cap FLOAT,
    price_change_24h FLOAT,
    price_change_percentage_24h FLOAT
);