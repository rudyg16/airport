import React, { useState } from "react"; // ✅ import useState
import "./Login.css";
import { FaUser, FaLock } from "react-icons/fa";
import axios from "axios";
import { useNavigate } from "react-router-dom";

function Login() {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [message, setMessage] = useState("");
  const navigate = useNavigate();


  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const res = await axios.post("http://localhost:8000/users/login", new URLSearchParams({
        username,
        password
      }), {
        headers: { "Content-Type": "application/x-www-form-urlencoded" }
      });
      setMessage(res.data.message);  // success
      const userId = res.data.user_id;
      localStorage.setItem("user_id", userId);
      navigate("/home");

    } catch (err) {

      setMessage("Login failed: " + (err.response?.data?.detail || "Unknown error"));
    }
  };

  return (
    <div className="login-page">
      <div className="login-box">
        <h2>LOGIN</h2>
        <p>{message}</p> {/* ✅ show feedback */}
        <form className="login-form" onSubmit={handleSubmit}> {/* ✅ fix submit handler */}
          <div className="input-group">
            <FaUser className="input-icon" />
            <input
              type="text"
              placeholder="Username"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
            />
          </div>
          <div className="input-group">
            <FaLock className="input-icon" />
            <input
              type="password"
              placeholder="Password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
            />
          </div>
          <button type="submit">Login Now</button>
        </form>
      </div>
    </div>
  );
}

export default Login;
