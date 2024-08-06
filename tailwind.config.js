/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './templates/**/*.html',
    './**/templates/**/*.html',
  ],
  theme: {
    extend: {},
    fontFamily: {
      "sans": ["Ubuntu", "Catamaran", "Cabin", "Fira Sans", "Roboto", "Noto Sans"],
    },
  },
  plugins: [
    require('@tailwindcss/typography'),
    require("daisyui"),
  ],
}

