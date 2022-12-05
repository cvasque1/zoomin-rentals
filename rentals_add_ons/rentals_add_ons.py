from flask import Blueprint, render_template
import database.db_connector as db

RentalsAddOns = Blueprint("rentals_add_ons", __name__, static_folder="static", template_folder="templates")
db_connection = db.connect_to_database()
db_connection.ping(True)

##############################
### Rentals Add Ons Routes ###
##############################
@RentalsAddOns.route('/')
def rentals_add_ons():
    # select all rental_add_ons
    query = "SELECT Rentals_Add_Ons.rental_add_on_id AS id, Rentals.rental_id AS 'Rental Id', \
                Add_Ons.add_on_id AS 'Add-On Id', Add_Ons.name AS 'Add-On Name' \
            FROM Rentals_Add_Ons \
            INNER JOIN Add_Ons ON Rentals_Add_Ons.add_on_id = Add_Ons.add_on_id \
            INNER JOIN Rentals ON Rentals_Add_Ons.rental_id = Rentals.rental_id \
            ORDER BY Rentals.rental_id, Add_Ons.add_on_id ASC;"
    cursor = db.execute_query(db_connection=db_connection, query=query)
    results = cursor.fetchall()
    return render_template('rentals_add_ons.j2', rentalAddOns=results)