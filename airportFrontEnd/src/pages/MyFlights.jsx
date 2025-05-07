import React, { useEffect, useState } from "react";
import "../pages/MyFlights.css";
import axios from "axios";

const MyFlights = () => {
  const [bookings, setBookings] = useState([]);

  useEffect(() => {
    const userId = localStorage.getItem("user_id");
    if (!userId) return;

    const fetchBookings = async () => {
      try {
        const res = await axios.get(`http://localhost:8000/tickets/by-user/${userId}`);
        console.log("Bookings received:", res.data); // Debug log
        setBookings(res.data);
      } catch (err) {
        console.error("Failed to fetch user bookings:", err);
      }
    };

    fetchBookings();
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
            {booking.flight.depart_time && (
              <>
                <p><strong>Date:</strong> {booking.flight.depart_time.split("T")[0]}</p>
                <p><strong>Time:</strong> {booking.flight.depart_time.split("T")[1]}</p>
              </>
            )}
            <p><strong>Airline:</strong> {booking.flight.airline || booking.flight.airline_name}</p>
            <p><strong>Passenger:</strong> {booking.passenger.name}</p>

            {booking.baggage && booking.baggage.length > 0 && (
              <div className="baggage-info">
                <p><strong>Baggage:</strong></p>
                <ul>
                  {booking.baggage.map((bag, idx) => (
                    <li key={idx}>{bag.type} ({bag.weight}lbs)</li>
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
