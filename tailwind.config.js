/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './templates/**/*.html',
    './test_management/templates/**/*.html',
  ],
  theme: {
    extend: {
      colors: {
        primary: '#428bca',
        'primary-dark': '#357ebd',
        secondary: '#5cb85c',
        accent: '#f0ad4e',
        background: '#f5f5f5',
        text: '#333333',
      },
      fontFamily: {
        sans: ['Inter', 'sans-serif'],
      },
    },
  },
  plugins: [],
} 