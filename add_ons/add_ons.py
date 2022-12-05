from flask import Blueprint, render_template, request, redirect
import database.db_connector as db

AddOns = Blueprint("add_ons", __name__, static_folder="static", template_folder="templates")
db_connection = db.connect_to_database()
db_connection.ping(True)


@AddOns.route('/', methods=["POST","GET"])
def add_ons():
    if request.method == "POST":
        # Create new add_on
        if request.form.get("add_add_on"):
            # get form inputs
            name_input = request.form["name"]
            description_input = request.form["description"]

            # build and make isnert query to database
            query_parameters = [name_input,description_input]
            query = "INSERT INTO Add_Ons (name, description) VALUES (%s, %s);"
            cursor = db.execute_query(db_connection=db_connection, query=query, query_params=query_parameters)
            return redirect("/Add_Ons")
    else: # GET request
        query = "SELECT * FROM Add_Ons;"
        cursor = db.execute_query(db_connection=db_connection, query=query)
        results = cursor.fetchall()
        return render_template('add_ons.j2', addOns=results)

# DELETE
@AddOns.route('/delete/<int:id>')
def add_ons_delete(id):
    query = "DELETE FROM Add_Ons WHERE add_on_id = %s;"
    cursor = db.execute_query(db_connection=db_connection, query=query, query_params=[id])
    return redirect("/Add_Ons")