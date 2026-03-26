<template>
  <div class="min-h-screen bg-gray-50 flex">
    <!-- Sidebar -->
    <aside class="w-64 bg-gray-900 text-white flex flex-col min-h-screen fixed left-0 top-0">
      <div class="px-6 py-5 border-b border-gray-800">
        <div class="flex items-center gap-3">
          <div class="w-9 h-9 bg-indigo-600 rounded-lg flex items-center justify-center">
            <svg class="w-5 h-5 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z"/>
            </svg>
          </div>
          <div>
            <span class="text-lg font-bold">Admin</span>
            <p class="text-xs text-gray-400">ClinicSearch</p>
          </div>
        </div>
      </div>

      <nav class="flex-1 px-3 py-4 space-y-1">
        <router-link to="/admin" class="flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm font-medium transition-colors"
          :class="$route.path === '/admin' ? 'bg-indigo-600 text-white' : 'text-gray-400 hover:bg-gray-800 hover:text-white'">
          <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6"/>
          </svg>
          Dashboard
        </router-link>

        <router-link to="/admin/users" class="flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm font-medium transition-colors"
          :class="$route.path === '/admin/users' ? 'bg-indigo-600 text-white' : 'text-gray-400 hover:bg-gray-800 hover:text-white'">
          <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-5.197m13.5-9a2.5 2.5 0 11-5 0 2.5 2.5 0 015 0z"/>
          </svg>
          Quản lý Users
        </router-link>
      </nav>

      <div class="px-4 py-4 border-t border-gray-800">
        <div class="flex items-center gap-3">
          <div class="w-8 h-8 bg-indigo-600 rounded-full flex items-center justify-center text-xs font-bold">
            {{ userInitials }}
          </div>
          <div class="flex-1 min-w-0">
            <p class="text-sm font-medium truncate">{{ user?.full_name || 'Admin' }}</p>
            <p class="text-xs text-gray-400 truncate">{{ user?.email }}</p>
          </div>
          <button @click="handleLogout" class="p-1.5 rounded-lg hover:bg-gray-800 text-gray-400 hover:text-red-400 transition-colors" title="Đăng xuất">
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1"/>
            </svg>
          </button>
        </div>
      </div>
    </aside>

    <!-- Main Content -->
    <main class="flex-1 ml-64 min-h-screen">
      <header class="bg-white border-b border-gray-200 sticky top-0 z-10">
        <div class="px-8 py-4 flex items-center justify-between">
          <div>
            <h1 class="text-xl font-semibold text-gray-900">Quản lý Users</h1>
            <p class="text-sm text-gray-500">Danh sách và quản lý tài khoản người dùng</p>
          </div>
          <div class="flex items-center gap-3">
            <span class="inline-flex items-center px-2.5 py-1 rounded-full text-xs font-medium bg-indigo-100 text-indigo-700">
              <span class="w-1.5 h-1.5 rounded-full bg-indigo-500 mr-1.5"></span>
              Admin Panel
            </span>
          </div>
        </div>
      </header>

      <div class="px-8 py-6">
        <!-- Filters -->
        <div class="bg-white rounded-xl shadow-sm border border-gray-100 p-4 mb-4">
          <div class="flex flex-wrap gap-3">
            <select v-model="filters.role" @change="fetchUsers" class="px-3 py-2 border border-gray-200 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-transparent">
              <option value="">Tất cả vai trò</option>
              <option value="patient">Bệnh nhân</option>
              <option value="doctor">Bác sĩ</option>
              <option value="clinic_owner">Chủ phòng khám</option>
              <option value="admin">Admin</option>
            </select>
            <button @click="clearFilters" class="px-3 py-2 border border-gray-200 rounded-lg text-sm text-gray-600 hover:bg-gray-50 transition-colors">
              Xóa bộ lọc
            </button>
            <span class="ml-auto flex items-center text-sm text-gray-500">
              Hiển thị {{ users.length }} / {{ total }} người dùng
            </span>
          </div>
        </div>

        <!-- Users Table -->
        <div class="bg-white rounded-xl shadow-sm border border-gray-100 overflow-hidden">
          <div v-if="loading" class="text-center py-16">
            <div class="inline-block w-8 h-8 border-4 border-indigo-200 border-t-indigo-600 rounded-full animate-spin"></div>
            <p class="mt-3 text-sm text-gray-500">Đang tải dữ liệu...</p>
          </div>

          <div v-else-if="users.length === 0" class="text-center py-16">
            <div class="w-16 h-16 bg-gray-100 rounded-full flex items-center justify-center mx-auto mb-4">
              <svg class="w-8 h-8 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z"/>
              </svg>
            </div>
            <p class="text-gray-500">Không có người dùng nào</p>
          </div>

          <div v-else class="overflow-x-auto">
            <table class="w-full">
              <thead class="bg-gray-50 border-b border-gray-100">
                <tr>
                  <th class="px-4 py-3 text-left text-xs font-semibold text-gray-500 uppercase tracking-wider">Người dùng</th>
                  <th class="px-4 py-3 text-left text-xs font-semibold text-gray-500 uppercase tracking-wider">Email</th>
                  <th class="px-4 py-3 text-left text-xs font-semibold text-gray-500 uppercase tracking-wider">Số điện thoại</th>
                  <th class="px-4 py-3 text-left text-xs font-semibold text-gray-500 uppercase tracking-wider">Vai trò</th>
                  <th class="px-4 py-3 text-left text-xs font-semibold text-gray-500 uppercase tracking-wider">Trạng thái</th>
                  <th class="px-4 py-3 text-left text-xs font-semibold text-gray-500 uppercase tracking-wider">Ngày tạo</th>
                  <th class="px-4 py-3 text-right text-xs font-semibold text-gray-500 uppercase tracking-wider">Hành động</th>
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
                      <button @click="showRoleModal(u)"
                        class="px-2.5 py-1 bg-indigo-50 text-indigo-600 rounded-lg text-xs font-medium hover:bg-indigo-100 transition-colors">
                        Đổi vai trò
                      </button>
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
              <div class="text-sm text-gray-500">
                Trang {{ page }} / {{ totalPages }}
              </div>
              <div class="flex gap-1">
                <button @click="changePage(page - 1)" :disabled="page <= 1"
                  class="px-3 py-1.5 rounded-lg text-sm border border-gray-200 hover:bg-gray-50 disabled:opacity-40 disabled:cursor-not-allowed transition-colors">
                  ‹
                </button>
                <button v-for="p in visiblePages" :key="p" @click="changePage(p)"
                  :class="p === page ? 'bg-indigo-600 text-white border-indigo-600' : 'bg-white text-gray-700 border-gray-200 hover:bg-gray-50'"
                  class="px-3 py-1.5 rounded-lg text-sm border transition-colors">
                  {{ p }}
                </button>
                <button @click="changePage(page + 1)" :disabled="page >= totalPages"
                  class="px-3 py-1.5 rounded-lg text-sm border border-gray-200 hover:bg-gray-50 disabled:opacity-40 disabled:cursor-not-allowed transition-colors">
                  ›
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </main>

    <!-- Role Change Modal -->
    <div v-if="roleModal.show" class="fixed inset-0 bg-black/50 flex items-center justify-center z-50" @click.self="roleModal.show = false">
      <div class="bg-white rounded-xl shadow-xl max-w-md w-full mx-4 overflow-hidden">
        <div class="px-6 py-4 border-b border-gray-100 flex items-center justify-between">
          <h3 class="text-lg font-semibold text-gray-900">Đổi vai trò</h3>
          <button @click="roleModal.show = false" class="p-1 rounded-lg hover:bg-gray-100 text-gray-400 hover:text-gray-600 transition-colors">
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/>
            </svg>
          </button>
        </div>
        <div class="px-6 py-4">
          <p class="text-sm text-gray-600 mb-1">Người dùng: <strong class="text-gray-900">{{ roleModal.user?.full_name }}</strong></p>
          <p class="text-sm text-gray-500 mb-4">Email: {{ roleModal.user?.email }}</p>
          <label class="block text-sm font-medium text-gray-700 mb-2">Chọn vai trò mới</label>
          <div class="space-y-2">
            <label v-for="r in availableRoles" :key="r.value" class="flex items-center gap-3 p-3 border rounded-lg cursor-pointer transition-colors"
              :class="roleModal.newRole === r.value ? 'border-indigo-500 bg-indigo-50' : 'border-gray-200 hover:bg-gray-50'">
              <input type="radio" :value="r.value" v-model="roleModal.newRole" class="text-indigo-600 focus:ring-indigo-500">
              <div>
                <p class="text-sm font-medium text-gray-900">{{ r.label }}</p>
                <p class="text-xs text-gray-500">{{ r.description }}</p>
              </div>
            </label>
          </div>
        </div>
        <div class="px-6 py-4 bg-gray-50 border-t border-gray-100 flex gap-2 justify-end">
          <button @click="roleModal.show = false"
            class="px-4 py-2 border border-gray-200 text-gray-700 rounded-lg text-sm font-medium hover:bg-gray-200 transition-colors">
            Hủy
          </button>
          <button @click="confirmRoleChange" :disabled="roleModal.loading || roleModal.newRole === roleModal.user?.role"
            class="px-4 py-2 bg-indigo-600 text-white rounded-lg text-sm font-medium hover:bg-indigo-700 transition-colors disabled:opacity-60">
            {{ roleModal.loading ? 'Đang xử lý...' : 'Xác nhận' }}
          </button>
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
  const name = user.value?.full_name || 'A'
  return name.split(' ').map(w => w[0]).join('').toUpperCase().slice(0, 2)
})

const users = ref([])
const loading = ref(false)
const page = ref(1)
const pageSize = ref(20)
const total = ref(0)
const filters = ref({ role: '' })

const roleModal = ref({ show: false, user: null, newRole: '', loading: false })

const availableRoles = [
  { value: 'patient', label: 'Bệnh nhân', description: 'Người dùng thông thường, đặt lịch khám' },
  { value: 'doctor', label: 'Bác sĩ', description: 'Nhân viên y tế, khám bệnh cho bệnh nhân' },
  { value: 'clinic_owner', label: 'Chủ phòng khám', description: 'Quản lý phòng khám và bác sĩ' },
  { value: 'admin', label: 'Admin', description: 'Toàn quyền quản trị hệ thống' },
]

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

const changePage = (newPage) => {
  page.value = newPage
  fetchUsers()
}

const showRoleModal = (u) => {
  roleModal.value = { show: true, user: u, newRole: u.role, loading: false }
}

const confirmRoleChange = async () => {
  roleModal.value.loading = true
  try {
    await api.put(`/users/admin/${roleModal.value.user.id}/role`, null, {
      params: { new_role: roleModal.value.newRole },
    })
    roleModal.value.show = false
    await fetchUsers()
  } catch (error) {
    console.error('Error changing role:', error)
  } finally {
    roleModal.value.loading = false
  }
}

const toggleUserStatus = async (u) => {
  try {
    await api.put(`/users/admin/${u.id}/status`, { is_active: !u.is_active })
    await fetchUsers()
  } catch (error) {
    console.error('Error toggling user status:', error)
  }
}

const handleLogout = async () => {
  await authStore.logout()
  router.push('/login')
}

onMounted(() => {
  fetchUsers()
})
</script>
