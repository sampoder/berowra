module.exports = {
  purge: [
    './templates/**/*.html',
    './templates/api.html',
  ],
  theme: {
    fontFamily: {
      display: ["Roboto Mono", "Menlo", "monospace"],
      body: ["Roboto Mono", "Menlo", "monospace"],
    },
    extend: {
      colors: {
        primary: {
          50: "#f7fee7",
          100: "#ecfccb",
          200: "#d9f99d",
          300: "#bef264",
          400: "#a3e635",
          500: "#84cc16",
          600: "#65a30d",
          700: "#4d7c0f",
          800: "#3f6212",
          900: "#365314",
        },
        gray: {
          50: "#fafafa",
          100: "#f4f4f5",
          200: "#e4e4e7",
          300: "#d4d4d8",
          400: "#a1a1aa",
          500: "#71717a",
          600: "#52525b",
          700: "#3f3f46",
          800: "#27272a",
          900: "#18181b",
        },
      },
    },
  },
  plugins: [
    require('@tailwindcss/forms'),
    // ...
  ],
};
