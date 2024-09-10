from flask import Flask, render_template_string, abort, request, redirect, url_for, Response
import sqlite3
import csv
import io
import pandas as pd
import datetime

app = Flask(__name__)

LOG_FILE = 'download_log.txt'

# HTML template for rendering the databases and tables
HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
<title>{{ db_name | capitalize if db_name else "Gagnagrunnar" }}</title>
<style>
table, th, td {
  border: 1px solid black;
  border-collapse: collapse;
}
th, td {
  padding: 10px;
  text-align: left;
}
</style>
</head>
<body>
{% if not db_name %}
<h2>Gagnagrunnar</h2> <!-- Changed from "Select Database" to "Gagnagrunnar" -->
<ul>
  <li><a href="/gogn">Upprunaleg Gögn</a></li> <!-- Changed label to "Upprunaleg Gögn" -->
  <li><a href="/vinnsla">Vinnslugögn</a></li> <!-- Changed label to "Vinnslugögn" -->
  <li><a href="/nytt">Ný Gögn</a></li> <!-- Changed label to "Ný Gögn" -->
</ul>
{% elif not table_name %}
<h2>Töflur í {{ db_name | capitalize }} (Max 2000 rows)</h2>
<ul>
  {% for table in tables %}
  <li>
    <a href="/{{ db_name }}/{{ table }}">{{ table }}</a> - 
    <a href="/download/{{ db_name }}/{{ table }}/csv">csv</a> - 
    <a href="/download/{{ db_name }}/{{ table }}/excel">excel</a>
  </li>
  {% endfor %}
</ul>
{% else %}
<h2>{{ table_name | capitalize }} (Max 2000 rows)</h2>
<table>
  <tr>
    {% for column in columns %}
    <th>{{ column }}</th>
    {% endfor %}
  </tr>
  {% for row in rows %}
  <tr>
    {% for cell in row %}
    <td>{{ cell }}</td>
    {% endfor %}
  </tr>
  {% endfor %}
</table>
{% endif %}
</body>
</html>
"""

# HTML template for the download form (prompt for name)
DOWNLOAD_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
<title>Download</title>
</head>
<body>
<h2>Download</h2>
<form method="POST">
  <label for="name">Nafn Starfsmanns:</label><br>
  <input type="text" id="name" name="name" required><br><br>
  <input type="submit" value="Download {{ format }}">
</form>
</body>
</html>
"""

# HTML template for displaying the log
LOG_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
<title>Download Log</title>
</head>
<body>
<h2>Download Log</h2>
<table border="1">
<tr>
    <th>Timestamp</th>
    <th>Name</th>
    <th>Database</th>
    <th>Table</th>
    <th>Format</th>
</tr>
{% for log_entry in log_entries %}
<tr>
    <td>{{ log_entry.timestamp }}</td>
    <td>{{ log_entry.name }}</td>
    <td>{{ log_entry.db_name }}</td>
    <td>{{ log_entry.table_name }}</td>
    <td>{{ log_entry.format }}</td>
</tr>
{% endfor %}
</table>
</body>
</html>
"""

# Function to select the database path based on the database name
def get_db_path(db_name):
    if db_name == 'gogn':
        return 'gogn.db'
    elif db_name == 'vinnsla':
        return 'vinnsla.db'
    elif db_name == 'nytt':
        return 'nytt.db'
    else:
        return None

# Function to connect to the appropriate database
def get_db_connection(db_name):
    db_path = get_db_path(db_name)
    if db_path:
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        return conn
    return None

# Route to display the available databases and tables
@app.route('/', defaults={'db_name': None, 'table_name': None})
@app.route('/<db_name>', defaults={'table_name': None})
@app.route('/<db_name>/<table_name>')
def show_table(db_name, table_name):
    if not db_name:  # If no database is selected, show the database options
        return render_template_string(HTML_TEMPLATE, db_name=None)

    conn = get_db_connection(db_name)
    if conn is None:
        abort(404)  # If database not found, return 404

    cur = conn.cursor()
    
    if table_name is None:
        # Fetch and display a list of all tables in the selected database
        cur.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = [row[0] for row in cur.fetchall()]
        conn.close()
        return render_template_string(HTML_TEMPLATE, db_name=db_name, tables=tables)
    else:
        # Display the first 2000 rows from the selected table in the selected database
        try:
            cur.execute(f'SELECT * FROM {table_name} LIMIT 2000')
        except sqlite3.OperationalError:
            conn.close()
            abort(404)  # Table not found, return 404
        rows = cur.fetchall()
        columns = [description[0] for description in cur.description]
        conn.close()
        return render_template_string(HTML_TEMPLATE, db_name=db_name, rows=rows, columns=columns, table_name=table_name)

# Route for download form (CSV/Excel)
@app.route('/download/<db_name>/<table_name>/<format>', methods=['GET', 'POST'])
def download(db_name, table_name, format):
    if request.method == 'POST':
        name = request.form['name']
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Log the download instance
        with open(LOG_FILE, 'a') as log_file:
            log_file.write(f"{timestamp},{name},{db_name},{table_name},{format}\n")

        if format == 'csv':
            return export_csv(db_name, table_name)
        elif format == 'excel':
            return export_excel(db_name, table_name)

    return render_template_string(DOWNLOAD_TEMPLATE, format=format)

# Route to export the table as CSV
def export_csv(db_name, table_name):
    conn = get_db_connection(db_name)
    if conn is None:
        abort(404)

    cur = conn.cursor()
    try:
        cur.execute(f'SELECT * FROM {table_name}')
    except sqlite3.OperationalError:
        conn.close()
        abort(404)

    # Fetch the data
    rows = cur.fetchall()
    columns = [description[0] for description in cur.description]
    conn.close()

    # Create a CSV in-memory file
    output = io.StringIO()
    writer = csv.writer(output)

    # Write the header
    writer.writerow(columns)

    # Write the data rows
    for row in rows:
        writer.writerow([str(cell) for cell in row])

    # Prepare CSV as a response
    output.seek(0)
    return Response(output, mimetype='text/csv',
                    headers={"Content-Disposition": f"attachment;filename={table_name}.csv"})

# Route to export the table as Excel
def export_excel(db_name, table_name):
    conn = get_db_connection(db_name)
    if conn is None:
        abort(404)

    cur = conn.cursor()
    try:
        cur.execute(f'SELECT * FROM {table_name}')
    except sqlite3.OperationalError:
        conn.close()
        abort(404)

    # Fetch the data
    rows = cur.fetchall()
    columns = [description[0] for description in cur.description]
    conn.close()

    # Create a pandas DataFrame
    df = pd.DataFrame(rows, columns=columns)

    # Create an in-memory Excel file
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False)

    # Prepare Excel as a response
    output.seek(0)
    return Response(output, mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
                    headers={"Content-Disposition": f"attachment;filename={table_name}.xlsx"})

# Route to view the log of downloads
@app.route('/log')
def view_log():
    log_entries = []
    try:
        with open(LOG_FILE, 'r') as log_file:
            for line in log_file:
                timestamp, name, db_name, table_name, format = line.strip().split(',')
                log_entries.append({
                    'timestamp': timestamp,
                    'name': name,
                    'db_name': db_name,
                    'table_name': table_name,
                    'format': format
                })
    except FileNotFoundError:
        pass

    return render_template_string(LOG_TEMPLATE, log_entries=log_entries)

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=3500)
