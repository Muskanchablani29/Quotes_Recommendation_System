# Quotes Chatbot Frontend

React-based chat interface for the Quotes Recommendation Chatbot.

## Features

- Modern, responsive chat interface
- Quick reply buttons for common queries
- Real-time message display
- Loading states
- Dark mode support
- Smooth animations

## Setup

1. Install dependencies:
   ```bash
   npm install
   ```

2. Start the development server:
   ```bash
   npm start
   ```

3. Open [http://localhost:3000](http://localhost:3000) in your browser.

## API Configuration

The frontend communicates with the Django backend. Update the `API_URL` in `src/App.js` if your backend runs on a different URL.

```javascript
const API_URL = 'http://localhost:8000/api';
```

## Building for Production

```bash
npm run build
```

This will create an optimized production build in the `build` folder.

