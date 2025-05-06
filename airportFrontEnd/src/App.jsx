import { useState } from 'react';
import 'boxicons/css/boxicons.min.css';
import Navbar from './components/common/Navbar.jsx'

function App() {
  const [isMenuOpen,setIsMenuOpen] = useState(false)

    {/**/}
  return (
    <Navbar></Navbar>
  )
}

export default App
