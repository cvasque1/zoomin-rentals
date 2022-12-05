from flask import Blueprint, render_template, redirect, request
import database.db_connector as db
from collections import defaultdict

Rentals = Blueprint("rentals", __name__, static_folder="static", template_folder="templates")
db_connection = db.connect_to_database()
db_connection.ping(True)


@Rentals.route('/', methods=["POST","GET"])
def rentals():
    # Foreign key queries to populate forms
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
    # Select addons related to rental_ids (intersection table query)
    query = "SELECT Rentals_Add_Ons.rental_id, Add_Ons.name \
            FROM Rentals_Add_Ons \
            INNER JOIN Add_Ons ON Rentals_Add_Ons.add_on_id = Add_Ons.add_on_id \
            ORDER BY rental_id ASC;"
    cursor = db.execute_query(db_connection=db_connection, query=query)
    results = cursor.fetchall()
    # Create hashtable of intersection values to display multiple addOns per rental in table
    intersections = defaultdict(list)
    for r in results:
        intersections[r['rental_id']].append(r['name'])
    
    if request.method == "POST":
        # create new rental
        if request.form.get("add_rental"):
            # get form inputs
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

            # build and make insert query to database
            # account for nullable relationship with Booking_Agents
            if agent_input == "none":
                query_parameters = [driver_input,location_input,car_input,None,pickup_time_input,pickup_date_input,
                                    return_time_input,return_date_input,payment_input,cost_input]
            else:
                query_parameters = [driver_input,location_input,car_input,agent_input,pickup_time_input,
                                    pickup_date_input,return_time_input,return_date_input,payment_input,cost_input]
            query = "INSERT INTO Rentals (driver_id, location_id, car_id, agent_id, pickup_time, pickup_date, \
                        return_time, return_date, payment_type, total_cost) \
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"
            cursor = db.execute_query(db_connection=db_connection, query=query, query_params=query_parameters)
            rentalID = cursor.lastrowid
            # Intersection table insert occur in Rentals page. 
            # If addOns selected, make entry for each in intersection table.
            if len(add_ons_input) > 0:
                for add_on_input in add_ons_input:
                    query_parameters = [rentalID, add_on_input]
                    query = "INSERT INTO Rentals_Add_Ons (rental_id, add_on_id) VALUES (%s, %s);"
                    cursor = db.execute_query(db_connection=db_connection, query=query, query_params=query_parameters)
            return redirect("/Rentals")

        # search for rental by pickup date
        elif request.form.get("search_rental"):
            # Select ALL rentals, left joining foregin keys to display aliases rather than ids, matching pickup date
            pickup_date_input = request.form["pickup_date"]
            query = "SELECT R.rental_id, CONCAT(D.first_name,' ',D.last_name) as driver, CONCAT(L.address,', ',L.city) as locale, \
                        CONCAT(C.make,' ',C.model) as car, IFNULL(CONCAT(A.first_name,' ',A.last_name), '') as agent, \
                        R.pickup_time, R.pickup_date, R.return_time, R.return_date, R.payment_type, R.total_cost FROM Rentals AS R \
                    LEFT JOIN Drivers AS D ON R.driver_id = D.driver_id \
                    LEFT JOIN Locations AS L ON R.location_id = L.location_id \
                    LEFT JOIN Cars AS C ON R.car_id = C.car_id \
                    LEFT JOIN Booking_Agents AS A ON R.agent_id = A.agent_id \
                    WHERE R.pickup_date = %s ORDER BY rental_id ASC"
            # Select addons related to rental_ids (intersection table query)
            cursor = db.execute_query(db_connection=db_connection, query=query, query_params=[pickup_date_input])
            resultsTable = cursor.fetchall()
            return render_template('rentals.j2', Rentals=resultsTable, locations=searchResultsLoc, cars=searchResultsCar,
                                     drivers=searchResultsDriver, addOns=searchResultsAddOn, intersections=intersections)
    else: # GET request
        # Select ALL rentals, left joining foregin keys to display aliases rather than ids
        query = "SELECT R.rental_id, CONCAT(D.first_name,' ',D.last_name) as driver, CONCAT(L.address,', ',L.city) as locale, \
                    CONCAT(C.make,' ',C.model) as car, IFNULL(CONCAT(A.first_name,' ',A.last_name), '') as agent, \
                    R.pickup_time, R.pickup_date, R.return_time, R.return_date, R.payment_type, R.total_cost FROM Rentals AS R \
                LEFT JOIN Drivers AS D ON R.driver_id = D.driver_id \
                LEFT JOIN Locations AS L ON R.location_id = L.location_id \
                LEFT JOIN Cars AS C ON R.car_id = C.car_id \
                LEFT JOIN Booking_Agents AS A ON R.agent_id = A.agent_id;"
        cursor = db.execute_query(db_connection=db_connection, query=query)
        resultsTable = cursor.fetchall()
        return render_template('rentals.j2', Rentals=resultsTable, locations=searchResultsLoc, cars=searchResultsCar, 
                                drivers=searchResultsDriver, agents=searchResultsAgent, addOns=searchResultsAddOn, 
                                intersections=intersections)

# UPDATE
@Rentals.route('/update/<int:id>', methods=["POST", "GET"])
def rentals_update(id):
    # Foreign key queries to populate forms
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
    # hashtable with booking agents. this is used to prepopulate agent form value
    #  whether it is Null or not
    searchResultsAgent = []
    for agent in searchResultsAgents:
        searchResultsAgent.append({'agent_id': agent['agent_id'], 'name': agent['name']}.copy())
    searchResultsAgent.append({'agent_id': "none", 'name': "None"})
    querySearch5 = "SELECT add_on_id, name FROM Add_Ons;"
    cursor = db.execute_query(db_connection=db_connection, query=querySearch5)
    searchResultsAddOn = cursor.fetchall()
    # Select addons related to rental_ids (intersection table query)
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
    
    if request.method == "POST":
        # update rental
        if request.form.get("update_rental"):
            # get form inputs
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

            # build update query
            # account for nullable relationship with Booking_Agents
            if agent_input == "none":
                query_parameters = [driver_input,location_input,car_input,pickup_time_input,pickup_date_input,
                                    return_time_input,return_date_input,payment_input,cost_input]
                query_parameters.append(id)
                query = "UPDATE Rentals SET Rentals.driver_id = %s, Rentals.location_id = %s, Rentals.car_id = %s, \
                            Rentals.agent_id = NULL, Rentals.pickup_time = %s, Rentals.pickup_date = %s, \
                            Rentals.return_time = %s, Rentals.return_date = %s, Rentals.payment_type = %s, Rentals.total_cost = %s \
                        WHERE Rentals.rental_id = %s"
            else:
                query_parameters = [driver_input,location_input,car_input,agent_input,pickup_time_input,
                                    pickup_date_input,return_time_input,return_date_input,payment_input,cost_input]
                query_parameters.append(id)
                query = "UPDATE Rentals SET Rentals.driver_id = %s, Rentals.location_id = %s, Rentals.car_id = %s, \
                            Rentals.agent_id = %s, Rentals.pickup_time = %s, Rentals.pickup_date = %s, \
                            Rentals.return_time = %s, Rentals.return_date = %s, Rentals.payment_type = %s, Rentals.total_cost = %s \
                        WHERE Rentals.rental_id = %s"
            # make update query
            cursor = db.execute_query(db_connection=db_connection, query=query, query_params=query_parameters)
            # Makes changes to intersection table based on the add_ons removed and added to rental entry
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
            for addOn in remove_addOns: # Add_ons removed from intersection table
                query_parameters = [id, int(addOn)]
                query = "DELETE FROM Rentals_Add_Ons WHERE rental_id = %s AND add_on_id = %s;"
                cursor = db.execute_query(db_connection=db_connection, query=query, query_params=query_parameters)
            for addOn in add_ons_input: # Add_ons added to itnersection table
                if addOn not in old_add_ons_input:
                    query_parameters = [id, int(addOn)]
                    query = "INSERT INTO Rentals_Add_Ons (rental_id, add_on_id) VALUES (%s, %s);"
                    cursor = db.execute_query(db_connection=db_connection, query=query, query_params=query_parameters)         

        return redirect("/Rentals")
    else: # GET request
        # Select single rental, left joining foregin keys to display aliases rather than ids
        query = "SELECT R.rental_id, R.driver_id, CONCAT(D.first_name,' ',D.last_name) as driver, R.location_id, \
                    CONCAT(L.address,', ',L.city) as locale, R.car_id, CONCAT(C.make,' ',C.model) as car, R.agent_id, \
                    IFNULL(CONCAT(A.first_name,' ',A.last_name), '') as agent, R.pickup_time, R.pickup_date, \
                    R.return_time, R.return_date, R.payment_type, R.total_cost FROM Rentals AS R \
                LEFT JOIN Drivers AS D ON R.driver_id = D.driver_id \
                LEFT JOIN Locations AS L ON R.location_id = L.location_id \
                LEFT JOIN Cars AS C ON R.car_id = C.car_id \
                LEFT JOIN Booking_Agents AS A ON R.agent_id = A.agent_id \
                WHERE R.rental_id = %s;"
        cursor = db.execute_query(db_connection=db_connection, query=query, query_params=[id])
        resultsTable = cursor.fetchall()
        
        return render_template('rentals_update.j2', rental=resultsTable[0], locations=searchResultsLoc, 
            cars=searchResultsCar, drivers=searchResultsDriver, agents=searchResultsAgent, 
            addOns=searchResultsAddOn, intersections=intersections)

# DELETE
@Rentals.route('/delete/<int:id>')
def rentals_delete(id):
    query = "DELETE FROM Rentals WHERE rental_id = %s;"
    cursor = db.execute_query(db_connection=db_connection, query=query, query_params=[id])
    return redirect('/Rentals')