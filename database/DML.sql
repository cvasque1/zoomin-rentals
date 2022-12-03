------------------
-- DRIVERS PAGE --
------------------

-- select all drivers
SELECT * FROM Drivers;

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


----------------------------
------ LOCATIONS PAGE ------
----------------------------
-- select all cars
SELECT * FROM Locations;
-- select cities for search feature
SELECT city FROM Locations;
-- select specific location for update
SELECT * FROM Locations WHERE city = %s;

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


--------------------------
------ RENTALS PAGE ------
--------------------------

-- select all rentals
SELECT * FROM Rentals;

-- select foreign key ids
SELECT * FROM Rentals WHERE Rentals.location_id = :rental_location_id_input;
SELECT * FROM Rentals WHERE Rentals.car_id = :rental_car_id_input;

-- create a new rental entry
INSERT INTO Rentals (location_id, car_id, rental_time, rental_date, pickup_time, pickup_date, return_time, return_date, payment_type, current_status, total_penalties, total_cost) VALUES 
(:location_id_input, :car_id_input, :rental_time_input, :rental_date_input, :pickup_time_input, :pickup_date_input, :return_time_input, :return_date_input, :payment_type_input, :current_status_input, :total_penalties_input, :total_cost_input);

-- update an existing rental entry
UPDATE Rentals SET 
    location_id = :location_id_input,
    car_id = :car_id_input,
    rental_time = :rental_time_input,
    rental_date = :rental_date_input,
    pickup_time = :pickup_time_input,
    pickup_date = :pickup_date_input,
    return_time = :return_time_input,
    return_date = :return_date_input,
    payment_type = :payment_type_input,
    current_status = :current_status_input,
    total_penalties = :total_penalties_input,
    total_cost = :total_cost_input
WHERE rental_id = :rental_id_input;

-- delete an exisiting rental
DELETE FROM Rentals WHERE rental_id = :rental_id_input;


-----------------------
------ CARS PAGE ------
----------------------

-- select all cars
SELECT * FROM Cars;
-- select car of specific id
SELECT * FROM Cars WHERE car_id = :car_id_input;
-- select Cars make
SELECT make FROM Cars;
-- select all cars filtered by current_availability
SELECT * FROM Cars WHERE current_availability = :urrent_availability_input;
-- select all cars filtered by make
SELECT * FROM Cars WHERE make = :make_input;

-- select foreign key ids
SELECT * FROM Cars WHERE Cars.location_id = :car_location_id_input;
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


-----------------------
------ DRIVERS_RENTAL PAGE ------
----------------------

-- select all cars
SELECT * FROM Drivers_Rentals;

-- SELECT driver_id, rental_id FROM Drivers_Rentals 
--     INNER JOIN Drivers
--     ON driver_id = Drivers.driver_id;


SELECT Driver.driver_id, Rental.rental_id FROM Drivers_Rentals 
    INNER JOIN Drivers
    ON Rental.driver_id = Drivers.driver_id
    INNER JOIN Rentals
    ON Drivers.driver_id = Rental.driver_id;


-- create a new car entry
INSERT INTO Drivers_Rentals (driver_id, rental_id) VALUES 
(:driver_id_input, :rental_id_input);

-- update an existing car entry
UPDATE Drivers_Rentals SET 
    driver_id = :driver_id_input,
    rental_id = :rental_id_input,
WHERE driver_rental_id = :driver_rental_id_input;

-- delete an exisiting car
DELETE FROM Drivers_Rentals WHERE driver_rental_id = :driver_rental_id_input;

-- Intersection Table
SELECT Rentals_Add_Ons.rental_add_on_id AS id, Rentals.rental_id AS "Rental Id", Add_Ons.add_on_id AS "Add-On Id", Add_Ons.name AS "Add-On Name"  FROM Rentals_Add_Ons 
INNER JOIN Add_Ons ON Rentals_Add_Ons.add_on_id = Add_Ons.add_on_id 
INNER JOIN Rentals ON Rentals_Add_Ons.rental_id = Rentals.rental_id;

-- Cars lcoations
SELECT Cars.car_id, Locations.address AS 'Location', Cars.make, Cars.model, Cars.year, Cars.car_body_type, Cars.daily_price, Cars.color, Cars.license_plate_num, Cars.vin, Cars.current_mileage, Cars.current_availability 
FROM Cars 
LEFT JOIN Locations ON Cars.location_id = Locations.location_id; 

SELECT Rentals.rental_id, Rentals.driver_id, Rentals.location_id, Rentals.car_id, Rentals_Add_Ons.add_on_id FROM Rentals INNER JOIN Rentals_Add_Ons ON Rentals.rental_id = 16; 



SELECT Rentals_Add_Ons.rental_id, Add_Ons.name FROM Rentals_Add_Ons INNER JOIN Add_Ons ON Rentals_Add_Ons.add_on_id = Add_Ons.add_on_id ORDER BY rental_id ASC;


SELECT r.rental_id, r.driver_id, r.location_id, r.car_id, ra.add_on_id, 
    r.rental_time, r.rental_date, r.pickup_time, r.pickup_date, 
    r.return_time, r.return_date, r.payment_type, r.current_status,
    r.total_penalties, a.name, r.total_cost
FROM Rentals AS r 
LEFT JOIN Rentals_Add_Ons AS ra ON r.rental_id = ra.rental_id 
LEFT JOIN Add_Ons AS a ON ra.add_on_id = a.add_on_id;

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

UPDATE Rentals_Add_Ons SET
