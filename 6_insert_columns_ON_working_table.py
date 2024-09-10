import sqlite3

db_file = 'gotuljosaskra.db'

# Connect to the SQLite database
conn = sqlite3.connect(db_file)
cursor = conn.cursor()

# Step 1: Rename columns with spaces to use underscores
def rename_columns_with_underscores(table_name):
    cursor.execute(f"PRAGMA table_info({table_name})")
    columns = cursor.fetchall()
    
    for column in columns:
        old_column_name = column[1]
        if ' ' in old_column_name:
            new_column_name = old_column_name.replace(' ', '_')
            cursor.execute(f'ALTER TABLE {table_name} RENAME COLUMN "{old_column_name}" TO "{new_column_name}"')
            print(f'Renamed column "{old_column_name}" to "{new_column_name}"')

# Step 2: Create a new table with the desired structure
def create_new_table_with_empty_columns():
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS working_ON_table_new (
            ID TEXT,
            Lóð TEXT,
            Heimtaugarskápur TEXT,
            Heimtaugarskápur_XID TEXT,
            Auðkenni_ljósastaurs TEXT,
            Ljósastaur_XID TEXT,
            Gata TEXT,
            Staðsetning TEXT,
            Tegund_viðfangs TEXT,
            Undirtegund TEXT,
            X_lengdargráða TEXT,
            Y_Breidd TEXT,
            GPS_hæð TEXT,
            X TEXT,
            Y TEXT,
            "Dags._uppsett" TEXT,
            Eigandi_2 TEXT,
            Eigandi_Umsjón_starfsmaður TEXT,
            Kennitala_eiganda TEXT,
            Framleiðandi TEXT,
            Birgir TEXT,
            Efni_staurs TEXT,
            Litur_staurs TEXT,
            Hæð_staurs_m TEXT,
            Hefur_topp_arm TEXT,
            Tegund_topps_arms TEXT,
            Framleiðandi_topps_arms TEXT,
            Söluaðili_topps_arms TEXT,
            Tengill TEXT,
            Ljósleiðarapípa TEXT,
            Dags_burðarþolsprófunar TEXT,
            Framkvæmdaraðili_burðarþolsprófunar TEXT,
            Tegund_undirstöðu TEXT,
            Staða TEXT,
            Ástandseinkunn TEXT
        )
    ''')
    print("New table with empty columns created.")

# Step 3: Insert existing data from working_ON_table into the new table
def populate_new_table():
    cursor.execute('''
        INSERT INTO working_ON_table_new (
            Heimtaugarskápur_XID, 
            Ljósastaur_XID, 
            Gata, 
            Staðsetning, 
            Tegund_viðfangs, 
            Undirtegund, 
            X, 
            Y, 
            "Dags._uppsett", 
            Eigandi_2, 
            Eigandi_Umsjón_starfsmaður, 
            Kennitala_eiganda, 
            Hæð_staurs_m
        )
        SELECT 
            Heimtaugarskápur_XID, 
            Ljósastaur_XID, 
            Gata, 
            Staðsetning, 
            Tegund_viðfangs, 
            Undirtegund, 
            X, 
            Y, 
            "Dags._uppsett", 
            Eigandi_2, 
            Eigandi_Umsjón_starfsmaður, 
            Kennitala_eiganda, 
            Hæð_staurs_m
        FROM working_ON_table
    ''')
    print("Data copied to the new table.")

# Step 4: Drop the old table and rename the new one
def replace_old_table():
    cursor.execute('DROP TABLE IF EXISTS working_ON_table')
    cursor.execute('ALTER TABLE working_ON_table_new RENAME TO working_ON_table')
    print("Old table dropped and new table renamed.")

# Execute all steps
rename_columns_with_underscores('working_ON_table')
create_new_table_with_empty_columns()
populate_new_table()
replace_old_table()

# Commit changes and close the connection
conn.commit()
conn.close()

print("Table modification completed successfully.")
