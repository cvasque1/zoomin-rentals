from flask import Flask, render_template, json, redirect
from flask_mysqldb import MySQL
from flask import request
import os

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'classmysql.engr.oregonstate.edu'
app.config['MYSQL_USER'] = 'cs340_vasqucar'
app.config['MYSQL_PASSWORD'] = '0054' #last 4 of onid
app.config['MYSQL_DB'] = 'cs340_vasqucar'
app.config['MYSQL_CURSORCLASS'] = "DictCursor"


mysql = MySQL(app)


# Routes
@app.route('/')
def root():
    return render_template('index.j2')


@app.route('/Rentals')
def rentals():
    return render_template('rentals.j2')


@app.route('/Cars')
def cars():
    return render_template('cars.j2')


@app.route('/Drivers')
def drivers():
    return render_template('drivers.j2')


@app.route('/Drivers_Rentals')
def drivers_rentals():
    return render_template('drivers_rentals.j2')


@app.route('/Locations')
def locations():
    return render_template('locations.j2')


# @app.route('/')
# def

# Listener
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 10293))
    #Start the app on port 3000, it will be different once hosted
    app.run(port=port, debug=True)