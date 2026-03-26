<template>
  <div class="relative min-h-screen bg-gradient-login flex items-center justify-center px-4 py-12">
    <!-- Decorative circles -->
    <div class="decorative-circle w-[500px] h-[500px] bg-primary-300 -top-48 -right-48 blur-3xl"></div>
    <div class="decorative-circle w-[400px] h-[400px] bg-primary-200 bottom-0 -left-48 blur-3xl"></div>

    <div class="relative w-full max-w-md">
      <!-- Header -->
      <div class="text-center mb-8">
        <div class="w-12 h-12 bg-primary-600 rounded-2xl shadow-md flex items-center justify-center mx-auto mb-4">
          <svg class="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6v6m0 0v6m0-6h6m-6 0H6"/>
          </svg>
        </div>
        <h1 class="text-2xl font-extrabold text-gray-900 mb-1">Đăng nhập</h1>
        <p class="text-sm text-gray-500">Chào mừng bạn trở lại ClinicSearch</p>
      </div>

      <!-- Card -->
      <div class="bg-white rounded-2xl shadow-sm border border-gray-100 p-7">
        <form @submit.prevent="handleLogin" class="space-y-4">
          <!-- Email -->
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1.5">Email</label>
            <input
              v-model="form.email"
              type="email"
              name="email"
              autocomplete="email"
              required
              placeholder="nhap@email.com"
              class="input-field"
            />
          </div>

          <!-- Password -->
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1.5">Mật khẩu</label>
            <input
              v-model="form.password"
              type="password"
              name="password"
              autocomplete="current-password"
              required
              placeholder="Nhập mật khẩu"
              class="input-field"
            />
          </div>

          <!-- Error -->
          <div v-if="error" class="flex items-center gap-2 bg-red-50 border border-red-100 rounded-lg px-4 py-3">
            <svg class="w-5 h-5 text-red-500 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/>
            </svg>
            <span class="text-sm text-red-600">{{ error }}</span>
          </div>

          <!-- Submit -->
          <button
            type="submit"
            :disabled="loading"
            class="btn-primary w-full py-2.5 text-sm font-medium disabled:opacity-50 disabled:cursor-not-allowed"
          >
            <span v-if="loading" class="flex items-center justify-center gap-2">
              <svg class="w-4 h-4 animate-spin" fill="none" viewBox="0 0 24 24">
                <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z"></path>
              </svg>
              Đang đăng nhập...
            </span>
            <span v-else>Đăng nhập</span>
          </button>
        </form>

        <!-- Divider -->
        <div class="flex items-center gap-3 my-5">
          <div class="flex-1 h-px bg-gray-200"></div>
          <span class="text-xs text-gray-400 font-medium">hoặc</span>
          <div class="flex-1 h-px bg-gray-200"></div>
        </div>

        <!-- Register link -->
        <p class="text-center text-sm text-gray-500">
          Chưa có tài khoản?
          <router-link to="/register" class="text-primary-600 font-medium hover:text-primary-700 cursor-pointer">
            Đăng ký ngay
          </router-link>
        </p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'

const router = useRouter()
const authStore = useAuthStore()

const form = ref({ email: '', password: '' })
const error = ref('')
const loading = ref(false)

const handleLogin = async () => {
  error.value = ''
  loading.value = true
  try {
    await authStore.login(form.value.email, form.value.password)
    router.push('/clinics')
  } catch (e) {
    const d = e.response?.data?.detail
    if (Array.isArray(d)) {
      error.value = d.map((x) => x.msg || String(x)).join(', ')
    } else if (typeof d === 'string') {
      error.value = d
    } else {
      error.value = e.message || 'Đăng nhập thất bại. Vui lòng thử lại.'
    }
  } finally {
    loading.value = false
  }
}
</script>
