from flask import Flask, render_template, json, redirect, request
from flask_mysqldb import MySQL
from flask import request
import os
import database.db_connector as db

app = Flask(__name__)
db_connection = db.connect_to_database()
db_connection.ping(True)


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

#####################
### Driver Routes ###
#####################
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
    # else:
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
    

#############################
### Driver Rentals Routes ###
#############################
@app.route('/Drivers_Rentals')
def drivers_rentals():
    return render_template('drivers_rentals.j2')
    

######################
### Rentals Routes ###
######################
@app.route('/Rentals', methods=["POST","GET"])
def rentals():
    querySearch = "SELECT location_id, address, city FROM Locations;"
    cursor = db.execute_query(db_connection=db_connection, query=querySearch)
    searchResultsLoc = cursor.fetchall()
    querySearch2 = "SELECT car_id, make, model, color, vin FROM Cars;"
    cursor = db.execute_query(db_connection=db_connection, query=querySearch2)
    searchResultsCar = cursor.fetchall()
    if request.method == "POST":
        if request.form.get("add_rental"):
            location_input = request.form["location"]
            car_input = request.form["car"]
            rental_time_input = request.form["rental_time"] + ":00"
            rental_date_input = request.form["rental_date"]
            pickup_time_input = request.form["pickup_time"] + ":00"
            pickup_date_input = request.form["pickup_date"]
            return_time_input = request.form["return_time"] + ":00"
            return_date_input = request.form["return_date"]
            payment_input = request.form["payment"]
            status_input = request.form["status"]
            penalties_input = request.form["penalties"]
            cost_input = request.form["cost"]
            query_parameters = [location_input,car_input,rental_time_input,rental_date_input,pickup_time_input,pickup_date_input,return_time_input,return_date_input,payment_input,status_input,penalties_input,cost_input]
            print(rental_date_input, rental_time_input)
            query = "INSERT INTO Rentals (location_id, car_id, rental_time, rental_date, pickup_time, pickup_date, return_time, return_date, payment_type, current_status, total_penalties, total_cost) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"
            cursor = db.execute_query(db_connection=db_connection, query=query, query_params=query_parameters)
            return redirect("/Rentals")
        elif request.form.get("search_rental"):
            rental_date_input = request.form["rental_date"]
            query = "SELECT * FROM Rentals WHERE rental_date = %s;"
            cursor = db.execute_query(db_connection=db_connection, query=query, query_params=[rental_date_input])
            results = cursor.fetchall()
            return render_template('rentals.j2', Rentals=results, locations=searchResultsLoc, cars=searchResultsCar)
    # else:
    query = "SELECT * FROM Rentals;"
    cursor = db.execute_query(db_connection=db_connection, query=query)
    results = cursor.fetchall()
    return render_template('rentals.j2', Rentals=results, locations=searchResultsLoc, cars=searchResultsCar)


@app.route('/Rentals/update/<int:id>')
def rentals_update():
    return render_template('rentals.j2')


@app.route('/Rentals/delete/<int:id>')
def rentals_delete():
    return redirect('/Rentals')


###################
### Cars Routes ###
###################
@app.route('/Cars', methods=["POST", "GET"])
def cars():
    querySearch = "SELECT location_id, address, city FROM Locations;"
    cursor = db.execute_query(db_connection=db_connection, query=querySearch)
    searchResults = cursor.fetchall()
    querySearch = "SELECT make FROM Cars;"
    cursor = db.execute_query(db_connection=db_connection, query=querySearch)
    searchResultsMake = cursor.fetchall()
    if request.method == "POST":
        if request.form.get("add_car"):
            location_input = request.form["location"]
            make_input = request.form["make"]
            model_input = request.form["model"]
            year_input = request.form["year"]
            body_input = request.form["body_type"]
            price_input = request.form["price"]
            color_input = request.form["color"]
            plate_input = request.form["plate"]
            vin_input = request.form["vin"]
            mileage_input = request.form["mileage"]
            availability_input = request.form["availability"]
            query_parameters = [location_input,make_input,model_input,year_input,body_input,price_input,color_input,plate_input,vin_input,mileage_input,availability_input]

            query = "INSERT INTO Cars (location_id, make, model, year, car_body_type, daily_price, color, license_plate_num, vin, current_mileage, current_availability) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"
            cursor = db.execute_query(db_connection=db_connection, query=query, query_params=query_parameters)
            return redirect("/Cars")
        elif request.form.get("search_car_make"):
            make_input = request.form["make"]
            query = "SELECT * FROM Cars WHERE make = %s;"
            cursor = db.execute_query(db_connection=db_connection, query=query, query_params=[make_input])
            results = cursor.fetchall()
            return render_template('cars.j2', Cars=results, locations=searchResults, makes=searchResultsMake)
        elif request.form.get("search_car_availability"):
            availability_input = request.form["availability"]
            query = "SELECT * FROM Cars WHERE current_availability = %s;"
            cursor = db.execute_query(db_connection=db_connection, query=query, query_params=[availability_input])
            results = cursor.fetchall()
            return render_template('cars.j2', Cars=results, locations=searchResults, makes=searchResultsMake)
    # else:
    query = "SELECT * FROM Cars;"
    cursor = db.execute_query(db_connection=db_connection, query=query)
    results = cursor.fetchall()
    return render_template('cars.j2', Cars=results, locations=searchResults, makes=searchResultsMake)


@app.route('/Cars/update/<int:id>', methods=["POST","GET"])
def cars_update(id):
    querySearch = "SELECT location_id, address, city FROM Locations;"
    cursor = db.execute_query(db_connection=db_connection, query=querySearch)
    searchResults = cursor.fetchall()
    if request.method == "POST":
        if request.form.get("update_car"):
            location_input = request.form["location"]
            make_input = request.form["make"]
            model_input = request.form["model"]
            year_input = request.form["year"]
            body_input = request.form["body_type"]
            price_input = request.form["price"]
            color_input = request.form["color"]
            plate_input = request.form["plate"]
            vin_input = request.form["vin"]
            mileage_input = request.form["mileage"]
            availability_input = request.form["availability"]
            query_parameters = [location_input,make_input,model_input,year_input,body_input,price_input,color_input,plate_input,vin_input,mileage_input,availability_input]
            query_parameters.append(id)

            query = "UPDATE Cars SET Cars.location_id = %s, Cars.make = %s, Cars.model = %s, Cars.year = %s, Cars.car_body_type = %s, Cars.daily_price = %s, Cars.color = %s, Cars.license_plate_num = %s, Cars.vin = %s, Cars.current_mileage = %s, Cars.current_availability = %s WHERE Cars.car_id = %s"
            cursor = db.execute_query(db_connection=db_connection, query=query, query_params=query_parameters)
            
        return redirect("/Cars")
    else:
        query = "SELECT * FROM Cars WHERE car_id = %s;"
        cursor = db.execute_query(db_connection=db_connection, query=query, query_params=[id])
        results = cursor.fetchall()
        body_types = ["Sedan", "Coupe", "SUV", "Minivan"]
        return render_template('cars_update.j2', car=results[0], locations=searchResults, body_types=body_types)


@app.route('/Cars/delete/<int:id>')
def cars_delete(id):
    query = "DELETE FROM Cars WHERE car_id = %s;"
    cursor = db.execute_query(db_connection=db_connection, query=query, query_params=[id])
    return redirect('/Cars')


########################
### Locations Routes ###
########################
@app.route('/Locations', methods=["POST","GET"])
def locations():
    querySearch = "SELECT city FROM Locations;"
    cursor = db.execute_query(db_connection=db_connection, query=querySearch)
    searchResults = cursor.fetchall()
    if request.method == "POST":
        if request.form.get("add_location"):
            address_input = request.form["address"]
            city_input = request.form["city"]
            state_input = request.form["state"]
            zipcode_input = request.form["zipcode"]
            qty_input = request.form["qty"]
            query_parameters = [address_input,city_input,state_input,zipcode_input,qty_input]
            query = "INSERT INTO Locations (address, city, state, zipcode, num_cars) VALUES (%s, %s, %s, %s, %s);"
            cursor = db.execute_query(db_connection=db_connection, query=query, query_params=query_parameters)
            return redirect("/Locations")

        elif request.form.get("search_location"):
            city_input = request.form["city"]
            query = "SELECT * FROM Locations WHERE city = %s;"
            cursor = db.execute_query(db_connection=db_connection, query=query, query_params=[city_input])
            results = cursor.fetchall()
            return render_template('locations.j2', Locations=results, cities=searchResults)
            
    query = "SELECT * FROM Locations;"
    cursor = db.execute_query(db_connection=db_connection, query=query)
    results = cursor.fetchall()
    return render_template('locations.j2', Locations=results, cities=searchResults)


@app.route('/Locations/update/<int:id>', methods=["POST", "GET"])
def locations_update(id):
    if request.method == "POST":
        if request.form.get("update_location"):
            address_input = request.form["address"]
            city_input = request.form["city"]
            state_input = request.form["state"]
            zipcode_input = request.form["zipcode"]
            qty_input = request.form["qty"]
            query_parameters = [address_input,city_input,state_input,zipcode_input,qty_input]
            query_parameters.append(id)

            query = "UPDATE Locations SET Locations.address = %s, Locations.city = %s, Locations.state = %s, Locations.zipcode = %s, Locations.num_cars = %s WHERE Locations.location_id = %s"
            cursor = db.execute_query(db_connection=db_connection, query=query, query_params=query_parameters)
            
        return redirect("/Locations")
    else:
        query = "SELECT * FROM Locations WHERE location_id = %s;"
        cursor = db.execute_query(db_connection=db_connection, query=query, query_params=[id])
        results = cursor.fetchall()
        return render_template('locations_update.j2', location=results[0])


@app.route('/Locations/delete/<int:id>')
def locations_delete(id):
    query = "DELETE FROM Locations WHERE location_id = %s;"
    cursor = db.execute_query(db_connection=db_connection, query=query, query_params=[id])
    return redirect("/Locations")


# Listener
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 10293))
    #Start the app on port 3000, it will be different once hosted
    app.run(port=port, debug=True)