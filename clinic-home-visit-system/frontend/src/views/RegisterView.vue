<template>
  <div class="relative min-h-screen bg-gradient-login flex items-center justify-center px-4 py-12">
    <!-- Decorative circles -->
    <div class="decorative-circle w-[500px] h-[500px] bg-primary-300 -top-48 -left-48 blur-3xl"></div>
    <div class="decorative-circle w-[400px] h-[400px] bg-primary-200 bottom-0 -right-48 blur-3xl"></div>

    <div class="relative w-full max-w-md">
      <!-- Header -->
      <div class="text-center mb-8">
        <div class="w-12 h-12 bg-primary-600 rounded-2xl shadow-md flex items-center justify-center mx-auto mb-4">
          <svg class="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6v6m0 0v6m0-6h6m-6 0H6"/>
          </svg>
        </div>
        <h1 class="text-2xl font-extrabold text-gray-900 mb-1">Tạo tài khoản</h1>
        <p class="text-sm text-gray-500">Tham gia ClinicSearch ngay hôm nay</p>
      </div>

      <!-- Card -->
      <div class="bg-white rounded-2xl shadow-sm border border-gray-100 p-7">
        <form @submit.prevent="handleRegister" class="space-y-4">
          <!-- Full Name -->
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1.5">Họ và tên</label>
            <input
              v-model="form.full_name"
              type="text"
              required
              placeholder="Nguyễn Văn A"
              class="input-field"
            />
          </div>

          <!-- Email -->
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1.5">Email</label>
            <input
              v-model="form.email"
              type="email"
              required
              placeholder="nhap@email.com"
              class="input-field"
            />
          </div>

          <!-- Phone (optional) -->
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1.5">
              Số điện thoại <span class="text-gray-400 font-normal">(tùy chọn)</span>
            </label>
            <input
              v-model="form.phone"
              type="tel"
              placeholder="0xxx xxx xxx"
              class="input-field"
            />
          </div>

          <!-- Password -->
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1.5">Mật khẩu</label>
            <input
              v-model="form.password"
              type="password"
              required
              minlength="8"
              placeholder="Tối thiểu 8 ký tự"
              class="input-field"
            />
          </div>

          <!-- Confirm Password -->
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1.5">Xác nhận mật khẩu</label>
            <input
              v-model="form.confirm_password"
              type="password"
              required
              placeholder="Nhập lại mật khẩu"
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

          <!-- Success -->
          <div v-if="success" class="flex items-center gap-2 bg-green-50 border border-green-100 rounded-lg px-4 py-3">
            <svg class="w-5 h-5 text-green-500 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"/>
            </svg>
            <span class="text-sm text-green-700">{{ success }}</span>
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
              Đang đăng ký...
            </span>
            <span v-else>Tạo tài khoản</span>
          </button>
        </form>

        <!-- Divider -->
        <div class="flex items-center gap-3 my-5">
          <div class="flex-1 h-px bg-gray-200"></div>
          <span class="text-xs text-gray-400 font-medium">hoặc</span>
          <div class="flex-1 h-px bg-gray-200"></div>
        </div>

        <!-- Login link -->
        <p class="text-center text-sm text-gray-500">
          Đã có tài khoản?
          <router-link to="/login" class="text-primary-600 font-medium hover:text-primary-700 cursor-pointer">
            Đăng nhập ngay
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

const form = ref({ full_name: '', email: '', phone: '', password: '', confirm_password: '' })
const error = ref('')
const success = ref('')
const loading = ref(false)

const handleRegister = async () => {
  error.value = ''
  success.value = ''

  if (form.value.password !== form.value.confirm_password) {
    error.value = 'Mật khẩu xác nhận không khớp'
    return
  }

  loading.value = true
  try {
    await authStore.register({
      full_name: form.value.full_name,
      email: form.value.email,
      phone: form.value.phone || undefined,
      password: form.value.password,
    })
    await router.push('/')
  } catch (e) {
    error.value = e.response?.data?.detail || 'Đăng ký thất bại. Vui lòng thử lại.'
  } finally {
    loading.value = false
  }
}
</script>
