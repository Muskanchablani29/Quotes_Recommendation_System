import React, { useState, useEffect, useRef } from 'react';
import axios from 'axios';
import './App.css';

// API URL
const API_URL = 'http://localhost:8000/api';

// ==================== AUTH HELPER ====================
const getAuthHeader = () => {
  const token = localStorage.getItem('access_token');
  return token ? { Authorization: `Bearer ${token}` } : {};
};

// ==================== MODAL COMPONENT ====================
const Modal = ({ isOpen, onClose, children, title }) => {
  if (!isOpen) return null;
  return (
    <div className="modal-overlay" onClick={onClose}>
      <div className="modal-content" onClick={e => e.stopPropagation()}>
        <div className="modal-header">
          <h2>{title}</h2>
          <button className="modal-close" onClick={onClose}>×</button>
        </div>
        <div className="modal-body">{children}</div>
      </div>
    </div>
  );
};

// ==================== NAVIGATION ====================
const Navigation = ({ user, onLoginClick, onRegisterClick, onLogout, currentView, setCurrentView, theme, toggleTheme }) => {
  return (
    <nav className="main-nav">
      <div className="nav-brand">
        <span className="nav-logo">💬</span>
        <span className="nav-title">QuotesBot</span>
      </div>
      <div className="nav-links">
        <button className={`nav-link ${currentView === 'chat' ? 'active' : ''}`} onClick={() => setCurrentView('chat')}>
          <span>💬</span> Chat
        </button>
        <button className={`nav-link ${currentView === 'quotes' ? 'active' : ''}`} onClick={() => setCurrentView('quotes')}>
          <span>📚</span> Quotes
        </button>
        <button className={`nav-link ${currentView === 'categories' ? 'active' : ''}`} onClick={() => setCurrentView('categories')}>
          <span>🏷️</span> Categories
        </button>
        {user && (
          <button className={`nav-link ${currentView === 'favorites' ? 'active' : ''}`} onClick={() => setCurrentView('favorites')}>
            <span>❤️</span> Favorites
          </button>
        )}
      </div>
      <div className="nav-actions">
        <button className="theme-toggle" onClick={toggleTheme}>
          {theme === 'light' ? '🌙' : '☀️'}
        </button>
        {user ? (
          <div className="user-menu">
            <span className="user-name">{user.username}</span>
            <button className="btn-logout" onClick={onLogout}>Logout</button>
          </div>
        ) : (
          <div className="auth-buttons">
            <button className="btn-login" onClick={onLoginClick}>Login</button>
            <button className="btn-register" onClick={onRegisterClick}>Register</button>
          </div>
        )}
      </div>
    </nav>
  );
};

// ==================== LOGIN FORM ====================
const LoginForm = ({ onLogin, onSwitchToRegister, onClose }) => {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setLoading(true);
    try {
      const response = await axios.post(`${API_URL}/auth/login/`, { username, password });
      localStorage.setItem('access_token', response.data.access);
      localStorage.setItem('refresh_token', response.data.refresh);
      onLogin(response.data.user || { username });
      onClose();
    } catch (err) {
      setError('Invalid credentials. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <form className="auth-form" onSubmit={handleSubmit}>
      <h2>Welcome Back! 👋</h2>
      {error && <div className="error-message">{error}</div>}
      <div className="form-group">
        <input type="text" placeholder="Username" value={username} onChange={e => setUsername(e.target.value)} required />
      </div>
      <div className="form-group">
        <input type="password" placeholder="Password" value={password} onChange={e => setPassword(e.target.value)} required />
      </div>
      <button type="submit" className="btn-submit" disabled={loading}>
        {loading ? 'Logging in...' : 'Login'}
      </button>
      <p className="switch-auth">
        Don't have an account? <button type="button" onClick={onSwitchToRegister}>Register</button>
      </p>
    </form>
  );
};

// ==================== REGISTER FORM ====================
const RegisterForm = ({ onRegister, onSwitchToLogin, onClose }) => {
  const [username, setUsername] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [passwordConfirm, setPasswordConfirm] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    if (password !== passwordConfirm) {
      setError('Passwords do not match!');
      return;
    }
    setLoading(true);
    try {
      await axios.post(`${API_URL}/auth/register/`, {
        username, email, password, password_confirm: passwordConfirm
      });
      onClose();
      alert('Registration successful! Please login.');
    } catch (err) {
      setError(err.response?.data?.message || 'Registration failed. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <form className="auth-form" onSubmit={handleSubmit}>
      <h2>Create Account 🎉</h2>
      {error && <div className="error-message">{error}</div>}
      <div className="form-group">
        <input type="text" placeholder="Username" value={username} onChange={e => setUsername(e.target.value)} required />
      </div>
      <div className="form-group">
        <input type="email" placeholder="Email" value={email} onChange={e => setEmail(e.target.value)} required />
      </div>
      <div className="form-group">
        <input type="password" placeholder="Password" value={password} onChange={e => setPassword(e.target.value)} required />
      </div>
      <div className="form-group">
        <input type="password" placeholder="Confirm Password" value={passwordConfirm} onChange={e => setPasswordConfirm(e.target.value)} required />
      </div>
      <button type="submit" className="btn-submit" disabled={loading}>
        {loading ? 'Creating...' : 'Register'}
      </button>
      <p className="switch-auth">
        Already have an account? <button type="button" onClick={onSwitchToLogin}>Login</button>
      </p>
    </form>
  );
};

// ==================== CHAT VIEW ====================
const ChatView = ({ user }) => {
  const [messages, setMessages] = useState([]);
  const [inputText, setInputText] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const messagesEndRef = useRef(null);

  useEffect(() => {
    const greeting = {
      sender: 'bot',
      text: "Hello! I'm your Quotes Assistant. I can help you find inspiring quotes for any mood or topic. Tell me how you're feeling or what kind of quote you'd like! 🌟",
      time: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
    };
    setMessages([greeting]);
  }, []);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  const sendMessage = async (text) => {
    const userMessage = { sender: 'user', text, time: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }) };
    setMessages(prev => [...prev, userMessage]);
    setIsLoading(true);

    try {
      const response = await axios.post(`${API_URL}/chat/`, { message: text }, { headers: getAuthHeader() });
      if (response.data.success) {
        const botMessage = { sender: 'bot', text: response.data.response, source: response.data.source, time: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }) };
        setMessages(prev => [...prev, botMessage]);
      }
    } catch (error) {
      setMessages(prev => [...prev, { sender: 'bot', text: "I'm here to help you find the perfect quote! Try asking for a motivational, love, or life quote.", time: new Date().toLocaleTimeString() }]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    if (inputText.trim() && !isLoading) {
      sendMessage(inputText);
      setInputText('');
    }
  };

  const quickReplies = [
    { emoji: '💪', text: 'motivational quote' },
    { emoji: '❤️', text: 'love quote' },
    { emoji: '🌟', text: 'inspirational quote' },
    { emoji: '🌱', text: 'life quote' },
    { emoji: '🏆', text: 'success quote' },
    { emoji: '🤝', text: 'friendship quote' },
  ];

  return (
    <div className="chat-view">
      <div className="message-list">
        {messages.map((msg, idx) => (
          <div key={idx} className={`message ${msg.sender === 'user' ? 'message-user' : 'message-bot'}`}>
            <div className="message-content">
              {msg.sender === 'bot' && <div className="bot-avatar">🤖</div>}
              <div className="message-bubble">
                <p>{msg.text}</p>
                <span className="message-time">{msg.time}</span>
              </div>
            </div>
          </div>
        ))}
        {isLoading && <div className="typing-indicator"><span>•</span><span>•</span><span>•</span></div>}
        <div ref={messagesEndRef} />
      </div>
      <div className="quick-replies">
        {quickReplies.map((reply, idx) => (
          <button key={idx} className="quick-reply-chip" onClick={() => sendMessage(reply.text)}>
            {reply.emoji} {reply.text}
          </button>
        ))}
      </div>
      <form className="message-input-container" onSubmit={handleSubmit}>
        <input type="text" className="message-input" placeholder="Type your message..." value={inputText} onChange={e => setInputText(e.target.value)} disabled={isLoading} />
        <button type="submit" className="send-button" disabled={isLoading || !inputText.trim()}>➤</button>
      </form>
    </div>
  );
};

// ==================== QUOTES VIEW ====================
const QuotesView = ({ user }) => {
  const [quotes, setQuotes] = useState([]);
  const [loading, setLoading] = useState(true);
  const [searchQuery, setSearchQuery] = useState('');

  useEffect(() => {
    fetchQuotes();
  }, []);

  const fetchQuotes = async () => {
    setLoading(true);
    try {
      const response = await axios.get(`${API_URL}/quotes/`);
      setQuotes(response.data.results || response.data);
    } catch (error) {
      console.error('Error fetching quotes:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleSearch = async () => {
    if (!searchQuery.trim()) {
      fetchQuotes();
      return;
    }
    setLoading(true);
    try {
      const response = await axios.get(`${API_URL}/search/?q=${searchQuery}`);
      setQuotes(response.data);
    } catch (error) {
      console.error('Search error:', error);
    } finally {
      setLoading(false);
    }
  };

  const addToFavorites = async (quoteId) => {
    if (!user) {
      alert('Please login to add favorites!');
      return;
    }
    try {
      await axios.post(`${API_URL}/favorites/`, { quote: quoteId }, { headers: getAuthHeader() });
      alert('Added to favorites! ❤️');
    } catch (error) {
      console.error('Error adding favorite:', error);
    }
  };

  return (
    <div className="quotes-view">
      <div className="quotes-header">
        <h2>📚 Browse Quotes</h2>
        <div className="search-box">
          <input type="text" placeholder="Search quotes..." value={searchQuery} onChange={e => setSearchQuery(e.target.value)} onKeyPress={e => e.key === 'Enter' && handleSearch()} />
          <button onClick={handleSearch}>🔍</button>
        </div>
      </div>
      {loading ? (
        <div className="loading-spinner"></div>
      ) : (
        <div className="quotes-grid">
          {quotes.map(quote => (
            <div key={quote.id} className="quote-card">
              <div className="quote-text">"{quote.text}"</div>
              <div className="quote-author">— {quote.author_name || quote.author?.name}</div>
              <div className="quote-category">{quote.category_name || quote.category?.name}</div>
              <div className="quote-actions">
                <button className="btn-favorite" onClick={() => addToFavorites(quote.id)}>❤️</button>
                <button className="btn-share" onClick={() => navigator.clipboard.writeText(`"${quote.text}" - ${quote.author_name}`)}>📤</button>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

// ==================== CATEGORIES VIEW ====================
const CategoriesView = ({ user }) => {
  const [categories, setCategories] = useState([]);
  const [selectedCategory, setSelectedCategory] = useState(null);
  const [categoryQuotes, setCategoryQuotes] = useState([]);

  useEffect(() => {
    fetchCategories();
  }, []);

  const fetchCategories = async () => {
    try {
      const response = await axios.get(`${API_URL}/categories/`);
      setCategories(response.data.results || response.data);
    } catch (error) {
      console.error('Error fetching categories:', error);
    }
  };

  const selectCategory = async (category) => {
    setSelectedCategory(category);
    try {
      const response = await axios.get(`${API_URL}/quotes/?category=${category.name}`);
      setCategoryQuotes(response.data.results || response.data);
    } catch (error) {
      console.error('Error fetching category quotes:', error);
    }
  };

  const getRandomQuote = async (categoryName) => {
    try {
      const response = await axios.get(`${API_URL}/quotes/?category=${categoryName}`);
      const quotes = response.data.results || response.data;
      if (quotes.length > 0) {
        const randomQuote = quotes[Math.floor(Math.random() * quotes.length)];
        alert(`"${randomQuote.text}"\n\n— ${randomQuote.author_name}`);
      }
    } catch (error) {
      console.error('Error:', error);
    }
  };

  return (
    <div className="categories-view">
      <h2>🏷️ Browse by Category</h2>
      <div className="categories-grid">
        {categories.map(cat => (
          <div key={cat.id} className="category-card" onClick={() => selectCategory(cat)} style={{ borderColor: cat.color }}>
            <div className="category-icon" style={{ background: cat.color }}>{cat.name[0]}</div>
            <h3>{cat.name}</h3>
            <p>{cat.description || `${cat.quote_count || 0} quotes`}</p>
            <button className="btn-get-quote" onClick={(e) => { e.stopPropagation(); getRandomQuote(cat.name); }}>Get Random Quote</button>
          </div>
        ))}
      </div>
      {selectedCategory && (
        <div className="category-quotes">
          <h3>{selectedCategory.name} Quotes</h3>
          <div className="quotes-list">
            {categoryQuotes.slice(0, 5).map(quote => (
              <div key={quote.id} className="quote-item">
                <p>"{quote.text}"</p>
                <span>— {quote.author_name}</span>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
};

// ==================== FAVORITES VIEW ====================
const FavoritesView = ({ user }) => {
  const [favorites, setFavorites] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (user) fetchFavorites();
  }, [user]);

  const fetchFavorites = async () => {
    setLoading(true);
    try {
      const response = await axios.get(`${API_URL}/favorites/`, { headers: getAuthHeader() });
      setFavorites(response.data.results || response.data);
    } catch (error) {
      console.error('Error fetching favorites:', error);
    } finally {
      setLoading(false);
    }
  };

  const removeFavorite = async (id) => {
    try {
      await axios.delete(`${API_URL}/favorites/${id}/`, { headers: getAuthHeader() });
      setFavorites(favorites.filter(f => f.id !== id));
    } catch (error) {
      console.error('Error removing favorite:', error);
    }
  };

  if (!user) {
    return <div className="favorites-view"><div className="login-prompt">Please login to view your favorites! 🔐</div></div>;
  }

  return (
    <div className="favorites-view">
      <h2>❤️ Your Favorites</h2>
      {loading ? <div className="loading-spinner"></div> : favorites.length === 0 ? (
        <div className="empty-state">No favorites yet! Start adding quotes you love. 🌟</div>
      ) : (
        <div className="favorites-list">
          {favorites.map(fav => (
            <div key={fav.id} className="favorite-card">
              <p className="favorite-quote">"{fav.quote?.text}"</p>
              <span className="favorite-author">— {fav.quote?.author_name}</span>
              <button className="btn-remove" onClick={() => removeFavorite(fav.id)}>🗑️</button>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

// ==================== MAIN APP ====================
function App() {
  const [user, setUser] = useState(null);
  const [currentView, setCurrentView] = useState('chat');
  const [theme, setTheme] = useState('light');
  const [showLoginModal, setShowLoginModal] = useState(false);
  const [showRegisterModal, setShowRegisterModal] = useState(false);

  useEffect(() => {
    const savedTheme = localStorage.getItem('theme') || 'light';
    setTheme(savedTheme);
    document.body.className = savedTheme;
    
    // Check for existing token
    const token = localStorage.getItem('access_token');
    if (token) {
      setUser({ username: 'User' }); // Simplified - would fetch user data in production
    }
  }, []);

  const toggleTheme = () => {
    const newTheme = theme === 'light' ? 'dark' : 'light';
    setTheme(newTheme);
    localStorage.setItem('theme', newTheme);
    document.body.className = newTheme;
  };

  const handleLogin = (userData) => {
    setUser(userData);
  };

  const handleLogout = () => {
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
    setUser(null);
    setCurrentView('chat');
  };

  return (
    <div className={`app ${theme}`}>
      <div className="app-background">
        <div className="bg-shape bg-shape-1"></div>
        <div className="bg-shape bg-shape-2"></div>
        <div className="bg-shape bg-shape-3"></div>
      </div>
      
      <Navigation 
        user={user} 
        onLoginClick={() => setShowLoginModal(true)}
        onRegisterClick={() => setShowRegisterModal(true)}
        onLogout={handleLogout}
        currentView={currentView}
        setCurrentView={setCurrentView}
        theme={theme}
        toggleTheme={toggleTheme}
      />

      <main className="main-content">
        {currentView === 'chat' && <ChatView user={user} />}
        {currentView === 'quotes' && <QuotesView user={user} />}
        {currentView === 'categories' && <CategoriesView user={user} />}
        {currentView === 'favorites' && <FavoritesView user={user} />}
      </main>

      <Modal isOpen={showLoginModal} onClose={() => setShowLoginModal(false)} title="Login">
        <LoginForm 
          onLogin={handleLogin} 
          onSwitchToRegister={() => { setShowLoginModal(false); setShowRegisterModal(true); }}
          onClose={() => setShowLoginModal(false)}
        />
      </Modal>

      <Modal isOpen={showRegisterModal} onClose={() => setShowRegisterModal(false)} title="Register">
        <RegisterForm 
          onRegister={() => {}}
          onSwitchToLogin={() => { setShowRegisterModal(false); setShowLoginModal(true); }}
          onClose={() => setShowRegisterModal(false)}
        />
      </Modal>
    </div>
  );
}

export default App;

