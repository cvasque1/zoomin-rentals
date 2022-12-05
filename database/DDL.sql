SET FOREIGN_KEY_CHECKS=0;
SET UNIQUE_CHECKS=0;
SET AUTOCOMMIT=0;

DROP TABLE IF EXISTS `Rentals`;
DROP TABLE IF EXISTS `Drivers`;
DROP TABLE IF EXISTS `Booking_Agents`;
DROP TABLE IF EXISTS `Cars`;
DROP TABLE IF EXISTS `Locations`;
DROP TABLE IF EXISTS `Add_Ons`;
DROP TABLE IF EXISTS `Rentals_Add_Ons`;


CREATE OR REPLACE TABLE `Rentals` (
    `rental_id` int(11) NOT NULL AUTO_INCREMENT,
    `driver_id` int(11) NOT NULL,
    `location_id` int(11) NOT NULL,
    `car_id` int(11) NOT NULL,
    `agent_id` int(11) NULL,
    `pickup_time` time NOT NULL,
    `pickup_date` date NOT NULL,
    `return_time` time NOT NULL,
    `return_date` date NOT NULL,
    `payment_type` varchar(255) NOT NULL,
    `total_cost` int(11) NOT NULL,
    PRIMARY KEY (`rental_id`),
    FOREIGN KEY (`driver_id`) REFERENCES `Drivers` (`driver_id`)
    ON DELETE CASCADE,
    FOREIGN KEY (`location_id`) REFERENCES `Locations` (`location_id`)
    ON DELETE CASCADE,
    FOREIGN KEY (`car_id`) REFERENCES `Cars` (`car_id`)
    ON DELETE CASCADE,
    FOREIGN KEY (`agent_id`) REFERENCES `Booking_Agents` (`agent_id`)
    ON DELETE SET NULL
);


CREATE OR REPLACE TABLE `Drivers` (
    `driver_id` int(11) NOT NULL AUTO_INCREMENT,
    `first_name` varchar(255) NOT NULL,
    `last_name` varchar(255) NOT NULL,
    `email` varchar(255) NOT NULL,
    `phone` varchar(20) NOT NULL,
    `street` varchar(255) NOT NULL,
    `city` varchar(255) NOT NULL,
    `state` varchar(255) NOT NULL,
    `zipcode` varchar(10) NOT NULL,
    PRIMARY KEY(`driver_id`)
);


CREATE OR REPLACE TABLE `Booking_Agents` (
    `agent_id` int(11) NOT NULL AUTO_INCREMENT,
    `first_name` varchar(255) NOT NULL,
    `last_name` varchar(255) NOT NULL,
    `email` varchar(255) NOT NULL,
    PRIMARY KEY(`agent_id`)
);


CREATE OR REPLACE TABLE `Cars` (
    `car_id` int(11) NOT NULL AUTO_INCREMENT,
    `location_id` int(11) NOT NULL,
    `make` varchar(255) NOT NULL,
    `model` varchar(255) NOT NULL,
    `year` varchar(255) NOT NULL,
    `car_body_type` varchar(255) NOT NULL,
    `daily_price` int(3) NOT NULL,
    `color` varchar(255) NOT NULL,
    `license_plate_num` varchar(255) NOT NULL,
    `vin` varchar(255) NOT NULL,
    `current_mileage` int(6) NOT NULL,
    `current_availability` varchar(255) NOT NULL,
    PRIMARY KEY (`car_id`),
    FOREIGN KEY (`location_id`) REFERENCES `Locations` (`location_id`)
    ON DELETE CASCADE
);


CREATE OR REPLACE TABLE `Locations` (
    `location_id` int(11) NOT NULL AUTO_INCREMENT,
    `address` varchar(255) NOT NULL,
    `city` varchar(255) NOT NULL,
    `state` varchar(255) NOT NULL,
    `zipcode` varchar(10) NOT NULL,
    `num_cars` int(3) NOT NULL,
    PRIMARY KEY(`location_id`)
);


CREATE OR REPLACE TABLE `Add_Ons` (
    `add_on_id` int(11) NOT NULL AUTO_INCREMENT,
    `name` varchar(255) NOT NULL,
    `description` varchar(255) NOT NULL,
    PRIMARY KEY(`add_on_id`)
);

-- Create intersection table for Rentals and Add_Ons
CREATE OR REPLACE TABLE `Rentals_Add_Ons` (
    `rental_add_on_id` int(11) NOT NULL AUTO_INCREMENT,
    `rental_id` int(11) NOT NULL,
    `add_on_id` int(11) NOT NULL,
    PRIMARY KEY(`rental_add_on_id`),
    FOREIGN KEY (`rental_id`) REFERENCES `Rentals` (`rental_id`)
    ON DELETE CASCADE,
    FOREIGN KEY (`add_on_id`) REFERENCES `Add_Ons` (`add_on_id`)
    ON DELETE CASCADE
);


INSERT INTO Rentals (driver_id, location_id, car_id, agent_id, pickup_time, pickup_date, return_time, return_date, payment_type, total_cost) VALUES 
('1','1','1', Null, '14:00:00', '2022-11-13','14:00:00','2020-06-15','credit', '100'),
('2','1','1', '2', '18:00:00','2022-11-18','18:00:00','2020-02-20','credit', '100'),
('1','3','3', '1', '10:00:00','2022-11-24','10:00:00','2021-09-07','cash', '75');


INSERT INTO Drivers (first_name, last_name, email, phone, street, city, state, zipcode) VALUES 
('Joanne','Dorsey','erika1978@gmail.com','831-291-5800','4306 Atha Drive','Taft','CA','93258'),
('Javier','Jolcomb','trenton1975@hotmail.com','323-394-9408','4121 Doctors Drive','Los Angeles','CA','90017'),
('Inez','Jackson','hildegard2010@gmail.com','845-612-8109','3730 Benedum Drive','Brewster','NY','10509');


INSERT INTO Booking_Agents (first_name, last_name, email) VALUES 
('Mario','Richardson','lisette.jenki@zoominrentals.com'),
('John','Slawson','carey1996@zoominrentals.com'),
('Phyllis ','Fields','maxine1996@zoominrentals.com');


INSERT INTO Locations (city, state, address, zipcode, num_cars) VALUES 
('San Francisco', 'CA', '1001 Fremont St', 90415, 20),
('Los Angeles', 'CA', '2000 WilShire', 90008, 25),
('New York City', 'NY', '6000 Wall St', 10005, 16);


INSERT INTO Cars (location_id, make, model, year, car_body_type, daily_price, color, license_plate_num, vin, current_mileage, current_availability) VALUES 
((SELECT location_id FROM Locations WHERE city = 'San Francisco'),'BMW','328i','1996','Sedan','50','Black','4UPZ565','WAULF78K89N032914','189000','Unavailable'),
((SELECT location_id FROM Locations WHERE city = 'San Francisco'),'Ferrari','LaFerrari','2018','Coupe','10000','Red','2RDX156','JH4DA3350GS005185','2000','Available'),
((SELECT location_id FROM Locations WHERE city = 'New York City'),'Toyota','Corolla','2015','Sedan','25','Blue','5SBQ300','1G4AH51N1K6437778','70000','Unavailable') ;


INSERT INTO Add_Ons (name, description) VALUES
("SAT Radio", "Access to our Sirius XM Satellite Radio"),
("Prepaid Tolls", "Unlimited use of automated toll lanes at no cost."),
("Snow Chains", "System of chain designed to cover a tire to get better traction in the snow.");


INSERT INTO Rentals_Add_Ons (rental_id, add_on_id) VALUES
(
    (SELECT rental_id FROM Rentals WHERE driver_id = 1 AND car_id = 1 AND pickup_date = '2022-11-13'),
    (SELECT add_on_id FROM Add_Ons WHERE name = "SAT Radio")
),
(
    (SELECT rental_id FROM Rentals WHERE driver_id = 2 AND car_id = 1 AND pickup_date = '2022-11-18'),
    (SELECT add_on_id FROM Add_Ons WHERE name = "Prepaid Tolls")
),
(
    (SELECT rental_id FROM Rentals WHERE driver_id = 1 AND car_id = 1 AND pickup_date = '2022-11-13'),
    (SELECT add_on_id FROM Add_Ons WHERE name = "Snow Chains")
);



SET FOREIGN_KEY_CHECKS=1;
SET UNIQUE_CHECKS=1;
COMMIT;