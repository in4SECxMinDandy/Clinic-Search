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
            <h1 class="text-lg font-semibold text-gray-900">Quản lý Chủ phòng khám</h1>
          </div>
        </div>
      </div>
    </header>

    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
      <!-- Info Box -->
      <div class="bg-indigo-50 border border-indigo-200 rounded-xl p-4 mb-4">
        <p class="text-sm text-indigo-800">
          <strong>Chủ phòng khám (Clinic Owner)</strong> là người có quyền quản lý phòng khám và bác sĩ của họ.
          Bạn có thể nâng cấp một tài khoản <strong>patient</strong> thành <strong>clinic_owner</strong> để cấp quyền quản lý phòng khám.
        </p>
      </div>

      <!-- Filters -->
      <div class="bg-white rounded-xl shadow-sm border border-gray-100 p-4 mb-4">
        <div class="flex flex-wrap gap-3">
          <select v-model="filters.role" @change="fetchUsers" class="px-3 py-2 border border-gray-200 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500">
            <option value="">Tất cả vai trò</option>
            <option value="patient">Bệnh nhân</option>
            <option value="clinic_owner">Chủ phòng khám</option>
            <option value="doctor">Bác sĩ</option>
            <option value="admin">Admin</option>
          </select>
          <button @click="clearFilters" class="px-3 py-2 border border-gray-200 rounded-lg text-sm text-gray-600 hover:bg-gray-50 transition-colors">Xóa lọc</button>
          <span class="ml-auto text-sm text-gray-500 self-center">Tổng: {{ total }} người dùng</span>
        </div>
      </div>

      <!-- Table -->
      <div class="bg-white rounded-xl shadow-sm border border-gray-100 overflow-hidden">
        <div v-if="loading" class="text-center py-16">
          <div class="inline-block w-8 h-8 border-4 border-indigo-200 border-t-indigo-600 rounded-full animate-spin"></div>
          <p class="mt-3 text-sm text-gray-500">Đang tải...</p>
        </div>

        <div v-else-if="users.length === 0" class="text-center py-16">
          <div class="w-16 h-16 bg-gray-100 rounded-full flex items-center justify-center mx-auto mb-4">
            <svg class="w-8 h-8 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0z"/>
            </svg>
          </div>
          <p class="text-gray-500">Không có người dùng nào</p>
        </div>

        <div v-else class="overflow-x-auto">
          <table class="w-full">
            <thead class="bg-gray-50 border-b border-gray-100">
              <tr>
                <th class="px-4 py-3 text-left text-xs font-semibold text-gray-500 uppercase">Người dùng</th>
                <th class="px-4 py-3 text-left text-xs font-semibold text-gray-500 uppercase">Email</th>
                <th class="px-4 py-3 text-left text-xs font-semibold text-gray-500 uppercase">Số điện thoại</th>
                <th class="px-4 py-3 text-left text-xs font-semibold text-gray-500 uppercase">Vai trò</th>
                <th class="px-4 py-3 text-left text-xs font-semibold text-gray-500 uppercase">Trạng thái</th>
                <th class="px-4 py-3 text-left text-xs font-semibold text-gray-500 uppercase">Ngày tạo</th>
                <th class="px-4 py-3 text-right text-xs font-semibold text-gray-500 uppercase">Hành động</th>
              </tr>
            </thead>
            <tbody class="divide-y divide-gray-50">
              <tr v-for="u in users" :key="u.id" class="hover:bg-gray-50 transition-colors">
                <td class="px-4 py-3">
                  <div class="flex items-center gap-3">
                    <div class="w-8 h-8 bg-indigo-100 rounded-full flex items-center justify-center text-xs font-bold text-indigo-600">
                      {{ getInitials(u.full_name) }}
                    </div>
                    <div class="text-sm font-medium text-gray-900">{{ u.full_name }}</div>
                  </div>
                </td>
                <td class="px-4 py-3 text-sm text-gray-600">{{ u.email }}</td>
                <td class="px-4 py-3 text-sm text-gray-500">{{ u.phone || '—' }}</td>
                <td class="px-4 py-3">
                  <span :class="roleClass(u.role)" class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium">
                    {{ roleLabel(u.role) }}
                  </span>
                </td>
                <td class="px-4 py-3">
                  <span :class="u.is_active ? 'bg-green-100 text-green-700' : 'bg-red-100 text-red-700'"
                    class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium">
                    {{ u.is_active ? 'Hoạt động' : 'Bị khóa' }}
                  </span>
                </td>
                <td class="px-4 py-3 text-sm text-gray-500">{{ formatDate(u.created_at) }}</td>
                <td class="px-4 py-3 text-right">
                  <div class="flex items-center gap-1 justify-end">
                    <!-- Upgrade to clinic_owner -->
                    <button v-if="u.role === 'patient'" @click="upgradeToClinicOwner(u)"
                      class="px-2.5 py-1 bg-purple-50 text-purple-600 rounded-lg text-xs font-medium hover:bg-purple-100 transition-colors">
                      Nâng cấp lên Chủ PK
                    </button>
                    <!-- Downgrade from clinic_owner -->
                    <button v-if="u.role === 'clinic_owner'" @click="downgradeToPatient(u)"
                      class="px-2.5 py-1 bg-yellow-50 text-yellow-600 rounded-lg text-xs font-medium hover:bg-yellow-100 transition-colors">
                      Hạ xuống Bệnh nhân
                    </button>
                    <!-- Toggle status -->
                    <button @click="toggleUserStatus(u)"
                      :class="u.is_active ? 'bg-red-50 text-red-600 hover:bg-red-100' : 'bg-green-50 text-green-600 hover:bg-green-100'"
                      class="px-2.5 py-1 rounded-lg text-xs font-medium transition-colors">
                      {{ u.is_active ? 'Khóa' : 'Kích hoạt' }}
                    </button>
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
              <button v-for="p in visiblePages" :key="p" @click="changePage(p)"
                :class="p === page ? 'bg-indigo-600 text-white border-indigo-600' : 'bg-white text-gray-700 border-gray-200 hover:bg-gray-50'" class="px-3 py-1.5 rounded-lg text-sm border transition-colors">{{ p }}</button>
              <button @click="changePage(page + 1)" :disabled="page >= totalPages" class="px-3 py-1.5 rounded-lg text-sm border border-gray-200 hover:bg-gray-50 disabled:opacity-40 transition-colors">›</button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import api from '../services/api'

const users = ref([])
const loading = ref(false)
const page = ref(1)
const pageSize = ref(20)
const total = ref(0)
const filters = ref({ role: 'patient' })

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

const roleClass = (role) => {
  const classes = {
    admin: 'bg-red-100 text-red-700',
    doctor: 'bg-blue-100 text-blue-700',
    clinic_owner: 'bg-purple-100 text-purple-700',
    patient: 'bg-green-100 text-green-700',
  }
  return classes[role] || 'bg-gray-100 text-gray-700'
}

const roleLabel = (role) => {
  const labels = {
    admin: 'Admin',
    doctor: 'Bác sĩ',
    clinic_owner: 'Chủ phòng khám',
    patient: 'Bệnh nhân',
  }
  return labels[role] || role
}

const formatDate = (dt) => {
  if (!dt) return '—'
  const d = new Date(dt)
  return d.toLocaleDateString('vi-VN', { day: '2-digit', month: '2-digit', year: 'numeric' })
}

const fetchUsers = async () => {
  loading.value = true
  try {
    const params = { page: page.value, page_size: pageSize.value }
    if (filters.value.role) params.role_filter = filters.value.role
    const response = await api.get('/users/admin/all', { params })
    users.value = response.data.users || []
    total.value = response.data.total || 0
  } catch (error) {
    console.error('Error fetching users:', error)
  } finally {
    loading.value = false
  }
}

const clearFilters = () => {
  filters.value = { role: '' }
  page.value = 1
  fetchUsers()
}

const changePage = (p) => { page.value = p; fetchUsers() }

const upgradeToClinicOwner = async (u) => {
  if (!confirm(`Nâng cấp "${u.full_name}" (${u.email}) lên Chủ phòng khám?`)) return
  try {
    await api.put(`/users/admin/${u.id}/role`, null, { params: { new_role: 'clinic_owner' } })
    await fetchUsers()
  } catch (error) {
    console.error('Error upgrading:', error)
    alert('Lỗi: ' + (error.response?.data?.detail || 'Không thể nâng cấp'))
  }
}

const downgradeToPatient = async (u) => {
  if (!confirm(`Hạ "${u.full_name}" (${u.email}) xuống Bệnh nhân? Họ sẽ mất quyền quản lý phòng khám.`)) return
  try {
    await api.put(`/users/admin/${u.id}/role`, null, { params: { new_role: 'patient' } })
    await fetchUsers()
  } catch (error) {
    console.error('Error downgrading:', error)
    alert('Lỗi: ' + (error.response?.data?.detail || 'Không thể hạ cấp'))
  }
}

const toggleUserStatus = async (u) => {
  try {
    await api.put(`/users/admin/${u.id}/status`, { is_active: !u.is_active })
    await fetchUsers()
  } catch (error) {
    console.error('Error toggling status:', error)
    alert('Lỗi: ' + (error.response?.data?.detail || 'Không thể thay đổi trạng thái'))
  }
}

onMounted(() => { fetchUsers() })
</script>
