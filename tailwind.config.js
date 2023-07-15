/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./journal/**/*.{html,js}",
    "./accounts/**/*.{html,js}"            
],
  theme: {
    extend: {
      colors: {
        "mindcream": "#FFFFDB",
        "mindpurple": "#700170",
        "mindtextmetal": "#121212"

      }
    },
  },
  plugins: [],
}

