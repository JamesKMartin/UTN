from flask import Flask, render_template
import sqlite3

app = Flask(__name__)

@app.route('/users')
def users():
    # Connect to the database
    conn = sqlite3.connect('database.py')
    c = conn.cursor()

    # Fetch data from the database
    c.execute("SELECT * FROM users")
    data = c.fetchall()

    # Close the connection
    conn.close()

    # Render the data in the template
    return render_template('statistic.html', users=data)

if __name__ == '__main__':
    app.run(debug=True)