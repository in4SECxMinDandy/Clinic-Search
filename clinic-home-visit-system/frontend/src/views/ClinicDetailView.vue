<template>
  <div class="min-h-screen bg-gray-50">
    <!-- Header -->
    <section class="bg-white border-b border-gray-100">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div class="flex items-center justify-between">
          <router-link to="/clinics" class="flex items-center gap-2 text-gray-500 hover:text-gray-700 transition-colors">
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 19l-7-7m0 0l7-7m-7 7h18"/>
            </svg>
            <span class="text-sm">Quay lại</span>
          </router-link>
        </div>
      </div>
    </section>

    <!-- Loading -->
    <div v-if="loading" class="flex flex-col items-center justify-center py-24">
      <div class="loading-spinner border-t-primary-600 border-4 border-gray-200 border-t-4 rounded-full w-12 h-12 animate-spin"></div>
      <p class="mt-4 text-sm text-gray-500">Đang tải thông tin phòng khám...</p>
    </div>

    <!-- Error -->
    <div v-else-if="error" class="flex flex-col items-center justify-center py-24 text-center max-w-md mx-auto px-4">
      <div class="w-16 h-16 bg-red-50 rounded-full flex items-center justify-center mb-4">
        <svg class="w-8 h-8 text-red-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"/>
        </svg>
      </div>
      <p class="text-gray-600">{{ error }}</p>
      <router-link to="/clinics" class="mt-4 text-primary-600 hover:underline text-sm">Quay lại danh sách</router-link>
    </div>

    <!-- Content -->
    <div v-else-if="clinic" class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 space-y-6">
      <!-- Hero Card -->
      <div class="bg-white rounded-2xl shadow-sm border border-gray-100 overflow-hidden">
        <!-- Clinic Image -->
        <div v-if="clinic.images && clinic.images.length" class="relative h-56 sm:h-72 bg-gray-100">
          <img :src="clinic.images[0]" :alt="clinic.name" class="w-full h-full object-cover" />
          <div class="absolute inset-0 bg-gradient-to-t from-black/50 to-transparent"></div>
          <div class="absolute bottom-4 left-4 right-4">
            <h1 class="text-2xl font-bold text-white">{{ clinic.name }}</h1>
            <p class="text-white/80 text-sm mt-1 flex items-center gap-1">
              <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z"/>
              </svg>
              {{ clinic.address }}
            </p>
          </div>
        </div>

        <!-- No image fallback -->
        <div v-else class="bg-gradient-to-br from-primary-500 to-primary-700 h-40 flex items-center px-8">
          <div>
            <h1 class="text-2xl font-bold text-white">{{ clinic.name }}</h1>
            <p class="text-white/80 text-sm mt-1">{{ clinic.address }}</p>
          </div>
        </div>

        <!-- Info Strip -->
        <div class="px-6 py-5 border-b border-gray-100">
          <!-- Badges -->
          <div class="flex flex-wrap gap-2 mb-4">
            <span v-if="clinic.supports_home_visit" class="inline-flex items-center gap-1 bg-emerald-50 text-emerald-700 border border-emerald-200 px-3 py-1 rounded-full text-xs font-medium">
              <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6"/>
              </svg>
              Khám tại nhà
            </span>
            <span v-if="clinic.is_verified" class="inline-flex items-center gap-1 bg-blue-50 text-blue-700 border border-blue-200 px-3 py-1 rounded-full text-xs font-medium">
              <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z"/>
              </svg>
              Đã xác minh
            </span>
          </div>

          <!-- Stats Grid -->
          <div class="grid grid-cols-2 sm:grid-cols-4 gap-4">
            <!-- Distance -->
            <div class="flex items-center gap-3">
              <div class="w-10 h-10 bg-indigo-50 rounded-xl flex items-center justify-center flex-shrink-0">
                <svg class="w-5 h-5 text-indigo-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z"/>
                </svg>
              </div>
              <div>
                <p class="text-xs text-gray-400">Khoảng cách</p>
                <p class="text-sm font-semibold text-gray-800">{{ clinic.distance_km ? clinic.distance_km.toFixed(1) + ' km' : '—' }}</p>
              </div>
            </div>

            <!-- Travel Time -->
            <div class="flex items-center gap-3">
              <div class="w-10 h-10 bg-indigo-50 rounded-xl flex items-center justify-center flex-shrink-0">
                <svg class="w-5 h-5 text-indigo-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"/>
                </svg>
              </div>
              <div>
                <p class="text-xs text-gray-400">Di chuyển</p>
                <p class="text-sm font-semibold text-gray-800">{{ clinic.estimated_travel_time_min ? clinic.estimated_travel_time_min + ' phút' : '—' }}</p>
              </div>
            </div>

            <!-- Price -->
            <div class="flex items-center gap-3">
              <div class="w-10 h-10 bg-emerald-50 rounded-xl flex items-center justify-center flex-shrink-0">
                <svg class="w-5 h-5 text-emerald-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/>
                </svg>
              </div>
              <div>
                <p class="text-xs text-gray-400">Giá khám</p>
                <p class="text-sm font-semibold text-gray-800">
                  {{ clinic.min_price ? formatPrice(clinic.min_price) : '—' }}
                  <span v-if="clinic.max_price"> – {{ formatPrice(clinic.max_price) }}</span>
                </p>
              </div>
            </div>

            <!-- Rating -->
            <div class="flex items-center gap-3">
              <div class="w-10 h-10 bg-amber-50 rounded-xl flex items-center justify-center flex-shrink-0">
                <svg class="w-5 h-5 text-amber-500" fill="currentColor" viewBox="0 0 20 20">
                  <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z"/>
                </svg>
              </div>
              <div>
                <p class="text-xs text-gray-400">Đánh giá</p>
                <p class="text-sm font-semibold text-gray-800">{{ clinic.rating ? clinic.rating.toFixed(1) : '—' }}</p>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Main Content Grid -->
      <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <!-- Left Column -->
        <div class="lg:col-span-2 space-y-6">
          <!-- About -->
          <div class="bg-white rounded-2xl shadow-sm border border-gray-100 p-6">
            <h2 class="text-lg font-bold text-gray-900 mb-3 flex items-center gap-2">
              <svg class="w-5 h-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/>
              </svg>
              Giới thiệu
            </h2>
            <p class="text-gray-600 text-sm leading-relaxed">{{ aboutText }}</p>
          </div>

          <!-- Specialties -->
          <div class="bg-white rounded-2xl shadow-sm border border-gray-100 p-6">
            <h2 class="text-lg font-bold text-gray-900 mb-3 flex items-center gap-2">
              <svg class="w-5 h-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2"/>
              </svg>
              Chuyên khoa
            </h2>
            <div v-if="clinic.specialties && clinic.specialties.length" class="flex flex-wrap gap-2">
              <span v-for="s in clinic.specialties" :key="s" class="bg-primary-50 text-primary-700 border border-primary-100 px-3 py-1.5 rounded-full text-xs font-medium">
                {{ getSpecialtyLabel(s) }}
              </span>
            </div>
            <p v-else class="text-gray-400 text-sm">Không có thông tin chuyên khoa</p>
          </div>

          <!-- Doctors -->
          <div class="bg-white rounded-2xl shadow-sm border border-gray-100 p-6">
            <h2 class="text-lg font-bold text-gray-900 mb-4 flex items-center gap-2">
              <svg class="w-5 h-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"/>
              </svg>
              Bác sĩ
              <span v-if="doctors.length" class="ml-1 text-sm font-normal text-gray-400">({{ doctors.length }})</span>
            </h2>

            <div v-if="doctorsLoading" class="flex justify-center py-8">
              <div class="loading-spinner border-t-primary-600 border-4 border-gray-200 border-t-4 rounded-full w-8 h-8 animate-spin"></div>
            </div>

            <div v-else-if="doctors.length" class="space-y-3">
              <div
                v-for="doctor in doctors"
                :key="doctor.id"
                class="flex items-center gap-4 p-4 rounded-xl border border-gray-100 hover:border-primary-200 hover:bg-primary-50/30 transition-all cursor-pointer"
                @click="selectDoctor(doctor)"
                :class="selectedDoctor?.id === doctor.id ? 'border-primary-300 bg-primary-50/30 ring-1 ring-primary-200' : ''"
              >
                <div class="w-12 h-12 rounded-full overflow-hidden bg-gray-100 flex-shrink-0">
                  <img v-if="doctor.avatar" :src="doctor.avatar" :alt="doctor.name" class="w-full h-full object-cover" />
                  <div v-else class="w-full h-full flex items-center justify-center bg-primary-100">
                    <span class="text-lg font-semibold text-primary-700">{{ doctor.name?.charAt(0) || '?' }}</span>
                  </div>
                </div>
                <div class="flex-1 min-w-0">
                  <div class="flex items-center gap-2">
                    <h3 class="font-semibold text-gray-900 text-sm">{{ doctor.name }}</h3>
                    <span v-if="doctor.is_verified" class="inline-flex items-center">
                      <svg class="w-3.5 h-3.5 text-blue-500" fill="currentColor" viewBox="0 0 20 20">
                        <path fill-rule="evenodd" d="M6.267 3.455a3.066 3.066 0 001.745-.723 3.066 3.066 0 013.976 0 3.066 3.066 0 001.745.723 3.066 3.066 0 012.812 2.812c.051.643.304 1.254.723 1.745a3.066 3.066 0 010 3.976 3.066 3.066 0 00-.723 1.745 3.066 3.066 0 01-2.812 2.812 3.066 3.066 0 00-1.745.723 3.066 3.066 0 01-3.976 0 3.066 3.066 0 00-1.745-.723 3.066 3.066 0 01-2.812-2.812 3.066 3.066 0 00-.723-1.745 3.066 3.066 0 010-3.976 3.066 3.066 0 00.723-1.745 3.066 3.066 0 012.812-2.812zm7.44 5.252a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd"/>
                      </svg>
                    </span>
                  </div>
                  <p class="text-xs text-gray-500 mt-0.5">{{ doctor.specialty }}</p>
                  <div class="flex items-center gap-3 mt-1.5">
                    <span class="flex items-center gap-0.5 text-xs text-amber-500 font-medium">
                      <svg class="w-3.5 h-3.5" fill="currentColor" viewBox="0 0 20 20">
                        <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z"/>
                      </svg>
                      {{ doctor.rating ? doctor.rating.toFixed(1) : '—' }}
                    </span>
                    <span class="text-xs text-gray-400">{{ doctor.experience_years }} năm kinh nghiệm</span>
                  </div>
                </div>
                <svg class="w-4 h-4 text-gray-300 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"/>
                </svg>
              </div>
            </div>
            <p v-else class="text-gray-400 text-sm text-center py-6">Không có thông tin bác sĩ</p>
          </div>

          <!-- Reviews -->
          <div class="bg-white rounded-2xl shadow-sm border border-gray-100 p-6">
            <h2 class="text-lg font-bold text-gray-900 mb-4 flex items-center gap-2">
              <svg class="w-5 h-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11.049 2.927c.3-.921 1.603-.921 1.902 0l1.519 4.674a1 1 0 00.95.69h4.915c.969 0 1.371 1.24.588 1.81l-3.976 2.888a1 1 0 00-.363 1.118l1.518 4.674c.3.922-.755 1.688-1.538 1.118l-3.976-2.888a1 1 0 00-1.176 0l-3.976 2.888c-.783.57-1.838-.197-1.538-1.118l1.518-4.674a1 1 0 00-.363-1.118l-3.976-2.888c-.784-.57-.38-1.81.588-1.81h4.914a1 1 0 00.951-.69l1.519-4.674z"/>
              </svg>
              Đánh giá
              <span v-if="reviews.length" class="ml-1 text-sm font-normal text-gray-400">({{ reviews.length }})</span>
            </h2>

            <div v-if="reviewsLoading" class="flex justify-center py-8">
              <div class="loading-spinner border-t-primary-600 border-4 border-gray-200 border-t-4 rounded-full w-8 h-8 animate-spin"></div>
            </div>

            <div v-else-if="reviews.length" class="space-y-4">
              <div v-for="review in reviews" :key="review.id" class="border-b border-gray-50 pb-4 last:border-0">
                <div class="flex items-center justify-between mb-2">
                  <div class="flex items-center gap-2">
                    <div class="flex gap-0.5">
                      <svg v-for="i in 5" :key="i" class="w-4 h-4" :class="i <= review.rating ? 'text-amber-400' : 'text-gray-200'" fill="currentColor" viewBox="0 0 20 20">
                        <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z"/>
                      </svg>
                    </div>
                    <span class="text-sm font-medium text-gray-700">{{ getReviewerName(review.user_id) }}</span>
                  </div>
                  <span class="text-xs text-gray-400">{{ formatDate(review.created_at) }}</span>
                </div>
                <p class="text-sm text-gray-600 leading-relaxed">{{ review.comment }}</p>
                <div v-if="review.pros || review.cons" class="flex flex-wrap gap-3 mt-2">
                  <span v-if="review.pros" class="inline-flex items-center gap-1 text-xs text-emerald-600 bg-emerald-50 px-2 py-0.5 rounded-full">
                    <svg class="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"/>
                    </svg>
                    {{ review.pros }}
                  </span>
                  <span v-if="review.cons" class="inline-flex items-center gap-1 text-xs text-red-500 bg-red-50 px-2 py-0.5 rounded-full">
                    <svg class="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/>
                    </svg>
                    {{ review.cons }}
                  </span>
                </div>
                <div v-if="review.reply" class="mt-3 ml-4 pl-3 border-l-2 border-primary-200 bg-primary-50/50 rounded-r-lg p-3">
                  <p class="text-xs font-medium text-primary-700 mb-1">Phản hồi từ phòng khám:</p>
                  <p class="text-sm text-gray-600">{{ review.reply }}</p>
                </div>
              </div>
            </div>
            <p v-else class="text-gray-400 text-sm text-center py-6">Chưa có đánh giá nào</p>
          </div>
        </div>

        <!-- Right Column - Booking Form -->
        <div class="lg:col-span-1">
          <div class="bg-white rounded-2xl shadow-sm border border-gray-100 p-6 sticky top-6">
            <h2 class="text-lg font-bold text-gray-900 mb-4 flex items-center gap-2">
              <svg class="w-5 h-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z"/>
              </svg>
              Đặt lịch khám
            </h2>

            <!-- Not logged in -->
            <div v-if="!isLoggedIn" class="text-center py-6">
              <div class="w-12 h-12 bg-gray-50 rounded-full flex items-center justify-center mx-auto mb-3">
                <svg class="w-6 h-6 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"/>
                </svg>
              </div>
              <p class="text-sm text-gray-500 mb-4">Vui lòng đăng nhập để đặt lịch khám</p>
              <router-link to="/login" class="block w-full bg-primary-600 text-white py-2.5 px-4 rounded-xl hover:bg-primary-700 text-center text-sm font-medium transition-colors">
                Đăng nhập
              </router-link>
            </div>

            <!-- Booking form -->
            <form v-else @submit.prevent="handleBooking" class="space-y-4">
              <!-- Select Doctor -->
              <div>
                <label class="label">Bác sĩ</label>
                <select v-model="bookingForm.doctor_id" class="input" required>
                  <option value="">Chọn bác sĩ</option>
                  <option v-for="doc in doctors" :key="doc.id" :value="doc.id">
                    {{ doc.name }} — {{ doc.specialty }}
                  </option>
                </select>
              </div>

              <!-- Select Date -->
              <div>
                <label class="label">Ngày khám</label>
                <input
                  v-model="bookingForm.scheduled_date"
                  type="date"
                  :min="minDate"
                  :max="maxDate"
                  class="input"
                  required
                />
              </div>

              <!-- Select Time -->
              <div>
                <label class="label">Giờ khám</label>
                <select v-model="bookingForm.scheduled_time" class="input" required :disabled="!bookingForm.scheduled_date">
                  <option value="">Chọn giờ</option>
                  <option v-for="slot in availableSlots" :key="slot" :value="slot">{{ slot }}</option>
                </select>
                <p v-if="bookingForm.scheduled_date && availableSlots.length === 0" class="text-xs text-amber-600 mt-1">
                  Không có lịch trống cho ngày này
                </p>
              </div>

              <!-- Booking Type -->
              <div>
                <label class="label">Hình thức khám</label>
                <div class="space-y-2">
                  <label class="flex items-center gap-2 p-3 rounded-xl border cursor-pointer transition-colors"
                    :class="bookingForm.booking_type === 'at_clinic' ? 'border-primary-300 bg-primary-50 ring-1 ring-primary-200' : 'border-gray-200'"
                  >
                    <input v-model="bookingForm.booking_type" type="radio" value="at_clinic" class="text-primary-600" />
                    <svg class="w-4 h-4 text-gray-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4"/>
                    </svg>
                    <div>
                      <p class="text-xs font-medium text-gray-700">Tại phòng khám</p>
                      <p class="text-xs text-gray-400">{{ clinic.min_price ? 'Từ ' + formatPrice(clinic.min_price) : '' }}</p>
                    </div>
                  </label>
                  <label v-if="clinic.supports_home_visit"
                    class="flex items-center gap-2 p-3 rounded-xl border cursor-pointer transition-colors"
                    :class="bookingForm.booking_type === 'home_visit' ? 'border-primary-300 bg-primary-50 ring-1 ring-primary-200' : 'border-gray-200'"
                  >
                    <input v-model="bookingForm.booking_type" type="radio" value="home_visit" class="text-primary-600" />
                    <svg class="w-4 h-4 text-gray-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6"/>
                    </svg>
                    <div>
                      <p class="text-xs font-medium text-gray-700">Khám tại nhà</p>
                      <p class="text-xs text-gray-400">Bán kính {{ clinic.home_visit_radius_km || 10 }}km</p>
                    </div>
                  </label>
                </div>
              </div>

              <!-- Home Address (if home visit) -->
              <div v-if="bookingForm.booking_type === 'home_visit'">
                <label class="label">Địa chỉ nhà</label>
                <textarea
                  v-model="bookingForm.home_address"
                  class="input"
                  rows="2"
                  placeholder="Số nhà, đường, phường/xã, quận/huyện..."
                ></textarea>
              </div>

              <!-- Notes -->
              <div>
                <label class="label">Ghi chú</label>
                <textarea
                  v-model="bookingForm.notes"
                  class="input"
                  rows="2"
                  placeholder="Mô tả triệu chứng, dị ứng..."
                ></textarea>
              </div>

              <!-- Payment -->
              <div>
                <label class="label">Thanh toán</label>
                <select v-model="bookingForm.payment_method" class="input">
                  <option value="cash">Tiền mặt</option>
                  <option value="transfer">Chuyển khoản</option>
                </select>
              </div>

              <!-- Error -->
              <div v-if="bookingError" class="bg-red-50 border border-red-100 text-red-600 p-3 rounded-xl text-sm">
                {{ bookingError }}
              </div>

              <!-- Success -->
              <div v-if="bookingSuccess" class="bg-emerald-50 border border-emerald-100 text-emerald-700 p-3 rounded-xl text-sm">
                {{ bookingSuccess }}
              </div>

              <!-- Submit -->
              <button
                type="submit"
                :disabled="bookingLoading"
                class="w-full bg-primary-600 text-white py-3 px-4 rounded-xl hover:bg-primary-700 disabled:opacity-50 font-medium text-sm transition-colors flex items-center justify-center gap-2"
              >
                <span v-if="bookingLoading" class="loading-spinner border-t-white border-2 border-white/30 border-t-2 rounded-full w-4 h-4 animate-spin"></span>
                {{ bookingLoading ? 'Đang đặt...' : 'Xác nhận đặt lịch' }}
              </button>
            </form>
          </div>
        </div>
      </div>
    </div>

    <!-- Not Found -->
    <div v-else class="flex flex-col items-center justify-center py-24 text-center">
      <div class="w-16 h-16 bg-gray-100 rounded-full flex items-center justify-center mb-4">
        <svg class="w-8 h-8 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4"/>
        </svg>
      </div>
      <p class="text-gray-500 font-medium">Không tìm thấy phòng khám</p>
      <router-link to="/clinics" class="mt-4 text-primary-600 hover:underline text-sm">Quay lại danh sách</router-link>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useClinicStore } from '../stores/clinic'
import { useAuthStore } from '../stores/auth'
import api from '../services/api'

const route = useRoute()
const router = useRouter()
const clinicStore = useClinicStore()
const authStore = useAuthStore()

// Clinic data
const clinic = ref(null)
const doctors = ref([])
const reviews = ref([])
const loading = ref(true)
const doctorsLoading = ref(false)
const reviewsLoading = ref(false)
const error = ref('')

// Booking
const bookingForm = ref({
  doctor_id: '',
  scheduled_date: '',
  scheduled_time: '',
  booking_type: 'at_clinic',
  home_address: '',
  notes: '',
  payment_method: 'cash',
})
const bookingError = ref('')
const bookingSuccess = ref('')
const bookingLoading = ref(false)

// Selected doctor
const selectedDoctor = ref(null)

// Availability
const availableSlots = ref([])

// Auth
const isLoggedIn = computed(() => authStore.isAuthenticated)

// Date limits
const minDate = computed(() => {
  const d = new Date()
  d.setDate(d.getDate() + 1)
  return d.toISOString().split('T')[0]
})

const maxDate = computed(() => {
  const d = new Date()
  d.setDate(d.getDate() + 30)
  return d.toISOString().split('T')[0]
})

// Specialty labels
const SPECIALTY_LABELS = {
  general: 'Đa khoa',
  pediatrics: 'Nhi khoa',
  cardiology: 'Tim mạch',
  dermatology: 'Da liễu',
  dentistry: 'Nha khoa',
  orthopedics: 'Chỉnh hình',
  neurology: 'Thần kinh',
  ophthalmology: 'Mắt',
  internal_medicine: 'Nội tổng hợp',
  surgery: 'Ngoại khoa',
  radiology: 'Chẩn đoán hình ảnh',
  laboratory: 'Xét nghiệm',
  clinic: 'Phòng khám',
  pharmacy: 'Nhà thuốc',
  hospital: 'Bệnh viện',
}

function getSpecialtyLabel(s) {
  return SPECIALTY_LABELS[s?.toLowerCase()] || s || 'Khác'
}

// Format price
function formatPrice(value) {
  if (!value) return ''
  return new Intl.NumberFormat('vi-VN').format(value) + 'đ'
}

// About text
const aboutText = computed(() => {
  if (!clinic.value) return ''
  const name = clinic.value.name || ''
  const address = clinic.value.address || ''
  const hours = clinic.value.opening_time && clinic.value.closing_time
    ? `từ ${clinic.value.opening_time} đến ${clinic.value.closing_time}`
    : 'T2-T7'
  return `${name} là cơ sở y tế đáng tin cậy tọa lạc tại ${address}. Phòng khám hoạt động ${hours}, cung cấp các dịch vụ khám chữa bệnh chất lượng cao với đội ngũ bác sĩ giàu kinh nghiệm.`
})

// Reviewer names (deterministic from user_id)
const REVIEWER_NAMES = [
  'Nguyễn Văn An', 'Trần Thị Bình', 'Lê Hoàng Cường', 'Phạm Minh Đức',
  'Hoàng Thu Hà', 'Vũ Thanh Lan', 'Đặng Quốc Duy', 'Bùi Thu Hương',
  'Cao Minh Khoa', 'Đinh Thị Kim', 'Phan Văn Lâm', 'Trịnh Thị Mai',
]

function getReviewerName(userId) {
  if (!userId) return 'Người dùng'
  let hash = 0
  for (let i = 0; i < userId.length; i++) {
    hash = ((hash << 5) - hash) + userId.charCodeAt(i)
    hash |= 0
  }
  return REVIEWER_NAMES[Math.abs(hash) % REVIEWER_NAMES.length]
}

function formatDate(dateStr) {
  if (!dateStr) return ''
  const d = new Date(dateStr)
  return d.toLocaleDateString('vi-VN', { day: 'numeric', month: 'short', year: 'numeric' })
}

// Fetch clinic
async function fetchClinicDetails() {
  loading.value = true
  error.value = ''
  try {
    const params = {}
    if (clinicStore.filters.lat && clinicStore.filters.lng) {
      params.lat = clinicStore.filters.lat
      params.lng = clinicStore.filters.lng
    }
    const response = await api.get(`/clinics/${route.params.id}`, { params })
    clinic.value = response.data
    // Auto-fetch doctors and reviews after getting clinic
    if (clinic.value) {
      fetchDoctors()
      fetchReviews()
    }
  } catch (err) {
    error.value = err.response?.data?.detail || 'Không thể tải thông tin phòng khám'
    console.error('Clinic fetch error:', err)
  } finally {
    loading.value = false
  }
}

// Fetch doctors
async function fetchDoctors() {
  doctorsLoading.value = true
  try {
    const response = await api.get('/doctors', {
      params: { clinic_id: route.params.id, page_size: 50 }
    })
    doctors.value = response.data || []
    // Auto-select first doctor
    if (doctors.value.length > 0 && !selectedDoctor.value) {
      selectDoctor(doctors.value[0])
    }
  } catch (err) {
    console.error('Doctors fetch error:', err)
  } finally {
    doctorsLoading.value = false
  }
}

// Fetch reviews
async function fetchReviews() {
  reviewsLoading.value = true
  try {
    const response = await api.get(`/reviews/clinic/${route.params.id}`, {
      params: { page_size: 10 }
    })
    reviews.value = response.data?.reviews || []
    // Update clinic rating if reviews exist
    if (reviews.value.length > 0) {
      const avg = reviews.value.reduce((sum, r) => sum + r.rating, 0) / reviews.value.length
      clinic.value = { ...clinic.value, rating: Math.round(avg * 10) / 10 }
    }
  } catch (err) {
    // Review service might not have reviews yet — that's ok
    reviews.value = []
  } finally {
    reviewsLoading.value = false
  }
}

// Select doctor
async function selectDoctor(doctor) {
  selectedDoctor.value = doctor
  bookingForm.value.doctor_id = doctor.id
  bookingForm.value.scheduled_time = ''
  availableSlots.value = []
}

// Watch date change to load slots
watch(() => bookingForm.value.scheduled_date, async (newDate) => {
  if (!newDate || !bookingForm.value.doctor_id) {
    availableSlots.value = []
    return
  }
  try {
    const response = await api.get(`/doctors/${bookingForm.value.doctor_id}/slots`, {
      params: { date: newDate, duration_minutes: 30 }
    })
    availableSlots.value = (response.data?.slots || [])
      .filter(s => s.available)
      .map(s => {
        const d = new Date(s.start)
        return `${String(d.getHours()).padStart(2, '0')}:${String(d.getMinutes()).padStart(2, '0')}`
      })
  } catch {
    availableSlots.value = []
  }
})

// Watch doctor change
watch(() => bookingForm.value.doctor_id, () => {
  availableSlots.value = []
  bookingForm.value.scheduled_time = ''
})

// Booking submit
async function handleBooking() {
  bookingError.value = ''
  bookingSuccess.value = ''

  if (!bookingForm.value.doctor_id) {
    bookingError.value = 'Vui lòng chọn bác sĩ'
    return
  }
  if (!bookingForm.value.scheduled_date) {
    bookingError.value = 'Vui lòng chọn ngày khám'
    return
  }
  if (!bookingForm.value.scheduled_time) {
    bookingError.value = 'Vui lòng chọn giờ khám'
    return
  }

  bookingLoading.value = true
  try {
    const scheduledAt = `${bookingForm.value.scheduled_date}T${bookingForm.value.scheduled_time}:00`
    await api.post('/bookings', {
      clinic_id: route.params.id,
      doctor_id: bookingForm.value.doctor_id,
      booking_type: bookingForm.value.booking_type,
      scheduled_at: scheduledAt,
      duration_minutes: 30,
      home_address: bookingForm.value.booking_type === 'home_visit' ? bookingForm.value.home_address : undefined,
      notes: bookingForm.value.notes || undefined,
      payment_method: bookingForm.value.payment_method,
    })

    bookingSuccess.value = 'Đặt lịch thành công! Bạn sẽ được chuyển đến trang lịch hẹn.'
    setTimeout(() => router.push('/bookings'), 2000)
  } catch (err) {
    bookingError.value = err.response?.data?.detail || 'Đặt lịch thất bại. Vui lòng thử lại.'
  } finally {
    bookingLoading.value = false
  }
}

onMounted(() => {
  fetchClinicDetails()
})
</script>
