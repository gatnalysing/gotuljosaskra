import sqlite3

db_file = 'gotuljosaskra.db'

# Connect to the SQLite database
conn = sqlite3.connect(db_file)
cursor = conn.cursor()

# Get the column names of both tables for reference
def get_column_count(table_name):
    cursor.execute(f"PRAGMA table_info({table_name})")
    return len(cursor.fetchall())

# Populate empty cells in LISKA_Ljosbunadur_1106_2024 with corresponding data from MainManager_ljosbunadur
def populate_liska_from_mainmanager():
    # Get the number of columns in both tables (assuming order matches)
    liska_column_count = get_column_count('LISKA_Ljosbunadur_1106_2024')
    mainmanager_column_count = get_column_count('MainManager_ljosbunadur')

    # Ensure both tables have the same number of columns
    if liska_column_count != mainmanager_column_count:
        print("Error: The number of columns between the two tables does not match.")
        return

    # Fetch all rows from LISKA_Ljosbunadur_1106_2024
    cursor.execute("SELECT * FROM LISKA_Ljosbunadur_1106_2024")
    liska_rows = cursor.fetchall()

    # Iterate through each row of LISKA_Ljosbunadur_1106_2024
    for liska_row in liska_rows:
        # Get the Ljósabúnaður_XID to match with MainManager_ljosbunadur
        ljosabunadur_xid = liska_row[3]  # Column 4 is Ljósabúnaður_XID (index starts at 0)
        
        # Find the corresponding row in MainManager_ljosbunadur based on Ljósabúnaður_XID
        cursor.execute(f"SELECT * FROM MainManager_ljosbunadur WHERE Ljósabúnaður_XID = ?", (ljosabunadur_xid,))
        mainmanager_row = cursor.fetchone()

        if mainmanager_row:
            # Create the updated row by filling in missing data
            updated_row = list(liska_row)
            for i in range(liska_column_count):
                # If the value in LISKA_Ljosbunadur is empty, take the value from MainManager
                if not updated_row[i]:
                    updated_row[i] = mainmanager_row[i]

            # Update the row in the LISKA_Ljosbunadur_1106_2024 table
            cursor.execute(f"""
                UPDATE LISKA_Ljosbunadur_1106_2024 
                SET {', '.join([f'column{i + 1} = ?' for i in range(liska_column_count)])}
                WHERE Ljósabúnaður_XID = ?
            """, updated_row + [ljosabunadur_xid])

    # Commit the changes
    conn.commit()
    print("Empty cells in LISKA_Ljosbunadur_1106_2024 have been filled.")

# Run the function to populate the data
populate_liska_from_mainmanager()

# Close the connection
conn.close()
