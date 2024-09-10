import sqlite3
import pandas as pd
import os

db_file = 'gotuljosaskra.db'
csv_dir = 'csv'

# Connect to the SQLite database
conn = sqlite3.connect(db_file)
cursor = conn.cursor()

# Function to purge existing tables
def purge_tables():
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    print("Purging existing tables...")
    for table in tables:
        print(f"Dropped table {table[0]}")
        cursor.execute(f'DROP TABLE IF EXISTS "{table[0]}"')  # Quoting table names
    conn.commit()

# Function to clean up column names (remove brackets)
def clean_column_names(df):
    df.columns = [col.replace('[', '').replace(']', '').replace(' ', '_') for col in df.columns]
    return df

# Function to import CSV files
def import_csv_files():
    csv_files = [f for f in os.listdir(csv_dir) if f.endswith('.csv')]
    for csv_file in csv_files:
        csv_file_path = os.path.join(csv_dir, csv_file)
        table_name = os.path.splitext(csv_file)[0].replace('-', '_')
        df = pd.read_csv(csv_file_path, dtype=str)  # Import all columns as text
        df = clean_column_names(df)  # Clean column names
        df.to_sql(table_name, conn, if_exists='replace', index=False)
        print(f"Imported {csv_file} into table {table_name}")

# Purge existing tables and re-import CSV files
if __name__ == "__main__":
    purge_tables()
    import_csv_files()
    print("All CSV files have been imported into the SQLite database.")
    conn.close()
