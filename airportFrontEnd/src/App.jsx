import { useState } from 'react';
import {Routes, Route } from 'react-router-dom';


import Navbar from './components/Navbar'
import Home from './pages/Home'
import UserProfile from './pages/UserProfile'
import FindFlight from './pages/FindFlight'
import Search from './pages/Search'

function App() {
  return (
    <>
      <Navbar />
      <div className="min-h-screen max-w-full mx-auto ">{/*min - h - screen max-w-full mx-auto*/}
      <Routes>
        <Route path="/Home" element={<Home />} />
        <Route path="/UserProfile" element={<UserProfile />} />
        <Route path="/FindFlight" element={<FindFlight />} />
        <Route path="/Search" element={<Search />} />
      </Routes>
      </div>
    </>
  );
}

export default App
