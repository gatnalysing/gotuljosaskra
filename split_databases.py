import sqlite3

def create_and_copy_tables(db_path, new_db_path, tables_to_copy):
    # Connect to the original database and the new database
    conn_original = sqlite3.connect(db_path)
    conn_new = sqlite3.connect(new_db_path)
    
    cursor_original = conn_original.cursor()
    cursor_new = conn_new.cursor()

    # Copy each table from the original to the new database
    for table in tables_to_copy:
        # Fetch the CREATE TABLE statement for each table
        cursor_original.execute(f"SELECT sql FROM sqlite_master WHERE type='table' AND name='{table}'")
        create_table_sql = cursor_original.fetchone()
        
        if create_table_sql:
            cursor_new.execute(create_table_sql[0])  # Create the table in the new database
            
            # Copy data from the original table to the new table
            cursor_new.execute(f"INSERT INTO {table} SELECT * FROM {table}")

    # Commit changes and close the new database connection
    conn_new.commit()
    conn_new.close()
    
    # Close the original database connection
    conn_original.close()

# Database paths
original_db = 'gotuljosaskra.db'
gogn_db = 'gogn.db'
vinnsla_db = 'vinnsla.db'
nytt_db = 'nytt.db'

# Tables to move to 'gogn.db'
gogn_tables = [
    'ON_ljosbunadur_2023', 'MainManager_heimtaugaskapar', 'MainManager_ljosbunadur',
    'LISKA_Ljosbunadur_1106_2024', 'LISKA_Ljosastaurar_1106_2024', 'MainManager_ljosastaurar'
]

# Tables to move to 'vinnsla.db'
vinnsla_tables = [
    'LISKA_heimtaugaskapar_allir_2024_05_27', 'Liska_nyr_ljosbunadur_1106_2024',
    'Liska_nyjir_ljosastaurar_1106_2024', 'working_ON_table'
]

# Tables to move to 'nytt.db'
nytt_tables = [
    'Liska_nyjir_ljosastaurar', 'Liska_nyr_ljosbunadur'
]

# Create the 'gogn.db' and copy tables
create_and_copy_tables(original_db, gogn_db, gogn_tables)

# Create the 'vinnsla.db' and copy tables
create_and_copy_tables(original_db, vinnsla_db, vinnsla_tables)

# Create the 'nytt.db' and copy tables
create_and_copy_tables(original_db, nytt_db, nytt_tables)

print("Database split and tables copied successfully.")
