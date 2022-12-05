from flask import Blueprint, render_template, redirect, request
import database.db_connector as db

Locations = Blueprint("locations", __name__, static_folder="static", template_folder="templates")
db_connection = db.connect_to_database()
db_connection.ping(True)


@Locations.route('/', methods=["POST","GET"])
def locations():
    # select specific location for search based on city
    querySearch = "SELECT city FROM Locations;"
    cursor = db.execute_query(db_connection=db_connection, query=querySearch)
    searchResults = cursor.fetchall()

    if request.method == "POST":
        # create new location
        if request.form.get("add_location"):
            # get form inputs
            address_input = request.form["address"]
            city_input = request.form["city"]
            state_input = request.form["state"]
            zipcode_input = request.form["zipcode"]
            qty_input = request.form["qty"]

            # build and make insert query to database
            query_parameters = [address_input,city_input,state_input,zipcode_input,qty_input]
            query = "INSERT INTO Locations (address, city, state, zipcode, num_cars) \
                    VALUES (%s, %s, %s, %s, %s);"
            cursor = db.execute_query(db_connection=db_connection, query=query, query_params=query_parameters)
            return redirect("/Locations")
        
        # search for location by city
        elif request.form.get("search_location"):
            city_input = request.form["city"]
            query = "SELECT * FROM Locations WHERE city = %s;"
            cursor = db.execute_query(db_connection=db_connection, query=query, query_params=[city_input])
            results = cursor.fetchall()
            return render_template('locations.j2', Locations=results, cities=searchResults)
    else: # GET request  
        query = "SELECT * FROM Locations;"
        cursor = db.execute_query(db_connection=db_connection, query=query)
        results = cursor.fetchall()
        return render_template('locations.j2', Locations=results, cities=searchResults)

# UPDATE
@Locations.route('/update/<int:id>', methods=["POST", "GET"])
def locations_update(id):
    if request.method == "POST":
        # update location
        if request.form.get("update_location"):
            address_input = request.form["address"]
            city_input = request.form["city"]
            state_input = request.form["state"]
            zipcode_input = request.form["zipcode"]
            qty_input = request.form["qty"]
            
            # build and make update query to database
            query_parameters = [address_input,city_input,state_input,zipcode_input,qty_input]
            query_parameters.append(id)
            query = "UPDATE Locations SET Locations.address = %s, Locations.city = %s, Locations.state = %s, \
                        Locations.zipcode = %s, Locations.num_cars = %s \
                    WHERE Locations.location_id = %s"
            cursor = db.execute_query(db_connection=db_connection, query=query, query_params=query_parameters)
            
        return redirect("/Locations")
    else: # GET request
        query = "SELECT * FROM Locations WHERE location_id = %s;"
        cursor = db.execute_query(db_connection=db_connection, query=query, query_params=[id])
        results = cursor.fetchall()
        return render_template('locations_update.j2', location=results[0])

# DELETE
@Locations.route('/delete/<int:id>')
def locations_delete(id):
    query = "DELETE FROM Locations WHERE location_id = %s;"
    cursor = db.execute_query(db_connection=db_connection, query=query, query_params=[id])
    return redirect("/Locations")