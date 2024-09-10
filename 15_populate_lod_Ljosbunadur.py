import sqlite3

def update_lod_from_ljosastaurar(db_path):
    # Connect to the SQLite database
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Step 1: Fetch all rows from Liska_nyjir_ljosastaurar where Lóð is not NULL
    cursor.execute('''
        SELECT Lóð, Ljósastaur_XID
        FROM Liska_nyjir_ljosastaurar
        WHERE Lóð IS NOT NULL;
    ''')
    rows = cursor.fetchall()

    # Step 2: Update corresponding rows in Liska_nyr_ljosbunadur_1106_2024 based on Ljósastaur_XID
    for row in rows:
        lod_value = row[0]
        ljosastaur_xid = row[1]

        # Update the Lóð column in Liska_nyr_ljosbunadur_1106_2024 where Ljósastaur_XID matches
        cursor.execute('''
            UPDATE Liska_nyr_ljosbunadur_1106_2024
            SET Lóð = ?
            WHERE Ljósastaur_XID = ?;
        ''', (lod_value, ljosastaur_xid))

    # Commit the changes
    conn.commit()

    # Close the connection
    conn.close()

    print("Lóð column updated successfully.")

if __name__ == "__main__":
    db_path = 'gotuljosaskra.db'  # Replace with the correct database path if necessary
    update_lod_from_ljosastaurar(db_path)
