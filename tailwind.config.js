/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./main/templates/**/*.html",
  ],
  theme: {
    extend: {
      colors: {
        warmcream: '#FAF3E0',
        slateblueSoft: '#7B8FA1',
        periwinkle: '#B4B4FF'
      },
      fontFamily: {
        poppins: ['Poppins', 'sans-serif'],
        inter: ['Inter', 'sans-serif']
      }
    },
  },
  plugins: [],
} 