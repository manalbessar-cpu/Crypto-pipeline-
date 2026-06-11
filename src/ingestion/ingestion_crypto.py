import requests
import json
import os
from datetime import datetime
from minio import Minio

# =========================
# 1. CONFIG
# =========================

url = "https://api.coingecko.com/api/v3/coins/markets"

params = {
    "vs_currency": "usd",
    "order": "market_cap_desc",
    "per_page": 50,
    "page": 1,
    "sparkline": "false"
}

# MinIO config
client = Minio(
    "localhost:9000",
    access_key="minio",
    secret_key="minio123",
    secure=False
)

bucket = "crypto-bronze"

# =========================
# 2. CREATE BUCKET IF NOT EXISTS
# =========================

if not client.bucket_exists(bucket):
    client.make_bucket(bucket)

# =========================
# 3. API CALL (WITH SAFETY)
# =========================

try:
    response = requests.get(url, params=params, timeout=10)
    response.raise_for_status()
    data = response.json()

except Exception as e:
    print("❌ API Error:", e)
    exit()

# =========================
# 4. SAVE LOCAL BRONZE FILE
# =========================

now = datetime.now()

folder = f"data/bronze/{now.strftime('%Y/%m/%d')}"
os.makedirs(folder, exist_ok=True)

filename = f"{folder}/raw.json"

with open(filename, "w", encoding="utf-8") as f:
    json.dump(data, f, indent=4)

print("✅ Saved locally:", filename)

# =========================
# 5. UPLOAD TO MINIO
# =========================

object_name = f"{now.strftime('%Y/%m/%d')}/raw.json"

client.fput_object(
    bucket,
    object_name,
    filename
)

print("🚀 Uploaded to MinIO:", f"{bucket}/{object_name}")

# =========================
# DONE
# =========================

print("🥉 Bronze ingestion completed successfully")