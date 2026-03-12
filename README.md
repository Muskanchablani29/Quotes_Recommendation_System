# Enhanced Quotes Recommendation Chatbot 🤖💬

An advanced AI-powered chatbot that uses Natural Language Processing (NLP) to understand user queries, detect moods, and recommend personalized quotes with gamification, social features, and premium capabilities.

## 🚀 New Features & Enhancements

### ✨ Core Features
- **AI-Powered Chatbot** - Rasa-based NLP for intelligent conversations
- **Mood Detection** - Advanced sentiment analysis with VADER & TextBlob
- **Personalized Recommendations** - ML-based quote suggestions
- **Multi-language Support** - Detect and respond in user's language
- **Real-time Search** - Full-text search across quotes, authors, and tags

### 👤 User Features
- **User Authentication** - JWT-based secure authentication
- **User Profiles** - Customizable profiles with avatars
- **Favorites System** - Save and organize favorite quotes
- **View History** - Track all viewed quotes
- **Collections** - Create custom quote collections
- **Mood Tracking** - Log and visualize mood trends over time

### 🎮 Gamification
- **Points System** - Earn points for activities
- **Achievements** - Unlock badges and rewards
- **Daily Streaks** - Maintain login streaks for bonuses
- **Leaderboards** - Compete with other users
- **Levels & Rewards** - Progress through levels

### 💎 Premium Features
- **Premium Subscriptions** - Stripe payment integration
- **Exclusive Quotes** - Access premium-only content
- **Ad-Free Experience** - No advertisements
- **Priority Support** - Faster response times
- **Custom Categories** - Create personal categories

### 📊 Analytics & Insights
- **User Dashboard** - Personal statistics and insights
- **Mood Trends** - Visualize emotional patterns
- **Activity Tracking** - Monitor engagement metrics
- **Popular Quotes** - Trending and most-liked quotes
- **Author Analytics** - Most quoted authors

### 🔔 Notifications
- **Daily Quotes** - Email delivery at custom times
- **Achievement Alerts** - Instant notifications for unlocks
- **Weekly Digest** - Summary of activity
- **Push Notifications** - Real-time updates (planned)
- **SMS Quotes** - Text message delivery (planned)

### 🎨 UI/UX Enhancements
- **Dark/Light Mode** - Theme customization
- **Responsive Design** - Mobile-friendly interface
- **Quote Cards** - Shareable image generation
- **Social Sharing** - Share to Twitter, Facebook, Instagram
- **Voice Input** - Speech-to-text support (planned)
- **Accessibility** - WCAG 2.1 compliant

### 🔧 Technical Features
- **MySQL Database** - Robust data storage
- **Redis Caching** - Fast data retrieval
- **Celery Tasks** - Background job processing
- **API Documentation** - Swagger/OpenAPI docs
- **Rate Limiting** - API throttling
- **Security** - HTTPS, CORS, CSRF protection

## 📁 Enhanced Project Structure

```
SmartBridge/
├── backend/
│   ├── chatbot_rasa/          # Rasa NLP engine
│   │   ├── actions/           # Custom Rasa actions
│   │   ├── data/              # Training data
│   │   ├── models/            # Trained models
│   │   └── config.yml         # Rasa configuration
│   ├── quotes/                # Main Django app
│   │   ├── management/        # Custom commands
│   │   │   └── commands/
│   │   │       ├── import_quotes.py
│   │   │       └── create_achievements.py
│   │   ├── models.py          # Database models (15+ models)
│   │   ├── serializers.py     # DRF serializers
│   │   ├── views.py           # API views
│   │   ├── urls.py            # URL routing
│   │   ├── admin.py           # Admin panel config
│   │   ├── tasks.py           # Celery tasks
│   │   └── utils.py           # Utility functions
│   ├── quotes_api/            # Django project
│   │   ├── settings.py        # Enhanced settings
│   │   ├── celery.py          # Celery config
│   │   └── urls.py            # Main URL config
│   ├── data/                  # Quotes dataset
│   ├── media/                 # User uploads
│   ├── logs/                  # Application logs
│   ├── requirements.txt       # Python dependencies
│   ├── .env.example           # Environment template
│   └── manage.py              # Django management
├── frontend/                  # React application
│   ├── src/
│   │   ├── components/        # React components
│   │   ├── pages/             # Page components
│   │   ├── services/          # API services
│   │   ├── context/           # React context
│   │   ├── hooks/             # Custom hooks
│   │   └── utils/             # Utility functions
│   ├── public/                # Static assets
│   └── package.json           # Node dependencies
├── SETUP_GUIDE.md             # Detailed setup instructions
├── README.md                  # This file
├── start_all_enhanced.bat     # Windows startup script
└── TODO.md                    # Development roadmap
```

## 🛠️ Tech Stack

### Backend
- **Framework**: Django 4.2 + Django REST Framework
- **Database**: MySQL 8.0
- **Cache**: Redis
- **Task Queue**: Celery + Celery Beat
- **NLP Engine**: Rasa 3.6
- **Authentication**: JWT (Simple JWT)
- **API Docs**: drf-yasg (Swagger)

### NLP & AI
- **Rasa**: Intent classification & dialogue management
- **NLTK**: Natural language processing
- **TextBlob**: Sentiment analysis
- **VADER**: Social media sentiment
- **langdetect**: Language detection
- **OpenAI**: AI quote generation (optional)

### Frontend
- **Framework**: React 18
- **UI Library**: Material-UI (MUI)
- **Routing**: React Router v6
- **HTTP Client**: Axios
- **Charts**: Recharts
- **Animations**: Framer Motion
- **Notifications**: React Toastify
- **Social Sharing**: React Share

### DevOps & Tools
- **Version Control**: Git
- **Package Manager**: pip, npm
- **Environment**: python-dotenv
- **Testing**: pytest, Jest
- **Monitoring**: Sentry (optional)

## 📋 Database Models

### Core Models
1. **User** - Extended user model with profile data
2. **Author** - Quote authors with biography
3. **Category** - Quote categories
4. **Tag** - Multi-tag system
5. **Quote** - Main quote model with metadata

### User Interaction Models
6. **Favorite** - User favorites
7. **QuoteHistory** - View tracking
8. **Rating** - Quote ratings (1-5 stars)
9. **Comment** - Comments and discussions
10. **Collection** - User-created collections

### Gamification Models
11. **Achievement** - Available achievements
12. **UserAchievement** - Earned achievements
13. **MoodLog** - Mood tracking

### System Models
14. **Notification** - User notifications
15. **Subscription** - Premium subscriptions
16. **Analytics** - Event tracking

## 🔌 API Endpoints

### Authentication
```
POST   /api/auth/register/           - Register new user
POST   /api/auth/login/              - User login
POST   /api/auth/token/refresh/      - Refresh JWT token
```

### Quotes
```
GET    /api/quotes/                  - List quotes (paginated)
GET    /api/quotes/{id}/             - Get quote details
GET    /api/quotes/random/           - Random quote
GET    /api/quotes/trending/         - Trending quotes
GET    /api/quotes/recommended/      - Personalized recommendations
POST   /api/quotes/{id}/favorite/    - Toggle favorite
POST   /api/quotes/{id}/rate/        - Rate quote (1-5)
POST   /api/quotes/{id}/share/       - Track share
GET    /api/quotes/{id}/image/       - Generate quote image
```

### Categories & Authors
```
GET    /api/categories/              - List categories
GET    /api/categories/{id}/quotes/  - Category quotes
GET    /api/authors/                 - List authors
GET    /api/authors/{id}/quotes/     - Author quotes
```

### User Profile
```
GET    /api/profile/me/              - Current user profile
PATCH  /api/profile/me/              - Update profile
GET    /api/profile/favorites/       - User favorites
GET    /api/profile/history/         - View history
GET    /api/profile/stats/           - User statistics
GET    /api/profile/mood_trends/     - Mood trends
```

### Collections
```
GET    /api/collections/             - List collections
POST   /api/collections/             - Create collection
GET    /api/collections/{id}/        - Collection details
POST   /api/collections/{id}/add_quote/     - Add quote
POST   /api/collections/{id}/remove_quote/  - Remove quote
```

### Chatbot & Utilities
```
POST   /api/chat/                    - Chat with bot
POST   /api/mood/detect/             - Detect mood
GET    /api/daily-quote/             - Daily quote
GET    /api/search/?q=query          - Search quotes
```

## 🚀 Quick Start

### Prerequisites
- Python 3.10+
- Node.js 16+
- MySQL 8.0+
- Redis Server

### Installation

1. **Clone repository**
```bash
git clone <repository-url>
cd SmartBridge
```

2. **Setup Backend**
```bash
cd backend
python -m venv venv
venv\Scripts\activate  # Windows
pip install -r requirements.txt
```

3. **Configure Database**
```sql
CREATE DATABASE quotes_db CHARACTER SET utf8mb4;
```

4. **Setup Environment**
```bash
cp .env.example .env
# Edit .env with your configuration
```

5. **Run Migrations**
```bash
python manage.py migrate
python manage.py createsuperuser
python manage.py import_quotes
python manage.py create_achievements
```

6. **Setup Frontend**
```bash
cd ../frontend
npm install
```

7. **Start All Services**
```bash
# Use the startup script
start_all_enhanced.bat  # Windows
```

Or start manually:
- Django: `python manage.py runserver`
- Celery Worker: `celery -A quotes_api worker -l info`
- Celery Beat: `celery -A quotes_api beat -l info`
- Rasa: `rasa run --enable-api --cors "*"`
- Rasa Actions: `rasa run actions`
- Frontend: `npm start`

## 📖 Documentation

- **Setup Guide**: See [SETUP_GUIDE.md](SETUP_GUIDE.md)
- **API Docs**: http://localhost:8000/api/docs/
- **Admin Panel**: http://localhost:8000/admin/

## 🎯 Roadmap

### Phase 1 ✅ (Completed)
- [x] MySQL database migration
- [x] User authentication & profiles
- [x] Advanced sentiment analysis
- [x] Favorites & history
- [x] Rating system
- [x] Collections
- [x] Gamification
- [x] Caching & performance

### Phase 2 🚧 (In Progress)
- [ ] Mobile app (React Native)
- [ ] Social authentication
- [ ] Payment integration
- [ ] AI quote generation
- [ ] Voice input/output
- [ ] Browser extension

### Phase 3 📅 (Planned)
- [ ] Multi-language quotes
- [ ] Community features
- [ ] Advanced analytics
- [ ] API marketplace
- [ ] White-label solution

## 🤝 Contributing

Contributions are welcome! Please read our contributing guidelines.

## 📄 License

MIT License - see LICENSE file for details

## 👥 Team

Developed by SmartBridge Team

## 📞 Support

For issues and questions:
- GitHub Issues
- Email: support@quotesbot.com
- Documentation: [SETUP_GUIDE.md](SETUP_GUIDE.md)

## 🙏 Acknowledgments

- Rasa for NLP framework
- Django & DRF communities
- React community
- All open-source contributors

---

**Version**: 2.0.0  
**Last Updated**: 2024  
**Status**: Active Development
#   Q u o t e s _ R e c o m m e n d a t i o n _ S y s t e m  
 