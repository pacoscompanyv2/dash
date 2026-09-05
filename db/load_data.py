import os
import pandas as pd
from sqlalchemy import create_engine, text

DB_HOST = os.getenv("DB_HOST", "db")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME", "salesdb")
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASSWORD = os.getenv("DB_PASSWORD", "postgres")

CSV_PATH = os.getenv("CSV_PATH", "data/SalesRecords.csv")
SCHEMA_PATH = os.path.join(os.path.dirname(__file__), "schema.sql")

engine = create_engine(f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}")


def table_has_data(conn):
    result = conn.execute(text("SELECT to_regclass('public.sales')"))
    exists = result.scalar()
    if not exists:
        return False
    count = conn.execute(text("SELECT COUNT(*) FROM sales")).scalar()
    return count > 0


def load():
    with engine.begin() as conn:
        if table_has_data(conn):
            print("La tabla sales ya tiene datos, no se vuelve a cargar.")
            return

        with open(SCHEMA_PATH) as f:
            conn.execute(text(f.read()))

    df = pd.read_csv(CSV_PATH)
    df.columns = [
        "region", "country", "item_type", "sales_channel", "order_priority",
        "order_date", "order_id", "ship_date", "units_sold", "unit_price",
        "unit_cost", "total_revenue", "total_cost", "total_profit",
    ]
    df["order_date"] = pd.to_datetime(df["order_date"])
    df["ship_date"] = pd.to_datetime(df["ship_date"])

    df.to_sql("sales", engine, if_exists="append", index=False)
    print(f"Cargadas {len(df)} filas en la tabla sales.")


if __name__ == "__main__":
    load()
