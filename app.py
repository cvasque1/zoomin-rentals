from flask import Flask, render_template, json, redirect, request
from flask_mysqldb import MySQL
from flask import request
import os
import database.db_connector as db

db_connection = db.connect_to_database()
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


@app.route('/Drivers', methods=["POST", "GET"])
def drivers():
    if request.method == "POST":
        if request.form.get("add_driver"):
            first_name_input = request.form["first_name"]
            last_name_input = request.form["last_name"]
            email_input = request.form["email"]
            phone_input = request.form["phone"]
            street_input = request.form["street"]
            city_input = request.form["city"]
            state_input = request.form["state"]
            zipcode_input = request.form["zipcode"]
            query_parameters = [first_name_input,last_name_input,email_input,phone_input,street_input,city_input,state_input,zipcode_input]

            query = "INSERT INTO Drivers (first_name, last_name, email, phone, street, city, state, zipcode) VALUES (%s, %s, %s, %s, %s, %s, %s, %s);"
            cursor = db.execute_query(db_connection=db_connection, query=query, query_params=query_parameters)
            return redirect("/Drivers")

        elif request.form.get("search_driver"):
            last_name_input = request.form["last_name"]
            query = "SELECT * FROM Drivers WHERE last_name LIKE %s;"
            cursor = db.execute_query(db_connection=db_connection, query=query, query_params=(last_name_input + '%',))
            results = cursor.fetchall()
            return render_template('drivers.j2', Drivers=results)
        
    else:
        query = "SELECT * FROM Drivers;"
        cursor = db.execute_query(db_connection=db_connection, query=query)
        results = cursor.fetchall()
        return render_template('drivers.j2', Drivers=results)


@app.route('/Drivers/update/<int:id>', methods=["POST", "GET"])
def drivers_update(id):
    if request.method == "POST":
        if request.form.get("update_driver"):
            first_name_input = request.form["first_name"]
            last_name_input = request.form["last_name"]
            email_input = request.form["email"]
            phone_input = request.form["phone"]
            street_input = request.form["street"]
            city_input = request.form["city"]
            state_input = request.form["state"]
            zipcode_input = request.form["zipcode"]
            query_parameters = [first_name_input,last_name_input,email_input,phone_input,street_input,city_input,state_input,zipcode_input]
            query_parameters.append(id)

            query = "UPDATE Drivers SET Drivers.first_name = %s, Drivers.last_name = %s, Drivers.email = %s, Drivers.phone = %s, Drivers.street = %s, Drivers.city = %s, Drivers.state = %s, Drivers.zipcode = %s WHERE Drivers.driver_id = %s"
            cursor = db.execute_query(db_connection=db_connection, query=query, query_params=query_parameters)
            
        return redirect("/Drivers")
    else:
        query = "SELECT * FROM Drivers WHERE driver_id = %s;"
        cursor = db.execute_query(db_connection=db_connection, query=query, query_params=[id])
        results = cursor.fetchall()
        return render_template('drivers_update.j2', driver=results[0])


@app.route('/Drivers/delete/<int:id>')
def drivers_delete(id):
    query = "DELETE FROM Drivers WHERE driver_id = %s;"
    cursor = db.execute_query(db_connection=db_connection, query=query, query_params=[id])
    return redirect("/Drivers")
    

@app.route('/Drivers_Rentals')
def drivers_rentals():
    return render_template('drivers_rentals.j2')


@app.route('/Locations', methods=["POST", "GET"])
def locations():
    if request.method == "POST": #add location function
        if request.form.get("add_location"): #if the name of form is "add_location"
            address_input = request.form["address"]
            city_input = request.form["city"]
            state_input = request.form["state"]
            zip_input = request.form["zip_code"]
            num_cars_input = request.form["num_cars"]
            query_parameters = [address_input, city_input, state_input, zip_input, num_cars_input]

            query = "INSERT INTO Locations (address, city, state, zip_code, num_cars) VALUES (%s, %s, %s, %s, %s);"
            cursor = db.execute_query(db_connection=db_connection, query=query, query_params=query_parameters)
            return redirect("/Locations") #essentially a refresh at the end

    else: #otherwise just display all records into table
        query = "SELECT * FROM Locations;"
        cursor = db.execute_query(db_connection=db_connection, query=query)
        results = cursor.fetchall()
        return render_template('locations.j2', Locations=results)


@app.route('Locations/update/<int:id>', methods=["POST", "GET"])
def location_update(id):
    if request.method == "POST":
        if request.form.get("update_location")
            address_input = request.form["address"]
            city_input = request.form["city"]
            state_input = request.form["state"]
            zip_input = request.form["zip_code"]
            num_cars_input = request.form["num_cars"]
            query_parameters = [address_input, city_input, state_input, zip_input, num_cars_input]
            query_parameters.append(id)

            query = "UPDATE Locations SET Locations.address = %s, Locations.city = %s, Locations.state = %s, Locations.zip_code= %s, Locations.num_cars = %s WHERE Locations.location_id = %s"
            cursor = db.execute_query(db_connection=db_connection, query=query, query_params=query_parameters)

        return redirect("/Locations")

    else:
        query = "SELECT * From Locations WHERE location_id = %s"
        cursor = db.execute_query(db_connection=db_connection, query=query, query_params=[id])
        results = cursor.fetchall()
        return render_template('locations_update.j2', location=results[0])


@app.route('Locations/delete/<int:id>', methods=["POST","GET"])
def locations_delete(id):
    query = "DELETE from Locations WHERE location_id = %s"
    cursor = db.execute_query(db_connection=db_connection, query=query, query_params=[id])
    return redirect("/Locations")







# @app.route('/')
# def

# Listener
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 10293))
    #Start the app on port 3000, it will be different once hosted
    app.run(port=port, debug=True)