from flask import Flask, render_template, request, redirect
from users import User,AdminUser
import db

user = None

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home():
	data = []
	flights = []
	searched = False
	result = ""
	if request.method == "POST":
		if "logout" in request.form:
			global user
			user = None
		if "from" in request.form:
			if request.form["from"] != "" or request.form["to"] != "" or request.form["Departure"] != "":
				try:
					flights = db.query_data("SELECT * FROM flights WHERE start = '{}' OR destination = '{}' OR date = '{}'".format(request.form["from"], request.form["to"], request.form["Departure"]))
					searched = True
				except BaseException as e:
					result = "Some Error ocurred"
					print(e)
		if "order" in request.form:
			if request.form["order"] != "" and user != None:
				flight = request.form["order"].split(":")
				for f in flight:
					arr = f.split(',')
					for seats in range(1, len(arr)):
						try:
							db.insert_data("INSERT INTO seats (seat_from_flight, seat_number, reserved_by) VALUES (?, ?, ?)", (arr[0], arr[seats], int(user.getID())))
							result = "Reservation successful"
						except BaseException as e:
							result = "Some Error ocurred"
							print(e)
			else:
				result="Not logged in"	
						
	try:
		if not searched:
			flights = db.query_data("SELECT * FROM flights")
		for flight in range(len(flights)):
			seats = []
			planedata = db.query_data("SELECT * FROM planes WHERE planeID = {}".format(flights[flight][1]))
			seats_reservated = db.query_data("SELECT * FROM seats WHERE seat_from_flight = {}".format(flights[flight][0]))
			for seat in seats_reservated:
				seats.append(seat[1])
			seats_remaining = int(planedata[0][1]) * int(planedata[0][2]) - len(seats_reservated)
			data.append((flight, flights[flight][0], flights[flight][2], flights[flight][3], flights[flight][4], int(flights[flight][5]), flights[flight][6], flights[flight][7], int(flights[flight][8]), seats_remaining, int(planedata[0][1]), int(planedata[0][2]), seats))
	except BaseException as e:
		data = "Some Error ocurred"
		print(e)
	loggedIn = False
	username = ""
	if user != None:
		loggedIn = True
		username = user.getUsername()
	return render_template('index.html', data=data, loggedIn=loggedIn, username=username, result=result)
	
@app.route('/login', methods=['GET', 'POST'])
def login():
	if request.method == "POST":
	        try:
	        	query = db.query_data("SELECT * FROM users WHERE user_name = '{}'".format(request.form["username"]))
	        	if str(query[0][4]) == str(request.form["password"]):
	        		data = "Successful"
	        		global user
	        		user = User(query[0][0], query[0][1], query[0][2], query[0][3], query[0][4])
	        		return redirect("/")
	        	else:
	        		data = "Wrong password"
	        except BaseException as e:
	        	data = "No user with this username"
	        	print(e)
	        return render_template('login.html', data=[data])
	return render_template('login.html', data=[])
		
@app.route('/register', methods=['GET', 'POST'])
def register():
	if request.method == 'POST':
		usernames = []
		for user in db.query_data("SELECT user_name FROM users"):
			usernames.append(user[0])
		if request.form["username"] not in usernames:
			if request.form["password"] == request.form["passwordrepeat"]:
				db.insert_data("INSERT INTO users (name, user_name, email, passwort, is_admin) VALUES (?, ?, ?, ?, ?)", (request.form["name"], request.form["username"], request.form["email"], str(request.form["password"]), 0))
				result = "Successful"
			else:
				result = "The Passwords are not the same"
		else:
			data = "Username already taken"
		return render_template('register.html', result=[result])
	return render_template('register.html', result=[])
	
@app.route('/admin', methods=['GET', 'POST'])
def admin():
	if request.method == "POST":
		global user
		if type(user) is AdminUser:
			try:	
				if "imported_filename" in request.form:
					with open(request.form["imported_filename"]) as f:
    						lines = f.readlines()
    						header = lines[0].replace('\n', '')
    						columnname = header.split('\t')
    						wrong_format = False
    						if columnname[0] == "PlaneID" and columnname[1] == "Company" and columnname[2] == "Start" and columnname[3] == "Destination" and columnname[4] == "Duration" and columnname[5] == "Date" and columnname[6] == "Time" and columnname[7] == "Prize":
    							wrong_format = True
    							for line in range(1, len(lines)):
    								column = lines[line].replace('\n', '').split('\t')
    								db.insert_data("INSERT INTO flights (planeid, company, start, destination, duration, date, time, prize_per_ticket) VALUES (?, ?, ?, ?, ?, ?, ?, ?)", (int(column[0]), column[1], column[2], column[3], int(column[4]), column[5], column[6], int(column[7])))
    						if columnname[0] == "Seat_height" and columnname[1] == "Seat_width":
    							wrong_format = True
    							for line in range(1, len(lines)):
    								column = lines[line].replace('\n', '').split('\t')
    								print(column)
	    							db.insert_data("INSERT INTO planes (seat_height, seat_width) VALUES (?, ?)", (int(column[0]), int(column[1])))
	    					if columnname[0] == "Seat_from_flight" and columnname[1] == "Seat_number" and columnname[2] == "Reserved_by":
	    						wrong_format = True
	    						for line in range(1, len(lines)):
    								column = lines[line].replace('\n', '').split('\t')
	    							db.insert_data("INSERT INTO seats (seat_from_flight, seat_number, reserved_by) VALUES (?, ?, ?)", (int(column[0]), column[1], int(column[2])))				
	    					if not wrong_format:
	    						result=["Wrong format"]
	    					else:
	    						result=["Successfully added the file to the database"]
	    						
				elif "planeid" not in request.form:
					for seat_cancelation in request.form:
						split = seat_cancelation.split('?')
						db.delete_data("DELETE FROM seats WHERE seat_from_flight = {} AND seat_number = '{}'".format(split[0], split[1]))
						result=["Successfully removed reservation"]
				else:
					if request.form["seat_height"] != "":
						db.insert_data("INSERT INTO planes (seat_height, seat_width) VALUES (?, ?)", (request.form["seat_height"], request.form["seat_width"]))
						result=["Successfully added a plane"]
					if request.form["planeid"] != "":
						for plane in db.query_data("SELECT planeID FROM planes"):
							if int(request.form["planeid"]) == int(plane[0]):
								db.insert_data("INSERT INTO flights (planeid, company, start, destination, duration, date, time, prize_per_ticket) VALUES (?, ?, ?, ?, ?, ?, ?, ?)", (request.form["planeid"], request.form["company"], request.form["start"], request.form["destination"], request.form["duration"], request.form["date"], request.form["time"], request.form["prize"]))
								result=["Successfully added a flight"]
								break
							else:
								result = ["No Plane with this ID exists"]
			except BaseException as e:
				result = ["Somethings went wrong"]
				print(e)
			planes = db.query_data("SELECT * FROM planes")
			flights = db.query_data("SELECT * FROM flights")
			seats = db.query_data("SELECT * FROM seats ORDER BY seat_from_flight DESC")
			return render_template('admin.html', planes=planes,flights=flights, result=[result], seats=seats)
		else:
			try:
				query = db.query_data("SELECT * FROM users WHERE user_name = '{}'".format(request.form["username"]))
				if query[0][4] == str(request.form["password"]) and query[0][5] == 1:
					planes = db.query_data("SELECT * FROM planes")
					flights = db.query_data("SELECT * FROM flights")
					seats = db.query_data("SELECT * FROM seats ORDER BY seat_from_flight DESC")
					user = AdminUser(query[0][0], query[0][1], query[0][2], query[0][3], query[0][4])
					return render_template('admin.html', planes=planes, flights=flights, seats=seats)	        		
				else:
					result = "Wrong password"
			except:
				result = "No user with this username"
			return render_template('adminlogin.html', result=[result])
	return render_template('adminlogin.html')
	
@app.route('/statistics', methods=['GET', 'POST'])
def stats():
	total_seats = 0
	flights= db.query_data("SELECT * FROM flights")
	for flight in flights:
		plane = db.query_data("SELECT * FROM planes WHERE planeID = {}".format(flight[1]))
		total_seats += plane[0][1]*plane[0][2]


	remaining_seats = db.query_data("SELECT * FROM seats")
	free_seats = total_seats - len(remaining_seats)

	# Statistics
	
  	#total_seats = 20
	Users_System= 15
	
	
	free_perecent	= (free_seats/total_seats)*100
	remaining_percent = (len(remaining_seats)/total_seats)*100

	#Leute

	headings= ("Name", "Spitzname",  "Email" )
	data = []
	for user in remaining_seats:
		user2 = db.query_data("SELECT name, user_name, email FROM users WHERE userID = '{}'".format(user[2]))[0]
		isIn = False
		if user2 not in data:
			data.append(user2)
	
	return render_template('statistics.html', free_seats=free_seats,total_seats=total_seats,free_perecent=free_perecent,remaining_percent=remaining_percent,headings=headings, data=data)


@app.route('/help', methods=['GET', 'POST'])
def help():
	return render_template('help.html')

@app.route('/reservation', methods=['GET', 'POST'])
def reservation():
	if user != None:
		data = db.query_data("SELECT * FROM seats WHERE reserved_by = {}".format(user.getID()))
		if len(data) != 0:
			f = db.query_data("SELECT * FROM flights WHERE flightID = {}".format(data[0][0]))
			p = db.query_data("SELECT * FROM planes WHERE planeID = {}".format(f[0][1]))
			seats_reservated = db.query_data("SELECT * FROM seats WHERE seat_from_flight = {} AND reserved_by = {}".format(data[0][0], user.getID()))
			seats = []
			for seat in seats_reservated:
				seats.append(seat[1])
			flights = [[f[0][0], f[0]+p[0]+tuple([seats])]]
			for item in data:
				isIn = None
				for flight in range(len(flights)):
					if item[0] in flights[flight]:
						isIn = flight
				if isIn != None:
					flights[isIn].append(item[1])
				else:
					f = db.query_data("SELECT * FROM flights WHERE flightID = {}".format(item[0]))
					p = db.query_data("SELECT * FROM planes WHERE planeID = {}".format(f[0][1]))
					seats_reservated = db.query_data("SELECT * FROM seats WHERE seat_from_flight = {} AND reserved_by = {}".format(item[0], item[2]))
					seats = []
					for seat in seats_reservated:
						seats.append(seat[1])
					flights.append([item[0], f[0]+p[0]+tuple([seats]), item[1]])
			return render_template('reservation.html', data=flights, result=[])
	return render_template('reservation.html', data=[], result=["No reservations yet!"])
if __name__ == '__main__':
	db.initdatabase()
	app.run()

