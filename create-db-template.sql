CREATE DATABASE airportDB;

USE airport;
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

CREATE TABLE BOOLEAN
