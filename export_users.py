import os
import pandas as pd
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

uri = os.getenv("DATABASE_URL", "postgres://ubum9nbgnfakff:p90f3d00f08d827dc5d02b9a2974c9cf34c1bf97cf48d3446692979f84f659b58@c3v5n5ajfopshl.cluster-czrs8kj4isg7.us-east-1.rds.amazonaws.com:5432/d7p32cje4m2pt2")
if uri.startswith("postgres://"):
    uri = uri.replace("postgres://", "postgresql://", 1)

if not uri:
    uri = "sqlite:///instance/app.db"

app.config["SQLALCHEMY_DATABASE_URI"] = uri
db = SQLAlchemy(app)

EXPORT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "exports")
os.makedirs(EXPORT_DIR, exist_ok=True)


def export_table(table_name: str):
    """Export a specific table from the database (Postgres or SQLite) to Excel and CSV"""
    try:
        with app.app_context():  #
            query = f"SELECT * FROM {table_name}"
            df = pd.read_sql_query(query, db.engine)

            if df.empty:
                print(f"No data found in table '{table_name}'.")
                return

            excel_path = os.path.join(EXPORT_DIR, f"{table_name}_data.xlsx")
            csv_path = os.path.join(EXPORT_DIR, f"{table_name}_data.csv")

            df.to_excel(excel_path, index=False)
            df.to_csv(csv_path, index=False)

            print(f"Data exported successfully:\n- {excel_path}\n- {csv_path}")

    except Exception as e:
        print(f"Error exporting data: {e}")


if __name__ == "__main__":
    export_table("student")
