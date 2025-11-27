/**
 * API Client for Task Manager Backend
 * 
 * Usage:
 * import apiClient from './api/apiClient';
 * 
 * // Login and set token
 * const response = await apiClient.post('/token/', { username, password });
 * apiClient.setToken(response.data.access);
 * 
 * // Make authenticated requests
 * const tasks = await apiClient.get('/tasks/');
 */

import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api';

const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Token management
let accessToken = localStorage.getItem('access_token');

apiClient.setToken = (token) => {
  accessToken = token;
  localStorage.setItem('access_token', token);
};

apiClient.clearToken = () => {
  accessToken = null;
  localStorage.removeItem('access_token');
  localStorage.removeItem('refresh_token');
};

// Request interceptor to add auth token
apiClient.interceptors.request.use(
  (config) => {
    if (accessToken) {
      config.headers.Authorization = `Bearer ${accessToken}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

// Response interceptor to handle token refresh
apiClient.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config;
    
    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true;
      
      const refreshToken = localStorage.getItem('refresh_token');
      if (refreshToken) {
        try {
          const response = await axios.post(`${API_BASE_URL}/token/refresh/`, {
            refresh: refreshToken,
          });
          
          apiClient.setToken(response.data.access);
          originalRequest.headers.Authorization = `Bearer ${response.data.access}`;
          return apiClient(originalRequest);
        } catch (refreshError) {
          apiClient.clearToken();
          window.location.href = '/login';
        }
      }
    }
    
    return Promise.reject(error);
  }
);

export default apiClient;
