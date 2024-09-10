import sqlite3

def copy_column_values(db_path):
    # Connect to the SQLite database
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Step 1: Update the Auðkenni_ljósastaurs column to match Ljósastaur_XID
    cursor.execute('''
        UPDATE working_ON_table
        SET "Auðkenni_ljósastaurs" = "Ljósastaur_XID";
    ''')

    # Commit the changes
    conn.commit()

    # Close the connection
    conn.close()

    print('Auðkenni_ljósastaurs column updated to match Ljósastaur_XID.')

if __name__ == "__main__":
    db_path = 'gotuljosaskra.db'  # Replace with the correct database path if necessary
    copy_column_values(db_path)
