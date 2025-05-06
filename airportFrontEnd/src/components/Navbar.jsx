import React, { useState } from 'react'
import { Link } from 'react-router-dom'
import 'boxicons/css/boxicons.min.css'

import airplane from "../assets/plane.svg"
import userpfp from "../assets/userpfp.svg"

export default function Navbar() {
  const navLinks = [
    { to: "/Home", label: "Home" },
    { to: "/FindFlight", label: "Find Flight" },
    { to: "/Search", label: "Search" }
  ]

  return (
    <div className="w-full bg-white">
      <header className="flex justify-between items-center py-6 px-8 md:px-32 bg-white border-b border-gray-300">
        {/* Logo */}
        <Link to="/Home" className="">
          <img
            src={airplane}
            alt="airplane logo"
            className="w-20 hover:scale-105 transition-all"
          />
        </Link>

        {/* Desktop Nav Links */}
        <ul className="hidden xl:flex items-center gap-12 font-semibold text-base">
          {navLinks.map(link => (
            <li key={link.to} className="p-3 hover:bg-airplaneBlue hover:text-white rounded-md transition-all">
              <Link to={link.to}>
                {link.label}
              </Link>
            </li>
          ))}
        </ul>

        {/* User Profile Icon */}
        <Link to="/UserProfile" className="hidden xl:block">
          <img
            src={userpfp}
            alt="pfp"
            className="w-10 hover:scale-105 transition-all"
          />
        </Link>
      </header>
    </div>
  )
}
