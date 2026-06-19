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


bronze_bucket = "crypto-bronze"
silver_bucket = "crypto-silver"

today = datetime.now()

date_path = today.strftime("%Y/%m/%d")
file_date = today.strftime("%Y-%m-%d")

bronze_object = f"{date_path}/raw.json"

# =========================
# 2. DOWNLOAD FROM BRONZE
# =========================

local_input = "temp_raw.json"

client.fget_object(
    bronze_bucket,
    bronze_object,
    local_input
)

print("📥 Downloaded from Bronze:", bronze_object)

# =========================
# 3. LOAD DATA
# =========================

df = pd.read_json(local_input)

# =========================
# 4. TRANSFORMATION (SILVER)
# =========================

columns = [
    "id",
    "symbol",
    "name",
    "market_cap_rank",
    "current_price",
    "high_24h",
    "low_24h",
    "total_volume",
    "market_cap",
    "price_change_24h",
    "price_change_percentage_24h",
    "last_updated"
]

df = df[columns]

df = df.drop_duplicates()
df = df.dropna(subset=["id", "current_price"])

# =========================
# 5. SAVE LOCAL PARQUET
# =========================

silver_local_folder = "data/silver"
os.makedirs(silver_local_folder, exist_ok=True)

local_output = f"{silver_local_folder}/crypto_market_{file_date}.parquet"

df.to_parquet(local_output, index=False)

print("💾 Saved locally:", local_output)

# =========================
# 6. UPLOAD TO MINIO
# =========================

if not client.bucket_exists(silver_bucket):
    client.make_bucket(silver_bucket)

silver_object = f"{file_date}/crypto_market.parquet"

client.fput_object(
    silver_bucket,
    silver_object,
    local_output
)

print("🚀 Uploaded to Silver MinIO:", silver_object)

# =========================
# 7. CLEAN TEMP FILE
# =========================

if os.path.exists(local_input):
    os.remove(local_input)

print("🧹 Temp file removed")
print("🥈 Silver Layer Completed Successfully")