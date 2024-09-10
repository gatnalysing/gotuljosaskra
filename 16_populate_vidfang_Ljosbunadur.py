import sqlite3

def update_vidfang_from_ljosastaurar(db_path):
    # Connect to the SQLite database
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Step 1: Fetch all rows from Liska_nyjir_ljosastaurar where Viðfang is not NULL
    cursor.execute('''
        SELECT Tegund_viðfangs, Ljósastaur_XID
        FROM Liska_nyjir_ljosastaurar
        WHERE Tegund_viðfangs IS NOT NULL;
    ''')
    rows = cursor.fetchall()

    # Step 2: Update corresponding rows in Liska_nyr_ljosbunadur_1106_2024 based on Ljósastaur_XID
    for row in rows:
        vidfang_value = row[0]
        ljosastaur_xid = row[1]

        # Update the Viðfang column in Liska_nyr_ljosbunadur_1106_2024 where Ljósastaur_XID matches
        cursor.execute('''
            UPDATE Liska_nyr_ljosbunadur_1106_2024
            SET Viðfang = ?
            WHERE Ljósastaur_XID = ?;
        ''', (vidfang_value, ljosastaur_xid))

    # Commit the changes
    conn.commit()

    # Close the connection
    conn.close()

    print("Viðfang column updated successfully.")

if __name__ == "__main__":
    db_path = 'gotuljosaskra.db'  # Replace with the correct database path if necessary
    update_vidfang_from_ljosastaurar(db_path)
