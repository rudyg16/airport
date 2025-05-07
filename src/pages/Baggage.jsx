import React, { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import "./Baggage.css";

const Baggage = () => {
  const navigate = useNavigate();
  const [passenger, setPassenger] = useState(null);
  const [bags, setBags] = useState([{ id: 1, weight: "" }]);

  useEffect(() => {
    const storedPassenger = localStorage.getItem("selectedPassenger");
    if (storedPassenger) {
      setPassenger(JSON.parse(storedPassenger));
    }
  }, []);

  const handleWeightChange = (id, value) => {
    setBags((prev) =>
      prev.map((bag) =>
        bag.id === id ? { ...bag, weight: value } : bag
      )
    );
  };

  const addBag = () => {
    setBags((prev) => [...prev, { id: prev.length + 1, weight: "" }]);
  };

  const handleSubmit = () => {
    const filledBags = bags.filter((bag) => bag.weight.trim() !== "");
    localStorage.setItem("baggageInfo", JSON.stringify(filledBags));
    navigate("/confirmation");
  };

  return (
    <div className="baggage-container">
      <h2>Baggage Information</h2>
      {passenger && (
        <p className="passenger-label">
          Adding bags for: <strong>{passenger.name}</strong>
        </p>
      )}
      {bags.map((bag) => (
        <div className="baggage-row" key={bag.id}>
          <label>Bag {bag.id} Weight (lbs):</label>
          <input
            type="number"
            value={bag.weight}
            onChange={(e) => handleWeightChange(bag.id, e.target.value)}
            min="0"
          />
        </div>
      ))}
      <button className="add-bag-btn" onClick={addBag}>
        + Add Another Bag
      </button>
      <button className="submit-baggage-btn" onClick={handleSubmit}>
        Continue to Confirmation
      </button>
    </div>
  );
};

export default Baggage;
