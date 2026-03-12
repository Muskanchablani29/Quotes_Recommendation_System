import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000/api';
const RASA_URL = process.env.REACT_APP_RASA_URL || 'http://localhost:5005';

// Create axios instance
const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor to add auth token
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('access_token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

// Response interceptor to handle token refresh
api.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config;

    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true;

      try {
        const refreshToken = localStorage.getItem('refresh_token');
        const response = await axios.post(`${API_BASE_URL}/auth/token/refresh/`, {
          refresh: refreshToken,
        });

        const { access } = response.data;
        localStorage.setItem('access_token', access);

        originalRequest.headers.Authorization = `Bearer ${access}`;
        return api(originalRequest);
      } catch (refreshError) {
        localStorage.removeItem('access_token');
        localStorage.removeItem('refresh_token');
        window.location.href = '/login';
        return Promise.reject(refreshError);
      }
    }

    return Promise.reject(error);
  }
);

// Auth API
export const authAPI = {
  register: (data) => api.post('/auth/register/', data),
  login: (data) => api.post('/auth/login/', data),
  logout: () => {
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
  },
};

// Quotes API
export const quotesAPI = {
  getQuotes: (params) => api.get('/quotes/', { params }),
  getQuote: (id) => api.get(`/quotes/${id}/`),
  getRandomQuote: (category) => api.get('/quotes/random/', { params: { category } }),
  getTrendingQuotes: () => api.get('/quotes/trending/'),
  getRecommendedQuotes: () => api.get('/quotes/recommended/'),
  favoriteQuote: (id) => api.post(`/quotes/${id}/favorite/`),
  rateQuote: (id, score) => api.post(`/quotes/${id}/rate/`, { score }),
  shareQuote: (id) => api.post(`/quotes/${id}/share/`),
  getQuoteImage: (id) => api.get(`/quotes/${id}/image/`),
  searchQuotes: (query) => api.get('/search/', { params: { q: query } }),
};

// Categories API
export const categoriesAPI = {
  getCategories: () => api.get('/categories/'),
  getCategoryQuotes: (id) => api.get(`/categories/${id}/quotes/`),
};

// Authors API
export const authorsAPI = {
  getAuthors: (params) => api.get('/authors/', { params }),
  getAuthor: (id) => api.get(`/authors/${id}/`),
  getAuthorQuotes: (id) => api.get(`/authors/${id}/quotes/`),
};

// User Profile API
export const profileAPI = {
  getProfile: () => api.get('/profile/me/'),
  updateProfile: (data) => api.patch('/profile/me/', data),
  getFavorites: () => api.get('/profile/favorites/'),
  getHistory: () => api.get('/profile/history/'),
  getStats: () => api.get('/profile/stats/'),
  getMoodTrends: (days) => api.get('/profile/mood_trends/', { params: { days } }),
};

// Collections API
export const collectionsAPI = {
  getCollections: () => api.get('/collections/'),
  getCollection: (id) => api.get(`/collections/${id}/`),
  createCollection: (data) => api.post('/collections/', data),
  updateCollection: (id, data) => api.patch(`/collections/${id}/`, data),
  deleteCollection: (id) => api.delete(`/collections/${id}/`),
  addQuoteToCollection: (id, quoteId) => api.post(`/collections/${id}/add_quote/`, { quote_id: quoteId }),
  removeQuoteFromCollection: (id, quoteId) => api.post(`/collections/${id}/remove_quote/`, { quote_id: quoteId }),
};

// Chatbot API
export const chatAPI = {
  sendMessage: (message) => api.post('/chat/', { message }),
};

// Mood API
export const moodAPI = {
  detectMood: (text, intensity) => api.post('/mood/detect/', { text, intensity }),
};

// Daily Quote API
export const dailyQuoteAPI = {
  getDailyQuote: () => api.get('/daily-quote/'),
};

export default api;
