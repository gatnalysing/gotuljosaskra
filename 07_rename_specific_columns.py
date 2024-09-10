import sqlite3
import sys

def rename_columns(db_path, table_name):
    # Connect to the SQLite database
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Begin transaction
    cursor.execute("BEGIN TRANSACTION;")

    # Get the column names from the table
    cursor.execute(f"PRAGMA table_info({table_name});")
    columns = cursor.fetchall()

    # Define the specific renames you want to do
    rename_map = {
        "Dags._burðarþolsprófunar": "Dags_burðarþolsprófunar",
        "Dags._uppsett": "Dags_uppsett"
    }

    # Create the new column names list
    new_columns = []
    for col in columns:
        col_name = col[1]
        # Rename specific columns based on the map
        if col_name in rename_map:
            new_columns.append(rename_map[col_name])
        else:
            new_columns.append(col_name)

    # Generate the SELECT clause with the new column names (escape column names with double quotes)
    select_clause = ', '.join([f'"{col[1]}" AS "{new_col}"' for col, new_col in zip(columns, new_columns)])

    # Create the new table
    new_table_name = f"new_{table_name}"
    cursor.execute(f'''
        CREATE TABLE {new_table_name} AS
        SELECT {select_clause}
        FROM "{table_name}";
    ''')

    # Drop the old table
    cursor.execute(f'DROP TABLE "{table_name}";')

    # Rename the new table to the original table name
    cursor.execute(f'ALTER TABLE "{new_table_name}" RENAME TO "{table_name}";')

    # Commit transaction
    conn.commit()

    # Close the connection
    conn.close()

    print(f"Successfully renamed columns in table '{table_name}' in database '{db_path}'.")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python3 rename_specific_columns.py <db_path> <table_name>")
        sys.exit(1)

    db_path = sys.argv[1]
    table_name = sys.argv[2]

    rename_columns(db_path, table_name)
