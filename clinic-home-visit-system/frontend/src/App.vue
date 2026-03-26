<template>
  <div id="app" class="min-h-screen bg-gray-50">
    <!-- Navbar -->
    <header class="sticky top-0 z-50 bg-white/80 backdrop-blur-sm border-b border-gray-100 shadow-sm">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="flex justify-between items-center h-16">
          <!-- Logo -->
          <router-link to="/" class="flex items-center gap-2.5 group">
            <div class="w-9 h-9 bg-primary-600 rounded-lg flex items-center justify-center shadow-sm group-hover:bg-primary-700 transition-colors duration-200">
              <svg class="w-5 h-5 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6v6m0 0v6m0-6h6m-6 0H6"/>
              </svg>
            </div>
            <span class="text-xl font-bold">
              <span class="text-gray-900">Clinic</span><span class="text-primary-600">Search</span>
            </span>
          </router-link>

          <!-- Navigation - Not logged in -->
          <nav v-if="!isLoggedIn" class="flex items-center gap-1">
            <router-link to="/clinics" class="nav-link text-sm font-medium text-gray-600 hover:text-gray-900">
              Tìm phòng khám
            </router-link>
            <router-link to="/login" class="nav-link text-sm font-medium text-gray-600 hover:text-gray-900">
              Đăng nhập
            </router-link>
            <router-link to="/register" class="btn-primary ml-2 text-sm font-medium px-4 py-2">
              Đăng ký
            </router-link>
          </nav>

          <!-- Navigation - Logged in -->
          <nav v-else class="flex items-center gap-1">
            <!-- Admin Only: Full Admin Panel -->
            <div v-if="isAdmin" class="relative" ref="adminDropdownRef">
              <button @click="adminMenuOpen = !adminMenuOpen" class="flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-sm font-medium transition-colors duration-150"
                :class="adminMenuOpen || isAdminRoute ? 'bg-indigo-50 text-indigo-700' : 'text-indigo-600 hover:bg-indigo-50'">
                <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m5.618-2.547a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z"/>
                </svg>
                Quản trị
                <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"/>
                </svg>
              </button>
              <div v-if="adminMenuOpen" class="absolute right-0 mt-1 w-56 bg-white rounded-xl shadow-lg border border-gray-100 py-1 z-50">
                <p class="px-4 py-2 text-xs text-gray-400 font-medium uppercase tracking-wider">Hệ thống</p>
                <router-link to="/admin" @click="adminMenuOpen = false"
                  class="flex items-center gap-2.5 px-4 py-2 text-sm text-gray-700 hover:bg-gray-50 transition-colors"
                  :class="$route.path === '/admin' ? 'bg-indigo-50 text-indigo-700 font-medium' : ''">
                  <svg class="w-4 h-4 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6"/></svg>
                  Dashboard
                </router-link>
                <router-link to="/admin/users" @click="adminMenuOpen = false"
                  class="flex items-center gap-2.5 px-4 py-2 text-sm text-gray-700 hover:bg-gray-50 transition-colors"
                  :class="$route.path === '/admin/users' ? 'bg-indigo-50 text-indigo-700 font-medium' : ''">
                  <svg class="w-4 h-4 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-5.197m13.5-9a2.5 2.5 0 11-5 0 2.5 2.5 0 015 0z"/></svg>
                  Người dùng
                </router-link>
                <router-link to="/admin/clinics" @click="adminMenuOpen = false"
                  class="flex items-center gap-2.5 px-4 py-2 text-sm text-gray-700 hover:bg-gray-50 transition-colors"
                  :class="$route.path === '/admin/clinics' ? 'bg-indigo-50 text-indigo-700 font-medium' : ''">
                  <svg class="w-4 h-4 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4"/></svg>
                  Phòng khám
                </router-link>
                <router-link to="/admin/doctors" @click="adminMenuOpen = false"
                  class="flex items-center gap-2.5 px-4 py-2 text-sm text-gray-700 hover:bg-gray-50 transition-colors"
                  :class="$route.path === '/admin/doctors' ? 'bg-indigo-50 text-indigo-700 font-medium' : ''">
                  <svg class="w-4 h-4 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"/></svg>
                  Bác sĩ
                </router-link>
                <router-link to="/admin/clinic-owners" @click="adminMenuOpen = false"
                  class="flex items-center gap-2.5 px-4 py-2 text-sm text-gray-700 hover:bg-gray-50 transition-colors"
                  :class="$route.path === '/admin/clinic-owners' ? 'bg-indigo-50 text-indigo-700 font-medium' : ''">
                  <svg class="w-4 h-4 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0z"/></svg>
                  Chủ phòng khám
                </router-link>
              </div>
            </div>

            <!-- Clinic Owner Only: Management Panel -->
            <div v-if="isClinicOwner && !isAdmin" class="relative" ref="ownerDropdownRef">
              <button @click="ownerMenuOpen = !ownerMenuOpen" class="flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-sm font-medium transition-colors duration-150"
                :class="ownerMenuOpen || isOwnerRoute ? 'bg-emerald-50 text-emerald-700' : 'text-emerald-600 hover:bg-emerald-50'">
                <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4"/>
                </svg>
                Quản lý phòng khám
                <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"/>
                </svg>
              </button>
              <div v-if="ownerMenuOpen" class="absolute right-0 mt-1 w-52 bg-white rounded-xl shadow-lg border border-gray-100 py-1 z-50">
                <p class="px-4 py-2 text-xs text-gray-400 font-medium uppercase tracking-wider">Clinic Owner</p>
                <router-link to="/owner/dashboard" @click="ownerMenuOpen = false"
                  class="flex items-center gap-2.5 px-4 py-2 text-sm text-gray-700 hover:bg-gray-50 transition-colors"
                  :class="$route.path === '/owner/dashboard' ? 'bg-emerald-50 text-emerald-700 font-medium' : ''">
                  <svg class="w-4 h-4 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2H6a2 2 0 01-2-2V6zM14 6a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2h-2a2 2 0 01-2-2V6zM4 16a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2H6a2 2 0 01-2-2v-2a2 2 0 012-2h2a2 2 0 012-2v-2z"/></svg>
                  Dashboard
                </router-link>
                <router-link to="/owner/clinics" @click="ownerMenuOpen = false"
                  class="flex items-center gap-2.5 px-4 py-2 text-sm text-gray-700 hover:bg-gray-50 transition-colors"
                  :class="$route.path === '/owner/clinics' ? 'bg-emerald-50 text-emerald-700 font-medium' : ''">
                  <svg class="w-4 h-4 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4"/></svg>
                  Phòng khám của tôi
                </router-link>
                <router-link to="/owner/doctors" @click="ownerMenuOpen = false"
                  class="flex items-center gap-2.5 px-4 py-2 text-sm text-gray-700 hover:bg-gray-50 transition-colors"
                  :class="$route.path === '/owner/doctors' ? 'bg-emerald-50 text-emerald-700 font-medium' : ''">
                  <svg class="w-4 h-4 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"/></svg>
                  Bác sĩ
                </router-link>
              </div>
            </div>

            <!-- Regular User only: Browse clinics -->
            <router-link v-if="!isAdmin && !isClinicOwner" to="/clinics" class="nav-link text-sm font-medium text-gray-600 hover:text-gray-900">
              Tìm phòng khám
            </router-link>

            <!-- Regular User only: Lịch hẹn link (not for admin/clinic_owner) -->
            <router-link v-if="!isAdmin && !isClinicOwner" to="/bookings" class="nav-link text-sm font-medium text-gray-600 hover:text-gray-900">
              Lịch hẹn
            </router-link>

            <div class="h-8 w-px bg-gray-200 mx-1"></div>

            <!-- User Account Dropdown -->
            <div class="relative" ref="userDropdownRef">
              <button @click="userMenuOpen = !userMenuOpen" class="flex items-center gap-2 px-3 py-1.5 rounded-lg hover:bg-gray-100 cursor-pointer transition-colors duration-150">
                <div class="w-7 h-7 rounded-full flex items-center justify-center" :class="isAdmin ? 'bg-indigo-100' : isClinicOwner ? 'bg-emerald-100' : 'bg-primary-100'">
                  <svg class="w-4 h-4" :class="isAdmin ? 'text-indigo-600' : isClinicOwner ? 'text-emerald-600' : 'text-primary-600'" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"/>
                  </svg>
                </div>
                <span class="text-sm font-medium text-gray-700">{{ user?.full_name || 'Tài khoản' }}</span>
                <span v-if="isAdmin" class="hidden md:inline text-xs px-1.5 py-0.5 rounded-full bg-indigo-100 text-indigo-700 font-medium">Admin</span>
                <span v-if="isClinicOwner" class="hidden md:inline text-xs px-1.5 py-0.5 rounded-full bg-emerald-100 text-emerald-700 font-medium">Chủ PK</span>
              </button>
              <div v-if="userMenuOpen" class="absolute right-0 mt-1 w-48 bg-white rounded-xl shadow-lg border border-gray-100 py-1 z-50">
                <div class="px-4 py-2 border-b border-gray-100">
                  <p class="text-sm font-medium text-gray-900">{{ user?.full_name || 'User' }}</p>
                  <p class="text-xs text-gray-500">{{ user?.email }}</p>
                </div>
                <router-link to="/profile" @click="userMenuOpen = false"
                  class="flex items-center gap-2.5 px-4 py-2 text-sm text-gray-700 hover:bg-gray-50 transition-colors">
                  <svg class="w-4 h-4 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z"/></svg>
                  Hồ sơ cá nhân
                </router-link>
                <button @click="handleLogout" class="w-full flex items-center gap-2.5 px-4 py-2 text-sm text-red-600 hover:bg-red-50 transition-colors">
                  <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1"/></svg>
                  Đăng xuất
                </button>
              </div>
            </div>
          </nav>
        </div>
      </div>
    </header>

    <!-- Main Content -->
    <main>
      <router-view />
    </main>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useAuthStore } from './stores/auth'

const router = useRouter()
const route = useRoute()
const authStore = useAuthStore()

const adminMenuOpen = ref(false)
const adminDropdownRef = ref(null)
const ownerMenuOpen = ref(false)
const ownerDropdownRef = ref(null)
const userMenuOpen = ref(false)
const userDropdownRef = ref(null)

const isLoggedIn = computed(() => authStore.isAuthenticated)
const user = computed(() => authStore.user)
const isAdmin = computed(() => authStore.isAdmin)
const isClinicOwner = computed(() => authStore.isClinicOwner)
const isAdminRoute = computed(() => route.path.startsWith('/admin'))
const isOwnerRoute = computed(() => route.path.startsWith('/owner'))

const handleLogout = async () => {
  userMenuOpen.value = false
  await authStore.logout()
  router.push('/')
}

const handleClickOutside = (event) => {
  if (adminDropdownRef.value && !adminDropdownRef.value.contains(event.target)) {
    adminMenuOpen.value = false
  }
  if (ownerDropdownRef.value && !ownerDropdownRef.value.contains(event.target)) {
    ownerMenuOpen.value = false
  }
  if (userDropdownRef.value && !userDropdownRef.value.contains(event.target)) {
    userMenuOpen.value = false
  }
}

onMounted(() => { document.addEventListener('click', handleClickOutside) })
onUnmounted(() => { document.removeEventListener('click', handleClickOutside) })
</script>

<style>
/* Import Inter font */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap');

* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Inter, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  background: #f9fafb;
  color: #111827;
  line-height: 1.5;
}

#app {
  min-height: 100vh;
}

a {
  color: inherit;
  text-decoration: none;
}

/* Focus visible for accessibility */
:focus-visible {
  outline: none;
  ring: 2px;
  ring-color: #818cf8;
  ring-offset: 2px;
}
</style>
