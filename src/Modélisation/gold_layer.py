import pandas as pd
import os
from datetime import datetime
from minio import Minio
from dotenv import load_dotenv
load_dotenv()
# =========================
# 1. CONFIG
# =========================

client = Minio(
    os.getenv("MINIO_ENDPOINT"),
    access_key=os.getenv("MINIO_ACCESS_KEY"),
    secret_key=os.getenv("MINIO_SECRET_KEY"),
    secure=os.getenv("MINIO_SECURE", "False").lower() == "true"
)



silver_bucket = "crypto-silver"
gold_bucket = "crypto-gold"

today = datetime.now()
file_date = today.strftime("%Y-%m-%d")

silver_object = f"{file_date}/crypto_market.parquet"

# =========================
# 2. LOAD SILVER FROM MINIO
# =========================

local_file = "silver_temp.parquet"

client.fget_object(
    silver_bucket,
    silver_object,
    local_file
)

df = pd.read_parquet(local_file)

# =========================
# 3. DATE + TIME EXTRACTION
# =========================

df["datetime"] = pd.to_datetime(df["last_updated"])

df["full_date"] = df["datetime"].dt.date
df["year"] = df["datetime"].dt.year
df["quarter"] = df["datetime"].dt.quarter
df["month"] = df["datetime"].dt.month
df["week"] = df["datetime"].dt.isocalendar().week.astype(int)
df["day"] = df["datetime"].dt.day

df["hour"] = df["datetime"].dt.hour
df["minute"] = df["datetime"].dt.minute

# =========================
# 4. DIM_CRYPTO
# =========================

dim_crypto = df[[
    "id",
    "symbol",
    "name",
    "market_cap_rank"
]].drop_duplicates()

dim_crypto = dim_crypto.reset_index(drop=True)
dim_crypto["crypto_id"] = dim_crypto.index + 1

# =========================
# 5. DIM_DATE
# =========================

dim_date = df[[
    "full_date",
    "year",
    "quarter",
    "month",
    "week",
    "day"
]].drop_duplicates()

dim_date = dim_date.reset_index(drop=True)
dim_date["date_id"] = dim_date.index + 1

# =========================
# 6. DIM_TIME
# =========================

dim_time = df[[
    "hour",
    "minute"
]].drop_duplicates()

dim_time = dim_time.reset_index(drop=True)
dim_time["time_id"] = dim_time.index + 1

# =========================
# 7. FACT TABLE
# =========================

fact = df.copy()

# 🔗 join DIM_CRYPTO
fact = fact.merge(
    dim_crypto,
    on=["id", "symbol", "name", "market_cap_rank"],
    how="left"
)

# 🔗 join DIM_DATE
fact = fact.merge(
    dim_date,
    on=["full_date", "year", "quarter", "month", "week", "day"],
    how="left"
)

# 🔗 join DIM_TIME
fact = fact.merge(
    dim_time,
    on=["hour", "minute"],
    how="left"
)

fact_crypto_market = fact[[
    "crypto_id",
    "date_id",
    "time_id",
    "current_price",
    "high_24h",
    "low_24h",
    "total_volume",
    "market_cap",
    "price_change_24h",
    "price_change_percentage_24h"
]]

# =========================
# 8. REFERENTIAL INTEGRITY CHECK
# =========================

assert fact_crypto_market["crypto_id"].isnull().sum() == 0
assert fact_crypto_market["date_id"].isnull().sum() == 0
assert fact_crypto_market["time_id"].isnull().sum() == 0

print("✅ Referential Integrity OK")

# =========================
# 9. SAVE GOLD (PARQUET FILES)
# =========================

gold_folder = "data/gold"
os.makedirs(gold_folder, exist_ok=True)

dim_crypto_file = f"{gold_folder}/dim_crypto_{file_date}.parquet"
dim_date_file = f"{gold_folder}/dim_date_{file_date}.parquet"
dim_time_file = f"{gold_folder}/dim_time_{file_date}.parquet"
fact_file = f"{gold_folder}/fact_crypto_market_{file_date}.parquet"

dim_crypto.to_parquet(dim_crypto_file, index=False)
dim_date.to_parquet(dim_date_file, index=False)
dim_time.to_parquet(dim_time_file, index=False)
fact_crypto_market.to_parquet(fact_file, index=False)

# =========================
# 10. UPLOAD TO MINIO
# =========================

if not client.bucket_exists(gold_bucket):
    client.make_bucket(gold_bucket)

client.fput_object(gold_bucket, f"{file_date}/dim_crypto.parquet", dim_crypto_file)
client.fput_object(gold_bucket, f"{file_date}/dim_date.parquet", dim_date_file)
client.fput_object(gold_bucket, f"{file_date}/dim_time.parquet", dim_time_file)
client.fput_object(gold_bucket, f"{file_date}/fact_crypto_market.parquet", fact_file)

# =========================
# 11. CLEAN TEMP FILE
# =========================

os.remove(local_file)

print("🥇 GOLD STAR SCHEMA COMPLETED (EXACT ERD IMPLEMENTED)")