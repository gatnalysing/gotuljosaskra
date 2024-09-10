import sqlite3

def modify_table_structure(db_path):
    # Connect to the SQLite database
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Begin transaction
    cursor.execute("BEGIN TRANSACTION;")

    # Step 1: Create a new table with the desired structure
    cursor.execute('''
        CREATE TABLE new_working_ON_table (
            "ID" TEXT,
            "Lóð" TEXT,
            "Heimtaugarskápur" TEXT,
            "Heimtaugarskápur_XID" TEXT,
            "Auðkenni_ljósastaurs" TEXT,
            "Ljósastaur_XID" TEXT,
            "Gata" TEXT,
            "Staðsetning" TEXT,
            "Tegund_viðfangs" TEXT,
            "Undirtegund" TEXT,
            "X_(lengdargráða)" TEXT,
            "Y_(Breidd)" TEXT,
            "GPS_hæð" TEXT,
            "X" TEXT,
            "Y" TEXT,
            "Dags_uppsett" TEXT,
            "Eigandi_2" TEXT,
            "Eigandi_Umsjón-starfsmaður" TEXT,
            "Kennitala_eiganda" TEXT,
            "Framleiðandi" TEXT,
            "Birgir" TEXT,
            "Efni_staurs" TEXT,
            "Litur_staurs" TEXT,
            "Hæð_staurs_m" TEXT,
            "Hefur_topp_arm" TEXT,
            "Tegund_topps_arms" TEXT,
            "Framleiðandi_topps_arms" TEXT,
            "Söluaðili_topps_arms" TEXT,
            "Tengill" TEXT,
            "Ljósleiðarapípa" TEXT,
            "Dags_burðarþolsprófunar" TEXT,
            "Framkvæmdaraðili_burðarþolsprófunar" TEXT,
            "Tegund_undirstöðu" TEXT,
            "Staða" TEXT,
            "Ástandseinkunn" TEXT
        );
    ''')

    # Step 2: Copy data from the original table into the new table
    cursor.execute('''
        INSERT INTO new_working_ON_table (
            "Heimtaugarskápur_XID", 
            "Heimtaugarskápur", 
            "Ljósastaur_XID", 
            "Gata", 
            "Staðsetning", 
            "Tegund_viðfangs", 
            "Undirtegund", 
            "X", 
            "Y", 
            "Dags_uppsett", 
            "Eigandi_2", 
            "Eigandi_Umsjón-starfsmaður", 
            "Kennitala_eiganda", 
            "Hæð_staurs_m"
        )
        SELECT 
            "Heimtaugarskápur XID", 
            "Heimtaugarskápur", 
            "Ljósastaur XID", 
            "Gata", 
            "Staðsetning", 
            "Tegund viðfangs", 
            "Undirtegund", 
            "X", 
            "Y", 
            "Dags. uppsett", 
            "Eigandi 2", 
            "Eigandi Umsjón-starfsmaður", 
            "Kennitala eiganda", 
            "Hæð staurs [m]"
        FROM working_ON_table;
    ''')

    # Step 3: Drop the old table
    cursor.execute("DROP TABLE working_ON_table;")

    # Step 4: Rename the new table to the original table name
    cursor.execute("ALTER TABLE new_working_ON_table RENAME TO working_ON_table;")

    # Commit transaction
    conn.commit()

    # Close the connection
    conn.close()

    print("Table structure modified successfully!")

if __name__ == "__main__":
    db_path = 'gotuljosaskra.db'
    modify_table_structure(db_path)
