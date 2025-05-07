/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,jsx,ts,tsx}", // Make sure all your React files are included
  ],
  theme: {
    extend: {
      fontFamily: {
        sans: ['Poppins', 'sans-serif'], // <== this sets your app-wide font
      },
      colors: {
        // Optional custom colors
        airplaneBlue: "#3484FD",
        greenBlue: "#00ECC8",
      },
    },
  },
  plugins: [],
}
