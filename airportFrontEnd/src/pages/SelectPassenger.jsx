import React, { useEffect, useState } from "react";
import "./SelectPassenger.css";
import { useNavigate } from "react-router-dom";
import axios from "axios";

const SelectPassenger = () => {
  const navigate = useNavigate();
  const userId = localStorage.getItem("user_id");

  const [passengers, setPassengers] = useState([]);
  const [selectedPassengerId, setSelectedPassengerId] = useState(null);

  const [formData, setFormData] = useState({
    pass_fname: "",
    pass_lname: "",
    pass_passportID: "",
    state_ID: "",
    pass_email: "",
  });

  useEffect(() => {
    if (!userId) {
      alert("Please log in first.");
      navigate("/");
      return;
    }

    fetchPassengers();
  }, [userId]);

  const fetchPassengers = async () => {
    try {
      const res = await axios.get(`http://localhost:8000/passengers/by-user/${userId}`);
      setPassengers(res.data);
    } catch (err) {
      console.error("Failed to fetch passengers", err);
    }
  };

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData((prev) => ({ ...prev, [name]: value }));
  };

  const handleAddPassenger = async () => {
    const { pass_fname, pass_lname, pass_passportID, state_ID, pass_email } = formData;
    if (!pass_fname || !pass_lname || !pass_passportID || !state_ID || !pass_email) {
      alert("Please fill out all fields.");
      return;
    }

    try {
      await axios.post("http://localhost:8000/passengers", null, {
        params: {
          ...formData,
          user_id: userId,
        },
      });
      setFormData({
        pass_fname: "",
        pass_lname: "",
        pass_passportID: "",
        state_ID: "",
        pass_email: "",
      });
      fetchPassengers();
    } catch (err) {
      console.error("Error creating passenger", err);
      alert("Failed to add passenger.");
    }
  };

  const handleRemovePassenger = async (id) => {
    try {
      await axios.delete(`http://localhost:8000/passengers/${id}`, {
        params: { user_id: userId },
      });
      fetchPassengers();
    } catch (err) {
      console.error("Failed to delete passenger", err);
      alert("Unable to delete passenger.");
    }
  };

  const handleEditPassenger = async (passenger) => {
    const newFirst = prompt("Edit First Name", passenger.pass_fname);
    const newLast = prompt("Edit Last Name", passenger.pass_lname);
    if (!newFirst || !newLast) return;

    try {
      await axios.patch(`http://localhost:8000/passengers/${passenger.pass_id}`, null, {
        params: {
          user_id: userId,
          pass_fname: newFirst,
          pass_lname: newLast,
        },
      });
      fetchPassengers();
    } catch (err) {
      console.error("Error updating passenger", err);
      alert("Failed to update passenger.");
    }
  };

  const handleSelectPassenger = (id) => {
    setSelectedPassengerId(id);
  };

  const handleContinue = () => {
    const passenger = passengers.find((p) => p.pass_id === selectedPassengerId);
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
            key={passenger.pass_id}
            className={`passenger-card ${selectedPassengerId === passenger.pass_id ? "selected" : ""}`}
            onClick={() => handleSelectPassenger(passenger.pass_id)}
          >
            {passenger.pass_fname} {passenger.pass_lname}
            <div className="passenger-actions">
              <button onClick={(e) => { e.stopPropagation(); handleEditPassenger(passenger); }}>✎</button>
              <button onClick={(e) => { e.stopPropagation(); handleRemovePassenger(passenger.pass_id); }}>✕</button>
            </div>
          </div>
        ))}
      </div>

      <div className="add-passenger-form">
        <input name="pass_fname" value={formData.pass_fname} onChange={handleInputChange} placeholder="First Name" />
        <input name="pass_lname" value={formData.pass_lname} onChange={handleInputChange} placeholder="Last Name" />
        <input name="pass_passportID" value={formData.pass_passportID} onChange={handleInputChange} placeholder="Passport ID" />
        <input name="state_ID" value={formData.state_ID} onChange={handleInputChange} placeholder="State ID" />
        <input name="pass_email" value={formData.pass_email} onChange={handleInputChange} placeholder="Email" />
        <button onClick={handleAddPassenger}>Add Passenger</button>
      </div>

      <button className="continue-btn" onClick={handleContinue}>
        Continue to Baggage
      </button>
    </div>
  );
};

export default SelectPassenger;
