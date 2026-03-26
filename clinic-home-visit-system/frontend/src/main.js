import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import { pinia } from './pinia'
import { useAuthStore } from './stores/auth'
import { setAuthTokenAccessor, setOnAccessTokenRefreshed } from './services/api'
import './style.css'

function parseJwtRole(token) {
  if (!token) return null
  try {
    const payload = token.split('.')[1]
    return JSON.parse(atob(payload.replace(/-/g, '+').replace(/_/g, '/'))).role || null
  } catch {
    return null
  }
}

const ACCESS_STORAGE_KEY = 'access_token'

const auth = useAuthStore(pinia)
const stored = sessionStorage.getItem(ACCESS_STORAGE_KEY)
if (stored) {
  auth.token = stored
  auth.isAuthenticated = true
  auth.role = parseJwtRole(stored)
}

setAuthTokenAccessor(() => useAuthStore(pinia).token)
setOnAccessTokenRefreshed((token) => {
  const s = useAuthStore(pinia)
  s.token = token
  s.isAuthenticated = true
  s.role = parseJwtRole(token)
  try {
    sessionStorage.setItem(ACCESS_STORAGE_KEY, token)
  } catch (_) {}
})

createApp(App).use(pinia).use(router).mount('#app')
