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

-- select foreign key ids
SELECT * FROM Cars WHERE Cars.location_id = :car_location_id_input;

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

