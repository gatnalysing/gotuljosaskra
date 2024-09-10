import sqlite3

db_file = 'gotuljosaskra.db'

# Connect to the SQLite database
conn = sqlite3.connect(db_file)
cursor = conn.cursor()

# Step 1: Create a working table to collect unique Ljósastaur_XID values
def create_working_table():
    cursor.execute("DROP TABLE IF EXISTS Working_Ljosastaur_XID")
    cursor.execute("""
        CREATE TABLE Working_Ljosastaur_XID AS 
        SELECT DISTINCT Ljósastaur_XID 
        FROM Liska_nyr_ljosbunadur_1106_2024
        WHERE Ljósastaur_XID IS NOT NULL
    """)
    print("Working table 'Working_Ljosastaur_XID' created with unique Ljósastaur_XID values.")
    conn.commit()

# Step 2: Create the new table Liska_nyjir_ljosastaurar_1106_2024
def create_new_ljosastaurar_table():
    cursor.execute(f"""
        CREATE TABLE IF NOT EXISTS Liska_nyjir_ljosastaurar_1106_2024 AS 
        SELECT * FROM LISKA_Ljosastaurar_1106_2024 WHERE 0
    """)
    print("New table 'Liska_nyjir_ljosastaurar_1106_2024' created.")
    conn.commit()

# Step 3: Populate new table based on unique Ljósastaur_XID values
def populate_new_table():
    # Fetch all unique Ljósastaur_XID from the working table
    cursor.execute("SELECT DISTINCT Ljósastaur_XID FROM Working_Ljosastaur_XID")
    unique_xids = cursor.fetchall()
    
    for xid in unique_xids:
        xid_value = xid[0]

        # Fetch the corresponding row(s) from LISKA_Ljosastaurar_1106_2024
        cursor.execute(f"""
            INSERT INTO Liska_nyjir_ljosastaurar_1106_2024
            SELECT * FROM LISKA_Ljosastaurar_1106_2024
            WHERE Ljósastaur_XID = ?
        """, (xid_value,))
        
        print(f"Populated rows for Ljósastaur_XID: {xid_value}")
        
        # Commit after each insertion to avoid memory overhead
        conn.commit()

# Step 4: Clean up the working table after processing
def clean_up():
    cursor.execute("DROP TABLE IF EXISTS Working_Ljosastaur_XID")
    print("Cleaned up the working table.")

# Run the process
create_working_table()
create_new_ljosastaurar_table()
populate_new_table()
clean_up()

# Close the connection
conn.close()
