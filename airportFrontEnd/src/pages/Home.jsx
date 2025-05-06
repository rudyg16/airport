import React, { useState } from 'react'

import plane from "../assets/clouds.jpg"

export default function Home(){
    return(
        <div className="min-h-screen flex  justify-center ">
            
                <img src={plane} className="max-h-96"></img>
                <div>
                    
                </div>
        </div>
    );
}