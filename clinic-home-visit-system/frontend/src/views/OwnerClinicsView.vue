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
            <h1 class="text-lg font-semibold text-gray-900">Phòng khám của tôi</h1>
          </div>
          <button @click="showCreateModal = true" class="inline-flex items-center gap-2 px-4 py-2 bg-emerald-600 text-white rounded-lg text-sm font-medium hover:bg-emerald-700 transition-colors">
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4"/>
            </svg>
            Thêm phòng khám
          </button>
        </div>
      </header>

      <div class="max-w-7xl mx-auto px-8 py-6">
        <!-- Filters -->
        <div class="bg-white rounded-xl shadow-sm border border-gray-100 p-4 mb-4">
          <div class="flex flex-wrap gap-3">
            <input v-model="filters.search" @input="fetchClinics" placeholder="Tìm kiếm tên, địa chỉ..." class="px-3 py-2 border border-gray-200 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-emerald-500 w-64"/>
            <select v-model="filters.is_verified" @change="fetchClinics" class="px-3 py-2 border border-gray-200 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-emerald-500">
              <option value="">Tất cả trạng thái</option>
              <option value="true">Đã xác minh</option>
              <option value="false">Chưa xác minh</option>
            </select>
            <select v-model="filters.supports_home_visit" @change="fetchClinics" class="px-3 py-2 border border-gray-200 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-emerald-500">
              <option value="">Tất cả loại</option>
              <option value="true">Khám tại nhà</option>
              <option value="false">Chỉ khám tại phòng khám</option>
            </select>
            <button @click="clearFilters" class="px-3 py-2 border border-gray-200 rounded-lg text-sm text-gray-600 hover:bg-gray-50 transition-colors">Xóa lọc</button>
            <span class="ml-auto text-sm text-gray-500 self-center">Tổng: {{ total }} phòng khám</span>
          </div>
        </div>

        <!-- Table -->
        <div class="bg-white rounded-xl shadow-sm border border-gray-100 overflow-hidden">
          <div v-if="loading" class="text-center py-16">
            <div class="inline-block w-8 h-8 border-4 border-emerald-200 border-t-emerald-600 rounded-full animate-spin"></div>
            <p class="mt-3 text-sm text-gray-500">Đang tải...</p>
          </div>

          <div v-else-if="clinics.length === 0" class="text-center py-16">
            <div class="w-16 h-16 bg-gray-100 rounded-full flex items-center justify-center mx-auto mb-4">
              <svg class="w-8 h-8 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4"/>
              </svg>
            </div>
            <p class="text-gray-500">Bạn chưa có phòng khám nào</p>
            <button @click="showCreateModal = true" class="mt-4 px-4 py-2 bg-emerald-600 text-white rounded-lg text-sm font-medium hover:bg-emerald-700 transition-colors">
              Tạo phòng khám mới
            </button>
          </div>

          <div v-else class="overflow-x-auto">
            <table class="w-full">
              <thead class="bg-gray-50 border-b border-gray-100">
                <tr>
                  <th class="px-4 py-3 text-left text-xs font-semibold text-gray-500 uppercase">Tên</th>
                  <th class="px-4 py-3 text-left text-xs font-semibold text-gray-500 uppercase">Địa chỉ</th>
                  <th class="px-4 py-3 text-left text-xs font-semibold text-gray-500 uppercase">Chuyên khoa</th>
                  <th class="px-4 py-3 text-left text-xs font-semibold text-gray-500 uppercase">Giờ mở cửa</th>
                  <th class="px-4 py-3 text-left text-xs font-semibold text-gray-500 uppercase">Trạng thái</th>
                  <th class="px-4 py-3 text-left text-xs font-semibold text-gray-500 uppercase">Giá</th>
                  <th class="px-4 py-3 text-right text-xs font-semibold text-gray-500 uppercase">Hành động</th>
                </tr>
              </thead>
              <tbody class="divide-y divide-gray-50">
                <tr v-for="c in clinics" :key="c.id" class="hover:bg-gray-50 transition-colors">
                  <td class="px-4 py-3">
                    <div class="font-medium text-gray-900">{{ c.name }}</div>
                    <div class="text-xs text-gray-400 font-mono">{{ c.id.slice(0,8) }}...</div>
                  </td>
                  <td class="px-4 py-3 text-sm text-gray-600 max-w-48 truncate">{{ c.address }}</td>
                  <td class="px-4 py-3">
                    <div class="flex flex-wrap gap-1">
                      <span v-for="s in (c.specialties || []).slice(0, 2)" :key="s" class="px-2 py-0.5 bg-emerald-50 text-emerald-600 rounded text-xs">{{ s }}</span>
                      <span v-if="(c.specialties || []).length > 2" class="px-2 py-0.5 bg-gray-100 text-gray-500 rounded text-xs">+{{ c.specialties.length - 2 }}</span>
                    </div>
                  </td>
                  <td class="px-4 py-3 text-sm text-gray-600">{{ formatTime(c.opening_time) }} - {{ formatTime(c.closing_time) }}</td>
                  <td class="px-4 py-3">
                    <span :class="c.is_verified ? 'bg-green-100 text-green-700' : 'bg-yellow-100 text-yellow-700'" class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium">
                      {{ c.is_verified ? 'Đã xác minh' : 'Chưa xác minh' }}
                    </span>
                    <span v-if="c.supports_home_visit" class="ml-1 inline-flex items-center px-2 py-0.5 bg-purple-100 text-purple-700 rounded text-xs">Khám tại nhà</span>
                  </td>
                  <td class="px-4 py-3 text-sm text-gray-600">
                    <span v-if="c.min_price && c.max_price">{{ formatPrice(c.min_price) }} - {{ formatPrice(c.max_price) }}</span>
                    <span v-else-if="c.min_price">Từ {{ formatPrice(c.min_price) }}</span>
                    <span v-else class="text-gray-400">—</span>
                  </td>
                  <td class="px-4 py-3 text-right">
                    <div class="flex items-center gap-1 justify-end">
                      <button @click="openEditModal(c)"
                        class="px-2.5 py-1 bg-gray-100 text-gray-600 rounded-lg text-xs font-medium hover:bg-gray-200 transition-colors">
                        Sửa
                      </button>
                      <button @click="openDoctorsModal(c)"
                        class="px-2.5 py-1 bg-blue-50 text-blue-600 rounded-lg text-xs font-medium hover:bg-blue-100 transition-colors">
                        Bác sĩ
                      </button>
                      <button @click="openViewModal(c)"
                        class="px-2.5 py-1 bg-gray-100 text-gray-600 rounded-lg text-xs font-medium hover:bg-gray-200 transition-colors">
                        Xem
                      </button>
                    </div>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </main>

    <!-- Create/Edit Modal -->
    <div v-if="showCreateModal" class="fixed inset-0 bg-black/50 flex items-center justify-center z-50" @click.self="closeModal">
      <div class="bg-white rounded-xl shadow-xl max-w-2xl w-full mx-4 max-h-[90vh] overflow-y-auto">
        <div class="px-6 py-4 border-b border-gray-100 flex items-center justify-between">
          <h3 class="text-lg font-semibold text-gray-900">{{ editingClinic ? 'Sửa phòng khám' : 'Thêm phòng khám mới' }}</h3>
          <button @click="closeModal" class="p-1 rounded-lg hover:bg-gray-100 text-gray-400 hover:text-gray-600 transition-colors">
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/>
            </svg>
          </button>
        </div>
        <div class="px-6 py-4 space-y-4">
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1.5">Tên phòng khám *</label>
            <input v-model="form.name" type="text" placeholder="VD: Phòng khám Đa khoa ABC"
              class="w-full px-3 py-2 border border-gray-200 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-emerald-500 focus:border-transparent"/>
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1.5">Địa chỉ *</label>
            <input v-model="form.address" type="text" placeholder="VD: 123 Nguyễn Trãi, Q1, TP.HCM"
              class="w-full px-3 py-2 border border-gray-200 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-emerald-500 focus:border-transparent"/>
          </div>
          <div class="grid grid-cols-2 gap-4">
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1.5">Giờ mở cửa</label>
              <input v-model="form.opening_time" type="time"
                class="w-full px-3 py-2 border border-gray-200 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-emerald-500 focus:border-transparent"/>
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1.5">Giờ đóng cửa</label>
              <input v-model="form.closing_time" type="time"
                class="w-full px-3 py-2 border border-gray-200 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-emerald-500 focus:border-transparent"/>
            </div>
          </div>
          <div class="grid grid-cols-2 gap-4">
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1.5">Giá khám tối thiểu (VNĐ)</label>
              <input v-model.number="form.min_price" type="number" min="0" placeholder="VD: 100000"
                class="w-full px-3 py-2 border border-gray-200 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-emerald-500 focus:border-transparent"/>
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1.5">Giá khám tối đa (VNĐ)</label>
              <input v-model.number="form.max_price" type="number" min="0" placeholder="VD: 500000"
                class="w-full px-3 py-2 border border-gray-200 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-emerald-500 focus:border-transparent"/>
            </div>
          </div>
          <div class="grid grid-cols-2 gap-4">
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1.5">Latitude</label>
              <input v-model.number="form.lat" type="number" step="any" placeholder="VD: 10.7769"
                class="w-full px-3 py-2 border border-gray-200 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-emerald-500 focus:border-transparent"/>
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1.5">Longitude</label>
              <input v-model.number="form.lng" type="number" step="any" placeholder="VD: 106.7000"
                class="w-full px-3 py-2 border border-gray-200 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-emerald-500 focus:border-transparent"/>
            </div>
          </div>
          <div>
            <label class="flex items-center gap-3 cursor-pointer">
              <input type="checkbox" v-model="form.supports_home_visit" class="w-4 h-4 text-emerald-600 border-gray-300 rounded focus:ring-emerald-500"/>
              <span class="text-sm text-gray-700">Hỗ trợ khám tại nhà</span>
            </label>
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1.5">Mô tả</label>
            <textarea v-model="form.description" rows="3" placeholder="Mô tả về phòng khám..."
              class="w-full px-3 py-2 border border-gray-200 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-emerald-500 focus:border-transparent resize-none"></textarea>
          </div>
        </div>
        <div class="px-6 py-4 bg-gray-50 border-t border-gray-100 flex gap-2 justify-end">
          <button @click="closeModal"
            class="px-4 py-2 border border-gray-200 text-gray-700 rounded-lg text-sm font-medium hover:bg-gray-200 transition-colors">
            Hủy
          </button>
          <button @click="saveClinic" :disabled="saving"
            class="px-4 py-2 bg-emerald-600 text-white rounded-lg text-sm font-medium hover:bg-emerald-700 transition-colors disabled:opacity-60">
            {{ saving ? 'Đang lưu...' : (editingClinic ? 'Lưu thay đổi' : 'Tạo phòng khám') }}
          </button>
        </div>
      </div>
    </div>

    <!-- View Detail Modal -->
    <div v-if="viewModal.show" class="fixed inset-0 bg-black/50 flex items-center justify-center z-50" @click.self="viewModal.show = false">
      <div class="bg-white rounded-xl shadow-xl max-w-2xl w-full mx-4 max-h-[90vh] overflow-y-auto">
        <div class="px-6 py-4 border-b border-gray-100 flex items-center justify-between">
          <h3 class="text-lg font-semibold text-gray-900">Chi tiết phòng khám</h3>
          <button @click="viewModal.show = false" class="p-1 rounded-lg hover:bg-gray-100 text-gray-400 hover:text-gray-600 transition-colors">
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/>
            </svg>
          </button>
        </div>
        <div class="px-6 py-4 space-y-4">
          <div class="grid grid-cols-2 gap-4">
            <div>
              <p class="text-xs text-gray-500">Tên</p>
              <p class="font-medium text-gray-900">{{ viewModal.clinic?.name }}</p>
            </div>
            <div>
              <p class="text-xs text-gray-500">Trạng thái</p>
              <span :class="viewModal.clinic?.is_verified ? 'bg-green-100 text-green-700' : 'bg-yellow-100 text-yellow-700'" class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium">
                {{ viewModal.clinic?.is_verified ? 'Đã xác minh' : 'Chưa xác minh' }}
              </span>
            </div>
            <div class="col-span-2">
              <p class="text-xs text-gray-500">Địa chỉ</p>
              <p class="text-gray-900">{{ viewModal.clinic?.address }}</p>
            </div>
            <div>
              <p class="text-xs text-gray-500">Giờ mở cửa</p>
              <p class="text-gray-900">{{ formatTime(viewModal.clinic?.opening_time) }} - {{ formatTime(viewModal.clinic?.closing_time) }}</p>
            </div>
            <div>
              <p class="text-xs text-gray-500">Giá khám</p>
              <p class="text-gray-900">
                <span v-if="viewModal.clinic?.min_price && viewModal.clinic?.max_price">{{ formatPrice(viewModal.clinic?.min_price) }} - {{ formatPrice(viewModal.clinic?.max_price) }}</span>
                <span v-else-if="viewModal.clinic?.min_price">Từ {{ formatPrice(viewModal.clinic?.min_price) }}</span>
                <span v-else class="text-gray-400">—</span>
              </p>
            </div>
            <div>
              <p class="text-xs text-gray-500">Khám tại nhà</p>
              <p class="text-gray-900">{{ viewModal.clinic?.supports_home_visit ? 'Có' : 'Không' }}</p>
            </div>
            <div>
              <p class="text-xs text-gray-500">Số bác sĩ</p>
              <p class="text-gray-900">{{ viewModal.clinic?.doctor_count || 0 }}</p>
            </div>
            <div v-if="viewModal.clinic?.description" class="col-span-2">
              <p class="text-xs text-gray-500">Mô tả</p>
              <p class="text-gray-900">{{ viewModal.clinic?.description }}</p>
            </div>
          </div>
        </div>
        <div class="px-6 py-4 bg-gray-50 border-t border-gray-100 flex gap-2 justify-end">
          <button @click="viewModal.show = false" class="px-4 py-2 bg-gray-200 text-gray-700 rounded-lg text-sm font-medium hover:bg-gray-300 transition-colors">Đóng</button>
          <button @click="openEditModal(viewModal.clinic); viewModal.show = false" class="px-4 py-2 bg-emerald-600 text-white rounded-lg text-sm font-medium hover:bg-emerald-700 transition-colors">Sửa</button>
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
const total = ref(0)
const loading = ref(false)
const saving = ref(false)

const filters = ref({
  search: '',
  is_verified: '',
  supports_home_visit: '',
})

const form = ref({
  name: '',
  address: '',
  opening_time: '08:00',
  closing_time: '17:00',
  min_price: null,
  max_price: null,
  lat: null,
  lng: null,
  supports_home_visit: false,
  description: '',
})

const showCreateModal = ref(false)
const editingClinic = ref(null)
const viewModal = ref({ show: false, clinic: null })

const formatTime = (time) => {
  if (!time) return '—'
  return time
}

const formatPrice = (price) => {
  if (!price) return '—'
  return new Intl.NumberFormat('vi-VN', { style: 'currency', currency: 'VND' }).format(price)
}

const fetchClinics = async () => {
  loading.value = true
  try {
    const params = {}
    if (filters.value.search) params.search = filters.value.search
    if (filters.value.is_verified) params.is_verified = filters.value.is_verified
    if (filters.value.supports_home_visit) params.supports_home_visit = filters.value.supports_home_visit

    // For clinic owner, use the owner endpoint
    const response = await api.get('/clinics/owner/my-clinics', { params })
    clinics.value = response.data.clinics || response.data || []
    total.value = clinics.value.length
  } catch (error) {
    console.error('Error fetching clinics:', error)
    // Fallback to regular clinics endpoint
    try {
      const response = await api.get('/clinics', { params })
      clinics.value = response.data.clinics || response.data || []
      total.value = clinics.value.length
    } catch (e) {
      console.error('Fallback also failed:', e)
    }
  } finally {
    loading.value = false
  }
}

const clearFilters = () => {
  filters.value = { search: '', is_verified: '', supports_home_visit: '' }
  fetchClinics()
}

const openEditModal = (clinic) => {
  editingClinic.value = clinic
  form.value = {
    name: clinic.name || '',
    address: clinic.address || '',
    opening_time: clinic.opening_time || '08:00',
    closing_time: clinic.closing_time || '17:00',
    min_price: clinic.min_price || null,
    max_price: clinic.max_price || null,
    lat: clinic.lat || null,
    lng: clinic.lng || null,
    supports_home_visit: clinic.supports_home_visit || false,
    description: clinic.description || '',
  }
  showCreateModal.value = true
}

const openViewModal = (clinic) => {
  viewModal.value = { show: true, clinic }
}

const openDoctorsModal = (clinic) => {
  router.push(`/owner/doctors?clinic_id=${clinic.id}`)
}

const closeModal = () => {
  showCreateModal.value = false
  editingClinic.value = null
  form.value = {
    name: '',
    address: '',
    opening_time: '08:00',
    closing_time: '17:00',
    min_price: null,
    max_price: null,
    lat: null,
    lng: null,
    supports_home_visit: false,
    description: '',
  }
}

const saveClinic = async () => {
  if (!form.value.name || !form.value.address) {
    alert('Vui lòng nhập tên và địa chỉ phòng khám')
    return
  }

  saving.value = true
  try {
    const payload = { ...form.value }
    if (editingClinic.value) {
      await api.put(`/clinics/${editingClinic.value.id}`, payload)
    } else {
      await api.post('/clinics', payload)
    }
    closeModal()
    await fetchClinics()
  } catch (error) {
    console.error('Error saving clinic:', error)
    alert('Lỗi khi lưu phòng khám: ' + (error.response?.data?.detail || error.message))
  } finally {
    saving.value = false
  }
}

const handleLogout = async () => {
  await authStore.logout()
  router.push('/login')
}

onMounted(() => {
  fetchClinics()
})
</script>
