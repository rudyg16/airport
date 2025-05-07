import React, { useState } from "react";
import "./SelectPassenger.css";
import { useNavigate } from "react-router-dom";

const SelectPassenger = () => {
  const navigate = useNavigate();

  const [passengers, setPassengers] = useState([
    { id: 1, name: "John Doe" },
    { id: 2, name: "Jane Smith" },
  ]);

  const [newPassenger, setNewPassenger] = useState("");
  const [selectedPassengerId, setSelectedPassengerId] = useState(null);

  const handleAddPassenger = () => {
    if (newPassenger.trim() === "") return;
    const newId = passengers.length + 1;
    const updatedPassengers = [...passengers, { id: newId, name: newPassenger }];
    setPassengers(updatedPassengers);
    setNewPassenger("");
  };

  const handleSelectPassenger = (id) => {
    setSelectedPassengerId(id);
  };

  const handleContinue = () => {
    if (!selectedPassengerId) {
      alert("Please select a passenger.");
      return;
    }

    const selectedPassenger = passengers.find(p => p.id === selectedPassengerId);
    localStorage.setItem("selectedPassenger", JSON.stringify(selectedPassenger));
    navigate("/baggage");
  };

  return (
    <div className="select-passenger-container">
      <h2>Select a Passenger</h2>

      <div className="passenger-list">
        {passengers.map((passenger) => (
          <div
            key={passenger.id}
            className={`passenger-card ${
              selectedPassengerId === passenger.id ? "selected" : ""
            }`}
            onClick={() => handleSelectPassenger(passenger.id)}
          >
            {passenger.name}
          </div>
        ))}
      </div>

      <div className="add-passenger-form">
        <input
          type="text"
          placeholder="Add new passenger"
          value={newPassenger}
          onChange={(e) => setNewPassenger(e.target.value)}
        />
        <button onClick={handleAddPassenger}>Add</button>
      </div>

      <button className="continue-btn" onClick={handleContinue}>
        Continue to Baggage
      </button>
    </div>
  );
};

export default SelectPassenger;
