<template>
  <div class="relative min-h-screen bg-gradient-hero overflow-hidden">
    <!-- Decorative circles -->
    <div class="decorative-circle w-[600px] h-[600px] bg-primary-400 -top-64 -right-64 blur-3xl"></div>
    <div class="decorative-circle w-[400px] h-[400px] bg-primary-300 bottom-0 -left-48 blur-3xl"></div>

    <!-- Hero Section -->
    <section class="relative max-w-2xl mx-auto px-4 pt-20 pb-12 text-center">
      <!-- Badge -->
      <div class="inline-flex items-center gap-1.5 px-4 py-1.5 bg-primary-50 border border-primary-100 rounded-full text-sm font-medium text-primary-700 mb-6">
        <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"/>
        </svg>
        Nền tảng y tế tin cậy
      </div>

      <!-- Title -->
      <h1 class="text-4xl sm:text-5xl font-extrabold text-gray-900 leading-tight mb-4">
        Tìm kiếm phòng khám<br>
        <span class="text-primary-600">gần bạn</span>
      </h1>

      <!-- Subtitle -->
      <p class="text-gray-500 text-base mb-10 max-w-lg mx-auto">
        Kết nối với các phòng khám uy tín và đặt lịch khám tại nhà một cách dễ dàng, nhanh chóng
      </p>

      <!-- Search Bar -->
      <div class="relative max-w-xl mx-auto">
        <form @submit.prevent="handleSearch" class="relative bg-white rounded-full shadow-md border border-gray-200 overflow-hidden transition-all duration-300 focus-within:shadow-lg focus-within:border-primary-300">
          <!-- Search Icon -->
          <div class="absolute inset-y-0 left-0 pl-5 flex items-center pointer-events-none">
            <svg class="w-5 h-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"/>
            </svg>
          </div>
          <!-- Input -->
          <input
            v-model="searchQuery"
            type="text"
            placeholder="Tìm kiếm phòng khám, chuyên khoa..."
            class="w-full pl-14 pr-32 py-4 text-base bg-transparent focus:outline-none placeholder-gray-400"
          />
          <!-- Search Button -->
          <button
            type="submit"
            class="absolute inset-y-1 right-1 px-6 bg-primary-600 text-white font-medium rounded-full hover:bg-primary-700 transition-colors duration-200 cursor-pointer"
          >
            Tìm kiếm
          </button>
        </form>
      </div>
    </section>

    <!-- Feature Cards -->
    <section class="max-w-3xl mx-auto px-4 pb-20">
      <div class="grid grid-cols-1 sm:grid-cols-3 gap-4">
        <!-- Feature 1: GPS -->
        <div class="feature-card">
          <div class="w-12 h-12 bg-violet-50 rounded-xl flex items-center justify-center mb-4">
            <svg class="w-6 h-6 text-violet-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z"/>
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 11a3 3 0 11-6 0 3 3 0 016 0z"/>
            </svg>
          </div>
          <h3 class="text-base font-bold text-gray-900 mb-1">GPS thông minh</h3>
          <p class="text-gray-400 text-xs">Tìm phòng khám gần nhất với khoảng cách chính xác</p>
        </div>

        <!-- Feature 2: Booking -->
        <div class="feature-card">
          <div class="w-12 h-12 bg-blue-50 rounded-xl flex items-center justify-center mb-4">
            <svg class="w-6 h-6 text-blue-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z"/>
            </svg>
          </div>
          <h3 class="text-base font-bold text-gray-900 mb-1">Đặt lịch dễ dàng</h3>
          <p class="text-gray-400 text-xs">Chọn bác sĩ và thời gian phù hợp với bạn</p>
        </div>

        <!-- Feature 3: Home Visit -->
        <div class="feature-card">
          <div class="w-12 h-12 bg-green-50 rounded-xl flex items-center justify-center mb-4">
            <svg class="w-6 h-6 text-green-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6"/>
            </svg>
          </div>
          <h3 class="text-base font-bold text-gray-900 mb-1">Khám tại nhà</h3>
          <p class="text-gray-400 text-xs">Dịch vụ khám tại nhà cho những ai cần</p>
        </div>
      </div>
    </section>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()
const searchQuery = ref('')

const handleSearch = () => {
  const query = searchQuery.value.trim()
  router.push({ name: 'Clinics', query: query ? { search: query } : {} })
}
</script>
