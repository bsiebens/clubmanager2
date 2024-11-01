/*
 * Copyright (c) 2024. https://github.com/bsiebens/ClubManager
 */

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
        "input-sm",
        "w-10",
        "w-12",
    ],
    theme: {
        extend: {
            screens: {
                tablet: '640px',
                laptop: '1064px',
                desktop: '1280px'
            }
        },
        fontFamily: {
            "sans": ["Ubuntu", "Noto Sans", "Catamaran", "Cabin", "Fira Sans", "Ubuntu", "Roboto"],
            "jersey": ['Graduate', 'sans-serif'],
        },
    },
    plugins: [
        require('@tailwindcss/typography'),
        require("daisyui"),
    ],
}

