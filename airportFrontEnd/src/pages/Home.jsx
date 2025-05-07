import React from "react";
import { Link } from "react-router-dom";
import "./Home.css";

const Home = () => {
  return (
    <div className="home-container">
      <h2>Welcome to SkyBook</h2>
      <p>Easily search, book, and manage your flights with a few clicks.</p>

      <div className="home-options">
        <Link to="/search" className="home-card">
          <h3>🔍 Search Flights</h3>
          <p>Find flights by city, date, and airline, and book in seconds.</p>
        </Link>

        <Link to="/select-passenger" className="home-card">
          <h3>🧍‍♂️ Passengers</h3>
          <p>Add and manage passengers for your bookings.</p>
        </Link>

        <Link to="/baggage" className="home-card">
          <h3>🧳 Baggage</h3>
          <p>Include carry-on and checked baggage details for each trip.</p>
        </Link>

        <Link to="/confirmation" className="home-card">
          <h3>✅ Confirm</h3>
          <p>Review all flight, passenger, and baggage details before finalizing.</p>
        </Link>

        <Link to="/my-flights" className="home-card">
          <h3>✈️ My Flights</h3>
          <p>View your upcoming booked flights and travel details.</p>
        </Link>
      </div>
    </div>
  );
};

export default Home;
