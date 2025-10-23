import os
import sqlite3
import pandas as pd

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "app.db")
EXPORT_DIR = os.path.join(BASE_DIR, "exports")
os.makedirs(EXPORT_DIR, exist_ok=True)

def export_table(table_name: str):
    """Export a specific table from SQLite to Excel and CSV"""
    if not os.path.exists(DB_PATH):
        print("Database file not found.")
        return

    try:
        conn = sqlite3.connect(DB_PATH)
        query = f"SELECT * FROM {table_name}"
        df = pd.read_sql_query(query, conn)
        conn.close()

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
