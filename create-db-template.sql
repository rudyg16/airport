CREATE DATABASE airportDB;

USE airportDB;
CREATE TABLE airline(
    airline_name VARCHAR(50) NOT NULL,

    PRIMARY KEY(airline_name),UNIQUE(airline_name)
);
CREATE TABLE airplane(
    airplane_id INT NOT NULL AUTO_INCREMENT,
    model VARCHAR(60) NOT NULL,
    capacity INT NOT NULL,
    airline_name VARCHAR(50) NOT NULL,

    PRIMARY KEY (airplane_id), UNIQUE(airplane_id), 
    FOREIGN KEY (airline_name) REFERENCES airline(airline_name)
);

CREATE TABLE terminal(
    terminal_letter VARCHAR(1) NOT NULL,
    PRIMARY KEY(terminal_letter),UNIQUE(terminal_letter)
);

CREATE TABLE gate(
    gate_num INT NOT NULL,
    terminal_letter VARCHAR(1) NOT NULL,

    PRIMARY KEY(gate_num), UNIQUE(gate_num),
    FOREIGN KEY(terminal_letter) REFERENCES terminal(terminal_letter)    
);

CREATE TABLE employee (
    employ_id INT AUTO_INCREMENT NOT NULL,
    employ_ssn VARCHAR(11) NOT NULL,
    job_role VARCHAR(60) NOT NULL,
    employ_fname VARCHAR(40) NOT NULL,
    employ_lname VARCHAR(40) NOT NULL,
    airline_name VARCHAR(50) NOT NULL,

    PRIMARY KEY(employ_id), UNIQUE(employ_id),
    FOREIGN KEY(airline_name) REFERENCES airline(airline_name)
)

CREATE TABLE passenger (
    pass_id INT NOT NULL AUTO_INCREMENT,
    pass_lname VARCHAR(40),
    pass_fname VARCHAR(40),
    pass_passportID VARCHAR(9),
    state_ID VARCHAR(12),
    pass_email VARCHAR(60),

    PRIMARY KEY(pass_id), UNIQUE(pass_id)
)

CREATE TABLE flight(
    flight_num INT NOT NULL AUTO_INCREMENT,
    depart_time DATETIME NOT NULL,
    arrival_time DATETIME NOT NULL,
    capacity INT NOT NULL,
    state_ID VARCHAR(12) NOT NULL,
    pass_email VARCHAR(60) NOT NULL,
    airline_name VARCHAR(50) NOT NULL,
    gate_num INT NOT NULL,
    
    PRIMARY KEY(flight_num), UNIQUE(flight_num),
    FOREIGN KEY(airline_name) REFERENCES airline(airline_name),
    FOREIGN KEY(gate_num) REFERENCES gate(gate_num)
)

ALTER TABLE flight 
ADD COLUMN arrival_country VARCHAR(50),
ADD COLUMN depart_country VARCHAR(50);
ALTER TABLE flight 
CHANGE arrival_location arrival_city VARCHAR(50),
CHANGE depart_location depart_city VARCHAR(50);


CREATE TABLE luggage(
    luggage_id INT NOT NULL AUTO_INCREMENT,
    pass_id INT NOT NULL,
    flight_num INT NOT NULL,
    
    PRIMARY KEY(luggage_id), UNIQUE(luggage_id),
    FOREIGN KEY(pass_id) REFERENCES passenger(pass_id),
    FOREIGN KEY(flight_num) REFERENCES flight(flight_num)
)

CREATE TABLE ticket(
    ticket_id INT NOT NULL AUTO_INCREMENT,
    seat_num SMALLINT NOT NULL,
    flight_num INT NOT NULL,
    
    PRIMARY KEY(ticket_id),UNIQUE(ticket_id),
    UNIQUE(flight_num,seat_num),
    FOREIGN KEY(flight_num) REFERENCES flight(flight_num)
)

CREATE TABLE crew(
    flight_num INT NOT NULL,
    employ_id INT NOT NULL,

    PRIMARY KEY (flight_num,employ_id),
    FOREIGN KEY(flight_num) REFERENCES flight(flight_num),
    FOREIGN KEY(employ_id) REFERENCES employee(employ_id)
)



