// auth.js
// Handles all authentication logic for the frontend.
// Stores JWT token and username in localStorage so the user
// stays logged in even after refreshing the page.
// Follows DRY principle — all auth logic lives here, not scattered around.

import axios from 'axios'

const API = `${import.meta.env.VITE_API_URL}/api/auth`

// Save token and username to localStorage
const saveAuth = (data) => {
    localStorage.setItem('token', data.access)
    localStorage.setItem('refresh', data.refresh)
    localStorage.setItem('username', data.username)
}

// Clear auth data on logout
export const logout = () => {
    localStorage.removeItem('token')
    localStorage.removeItem('refresh')
    localStorage.removeItem('username')
}

// Check if user is logged in
export const isLoggedIn = () => !!localStorage.getItem('token')

// Get current username
export const getUsername = () => localStorage.getItem('username')

// Register a new user
export const register = async (username, email, password) => {
    const response = await axios.post(`${API}/register/`, { username, email, password })
    saveAuth(response.data)
    return response.data
}

// Login an existing user
export const login = async (username, password) => {
    const response = await axios.post(`${API}/login/`, { username, password })
    saveAuth(response.data)
    return response.data
}