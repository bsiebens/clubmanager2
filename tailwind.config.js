/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './templates/**/*.html',
    './**/templates/**/*.html',
  ],
  theme: {
    extend: {},
    fontFamily: {
      "sans": ["Ubuntu"],
    },
  },
  plugins: [
    require('@tailwindcss/typography'),
    require("daisyui"),
  ],
}

