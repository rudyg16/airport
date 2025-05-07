import React, { useState } from "react";
import "./Search.css";
import { useNavigate } from "react-router-dom";

const Search = () => {
  const navigate = useNavigate();

  const [filters, setFilters] = useState({
    departureCity: "",
    arrivalCity: "",
    date: "",
    airline: "",
  });

  const mockFlights = [
    {
      id: 1,
      departureCity: "Dallas",
      arrivalCity: "New York",
      date: "2025-05-10",
      time: "09:00 AM",
      airline: "AirX",
    },
    {
      id: 2,
      departureCity: "San Francisco",
      arrivalCity: "Chicago",
      date: "2025-05-11",
      time: "1:30 PM",
      airline: "JetSky",
    },
    {
      id: 3,
      departureCity: "Miami",
      arrivalCity: "Seattle",
      date: "2025-05-12",
      time: "7:45 AM",
      airline: "BlueWings",
    },
  ];

  const [searchResults, setSearchResults] = useState(mockFlights);

  const handleInputChange = (e) => {
    setFilters({ ...filters, [e.target.name]: e.target.value });
  };

  const handleSearch = () => {
    const results = mockFlights.filter((flight) => {
      return (
        (!filters.departureCity ||
          flight.departureCity
            .toLowerCase()
            .includes(filters.departureCity.toLowerCase())) &&
        (!filters.arrivalCity ||
          flight.arrivalCity
            .toLowerCase()
            .includes(filters.arrivalCity.toLowerCase())) &&
        (!filters.date || flight.date === filters.date) &&
        (!filters.airline ||
          flight.airline.toLowerCase().includes(filters.airline.toLowerCase()))
      );
    });
    setSearchResults(results);
  };

  const handleSelect = (flight) => {
    localStorage.setItem("selectedFlight", JSON.stringify(flight));
    navigate("/select-passenger");
  };

  return (
    <div className="search-container">
      <h2>Search Flights</h2>
      <div className="search-form">
        <input
          type="text"
          name="departureCity"
          placeholder="Departure City"
          value={filters.departureCity}
          onChange={handleInputChange}
        />
        <input
          type="text"
          name="arrivalCity"
          placeholder="Arrival City"
          value={filters.arrivalCity}
          onChange={handleInputChange}
        />
        <input
          type="date"
          name="date"
          value={filters.date}
          onChange={handleInputChange}
        />
        <input
          type="text"
          name="airline"
          placeholder="Airline"
          value={filters.airline}
          onChange={handleInputChange}
        />
        <button onClick={handleSearch}>Search</button>
      </div>

      <div className="results">
        {searchResults.length === 0 ? (
          <p>No flights found.</p>
        ) : (
          searchResults.map((flight) => (
            <div key={flight.id} className="flight-card">
              <p>
                <strong>{flight.departureCity}</strong> →{" "}
                <strong>{flight.arrivalCity}</strong>
              </p>
              <p>Date: {flight.date}</p>
              <p>Time: {flight.time}</p>
              <p>Airline: {flight.airline}</p>
              <button onClick={() => handleSelect(flight)}>
                Select Flight
              </button>
            </div>
          ))
        )}
      </div>
    </div>
  );
};

export default Search;
