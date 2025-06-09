from flask import Flask, render_template
import mysql.connector

app = Flask(__name__)

# Connect to the MySQL database on management1 server
db_connection = mysql.connector.connect(
    host='localhost',
    user='root',
    password='shruti3108',
    database='cool'
)

@app.route('/')
def index():
    # Retrieve column names from MySQL database
    cursor = db_connection.cursor()
    cursor.execute("SHOW COLUMNS FROM urls")
    columns = [column[0] for column in cursor.fetchall()]
    print("Columns:", columns)  # Print column names for debugging

    # Retrieve data from MySQL database
    cursor.execute("SELECT * FROM urls")
    data = cursor.fetchall()

    # Close cursor and database connection
    cursor.close()
    db_connection.close()

    # Render HTML template with data and column names
    return render_template('index_mysql.html', data=data, columns=columns)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
