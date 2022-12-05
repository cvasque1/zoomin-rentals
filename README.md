# Zoomin' Rentals
Instructions for Git workflow: https://edstem.org/us/courses/28987/discussion/2007407

## Downloading and running
In the root directory, create a virtual environment:
      python -m venv venv
      
Activate virtual environment:
      ./venv/Scripts/activate
      
Install project dependencies:
      pip install -r requirements.txt
      
You can now run the Flask app:
      Flask run

## Directory Structure
.
├── app.py
├── .gitignore
├── README.md
├── requirements.txt
├── templates/
│   ├── base.j2
│   └── index.j2
├── static/
│   └── styles/
│       └── style.css
├── database/
│   ├── db_connector.py
│   ├── db_credentials.py
│   ├── DDL.sql
│   └── DML.sql
├── add_ons/
│   ├── add_ons.py
│   └── templates/
│       └── add_ons.j2
├── booking_agents/
│   ├── booking_agents.py
│   └── templates/
│       ├── booking_agents.j2
│       └── booking_agents_update.j2
├── cars/
│   ├── cars.py
│   └── templates/
│       ├── cars.j2
│       └── cars_update.j2
├── drivers/
│   ├── drivers.py
│   └── templates/
│       ├── drivers.j2
│       └── drivers_update.j2
├── locations/
│   ├── locations.py
│   └── templates/
│       ├── locations.j2
│       └── locations_update.j2
├── rentals/
│   ├── rentals.py
│   └── templates/
│       ├── rentals.j2
│       └── rentals_update.j2
└── rentals_add_ons/
    ├── rentals_add_ons.py
    └── templates/
        └── rentals_add_ons.j2