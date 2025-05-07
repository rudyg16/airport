USE airportDB;
#Login
SELECT * FROM  users WHERE username = 'Rodolfo' AND password = 'admin';

#Search
SELECT flight.*, model.capacity, airline.airline_name
FROM
    flight
    JOIN airplane ON flight.airplane_id = airplane.airplane_id
    JOIN model ON airplane.model_name = model.model_name
    JOIN airline ON airplane.airline_name = airline.airline_name
WHERE
    1 = 1
    AND flight.arrival_city LIKE '%Milan';

SELECT flight.*, model.capacity, airline.airline_name
FROM
    flight
    JOIN airplane ON flight.airplane_id = airplane.airplane_id
    JOIN model ON airplane.model_name = model.model_name
    JOIN airline ON airplane.airline_name = airline.airline_name
WHERE
    1 = 1
    AND flight.arrival_city LIKE '%Milan'
    AND flight.depart_city LIKE '%Dallas'
    AND airline.airline_name LIKE '%United Airlines' 
    AND DATE(flight.depart_time) = '2025-05-08';

#PASSENGER 
SELECT passenger.*,users.username FROM users JOIN passenger ON passenger.user_id = users.user_id WHERE users.user_id=3;
INSERT INTO
    passenger (
        pass_lname,
        pass_fname,
        pass_passportID,
        state_ID,
        pass_email,
        user_id
    )
VALUES ('James','Lebron', 'ABCDEFGHI',"ABCDEFGHIKLM", 'lebron@gmail.com', '3')

DELETE FROM passenger WHERE pass_lname='James' AND pass_fname ='Lebron';

#My Flights 
SELECT t.ticket_id, t.seat_num, t.flight_num, f.depart_city, f.arrival_city, f.depart_time, f.arrival_time, al.airline_name, p.pass_fname, p.pass_lname, l.weight, l.bagtype
FROM
    ticket t
    JOIN passenger p ON t.pass_id = p.pass_id
    JOIN flight f ON f.flight_num = t.flight_num
    JOIN airplane ap ON f.airplane_id = ap.airplane_id
    JOIN airline al ON ap.airline_name = al.airline_name
    LEFT JOIN luggage l ON l.ticket_id = t.ticket_id
WHERE
    p.user_id = ;

