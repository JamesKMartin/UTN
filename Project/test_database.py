import sys
from users import User,AdminUser
import seats
from database import UserSeatDatabase


"""Define TestSeats, TestUser, TestDatabase"""
seat1 = seats.Seat('4A', False)
seat2 = seats.Seat('4B', False)
seat3 = seats.Seat('4C', False)
user4 = User (5, 'test', 'Test', 'passwort123')

db = UserSeatDatabase("two.db")

def test_database():
    db.create_database()
    db.insert_seat(seat1)
    db.insert_seat(seat2)
    db.insert_seat(seat3)
    db.insert_user(user4)

    db.update_reservation('4A', db.user2.userID)
    db.update_reservation('4B', db.user2.userID)

    print(db.get_user_reservations(db.user2.userID))
    db.update_cancellation('4B', db.admin1)
    print(db.get_user_reservations(db.user2.userID))
    print(db.get_seat_reservations('4A'))


try:
    test_database()

except:
    print("Error %s:" % sys.exc_info()[0])
    sys.exit(1)

finally:
    if db.connection:
        db.connection.close()
