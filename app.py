from flask import Flask, render_template
from flask_mysqldb import MySQL
import os

# import Blueprints
from drivers.drivers import Drivers
from booking_agents.booking_agents import Agents
from rentals.rentals import Rentals
from rentals_add_ons.rentals_add_ons import RentalsAddOns
from add_ons.add_ons import AddOns
from cars.cars import Cars
from locations.locations import Locations


app = Flask(__name__)
# Blueprints
app.register_blueprint(Drivers, url_prefix="/Drivers")
app.register_blueprint(Agents, url_prefix="/Booking_Agents")
app.register_blueprint(Rentals, url_prefix="/Rentals")
app.register_blueprint(RentalsAddOns, url_prefix="/Rentals_Add_Ons")
app.register_blueprint(AddOns, url_prefix="/Add_Ons")
app.register_blueprint(Cars, url_prefix="/Cars")
app.register_blueprint(Locations, url_prefix="/Locations")

# Configure database
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


# Listener
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 4444))
    app.run(port=port, debug=True)