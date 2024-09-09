import sqlite3

db_file = 'gotuljosaskra.db'
unmatched_file = 'unmatched_xid.txt'
new_table = 'Liska_nyr_ljosbunadur_1106_2024'

# Connect to the SQLite database
conn = sqlite3.connect(db_file)
cursor = conn.cursor()

# Read unmatched XIDs from unmatched_xid.txt
def get_unmatched_xids():
    unmatched_xids = []
    with open(unmatched_file, 'r') as f:
        for line in f:
            if "No match for Ljósabúnaður_XID:" in line:
                unmatched_xid = line.split(": ")[1].strip()  # Extract the XID number
                unmatched_xids.append(unmatched_xid)
    return unmatched_xids

# Create new table with rows containing unmatched Ljósabúnaður_XID
def create_new_table_with_unmatched_xids():
    unmatched_xids = get_unmatched_xids()

    if not unmatched_xids:
        print("No unmatched XIDs found in the file.")
        return

    # Create the new table structure based on LISKA_Ljosbunadur_1106_2024
    cursor.execute(f"CREATE TABLE IF NOT EXISTS {new_table} AS SELECT * FROM LISKA_Ljosbunadur_1106_2024 WHERE 0")

    # Insert rows that match the unmatched XIDs
    placeholders = ', '.join('?' for _ in unmatched_xids)
    cursor.execute(f"""
        INSERT INTO {new_table}
        SELECT * FROM LISKA_Ljosbunadur_1106_2024 
        WHERE Ljósabúnaður_XID IN ({placeholders})
    """, unmatched_xids)

    conn.commit()
    print(f"New table '{new_table}' created with rows matching unmatched XIDs.")

# Run the function to create the new table
create_new_table_with_unmatched_xids()

# Close the connection
conn.close()
