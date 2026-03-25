import { defineStore } from 'pinia'
import api from '../services/api'

export const useAuthStore = defineStore('auth', {
  state: () => ({
    user: null,
    token: null,
    isAuthenticated: false,
  }),

  actions: {
    async login(email, password) {
      const response = await api.post('/auth/login', { email, password })
      this.token = response.data.access_token
      this.isAuthenticated = true
      await this.fetchUser()
      return response.data
    },

    async register(data) {
      const response = await api.post('/auth/register', data)
      this.token = response.data.access_token
      this.isAuthenticated = true
      return response.data
    },

    async fetchUser() {
      try {
        const response = await api.get('/users/me')
        this.user = response.data
      } catch (error) {
        this.logout()
      }
    },

    async logout() {
      try {
        await api.post('/auth/logout')
      } catch (e) {}
      this.user = null
      this.token = null
      this.isAuthenticated = false
    },

    async refresh() {
      try {
        const response = await api.post('/auth/refresh', {})
        this.token = response.data.access_token
        return true
      } catch {
        this.logout()
        return false
      }
    },
  },
})
