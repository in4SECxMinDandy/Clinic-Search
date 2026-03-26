import { defineStore } from 'pinia'
import api from '../services/api'

const ACCESS_STORAGE_KEY = 'access_token'

function persistAccessToken(token) {
  if (token) {
    sessionStorage.setItem(ACCESS_STORAGE_KEY, token)
  } else {
    sessionStorage.removeItem(ACCESS_STORAGE_KEY)
  }
}

function parseJwtRole(token) {
  if (!token) return null
  try {
    const payload = token.split('.')[1]
    const decoded = JSON.parse(atob(payload.replace(/-/g, '+').replace(/_/g, '/')))
    return decoded.role || null
  } catch {
    return null
  }
}

export const useAuthStore = defineStore('auth', {
  state: () => ({
    user: null,
    token: null,
    isAuthenticated: false,
    role: null,
  }),

  getters: {
    isAdmin: (state) => state.role === 'admin',
    isClinicOwner: (state) => state.role === 'clinic_owner',
    isDoctor: (state) => state.role === 'doctor',
    isPatient: (state) => state.role === 'patient',
    canManageClinics: (state) => state.role === 'admin' || state.role === 'clinic_owner',
    canManageDoctors: (state) => state.role === 'admin' || state.role === 'clinic_owner',
    canApproveBookings: (state) => state.role === 'admin' || state.role === 'clinic_owner' || state.role === 'doctor',
    canManageUsers: (state) => state.role === 'admin',
    canCancelAnyBooking: (state) => state.role === 'admin',
  },

  actions: {
    async login(email, password) {
      const response = await api.post('/auth/login', { email, password })
      this.token = response.data.access_token
      this.role = parseJwtRole(this.token)
      persistAccessToken(this.token)
      this.isAuthenticated = true
      await this.fetchUser()
      return response.data
    },

    async register(data) {
      const response = await api.post('/auth/register', data)
      this.token = response.data.access_token
      this.role = parseJwtRole(this.token)
      persistAccessToken(this.token)
      this.isAuthenticated = true
      await this.fetchUser()
      return response.data
    },

    async fetchUser() {
      try {
        const response = await api.get('/users/me')
        this.user = response.data
      } catch (error) {
        // Don't logout - just clear user data. Token is still valid for API calls.
        this.user = null
      }
    },

    async logout() {
      try {
        await api.post('/auth/logout')
      } catch (e) {}
      this.user = null
      this.token = null
      this.role = null
      persistAccessToken(null)
      this.isAuthenticated = false
    },

    async refresh() {
      try {
        const response = await api.post('/auth/refresh', {})
        this.token = response.data.access_token
        this.role = parseJwtRole(this.token)
        persistAccessToken(this.token)
        return true
      } catch {
        this.logout()
        return false
      }
    },

    setRoleFromToken(token) {
      this.role = parseJwtRole(token)
    },
  },
})
