import React, { useState } from 'react'
import { Link } from 'react-router-dom';

import airplane from "../../assets/plane.svg";
import userpfp from "../../assets/userpfp.svg";


export default function Navbar(){
    const [isMenuOpen,setIsMenuOpen] = useState(false)
        {/**/}
      const navLinks =[
        {to:"/Home",label:"Home"},
        {to: "/FindFlight", label: "FindFlight" },
        {to:"/UserProfile",label:"UserProfile"},
        {to:"/Search",label:"Search"}
      ]
      return (
        <div className="w-full h-full absolute bg-white"> {/*bg-gradient-to-r from-blue-400 to bg-emerald-300"*/}
          
          <header className="flex justify-between items-center py-6 px-8 md:px-32 bg-white border-b border-gray-300">
            {/* Logo */}
            <a href="#">
              <img src={airplane} alt="airplane logo" className="w-20 hover:scale-105 transition-all" />
            </a>
    
            {/* Nav Links - hidden on smaller screens */}
            <ul className="hidden xl:flex items-center gap-12 font-semibold text-base">
              <li className="p-3 hover:bg-airplaneBlue hover:text-white rounded-md transition-all cursor-pointer">
                 Hello
              </li>
              <li className="p-3 hover:bg-airplaneBlue hover:text-white rounded-md transition-all cursor-pointer">My Flights</li>
              <li className="p-3 hover:bg-airplaneBlue hover:text-white rounded-md transition-all cursor-pointer">Search</li>
            </ul>
            <a href="#" className="hidden xl:block">
                <img src={userpfp} alt="pfp" className="w-10 hover:scale-105 transition-all" />
            </a>
            <div className="block xl:hidden">
              <i className="bx bx-menu text-5xl cursor-pointer transition-all"
                onClick={() => setIsMenuOpen(!isMenuOpen)}>{/*Whenever theitem is clicked invert the state */}
              </i>
              <div className={`absolute xl:hidden top-24 left-0 w-full
              bg-white flex flex-col items-center gap-6 font-semibold text-lg
              transform transition-transform ${isMenuOpen?"opacity-100":"opacity-0"}`}style={{transition:"transform 0.3s ease,opacity 0.3s ease"}}>
                <li className="list-none w-full text-center p-4
                hover:bg-airplaneBlue hover:text-white 
                transition-all cursor-pointer">
                    Home 
                </li>
                <li className="list-none w-full text-center p-4
                hover:bg-airplaneBlue hover:text-white 
                transition-all cursor-pointer">
                  My Flights
                </li>
                <li className="list-none w-full text-center p-4
                hover:bg-airplaneBlue hover:text-white 
                transition-all cursor-pointer">
                  Search
                </li>
              </div>
            </div>
          </header>
        </div>
      );
}