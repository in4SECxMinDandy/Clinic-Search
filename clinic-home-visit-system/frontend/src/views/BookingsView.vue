<template>
  <div class="min-h-screen bg-gray-50">
    <nav class="bg-white shadow-sm">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="flex justify-between h-16">
          <div class="flex items-center">
            <router-link to="/" class="text-xl font-bold text-indigo-600">ClinicSearch</router-link>
          </div>
        </div>
      </div>
    </nav>

    <main class="max-w-4xl mx-auto px-4 py-8">
      <h1 class="text-3xl font-bold text-gray-900 mb-8">Lịch hẹn của tôi</h1>

      <div v-if="loading" class="text-center py-8">Đang tải...</div>

      <div v-else-if="bookings.length === 0" class="text-center py-12 bg-white rounded-xl shadow">
        <p class="text-gray-500 mb-4">Bạn chưa có lịch hẹn nào</p>
        <router-link to="/clinics" class="text-indigo-600 hover:text-indigo-700">Tìm phòng khám</router-link>
      </div>

      <div v-else class="space-y-4">
        <div v-for="booking in bookings" :key="booking.id" class="bg-white rounded-xl shadow p-6">
          <div class="flex justify-between items-start">
            <div>
              <h3 class="font-semibold text-gray-900">{{ booking.clinic_id }}</h3>
              <p class="text-sm text-gray-500 mt-1">{{ booking.scheduled_at }}</p>
              <span :class="statusClass(booking.status)" class="inline-block mt-2 px-3 py-1 rounded-full text-sm">
                {{ booking.status }}
              </span>
            </div>
            <div>
              <span class="text-lg font-semibold">{{ booking.booking_type === 'home_visit' ? 'Khám tại nhà' : 'Khám tại phòng khám' }}</span>
            </div>
          </div>
        </div>
      </div>
    </main>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import api from '../services/api'

const bookings = ref([])
const loading = ref(false)

const statusClass = (status) => {
  const classes = {
    pending: 'bg-yellow-100 text-yellow-700',
    confirmed: 'bg-blue-100 text-blue-700',
    completed: 'bg-green-100 text-green-700',
    cancelled: 'bg-red-100 text-red-700',
  }
  return classes[status] || 'bg-gray-100 text-gray-700'
}

const fetchBookings = async () => {
  loading.value = true
  try {
    const response = await api.get('/bookings')
    bookings.value = response.data.bookings || []
  } catch (error) {
    console.error('Error fetching bookings:', error)
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  fetchBookings()
})
</script>
