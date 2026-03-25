<template>
  <div class="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">
    <nav class="bg-white shadow-sm">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="flex justify-between h-16">
          <div class="flex items-center">
            <router-link to="/" class="text-xl font-bold text-indigo-600">ClinicSearch</router-link>
          </div>
          <div class="flex items-center space-x-4">
            <router-link to="/clinics" class="text-gray-600 hover:text-indigo-600 px-3 py-2 rounded-md">Tìm phòng khám</router-link>
            <router-link v-if="!isLoggedIn" to="/login" class="text-gray-600 hover:text-indigo-600 px-3 py-2 rounded-md">Đăng nhập</router-link>
            <router-link v-if="!isLoggedIn" to="/register" class="bg-indigo-600 text-white px-4 py-2 rounded-md hover:bg-indigo-700">Đăng ký</router-link>
            <router-link v-if="isLoggedIn" to="/bookings" class="text-gray-600 hover:text-indigo-600 px-3 py-2 rounded-md">Lịch hẹn</router-link>
          </div>
        </div>
      </div>
    </nav>

    <main class="max-w-7xl mx-auto px-4 py-16 sm:px-6 lg:px-8">
      <div class="text-center">
        <h1 class="text-4xl font-bold text-gray-900 mb-4">Tìm kiếm phòng khám gần bạn</h1>
        <p class="text-xl text-gray-600 mb-8">Đặt lịch khám tại nhà hoặc tại phòng khám một cách dễ dàng</p>

        <div class="max-w-2xl mx-auto">
          <div class="relative">
            <input
              v-model="searchQuery"
              type="text"
              placeholder="Tìm kiếm phòng khám, bác sĩ, chuyên khoa..."
              class="w-full px-6 py-4 text-lg border border-gray-300 rounded-full shadow-lg focus:outline-none focus:ring-2 focus:ring-indigo-500"
              @keyup.enter="searchClinics"
            />
            <button
              @click="searchClinics"
              class="absolute right-2 top-1/2 -translate-y-1/2 bg-indigo-600 text-white px-6 py-2 rounded-full hover:bg-indigo-700"
            >
              Tìm kiếm
            </button>
          </div>
        </div>

        <div class="mt-12 grid grid-cols-1 md:grid-cols-3 gap-8">
          <div class="bg-white p-6 rounded-xl shadow-md">
            <div class="w-12 h-12 bg-indigo-100 rounded-full flex items-center justify-center mb-4 mx-auto">
              <svg class="w-6 h-6 text-indigo-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z"/>
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 11a3 3 0 11-6 0 3 3 0 016 0z"/>
              </svg>
            </div>
            <h3 class="text-lg font-semibold text-gray-900 mb-2">GPS thông minh</h3>
            <p class="text-gray-600">Tìm phòng khám gần nhất với khoảng cách chính xác</p>
          </div>
          <div class="bg-white p-6 rounded-xl shadow-md">
            <div class="w-12 h-12 bg-indigo-100 rounded-full flex items-center justify-center mb-4 mx-auto">
              <svg class="w-6 h-6 text-indigo-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 5a2 2 0 012-2h3.28a1 1 0 01.948.684l1.498 4.493a1 1 0 01-.502 1.21l-2.257 1.13a11.042 11.042 0 005.516 5.516l1.13-2.257a1 1 0 011.21-.502l4.493 1.498a1 1 0 01.684.949V19a2 2 0 01-2 2h-1C9.716 21 3 14.284 3 6V5z"/>
              </svg>
            </div>
            <h3 class="text-lg font-semibold text-gray-900 mb-2">Đặt lịch dễ dàng</h3>
            <p class="text-gray-600">Chọn bác sĩ và thời gian phù hợp với bạn</p>
          </div>
          <div class="bg-white p-6 rounded-xl shadow-md">
            <div class="w-12 h-12 bg-indigo-100 rounded-full flex items-center justify-center mb-4 mx-auto">
              <svg class="w-6 h-6 text-indigo-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6"/>
              </svg>
            </div>
            <h3 class="text-lg font-semibold text-gray-900 mb-2">Khám tại nhà</h3>
            <p class="text-gray-600">Dịch vụ khám tại nhà cho những ai cần</p>
          </div>
        </div>
      </div>
    </main>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'

const router = useRouter()
const authStore = useAuthStore()
const searchQuery = ref('')

const isLoggedIn = computed(() => authStore.isAuthenticated)

const searchClinics = () => {
  router.push({ name: 'Clinics', query: { search: searchQuery.value } })
}
</script>
