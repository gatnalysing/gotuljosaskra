import sqlite3

db_file = 'gotuljosaskra.db'

# Connect to the SQLite database
conn = sqlite3.connect(db_file)
cursor = conn.cursor()

# Function to drop the unwanted ID column and add a new one as the first column
def modify_table(table_name):
    try:
        # Get the table structure excluding the unwanted ID column
        cursor.execute(f"PRAGMA table_info({table_name})")
        columns = cursor.fetchall()
        column_names = [column[1] for column in columns if column[1] != 'ID']

        # Create a new table with the correct structure (ID as the first column)
        new_table_name = f"{table_name}_new"
        columns_sql = ', '.join(column_names)
        create_sql = f"CREATE TABLE {new_table_name} (ID TEXT, {columns_sql})"
        cursor.execute(create_sql)
        
        # Copy the data from the old table to the new table
        copy_sql = f"INSERT INTO {new_table_name} (ID, {columns_sql}) SELECT NULL, {columns_sql} FROM {table_name}"
        cursor.execute(copy_sql)
        
        # Drop the old table
        cursor.execute(f"DROP TABLE {table_name}")
        
        # Rename the new table to the original table name
        cursor.execute(f"ALTER TABLE {new_table_name} RENAME TO {table_name}")
        
        print(f"Modified {table_name} to have ID as the first column.")
    
    except sqlite3.Error as e:
        print(f"Error modifying {table_name}: {e}")

# Modify both tables
tables_to_modify = ['LISKA_Ljosbunadur_1106_2024', 'LISKA_Ljosastaurar_1106_2024']

for table in tables_to_modify:
    modify_table(table)

# Commit and close the connection
conn.commit()
conn.close()

print("Finished modifying the tables.")
