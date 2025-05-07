import { Link } from 'react-router-dom';
import './Navbar.css';

const Navbar = () => {
  return (
    <nav>
      <div className="nav-links">
        <Link to="/home">Home</Link>
        <Link to="/search">Search</Link>
        <Link to="/select-passenger">Select Passenger</Link>
        <Link to="/baggage">Baggage</Link>
        <Link to="/confirmation">Confirmation</Link>
        <Link to="/my-flights">My Flights</Link>
      </div>
      <Link to="/">Logout</Link>
    </nav>
  );
};

export default Navbar;
