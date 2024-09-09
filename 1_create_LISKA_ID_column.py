import sqlite3

db_file = 'gotuljosaskra.db'

# Connect to the SQLite database
conn = sqlite3.connect(db_file)
cursor = conn.cursor()

# Function to add an empty ID column as the first column
def add_id_column_as_first(table_name):
    try:
        # Get current columns
        cursor.execute(f"PRAGMA table_info({table_name})")
        columns = cursor.fetchall()
        column_names = [f'"{column[1]}"' for column in columns]  # Properly quote column names
        
        # If 'ID' is not already a column, we will recreate the table with it as the first column
        if '"ID"' not in column_names:
            new_columns = ['ID TEXT'] + column_names  # Add ID and preserve other columns
            new_columns_str = ', '.join(new_columns)
            
            # Rename the current table
            cursor.execute(f'ALTER TABLE {table_name} RENAME TO {table_name}_backup')

            # Create the new table with the ID as the first column
            cursor.execute(f'CREATE TABLE {table_name} ({new_columns_str})')

            # Insert data from the old table to the new one, using NULL for the new ID column
            old_columns_str = ', '.join(column_names)
            cursor.execute(f'INSERT INTO {table_name} ({old_columns_str}) SELECT {old_columns_str} FROM {table_name}_backup')

            # Drop the backup table
            cursor.execute(f'DROP TABLE {table_name}_backup')

            print(f'Added ID column as the first column in {table_name}')
        else:
            print(f'ID column already exists in {table_name}')
    
    except sqlite3.Error as e:
        print(f"Error modifying {table_name}: {e}")

# Add the ID column to both tables
tables_to_modify = ['LISKA_Ljosbunadur_1106_2024', 'LISKA_Ljosastaurar_1106_2024']

for table in tables_to_modify:
    add_id_column_as_first(table)

# Commit and close the connection
conn.commit()
conn.close()

print("Finished modifying the tables.")
