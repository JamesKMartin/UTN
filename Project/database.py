import sqlite3
import sys
from users import User,AdminUser
import seat

#class UserSeatDatabase ():

"""creates 4 users already of whom one is a admin user"""
user1 = User(1, 'elms', 'Elmo', 'passwort123')
user2 = User(2, 'kleinerTim', 'Timmy', 'abrakadabra')
user3 = User(3, 'pizza', 'Hungry Person', 'pizza')
admin1 = AdminUser(4, 'rosa', 'Rosa', 'suchagoodpasswort')

#---------CREATE DATABASE AND CHANGE FILETYPE -------------

def make_connection(database_file, query):
    '''
    Common connection function that will fetch data with a given query in a specific DB
    The cursor will be closed at the end of it
    '''
    connection = sqlite3.connect(database_file)
    cursor = connection.cursor()
    cursor.execute(query)  # if id is available here we can also use    cursor.execute(query, [person_id])
    results = cursor.fetchall()
    cursor.close()
    connection.close()
    return results

def create_database(file):
    """
    turns given .txt or json file into sql file
    """

    """scan given Seats and checks which one is displayed as X, sets value of is_reserved True in that case"""
    """inserts 4 users already of whom one is a admin user"""
    pass

def create_json():
    """
    turns sql file into json file
    """
    pass

def create_users():
    """
    creates a table which is seperated from the seatRegistration to store Login data
    """
    with connection:
        cursor.execute("""CREATE TABLE users (userID integer, name text, user_name text, passwort text)""")


def create_seats():
    """
    creates a table to display which seat is taken by which user
    """
    with connection:
        cursor.execute("""CREATE TABLE seats (seat_number text, is_reserved blob, reserved_by integer)""")


#--------------------------INSERT IN DATABASE--------------------

def insert_user(user):
    with connection:
        cursor.execute("INSERT INTO users VALUES (:userID, :name, :user_name, :passwort)", {'userID': user.userID,
                                                                                  'name': user.user_name,
                                                                                  'user_name': user.name,
                                                                                  'passwort': user.passwort})

def insert_seat(seat):
    with connection:
        cursor.execute("INSERT INTO seats VALUES (:seat_number, :is_occupied, :reserved_by)", {'seat_number': seat.seat_number,
                                                                                 'is_occupied': seat.is_occupied,
                                                                                 'reserved_by': None})

#--------------------------UPDATE DATABASE-----------------------

def update_reservation(number, userID):
    cursor.execute("""SELECT is_reserved FROM seats WHERE seat_number = :seat_number """,
                  {'seat_number': number})
    # only reserve a seat if not reserved yet
    if (cursor.fetchone()[0] == False):
        with connection:
            cursor.execute("""UPDATE seats SET reserved_by = :reserved_by
                        WHERE seat_number = :seat_number """,
                      {'seat_number': number, 'reserved_by': userID})
            cursor.execute("""UPDATE seats SET is_reserved = :is_reserved
                        WHERE seat_number = :seat_number """,
                      {'seat_number': number, 'is_reserved': True})
        # change is_reserved in seat itself
    else:
        print("You cannot reserve a seat that is already taken, please choose a free seat")



def update_cancellation(number, user):
    # check for Admin rights to cancel
    if (type(user) != AdminUser):
        print("You are not an Admin, you do not have the right to cancel a reservation")
        return

    cursor.execute("""SELECT is_reserved FROM seats WHERE seat_number = :seat_number """,
                  {'seat_number': number})
    # only reserve a seat if not reserved yet
    if(cursor.fetchone()[0] == True):
        with connection:
            cursor.execute("""UPDATE seats SET reserved_by = :reserved_by
                        WHERE seat_number = :seat_number """,
                      {'seat_number': number, 'reserved_by': None})
            cursor.execute("""UPDATE seats SET is_reserved = :is_reserved
                        WHERE seat_number = :seat_number """,
                      {'seat_number': number, 'is_reserved': False})
        # change is_reserved in seat itself
    else:
        print("You did choose a seat that is currently not reserved, please try another seat number")

def update_user_passwort(user):
    with connection:
        cursor.execute("""UPDATE users SET passwort = :passwort
                    WHERE userID = :userID """,
                  {'userID': user.userID, 'passwort': user.passwort})

def remove_user(user):
    with connection:
        cursor.execute("DELETE from users WHERE userID = :userID",
                  {'userID': user.userID})


#------------------------GETTER-----------------------------

def get_user_reservations(userID):
    """
    returns the seat numbers a user reserved
    """
    cursor.execute("SELECT * FROM seats WHERE reserved_by=:reserved_by", {'reserved_by': userID})
    return cursor.fetchall()

def get_seat_reservations(number):
    """
    returns which user reserved a specific seat
    """
    cursor.execute("SELECT * FROM seats WHERE seat_number=:seat_number", {'seat_number': number})
    return cursor.fetchone()[2]



"""Define TestSeats"""
seat1 = seat.Seat('4A', False)
seat2 = seat.Seat('4B', False)
seat3 = seat.Seat('4C', False)


try:
    connection = sqlite3.connect("our.db")
    cursor = connection.cursor()

    """
    create_users()
    create_seats()
    
    insert_seat(seat1)
    insert_seat(seat2)
    insert_seat(seat3)
    insert_user(user1)
    insert_user(user2)
    insert_user(user3)
    insert_user(admin1)
    update_reservation('4A', user2.userID)
    update_reservation('4B', user2.userID)
    print(get_user_reservations(user2.userID))
    update_cancellation('4B', admin1)
    print(get_user_reservations(user2.userID))
    print(get_seat_reservations('4A'))
    """

except:
    print("Error %s:" % sys.exc_info()[0])
    sys.exit(1)
finally:
    if connection:
        connection.close() # after we are done, we should close the connection with the database, always.