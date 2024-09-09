import sqlite3

db_file = 'gotuljosaskra.db'

# Connect to the SQLite database
conn = sqlite3.connect(db_file)
cursor = conn.cursor()

# Function to add an ID column if it doesn't exist
def add_id_column(table_name):
    try:
        # Check if the column already exists
        cursor.execute(f"PRAGMA table_info({table_name})")
        columns = cursor.fetchall()
        column_names = [column[1] for column in columns]
        
        if 'ID' not in column_names:
            # Add the ID column if it's not already there
            cursor.execute(f'ALTER TABLE {table_name} ADD COLUMN ID TEXT')
            print(f'Added ID column to {table_name}')
        else:
            print(f'ID column already exists in {table_name}')
    
    except sqlite3.Error as e:
        print(f"Error modifying {table_name}: {e}")

# Add the ID column to both tables
tables_to_modify = ['LISKA_Ljosbunadur_1106_2024', 'LISKA_Ljosastaurar_1106_2024']

for table in tables_to_modify:
    add_id_column(table)

# Commit and close the connection
conn.commit()
conn.close()

print("Finished modifying the tables.")
