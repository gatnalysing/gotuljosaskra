import sqlite3
import time

def get_column_names(cursor, table_name):
    """Fetch all column names for a given table, quoted to handle special characters."""
    cursor.execute(f'PRAGMA table_info({table_name})')
    columns = cursor.fetchall()
    column_names = [f'"{col[1]}"' for col in columns if col[1] != 'Ljósastaur_XID']  # Exclude reference column
    return column_names

def update_columns(db_path):
    # Connect to the SQLite database
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Step 1: Fetch column names from Liska_nyjir_ljosastaurar_1106_2024 and Working_on_table
    target_columns = get_column_names(cursor, 'Liska_nyjir_ljosastaurar_1106_2024')
    source_columns = get_column_names(cursor, 'Working_on_table')

    # Step 2: Fetch all rows from Liska_nyjir_ljosastaurar_1106_2024 that have a matching Ljósastaur_XID in Working_on_table
    cursor.execute('''
        SELECT rowid, Ljósastaur_XID
        FROM Liska_nyjir_ljosastaurar_1106_2024
        WHERE Ljósastaur_XID IS NOT NULL;
    ''')
    rows = cursor.fetchall()

    # Initialize counters for progress tracking
    row_counter = 0  # Tracks total processed rows
    dot_counter = 0  # Tracks progress for printing dots

    # Step 3: Dynamically build the query based on column names
    column_mapping = ', '.join([f'{target} = ?' for target in target_columns])
    update_query = f'UPDATE Liska_nyjir_ljosastaurar_1106_2024 SET {column_mapping} WHERE rowid = ?'

    for row in rows:
        row_id = row[0]
        ljósastaur_xid = row[1]

        # Fetch corresponding data from Working_on_table based on Ljósastaur_XID
        cursor.execute(f'''
            SELECT {', '.join(source_columns)}
            FROM Working_on_table
            WHERE Ljósastaur_XID = ?;
        ''', (ljósastaur_xid,))
        result = cursor.fetchone()

        if result:
            # Update the corresponding row in Liska_nyjir_ljosastaurar_1106_2024
            cursor.execute(update_query, (*result, row_id))
            conn.commit()

        # Throttling: Delay for 3 milliseconds (0.003 seconds)
        time.sleep(0.003)

        # Increment row counter and dot counter
        row_counter += 1
        dot_counter += 1

        # Print a dot every 100 rows
        if dot_counter == 100:
            print('.', end='', flush=True)
            dot_counter = 0

        # Print a new line with total every 1000 rows
        if row_counter % 1000 == 0:
            print(f"\n{row_counter} rows processed.")

    # Close the connection
    conn.close()

    print(f'\nProcessed {row_counter} rows in total in Liska_nyjir_ljosastaurar_1106_2024.')

if __name__ == "__main__":
    db_path = 'gotuljosaskra.db'  # Replace with the correct database path if necessary
    update_columns(db_path)
