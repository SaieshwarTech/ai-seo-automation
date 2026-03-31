/** @type {import('tailwindcss').Config} */
export default {
  content: ["./index.html", "./src/**/*.{js,ts,jsx,tsx}"],
  theme: {
    extend: {
      colors: {
        panel: "#0f172a",
        frame: "#0b1220",
        accent: "#00e7b3",
        accentSoft: "#00b4ff"
      },
      boxShadow: {
        glow: "0 0 60px rgba(0, 231, 179, 0.2)"
      },
      fontFamily: {
        display: ["Space Grotesk", "sans-serif"],
        body: ["Manrope", "sans-serif"]
      }
    }
  },
  plugins: []
};

