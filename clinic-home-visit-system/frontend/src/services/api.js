import axios from 'axios'

const ACCESS_STORAGE_KEY = 'access_token'

const api = axios.create({
  baseURL: '/api/v1',
  withCredentials: true,
  timeout: 30000,
})

/** Set in main.js so we avoid circular imports with the auth store. */
let getAccessToken = () => null
/** Called after refresh so Pinia + retry use the new access token. */
let onAccessTokenRefreshed = () => {}

export function setAuthTokenAccessor(fn) {
  getAccessToken = typeof fn === 'function' ? fn : () => null
}

export function setOnAccessTokenRefreshed(fn) {
  onAccessTokenRefreshed = typeof fn === 'function' ? fn : () => {}
}

function isAuthBypassUrl(url) {
  if (!url) return false
  return (
    url.includes('auth/login') ||
    url.includes('auth/register') ||
    url.includes('auth/refresh')
  )
}

api.interceptors.request.use((config) => {
  const t = getAccessToken()
  if (t) {
    config.headers.Authorization = `Bearer ${t}`
  }
  return config
})

api.interceptors.response.use(
  response => response,
  async error => {
    const status = error.response?.status
    const cfg = error.config
    if (status !== 401 || !cfg || cfg.__authRetry) {
      return Promise.reject(error)
    }
    const url = cfg.url || ''
    if (isAuthBypassUrl(url)) {
      return Promise.reject(error)
    }

    cfg.__authRetry = true
    try {
      const { data } = await api.post('/auth/refresh', {})
      const next = data?.access_token
      if (next) {
        try {
          sessionStorage.setItem(ACCESS_STORAGE_KEY, next)
        } catch (_) {}
        onAccessTokenRefreshed(next)
        cfg.headers = cfg.headers || {}
        cfg.headers.Authorization = `Bearer ${next}`
      }
      return api.request(cfg)
    } catch (refreshErr) {
      try {
        sessionStorage.removeItem(ACCESS_STORAGE_KEY)
      } catch (_) {}
      if (!window.location.pathname.startsWith('/login')) {
        window.location.href = '/login'
      }
      return Promise.reject(refreshErr)
    }
  }
)

export default api
