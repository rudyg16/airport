// src/App.jsx
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Navbar from "./components/Navbar";
import Login from "./pages/Login";
import Home from "./pages/Home";
import Search from "./pages/Search";
import SelectPassenger from "./pages/SelectPassenger";
import Baggage from "./pages/Baggage";
import Confirmation from "./pages/Confirmation";
import MyFlights from "./pages/MyFlights";

function App() {
  return (
    <Router>
      <Navbar />
      <Routes>
        <Route path="/" element={<Login />} />
        <Route path="/home" element={<Home />} />
        <Route path="/search" element={<Search />} />
        <Route path="/select-passenger" element={<SelectPassenger />} />
        <Route path="/baggage" element={<Baggage />} />
        <Route path="/confirmation" element={<Confirmation />} />
        <Route path="/my-flights" element={<MyFlights />} />
      </Routes>
    </Router>
  );
}

export default App;
