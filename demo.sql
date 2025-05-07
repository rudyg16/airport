USE airportDB;

SELECT *
FROM users
    JOIN passenger ON users.user_id = passenger.user_id WHERE users.username='Rodolfo';

SELECT * FROM luggage;
SELECT * FROM ticket JOIN passenger ON ticket.pass_id = passenger.pass_id;

SELECT t.ticket_id, t.seat_num, f.depart_city, f.arrival_city, p.pass_fname, p.pass_lname, p.user_id,p.pass_id
FROM
    ticket t
    JOIN flight f ON t.flight_num = f.flight_num
    JOIN passenger p ON t.pass_id = p.pass_id
WHERE
    p.user_id = 3;