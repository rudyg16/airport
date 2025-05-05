/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {

      colors:{//Predefine colors here 
        airplaneBlue: "#3484FD", 
        greenBlue:"#00CEC8",
      }
    },
  },
  plugins: [],
}

