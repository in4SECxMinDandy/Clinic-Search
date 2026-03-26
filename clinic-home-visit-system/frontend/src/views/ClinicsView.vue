<template>
  <div class="min-h-screen bg-gray-50">
    <!-- Header -->
    <section class="bg-white border-b border-gray-100">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <h1 class="text-2xl font-extrabold text-gray-900">Tìm phòng khám</h1>
        <p class="text-sm text-gray-400 mt-1">Khám phá các phòng khám gần bạn</p>
      </div>
    </section>

    <!-- Location Status Banner -->
    <div v-if="locationStatus" class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 pt-6">
      <div class="flex items-center justify-between px-4 py-3 rounded-xl" :class="locationBannerClass">
        <div class="flex items-center gap-3">
          <span v-html="locationIcon"></span>
          <div>
            <p class="text-sm font-medium">{{ locationStatus.message }}</p>
            <p v-if="locationStatus.accuracy" class="text-xs opacity-75">
              Độ chính xác: ±{{ Math.round(locationStatus.accuracy) }}m
            </p>
            <p v-if="locationStatus.city" class="text-xs opacity-75">{{ locationStatus.city }}</p>
          </div>
        </div>
        <button
          v-if="locationStatus.source !== 'gps' && locationStatus.source !== 'wifi'"
          @click="retryLocation"
          class="text-xs underline hover:no-underline opacity-80 hover:opacity-100"
        >
          Thử lại
        </button>
      </div>
    </div>

    <!-- Main Content -->
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <div class="flex gap-8">
        <!-- Sidebar Filters -->
        <aside class="w-60 flex-shrink-0">
          <div class="bg-white rounded-2xl shadow-sm border border-gray-100 p-5 sticky top-20">
            <!-- Filter Header -->
            <div class="flex items-center gap-2 mb-5">
              <svg class="w-4 h-4 text-gray-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 4a1 1 0 011-1h16a1 1 0 011 1v2.586a1 1 0 01-.293.707l-6.414 6.414a1 1 0 00-.293.707V17l-4 4v-6.586a1 1 0 00-.293-.707L3.293 7.293A1 1 0 013 6.586V4z"/>
              </svg>
              <span class="font-bold text-sm text-gray-800">Bộ lọc</span>
            </div>

            <!-- Filter Fields -->
            <div class="space-y-4">
              <!-- Search -->
              <div>
                <label class="text-xs font-semibold text-gray-500 uppercase tracking-wide mb-1.5 block">Tìm kiếm</label>
                <input
                  v-model="filters.search"
                  type="text"
                  placeholder="Tên phòng khám..."
                  class="input-field text-sm"
                />
              </div>

              <!-- Radius -->
              <div>
                <label class="text-xs font-semibold text-gray-500 uppercase tracking-wide mb-1.5 block">Bán kính (km)</label>
                <input
                  v-model.number="filters.radius_km"
                  type="number"
                  min="1"
                  max="50"
                  placeholder="10"
                  class="input-field text-sm"
                />
              </div>

              <!-- Specialty -->
              <div>
                <label class="text-xs font-semibold text-gray-500 uppercase tracking-wide mb-1.5 block">Chuyên khoa</label>
                <select v-model="filters.specialty" class="input-field text-sm">
                  <option value="">Tất cả</option>
                  <option v-for="s in specialtyOptions" :key="s.value" :value="s.value">{{ s.label }}</option>
                </select>
              </div>

              <!-- Home Visit Toggle -->
              <div>
                <label class="text-xs font-semibold text-gray-500 uppercase tracking-wide mb-3 block">Khám tại nhà</label>
                <button
                  type="button"
                  @click="filters.home_visit = !filters.home_visit"
                  :class="[
                    'toggle-switch relative inline-flex h-6 w-11 items-center rounded-full transition-colors duration-200 focus:outline-none focus-visible:ring-2 focus-visible:ring-primary-400 focus-visible:ring-offset-2',
                    filters.home_visit ? 'bg-primary-600' : 'bg-gray-200'
                  ]"
                  role="switch"
                  :aria-checked="filters.home_visit"
                >
                  <span
                    :class="[
                      'toggle-switch-thumb inline-block h-5 w-5 rounded-full bg-white shadow-sm transform transition-all duration-200',
                      filters.home_visit ? 'translate-x-5' : 'translate-x-0.5'
                    ]"
                  ></span>
                </button>
              </div>

              <!-- Manual Address Input (fallback) -->
              <div>
                <label class="text-xs font-semibold text-gray-500 uppercase tracking-wide mb-1.5 block">Hoặc nhập địa chỉ</label>
                <div class="flex gap-2">
                  <input
                    v-model="manualAddress"
                    type="text"
                    placeholder="VD: 123 Nguyễn Trãi, Q1"
                    class="input-field text-sm flex-1"
                    @keyup.enter="geocodeAddress"
                  />
                  <button
                    @click="geocodeAddress"
                    class="px-3 py-2 bg-primary-600 text-white rounded-lg hover:bg-primary-700 text-sm transition-colors"
                  >
                    Tìm
                  </button>
                </div>
                <p v-if="geocodeError" class="text-xs text-red-500 mt-1">{{ geocodeError }}</p>
              </div>

              <!-- Apply Button -->
              <button
                @click="applyFilters"
                class="btn-primary w-full text-sm py-2 mt-2"
              >
                Áp dụng bộ lọc
              </button>
            </div>
          </div>
        </aside>

        <!-- Clinic List -->
        <main class="flex-1 min-w-0">
          <!-- Loading State -->
          <div v-if="loading" class="flex flex-col items-center justify-center py-16">
            <div class="loading-spinner border-t-primary-600 border-4 border-gray-200 border-t-4 rounded-full w-12 h-12 animate-spin"></div>
            <p class="mt-4 text-sm text-gray-500">Đang tải danh sách phòng khám...</p>
          </div>

          <!-- Error State -->
          <div v-else-if="error" class="flex flex-col items-center justify-center py-16 text-center">
            <div class="w-16 h-16 bg-red-50 rounded-full flex items-center justify-center mb-4">
              <svg class="w-8 h-8 text-red-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"/>
              </svg>
            </div>
            <p class="text-sm text-red-600">{{ error }}</p>
            <button @click="applyFilters" class="btn-primary mt-4 text-sm px-6 py-2">Thử lại</button>
          </div>

          <!-- Empty State -->
          <div v-else-if="clinics.length === 0" class="flex flex-col items-center justify-center py-16 text-center">
            <div class="w-16 h-16 bg-gray-100 rounded-full flex items-center justify-center mb-4">
              <svg class="w-8 h-8 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4"/>
              </svg>
            </div>
            <p class="text-gray-500 font-medium">Không tìm thấy phòng khám nào</p>
            <p class="text-sm text-gray-400 mt-1">Thử thay đổi bộ lọc hoặc từ khóa tìm kiếm</p>
          </div>

          <!-- Clinic List -->
          <div v-else class="space-y-4">
            <ClinicCard
              v-for="clinic in clinics"
              :key="clinic.id"
              :clinic="clinic"
            />
          </div>

          <!-- Pagination -->
          <div v-if="clinics.length > 0 && totalPages > 1" class="flex items-center justify-center gap-3 mt-8">
            <button
              @click="prevPage"
              :disabled="currentPage === 1"
              class="btn-secondary px-4 py-2 text-sm disabled:opacity-40 disabled:cursor-not-allowed"
            >
              Trước
            </button>
            <span class="text-sm text-gray-600">
              Trang {{ currentPage }} / {{ totalPages }}
            </span>
            <button
              @click="nextPage"
              :disabled="currentPage === totalPages"
              class="btn-secondary px-4 py-2 text-sm disabled:opacity-40 disabled:cursor-not-allowed"
            >
              Sau
            </button>
          </div>

          <!-- Results Count -->
          <p v-if="clinics.length > 0" class="text-center text-sm text-gray-400 mt-6">
            Tìm thấy {{ total }} phòng khám
          </p>
        </main>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useClinicStore } from '../stores/clinic'
import ClinicCard from '../components/ClinicCard.vue'
import { getUserLocation } from '../utils/geolocation'

const route = useRoute()
const router = useRouter()
const clinicStore = useClinicStore()

// Specialty options matching backend
const specialtyOptions = [
  { value: 'general', label: 'Đa khoa' },
  { value: 'pediatrics', label: 'Nhi khoa' },
  { value: 'cardiology', label: 'Tim mạch' },
  { value: 'dermatology', label: 'Da liễu' },
  { value: 'dentistry', label: 'Nha khoa' },
  { value: 'orthopedics', label: 'Chỉnh hình' },
]

// Filters state
const filters = ref({
  search: route.query.search || '',
  specialty: route.query.specialty || '',
  home_visit: route.query.home_visit === 'true',
  radius_km: Number(route.query.radius_km) || 10,
  page: Number(route.query.page) || 1,
})

// Location state
const locationStatus = ref(null)
const manualAddress = ref('')
const geocodeError = ref('')

// Pagination
const currentPage = ref(Number(route.query.page) || 1)
const perPage = 10
const total = ref(0)
const totalPages = computed(() => Math.ceil(total.value / perPage))

// Data state
const clinics = ref([])
const loading = ref(false)
const error = ref('')

// Location banner styling
const locationBannerClass = computed(() => {
  if (!locationStatus.value) return ''
  switch (locationStatus.value.source) {
    case 'gps': return 'bg-emerald-50 border border-emerald-200 text-emerald-800'
    case 'wifi': return 'bg-blue-50 border border-blue-200 text-blue-800'
    case 'ip': return 'bg-amber-50 border border-amber-200 text-amber-800'
    default: return 'bg-gray-50 border border-gray-200 text-gray-700'
  }
})

// Location icon
const locationIcon = computed(() => {
  if (!locationStatus.value) return ''
  switch (locationStatus.value.source) {
    case 'gps':
      return `<svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z"/>
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 11a3 3 0 11-6 0 3 3 0 016 0z"/>
      </svg>`
    case 'wifi':
      return `<svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8.111 16.404a5.5 5.5 0 017.778 0M12 20h.01m-7.08-7.071c3.904-3.905 10.236-3.905 14.14 0M1.394 9.393c5.857-5.857 15.355-5.857 21.213 0"/>
      </svg>`
    case 'ip':
      return `<svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 12a9 9 0 01-9 9m9-9a9 9 0 00-9-9m9 9H3m9 9a9 9 0 01-9-9m9 9c1.657 0 3-4.03 3-9s-1.343-9-3-9m0 18c-1.657 0-3-4.03-3-9s1.343-9 3-9m-9 9a9 9 0 019-9"/>
      </svg>`
    default:
      return `<svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/>
      </svg>`
  }
})

const initLocation = async () => {
  const result = await getUserLocation()
  if (result) {
    locationStatus.value = result
    clinicStore.setUserLocation(result.lat, result.lng, result.source)
  } else {
    locationStatus.value = {
      source: 'manual',
      message: 'Không lấy được vị trí tự động. Nhập địa chỉ để tìm phòng khám gần nhất.',
    }
  }
}

const retryLocation = () => {
  initLocation()
}

const geocodeAddress = async () => {
  if (!manualAddress.value.trim()) return
  loading.value = true
  geocodeError.value = ''
  try {
    const resp = await fetch(`/api/v1/gps/geocode?address=${encodeURIComponent(manualAddress.value)}`)
    if (!resp.ok) {
      if (resp.status === 404) {
        geocodeError.value = 'Không tìm thấy địa chỉ này. Vui lòng nhập địa chỉ cụ thể hơn.'
      } else {
        geocodeError.value = 'Lỗi khi tra cứu địa chỉ. Vui lòng thử lại.'
      }
      return
    }
    const data = await resp.json()
    if (data.lat && data.lng) {
      locationStatus.value = {
        source: 'manual',
        message: `Địa chỉ: ${manualAddress.value}`,
        lat: data.lat,
        lng: data.lng,
      }
      clinicStore.setUserLocation(data.lat, data.lng, 'manual')
      applyFilters()
    } else {
      geocodeError.value = 'Không tìm thấy địa chỉ. Vui lòng thử địa chỉ khác.'
    }
  } catch {
    geocodeError.value = 'Lỗi khi tra cứu địa chỉ. Vui lòng thử lại.'
  } finally {
    loading.value = false
  }
}

// Apply filters and fetch clinics
const applyFilters = async () => {
  loading.value = true
  error.value = ''

  try {
    // Build query params - only backend-supported params
    const queryParams = {}
    if (filters.value.search) queryParams.search = filters.value.search
    if (filters.value.specialty) queryParams.specialty = filters.value.specialty
    if (filters.value.home_visit) queryParams.supports_home_visit = true
    if (filters.value.radius_km) {
      queryParams.radius_km = Math.min(filters.value.radius_km, 50)
    }
    queryParams.page = currentPage.value
    queryParams.page_size = perPage

    // Include lat/lng if available
    if (clinicStore.filters.lat && clinicStore.filters.lng) {
      queryParams.lat = clinicStore.filters.lat
      queryParams.lng = clinicStore.filters.lng
    }

    // Update URL
    router.push({ name: 'Clinics', query: queryParams })

    // Fetch clinics
    await clinicStore.fetchClinics(queryParams)
    clinics.value = clinicStore.clinics
    total.value = clinicStore.total
  } catch (e) {
    error.value = e.response?.data?.detail || 'Không thể tải danh sách phòng khám. Vui lòng thử lại.'
  } finally {
    loading.value = false
  }
}

// Pagination
const prevPage = () => {
  if (currentPage.value > 1) {
    currentPage.value--
    applyFilters()
  }
}

const nextPage = () => {
  if (currentPage.value < totalPages.value) {
    currentPage.value++
    applyFilters()
  }
}

// Watch for route changes
watch(() => route.query, () => {
  filters.value.search = route.query.search || ''
  filters.value.specialty = route.query.specialty || ''
  filters.value.home_visit = route.query.home_visit === 'true'
  filters.value.radius_km = Number(route.query.radius_km) || 10
  currentPage.value = Number(route.query.page) || 1
}, { deep: true })

// Initial load
onMounted(async () => {
  await initLocation()
  await applyFilters()
})
</script>
