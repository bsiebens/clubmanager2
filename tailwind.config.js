/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './templates/**/*.html',
    './**/templates/**/*.html',
  ],
  safelist: [
    "checkbox-sm",
    "file-input-sm",
    "select-sm",
    "file-input-sm",
    "checkbox-xs",
    "file-input-xs",
    "input-xs",
    "select-xs",
  ],
  theme: {
    extend: {},
    fontFamily: {
      "sans": ["Catamaran", "Noto Sans", "Catamaran", "Cabin", "Fira Sans", "Ubuntu", "Roboto"],
    },
  },
  plugins: [
    require('@tailwindcss/typography'),
    require("daisyui"),
  ],
}

