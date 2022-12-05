from flask import Blueprint, render_template, redirect, request
import database.db_connector as db

Cars = Blueprint("cars", __name__, static_folder="static", template_folder="templates")
db_connection = db.connect_to_database()
db_connection.ping(True)


@Cars.route('/', methods=["POST", "GET"])
def cars():
    # Foreign key queries to populate forms
    querySearch = "SELECT location_id, address, city FROM Locations;"
    cursor = db.execute_query(db_connection=db_connection, query=querySearch)
    searchResults = cursor.fetchall()
    querySearch = "SELECT make FROM Cars;"
    cursor = db.execute_query(db_connection=db_connection, query=querySearch)
    searchResultsMake = cursor.fetchall()

    if request.method == "POST":
        # create new car
        if request.form.get("add_car"):
            # get form input
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
            
            # build and make insert query to database
            query_parameters = [location_input,make_input,model_input,year_input,body_input,price_input,
                                color_input,plate_input,vin_input,mileage_input,availability_input]
            query = "INSERT INTO Cars (location_id, make, model, year, car_body_type, daily_price, color, \
                        license_plate_num, vin, current_mileage, current_availability) \
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"
            cursor = db.execute_query(db_connection=db_connection, query=query, query_params=query_parameters)
            return redirect("/Cars")

        # search for car by make
        elif request.form.get("search_car_make"):
            # select all cars, left joining foregin keys to display aliases rather than ids, matching make
            make_input = request.form["make"]
            query = "SELECT C.car_id, CONCAT(L.address,', ',L.city) AS 'Location', C.make, C.model, C.year, C.car_body_type, \
                        C.daily_price, C.color, C.license_plate_num, C.vin, C.current_mileage, C.current_availability \
                    FROM Cars AS C\
                    LEFT JOIN Locations AS L ON C.location_id = L.location_id \
                    WHERE C.make = %s;"
            cursor = db.execute_query(db_connection=db_connection, query=query, query_params=[make_input])
            results = cursor.fetchall()
            return render_template('cars.j2', Cars=results, locations=searchResults, makes=searchResultsMake)
        
        # search for car by availability
        elif request.form.get("search_car_availability"):
            # select all cars, left joining foregin keys to display aliases rather than ids, matching availability
            availability_input = request.form["availability"]
            query = "SELECT C.car_id, CONCAT(L.address,', ',L.city) AS 'Location', C.make, C.model, C.year, C.car_body_type, \
                        C.daily_price, C.color, C.license_plate_num, C.vin, C.current_mileage, C.current_availability \
                    FROM Cars AS C\
                    LEFT JOIN Locations AS L ON C.location_id = L.location_id \
                    WHERE C.current_availability = %s;"
            cursor = db.execute_query(db_connection=db_connection, query=query, query_params=[availability_input])
            results = cursor.fetchall()
            return render_template('cars.j2', Cars=results, locations=searchResults, makes=searchResultsMake)
    else: # GET request
        # select all cars, left joining foregin keys to display aliases rather than ids
        query = "SELECT C.car_id, CONCAT(L.address,', ',L.city) AS 'Location', C.make, C.model, C.year, C.car_body_type, \
                    C.daily_price, C.color, C.license_plate_num, C.vin, C.current_mileage, C.current_availability \
                FROM Cars AS C\
                LEFT JOIN Locations AS L ON C.location_id = L.location_id;"
        cursor = db.execute_query(db_connection=db_connection, query=query)
        results = cursor.fetchall()
        return render_template('cars.j2', Cars=results, locations=searchResults, makes=searchResultsMake)

# UPDATE
@Cars.route('/update/<int:id>', methods=["POST","GET"])
def cars_update(id):
    # Foreign key queries to populate forms
    querySearch = "SELECT location_id, address, city FROM Locations;"
    cursor = db.execute_query(db_connection=db_connection, query=querySearch)
    searchResults = cursor.fetchall()

    if request.method == "POST":
        # update car
        if request.form.get("update_car"):
            # get form input
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

            # build and make update query to database
            query_parameters = [location_input,make_input,model_input,year_input,body_input,price_input,
                                color_input,plate_input,vin_input,mileage_input,availability_input]
            query_parameters.append(id)
            query = "UPDATE Cars SET Cars.location_id = %s, Cars.make = %s, Cars.model = %s, Cars.year = %s, \
                        Cars.car_body_type = %s, Cars.daily_price = %s, Cars.color = %s, Cars.license_plate_num = %s, \
                        Cars.vin = %s, Cars.current_mileage = %s, Cars.current_availability = %s \
                    WHERE Cars.car_id = %s"
            cursor = db.execute_query(db_connection=db_connection, query=query, query_params=query_parameters)
            
        return redirect("/Cars")
    else:
        # select all cars, left joining foregin keys to display aliases rather than ids
        query = "SELECT C.car_id, L.location_id, CONCAT(L.address,', ',L.city) AS 'Location', C.make, \
                    C.model, C.year, C.car_body_type, C.daily_price, C.color, C.license_plate_num, \
                    C.vin, C.current_mileage, C.current_availability \
                FROM Cars AS C\
                LEFT JOIN Locations AS L ON C.location_id = L.location_id \
                WHERE C.car_id = %s;"
        cursor = db.execute_query(db_connection=db_connection, query=query, query_params=[id])
        results = cursor.fetchall()
        body_types = ["Sedan", "Coupe", "SUV", "Minivan"]
        return render_template('cars_update.j2', car=results[0], locations=searchResults, body_types=body_types)

# DELETE
@Cars.route('/delete/<int:id>')
def cars_delete(id):
    query = "DELETE FROM Cars WHERE car_id = %s;"
    cursor = db.execute_query(db_connection=db_connection, query=query, query_params=[id])
    return redirect('/Cars')