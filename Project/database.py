import sqlite3
import sys
from users import User,AdminUser
import seats

# Todo: programm make_connection more beautiful so the connection is closed after an action and the database is not open the whole time;
# Todo: Read the given .txt or json into a list for an easy change to .db
# Todo: Change the .db back to json if needed for an update
class UserSeatDatabase ():

    def __init__(self, filename):
        self.database_file = filename
        self.connection = sqlite3.connect(self.database_file)
        self.cursor = self.connection.cursor()

        # creates 4 users already of whom one is an admin user
        self.user1 = User(1, 'elms', 'Elmo', 'passwort123')
        self.user2 = User(2, 'kleinerTim', 'Timmy', 'abrakadabra')
        self.user3 = User(3, 'pizza', 'Hungry Person', 'pizza')
        self.admin1 = AdminUser(4, 'rosa', 'Rosa', 'suchagoodpasswort')

    #---------CREATE DATABASE AND CHANGE FILETYPE -------------

    def make_connection(self, query):
        '''
        Conncection funtion which will create a conncection and the database so the cursor can execute a given query
        '''

        with self.connection:
            self.cursor.execute(query)
        results = self.cursor.fetchall()

        return results

    def create_database(self):
        """
        turns given .txt or json file into sql file
        """
        self.create_users()
        self.create_seats()
        # scan given Seats and checks which one is displayed as X, sets value of is_reserved True in that case
        # inserts 4 users already of whom one is a admin user
        self.insert_user(self.user1)
        self.insert_user(self.user2)
        self.insert_user(self.user3)
        self.insert_user(self.admin1)

    def create_json(self):
        """
        turns sql file into json file
        """
        pass

    def create_users(self):
        """
        creates a table which is seperated from the seatRegistration to store Login data
        """
        query = "CREATE TABLE users (userID integer, name text, user_name text, passwort text)"
        self.make_connection(query)


    def create_seats(self):
        """
        creates a table to display which seat is taken by which user
        """
        query = "CREATE TABLE seats (seat_number text, is_reserved blob, reserved_by integer)"
        self.make_connection(query)

    #--------------------------INSERT IN DATABASE--------------------

    def insert_user(self, user):
        with self.connection:
            self.cursor.execute("INSERT INTO users VALUES (:userID, :name, :user_name, :passwort)", {'userID': user.userID,
                                                                                  'name': user.user_name,
                                                                                  'user_name': user.name,
                                                                                  'passwort': user.passwort})

    def insert_seat(self, seat):
       with self.connection:
           self.cursor.execute("INSERT INTO seats VALUES (:seat_number, :is_reserved, :reserved_by)", {'seat_number': seat.seat_number,
                                                                                 'is_reserved': seat.is_reserved,
                                                                                 'reserved_by': None})

    #--------------------------UPDATE DATABASE-----------------------

    def update_reservation(self, number, userID):
        self.cursor.execute("""SELECT is_reserved FROM seats WHERE seat_number = :seat_number """,
                  {'seat_number': number})
        # only reserve a seat if not reserved yet
        if (self.cursor.fetchone()[0] == False):
            with self.connection:
                self.cursor.execute("""UPDATE seats SET reserved_by = :reserved_by
                            WHERE seat_number = :seat_number """,
                          {'seat_number': number, 'reserved_by': userID})
                self.cursor.execute("""UPDATE seats SET is_reserved = :is_reserved
                            WHERE seat_number = :seat_number """,
                          {'seat_number': number, 'is_reserved': True})
            # change is_reserved in seat itself
        else:
            print("You cannot reserve a seat that is already taken, please choose a free seat")


    def update_cancellation(self, number, user):
        # check for Admin rights to cancel
        if (type(user) != AdminUser):
            print("You are not an Admin, you do not have the right to cancel a reservation")
            return

        self.cursor.execute("""SELECT is_reserved FROM seats WHERE seat_number = :seat_number """,
                      {'seat_number': number})
        # only reserve a seat if not reserved yet
        if(self.cursor.fetchone()[0] == True):
            with self.connection:
                self.cursor.execute("""UPDATE seats SET reserved_by = :reserved_by
                            WHERE seat_number = :seat_number """,
                          {'seat_number': number, 'reserved_by': None})
                self.cursor.execute("""UPDATE seats SET is_reserved = :is_reserved
                            WHERE seat_number = :seat_number """,
                          {'seat_number': number, 'is_reserved': False})
            # change is_reserved in seat itself
        else:
            print("You did choose a seat that is currently not reserved, please try another seat number")

    def update_user_passwort(self, user):
        query = ("""UPDATE users SET passwort = :passwort
                        WHERE userID = :userID """,
                      {'userID': user.userID, 'passwort': user.passwort})
        self.make_connection(query)

    def remove_user(self, user):
        query = ("DELETE from users WHERE userID = :userID",
                      {'userID': user.userID})
        self.make_connection(query)


    #------------------------GETTER-----------------------------

    def get_user_reservations(self, userID):
        """
        returns the seat numbers a user reserved
        """
        self.cursor.execute("SELECT * FROM seats WHERE reserved_by=:reserved_by", {'reserved_by': userID})
        return self.cursor.fetchall()

    def get_seat_reservations(self, number):
        """
        returns which user reserved a specific seat
        """
        self.cursor.execute("SELECT * FROM seats WHERE seat_number=:seat_number", {'seat_number': number})
        return self.cursor.fetchone()[2]

