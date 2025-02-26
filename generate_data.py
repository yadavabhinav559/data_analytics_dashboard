import pandas as pd
import numpy as np
import psycopg2
from sqlalchemy import create_engine

# Generate 1 year of sample business KPI data
np.random.seed(42)
data = {
    "date": pd.date_range(start="2023-01-01", periods=365, freq="D"),
    "revenue": np.random.randint(5000, 20000, 365),
    "expenses": np.random.randint(2000, 15000, 365),
    "profit": np.random.randint(1000, 10000, 365),
    "customer_count": np.random.randint(100, 1000, 365),
}

df = pd.DataFrame(data)

# PostgreSQL connection details
DB_URL = "postgresql://postgres:0@localhost/business_db"

# Save data to PostgreSQL
engine = create_engine(DB_URL)
df.to_sql("kpi_data", engine, if_exists="replace", index=False)

print("✅ Successfully inserted 1 year of data into PostgreSQL!")
