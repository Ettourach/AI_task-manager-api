# Frontend Setup Guide

This directory contains scaffolding for a React frontend application.

## Quick Start

1. Initialize the project with Vite:
```bash
npm create vite@latest . -- --template react
```

2. Install dependencies:
```bash
npm install
npm install axios tailwindcss postcss autoprefixer
npx tailwindcss init -p
```

3. Configure Tailwind CSS in `tailwind.config.js`:
```javascript
/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {},
  },
  plugins: [],
}
```

4. Add Tailwind directives to `src/index.css`:
```css
@tailwind base;
@tailwind components;
@tailwind utilities;
```

5. Start the development server:
```bash
npm run dev
```

## Project Structure

```
frontend/
├── src/
│   ├── components/
│   │   ├── TaskList.jsx      # Task list component
│   │   └── AISuggest.jsx     # AI suggestion component
│   ├── api/
│   │   └── apiClient.js      # Axios API client
│   ├── App.jsx
│   ├── main.jsx
│   └── index.css
├── package.json
└── README.md
```

## Available Scripts

- `npm run dev` - Start development server
- `npm run build` - Build for production
- `npm run preview` - Preview production build

## API Integration

The API client is configured to connect to the Django backend at `http://localhost:8000/api/`.
Make sure to set the JWT token for authenticated requests.
