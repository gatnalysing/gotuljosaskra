import sqlite3
from pyproj import Transformer
import time

# Coordinate conversion function using pyproj
def convert_coordinates(x, y):
    transformer = Transformer.from_crs("epsg:3057", "epsg:4326")  # ISN93 to WGS84
    lat, lon = transformer.transform(x, y)
    return lat, lon

# Format the coordinate to make sure it has a decimal point in the right place
def format_coordinate(coord):
    return float(coord)

def update_coordinates_with_progress(db_path):
    # Connect to the SQLite database
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Step 1: Fetch all rows from Working_on_table that need coordinates updated
    cursor.execute('''
        SELECT rowid, X, Y 
        FROM Working_on_table
        WHERE X IS NOT NULL AND Y IS NOT NULL;
    ''')
    rows = cursor.fetchall()

    # Initialize counters for progress tracking
    total_rows = len(rows)
    dot_counter = 0  # Tracks progress for printing dots
    row_counter = 0  # Tracks total processed rows

    # Step 2: Convert and update coordinates for each row, with throttling and progress display
    for row in rows:
        row_id = row[0]
        x_value = format_coordinate(row[1])
        y_value = format_coordinate(row[2])

        # Convert the coordinates from ISN93 to WGS84
        latitude, longitude = convert_coordinates(x_value, y_value)

        # Update the respective columns in the Working_on_table
        cursor.execute('''
            UPDATE Working_on_table
            SET "X_(lengdargráða)" = ?, "Y_(Breidd)" = ?
            WHERE rowid = ?;
        ''', (longitude, latitude, row_id))

        # Commit the change for this row
        conn.commit()

        # Throttling: Delay for 3 milliseconds (0.003 seconds)
        time.sleep(0.003)

        # Increment row counter and print progress
        row_counter += 1
        dot_counter += 1

        # Print a dot for every 100 rows
        if dot_counter == 100:
            print('.', end='', flush=True)
            dot_counter = 0

        # Move to a new line every 1000 rows
        if row_counter % 1000 == 0:
            print(f" {row_counter}/{total_rows}")

    # Close the connection
    conn.close()

    print(f'\nCoordinates updated successfully for {row_counter} rows in Working_on_table.')

if __name__ == "__main__":
    db_path = 'gotuljosaskra.db'  # Replace with the correct database path if necessary
    update_coordinates_with_progress(db_path)
