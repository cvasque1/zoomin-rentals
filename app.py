from flask import Flask, render_template, json, redirect, request
from flask_mysqldb import MySQL
from flask import request
import os
import database.db_connector as db
from collections import defaultdict

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



############################
### Booking Agent Routes ###
############################
@app.route('/Booking_Agents', methods=["POST", "GET"])
def booking_agents():
    if request.method == "POST":
        if request.form.get("add_agent"):
            first_name_input = request.form["first_name"]
            last_name_input = request.form["last_name"]
            email_input = request.form["email"]
            query_parameters = [first_name_input,last_name_input,email_input]

            query = "INSERT INTO Booking_Agents (first_name, last_name, email) VALUES (%s, %s, %s);"
            cursor = db.execute_query(db_connection=db_connection, query=query, query_params=query_parameters)
            return redirect("/Booking_Agents")
        elif request.form.get("search_agent"):
            last_name_input = request.form["last_name"]
            query = "SELECT * FROM Booking_Agents WHERE last_name LIKE %s;"
            cursor = db.execute_query(db_connection=db_connection, query=query, query_params=(last_name_input + '%',))
            results = cursor.fetchall()
            return render_template('booking_agents.j2', Agents=results)
    # else:
    query = "SELECT * FROM Booking_Agents;"
    cursor = db.execute_query(db_connection=db_connection, query=query)
    results = cursor.fetchall()
    return render_template('booking_agents.j2', Agents=results)


@app.route('/Booking_Agents/update/<int:id>', methods=["POST", "GET"])
def booking_agents_update(id):
    if request.method == "POST":
        if request.form.get("update_agent"):
            first_name_input = request.form["first_name"]
            last_name_input = request.form["last_name"]
            email_input = request.form["email"]
            query_parameters = [first_name_input,last_name_input,email_input]
            query_parameters.append(id)

            query = "UPDATE Booking_Agents SET Booking_Agents.first_name = %s, Booking_Agents.last_name = %s, Booking_Agents.email = %s WHERE Booking_Agents.agent_id = %s"
            cursor = db.execute_query(db_connection=db_connection, query=query, query_params=query_parameters)
            
        return redirect("/Booking_Agents")
    
    query = "SELECT * FROM Booking_Agents WHERE agent_id = %s;"
    cursor = db.execute_query(db_connection=db_connection, query=query, query_params=[id])
    results = cursor.fetchall()
    return render_template('booking_agents_update.j2', agent=results[0])


@app.route('/Booking_Agents/delete/<int:id>')
def booking_agents_delete(id):
    query = "DELETE FROM Booking_Agents WHERE agent_id = %s;"
    cursor = db.execute_query(db_connection=db_connection, query=query, query_params=[id])
    return redirect("/Booking_Agents")
    
    

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
    querySearch3 = "SELECT driver_id, CONCAT(first_name,' ',last_name) AS name FROM Drivers;"
    cursor = db.execute_query(db_connection=db_connection, query=querySearch3)
    searchResultsDriver = cursor.fetchall()
    querySearch4 = "SELECT agent_id, CONCAT(first_name,' ',last_name) AS name FROM Booking_Agents;"
    cursor = db.execute_query(db_connection=db_connection, query=querySearch4)
    searchResultsAgent = cursor.fetchall()
    querySearch5 = "SELECT add_on_id, name FROM Add_Ons;"
    cursor = db.execute_query(db_connection=db_connection, query=querySearch5)
    searchResultsAddOn = cursor.fetchall()
    
    if request.method == "POST":
        if request.form.get("add_rental"):
            driver_input = request.form["driver"]
            location_input = request.form["location"]
            car_input = request.form["car"]
            agent_input = request.form["agent"]
            pickup_time_input = request.form["pickup_time"] + ":00"
            pickup_date_input = request.form["pickup_date"]
            return_time_input = request.form["return_time"] + ":00"
            return_date_input = request.form["return_date"]
            payment_input = request.form["payment"]
            cost_input = request.form["cost"]
            add_ons_input = request.form.getlist('add_ons')

            if agent_input == "none":
                query_parameters = [driver_input,location_input,car_input,None,pickup_time_input,pickup_date_input,return_time_input,return_date_input,payment_input,cost_input]
            else:
                query_parameters = [driver_input,location_input,car_input,agent_input,pickup_time_input,pickup_date_input,return_time_input,return_date_input,payment_input,cost_input]
            query = "INSERT INTO Rentals (driver_id, location_id, car_id, agent_id, pickup_time, pickup_date, return_time, return_date, payment_type, total_cost) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"
            cursor = db.execute_query(db_connection=db_connection, query=query, query_params=query_parameters)
            rentalID = cursor.lastrowid
            if len(add_ons_input) > 0:
                for add_on_input in add_ons_input:
                    query_parameters = [rentalID, add_on_input]
                    query = "INSERT INTO Rentals_Add_Ons (rental_id, add_on_id) VALUES (%s, %s);"
                    cursor = db.execute_query(db_connection=db_connection, query=query, query_params=query_parameters)
            return redirect("/Rentals")
        elif request.form.get("search_rental"):
            pickup_date_input = request.form["pickup_date"]
            query = "SELECT * FROM Rentals WHERE pickup_date = %s ORDER BY rental_id ASC;"
            cursor = db.execute_query(db_connection=db_connection, query=query, query_params=[pickup_date_input])
            resultsTable = cursor.fetchall()
            query = "SELECT Rentals_Add_Ons.rental_id, Add_Ons.name \
                FROM Rentals_Add_Ons \
                INNER JOIN Add_Ons ON Rentals_Add_Ons.add_on_id = Add_Ons.add_on_id \
                ORDER BY rental_id ASC;"
            cursor = db.execute_query(db_connection=db_connection, query=query)
            results = cursor.fetchall()
            intersections = defaultdict(list)
            for r in results:
                intersections[r['rental_id']].append(r['name'])

            return render_template('rentals.j2', Rentals=resultsTable, locations=searchResultsLoc, cars=searchResultsCar, drivers=searchResultsDriver, addOns=searchResultsAddOn, intersections=intersections)
    # else:
    query = "SELECT * FROM Rentals"
    cursor = db.execute_query(db_connection=db_connection, query=query)
    resultsTable = cursor.fetchall()
    query = "SELECT Rentals_Add_Ons.rental_id, Add_Ons.name \
        FROM Rentals_Add_Ons \
        INNER JOIN Add_Ons ON Rentals_Add_Ons.add_on_id = Add_Ons.add_on_id \
        ORDER BY rental_id ASC;"
    cursor = db.execute_query(db_connection=db_connection, query=query)
    results = cursor.fetchall()
    intersections = defaultdict(list)
    for r in results:
        intersections[r['rental_id']].append(r['name'])

    return render_template('rentals.j2', Rentals=resultsTable, locations=searchResultsLoc, cars=searchResultsCar, drivers=searchResultsDriver, agents=searchResultsAgent, addOns=searchResultsAddOn, intersections=intersections)


@app.route('/Rentals/update/<int:id>', methods=["POST", "GET"])
def rentals_update(id):
    querySearch = "SELECT location_id, address, city FROM Locations;"
    cursor = db.execute_query(db_connection=db_connection, query=querySearch)
    searchResultsLoc = cursor.fetchall()
    querySearch2 = "SELECT car_id, make, model, color, vin FROM Cars;"
    cursor = db.execute_query(db_connection=db_connection, query=querySearch2)
    searchResultsCar = cursor.fetchall()
    querySearch3 = "SELECT driver_id, CONCAT(first_name,' ',last_name) AS name FROM Drivers;"
    cursor = db.execute_query(db_connection=db_connection, query=querySearch3)
    searchResultsDriver = cursor.fetchall()
    querySearch4 = "SELECT agent_id, CONCAT(first_name,' ',last_name) AS name FROM Booking_Agents;"
    cursor = db.execute_query(db_connection=db_connection, query=querySearch4)
    searchResultsAgents = cursor.fetchall()
    searchResultsAgent = []
    for agent in searchResultsAgents:
        searchResultsAgent.append({'agent_id': agent['agent_id'], 'name': agent['name']}.copy())
    searchResultsAgent.append({'agent_id': "none", 'name': "None"})
    querySearch5 = "SELECT add_on_id, name FROM Add_Ons;"
    cursor = db.execute_query(db_connection=db_connection, query=querySearch5)
    searchResultsAddOn = cursor.fetchall()
    
    if request.method == "POST":
        if request.form.get("update_rental"):
            driver_input = request.form["driver"]
            location_input = request.form["location"]
            car_input = request.form["car"]
            agent_input = request.form["agent"]
            pickup_time_input = request.form["pickup_time"] + ":00"
            pickup_date_input = request.form["pickup_date"]
            return_time_input = request.form["return_time"] + ":00"
            return_date_input = request.form["return_date"]
            payment_input = request.form["payment"]
            cost_input = request.form["cost"]
            if agent_input == "none":
                query_parameters = [driver_input,location_input,car_input,pickup_time_input,pickup_date_input,return_time_input,return_date_input,payment_input,cost_input]
                query_parameters.append(id)
                query = "UPDATE Rentals SET Rentals.driver_id = %s, Rentals.location_id = %s, Rentals.car_id = %s, Rentals.agent_id = NULL, Rentals.pickup_time = %s, Rentals.pickup_date = %s, Rentals.return_time = %s, Rentals.return_date = %s, Rentals.payment_type = %s, Rentals.total_cost = %s WHERE Rentals.rental_id = %s"
            else:
                query_parameters = [driver_input,location_input,car_input,agent_input,pickup_time_input,pickup_date_input,return_time_input,return_date_input,payment_input,cost_input]
                query_parameters.append(id)
                query = "UPDATE Rentals SET Rentals.driver_id = %s, Rentals.location_id = %s, Rentals.car_id = %s, Rentals.agent_id = %s, Rentals.pickup_time = %s, Rentals.pickup_date = %s, Rentals.return_time = %s, Rentals.return_date = %s, Rentals.payment_type = %s, Rentals.total_cost = %s WHERE Rentals.rental_id = %s"
            cursor = db.execute_query(db_connection=db_connection, query=query, query_params=query_parameters)
            add_ons_input = request.form.getlist('add_ons')
            query = "SELECT Rentals_Add_Ons.add_on_id \
                FROM Rentals_Add_Ons \
                INNER JOIN Add_Ons ON Rentals_Add_Ons.add_on_id = Add_Ons.add_on_id \
                WHERE Rentals_Add_Ons.rental_id = %s \
                ORDER BY rental_id ASC;"
            cursor = db.execute_query(db_connection=db_connection, query=query, query_params=[id])
            resultsAddOns = cursor.fetchall()
            old_add_ons_input = [str(addOn['add_on_id']) for addOn in resultsAddOns]
            remove_addOns = set(old_add_ons_input) - set(add_ons_input)
            for addOn in remove_addOns:
                query_parameters = [id, int(addOn)]
                query = "DELETE FROM Rentals_Add_Ons WHERE rental_id = %s AND add_on_id = %s;"
                cursor = db.execute_query(db_connection=db_connection, query=query, query_params=query_parameters)
            for addOn in add_ons_input:
                if addOn not in old_add_ons_input:
                    query_parameters = [id, int(addOn)]
                    query = "INSERT INTO Rentals_Add_Ons (rental_id, add_on_id) VALUES (%s, %s);"
                    cursor = db.execute_query(db_connection=db_connection, query=query, query_params=query_parameters)         

        return redirect("/Rentals")
    
    query = "SELECT * FROM Rentals WHERE rental_id = %s"
    cursor = db.execute_query(db_connection=db_connection, query=query, query_params=[id])
    resultsTable = cursor.fetchall()
    query = "SELECT Rentals_Add_Ons.rental_id, Add_Ons.name \
        FROM Rentals_Add_Ons \
        INNER JOIN Add_Ons ON Rentals_Add_Ons.add_on_id = Add_Ons.add_on_id \
        WHERE Rentals_Add_Ons.rental_id = %s \
        ORDER BY rental_id ASC;"
    cursor = db.execute_query(db_connection=db_connection, query=query, query_params=[id])
    resultsAddOns = cursor.fetchall()
    intersections = set()
    for addOn in resultsAddOns:
        intersections.add(addOn['name'])
    
    return render_template('rentals_update.j2', rental=resultsTable[0], locations=searchResultsLoc, cars=searchResultsCar, drivers=searchResultsDriver, agents=searchResultsAgent, addOns=searchResultsAddOn, intersections=intersections)





@app.route('/Rentals/delete/<int:id>')
def rentals_delete(id):
    query = "DELETE FROM Rentals WHERE rental_id = %s;"
    cursor = db.execute_query(db_connection=db_connection, query=query, query_params=[id])
    return redirect('/Rentals')


#############################
### Driver Rentals Routes ###
#############################
@app.route('/Rentals_Add_Ons')
def rentals_add_ons():
    query = "SELECT Rentals_Add_Ons.rental_add_on_id AS id, Rentals.rental_id AS 'Rental Id', Add_Ons.add_on_id AS 'Add-On Id', Add_Ons.name AS 'Add-On Name' \
            FROM Rentals_Add_Ons \
            INNER JOIN Add_Ons ON Rentals_Add_Ons.add_on_id = Add_Ons.add_on_id \
            INNER JOIN Rentals ON Rentals_Add_Ons.rental_id = Rentals.rental_id \
            ORDER BY Rentals.rental_id, Add_Ons.add_on_id ASC;"
    cursor = db.execute_query(db_connection=db_connection, query=query)
    results = cursor.fetchall()
    return render_template('rentals_add_ons.j2', rentalAddOns=results)


########################
### Add_Ons Routes ###
########################
@app.route('/Add_Ons', methods=["POST","GET"])
def add_ons():
    if request.method == "POST":
        if request.form.get("add_add_on"):
            name_input = request.form["name"]
            description_input = request.form["description"]
            query_parameters = [name_input,description_input]
            query = "INSERT INTO Add_Ons (name, description) VALUES (%s, %s);"
            cursor = db.execute_query(db_connection=db_connection, query=query, query_params=query_parameters)
            return redirect("/Add_Ons")
           
    query = "SELECT * FROM Add_Ons;"
    cursor = db.execute_query(db_connection=db_connection, query=query)
    results = cursor.fetchall()
    return render_template('add_ons.j2', addOns=results)


@app.route('/Add_Ons/delete/<int:id>')
def add_ons_delete(id):
    query = "DELETE FROM Add_Ons WHERE add_on_id = %s;"
    cursor = db.execute_query(db_connection=db_connection, query=query, query_params=[id])
    return redirect("/Add_Ons")


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
    query = "SELECT Cars.car_id, Locations.address AS 'Location', Cars.make, Cars.model, Cars.year, Cars.car_body_type, Cars.daily_price, Cars.color, Cars.license_plate_num, Cars.vin, Cars.current_mileage, Cars.current_availability \
            FROM Cars \
            LEFT JOIN Locations ON Cars.location_id = Locations.location_id;"
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
    port = int(os.environ.get('PORT', 5000))
    #Start the app on port 3000, it will be different once hosted
    app.run(port=port, debug=True)