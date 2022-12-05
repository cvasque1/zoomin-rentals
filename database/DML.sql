------------------
-- DRIVERS PAGE --
------------------
-- select all drivers
SELECT * FROM Drivers;

-- select specific driver for update
SELECT * FROM Drivers WHERE driver_id = :driver_id_input;

-- search for driver with specific last name
SELECT * FROM Drivers WHERE last_name LIKE :last_name_input+'%';

-- create a new driver entry
INSERT INTO Drivers (first_name, last_name, email, phone, street, city, state, zipcode) VALUES 
(:first_name_input, :last_name_input, :email_input, :phone_input, :street_input, :city_input, :state_input, :zipcode_input);

-- update an existing driver entry
UPDATE Drivers SET 
    first_name = :first_name_input,
    last_name = :last_name_input,
    email = :email_input,
    phone = :phone_input,
    street = :street_input,
    city = :city_input,
    state = :state_input,
    zipcode = :zipcode_input
WHERE driver_id = :driver_id_input;

-- delete an exisiting driver
DELETE FROM Drivers WHERE driver_id = :driver_id_input;


-------------------------
-- BOOKING_AGENTS PAGE --
-------------------------
-- select all drivers
SELECT * FROM Booking_Agents;

-- select specific booking agent for update
SELECT * FROM Booking_Agents WHERE agent_id = :agent_id_input;

-- search for booking agent with specific last name
SELECT * FROM Booking_Agents WHERE last_name LIKE :last_name_input+'%';

-- create a booking agent entry
INSERT INTO Drivers (first_name, last_name, email, phone, street, city, state, zipcode) VALUES 
(:first_name_input, :last_name_input, :email_input, :phone_input, :street_input, :city_input, :state_input, :zipcode_input);

-- update an existing booking agent entry
UPDATE Booking_Agents SET 
    first_name = :first_name_input,
    last_name = :last_name_input,
    email = :email_input
WHERE agent_id = :agent_id_input;

-- delete an exisiting driver
DELETE FROM Booking_Agents WHERE agent_id = :agent_id_input;


--------------------------
------ RENTALS PAGE ------
--------------------------
-- select ALL rental for update, left joining foregin keys to display aliases rather than ids
SELECT R.rental_id, CONCAT(D.first_name,' ',D.last_name) as driver, CONCAT(L.address,', ',L.city) as locale, \
    CONCAT(C.make,' ',C.model) as car, IFNULL(CONCAT(A.first_name,' ',A.last_name), '') as agent, \
    R.pickup_time, R.pickup_date, R.return_time, R.return_date, R.payment_type, R.total_cost FROM Rentals AS R \
LEFT JOIN Drivers AS D ON R.driver_id = D.driver_id \
LEFT JOIN Locations AS L ON R.location_id = L.location_id \
LEFT JOIN Cars AS C ON R.car_id = C.car_id \
LEFT JOIN Booking_Agents AS A ON R.agent_id = A.agent_id;

-- select specific rental for update, left joining foregin keys to display aliases rather than ids
SELECT R.rental_id, R.driver_id, CONCAT(D.first_name,' ',D.last_name) as driver, R.location_id, 
    CONCAT(L.address,', ',L.city) as locale, R.car_id, CONCAT(C.make,' ',C.model) as car, R.agent_id, 
    IFNULL(CONCAT(A.first_name,' ',A.last_name), '') as agent, R.pickup_time, R.pickup_date, 
    R.return_time, R.return_date, R.payment_type, R.total_cost FROM Rentals AS R 
LEFT JOIN Drivers AS D ON R.driver_id = D.driver_id 
LEFT JOIN Locations AS L ON R.location_id = L.location_id 
LEFT JOIN Cars AS C ON R.car_id = C.car_id 
LEFT JOIN Booking_Agents AS A ON R.agent_id = A.agent_id 
WHERE R.rental_id = :rental_id_input;

-- select addons related to rental_ids (intersection table query)
SELECT Rentals_Add_Ons.rental_id, Add_Ons.name 
FROM Rentals_Add_Ons 
INNER JOIN Add_Ons ON Rentals_Add_Ons.add_on_id = Add_Ons.add_on_id 
WHERE Rentals_Add_Ons.rental_id = :rental_id_input 
ORDER BY rental_id ASC;

-- search for rental based on pickup_date
SELECT R.rental_id, CONCAT(D.first_name,' ',D.last_name) as driver, CONCAT(L.address,', ',L.city) as locale, 
    CONCAT(C.make,' ',C.model) as car, IFNULL(CONCAT(A.first_name,' ',A.last_name), '') as agent, 
    R.pickup_time, R.pickup_date, R.return_time, R.return_date, R.payment_type, R.total_cost FROM Rentals AS R 
LEFT JOIN Drivers AS D ON R.driver_id = D.driver_id 
LEFT JOIN Locations AS L ON R.location_id = L.location_id 
LEFT JOIN Cars AS C ON R.car_id = C.car_id 
LEFT JOIN Booking_Agents AS A ON R.agent_id = A.agent_id 
WHERE R.pickup_date = :pickup_date_input ORDER BY rental_id ASC;

-- select foreign keys to populate forms
SELECT location_id, address, city FROM Locations;
SELECT car_id, make, model, color, vin FROM Cars;
SELECT driver_id, CONCAT(first_name,' ',last_name) AS name FROM Drivers;
SELECT agent_id, CONCAT(first_name,' ',last_name) AS name FROM Booking_Agents;
SELECT add_on_id, name FROM Add_Ons;

-- create a new rental entry
INSERT INTO Rentals (driver_id, location_id, car_id, agent_id, pickup_time, pickup_date, return_time, return_date, payment_type, total_cost)
VALUES (:driver_id_input, :location_id_input, :car_id_input, :agent_id_input, :pickup_time_input, :pickup_date_input, :return_time_input, :return_date_input, :payment_type_input, :total_cost_input);

-- update an existing rental entry
UPDATE Rentals SET 
    driver_id = :driver_id_input,
    location_id = :location_id_input,
    car_id = :car_id_input,
    agent_id = :agent_id_input,
    pickup_time = :pickup_time_input,
    pickup_date = :pickup_date_input,
    return_time = :return_time_input,
    return_date = :return_date_input,
    payment_type = :payment_type_input,
    total_cost = :total_cost_input
WHERE rental_id = :rental_id_input;

-- delete an exisiting rental
DELETE FROM Rentals WHERE rental_id = :rental_id_input;


-----------------------
------ RENTALS_ADD_ONS PAGE ------
----------------------
-- select all rental_add_ons
SELECT Rentals_Add_Ons.rental_add_on_id AS id, Rentals.rental_id AS 'Rental Id', \
    Add_Ons.add_on_id AS 'Add-On Id', Add_Ons.name AS 'Add-On Name' \
FROM Rentals_Add_Ons \
INNER JOIN Add_Ons ON Rentals_Add_Ons.add_on_id = Add_Ons.add_on_id \
INNER JOIN Rentals ON Rentals_Add_Ons.rental_id = Rentals.rental_id \
ORDER BY Rentals.rental_id, Add_Ons.add_on_id ASC;

-- create new rental_add_on entry
INSERT INTO Rentals_Add_Ons (rental_id, add_on_id) 
VALUES (:rental_id_input, :add_on_id_input);

-- delete an exisiting rental_add_on
DELETE FROM Rentals_Add_Ons WHERE rental_id = rental_id_input AND add_on_id = add_on_id_input;


-----------------------
------ ADD_ONS PAGE ---
-----------------------
-- select all add_ons
SELECT * FROM Add_Ons;

-- create new add_on entry
INSERT INTO Add_Ons (name, description) 
VALUES (:name_input, :description_input);

-- delete an exisiting rental_add_on
DELETE FROM Add_Ons WHERE add_on_id = add_on_id_input;


-----------------------
------ CARS PAGE ------
-----------------------
-- select all cars, left joining foregin keys to display aliases rather than ids
SELECT C.car_id, CONCAT(L.address,', ',L.city) AS 'Location', C.make, C.model, C.year, C.car_body_type, \
    C.daily_price, C.color, C.license_plate_num, C.vin, C.current_mileage, C.current_availability \
FROM Cars AS C\
LEFT JOIN Locations AS L ON C.location_id = L.location_id;

-- select foreign keys to populate forms
SELECT location_id, address, city FROM Locations;

-- select specific car for update
SELECT * FROM Cars WHERE car_id = :car_id_input;

-- select Cars make for form
SELECT make FROM Cars;

-- select all cars filtered by current_availability
SELECT C.car_id, CONCAT(L.address,', ',L.city) AS 'Location', C.make, C.model, C.year, C.car_body_type, \
    C.daily_price, C.color, C.license_plate_num, C.vin, C.current_mileage, C.current_availability \
FROM Cars AS C\
LEFT JOIN Locations AS L ON C.location_id = L.location_id \
WHERE C.current_availability = %s;

-- select all cars filtered by make
SELECT C.car_id, CONCAT(L.address,', ',L.city) AS 'Location', C.make, C.model, C.year, C.car_body_type, \
    C.daily_price, C.color, C.license_plate_num, C.vin, C.current_mileage, C.current_availability \
FROM Cars AS C\
LEFT JOIN Locations AS L ON C.location_id = L.location_id \
WHERE C.make = %s;

-- select foreign key ids
SELECT location_id, address, city FROM Locations;

-- create a new car entry
INSERT INTO Cars (location_id, make, model, year, car_body_type, daily_price, color, license_plate_num, vin, current_mileage, current_availability) VALUES 
(:location_id_input, :make_input, :model_input, :year_input, :car_body_type_input, :daily_price_input, :color_input, :license_plate_num_input, :vin_input, :current_mileage_input, :current_availability_input);

-- update an existing car entry
UPDATE Cars SET 
    location_id = :location_id_input,
    make = :make_input,
    model = :model_input,
    year = :year_input,
    car_body_type = :car_body_type_input,
    daily_price = :daily_price_input,
    color = :color_input,
    license_plate_num = :license_plate_num_input,
    vin = :vin_input,
    current_mileage = :current_mileage_input,
    current_availability = :current_availability_input
WHERE car_id = :car_id_input;

-- delete an exisiting car
DELETE FROM Cars WHERE car_id = :car_id_input;


----------------------------
------ LOCATIONS PAGE ------
----------------------------
-- select all locations
SELECT * FROM Locations;

-- select cities for search feature
SELECT city FROM Locations;

-- select specific location for search based on city
SELECT * FROM Locations WHERE city = :city_input;

-- select specific location for update
SELECT * FROM Locations WHERE location_id = :location_id_input;

-- create a new car entry
INSERT INTO Location (city, state, address, zipcode, num_cars) VALUES 
(:city_input, :state_input, :address_input, :zipcode_input, :num_cars_input);

-- update an existing car entry
UPDATE Locations SET 
    city = :city_input,
    state = :state_input,
    address = :address_input,
    zipcode = :zipcode_input,
    num_cars = :num_cars_input
WHERE location_id = :location_id_input;

-- delete an exisiting car
DELETE FROM Locations WHERE location_id = :location_id_input;