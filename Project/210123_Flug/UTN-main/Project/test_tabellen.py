from flask import Flask, render_template, request
from users import User,AdminUser
import seats
import json
import sqlite3
from sqlite3 import Error

app = Flask(__name__)

@app.route('/statistics', methods=['GET', 'POST'])
def statistics():
    
	# database query to retrieve statistics information
	
	free_seats = 10
	total_seats = 25
	Users_System= 15
	
	headings= ("Name", "Spitzame",  "Email" )
	data = (
		( "Rolf",  "Rolfi", "rolf@gmx.de"),
		( "Amelie",  "Amy", "amy@freenet.de"),
		( "Rolf",  "Rolfi", "rolf@gmx.de"),
	)
	remaining_seats = total_seats - free_seats
	free_perecent	= (free_seats/total_seats)*100
	remaining_percent = (remaining_seats/total_seats)*100
	
	return render_template('tabelle.html',headings=headings, data=data )