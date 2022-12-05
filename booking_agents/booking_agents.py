from flask import Blueprint, render_template, redirect, request
import database.db_connector as db

Agents = Blueprint("booking_agents", __name__, static_folder="static", template_folder="templates")
db_connection = db.connect_to_database()
db_connection.ping(True)


@Agents.route('/', methods=["POST", "GET"])
def booking_agents():
    if request.method == "POST":
        # create new agent
        if request.form.get("add_agent"):
            # get form inputs
            first_name_input = request.form["first_name"]
            last_name_input = request.form["last_name"]
            email_input = request.form["email"]

            #build and make insert query to database
            query_parameters = [first_name_input,last_name_input,email_input]
            query = "INSERT INTO Booking_Agents (first_name, last_name, email) VALUES (%s, %s, %s);"
            cursor = db.execute_query(db_connection=db_connection, query=query, query_params=query_parameters)
            return redirect("/Booking_Agents")

        # search for agent by last name
        elif request.form.get("search_agent"):
            last_name_input = request.form["last_name"]
            query = "SELECT * FROM Booking_Agents WHERE last_name LIKE %s;"
            cursor = db.execute_query(db_connection=db_connection, query=query, query_params=(last_name_input + '%',))
            results = cursor.fetchall()
            return render_template('booking_agents.j2', Agents=results)
    else: # GET request
        query = "SELECT * FROM Booking_Agents;"
        cursor = db.execute_query(db_connection=db_connection, query=query)
        results = cursor.fetchall()
        return render_template('booking_agents.j2', Agents=results)

# UPDATE
@Agents.route('/update/<int:id>', methods=["POST", "GET"])
def booking_agents_update(id):
    if request.method == "POST":
        # update agent chosen
        if request.form.get("update_agent"):
            # get form inputs
            first_name_input = request.form["first_name"]
            last_name_input = request.form["last_name"]
            email_input = request.form["email"]
            
            # build and make update query to database
            query_parameters = [first_name_input,last_name_input,email_input]
            query_parameters.append(id)
            query = "UPDATE Booking_Agents SET Booking_Agents.first_name = %s, Booking_Agents.last_name = %s, \
                        Booking_Agents.email = %s WHERE Booking_Agents.agent_id = %s"
            cursor = db.execute_query(db_connection=db_connection, query=query, query_params=query_parameters)
            
        return redirect("/Booking_Agents")
    else: # GET request
        query = "SELECT * FROM Booking_Agents WHERE agent_id = %s;"
        cursor = db.execute_query(db_connection=db_connection, query=query, query_params=[id])
        results = cursor.fetchall()
        return render_template('booking_agents_update.j2', agent=results[0])

# DELETE
@Agents.route('/delete/<int:id>')
def booking_agents_delete(id):
    query = "DELETE FROM Booking_Agents WHERE agent_id = %s;"
    cursor = db.execute_query(db_connection=db_connection, query=query, query_params=[id])
    return redirect("/Booking_Agents")