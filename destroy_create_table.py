import sqlite3
import pandas as pd
import sys
import os

def destroy_create_table(db_file, table_name, csv_file):
    # Check if the CSV file exists
    if not os.path.exists(csv_file):
        print(f"Error: CSV file '{csv_file}' not found.")
        return

    # Connect to the SQLite database
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()

    try:
        # Drop the existing table if it exists
        cursor.execute(f"DROP TABLE IF EXISTS {table_name}")
        print(f"Table '{table_name}' dropped successfully.")
        
        # Read the CSV file into a DataFrame, treating all columns as TEXT
        df = pd.read_csv(csv_file, dtype=str)  # Ensuring all columns are read as text
        
        # Create the table from the DataFrame
        df.to_sql(table_name, conn, if_exists='replace', index=False)
        print(f"Table '{table_name}' recreated from '{csv_file}' successfully.")
    
    except Exception as e:
        print(f"Error: {e}")
    
    finally:
        # Commit the changes and close the connection
        conn.commit()
        conn.close()

if __name__ == "__main__":
    # Command-line arguments: table name and CSV file
    if len(sys.argv) != 4:
        print("Usage: python destroy_create_table.py <db_file> <table_name> <csv_file>")
        sys.exit(1)

    db_file = sys.argv[1]
    table_name = sys.argv[2]
    csv_file = sys.argv[3]

    # Call the function to destroy and recreate the table
    destroy_create_table(db_file, table_name, csv_file)
