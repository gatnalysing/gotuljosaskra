import sqlite3

def update_lod_from_heimtaugarskapar(db_path):
    # Connect to the SQLite database
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Step 1: Add the 'Lóð' column to 'Working_on_table' if it doesn't exist
    try:
        cursor.execute('''
            ALTER TABLE Working_on_table ADD COLUMN Lóð INTEGER;
        ''')
    except sqlite3.OperationalError:
        print('Column "Lóð" already exists in "Working_on_table".')

    # Step 2: Update the 'Lóð' column in 'Working_on_table' based on 'Heimtaugarskápur_XID'
    cursor.execute('''
        UPDATE Working_on_table
        SET Lóð = (
            SELECT Mainmanager_heimtaugaskapar.Lóð
            FROM Mainmanager_heimtaugaskapar
            WHERE Working_on_table.Heimtaugarskápur_XID = Mainmanager_heimtaugaskapar.Heimtaugarskápur_XID
        )
        WHERE EXISTS (
            SELECT 1
            FROM Mainmanager_heimtaugaskapar
            WHERE Working_on_table.Heimtaugarskápur_XID = Mainmanager_heimtaugaskapar.Heimtaugarskápur_XID
        );
    ''')

    # Commit the changes
    conn.commit()

    # Close the connection
    conn.close()

    print('Lóð column in Working_on_table updated based on Heimtaugarskápur_XID values from Mainmanager_heimtaugaskapar.')

if __name__ == "__main__":
    db_path = 'gotuljosaskra.db'  # Replace with the correct database path if necessary
    update_lod_from_heimtaugarskapar(db_path)
