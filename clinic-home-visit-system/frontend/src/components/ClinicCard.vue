<template>
  <div class="bg-white rounded-lg shadow-md p-6 hover:shadow-lg transition-shadow">
    <div class="flex justify-between items-start">
      <div class="flex-1">
        <h3 class="text-lg font-semibold text-gray-900">{{ clinic.name }}</h3>
        <p class="text-sm text-gray-500 mt-1">{{ clinic.address }}</p>

        <div class="flex flex-wrap gap-2 mt-3">
          <span v-for="s in clinic.specialties" :key="s" class="bg-indigo-100 text-indigo-700 text-xs px-2 py-1 rounded-full">
            {{ s }}
          </span>
        </div>

        <div class="flex items-center gap-4 mt-4 text-sm">
          <span v-if="clinic.distance_km" class="text-gray-600">
            <span class="font-medium">{{ clinic.distance_km }}</span> km
          </span>
          <span v-if="clinic.estimated_travel_time_min" class="text-gray-600">
            ~{{ clinic.estimated_travel_time_min }} phút
          </span>
          <span v-if="clinic.supports_home_visit" class="text-green-600 font-medium">
            Khám tại nhà
          </span>
        </div>
      </div>

      <router-link :to="`/clinics/${clinic.id}`" class="ml-4 bg-indigo-600 text-white px-4 py-2 rounded-lg hover:bg-indigo-700 text-sm">
        Chi tiết
      </router-link>
    </div>
  </div>
</template>

<script setup>
defineProps({
  clinic: {
    type: Object,
    required: true,
  },
})
</script>
