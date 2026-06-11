import pandas as pd



fact = pd.read_parquet("data/gold/fact_crypto_market_2026-06-10.parquet")
dim_crypto = pd.read_parquet("data/gold/dim_crypto_2026-06-10.parquet")
dim_date = pd.read_parquet("data/gold/dim_date_2026-06-10.parquet")
dim_time = pd.read_parquet("data/gold/dim_time_2026-06-10.parquet")

print("FACT:", fact.shape)
print(fact.head())

print("DIM_CRYPTO:", dim_crypto.shape)
print(dim_crypto.head())

print("DIM_DATE:", dim_date.shape)
print(dim_date.head())

print("DIM_TIME:", dim_time.shape)
print(dim_time.head())