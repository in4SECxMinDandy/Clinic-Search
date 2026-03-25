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

    <main class="max-w-7xl mx-auto px-4 py-8 sm:px-6 lg:px-8">
      <h1 class="text-3xl font-bold text-gray-900 mb-8">Tìm phòng khám</h1>

      <div class="grid grid-cols-1 lg:grid-cols-3 gap-8">
        <div class="lg:col-span-1">
          <div class="bg-white rounded-xl shadow p-6">
            <h3 class="text-lg font-semibold mb-4">Bộ lọc</h3>

            <div class="space-y-4">
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-1">Tìm kiếm</label>
                <input v-model="filters.search" type="text" placeholder="Tên phòng khám..." class="w-full px-3 py-2 border rounded-lg" />
              </div>

              <div>
                <label class="block text-sm font-medium text-gray-700 mb-1">Bán kính (km)</label>
                <input v-model.number="filters.radius_km" type="number" min="1" max="50" class="w-full px-3 py-2 border rounded-lg" />
              </div>

              <div>
                <label class="block text-sm font-medium text-gray-700 mb-1">Chuyên khoa</label>
                <select v-model="filters.specialty" class="w-full px-3 py-2 border rounded-lg">
                  <option value="">Tất cả</option>
                  <option v-for="s in specialties" :key="s" :value="s">{{ s }}</option>
                </select>
              </div>

              <div class="flex items-center">
                <input v-model="filters.supports_home_visit" type="checkbox" id="home_visit" class="mr-2" />
                <label for="home_visit" class="text-sm text-gray-700">Hỗ trợ khám tại nhà</label>
              </div>

              <button @click="applyFilters" class="w-full bg-indigo-600 text-white py-2 rounded-lg hover:bg-indigo-700">
                Áp dụng
              </button>
            </div>
          </div>
        </div>

        <div class="lg:col-span-2">
          <div v-if="loading" class="text-center py-8">Đang tải...</div>

          <div v-else-if="clinics.length === 0" class="text-center py-8 text-gray-500">
            Không tìm thấy phòng khám nào
          </div>

          <div v-else class="space-y-4">
            <ClinicCard v-for="clinic in clinics" :key="clinic.id" :clinic="clinic" />
          </div>
        </div>
      </div>
    </main>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { useClinicStore } from '../stores/clinic'
import ClinicCard from '../components/ClinicCard.vue'

const clinicStore = useClinicStore()
const route = useRoute()

const filters = ref({
  search: route.query.search || '',
  radius_km: 10,
  specialty: '',
  supports_home_visit: false,
})

const specialties = ['Nội khoa', 'Ngoại khoa', 'Tim mạch', 'Da liễu', 'Nhi khoa', 'Sản phụ khoa']
const clinics = ref([])
const loading = ref(false)

const applyFilters = async () => {
  loading.value = true
  try {
    await clinicStore.fetchClinics(filters.value)
    clinics.value = clinicStore.clinics
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  applyFilters()
})
</script>
