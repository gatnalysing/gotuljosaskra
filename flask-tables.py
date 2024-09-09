from flask import Flask, render_template_string, abort
import sqlite3

app = Flask(__name__)

# HTML template for rendering the tables
HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
<title>{{ table_name | capitalize }} Table</title>
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
{% if table_name %}
<h2>{{ table_name | capitalize }} Data</h2>
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
{% else %}
<h2>Available Tables</h2>
<ul>
  {% for table in tables %}
  <li><a href="/table/{{ table }}">{{ table }}</a></li>
  {% endfor %}
</ul>
{% endif %}
</body>
</html>
"""

def get_db_connection():
    conn = sqlite3.connect('gotuljosaskra.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/', defaults={'table_name': None})
@app.route('/<table_name>')
def show_table(table_name):
    conn = get_db_connection()
    cur = conn.cursor()
    if table_name is None:
        # Fetch and display a list of all tables
        cur.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = [row[0] for row in cur.fetchall()]
        conn.close()
        return render_template_string(HTML_TEMPLATE, tables=tables)
    else:
        # Display specific table data
        try:
            cur.execute(f'SELECT * FROM {table_name}')
        except sqlite3.OperationalError:
            conn.close()
            abort(404)  # Table not found, return 404
        rows = cur.fetchall()
        columns = [description[0] for description in cur.description]
        conn.close()
        return render_template_string(HTML_TEMPLATE, rows=rows, columns=columns, table_name=table_name)

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=3500)