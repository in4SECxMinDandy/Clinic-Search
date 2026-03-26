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
            <h1 class="text-lg font-semibold text-gray-900">Quản lý Bác sĩ</h1>
          </div>
          <button @click="openCreateModal" class="inline-flex items-center gap-2 px-4 py-2 bg-indigo-600 text-white rounded-lg text-sm font-medium hover:bg-indigo-700 transition-colors">
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4"/>
            </svg>
            Thêm bác sĩ
          </button>
        </div>
      </div>
    </header>

    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
      <!-- Filters -->
      <div class="bg-white rounded-xl shadow-sm border border-gray-100 p-4 mb-4">
        <div class="flex flex-wrap gap-3">
          <select v-model="filters.clinic_id" @change="fetchDoctors" class="px-3 py-2 border border-gray-200 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500 min-w-48">
            <option value="">Tất cả phòng khám</option>
            <option v-for="c in clinics" :key="c.id" :value="c.id">{{ c.name }}</option>
          </select>
          <input v-model="filters.specialty" @input="fetchDoctors" placeholder="Tìm chuyên khoa..." class="px-3 py-2 border border-gray-200 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500 w-48"/>
          <select v-model="filters.supports_home_visit" @change="fetchDoctors" class="px-3 py-2 border border-gray-200 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500">
            <option value="">Tất cả</option>
            <option value="true">Khám tại nhà</option>
            <option value="false">Chỉ tại phòng khám</option>
          </select>
          <button @click="clearFilters" class="px-3 py-2 border border-gray-200 rounded-lg text-sm text-gray-600 hover:bg-gray-50 transition-colors">Xóa lọc</button>
          <span class="ml-auto text-sm text-gray-500 self-center">Tổng: {{ total }} bác sĩ</span>
        </div>
      </div>

      <!-- Table -->
      <div class="bg-white rounded-xl shadow-sm border border-gray-100 overflow-hidden">
        <div v-if="loading" class="text-center py-16">
          <div class="inline-block w-8 h-8 border-4 border-indigo-200 border-t-indigo-600 rounded-full animate-spin"></div>
          <p class="mt-3 text-sm text-gray-500">Đang tải...</p>
        </div>

        <div v-else-if="doctors.length === 0" class="text-center py-16">
          <div class="w-16 h-16 bg-gray-100 rounded-full flex items-center justify-center mx-auto mb-4">
            <svg class="w-8 h-8 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"/>
            </svg>
          </div>
          <p class="text-gray-500">Không có bác sĩ nào</p>
        </div>

        <div v-else class="overflow-x-auto">
          <table class="w-full">
            <thead class="bg-gray-50 border-b border-gray-100">
              <tr>
                <th class="px-4 py-3 text-left text-xs font-semibold text-gray-500 uppercase">Bác sĩ</th>
                <th class="px-4 py-3 text-left text-xs font-semibold text-gray-500 uppercase">Chuyên khoa</th>
                <th class="px-4 py-3 text-left text-xs font-semibold text-gray-500 uppercase">Phòng khám</th>
                <th class="px-4 py-3 text-left text-xs font-semibold text-gray-500 uppercase">Kinh nghiệm</th>
                <th class="px-4 py-3 text-left text-xs font-semibold text-gray-500 uppercase">Đánh giá</th>
                <th class="px-4 py-3 text-left text-xs font-semibold text-gray-500 uppercase">Trạng thái</th>
                <th class="px-4 py-3 text-right text-xs font-semibold text-gray-500 uppercase">Hành động</th>
              </tr>
            </thead>
            <tbody class="divide-y divide-gray-50">
              <tr v-for="d in doctors" :key="d.id" class="hover:bg-gray-50 transition-colors">
                <td class="px-4 py-3">
                  <div class="flex items-center gap-3">
                    <div class="w-9 h-9 bg-indigo-100 rounded-full flex items-center justify-center text-xs font-bold text-indigo-600">
                      {{ getInitials(d.name) }}
                    </div>
                    <div>
                      <div class="font-medium text-gray-900">{{ d.name }}</div>
                      <div class="text-xs text-gray-400 font-mono">{{ d.id.slice(0,8) }}...</div>
                    </div>
                  </div>
                </td>
                <td class="px-4 py-3 text-sm text-gray-600">{{ d.specialty }}</td>
                <td class="px-4 py-3 text-sm text-gray-600">{{ getClinicName(d.clinic_id) }}</td>
                <td class="px-4 py-3 text-sm text-gray-600">{{ d.experience_years }} năm</td>
                <td class="px-4 py-3">
                  <div class="flex items-center gap-1">
                    <svg class="w-4 h-4 text-yellow-400" fill="currentColor" viewBox="0 0 20 20"><path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z"/></svg>
                    <span class="text-sm font-medium text-gray-700">{{ d.rating.toFixed(1) }}</span>
                    <span class="text-xs text-gray-400">({{ d.total_reviews }})</span>
                  </div>
                </td>
                <td class="px-4 py-3">
                  <span :class="d.is_verified ? 'bg-green-100 text-green-700' : 'bg-yellow-100 text-yellow-700'" class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium">
                    {{ d.is_verified ? 'Đã xác minh' : 'Chưa xác minh' }}
                  </span>
                  <span v-if="d.supports_home_visit" class="ml-1 inline-flex items-center px-2 py-0.5 bg-purple-100 text-purple-700 rounded text-xs">Khám tại nhà</span>
                  <span :class="d.is_active ? 'bg-green-100 text-green-700' : 'bg-red-100 text-red-700'" class="ml-1 inline-flex items-center px-2 py-0.5 rounded text-xs">
                    {{ d.is_active ? 'Hoạt động' : 'Không hoạt động' }}
                  </span>
                </td>
                <td class="px-4 py-3 text-right">
                  <div class="flex items-center gap-1 justify-end">
                    <button @click="openEditModal(d)" class="px-2.5 py-1 bg-indigo-50 text-indigo-600 rounded-lg text-xs font-medium hover:bg-indigo-100 transition-colors">Sửa</button>
                    <button @click="deleteDoctor(d)" class="px-2.5 py-1 bg-red-50 text-red-600 rounded-lg text-xs font-medium hover:bg-red-100 transition-colors">Xóa</button>
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
    <div v-if="showModal" class="fixed inset-0 bg-black/50 flex items-center justify-center z-50 p-4" @click.self="closeModal">
      <div class="bg-white rounded-xl shadow-xl max-w-2xl w-full max-h-[90vh] overflow-y-auto">
        <div class="px-6 py-4 border-b border-gray-100 flex items-center justify-between">
          <h3 class="text-lg font-semibold text-gray-900">{{ editDoctor ? 'Sửa bác sĩ' : 'Thêm bác sĩ' }}</h3>
          <button @click="closeModal" class="p-1 rounded-lg hover:bg-gray-100 text-gray-400 hover:text-gray-600 transition-colors">
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/></svg>
          </button>
        </div>
        <div class="px-6 py-4 space-y-4">
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">Tên bác sĩ *</label>
            <input v-model="form.name" type="text" class="w-full px-3 py-2 border border-gray-200 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500" placeholder="VD: BS. Nguyễn Văn A"/>
          </div>
          <div class="grid grid-cols-2 gap-4">
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">Phòng khám *</label>
              <select v-model="form.clinic_id" class="w-full px-3 py-2 border border-gray-200 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500">
                <option value="">-- Chọn phòng khám --</option>
                <option v-for="c in clinics" :key="c.id" :value="c.id">{{ c.name }}</option>
              </select>
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">Chuyên khoa *</label>
              <input v-model="form.specialty" type="text" class="w-full px-3 py-2 border border-gray-200 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500" placeholder="VD: Nội khoa"/>
            </div>
          </div>
          <div class="grid grid-cols-2 gap-4">
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">Số năm kinh nghiệm</label>
              <input v-model.number="form.experience_years" type="number" min="0" class="w-full px-3 py-2 border border-gray-200 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500" placeholder="5"/>
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">Số chứng chỉ hành nghề</label>
              <input v-model="form.license_number" type="text" class="w-full px-3 py-2 border border-gray-200 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500" placeholder="VD: 001234/YT"/>
            </div>
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">Bio</label>
            <textarea v-model="form.bio" rows="3" class="w-full px-3 py-2 border border-gray-200 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500 resize-none" placeholder="Giới thiệu bản thân..."></textarea>
          </div>
          <div class="flex items-center gap-6">
            <label class="flex items-center gap-2 cursor-pointer">
              <input type="checkbox" v-model="form.supports_home_visit" class="w-4 h-4 text-indigo-600 rounded border-gray-300 focus:ring-indigo-500"/>
              <span class="text-sm text-gray-700">Hỗ trợ khám tại nhà</span>
            </label>
            <div v-if="form.supports_home_visit">
              <label class="block text-sm font-medium text-gray-700 mb-1">Bán kính (km)</label>
              <input v-model.number="form.available_home_visit_radius_km" type="number" min="0" max="50" class="w-32 px-3 py-2 border border-gray-200 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500"/>
            </div>
          </div>
        </div>
        <div class="px-6 py-4 bg-gray-50 border-t border-gray-100 flex gap-2 justify-end">
          <button @click="closeModal" class="px-4 py-2 border border-gray-200 text-gray-700 rounded-lg text-sm font-medium hover:bg-gray-200 transition-colors">Hủy</button>
          <button @click="saveDoctor" :disabled="saving" class="px-4 py-2 bg-indigo-600 text-white rounded-lg text-sm font-medium hover:bg-indigo-700 transition-colors disabled:opacity-60">
            {{ saving ? 'Đang lưu...' : (editDoctor ? 'Lưu thay đổi' : 'Tạo mới') }}
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import api from '../services/api'

const doctors = ref([])
const clinics = ref([])
const loading = ref(false)
const saving = ref(false)
const page = ref(1)
const pageSize = ref(20)
const total = ref(0)
const showModal = ref(false)
const editDoctor = ref(null)

const filters = ref({ clinic_id: '', specialty: '', supports_home_visit: '' })

const form = ref({
  clinic_id: '', name: '', specialty: '', license_number: '',
  experience_years: 0, bio: '', avatar: '',
  supports_home_visit: false, available_home_visit_radius_km: 5,
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

const getInitials = (name) => {
  if (!name) return '?'
  return name.split(' ').map(w => w[0]).join('').toUpperCase().slice(0, 2)
}

const getClinicName = (clinicId) => {
  const c = clinics.value.find(x => x.id === clinicId)
  return c ? c.name : clinicId ? clinicId.slice(0, 8) + '...' : '—'
}

const fetchClinics = async () => {
  try {
    const response = await api.get('/clinics', { params: { page: 1, page_size: 100 } })
    clinics.value = response.data.clinics || []
  } catch (e) { console.error('Error fetching clinics:', e) }
}

const fetchDoctors = async () => {
  loading.value = true
  try {
    const params = { page: page.value, page_size: pageSize.value }
    if (filters.value.clinic_id) params.clinic_id = filters.value.clinic_id
    if (filters.value.specialty) params.specialty = filters.value.specialty
    if (filters.value.supports_home_visit) params.supports_home_visit = filters.value.supports_home_visit
    const response = await api.get('/doctors', { params })
    doctors.value = response.data || []
    total.value = doctors.value.length
  } catch (error) {
    console.error('Error fetching doctors:', error)
  } finally {
    loading.value = false
  }
}

const clearFilters = () => {
  filters.value = { clinic_id: '', specialty: '', supports_home_visit: '' }
  page.value = 1
  fetchDoctors()
}

const changePage = (p) => { page.value = p; fetchDoctors() }

const resetForm = () => {
  form.value = {
    clinic_id: '', name: '', specialty: '', license_number: '',
    experience_years: 0, bio: '', avatar: '',
    supports_home_visit: false, available_home_visit_radius_km: 5,
  }
}

const openCreateModal = () => {
  editDoctor.value = null
  resetForm()
  showModal.value = true
}

const openEditModal = (doctor) => {
  editDoctor.value = doctor
  form.value = {
    clinic_id: doctor.clinic_id,
    name: doctor.name,
    specialty: doctor.specialty,
    license_number: doctor.license_number || '',
    experience_years: doctor.experience_years || 0,
    bio: doctor.bio || '',
    avatar: doctor.avatar || '',
    supports_home_visit: doctor.supports_home_visit || false,
    available_home_visit_radius_km: doctor.available_home_visit_radius_km || 5,
  }
  showModal.value = true
}

const closeModal = () => {
  showModal.value = false
  editDoctor.value = null
  resetForm()
}

const saveDoctor = async () => {
  if (!form.value.name || !form.value.clinic_id || !form.value.specialty) {
    alert('Vui lòng điền đầy đủ thông tin bắt buộc')
    return
  }
  saving.value = true
  try {
    const payload = { ...form.value }
    if (editDoctor.value) {
      await api.put(`/doctors/${editDoctor.value.id}`, payload)
    } else {
      await api.post('/doctors', payload)
    }
    closeModal()
    await fetchDoctors()
  } catch (error) {
    console.error('Error saving doctor:', error)
    alert('Lỗi: ' + (error.response?.data?.detail || 'Vui lòng thử lại'))
  } finally {
    saving.value = false
  }
}

const deleteDoctor = async (doctor) => {
  if (!confirm(`Xóa bác sĩ "${doctor.name}"?`)) return
  try {
    await api.delete(`/doctors/${doctor.id}`)
    await fetchDoctors()
  } catch (error) {
    console.error('Error deleting doctor:', error)
    alert('Lỗi: ' + (error.response?.data?.detail || 'Vui lòng thử lại'))
  }
}

onMounted(() => {
  fetchClinics()
  fetchDoctors()
})
</script>
