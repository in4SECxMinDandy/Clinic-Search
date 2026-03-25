<template>
  <div class="min-h-screen bg-gray-50">
    <nav class="bg-white shadow-sm">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="flex justify-between h-16">
          <div class="flex items-center">
            <router-link to="/" class="text-xl font-bold text-indigo-600">ClinicSearch</router-link>
          </div>
          <div class="flex items-center space-x-4">
            <router-link to="/clinics" class="text-gray-600 hover:text-indigo-600 px-3 py-2">Quay lại</router-link>
          </div>
        </div>
      </div>
    </nav>

    <main class="max-w-7xl mx-auto px-4 py-8 sm:px-6 lg:px-8">
      <div v-if="loading" class="text-center py-16">
        <div class="loading-spinner mx-auto"></div>
        <p class="mt-4 text-gray-600">Đang tải...</p>
      </div>

      <div v-else-if="clinic" class="space-y-6">
        <div class="bg-white rounded-xl shadow-lg p-8">
          <div class="flex justify-between items-start">
            <div>
              <h1 class="text-3xl font-bold text-gray-900">{{ clinic.name }}</h1>
              <p class="mt-2 text-gray-600 flex items-center">
                <svg class="w-5 h-5 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z"/>
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 11a3 3 0 11-6 0 3 3 0 016 0z"/>
                </svg>
                {{ clinic.address }}
              </p>
            </div>
            <div v-if="clinic.supports_home_visit" class="bg-green-100 text-green-700 px-4 py-2 rounded-full font-medium">
              Hỗ trợ khám tại nhà
            </div>
          </div>

          <div class="mt-6 grid grid-cols-1 md:grid-cols-3 gap-6">
            <div class="flex items-center">
              <div class="w-12 h-12 bg-indigo-100 rounded-full flex items-center justify-center">
                <svg class="w-6 h-6 text-indigo-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z"/>
                </svg>
              </div>
              <div class="ml-4">
                <p class="text-sm text-gray-500">Khoảng cách</p>
                <p class="text-lg font-semibold">{{ clinic.distance_km ? clinic.distance_km + ' km' : 'N/A' }}</p>
              </div>
            </div>

            <div class="flex items-center">
              <div class="w-12 h-12 bg-indigo-100 rounded-full flex items-center justify-center">
                <svg class="w-6 h-6 text-indigo-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"/>
                </svg>
              </div>
              <div class="ml-4">
                <p class="text-sm text-gray-500">Thời gian di chuyển</p>
                <p class="text-lg font-semibold">{{ clinic.estimated_travel_time_min ? clinic.estimated_travel_time_min + ' phút' : 'N/A' }}</p>
              </div>
            </div>

            <div class="flex items-center">
              <div class="w-12 h-12 bg-indigo-100 rounded-full flex items-center justify-center">
                <svg class="w-6 h-6 text-indigo-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11.049 2.927c.3-.921 1.603-.921 1.902 0l1.519 4.674a1 1 0 00.95.69h4.915c.969 0 1.371 1.24.588 1.81l-3.976 2.888a1 1 0 00-.363 1.118l1.518 4.674c.3.922-.755 1.688-1.538 1.118l-3.976-2.888a1 1 0 00-1.176 0l-3.976 2.888c-.783.57-1.838-.197-1.538-1.118l1.518-4.674a1 1 0 00-.363-1.118l-3.976-2.888c-.784-.57-.38-1.81.588-1.81h4.914a1 1 0 00.951-.69l1.519-4.674z"/>
                </svg>
              </div>
              <div class="ml-4">
                <p class="text-sm text-gray-500">Đánh giá</p>
                <p class="text-lg font-semibold">{{ clinic.rating ? clinic.rating.toFixed(1) + '/5' : 'Chưa có' }}</p>
              </div>
            </div>
          </div>
        </div>

        <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
          <div class="lg:col-span-2 space-y-6">
            <div class="bg-white rounded-xl shadow p-6">
              <h2 class="text-xl font-semibold mb-4">Giới thiệu</h2>
              <p class="text-gray-600">{{ clinic.description || 'Không có mô tả' }}</p>
            </div>

            <div class="bg-white rounded-xl shadow p-6">
              <h2 class="text-xl font-semibold mb-4">Chuyên khoa</h2>
              <div class="flex flex-wrap gap-2">
                <span v-for="specialty in clinic.specialties" :key="specialty" class="bg-indigo-100 text-indigo-700 px-3 py-1 rounded-full text-sm">
                  {{ specialty }}
                </span>
                <span v-if="!clinic.specialties || clinic.specialties.length === 0" class="text-gray-500">Không có thông tin</span>
              </div>
            </div>

            <div class="bg-white rounded-xl shadow p-6">
              <h2 class="text-xl font-semibold mb-4">Bác sĩ</h2>
              <div v-if="clinic.doctors && clinic.doctors.length > 0" class="space-y-4">
                <div v-for="doctor in clinic.doctors" :key="doctor.id" class="flex items-center p-4 border border-gray-200 rounded-lg">
                  <div class="w-12 h-12 bg-gray-200 rounded-full flex items-center justify-center">
                    <span class="text-xl font-semibold text-gray-600">{{ doctor.name?.charAt(0) || '?' }}</span>
                  </div>
                  <div class="ml-4 flex-1">
                    <h3 class="font-semibold">{{ doctor.name }}</h3>
                    <p class="text-sm text-gray-500">{{ doctor.specialty }}</p>
                  </div>
                </div>
              </div>
              <p v-else class="text-gray-500">Không có thông tin bác sĩ</p>
            </div>

            <div class="bg-white rounded-xl shadow p-6">
              <h2 class="text-xl font-semibold mb-4">Đánh giá</h2>
              <div v-if="clinic.reviews && clinic.reviews.length > 0" class="space-y-4">
                <div v-for="review in clinic.reviews" :key="review.id" class="border-b border-gray-200 pb-4">
                  <div class="flex items-center mb-2">
                    <div class="flex text-yellow-400">
                      <span v-for="i in 5" :key="i">
                        <svg class="w-4 h-4" :class="i <= review.rating ? 'fill-current' : 'text-gray-300'" viewBox="0 0 20 20">
                          <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z"/>
                        </svg>
                      </span>
                    </div>
                    <span class="ml-2 text-sm text-gray-500">{{ review.user_name || 'Người dùng' }}</span>
                  </div>
                  <p class="text-gray-600">{{ review.comment }}</p>
                </div>
              </div>
              <p v-else class="text-gray-500">Chưa có đánh giá nào</p>
            </div>
          </div>

          <div class="lg:col-span-1">
            <div class="bg-white rounded-xl shadow p-6 sticky top-6">
              <h2 class="text-xl font-semibold mb-4">Đặt lịch khám</h2>
              
              <div v-if="!isLoggedIn" class="text-center py-4">
                <p class="text-gray-600 mb-4">Vui lòng đăng nhập để đặt lịch khám</p>
                <router-link to="/login" class="block w-full bg-indigo-600 text-white py-2 px-4 rounded-lg hover:bg-indigo-700 text-center">
                  Đăng nhập
                </router-link>
              </div>

              <form v-else @submit.prevent="handleBooking" class="space-y-4">
                <div>
                  <label class="label">Chọn bác sĩ</label>
                  <select v-model="bookingForm.doctor_id" class="input">
                    <option value="">Chọn bác sĩ</option>
                    <option v-for="doctor in clinic.doctors" :key="doctor.id" :value="doctor.id">
                      {{ doctor.name }} - {{ doctor.specialty }}
                    </option>
                  </select>
                </div>

                <div>
                  <label class="label">Ngày khám</label>
                  <input v-model="bookingForm.scheduled_date" type="date" :min="minDate" class="input" required />
                </div>

                <div>
                  <label class="label">Giờ khám</label>
                  <select v-model="bookingForm.scheduled_time" class="input" required>
                    <option value="">Chọn giờ</option>
                    <option v-for="time in availableTimes" :key="time" :value="time">{{ time }}</option>
                  </select>
                </div>

                <div>
                  <label class="flex items-center cursor-pointer">
                    <input v-model="bookingForm.is_home_visit" type="checkbox" class="mr-2" />
                    <span class="text-sm">Khám tại nhà (+{{ clinic.home_visit_fee ? clinic.home_visit_fee + 'đ' : 'Phí dịch vụ' }})</span>
                  </label>
                </div>

                <div>
                  <label class="label">Ghi chú</label>
                  <textarea v-model="bookingForm.notes" class="input" rows="3" placeholder="Mô tả triệu chứng..."></textarea>
                </div>

                <div v-if="bookingError" class="bg-red-50 text-red-600 p-3 rounded-lg text-sm">
                  {{ bookingError }}
                </div>

                <div v-if="bookingSuccess" class="bg-green-50 text-green-600 p-3 rounded-lg text-sm">
                  {{ bookingSuccess }}
                </div>

                <button type="submit" :disabled="bookingLoading" class="w-full bg-indigo-600 text-white py-3 px-4 rounded-lg hover:bg-indigo-700 disabled:opacity-50">
                  {{ bookingLoading ? 'Đang đặt...' : 'Xác nhận đặt lịch' }}
                </button>
              </form>
            </div>
          </div>
        </div>
      </div>

      <div v-else class="text-center py-16">
        <p class="text-gray-600">Không tìm thấy phòng khám</p>
        <router-link to="/clinics" class="mt-4 inline-block text-indigo-600 hover:text-indigo-700">
          Quay lại danh sách
        </router-link>
      </div>
    </main>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useClinicStore } from '../stores/clinic'
import { useAuthStore } from '../stores/auth'
import api from '../services/api'

const route = useRoute()
const router = useRouter()
const clinicStore = useClinicStore()
const authStore = useAuthStore()

const clinic = ref(null)
const loading = ref(true)
const bookingError = ref('')
const bookingSuccess = ref('')
const bookingLoading = ref(false)

const bookingForm = ref({
  doctor_id: '',
  scheduled_date: '',
  scheduled_time: '',
  is_home_visit: false,
  notes: ''
})

const isLoggedIn = computed(() => authStore.isAuthenticated)

const minDate = computed(() => {
  const tomorrow = new Date()
  tomorrow.setDate(tomorrow.getDate() + 1)
  return tomorrow.toISOString().split('T')[0]
})

const availableTimes = [
  '07:00', '07:30', '08:00', '08:30', '09:00', '09:30', '10:00', '10:30',
  '11:00', '11:30', '13:00', '13:30', '14:00', '14:30', '15:00', '15:30',
  '16:00', '16:30', '17:00', '17:30', '18:00', '18:30', '19:00', '19:30'
]

const fetchClinicDetails = async () => {
  loading.value = true
  try {
    const response = await api.get(`/clinics/${route.params.id}`)
    clinic.value = response.data
  } catch (error) {
    console.error('Error fetching clinic:', error)
  } finally {
    loading.value = false
  }
}

const handleBooking = async () => {
  bookingError.value = ''
  bookingSuccess.value = ''
  bookingLoading.value = true

  try {
    const scheduledAt = `${bookingForm.value.scheduled_date}T${bookingForm.value.scheduled_time}:00`
    
    await api.post('/bookings', {
      clinic_id: route.params.id,
      doctor_id: bookingForm.value.doctor_id || null,
      scheduled_at: scheduledAt,
      booking_type: bookingForm.value.is_home_visit ? 'home_visit' : 'at_clinic',
      notes: bookingForm.value.notes
    })

    bookingSuccess.value = 'Đặt lịch thành công! Bạn sẽ được chuyển đến trang lịch hẹn.'
    
    setTimeout(() => {
      router.push('/bookings')
    }, 2000)
  } catch (error) {
    bookingError.value = error.response?.data?.detail || 'Đặt lịch thất bại. Vui lòng thử lại.'
  } finally {
    bookingLoading.value = false
  }
}

onMounted(() => {
  fetchClinicDetails()
})
</script>
