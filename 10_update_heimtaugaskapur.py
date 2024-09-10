import sqlite3

def update_column_with_formatted_values(db_path):
    # Connect to the SQLite database
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Step 1: Select the Heimtaugarskápur_XID and the corresponding row ID
    cursor.execute('SELECT rowid, "Heimtaugarskápur_XID" FROM working_ON_table')
    rows = cursor.fetchall()

    # Step 2: Update the Heimtaugarskápur column based on the Heimtaugarskápur_XID values
    for row in rows:
        row_id = row[0]
        xid_value = row[1]

        # Check if xid_value is not None or empty
        if xid_value is not None and xid_value != '':
            # Step 3: Format the number with leading zeros and append '_01'
            formatted_value = f'{str(xid_value).zfill(4)}_01'

            # Step 4: Update the Heimtaugarskápur column with the formatted value
            cursor.execute('''
                UPDATE working_ON_table
                SET "Heimtaugarskápur" = ?
                WHERE rowid = ?;
            ''', (formatted_value, row_id))

    # Commit the changes
    conn.commit()

    # Close the connection
    conn.close()

    print('Heimtaugarskápur column updated based on Heimtaugarskápur_XID values.')

if __name__ == "__main__":
    db_path = 'gotuljosaskra.db'  # Replace with the correct database path if necessary
    update_column_with_formatted_values(db_path)
