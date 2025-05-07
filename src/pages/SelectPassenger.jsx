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
    const updatedList = [...passengers, { id: newId, name: newPassenger }];
    setPassengers(updatedList);
    setNewPassenger("");
  };

  const handleRemovePassenger = (id) => {
    const updated = passengers.filter((p) => p.id !== id);
    setPassengers(updated);
    if (selectedPassengerId === id) setSelectedPassengerId(null);
  };

  const handleSelectPassenger = (id) => {
    setSelectedPassengerId(id);
  };

  const handleContinue = () => {
    const passenger = passengers.find((p) => p.id === selectedPassengerId);
    if (!passenger) {
      alert("Please select a passenger.");
      return;
    }
    localStorage.setItem("selectedPassenger", JSON.stringify(passenger));
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
            <button
              className="remove-btn"
              onClick={(e) => {
                e.stopPropagation();
                handleRemovePassenger(passenger.id);
              }}
            >
              ✕
            </button>
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
