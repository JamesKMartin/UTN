from flask import Flask, render_template, request
from users import User,AdminUser
import seats
import json
import sqlite3
from sqlite3 import Error

content = []

app = Flask(__name__)

conn = None

user = None

def create_connection(db_file):
	try:
		global conn
		conn = sqlite3.connect(db_file, check_same_thread=False)
		return conn
	except Error as e:
        	print(e)


def create_table(create_table_sql):
	try:
		c = conn.cursor()
		c.execute(create_table_sql)
	except Error as e:
		print(e)
		
def query_data(sql):
	cur = conn.cursor()
	cur.execute(sql)
	rows = cur.fetchall()
	return rows
	
def insert_data(sql, params):
	cur = conn.cursor()
	cur.execute(sql, params)
	

def initdatabase():
	database = r"database.db"
	
	create_connection(database)

	sql_create_flights_table = """CREATE TABLE IF NOT EXISTS flights (flightID integer PRIMARY KEY NOT NULL, planeid integer, company text, start text, destination text, duration integer, date text, time text, prize_per_ticket integer);"""

	sql_create_users_table = """CREATE TABLE IF NOT EXISTS users (userID integer PRIMARY KEY NOT NULL, name text, user_name text, email text, passwort text, is_admin boolean);"""
    
	sql_create_seats_table = """CREATE TABLE IF NOT EXISTS seats (seat_from_flight integer, seat_number text, is_reserved boolean, reserved_by integer);"""
	
	sql_create_plane_table = """CREATE TABLE IF NOT EXISTS planes (planeID integer PRIMARY KEY NOT NULL, seat_height integer, seat_width integer);"""

    # create tables
	if conn is not None:
		create_table(sql_create_flights_table)
		create_table(sql_create_users_table)
		create_table(sql_create_seats_table)
		create_table(sql_create_plane_table)
		insert_data("INSERT INTO users (name, user_name, email, passwort, is_admin) VALUES (?, ?, ?, ?, ?)", ('user_name','name', 'email','p', 1))
	else:
		print("Error! cannot create the database connection.")
	print(query_data("SELECT * FROM users"))

@app.route('/', methods=['GET', 'POST'])
def home():
	try:
		data = []
		flights = query_data("SELECT * FROM flights")
		for flight in range(len(flights)):
			planedata = query_data("SELECT * FROM planes WHERE planeID = {}".format(flights[flight][1]))
			seats_reservated = query_data("SELECT * FROM seats WHERE seat_from_flight = {}".format(flights[flight][0]))
			seats_remaining = int(planedata[0][1]) * int(planedata[0][2]) - len(seats_reservated)
			
			print(flights[flight])
			data.append((flight, flights[flight][0], flights[flight][2], flights[flight][3], flights[flight][4], int(flights[flight][5]), flights[flight][6], flights[flight][7], int(flights[flight][8]), seats_remaining, int(planedata[0][1]), int(planedata[0][2])))
		print(data)
	except:
		data = []
	return render_template('index.html', data=data)
	
@app.route('/login', methods=['GET', 'POST'])
def login():
	if request.method == "POST":
	        try:
	        	query = query_data("SELECT * FROM users WHERE user_name = {}".format(request.form["username"]))
	        	if query[0][3] == request.form["password"]:
	        		data = "Successfull"
	        		user = User(query[0][0], query[0][1], query[0][2], query[0][3], query[0][4])
	        	else:
	        		data = "Falsches Passwort"
	        except:
	        	data = "Kein Nutzer mit diesem Namen"
	        return render_template('login.html', data=[data])
	return render_template('login.html', data=[])
	
@app.route('/register', methods=['GET', 'POST'])
def register():
	if request.method == 'POST':
		if request.form["username"] not in query_data("SELECT user_name FROM users"):
			if request.form["password"] == request.form["passwordrepeat"]:
				insert_data("INSERT INTO users (name, user_name, email, passwort, is_admin) VALUES (?, ?, ?, ?, ?)", (request.form["name"], request.form["username"], request.form["email"], request.form["password"], 0))
				data = "Successfull"
			else:
				data = "The Passwords are not the same"
		else:
			data = "Username already taken"
		return render_template('register.html', data=[data])
	return render_template('register.html', data=[])
	
@app.route('/admin', methods=['GET', 'POST'])
def admin():
	if request.method == "POST":
		global user
		if user != None:
			try:	
				if request.form["seat_height"] != "":
					insert_data("INSERT INTO planes (seat_height, seat_width) VALUES (?, ?)", (request.form["seat_height"], request.form["seat_width"]))
					result=["Successfully added a plane"]
				if request.form["planeid"] != "":
					for plane in query_data("SELECT planeID FROM planes"):
						if int(request.form["planeid"]) == int(plane[0]):
							insert_data("INSERT INTO flights (planeid, company, start, destination, duration, date, time, prize_per_ticket) VALUES (?, ?, ?, ?, ?, ?, ?, ?)", (request.form["planeid"], request.form["company"], request.form["start"], request.form["destination"], request.form["duration"], request.form["date"], request.form["time"], request.form["prize"]))
							result=["Successfully added a flight"]
							break
						else:
							result = ["No Plane with this ID exists"]
			except:
				result = ["Somethings went wrong"]
			db = [query_data("SELECT * FROM planes"), query_data("SELECT * FROM flights")]
			print(db)
			return render_template('admin.html', data=db+[result])
		else:
			try:
				query = query_data("SELECT * FROM users WHERE user_name = {}".format(request.form["username"]))
				if query[0][4] == request.form["password"] and query[0][5] == 1:
					db = [query_data("SELECT * FROM planes"), query_data("SELECT * FROM flights")]
					user = AdminUser(query[0][0], query[0][1], query[0][2], query[0][3], query[0][4])
					return render_template('admin.html', data=db)	        		
				else:
					data = "Falsches Passwort"
			except:
				data = "Kein Nutzer mit diesem Namen"
			return render_template('adminlogin.html', data=[data])
	return render_template('adminlogin.html')
	
@app.route('/statistics', methods=['GET', 'POST'])
def stats():
	return render_template('statistics.html')

@app.route('/help', methods=['GET', 'POST'])
def help():
	return render_template('help.html')

if __name__ == '__main__':
	initdatabase()
	print(str(content))
	app.run()

