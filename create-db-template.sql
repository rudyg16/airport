
DROP DATABASE IF EXISTS airportDB;
CREATE DATABASE airportDB;
USE airportDB;

--Run in order

/* Users (must come early so passenger can FK to it) */
CREATE TABLE users (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password VARCHAR(50) NOT NULL
);

/* Airlines */
CREATE TABLE airline ( airline_name VARCHAR(50) PRIMARY KEY );

CREATE TABLE model(
    model_name VARCHAR(60) NOT NULL PRIMARY KEY,
    capacity INT NOT NULL
);
/* Airplanes  */
CREATE TABLE airplane (
    airplane_id INT AUTO_INCREMENT PRIMARY KEY,
    model_name VARCHAR(60) NOT NULL,
    airline_name VARCHAR(50) NOT NULL,
    FOREIGN KEY(model_name) REFERENCES model(model_name),
    FOREIGN KEY (airline_name) REFERENCES airline(airline_name)
);

/* Terminals */
CREATE TABLE terminal ( terminal_letter CHAR(1) PRIMARY KEY );

/* Gates  – composite PK lets the same gate number exist in different terminals */
CREATE TABLE gate (
    gate_num INT NOT NULL,
    terminal_letter CHAR(1) NOT NULL,
    PRIMARY KEY (gate_num, terminal_letter),
    FOREIGN KEY (terminal_letter) REFERENCES terminal (terminal_letter)
);

/* Employees */
CREATE TABLE employee (
    employ_id INT AUTO_INCREMENT PRIMARY KEY,
    employ_ssn CHAR(11) NOT NULL,
    job_role VARCHAR(60) NOT NULL,
    employ_fname VARCHAR(40) NOT NULL,
    employ_lname VARCHAR(40) NOT NULL,
    airline_name VARCHAR(50) NOT NULL,
    FOREIGN KEY (airline_name) REFERENCES airline (airline_name)
);

/* Passengers (optionally linked 1‑to‑1 with a user account) */
CREATE TABLE passenger (
    pass_id INT AUTO_INCREMENT PRIMARY KEY,
    pass_lname VARCHAR(40),
    pass_fname VARCHAR(40),
    pass_passportID CHAR(9),
    state_ID VARCHAR(12),
    pass_email VARCHAR(60),
    user_id INT ,
    FOREIGN KEY (user_id) REFERENCES users (user_id)
);

#ALTER TABLE passenger DROP FOREIGN KEY passenger_ibfk_1;
#ALTER TABLE passenger DROP INDEX user_id; #remov user_id that had UNIQUE constraint 
#ALTER TABLE passenger ADD INDEX user_id INT;

#Use this to create new 1:M relationships
#ALTER TABLE passenger
#ADD CONSTRAINT fk_user_id
#FOREIGN KEY(user_id) REFERENCES users(user_id);

CREATE TABLE flight (
    flight_num INT AUTO_INCREMENT PRIMARY KEY,
    depart_time DATETIME NOT NULL,
    arrival_time DATETIME NOT NULL,
    capacity INT NOT NULL,
    state_ID VARCHAR(12) NOT NULL,
    pass_email VARCHAR(60) NOT NULL,
    airline_name VARCHAR(50) NOT NULL,
    gate_num INT NOT NULL,
    terminal_letter CHAR(1) NOT NULL,
    arrival_city VARCHAR(50),
    depart_city VARCHAR(50),
    arrival_country VARCHAR(50),
    depart_country VARCHAR(50),
    FOREIGN KEY (airline_name) REFERENCES airline (airline_name),
    FOREIGN KEY (gate_num, terminal_letter) REFERENCES gate (gate_num, terminal_letter)
);

/* Luggage -- belongs to a passenger per specific flight */
CREATE TABLE luggage (
    luggage_id INT AUTO_INCREMENT PRIMARY KEY,
    pass_id INT NOT NULL,
    flight_num INT NOT NULL,
    FOREIGN KEY (pass_id) REFERENCES passenger (pass_id),
    FOREIGN KEY (flight_num) REFERENCES flight (flight_num)
);

/* Tickets */
CREATE TABLE ticket (
    ticket_id INT AUTO_INCREMENT PRIMARY KEY,
    seat_num SMALLINT NOT NULL,
    flight_num INT NOT NULL,
    UNIQUE (flight_num, seat_num),
    FOREIGN KEY (flight_num) REFERENCES flight (flight_num)
);

/* Flight‑crew assignment for M-to-M relationship */
CREATE TABLE crew (
    flight_num INT NOT NULL,
    employ_id INT NOT NULL,
    PRIMARY KEY (flight_num, employ_id),
    FOREIGN KEY (flight_num) REFERENCES flight (flight_num),
    FOREIGN KEY (employ_id) REFERENCES employee (employ_id)
);