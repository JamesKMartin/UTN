import sqlite3
from sqlite3 import Error

def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)

    return conn


def execute_command(conn, create_table_sql):
    """ create a table from the create_table_sql statement
    :param conn: Connection object
    :param create_table_sql: a CREATE TABLE statement
    :return:
    """
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)


def main():
    database = r"database.db"

    sql_create_flights_table = """CREATE TABLE IF NOT EXISTS flights (flightID text, company text, start text, destination text, duration integer, date text, time text, prize_per_ticket integer);"""

    sql_create_users_table = """CREATE TABLE IF NOT EXISTS users (userID integer, name text, user_name text, passwort text);"""
    
    sql_create_seats_table = """CREATE TABLE IF NOT EXISTS seats (seat_from_flight text, seat_number text, is_reserved blob, reserved_by integer);"""

    # create a database connection
    conn = create_connection(database)

    # create tables
    if conn is not None:
        execute_command(conn, sql_create_flights_table)
        execute_command(conn, sql_create_users_table)
        execute_command(conn, sql_create_seats_table)
    else:
        print("Error! cannot create the database connection.")

