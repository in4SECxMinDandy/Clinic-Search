<template>
  <div class="min-h-screen bg-gray-50">
    <!-- Header -->
    <header class="bg-white border-b border-gray-200 sticky top-0 z-10">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="flex justify-between items-center h-16">
          <div class="flex items-center gap-4">
            <router-link to="/admin" class="flex items-center gap-2 text-sm text-gray-500 hover:text-gray-900 transition-colors">
              <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7"/>
              </svg>
              Quay lại Dashboard
            </router-link>
            <div class="h-6 w-px bg-gray-200"></div>
            <h1 class="text-lg font-semibold text-gray-900">Quản lý Phòng khám</h1>
          </div>
          <button @click="showCreateModal = true" class="inline-flex items-center gap-2 px-4 py-2 bg-indigo-600 text-white rounded-lg text-sm font-medium hover:bg-indigo-700 transition-colors">
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4"/>
            </svg>
            Thêm phòng khám
          </button>
        </div>
      </div>
    </header>

    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
      <!-- Filters -->
      <div class="bg-white rounded-xl shadow-sm border border-gray-100 p-4 mb-4">
        <div class="flex flex-wrap gap-3">
          <input v-model="filters.search" @input="fetchClinics" placeholder="Tìm kiếm tên, địa chỉ..." class="px-3 py-2 border border-gray-200 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500 w-64"/>
          <select v-model="filters.is_verified" @change="fetchClinics" class="px-3 py-2 border border-gray-200 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500">
            <option value="">Tất cả trạng thái</option>
            <option value="true">Đã xác minh</option>
            <option value="false">Chưa xác minh</option>
          </select>
          <select v-model="filters.supports_home_visit" @change="fetchClinics" class="px-3 py-2 border border-gray-200 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500">
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
          <div class="inline-block w-8 h-8 border-4 border-indigo-200 border-t-indigo-600 rounded-full animate-spin"></div>
          <p class="mt-3 text-sm text-gray-500">Đang tải...</p>
        </div>

        <div v-else-if="clinics.length === 0" class="text-center py-16">
          <div class="w-16 h-16 bg-gray-100 rounded-full flex items-center justify-center mx-auto mb-4">
            <svg class="w-8 h-8 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4"/>
            </svg>
          </div>
          <p class="text-gray-500">Không có phòng khám nào</p>
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
                    <span v-for="s in (c.specialties || []).slice(0, 2)" :key="s" class="px-2 py-0.5 bg-indigo-50 text-indigo-600 rounded text-xs">{{ s }}</span>
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
                    <button @click="openEditModal(c)" class="px-2.5 py-1 bg-indigo-50 text-indigo-600 rounded-lg text-xs font-medium hover:bg-indigo-100 transition-colors">Sửa</button>
                    <button @click="deleteClinic(c)" class="px-2.5 py-1 bg-red-50 text-red-600 rounded-lg text-xs font-medium hover:bg-red-100 transition-colors">Xóa</button>
                  </div>
                </td>
              </tr>
            </tbody>
          </table>

          <!-- Pagination -->
          <div class="px-4 py-3 border-t border-gray-100 flex items-center justify-between">
            <div class="text-sm text-gray-500">Trang {{ page }} / {{ totalPages }}</div>
            <div class="flex gap-1">
              <button @click="changePage(page - 1)" :disabled="page <= 1" class="px-3 py-1.5 rounded-lg text-sm border border-gray-200 hover:bg-gray-50 disabled:opacity-40 transition-colors">‹</button>
              <button v-for="p in visiblePages" :key="p" @click="changePage(p)" :class="p === page ? 'bg-indigo-600 text-white border-indigo-600' : 'bg-white text-gray-700 border-gray-200 hover:bg-gray-50'" class="px-3 py-1.5 rounded-lg text-sm border transition-colors">{{ p }}</button>
              <button @click="changePage(page + 1)" :disabled="page >= totalPages" class="px-3 py-1.5 rounded-lg text-sm border border-gray-200 hover:bg-gray-50 disabled:opacity-40 transition-colors">›</button>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Create/Edit Modal -->
    <div v-if="showCreateModal || editModal.clinic" class="fixed inset-0 bg-black/50 flex items-center justify-center z-50 p-4" @click.self="closeModal">
      <div class="bg-white rounded-xl shadow-xl max-w-2xl w-full max-h-[90vh] overflow-y-auto">
        <div class="px-6 py-4 border-b border-gray-100 flex items-center justify-between">
          <h3 class="text-lg font-semibold text-gray-900">{{ editModal.clinic ? 'Sửa phòng khám' : 'Thêm phòng khám' }}</h3>
          <button @click="closeModal" class="p-1 rounded-lg hover:bg-gray-100 text-gray-400 hover:text-gray-600 transition-colors">
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/></svg>
          </button>
        </div>
        <div class="px-6 py-4 space-y-4">
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">Tên phòng khám *</label>
            <input v-model="form.name" type="text" class="w-full px-3 py-2 border border-gray-200 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500" placeholder="VD: Phòng khám Đa khoa An Khang"/>
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">Địa chỉ *</label>
            <input v-model="form.address" type="text" class="w-full px-3 py-2 border border-gray-200 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500" placeholder="VD: 123 Nguyễn Trãi, Quận 1, TP.HCM"/>
          </div>
          <div class="grid grid-cols-2 gap-4">
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">Vĩ độ (lat) *</label>
              <input v-model.number="form.lat" type="number" step="0.00000001" class="w-full px-3 py-2 border border-gray-200 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500" placeholder="10.7629"/>
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">Kinh độ (lng) *</label>
              <input v-model.number="form.lng" type="number" step="0.00000001" class="w-full px-3 py-2 border border-gray-200 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500" placeholder="106.6603"/>
            </div>
          </div>
          <div class="grid grid-cols-2 gap-4">
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">Giờ mở cửa *</label>
              <input v-model="form.opening_time" type="time" class="w-full px-3 py-2 border border-gray-200 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500"/>
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">Giờ đóng cửa *</label>
              <input v-model="form.closing_time" type="time" class="w-full px-3 py-2 border border-gray-200 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500"/>
            </div>
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">Chuyên khoa * (phân cách bằng dấu phẩy)</label>
            <input v-model="specialtiesInput" type="text" class="w-full px-3 py-2 border border-gray-200 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500" placeholder="nội khoa, ngoại khoa, da liễu"/>
          </div>
          <div class="grid grid-cols-2 gap-4">
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">Giá tối thiểu (VNĐ)</label>
              <input v-model.number="form.min_price" type="number" class="w-full px-3 py-2 border border-gray-200 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500" placeholder="50000"/>
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">Giá tối đa (VNĐ)</label>
              <input v-model.number="form.max_price" type="number" class="w-full px-3 py-2 border border-gray-200 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500" placeholder="200000"/>
            </div>
          </div>
          <div class="grid grid-cols-2 gap-4">
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">Số điện thoại</label>
              <input v-model="form.phone" type="text" class="w-full px-3 py-2 border border-gray-200 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500" placeholder="028 1234 5678"/>
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">Email</label>
              <input v-model="form.email" type="email" class="w-full px-3 py-2 border border-gray-200 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500" placeholder="contact@clinic.vn"/>
            </div>
          </div>
          <div class="flex items-center gap-6">
            <label class="flex items-center gap-2 cursor-pointer">
              <input type="checkbox" v-model="form.supports_home_visit" class="w-4 h-4 text-indigo-600 rounded border-gray-300 focus:ring-indigo-500"/>
              <span class="text-sm text-gray-700">Hỗ trợ khám tại nhà</span>
            </label>
            <div v-if="form.supports_home_visit">
              <label class="block text-sm font-medium text-gray-700 mb-1">Bán kính khám tại nhà (km)</label>
              <input v-model.number="form.home_visit_radius_km" type="number" class="w-32 px-3 py-2 border border-gray-200 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500"/>
            </div>
          </div>
        </div>
        <div class="px-6 py-4 bg-gray-50 border-t border-gray-100 flex gap-2 justify-end">
          <button @click="closeModal" class="px-4 py-2 border border-gray-200 text-gray-700 rounded-lg text-sm font-medium hover:bg-gray-200 transition-colors">Hủy</button>
          <button @click="saveClinic" :disabled="saving" class="px-4 py-2 bg-indigo-600 text-white rounded-lg text-sm font-medium hover:bg-indigo-700 transition-colors disabled:opacity-60">
            {{ saving ? 'Đang lưu...' : (editModal.clinic ? 'Lưu thay đổi' : 'Tạo mới') }}
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import api from '../services/api'

const clinics = ref([])
const loading = ref(false)
const saving = ref(false)
const page = ref(1)
const pageSize = ref(20)
const total = ref(0)

const filters = ref({ search: '', is_verified: '', supports_home_visit: '' })
const showCreateModal = ref(false)
const editModal = ref({ clinic: null })
const specialtiesInput = ref('')

const form = ref({
  name: '', address: '', lat: null, lng: null,
  opening_time: '08:00', closing_time: '17:00',
  specialties: [], min_price: null, max_price: null,
  phone: '', email: '',
  supports_home_visit: false, home_visit_radius_km: 10,
})

const totalPages = computed(() => Math.max(1, Math.ceil(total.value / pageSize.value)))

const visiblePages = computed(() => {
  const pages = []
  const total = totalPages.value
  const current = page.value
  let start = Math.max(1, current - 2)
  let end = Math.min(total, start + 4)
  if (end - start < 4) start = Math.max(1, end - 4)
  for (let i = start; i <= end; i++) pages.push(i)
  return pages
})

const fetchClinics = async () => {
  loading.value = true
  try {
    const params = { page: page.value, page_size: pageSize.value }
    if (filters.value.search) params.search = filters.value.search
    if (filters.value.is_verified !== '') params.is_verified = filters.value.is_verified
    if (filters.value.supports_home_visit !== '') params.supports_home_visit = filters.value.supports_home_visit
    const response = await api.get('/clinics', { params })
    clinics.value = response.data.clinics || []
    total.value = response.data.total || 0
  } catch (error) {
    console.error('Error fetching clinics:', error)
  } finally {
    loading.value = false
  }
}

const clearFilters = () => {
  filters.value = { search: '', is_verified: '', supports_home_visit: '' }
  page.value = 1
  fetchClinics()
}

const changePage = (p) => { page.value = p; fetchClinics() }

const resetForm = () => {
  form.value = {
    name: '', address: '', lat: null, lng: null,
    opening_time: '08:00', closing_time: '17:00',
    specialties: [], min_price: null, max_price: null,
    phone: '', email: '',
    supports_home_visit: false, home_visit_radius_km: 10,
  }
  specialtiesInput.value = ''
}

const openEditModal = (clinic) => {
  editModal.value.clinic = clinic
  form.value = {
    name: clinic.name,
    address: clinic.address,
    lat: clinic.lat,
    lng: clinic.lng,
    opening_time: clinic.opening_time ? String(clinic.opening_time).substring(0, 5) : '08:00',
    closing_time: clinic.closing_time ? String(clinic.closing_time).substring(0, 5) : '17:00',
    specialties: clinic.specialties || [],
    min_price: clinic.min_price || null,
    max_price: clinic.max_price || null,
    phone: clinic.phone || '',
    email: clinic.email || '',
    supports_home_visit: clinic.supports_home_visit || false,
    home_visit_radius_km: clinic.home_visit_radius_km || 10,
  }
  specialtiesInput.value = (clinic.specialties || []).join(', ')
}

const closeModal = () => {
  showCreateModal.value = false
  editModal.value.clinic = null
  resetForm()
}

const saveClinic = async () => {
  saving.value = true
  try {
    const specialties = specialtiesInput.value.split(',').map(s => s.trim().toLowerCase()).filter(Boolean)
    const payload = {
      ...form.value,
      specialties,
      opening_time: form.value.opening_time + ':00',
      closing_time: form.value.closing_time + ':00',
    }
    if (editModal.value.clinic) {
      await api.put(`/clinics/${editModal.value.clinic.id}`, payload)
    } else {
      await api.post('/clinics', payload)
    }
    closeModal()
    await fetchClinics()
  } catch (error) {
    console.error('Error saving clinic:', error)
    alert('Lỗi khi lưu: ' + (error.response?.data?.detail || 'Vui lòng thử lại'))
  } finally {
    saving.value = false
  }
}

const deleteClinic = async (clinic) => {
  if (!confirm(`Xóa phòng khám "${clinic.name}"?`)) return
  try {
    await api.delete(`/clinics/${clinic.id}`)
    await fetchClinics()
  } catch (error) {
    console.error('Error deleting clinic:', error)
    alert('Lỗi khi xóa: ' + (error.response?.data?.detail || 'Vui lòng thử lại'))
  }
}

const formatTime = (t) => {
  if (!t) return '—'
  const s = String(t).substring(0, 5)
  return s
}

const formatPrice = (p) => {
  if (!p) return '—'
  return new Intl.NumberFormat('vi-VN', { style: 'currency', currency: 'VND' }).format(p).replace('₫', 'đ').trim()
}

onMounted(() => { fetchClinics() })
</script>
