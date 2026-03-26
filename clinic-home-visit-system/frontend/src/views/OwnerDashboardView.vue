<template>
  <div class="min-h-screen bg-gray-50 flex">
    <!-- Sidebar -->
    <aside class="w-64 bg-emerald-900 text-white flex flex-col min-h-screen fixed left-0 top-0">
      <div class="px-6 py-5 border-b border-emerald-800">
        <div class="flex items-center gap-3">
          <div class="w-9 h-9 bg-emerald-600 rounded-lg flex items-center justify-center">
            <svg class="w-5 h-5 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4"/>
            </svg>
          </div>
          <div>
            <span class="text-lg font-bold">Chủ phòng khám</span>
            <p class="text-xs text-emerald-300">ClinicSearch</p>
          </div>
        </div>
      </div>

      <nav class="flex-1 px-3 py-4 space-y-1">
        <router-link to="/owner/dashboard" class="flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm font-medium transition-colors"
          :class="$route.path === '/owner/dashboard' ? 'bg-emerald-600 text-white' : 'text-emerald-200 hover:bg-emerald-800 hover:text-white'">
          <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6"/>
          </svg>
          Dashboard
        </router-link>

        <router-link to="/owner/clinics" class="flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm font-medium transition-colors"
          :class="$route.path === '/owner/clinics' ? 'bg-emerald-600 text-white' : 'text-emerald-200 hover:bg-emerald-800 hover:text-white'">
          <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4"/>
          </svg>
          Phòng khám của tôi
        </router-link>

        <router-link to="/owner/doctors" class="flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm font-medium transition-colors"
          :class="$route.path === '/owner/doctors' ? 'bg-emerald-600 text-white' : 'text-emerald-200 hover:bg-emerald-800 hover:text-white'">
          <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"/>
          </svg>
          Bác sĩ
        </router-link>
      </nav>

      <div class="px-4 py-4 border-t border-emerald-800">
        <div class="flex items-center gap-3">
          <div class="w-8 h-8 bg-emerald-600 rounded-full flex items-center justify-center text-xs font-bold">
            {{ userInitials }}
          </div>
          <div class="flex-1 min-w-0">
            <p class="text-sm font-medium truncate">{{ user?.full_name || 'Chủ phòng khám' }}</p>
            <p class="text-xs text-emerald-300 truncate">{{ user?.email }}</p>
          </div>
          <button @click="handleLogout" class="p-1.5 rounded-lg hover:bg-emerald-800 text-emerald-300 hover:text-red-400 transition-colors" title="Đăng xuất">
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1"/>
            </svg>
          </button>
        </div>
      </div>
    </aside>

    <!-- Main Content -->
    <main class="flex-1 ml-64 min-h-screen">
      <!-- Top Bar -->
      <header class="bg-white border-b border-gray-200 sticky top-0 z-10">
        <div class="px-8 py-4 flex items-center justify-between">
          <div>
            <h1 class="text-xl font-semibold text-gray-900">Dashboard</h1>
            <p class="text-sm text-gray-500">Quản lý phòng khám của bạn</p>
          </div>
          <div class="flex items-center gap-3">
            <span class="inline-flex items-center px-2.5 py-1 rounded-full text-xs font-medium bg-emerald-100 text-emerald-700">
              <span class="w-1.5 h-1.5 rounded-full bg-emerald-500 mr-1.5"></span>
              Chủ phòng khám
            </span>
          </div>
        </div>
      </header>

      <div class="px-8 py-6">
        <!-- Loading State -->
        <div v-if="loading" class="flex items-center justify-center py-20">
          <div class="inline-block w-10 h-10 border-4 border-emerald-200 border-t-emerald-600 rounded-full animate-spin"></div>
          <p class="ml-4 text-gray-500">Đang tải dữ liệu...</p>
        </div>

        <template v-else>
          <!-- No Clinics Warning -->
          <div v-if="clinics.length === 0" class="bg-amber-50 border border-amber-200 rounded-xl p-6 mb-6">
            <div class="flex items-start gap-4">
              <div class="w-12 h-12 bg-amber-100 rounded-lg flex items-center justify-center flex-shrink-0">
                <svg class="w-6 h-6 text-amber-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"/>
                </svg>
              </div>
              <div>
                <h3 class="font-semibold text-amber-900">Bạn chưa có phòng khám nào</h3>
                <p class="mt-1 text-sm text-amber-700">Liên hệ admin để được tạo phòng khám hoặc tạo mới tại đây.</p>
                <router-link to="/owner/clinics" class="inline-flex items-center mt-3 px-4 py-2 bg-amber-600 text-white rounded-lg text-sm font-medium hover:bg-amber-700 transition-colors">
                  Tạo phòng khám mới
                </router-link>
              </div>
            </div>
          </div>

          <template v-else>
            <!-- Stats Cards -->
            <div class="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-5 gap-4 mb-6">
              <div class="bg-white rounded-xl shadow-sm border border-gray-100 p-4">
                <p class="text-xs text-gray-500 uppercase tracking-wider font-medium">Phòng khám</p>
                <p class="text-2xl font-bold text-emerald-600 mt-1">{{ clinics.length }}</p>
              </div>
              <div class="bg-white rounded-xl shadow-sm border border-gray-100 p-4">
                <p class="text-xs text-gray-500 uppercase tracking-wider font-medium">Bác sĩ</p>
                <p class="text-2xl font-bold text-blue-600 mt-1">{{ stats.total_doctors }}</p>
              </div>
              <div class="bg-white rounded-xl shadow-sm border border-gray-100 p-4">
                <div class="flex items-center gap-2 mb-1">
                  <div class="w-2 h-2 rounded-full bg-yellow-400"></div>
                  <p class="text-xs text-gray-500 uppercase tracking-wider font-medium">Đang chờ</p>
                </div>
                <p class="text-2xl font-bold text-yellow-600">{{ stats.by_status?.pending || 0 }}</p>
              </div>
              <div class="bg-white rounded-xl shadow-sm border border-gray-100 p-4">
                <div class="flex items-center gap-2 mb-1">
                  <div class="w-2 h-2 rounded-full bg-blue-400"></div>
                  <p class="text-xs text-gray-500 uppercase tracking-wider font-medium">Đã xác nhận</p>
                </div>
                <p class="text-2xl font-bold text-blue-600">{{ stats.by_status?.confirmed || 0 }}</p>
              </div>
              <div class="bg-white rounded-xl shadow-sm border border-gray-100 p-4">
                <div class="flex items-center gap-2 mb-1">
                  <div class="w-2 h-2 rounded-full bg-green-400"></div>
                  <p class="text-xs text-gray-500 uppercase tracking-wider font-medium">Hoàn thành</p>
                </div>
                <p class="text-2xl font-bold text-green-600">{{ stats.by_status?.completed || 0 }}</p>
              </div>
            </div>

            <!-- Clinics List -->
            <div class="bg-white rounded-xl shadow-sm border border-gray-100 p-6 mb-6">
              <div class="flex items-center justify-between mb-4">
                <h2 class="text-lg font-semibold text-gray-900">Phòng khám của bạn</h2>
                <router-link to="/owner/clinics" class="text-sm text-emerald-600 hover:text-emerald-700 font-medium">
                  Quản lý phòng khám
                </router-link>
              </div>
              <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                <div v-for="clinic in clinics.slice(0, 3)" :key="clinic.id" class="border border-gray-100 rounded-lg p-4 hover:border-emerald-200 transition-colors">
                  <div class="flex items-start justify-between">
                    <div>
                      <h3 class="font-medium text-gray-900">{{ clinic.name }}</h3>
                      <p class="text-sm text-gray-500 mt-1">{{ clinic.address }}</p>
                    </div>
                    <span :class="clinic.is_active ? 'bg-green-100 text-green-700' : 'bg-gray-100 text-gray-500'" class="inline-flex items-center px-2 py-0.5 rounded text-xs font-medium">
                      {{ clinic.is_active ? 'Hoạt động' : 'Không hoạt động' }}
                    </span>
                  </div>
                  <div class="mt-3 flex items-center gap-4 text-sm text-gray-500">
                    <span class="flex items-center gap-1">
                      <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"/>
                      </svg>
                      {{ clinic.doctor_count || 0 }} bác sĩ
                    </span>
                  </div>
                </div>
              </div>
            </div>

            <!-- Pending Bookings -->
            <div class="bg-white rounded-xl shadow-sm border border-gray-100 overflow-hidden">
              <div class="px-6 py-4 border-b border-gray-100 flex items-center justify-between">
                <h2 class="text-lg font-semibold text-gray-900">Lịch hẹn đang chờ xác nhận</h2>
                <span class="text-sm text-gray-500">{{ bookings.length }} lịch hẹn</span>
              </div>

              <div v-if="bookings.length === 0" class="text-center py-12">
                <div class="w-16 h-16 bg-gray-100 rounded-full flex items-center justify-center mx-auto mb-4">
                  <svg class="w-8 h-8 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z"/>
                  </svg>
                </div>
                <p class="text-gray-500">Không có lịch hẹn nào đang chờ</p>
              </div>

              <div v-else class="divide-y divide-gray-50">
                <div v-for="booking in bookings" :key="booking.id" class="px-6 py-4 flex items-center justify-between hover:bg-gray-50 transition-colors">
                  <div class="flex-1">
                    <div class="flex items-center gap-3">
                      <div class="w-10 h-10 bg-emerald-100 rounded-full flex items-center justify-center">
                        <svg class="w-5 h-5 text-emerald-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z"/>
                        </svg>
                      </div>
                      <div>
                        <p class="font-medium text-gray-900">{{ formatDate(booking.scheduled_at) }} - {{ formatTime(booking.scheduled_at) }}</p>
                        <p class="text-sm text-gray-500">
                          {{ booking.clinic_name || 'Phòng khám' }} - 
                          <span :class="booking.booking_type === 'home_visit' ? 'text-purple-600' : 'text-blue-600'">
                            {{ booking.booking_type === 'home_visit' ? 'Khám tại nhà' : 'Khám tại phòng khám' }}
                          </span>
                        </p>
                      </div>
                    </div>
                  </div>
                  <div class="flex items-center gap-2">
                    <span :class="statusClass(booking.status)" class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium">
                      {{ statusLabel(booking.status) }}
                    </span>
                    <button v-if="booking.status === 'pending'" @click="approveBooking(booking)"
                      class="px-3 py-1.5 bg-green-50 text-green-600 rounded-lg text-xs font-medium hover:bg-green-100 transition-colors">
                      Duyệt
                    </button>
                    <button v-if="booking.status === 'pending'" @click="showRejectModal(booking)"
                      class="px-3 py-1.5 bg-red-50 text-red-600 rounded-lg text-xs font-medium hover:bg-red-100 transition-colors">
                      Từ chối
                    </button>
                  </div>
                </div>
              </div>
            </div>
          </template>
        </template>
      </div>
    </main>

    <!-- Reject Modal -->
    <div v-if="rejectModal.show" class="fixed inset-0 bg-black/50 flex items-center justify-center z-50" @click.self="rejectModal.show = false">
      <div class="bg-white rounded-xl shadow-xl max-w-md w-full mx-4 overflow-hidden">
        <div class="px-6 py-4 border-b border-gray-100 flex items-center justify-between">
          <h3 class="text-lg font-semibold text-gray-900">Từ chối lịch hẹn</h3>
          <button @click="rejectModal.show = false" class="p-1 rounded-lg hover:bg-gray-100 text-gray-400 hover:text-gray-600 transition-colors">
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/>
            </svg>
          </button>
        </div>
        <div class="px-6 py-4">
          <p class="text-sm text-gray-600 mb-3">
            Bạn đang từ chối lịch hẹn. Hành động này sẽ đặt trạng thái thành <strong class="text-red-600">cancelled</strong>.
          </p>
          <label class="block text-sm font-medium text-gray-700 mb-1.5">Lý do từ chối (tùy chọn)</label>
          <textarea v-model="rejectModal.reason" rows="3" placeholder="Nhập lý do từ chối..."
            class="w-full px-3 py-2 border border-gray-200 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-red-500 focus:border-transparent resize-none"></textarea>
        </div>
        <div class="px-6 py-4 bg-gray-50 border-t border-gray-100 flex gap-2 justify-end">
          <button @click="rejectModal.show = false"
            class="px-4 py-2 border border-gray-200 text-gray-700 rounded-lg text-sm font-medium hover:bg-gray-200 transition-colors">
            Hủy
          </button>
          <button @click="confirmReject" :disabled="rejectModal.loading"
            class="px-4 py-2 bg-red-600 text-white rounded-lg text-sm font-medium hover:bg-red-700 transition-colors disabled:opacity-60">
            {{ rejectModal.loading ? 'Đang xử lý...' : 'Xác nhận từ chối' }}
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'
import api from '../services/api'

const router = useRouter()
const authStore = useAuthStore()

const user = computed(() => authStore.user)
const userInitials = computed(() => {
  const name = user.value?.full_name || 'C'
  return name.split(' ').map(w => w[0]).join('').toUpperCase().slice(0, 2)
})

const clinics = ref([])
const bookings = ref([])
const stats = ref({ by_status: {}, total_doctors: 0 })
const loading = ref(false)

const rejectModal = ref({ show: false, booking: null, reason: '', loading: false })

const statusClass = (status) => {
  const classes = {
    pending: 'bg-yellow-100 text-yellow-700',
    confirmed: 'bg-blue-100 text-blue-700',
    in_progress: 'bg-purple-100 text-purple-700',
    completed: 'bg-green-100 text-green-700',
    cancelled: 'bg-red-100 text-red-700',
    expired: 'bg-gray-100 text-gray-500',
  }
  return classes[status] || 'bg-gray-100 text-gray-700'
}

const statusLabel = (status) => {
  const labels = {
    pending: 'Đang chờ',
    confirmed: 'Đã xác nhận',
    in_progress: 'Đang khám',
    completed: 'Hoàn thành',
    cancelled: 'Đã hủy',
    expired: 'Hết hạn',
  }
  return labels[status] || status
}

const formatDate = (dt) => {
  if (!dt) return ''
  const d = new Date(dt)
  return d.toLocaleDateString('vi-VN', { day: '2-digit', month: '2-digit', year: 'numeric' })
}

const formatTime = (dt) => {
  if (!dt) return ''
  const d = new Date(dt)
  return d.toLocaleTimeString('vi-VN', { hour: '2-digit', minute: '2-digit' })
}

const fetchClinics = async () => {
  try {
    const response = await api.get('/clinics/owner/my-clinics')
    clinics.value = response.data.clinics || response.data || []
    
    // Calculate total doctors
    stats.value.total_doctors = clinics.value.reduce((sum, c) => sum + (c.doctor_count || 0), 0)
  } catch (error) {
    console.error('Error fetching clinics:', error)
  }
}

const fetchBookings = async () => {
  try {
    const response = await api.get('/bookings/clinic/owner/all')
    bookings.value = response.data.bookings || []

    // Calculate stats from bookings
    const byStatus = {}
    bookings.value.forEach(b => {
      byStatus[b.status] = (byStatus[b.status] || 0) + 1
    })
    stats.value.by_status = byStatus
  } catch (error) {
    console.error('Error fetching bookings:', error)
  }
}

const showRejectModal = (booking) => {
  rejectModal.value = { show: true, booking, reason: '', loading: false }
}

const approveBooking = async (booking) => {
  try {
    await api.put(`/bookings/clinic/${booking.clinic_id}/owner/update-status`, { status: 'confirmed' })
    await fetchBookings()
  } catch (error) {
    console.error('Error approving booking:', error)
    alert('Lỗi khi duyệt lịch hẹn: ' + (error.response?.data?.detail || error.message))
  }
}

const confirmReject = async () => {
  rejectModal.value.loading = true
  try {
    await api.put(`/bookings/clinic/${rejectModal.value.booking.clinic_id}/owner/update-status`, {
      status: 'cancelled',
      cancellation_reason: rejectModal.value.reason
    })
    rejectModal.value.show = false
    await fetchBookings()
  } catch (error) {
    console.error('Error rejecting booking:', error)
    alert('Lỗi khi từ chối lịch hẹn: ' + (error.response?.data?.detail || error.message))
  } finally {
    rejectModal.value.loading = false
  }
}

const handleLogout = async () => {
  await authStore.logout()
  router.push('/login')
}

onMounted(async () => {
  loading.value = true
  await Promise.all([fetchClinics(), fetchBookings()])
  loading.value = false
})
</script>
