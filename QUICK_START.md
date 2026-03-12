# 🚀 QUICK START GUIDE - Enhanced Quotes Chatbot

## ⚡ Fast Setup (5 Minutes)

### Step 1: Install Dependencies (2 min)

```bash
# Backend
cd backend
pip install -r requirements.txt

# Frontend  
cd ../frontend
npm install
```

### Step 2: Setup Database (1 min)

```sql
-- Open MySQL and run:
CREATE DATABASE quotes_db CHARACTER SET utf8mb4;
```

### Step 3: Configure Environment (30 sec)

Create `backend/.env`:
```env
DB_NAME=quotes_db
DB_USER=root
DB_PASSWORD=muskan123
DB_HOST=localhost
DB_PORT=3306
SECRET_KEY=your-secret-key-change-this
DEBUG=True
```

### Step 4: Initialize Database (1 min)

```bash
cd backend
python manage.py migrate
python manage.py createsuperuser
python manage.py import_quotes
python manage.py create_achievements
```

### Step 5: Start Everything (30 sec)

**Option A - Use Script (Recommended):**
```bash
start_all_enhanced.bat
```

**Option B - Manual Start:**

Open 6 terminals:

```bash
# Terminal 1 - Django
cd backend
python manage.py runserver

# Terminal 2 - Celery Worker
cd backend
celery -A quotes_api worker -l info --pool=solo

# Terminal 3 - Celery Beat
cd backend
celery -A quotes_api beat -l info

# Terminal 4 - Rasa Server
cd backend/chatbot_rasa
rasa run --enable-api --cors "*"

# Terminal 5 - Rasa Actions
cd backend/chatbot_rasa
rasa run actions

# Terminal 6 - React Frontend
cd frontend
npm start
```

---

## 🌐 Access Points

Once started, access:

- **Frontend**: http://localhost:3000
- **API**: http://localhost:8000/api/
- **Admin Panel**: http://localhost:8000/admin/
- **API Docs**: http://localhost:8000/api/docs/
- **Rasa**: http://localhost:5005

---

## 🧪 Test the Features

### 1. Test Authentication
```bash
# Register
curl -X POST http://localhost:8000/api/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{"username":"testuser","email":"test@example.com","password":"testpass123"}'

# Login
curl -X POST http://localhost:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"username":"testuser","password":"testpass123"}'
```

### 2. Test Quotes API
```bash
# Get random quote
curl http://localhost:8000/api/quotes/random/

# Get trending quotes
curl http://localhost:8000/api/quotes/trending/

# Search quotes
curl http://localhost:8000/api/search/?q=motivation
```

### 3. Test Chatbot
```bash
curl -X POST http://localhost:8000/api/chat/ \
  -H "Content-Type: application/json" \
  -d '{"message":"Give me a motivational quote"}'
```

### 4. Test Mood Detection
```bash
curl -X POST http://localhost:8000/api/mood/detect/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -d '{"text":"I feel sad today","intensity":7}'
```

---

## 📱 Frontend Features to Test

1. **Register/Login** - Create account and login
2. **Browse Quotes** - View quotes by category
3. **Search** - Search for specific quotes
4. **Favorites** - Add quotes to favorites
5. **Rate Quotes** - Give 1-5 star ratings
6. **Collections** - Create custom collections
7. **Chat** - Talk to the AI chatbot
8. **Profile** - View your stats and achievements
9. **Mood Tracker** - Log your mood
10. **Daily Quote** - Get quote of the day

---

## 🎮 Gamification Features

### Earn Points:
- View quote: +1 point
- Favorite quote: +5 points
- Rate quote: +3 points
- Share quote: +10 points
- Comment: +5 points
- Daily login: +10 points

### Unlock Achievements:
- ⭐ First Favorite (1 favorite)
- 📚 Quote Collector (10 favorites)
- 🏆 Quote Master (50 favorites)
- ⭐ Active Rater (10 ratings)
- 💬 Commentator (5 comments)
- 💰 Point Earner (100 points)
- 🔥 Week Streak (7 days)
- 🔥🔥 Month Streak (30 days)

---

## 🔧 Troubleshooting

### MySQL Connection Error
```bash
# Check MySQL is running
mysql -u root -p

# Verify database exists
SHOW DATABASES;
```

### Redis Not Running
```bash
# Windows: Start Redis server
redis-server

# Check Redis connection
redis-cli ping
# Should return: PONG
```

### Rasa Model Not Found
```bash
cd backend/chatbot_rasa
rasa train
```

### Port Already in Use
```bash
# Kill process on port 8000 (Windows)
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# Kill process on port 3000
netstat -ano | findstr :3000
taskkill /PID <PID> /F
```

### Celery Not Working on Windows
```bash
# Use --pool=solo flag
celery -A quotes_api worker -l info --pool=solo
```

---

## 📊 Admin Panel

Access: http://localhost:8000/admin/

Login with superuser credentials created earlier.

**What you can do:**
- Manage users
- Add/edit quotes
- Create categories
- Manage authors
- View analytics
- Configure achievements
- Monitor subscriptions

---

## 🎯 Key API Endpoints

### Public (No Auth Required)
```
GET  /api/quotes/                    # List quotes
GET  /api/quotes/random/             # Random quote
GET  /api/quotes/trending/           # Trending quotes
GET  /api/categories/                # List categories
GET  /api/authors/                   # List authors
GET  /api/daily-quote/               # Daily quote
POST /api/chat/                      # Chat with bot
POST /api/auth/register/             # Register
POST /api/auth/login/                # Login
```

### Authenticated (Requires Token)
```
GET  /api/quotes/recommended/        # Personalized quotes
POST /api/quotes/{id}/favorite/      # Toggle favorite
POST /api/quotes/{id}/rate/          # Rate quote
GET  /api/profile/me/                # User profile
GET  /api/profile/favorites/         # User favorites
GET  /api/profile/stats/             # User statistics
POST /api/collections/               # Create collection
POST /api/mood/detect/               # Detect mood
```

---

## 💡 Pro Tips

1. **Use Redis** for better performance (caching)
2. **Enable Celery** for background tasks
3. **Check logs** in `backend/logs/` for debugging
4. **Use API docs** at `/api/docs/` for testing
5. **Import sample data** with `import_quotes` command
6. **Create achievements** with `create_achievements` command
7. **Monitor Celery** tasks in separate terminal
8. **Use admin panel** for quick data management

---

## 📚 Documentation

- **Full Setup**: See `SETUP_GUIDE.md`
- **Implementation Details**: See `IMPLEMENTATION_SUMMARY.md`
- **Project Overview**: See `README.md`
- **API Docs**: http://localhost:8000/api/docs/

---

## 🆘 Need Help?

1. Check `SETUP_GUIDE.md` for detailed instructions
2. Review error logs in console
3. Verify all services are running
4. Check database connection
5. Ensure Redis is running
6. Verify Rasa model is trained

---

## ✅ Success Checklist

- [ ] MySQL database created
- [ ] Dependencies installed
- [ ] Migrations run successfully
- [ ] Sample data imported
- [ ] Achievements created
- [ ] Superuser created
- [ ] Django server running (port 8000)
- [ ] Celery worker running
- [ ] Celery beat running
- [ ] Rasa server running (port 5005)
- [ ] Rasa actions running
- [ ] Frontend running (port 3000)
- [ ] Can access admin panel
- [ ] Can register/login
- [ ] Can view quotes
- [ ] Can chat with bot

---

**🎉 You're all set! Enjoy your enhanced quotes chatbot!**
