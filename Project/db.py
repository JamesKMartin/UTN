import sqlite3
from sqlite3 import Error

conn = None

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
	conn.commit()
	
def delete_data(sql):
	cur = conn.cursor()
	cur.execute(sql)
	conn.commit()

def initdatabase():
	database = r"database.db"
	
	create_connection(database)

	sql_create_flights_table = """CREATE TABLE IF NOT EXISTS flights (flightID integer PRIMARY KEY NOT NULL, planeid integer, company text, start text, destination text, duration integer, date text, time text, prize_per_ticket integer);"""

	sql_create_users_table = """CREATE TABLE IF NOT EXISTS users (userID integer PRIMARY KEY NOT NULL, name text, user_name text, email text, passwort text, is_admin boolean);"""
    
	sql_create_seats_table = """CREATE TABLE IF NOT EXISTS seats (seat_from_flight integer, seat_number text, reserved_by integer);"""
	
	sql_create_plane_table = """CREATE TABLE IF NOT EXISTS planes (planeID integer PRIMARY KEY NOT NULL, seat_height integer, seat_width integer);"""

    # create tables
	if conn is not None:
		create_table(sql_create_flights_table)
		create_table(sql_create_users_table)
		create_table(sql_create_seats_table)
		create_table(sql_create_plane_table)
		if len(query_data("SELECT * FROM users")) == 0:
			insert_data("INSERT INTO users (name, user_name, email, passwort, is_admin) VALUES (?, ?, ?, ?, ?)", ('name','username', 'email','p', 1))

	else:
		print("Error! cannot create the database connection.")
