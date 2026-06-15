import snowflake.connector
import pandas as pd
import math
from datetime import datetime

# =========================
# CLEAN FUNCTION
# =========================
def clean_value(x):
    if pd.isna(x) or (isinstance(x, float) and math.isnan(x)):
        return None
    return float(x)

# =========================
# TODAY DATE
# =========================
today = datetime.now().strftime("%Y-%m-%d")

# =========================
# 1. CONNECTION
# =========================
conn = snowflake.connector.connect(
    user="MANAL",
    password="Bigdata2026@2004",
    account="stfsfeb-xv56862",
    warehouse="COMPUTE_WH",
    database="CRYPTO_DB",
    schema="PUBLIC"
)

cursor = conn.cursor()
print("✅ Connected to Snowflake")

# =========================
# 2. LOAD GOLD FILES
# =========================
dim_crypto = pd.read_parquet(
    f"data/gold/dim_crypto_{today}.parquet"
)

dim_date = pd.read_parquet(
    f"data/gold/dim_date_{today}.parquet"
)

dim_time = pd.read_parquet(
    f"data/gold/dim_time_{today}.parquet"
)

fact = pd.read_parquet(
    f"data/gold/fact_crypto_market_{today}.parquet"
)

print("📦 Gold data loaded")

# =========================
# 3. TYPE CLEANING
# =========================
dim_crypto = dim_crypto.astype({
    "crypto_id": int,
    "market_cap_rank": int
})

dim_date = dim_date.astype({
    "date_id": int,
    "year": int,
    "quarter": int,
    "month": int,
    "week": int,
    "day": int
})

dim_time = dim_time.astype({
    "time_id": int,
    "hour": int,
    "minute": int
})

# =========================
# 4. DIM_CRYPTO
# =========================
for _, row in dim_crypto.iterrows():
    cursor.execute("""
        INSERT INTO DIM_CRYPTO (
            crypto_id,
            coin_gecko_id,
            symbol,
            name,
            market_cap_rank
        )
        VALUES (%s,%s,%s,%s,%s)
    """, (
        int(row["crypto_id"]),
        row["id"],
        row["symbol"],
        row["name"],
        int(row["market_cap_rank"])
    ))

print("🟡 DIM_CRYPTO loaded")

# =========================
# 5. DIM_DATE
# =========================
for _, row in dim_date.iterrows():
    cursor.execute("""
        INSERT INTO DIM_DATE (
            date_id,
            full_date,
            year,
            quarter,
            month,
            week,
            day
        )
        VALUES (%s,%s,%s,%s,%s,%s,%s)
    """, (
        int(row["date_id"]),
        row["full_date"],
        int(row["year"]),
        int(row["quarter"]),
        int(row["month"]),
        int(row["week"]),
        int(row["day"])
    ))

print("🟡 DIM_DATE loaded")

# =========================
# 6. DIM_TIME
# =========================
for _, row in dim_time.iterrows():
    cursor.execute("""
        INSERT INTO DIM_TIME (
            time_id,
            hour,
            minute
        )
        VALUES (%s,%s,%s)
    """, (
        int(row["time_id"]),
        int(row["hour"]),
        int(row["minute"])
    ))

print("🟡 DIM_TIME loaded")

# =========================
# 7. FACT TABLE
# =========================
for _, row in fact.iterrows():
    cursor.execute("""
        INSERT INTO FACT_CRYPTO_MARKET (
            crypto_id,
            date_id,
            time_id,
            current_price,
            high_24h,
            low_24h,
            total_volume,
            market_cap,
            price_change_24h,
            price_change_percentage_24h
        )
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
    """, (
        int(row["crypto_id"]),
        int(row["date_id"]),
        int(row["time_id"]),
        clean_value(row["current_price"]),
        clean_value(row["high_24h"]),
        clean_value(row["low_24h"]),
        clean_value(row["total_volume"]),
        clean_value(row["market_cap"]),
        clean_value(row["price_change_24h"]),
        clean_value(row["price_change_percentage_24h"])
    ))

print("🔴 FACT loaded")

# =========================
# 8. COMMIT
# =========================
conn.commit()

# =========================
# 9. VALIDATION
# =========================
cursor.execute("SELECT COUNT(*) FROM DIM_CRYPTO")
print("DIM_CRYPTO:", cursor.fetchone())

cursor.execute("SELECT COUNT(*) FROM FACT_CRYPTO_MARKET")
print("FACT:", cursor.fetchone())

# =========================
# 10. CLOSE
# =========================
cursor.close()
conn.close()

print("🚀 Snowflake loading completed successfully")