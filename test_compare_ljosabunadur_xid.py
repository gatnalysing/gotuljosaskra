import sqlite3

db_file = 'gotuljosaskra.db'

# Connect to the SQLite database
conn = sqlite3.connect(db_file)
cursor = conn.cursor()

# Function to fetch Ljósabúnaður_XID values from a table
def fetch_ljosabunadur_xid(table_name):
    cursor.execute(f"SELECT Ljósabúnaður_XID FROM {table_name}")
    return cursor.fetchall()

# Function to compare Ljósabúnaður_XID values in both tables
def compare_ljosabunadur_xid():
    # Fetch Ljósabúnaður_XID from both tables
    cursor.execute("SELECT Ljósabúnaður_XID FROM LISKA_Ljosbunadur_1106_2024")
    liska_values = cursor.fetchall()
    
    cursor.execute("SELECT Ljósabúnaður_XID FROM MainManager_ljosbunadur")
    mainmanager_values = cursor.fetchall()

    # Set for efficient lookup of MainManager values
    mainmanager_set = set([row[0] for row in mainmanager_values])

    total_rows = len(liska_values)
    matching_count = 0
    empty_count = 0
    no_match_count = 0

    # Counters for how many results to show in detail
    show_limit = 5
    shown_matching = 0
    shown_no_match = 0

    # Compare the values
    for row in liska_values:
        xid = row[0]
        if xid == "" or xid is None:
            empty_count += 1
        elif xid in mainmanager_set:
            matching_count += 1
            if shown_matching < show_limit:
                print(f"Matching Ljósabúnaður_XID: {xid}")
                shown_matching += 1
        else:
            no_match_count += 1
            if shown_no_match < show_limit:
                print(f"No match for Ljósabúnaður_XID: {xid}")
                shown_no_match += 1

    print(f"\nSummary:\nTotal rows checked: {total_rows}\nMatching rows: {matching_count}\nEmpty rows: {empty_count}\nNo matches: {no_match_count}")

# Run the comparison function
compare_ljosabunadur_xid()

# Close the connection
conn.close()
