import React, { useState } from "react";
import "./Baggage.css";
import { useNavigate } from "react-router-dom";
import axios from "axios";

const Baggage = () => {
  const navigate = useNavigate();

  const passenger = JSON.parse(localStorage.getItem("selectedPassenger")) || {};
  const flight = JSON.parse(localStorage.getItem("selectedFlight")) || {};

  const [baggageList, setBaggageList] = useState([]);
  const [weight, setWeight] = useState("");
  const [type, setType] = useState("Carry-on");

  const handleAddBag = () => {
    if (!weight || isNaN(weight)) return;
    const newBag = { type, weight: parseFloat(weight) };
    setBaggageList([...baggageList, newBag]);
    setWeight("");
    setType("Carry-on");
  };

  const handleRemoveBag = (index) => {
    const updated = baggageList.filter((_, i) => i !== index);
    setBaggageList(updated);
  };

  const handleContinue = async () => {
    try {
      // Step 1: Book ticket
      const res = await axios.post("http://localhost:8000/tickets/book", null, {
        params: {
          flight_num: flight.flight_num,
          passenger_id: passenger.pass_id,
        },
      });

      const ticket = res.data;
      localStorage.setItem("confirmedTicket", JSON.stringify(ticket));

      // Step 2: Attach baggage if any
      for (const bag of baggageList) {
        await axios.post("http://localhost:8000/luggage", null, {
          params: {
            pass_id: passenger.pass_id,
            ticket_id: ticket.ticket_id,
            weight: bag.weight,
            bagtype: bag.type,
          },
        });
      }

      localStorage.setItem("baggageInfo", JSON.stringify(baggageList));
      navigate("/confirmation");
    } catch (err) {
      console.error("Booking failed:", err);
      alert("There was an error processing the booking.");
    }
  };

  return (
    <div className="baggage-container">
      <h2>Baggage Information</h2>
      <p className="subheading">
        Adding bags for: <strong>{passenger.pass_fname} {passenger.pass_lname}</strong>
      </p>

      <div className="baggage-form">
        <label>Bag {baggageList.length + 1} Weight (lbs):</label>
        <input
          type="number"
          placeholder="Enter weight"
          value={weight}
          onChange={(e) => setWeight(e.target.value)}
        />

        <label>Bag Type:</label>
        <select value={type} onChange={(e) => setType(e.target.value)}>
          <option value="Carry-on">Carry-on</option>
          <option value="Checked">Checked</option>
          <option value="Oversized">Oversized</option>
        </select>

        <button className="add-btn" onClick={handleAddBag}>
          + Add Another Bag
        </button>
      </div>

      {baggageList.length > 0 && (
        <div className="bag-list">
          {baggageList.map((bag, index) => (
            <div key={index} className="bag-card">
              <span>{bag.type} – {bag.weight} lbs</span>
              <button onClick={() => handleRemoveBag(index)}>✕</button>
            </div>
          ))}
        </div>
      )}

      <button className="continue-btn" onClick={handleContinue}>
        Continue to Confirmation
      </button>
    </div>
  );
};

export default Baggage;
