SET FOREIGN_KEY_CHECKS=0;
SET UNIQUE_CHECKS=0;
SET AUTOCOMMIT=0;

DROP TABLE IF EXISTS `rentals`;
DROP TABLE IF EXISTS `drivers`;
DROP TABLE IF EXISTS `cars`;
DROP TABLE IF EXISTS `locations`;
DROP TABLE IF EXISTS `drivers_rentals`;


CREATE OR REPLACE TABLE `Rentals` (
    `rental_id` int(11) NOT NULL AUTO_INCREMENT,
    `location_id` int(11) NOT NULL,
    `car_id` int(11) NOT NULL,
    `rental_time` time NOT NULL,
    `rental_date` date NOT NULL,
    `pickup_time` time NOT NULL,
    `pickup_date` date NOT NULL,
    `return_time` time NOT NULL,
    `return_date` date NOT NULL,
    `payment_type` varchar(255) NOT NULL,
    `current_status` varchar(255) NOT NULL,
    `total_penalties` int(5),
    `total_cost` int(11) NOT NULL,
    PRIMARY KEY (`rental_id`),
    FOREIGN KEY (`location_id`) REFERENCES `Locations` (`location_id`)
    ON DELETE CASCADE,
    FOREIGN KEY (`car_id`) REFERENCES `Cars` (`car_id`)
    ON DELETE CASCADE
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


CREATE OR REPLACE TABLE `Cars` (
    `car_id` int(11) NOT NULL AUTO_INCREMENT,
    `location_id` int(11) NOT NULL,
    `make` varchar(255) NOT NULL,
    `model` varchar(255) NOT NULL,
    `year` varchar(255) NOT NULL,
    `car_body_type` varchar(255),
    `daily_price` int(3),
    `color` varchar(255),
    `license_plate_num` varchar(255) NOT NULL,
    `vin` varchar(255) NOT NULL,
    `current_mileage` int(6),
    `current_availability` varchar(255),
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
    `num_cars` int(3),
    PRIMARY KEY(`location_id`)
);

-- Create intersection table for Drivers and Rentals
CREATE OR REPLACE TABLE `drivers_rentals` (
    `driver_rental_id` int(11) NOT NULL AUTO_INCREMENT,
    `driver_id` int(11) NOT NULL,
    `rental_id` int(11),
    PRIMARY KEY(`driver_rental_id`),
    FOREIGN KEY (`driver_id`) REFERENCES `Drivers` (`driver_id`)
    ON DELETE CASCADE,
    FOREIGN KEY (`rental_id`) REFERENCES `Rentals` (`rental_id`)
    ON DELETE CASCADE
);


INSERT INTO Rentals (location_id, car_id, rental_time, rental_date, pickup_time, pickup_date, return_time, return_date, payment_type, current_status, total_penalties, total_cost) VALUES 
('1','1','11:00:00','2020-06-12','14:00:00', '2020-06-13','14:00:00','2020-06-15','credit','active','20','100'),
('1','1','13:00:00','2020-02-17','18:00:00','2020-02-18','18:00:00','2020-02-20','credit','active','30','100'),
('3','3','07:00:00','2021-09-03','10:00:00','2021-09-04','10:00:00','2021-09-07','cash','active','40','75');


INSERT INTO Drivers (first_name, last_name, email, phone, street, city, state, zipcode) VALUES 
('Joanne','Dorsey','erika1978@gmail.com','831-291-5800','4306 Atha Drive','Taft','CA','93258'),
('Javier','Jolcomb','trenton1975@hotmail.com','323-394-9408','4121 Doctors Drive','Los Angeles','CA','90017'),
('Inez','Jackson','hildegard2010@gmail.com','845-612-8109','3730 Benedum Drive','Brewster','NY','10509');


INSERT INTO Cars (location_id, make, model, year, car_body_type, daily_price, color, license_plate_num, vin, current_mileage, current_availability) VALUES 
((SELECT location_id FROM Locations WHERE city = 'San Francisco'),'BMW','328i','1996','Sedan','50','Black','4UPZ565','WAULF78K89N032914','189000','Unavailable'),
((SELECT location_id FROM Locations WHERE city = 'San Francisco'),'Ferrari','LaFerrari','2018','Coupe','10000','Red','2RDX156','JH4DA3350GS005185','2000','Available'),
((SELECT location_id FROM Locations WHERE city = 'New York City'),'Toyota','Corolla','2015','Sedan','25','Blue','5SBQ300','1G4AH51N1K6437778','70000','Unavailable') ;


INSERT INTO Locations (city, state, address, zipcode, num_cars) VALUES 
('San Francisco', 'CA', '1001 Fremont St', 90415, 20),
('Los Angeles', 'CA', '2000 WilShire', 90008, 25),
('New York', 'NY', '6000 Wall St', 10005, 16);


INSERT INTO drivers_rentals (driver_id, rental_id) VALUES
(1,1),
(1,2),
(2,3);

-- We getting an error with the input below. Currently hardcoding id inputs for intersection table driver_rentals

-- (
--     (SELECT driver_id FROM Drivers WHERE first_name = "Joanne" AND last_name = "Dorsey"),
--     (SELECT rental_id FROM Rentals WHERE car_id = 1 AND pickup_time = '14:00:00' AND pickup_date = '2020-06-13')
-- )
-- (
--     (SELECT driver_id FROM Drivers WHERE first_name = "Joanne" AND last_name = "Dorsey"),
--     (SELECT rental_id FROM Rentals WHERE car_id = 1 AND pickup_time = '18:00:00' AND pickup_date = '2020-02-18')
-- )
-- (
--     (SELECT driver_id FROM Drivers WHERE first_name = "Javier" AND last_name = "Jolcomb"),
--     (SELECT rental_id FROM Rentals WHERE car_id = 2 AND pickup_time = '10:00:00' AND pickup_date = '2021-09-04')
-- );


SET FOREIGN_KEY_CHECKS=1;
SET UNIQUE_CHECKS=1;
COMMIT;