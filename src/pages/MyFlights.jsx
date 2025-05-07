import React, { useEffect, useState } from "react";
import "../pages/MyFlights.css";

const MyFlights = () => {
  const [bookings, setBookings] = useState([]);

  useEffect(() => {
    const flight = JSON.parse(localStorage.getItem("selectedFlight") || "null");
    const passenger = JSON.parse(localStorage.getItem("selectedPassenger") || "null");
    const baggage = JSON.parse(localStorage.getItem("baggageInfo") || "[]");    

    if (flight && passenger) {
      setBookings([
        {
          flight,
          passenger,
          baggage,
        },
      ]);
    }
  }, []);

  return (
    <div className="myflights-container">
      <h2>My Flights</h2>

      {bookings.length === 0 ? (
        <p>No flights booked yet.</p>
      ) : (
        bookings.map((booking, index) => (
          <div className="flight-card" key={index}>
            <h3>{booking.flight.departureCity} → {booking.flight.arrivalCity}</h3>
            <p><strong>Date:</strong> {booking.flight.date}</p>
            <p><strong>Time:</strong> {booking.flight.time}</p>
            <p><strong>Airline:</strong> {booking.flight.airline}</p>
            <p><strong>Passenger:</strong> {booking.passenger.name}</p>

            {booking.baggage && booking.baggage.length > 0 && (
              <div className="baggage-info">
                <p><strong>Baggage:</strong></p>
                <ul>
                  {booking.baggage.map((bag, idx) => (
                    <li key={idx}>
                      {bag.quantity} x {bag.type} ({bag.weight}lbs each)
                    </li>
                  ))}
                </ul>
              </div>
            )}
          </div>
        ))
      )}
    </div>
  );
};

export default MyFlights;
