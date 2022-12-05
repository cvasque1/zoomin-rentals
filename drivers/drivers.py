from flask import Blueprint, render_template, redirect, request
import database.db_connector as db

Drivers = Blueprint("drivers", __name__, static_folder="static", template_folder="templates")
db_connection = db.connect_to_database()
db_connection.ping(True)


@Drivers.route('/', methods=["POST", "GET"])
def drivers():
    if request.method == "POST":
        # create new driver
        if request.form.get("add_driver"): 
            # get form inputs
            first_name_input = request.form["first_name"]
            last_name_input = request.form["last_name"]
            email_input = request.form["email"]
            phone_input = request.form["phone"]
            street_input = request.form["street"]
            city_input = request.form["city"]
            state_input = request.form["state"]
            zipcode_input = request.form["zipcode"]
            
            #build and make insert query to database
            query_parameters = [first_name_input,last_name_input,email_input,phone_input,
                                street_input,city_input,state_input,zipcode_input]
            query = "INSERT INTO Drivers (first_name, last_name, email, phone, street, city, state, zipcode) \
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s);"
            cursor = db.execute_query(db_connection=db_connection, query=query, query_params=query_parameters)
            return redirect("/Drivers")

        # search for driver by last name
        elif request.form.get("search_driver"):
            last_name_input = request.form["last_name"]
            query = "SELECT * FROM Drivers WHERE last_name LIKE %s;"
            cursor = db.execute_query(db_connection=db_connection, query=query, query_params=(last_name_input + '%',))
            results = cursor.fetchall()
            return render_template('drivers.j2', Drivers=results)
    else: #GET request
        query = "SELECT * FROM Drivers;"
        cursor = db.execute_query(db_connection=db_connection, query=query)
        results = cursor.fetchall()
        return render_template('drivers.j2', Drivers=results)

# UPDATE
@Drivers.route('/update/<int:id>', methods=["POST", "GET"])
def drivers_update(id):
    if request.method == "POST":
        # update driver chosen
        if request.form.get("update_driver"):
            # get form inputs
            first_name_input = request.form["first_name"]
            last_name_input = request.form["last_name"]
            email_input = request.form["email"]
            phone_input = request.form["phone"]
            street_input = request.form["street"]
            city_input = request.form["city"]
            state_input = request.form["state"]
            zipcode_input = request.form["zipcode"]
            
            #build and make update query to database
            query_parameters = [first_name_input,last_name_input,email_input,phone_input,
                                street_input,city_input,state_input,zipcode_input]
            query_parameters.append(id)
            query = "UPDATE Drivers SET Drivers.first_name = %s, Drivers.last_name = %s, Drivers.email = %s, \
                        Drivers.phone = %s, Drivers.street = %s, Drivers.city = %s, Drivers.state = %s, \
                        Drivers.zipcode = %s WHERE Drivers.driver_id = %s"
            cursor = db.execute_query(db_connection=db_connection, query=query, query_params=query_parameters)

        return redirect("/Drivers")
    else: # GET request
        query = "SELECT * FROM Drivers WHERE driver_id = %s;"
        cursor = db.execute_query(db_connection=db_connection, query=query, query_params=[id])
        results = cursor.fetchall()
        return render_template('drivers_update.j2', driver=results[0])

# DELETE
@Drivers.route('/delete/<int:id>')
def drivers_delete(id):
    query = "DELETE FROM Drivers WHERE driver_id = %s;"
    cursor = db.execute_query(db_connection=db_connection, query=query, query_params=[id])
    return redirect("/Drivers")