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
      <!-- Header -->
      <header class="bg-white border-b border-gray-200 sticky top-0 z-10">
        <div class="max-w-7xl mx-auto px-8 py-4 flex justify-between items-center">
          <div class="flex items-center gap-4">
            <router-link to="/owner/dashboard" class="flex items-center gap-2 text-sm text-gray-500 hover:text-gray-900 transition-colors">
              <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7"/>
              </svg>
              Quay lại Dashboard
            </router-link>
            <div class="h-6 w-px bg-gray-200"></div>
            <h1 class="text-lg font-semibold text-gray-900">Quản lý Bác sĩ</h1>
          </div>
          <button @click="showCreateModal = true" class="inline-flex items-center gap-2 px-4 py-2 bg-emerald-600 text-white rounded-lg text-sm font-medium hover:bg-emerald-700 transition-colors">
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4"/>
            </svg>
            Thêm bác sĩ
          </button>
        </div>
      </header>

      <div class="max-w-7xl mx-auto px-8 py-6">
        <!-- Clinic Filter -->
        <div v-if="clinics.length > 1" class="bg-white rounded-xl shadow-sm border border-gray-100 p-4 mb-4">
          <div class="flex flex-wrap gap-3 items-center">
            <label class="text-sm font-medium text-gray-700">Phòng khám:</label>
            <select v-model="selectedClinic" @change="fetchDoctors" class="px-3 py-2 border border-gray-200 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-emerald-500">
              <option value="">Tất cả phòng khám</option>
              <option v-for="c in clinics" :key="c.id" :value="c.id">{{ c.name }}</option>
            </select>
            <span class="ml-auto text-sm text-gray-500">{{ doctors.length }} bác sĩ</span>
          </div>
        </div>

        <!-- Loading -->
        <div v-if="loading" class="text-center py-16">
          <div class="inline-block w-10 h-10 border-4 border-emerald-200 border-t-emerald-600 rounded-full animate-spin"></div>
          <p class="mt-4 text-sm text-gray-500">Đang tải dữ liệu...</p>
        </div>

        <!-- Empty State -->
        <div v-else-if="clinics.length === 0" class="bg-white rounded-xl shadow-sm border border-gray-100 p-8 text-center">
          <div class="w-16 h-16 bg-amber-100 rounded-full flex items-center justify-center mx-auto mb-4">
            <svg class="w-8 h-8 text-amber-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"/>
            </svg>
          </div>
          <h3 class="font-semibold text-gray-900">Bạn chưa có phòng khám nào</h3>
          <p class="mt-2 text-sm text-gray-500">Hãy tạo phòng khám trước để thêm bác sĩ.</p>
          <router-link to="/owner/clinics" class="inline-flex items-center mt-4 px-4 py-2 bg-emerald-600 text-white rounded-lg text-sm font-medium hover:bg-emerald-700 transition-colors">
            Tạo phòng khám
          </router-link>
        </div>

        <!-- Empty Doctors -->
        <div v-else-if="doctors.length === 0" class="bg-white rounded-xl shadow-sm border border-gray-100 p-8 text-center">
          <div class="w-16 h-16 bg-gray-100 rounded-full flex items-center justify-center mx-auto mb-4">
            <svg class="w-8 h-8 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"/>
            </svg>
          </div>
          <h3 class="font-semibold text-gray-900">Chưa có bác sĩ nào</h3>
          <p class="mt-2 text-sm text-gray-500">Thêm bác sĩ đầu tiên cho phòng khám của bạn.</p>
          <button @click="showCreateModal = true" class="inline-flex items-center mt-4 px-4 py-2 bg-emerald-600 text-white rounded-lg text-sm font-medium hover:bg-emerald-700 transition-colors">
            Thêm bác sĩ
          </button>
        </div>

        <!-- Doctors Grid -->
        <div v-else class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          <div v-for="doc in doctors" :key="doc.id" class="bg-white rounded-xl shadow-sm border border-gray-100 p-5 hover:border-emerald-200 transition-colors">
            <div class="flex items-start justify-between mb-3">
              <div class="flex items-center gap-3">
                <div class="w-12 h-12 bg-emerald-100 rounded-full flex items-center justify-center">
                  <svg class="w-6 h-6 text-emerald-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"/>
                  </svg>
                </div>
                <div>
                  <h3 class="font-semibold text-gray-900">{{ doc.name }}</h3>
                  <p class="text-sm text-gray-500">{{ doc.specialty }}</p>
                </div>
              </div>
              <span v-if="doc.is_verified" class="inline-flex items-center px-2 py-0.5 rounded-full text-xs font-medium bg-green-100 text-green-700">
                Đã xác minh
              </span>
              <span v-else class="inline-flex items-center px-2 py-0.5 rounded-full text-xs font-medium bg-yellow-100 text-yellow-700">
                Chưa xác minh
              </span>
            </div>

            <div class="space-y-2 text-sm text-gray-500 mb-4">
              <div v-if="doc.experience_years" class="flex items-center gap-2">
                <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"/>
                </svg>
                {{ doc.experience_years }} năm kinh nghiệm
              </div>
              <div v-if="doc.license_number" class="flex items-center gap-2">
                <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4M7.835 4.697a3.42 3.42 0 001.946-.806 3.42 3.42 0 014.438 0 3.42 3.42 0 001.946.806 3.42 3.42 0 013.138 3.138 3.42 3.42 0 00.806 1.946 3.42 3.42 0 010 4.438 3.42 3.42 0 00-.806 1.946 3.42 3.42 0 01-3.138 3.138 3.42 3.42 0 00-1.946.806 3.42 3.42 0 01-4.438 0 3.42 3.42 0 00-1.946-.806 3.42 3.42 0 01-3.138-3.138 3.42 3.42 0 00-.806-1.946 3.42 3.42 0 010-4.438 3.42 3.42 0 00.806-1.946 3.42 3.42 0 013.138-3.138z"/>
                </svg>
                {{ doc.license_number }}
              </div>
              <div class="flex items-center gap-2">
                <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11.049 2.927c.3-.921 1.603-.921 1.902 0l1.519 4.674a1 1 0 00.95.69h4.915c.969 0 1.371 1.24.588 1.81l-3.976 2.888a1 1 0 00-.363 1.118l1.518 4.674c.3.922-.755 1.688-1.538 1.118l-3.976-2.888a1 1 0 00-1.176 0l-3.976 2.888c-.783.57-1.838-.197-1.538-1.118l1.518-4.674a1 1 0 00-.363-1.118l-3.976-2.888c-.784-.57-.38-1.81.588-1.81h4.914a1 1 0 00.951-.69l1.519-4.674z"/>
                </svg>
                {{ doc.rating || 0 }} ({{ doc.total_reviews || 0 }} đánh giá)
              </div>
              <div v-if="doc.supports_home_visit" class="flex items-center gap-2">
                <svg class="w-4 h-4 text-purple-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6"/>
                </svg>
                <span class="text-purple-600">Hỗ trợ khám tại nhà</span>
              </div>
            </div>

            <div class="flex gap-2">
              <button @click="openEditModal(doc)" class="flex-1 px-3 py-2 bg-gray-100 text-gray-700 rounded-lg text-sm font-medium hover:bg-gray-200 transition-colors">
                Sửa
              </button>
              <button @click="openScheduleModal(doc)" class="flex-1 px-3 py-2 bg-blue-50 text-blue-600 rounded-lg text-sm font-medium hover:bg-blue-100 transition-colors">
                Lịch
              </button>
            </div>
          </div>
        </div>
      </div>
    </main>

    <!-- Create/Edit Doctor Modal -->
    <div v-if="showCreateModal" class="fixed inset-0 bg-black/50 flex items-center justify-center z-50" @click.self="closeModal">
      <div class="bg-white rounded-xl shadow-xl max-w-lg w-full mx-4 max-h-[90vh] overflow-y-auto">
        <div class="px-6 py-4 border-b border-gray-100 flex items-center justify-between">
          <h3 class="text-lg font-semibold text-gray-900">{{ editingDoctor ? 'Sửa bác sĩ' : 'Thêm bác sĩ mới' }}</h3>
          <button @click="closeModal" class="p-1 rounded-lg hover:bg-gray-100 text-gray-400 hover:text-gray-600 transition-colors">
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/>
            </svg>
          </button>
        </div>
        <div class="px-6 py-4 space-y-4">
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1.5">Tên bác sĩ *</label>
            <input v-model="form.name" type="text" placeholder="VD: BS. Nguyễn Văn A"
              class="w-full px-3 py-2 border border-gray-200 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-emerald-500 focus:border-transparent"/>
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1.5">Phòng khám *</label>
            <select v-model="form.clinic_id" class="w-full px-3 py-2 border border-gray-200 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-emerald-500">
              <option value="">Chọn phòng khám</option>
              <option v-for="c in clinics" :key="c.id" :value="c.id">{{ c.name }}</option>
            </select>
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1.5">Chuyên khoa *</label>
            <input v-model="form.specialty" type="text" placeholder="VD: Nội khoa, Ngoại khoa..."
              class="w-full px-3 py-2 border border-gray-200 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-emerald-500 focus:border-transparent"/>
          </div>
          <div class="grid grid-cols-2 gap-4">
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1.5">Số giấy phép</label>
              <input v-model="form.license_number" type="text" placeholder="VD: GP-12345"
                class="w-full px-3 py-2 border border-gray-200 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-emerald-500 focus:border-transparent"/>
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1.5">Kinh nghiệm (năm)</label>
              <input v-model.number="form.experience_years" type="number" min="0" placeholder="VD: 5"
                class="w-full px-3 py-2 border border-gray-200 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-emerald-500 focus:border-transparent"/>
            </div>
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1.5">Giới thiệu</label>
            <textarea v-model="form.bio" rows="3" placeholder="Mô tả về bác sĩ..."
              class="w-full px-3 py-2 border border-gray-200 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-emerald-500 focus:border-transparent resize-none"></textarea>
          </div>
          <div>
            <label class="flex items-center gap-3 cursor-pointer">
              <input type="checkbox" v-model="form.supports_home_visit" class="w-4 h-4 text-emerald-600 border-gray-300 rounded focus:ring-emerald-500"/>
              <span class="text-sm text-gray-700">Hỗ trợ khám tại nhà</span>
            </label>
          </div>
        </div>
        <div class="px-6 py-4 bg-gray-50 border-t border-gray-100 flex gap-2 justify-end">
          <button @click="closeModal"
            class="px-4 py-2 border border-gray-200 text-gray-700 rounded-lg text-sm font-medium hover:bg-gray-200 transition-colors">
            Hủy
          </button>
          <button @click="saveDoctor" :disabled="saving"
            class="px-4 py-2 bg-emerald-600 text-white rounded-lg text-sm font-medium hover:bg-emerald-700 transition-colors disabled:opacity-60">
            {{ saving ? 'Đang lưu...' : (editingDoctor ? 'Lưu thay đổi' : 'Thêm bác sĩ') }}
          </button>
        </div>
      </div>
    </div>

    <!-- Schedule Modal -->
    <div v-if="scheduleModal.show" class="fixed inset-0 bg-black/50 flex items-center justify-center z-50" @click.self="scheduleModal.show = false">
      <div class="bg-white rounded-xl shadow-xl max-w-lg w-full mx-4 max-h-[90vh] overflow-y-auto">
        <div class="px-6 py-4 border-b border-gray-100 flex items-center justify-between">
          <h3 class="text-lg font-semibold text-gray-900">Lịch làm việc - {{ scheduleModal.doctor?.name }}</h3>
          <button @click="scheduleModal.show = false" class="p-1 rounded-lg hover:bg-gray-100 text-gray-400 hover:text-gray-600 transition-colors">
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/>
            </svg>
          </button>
        </div>
        <div class="px-6 py-4">
          <div class="space-y-3">
            <div v-for="(day, idx) in daysOfWeek" :key="idx" class="flex items-center gap-3">
              <span class="w-24 text-sm font-medium text-gray-700">{{ day }}</span>
              <label class="flex items-center gap-2 cursor-pointer">
                <input type="checkbox" v-model="scheduleForm[day].enabled" class="w-4 h-4 text-emerald-600 border-gray-300 rounded focus:ring-emerald-500"/>
                <span class="text-sm text-gray-500">Làm việc</span>
              </label>
              <div v-if="scheduleForm[day].enabled" class="flex items-center gap-2">
                <input type="time" v-model="scheduleForm[day].start" class="px-2 py-1 border border-gray-200 rounded text-sm"/>
                <span class="text-gray-400">-</span>
                <input type="time" v-model="scheduleForm[day].end" class="px-2 py-1 border border-gray-200 rounded text-sm"/>
              </div>
            </div>
          </div>
        </div>
        <div class="px-6 py-4 bg-gray-50 border-t border-gray-100 flex gap-2 justify-end">
          <button @click="scheduleModal.show = false"
            class="px-4 py-2 border border-gray-200 text-gray-700 rounded-lg text-sm font-medium hover:bg-gray-200 transition-colors">
            Đóng
          </button>
          <button @click="saveSchedule" :disabled="scheduleModal.saving"
            class="px-4 py-2 bg-emerald-600 text-white rounded-lg text-sm font-medium hover:bg-emerald-700 transition-colors disabled:opacity-60">
            {{ scheduleModal.saving ? 'Đang lưu...' : 'Lưu lịch' }}
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useAuthStore } from '../stores/auth'
import api from '../services/api'

const router = useRouter()
const route = useRoute()
const authStore = useAuthStore()

const user = computed(() => authStore.user)
const userInitials = computed(() => {
  const name = user.value?.full_name || 'C'
  return name.split(' ').map(w => w[0]).join('').toUpperCase().slice(0, 2)
})

const clinics = ref([])
const doctors = ref([])
const loading = ref(false)
const saving = ref(false)

const selectedClinic = ref('')

const showCreateModal = ref(false)
const editingDoctor = ref(null)
const form = ref({
  name: '',
  clinic_id: '',
  specialty: '',
  license_number: '',
  experience_years: null,
  bio: '',
  supports_home_visit: false,
})

const scheduleModal = ref({ show: false, doctor: null, saving: false })
const daysOfWeek = ['Thứ 2', 'Thứ 3', 'Thứ 4', 'Thứ 5', 'Thứ 6', 'Thứ 7', 'Chủ nhật']

const scheduleForm = ref({})
for (const day of daysOfWeek) {
  scheduleForm.value[day] = { enabled: false, start: '08:00', end: '17:00' }
}

const fetchClinics = async () => {
  try {
    const response = await api.get('/clinics/owner/my-clinics')
    clinics.value = response.data.clinics || response.data || []

    // If clinic_id in query, select it
    if (route.query.clinic_id) {
      selectedClinic.value = route.query.clinic_id
    } else if (clinics.value.length === 1) {
      selectedClinic.value = clinics.value[0].id
    }
  } catch (error) {
    console.error('Error fetching clinics:', error)
  }
}

const fetchDoctors = async () => {
  loading.value = true
  try {
    const params = {}
    if (selectedClinic.value) {
      params.clinic_id = selectedClinic.value
    }
    const response = await api.get('/doctors', { params })
    doctors.value = response.data || []
  } catch (error) {
    console.error('Error fetching doctors:', error)
    doctors.value = []
  } finally {
    loading.value = false
  }
}

const openEditModal = (doctor) => {
  editingDoctor.value = doctor
  form.value = {
    name: doctor.name || '',
    clinic_id: doctor.clinic_id || '',
    specialty: doctor.specialty || '',
    license_number: doctor.license_number || '',
    experience_years: doctor.experience_years || null,
    bio: doctor.bio || '',
    supports_home_visit: doctor.supports_home_visit || false,
  }
  showCreateModal.value = true
}

const openScheduleModal = async (doctor) => {
  scheduleModal.value = { show: true, doctor, saving: false, schedules: [] }

  // Fetch existing schedules
  try {
    const response = await api.get(`/doctors/${doctor.id}/schedules`)
    const schedules = response.data || []

    // Reset form
    for (const day of daysOfWeek) {
      scheduleForm.value[day] = { enabled: false, start: '08:00', end: '17:00' }
    }

    // Map schedules to form
    const dayMap = { 0: 'Thứ 2', 1: 'Thứ 3', 2: 'Thứ 4', 3: 'Thứ 5', 4: 'Thứ 6', 5: 'Thứ 7', 6: 'Chủ nhật' }
    for (const s of schedules) {
      const dayName = dayMap[s.day_of_week]
      if (dayName) {
        scheduleForm.value[dayName] = {
          enabled: s.is_active,
          start: s.start_time?.substring(0, 5) || '08:00',
          end: s.end_time?.substring(0, 5) || '17:00',
        }
      }
    }
  } catch (error) {
    console.error('Error fetching schedules:', error)
  }
}

const closeModal = () => {
  showCreateModal.value = false
  editingDoctor.value = null
  form.value = {
    name: '',
    clinic_id: selectedClinic.value || '',
    specialty: '',
    license_number: '',
    experience_years: null,
    bio: '',
    supports_home_visit: false,
  }
}

const saveDoctor = async () => {
  if (!form.value.name || !form.value.clinic_id || !form.value.specialty) {
    alert('Vui lòng nhập đầy đủ thông tin bắt buộc')
    return
  }

  saving.value = true
  try {
    const payload = { ...form.value }
    if (editingDoctor.value) {
      await api.put(`/doctors/${editingDoctor.value.id}`, payload)
    } else {
      await api.post('/doctors', payload)
    }
    closeModal()
    await fetchDoctors()
  } catch (error) {
    console.error('Error saving doctor:', error)
    alert('Lỗi khi lưu: ' + (error.response?.data?.detail || error.message))
  } finally {
    saving.value = false
  }
}

const saveSchedule = async () => {
  const doctor = scheduleModal.value.doctor
  if (!doctor) return

  scheduleModal.value.saving = true
  try {
    const dayMap = { 'Thứ 2': 0, 'Thứ 3': 1, 'Thứ 4': 2, 'Thứ 5': 3, 'Thứ 6': 4, 'Thứ 7': 5, 'Chủ nhật': 6 }

    // For each day, create/update schedule
    for (const [dayName, dayData] of Object.entries(scheduleForm.value)) {
      const payload = {
        day_of_week: dayMap[dayName],
        start_time: dayData.enabled ? dayData.start + ':00' : '08:00:00',
        end_time: dayData.enabled ? dayData.end + ':00' : '17:00:00',
        is_active: dayData.enabled,
        slot_duration_minutes: 30,
      }
      await api.post(`/doctors/${doctor.id}/schedules`, payload)
    }

    scheduleModal.value.show = false
    alert('Đã lưu lịch làm việc thành công')
  } catch (error) {
    console.error('Error saving schedule:', error)
    alert('Lỗi khi lưu lịch: ' + (error.response?.data?.detail || error.message))
  } finally {
    scheduleModal.value.saving = false
  }
}

const handleLogout = async () => {
  await authStore.logout()
  router.push('/login')
}

onMounted(async () => {
  await fetchClinics()
  await fetchDoctors()

  // Set default clinic if only one
  if (clinics.value.length === 1 && !selectedClinic.value) {
    selectedClinic.value = clinics.value[0].id
    await fetchDoctors()
  }
})
</script>
