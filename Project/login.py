def signup():
 users = open("users.txt", "a")
 email = input("Enter email address: ")
 users.write(email + " ")
 users.close()
 pwd = input("Enter password: ")
 userpwd = open("userpwd.txt", "a")
 userpwd.write(pwd + " ")
 userpwd.close()
 con_pwd = input("Confirm password: ")
 if con_pwd == pwd:
   print("You have registered successfully!")
 else: print("Passwords don't match!")
def login():
     email = input("Enter email: ")
     pwd = input("Enter password: ")
     if email == "gogo" and pwd == "gaga":
          print("Logged in Successfully!")
     else:
          print("Login failed! \n")
while 1:
    print("********** Login System **********")
    print("1.Signup")
    print("2.Login")
    print("3.Exit")
    ch = int(input("Enter your choice: "))
    if ch == 1:
        signup()
    elif ch == 2:
        login()
    elif ch == 3:
        break
    else:
        print("Please input 1, 2 or 3!")