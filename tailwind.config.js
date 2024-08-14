/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './templates/**/*.html',
    './**/templates/**/*.html',
  ],
  safelist: [
    "checkbox-sm",
    "file-input-sm",
    "checkbox-xs",
    "file-input-xs",
    "input-xs",
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

