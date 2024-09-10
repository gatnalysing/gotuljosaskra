import sqlite3

db_file = 'gotuljosaskra.db'

# Connect to the SQLite database
conn = sqlite3.connect(db_file)
cursor = conn.cursor()

# Step 1: Create a copy of ON_ljosbunadur_2023
def create_working_table():
    cursor.execute('CREATE TABLE IF NOT EXISTS working_ON_table AS SELECT * FROM ON_ljosbunadur_2023')
    print("working_ON_table created as a copy of ON_ljosbunadur_2023")

# Step 2: Rename specific columns in working_ON_table
def rename_columns():
    # Renaming the columns using ALTER TABLE by recreating the table with renamed columns
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS temp_table AS 
        SELECT 
            DNR AS "Heimtaugarskápur XID",
            GLJ_ID AS "Ljósastaur XID",
            GATA_HEITI AS "Gata",
            STADUR AS "Staðsetning",
            STOLPA_TEG AS "Tegund viðfangs",
            STOLPA_SKM AS "Undirtegund",
            X AS "X",
            Y AS "Y",
            GLJ_DAGS AS "Dags. uppsett",
            EIGANDI AS "Eigandi 2",
            NAFN_NOTANDA AS "Eigandi Umsjón-starfsmaður",
            KT_NOTANDA AS "Kennitala eiganda",
            HAED_LAMPA AS "Hæð staurs [m]"
        FROM working_ON_table
    ''')
    print("Columns renamed.")

# Step 3: Drop the old working_ON_table and replace it with the new one
def finalize_table():
    cursor.execute('DROP TABLE IF EXISTS working_ON_table')
    cursor.execute('ALTER TABLE temp_table RENAME TO working_ON_table')
    print("Old working_ON_table dropped and new table renamed.")

# Execute all steps
create_working_table()
rename_columns()
finalize_table()

# Commit changes and close the connection
conn.commit()
conn.close()

print("Script completed successfully.")
