import { colors } from "./src/sytles/colors"
import { fontFamily } from "./src/sytles/fontFamily"


/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./src /**/*.{js,jsx,ts,tsx}"],
  presets: [require("nativewind/preset")],
  theme: {
    extend: {
      colors,
      fontFamily
    },
  },
  plugins: [],
}