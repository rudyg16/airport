import React from "react";
import "./Login.css";
import { FaUser, FaLock } from "react-icons/fa";

function Login() {
  return (
    <div className="login-page">
      <div className="login-box">
        <h2>LOGIN</h2>
        <p></p>
        <form className="login-form">
          <div className="input-group">
            <FaUser className="input-icon" />
            <input type="text" placeholder="Username" />
          </div>
          <div className="input-group">
            <FaLock className="input-icon" />
            <input type="password" placeholder="Password" />
          </div>
          <button type="submit">Login Now</button>
        </form>
      </div>
    </div>
  );
}

export default Login;
