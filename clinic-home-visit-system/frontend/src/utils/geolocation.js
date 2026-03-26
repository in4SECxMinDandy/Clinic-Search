/**
 * Geolocation Utility
 * Tự động lấy vị trí với fallback chain: GPS Device → High Accuracy (WiFi/Cell) → IP Geolocation → Manual
 */

const IP_API_URL = 'http://ip-api.com/json/?fields=status,lat,lon,city,region,country'

function tryGPS() {
  return new Promise((resolve) => {
    if (!navigator.geolocation) return resolve(null)
    navigator.geolocation.getCurrentPosition(
      (pos) => resolve({
        lat: pos.coords.latitude,
        lng: pos.coords.longitude,
        accuracy: pos.coords.accuracy,
        altitude: pos.coords.altitude,
      }),
      () => resolve(null),
      {
        enableHighAccuracy: false,
        timeout: 10000,
        maximumAge: 60000,
      }
    )
  })
}

function tryHighAccuracy() {
  return new Promise((resolve) => {
    if (!navigator.geolocation) return resolve(null)
    navigator.geolocation.getCurrentPosition(
      (pos) => resolve({
        lat: pos.coords.latitude,
        lng: pos.coords.longitude,
        accuracy: pos.coords.accuracy,
        altitude: pos.coords.altitude,
      }),
      () => resolve(null),
      {
        enableHighAccuracy: true,
        timeout: 15000,
        maximumAge: 0,
      }
    )
  })
}

async function tryIPGeolocation() {
  try {
    const resp = await fetch(IP_API_URL)
    const data = await resp.json()
    if (data.status === 'success') {
      return {
        lat: data.lat,
        lng: data.lon,
        accuracy: 5000,
        city: data.city,
        region: data.region,
        country: data.country,
      }
    }
  } catch {}
  return null
}

export async function getUserLocation() {
  const TIMEOUT_GPS = 3000
  const ACCURACY_THRESHOLD = 100

  // Tầng 1: GPS Device (nhanh, ưu tiên outdoor)
  try {
    const gpsResult = await Promise.race([
      tryGPS(),
      new Promise((resolve) => setTimeout(() => resolve(null), TIMEOUT_GPS)),
    ])
    if (gpsResult) {
      if (gpsResult.accuracy < ACCURACY_THRESHOLD) {
        return { source: 'gps', ...gpsResult }
      }
    }
  } catch {}

  // Tầng 2: High Accuracy (WiFi + Cell + GPS, tốt cho indoor)
  try {
    const highResult = await Promise.race([
      tryHighAccuracy(),
      new Promise((resolve) => setTimeout(() => resolve(null), TIMEOUT_GPS + 3000)),
    ])
    if (highResult) {
      if (highResult.accuracy < ACCURACY_THRESHOLD) {
        return { source: 'wifi', ...highResult }
      }
    }
  } catch {}

  // Tầng 3: IP Geolocation (fallback, ước tính đến thành phố)
  try {
    const ipResult = await tryIPGeolocation()
    if (ipResult) {
      return { source: 'ip', ...ipResult }
    }
  } catch {}

  // Tầng 4: Không lấy được vị trí → trả null (frontend sẽ hiển thị tất cả phòng khám)
  return null
}

export function getLocationSourceLabel(source) {
  const labels = {
    gps: 'GPS thiết bị',
    wifi: 'WiFi / Cell Tower',
    ip: 'Định vị IP',
    manual: 'Nhập thủ công',
  }
  return labels[source] || 'Không xác định'
}
