import { useState } from 'react'
import airplane from './assets/plane.svg'
//import Navbar from './components/common/Navbar'
function HoverComps({href="",defaultImg,hoverImg,alt="image",className}){
  
  return(

  )
}
function App() {
{/**/}
  return (
    <div className="w-full h-full absolute bg-white"> {/*bg-gradient-to-r from-blue-400 to bg-emerald-300"*/}
      
      <header className="flex justify-between 
      items-center text-black py-6 px-8
      md:px-32 bg-white border-gray-950 ">
        <a href="#">
          <img src = {airplane} alt="airplane logo" className="w-20 hover:scale-105 transition-all"></img>
        </a>
        <ul className="hidden xl:flex items-center gap-12 font-semibold text-base">
          <li className="p-3 hover:bg-airplaneBlue hover:text-white rounded-md 
          transition-all cursor-pointer">
            My Flights</li>
          <li className="p-3 hover:bg-airplaneBlue hover:text-white 
          rounded-md transition-all cursor-pointer">Search</li>
          <li></li>
        </ul>

      </header>

    </div>
  )
}

export default App
