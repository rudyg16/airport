import React, { useState } from "react";
import "./Search.css";
import { useNavigate } from "react-router-dom";
import axios from "axios";

const Search = () => {
  const navigate = useNavigate();

  const [filters, setFilters] = useState({
    departureCity: "",
    arrivalCity: "",
    date: "",
    airline: "",
  });

  const [searchResults, setSearchResults] = useState([]);
  const [message, setMessage] = useState("");

  const handleInputChange = (e) => {
    setFilters({ ...filters, [e.target.name]: e.target.value });
  };

  const handleSearch = async () => {
    try {
      const params = {};
      if (filters.departureCity) params.depart_city = filters.departureCity;
      if (filters.arrivalCity) params.arrival_city = filters.arrivalCity;
      if (filters.date) params.date = filters.date;
      if (filters.airline) params.airline_name = filters.airline;

      const res = await axios.get("http://localhost:8000/flights/search", {
        params,
      });

      setSearchResults(res.data);
      if (res.data.length === 0) {
        setMessage("No flights found.");
      } else {
        setMessage("");
      }
    } catch (err) {
      console.error("Search error:", err);
      setMessage("Error retrieving flights.");
      setSearchResults([]);
    }
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
        {message && <p>{message}</p>}

        {searchResults.map((flight) => {
          const [date, time] = flight.depart_time.split("T");
          return (
            <div key={flight.flight_num} className="flight-card">
              <p>
                <strong>{flight.depart_city}</strong> →{" "}
                <strong>{flight.arrival_city}</strong>
              </p>
              <p>Date: {date}</p>
              <p>Time: {time.slice(0, 5)}</p>
              <p>Airline: {flight.airline_name}</p>
              <p>Capacity: {flight.capacity}</p>
              <button onClick={() => handleSelect(flight)}>Select Flight</button>
            </div>
          );
        })}
      </div>
    </div>
  );
};

export default Search;
