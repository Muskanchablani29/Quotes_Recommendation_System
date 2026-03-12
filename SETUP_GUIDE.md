# Enhanced Quotes Recommendation Chatbot - Setup Guide

## Prerequisites

- Python 3.10+
- Node.js 16+
- MySQL 8.0+
- Redis Server
- Rasa Open Source

## Backend Setup

### 1. Install MySQL and Create Database

```sql
CREATE DATABASE quotes_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER 'quotes_user'@'localhost' IDENTIFIED BY 'your_password';
GRANT ALL PRIVILEGES ON quotes_db.* TO 'quotes_user'@'localhost';
FLUSH PRIVILEGES;
```

### 2. Install Redis

**Windows:**
- Download Redis from: https://github.com/microsoftarchive/redis/releases
- Install and start Redis server

**Linux/Mac:**
```bash
# Ubuntu/Debian
sudo apt-get install redis-server
sudo systemctl start redis

# Mac
brew install redis
brew services start redis
```

### 3. Setup Python Environment

```bash
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Create `.env` file in backend directory:

```env
# Copy from .env.example and fill in your values
SECRET_KEY=your-secret-key-here
DEBUG=True
DB_NAME=quotes_db
DB_USER=root
DB_PASSWORD=muskan123
DB_HOST=localhost
DB_PORT=3306
```

### 5. Run Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### 6. Create Superuser

```bash
python manage.py createsuperuser
```

### 7. Import Initial Data

```bash
# Import quotes from CSV
python manage.py import_quotes --file=data/quotes.csv

# Create achievements
python manage.py create_achievements
```

### 8. Start Services

**Terminal 1 - Django Server:**
```bash
python manage.py runserver
```

**Terminal 2 - Celery Worker:**
```bash
celery -A quotes_api worker -l info
```

**Terminal 3 - Celery Beat (Scheduler):**
```bash
celery -A quotes_api beat -l info
```

**Terminal 4 - Rasa Server:**
```bash
cd chatbot_rasa
rasa run --enable-api --cors "*"
```

**Terminal 5 - Rasa Actions Server:**
```bash
cd chatbot_rasa
rasa run actions
```

## Frontend Setup

### 1. Install Dependencies

```bash
cd frontend
npm install
```

### 2. Configure API Endpoint

Update `src/config.js`:

```javascript
export const API_BASE_URL = 'http://localhost:8000/api';
export const RASA_URL = 'http://localhost:5005';
```

### 3. Start Development Server

```bash
npm start
```

The app will open at http://localhost:3000

## Testing the Setup

1. **Backend API**: http://localhost:8000/api/
2. **Admin Panel**: http://localhost:8000/admin/
3. **API Documentation**: http://localhost:8000/api/docs/
4. **Frontend**: http://localhost:3000

## Quick Start Scripts

### Windows

**start_all.bat:**
```batch
@echo off
echo Starting all services...

start cmd /k "cd backend && venv\Scripts\activate && python manage.py runserver"
timeout /t 3
start cmd /k "cd backend && venv\Scripts\activate && celery -A quotes_api worker -l info"
timeout /t 3
start cmd /k "cd backend && venv\Scripts\activate && celery -A quotes_api beat -l info"
timeout /t 3
start cmd /k "cd backend\chatbot_rasa && rasa run --enable-api --cors *"
timeout /t 3
start cmd /k "cd backend\chatbot_rasa && rasa run actions"
timeout /t 3
start cmd /k "cd frontend && npm start"

echo All services started!
```

### Linux/Mac

**start_all.sh:**
```bash
#!/bin/bash

echo "Starting all services..."

# Start Django
cd backend
source venv/bin/activate
python manage.py runserver &

# Start Celery Worker
celery -A quotes_api worker -l info &

# Start Celery Beat
celery -A quotes_api beat -l info &

# Start Rasa
cd chatbot_rasa
rasa run --enable-api --cors "*" &
rasa run actions &

# Start Frontend
cd ../../frontend
npm start &

echo "All services started!"
```

## API Endpoints

### Authentication
- `POST /api/auth/register/` - Register new user
- `POST /api/auth/login/` - Login
- `POST /api/auth/token/refresh/` - Refresh JWT token

### Quotes
- `GET /api/quotes/` - List quotes (with pagination, search, filters)
- `GET /api/quotes/{id}/` - Get quote details
- `GET /api/quotes/random/` - Get random quote
- `GET /api/quotes/trending/` - Get trending quotes
- `GET /api/quotes/recommended/` - Get personalized recommendations
- `POST /api/quotes/{id}/favorite/` - Toggle favorite
- `POST /api/quotes/{id}/rate/` - Rate quote
- `POST /api/quotes/{id}/share/` - Track share
- `GET /api/quotes/{id}/image/` - Generate quote image

### Categories & Authors
- `GET /api/categories/` - List categories
- `GET /api/categories/{id}/quotes/` - Get quotes by category
- `GET /api/authors/` - List authors
- `GET /api/authors/{id}/quotes/` - Get quotes by author

### User Profile
- `GET /api/profile/me/` - Get current user profile
- `GET /api/profile/favorites/` - Get user favorites
- `GET /api/profile/history/` - Get view history
- `GET /api/profile/stats/` - Get user statistics
- `GET /api/profile/mood_trends/` - Get mood trends

### Collections
- `GET /api/collections/` - List collections
- `POST /api/collections/` - Create collection
- `POST /api/collections/{id}/add_quote/` - Add quote to collection
- `POST /api/collections/{id}/remove_quote/` - Remove quote from collection

### Chatbot & Mood
- `POST /api/chat/` - Chat with bot
- `POST /api/mood/detect/` - Detect mood from text

### Utilities
- `GET /api/daily-quote/` - Get daily quote
- `GET /api/search/?q=query` - Search quotes

## Features Implemented

### ✅ Phase 1 - Core Enhancements
- [x] MySQL Database with comprehensive models
- [x] User authentication with JWT
- [x] User profiles and personalization
- [x] Quote favorites and history
- [x] Advanced sentiment analysis
- [x] Mood detection and tracking

### ✅ Phase 2 - Advanced Features
- [x] Recommendation engine
- [x] Rating system
- [x] Comments and discussions
- [x] Collections (user-created)
- [x] Advanced search and filtering
- [x] Analytics tracking
- [x] Caching with Redis

### ✅ Phase 3 - Premium Features
- [x] Gamification (points, streaks, achievements)
- [x] Daily quotes via email
- [x] Notification system
- [x] Premium subscriptions
- [x] Quote image generation
- [x] Trending quotes
- [x] Background tasks with Celery

### 🚧 Phase 4 - To Be Implemented
- [ ] Mobile app (React Native)
- [ ] Social sharing integration
- [ ] Voice input/output
- [ ] AI quote generation (OpenAI)
- [ ] SMS notifications (Twilio)
- [ ] Payment integration (Stripe)
- [ ] Social authentication (Google, Facebook)
- [ ] Push notifications
- [ ] Browser extension
- [ ] Public API with rate limiting

## Environment Variables Reference

See `.env.example` for all available configuration options.

## Troubleshooting

### MySQL Connection Error
- Ensure MySQL is running
- Check database credentials in `.env`
- Verify database exists

### Redis Connection Error
- Ensure Redis server is running
- Check Redis URL in `.env`

### Rasa Server Not Responding
- Train Rasa model: `rasa train`
- Check Rasa is running on port 5005

### Celery Tasks Not Running
- Ensure Redis is running
- Check Celery worker is started
- Check Celery beat is started for scheduled tasks

## Production Deployment

### Security Checklist
- [ ] Set `DEBUG=False`
- [ ] Change `SECRET_KEY`
- [ ] Configure `ALLOWED_HOSTS`
- [ ] Use strong database passwords
- [ ] Enable HTTPS
- [ ] Configure CORS properly
- [ ] Set up proper logging
- [ ] Configure email settings
- [ ] Set up database backups

### Recommended Stack
- **Web Server**: Nginx
- **WSGI Server**: Gunicorn
- **Database**: MySQL 8.0+
- **Cache**: Redis
- **Task Queue**: Celery with Redis
- **Hosting**: AWS, DigitalOcean, or Heroku

## Support

For issues and questions, please check the documentation or create an issue in the repository.

## License

MIT License
