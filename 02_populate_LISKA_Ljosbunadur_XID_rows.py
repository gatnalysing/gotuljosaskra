import sqlite3
import time

db_file = 'gotuljosaskra.db'
summary_file = 'populate_summary.txt'
unmatched_file = 'unmatched_xid.txt'

# Connect to the SQLite database
conn = sqlite3.connect(db_file)
cursor = conn.cursor()

# Get the column names of both tables for reference
def get_column_names(table_name):
    cursor.execute(f"PRAGMA table_info({table_name})")
    return [column[1] for column in cursor.fetchall()]

# Populate empty cells in LISKA_Ljosbunadur_1106_2024 with corresponding data from MainManager_ljosbunadur
def populate_liska_from_mainmanager():
    # Get the column names from both tables
    liska_columns = get_column_names('LISKA_Ljosbunadur_1106_2024')
    mainmanager_columns = get_column_names('MainManager_ljosbunadur')

    # Ensure both tables have the same number of columns
    if len(liska_columns) != len(mainmanager_columns):
        print("Error: The number of columns between the two tables does not match.")
        return

    # Open the summary and unmatched files
    with open(summary_file, 'w') as summary, open(unmatched_file, 'w') as unmatched_log:
        # Fetch all rows from LISKA_Ljosbunadur_1106_2024
        cursor.execute("SELECT * FROM LISKA_Ljosbunadur_1106_2024")
        liska_rows = cursor.fetchall()

        total_rows = len(liska_rows)
        matching_rows = 0
        no_matches = 0

        # Iterate through each row of LISKA_Ljosbunadur_1106_2024
        for idx, liska_row in enumerate(liska_rows):
            # Get the Ljósabúnaður_XID to match with MainManager_ljosbunadur
            ljosabunadur_xid = liska_row[4]  # Column 4 is Ljósabúnaður_XID (index starts at 0)

            # Find the corresponding row in MainManager_ljosbunadur based on Ljósabúnaður_XID
            cursor.execute(f"SELECT * FROM MainManager_ljosbunadur WHERE Ljósabúnaður_XID = ?", (ljosabunadur_xid,))
            mainmanager_row = cursor.fetchone()

            if mainmanager_row:
                # Create the updated row by filling in missing data
                updated_row = list(liska_row)
                for i, column_name in enumerate(liska_columns):
                    # If the value in LISKA_Ljosbunadur is empty, take the value from MainManager
                    if not updated_row[i] and mainmanager_row[i]:
                        updated_row[i] = mainmanager_row[i]

                # Update the row in the LISKA_Ljosbunadur_1106_2024 table
                set_clause = ', '.join([f"[{column_name}] = ?" for column_name in liska_columns])
                cursor.execute(f"""
                    UPDATE LISKA_Ljosbunadur_1106_2024 
                    SET {set_clause}
                    WHERE Ljósabúnaður_XID = ?
                """, updated_row + [ljosabunadur_xid])

                matching_rows += 1
            else:
                # Log unmatched Ljósabúnaður_XID
                unmatched_log.write(f"No match for Ljósabúnaður_XID: {ljosabunadur_xid}\n")
                no_matches += 1

            # Sleep to limit the number of operations per second
            time.sleep(0.0015)  # ~1.5ms delay (~666 operations/sec)

            # Optional: print progress to CLI every 1000 rows
            if (idx + 1) % 1000 == 0:
                print(f"Processed {idx + 1} out of {total_rows} rows...")

        # Final summary
        summary.write(f"Summary:\n")
        summary.write(f"Total rows checked: {total_rows}\n")
        summary.write(f"Matching rows: {matching_rows}\n")
        summary.write(f"No matches: {no_matches}\n")

        print("Empty cells in LISKA_Ljosbunadur_1106_2024 have been filled.")
        print(f"Summary written to {summary_file}. Unmatched XIDs written to {unmatched_file}.")

# Run the function to populate the data
populate_liska_from_mainmanager()

# Close the connection
conn.close()
