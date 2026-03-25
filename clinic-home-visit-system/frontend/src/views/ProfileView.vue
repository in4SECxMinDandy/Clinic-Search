<template>
  <div class="min-h-screen bg-gray-50">
    <nav class="bg-white shadow-sm">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="flex justify-between h-16">
          <div class="flex items-center">
            <router-link to="/" class="text-xl font-bold text-indigo-600">ClinicSearch</router-link>
          </div>
        </div>
      </div>
    </nav>

    <main class="max-w-4xl mx-auto px-4 py-8">
      <h1 class="text-3xl font-bold text-gray-900 mb-8">Hồ sơ cá nhân</h1>

      <div class="bg-white rounded-xl shadow p-6">
        <div class="space-y-4">
          <div>
            <label class="block text-sm font-medium text-gray-700">Họ và tên</label>
            <p class="mt-1 text-lg">{{ user?.full_name }}</p>
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700">Email</label>
            <p class="mt-1 text-lg">{{ user?.email }}</p>
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700">Số điện thoại</label>
            <p class="mt-1 text-lg">{{ user?.phone || 'Chưa cập nhật' }}</p>
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700">Vai trò</label>
            <p class="mt-1 text-lg capitalize">{{ user?.role }}</p>
          </div>
        </div>

        <div class="mt-6 flex gap-4">
          <button @click="logout" class="bg-red-600 text-white px-4 py-2 rounded-lg hover:bg-red-700">Đăng xuất</button>
        </div>
      </div>
    </main>
  </div>
</template>

<script setup>
import { computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'

const router = useRouter()
const authStore = useAuthStore()
const user = computed(() => authStore.user)

const logout = () => {
  authStore.logout()
  router.push('/')
}

onMounted(() => {
  authStore.fetchUser()
})
</script>
