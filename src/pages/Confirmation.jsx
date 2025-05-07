import React, { useEffect, useState } from "react";
import "../pages/Confirmation.css";

const Confirmation = () => {
  const [flight, setFlight] = useState(null);
  const [passenger, setPassenger] = useState(null);
  const [baggage, setBaggage] = useState([]);

  useEffect(() => {
    const storedFlight = JSON.parse(localStorage.getItem("selectedFlight") || "null");
    const storedPassenger = JSON.parse(localStorage.getItem("selectedPassenger") || "null");
    const storedBaggage = JSON.parse(localStorage.getItem("baggageInfo") || "[]");    

    setFlight(storedFlight);
    setPassenger(storedPassenger);
    setBaggage(storedBaggage);
  }, []);

  if (!flight || !passenger) {
    return (
      <div className="confirmation-container">
        <div className="confirmation-card">
          <h2>Booking Confirmation</h2>
          <p>Booking details not found. Please start your booking again.</p>
        </div>
      </div>
    );
  }

  return (
    <div className="confirmation-container">
      <div className="confirmation-card">
        <h2>Booking Confirmation</h2>

        <div className="section">
          <h4>Passenger</h4>
          <p>{passenger.name}</p>
        </div>

        <div className="section">
          <h4>Flight Details</h4>
          <p>
            <strong>{flight.departureCity}</strong> →{" "}
            <strong>{flight.arrivalCity}</strong>
          </p>
          <p>Date: {flight.date}</p>
          <p>Time: {flight.time}</p>
          <p>Airline: {flight.airline}</p>
        </div>

        <div className="section">
          <h4>Baggage</h4>
          {baggage.length === 0 ? (
            <p>No baggage added</p>
          ) : (
            baggage.map((bag, index) => (
              <p key={index}>
                {bag.quantity} x {bag.type} ({bag.weight}lbs each)
              </p>
            ))
          )}
        </div>

        <p className="success-message">Thank you for booking with us!</p>
      </div>
    </div>
  );
};

export default Confirmation;
