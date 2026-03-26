<template>
  <router-link
    :to="`/clinics/${clinic.id}`"
    class="clinic-card flex group"
  >
    <!-- Specialty Accent Bar -->
    <div
      :class="[
        'w-1.5 rounded-l-2xl flex-shrink-0',
        specialtyConfig.accentColor
      ]"
    ></div>

    <!-- Card Content -->
    <div class="flex-1 p-5 flex items-center gap-4">
      <!-- Icon -->
      <div
        :class="[
          'w-12 h-12 rounded-xl flex items-center justify-center flex-shrink-0',
          specialtyConfig.iconBg
        ]"
      >
        <svg class="w-6 h-6" :class="specialtyConfig.iconColor" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4"/>
        </svg>
      </div>

      <!-- Info -->
      <div class="flex-1 min-w-0">
        <!-- Name -->
        <h3
          class="text-base font-bold text-gray-900 group-hover:text-primary-600 transition-colors duration-150 truncate"
        >
          {{ clinic.name }}
        </h3>

        <!-- Address -->
        <p class="text-xs text-gray-400 truncate mt-0.5">
          {{ clinic.address }}{{ clinic.city ? ', ' + clinic.city : '' }}
        </p>

        <!-- Badges -->
        <div class="flex flex-wrap items-center gap-2 mt-2.5">
          <!-- Specialty Badge -->
          <span
            :class="[
              'badge',
              specialtyConfig.badgeClass
            ]"
          >
            {{ specialtyConfig.label }}
          </span>

          <!-- Home Visit Badge -->
          <span
            v-if="clinic.home_visit || clinic.supports_home_visit"
            class="badge bg-emerald-50 text-emerald-700"
          >
            Khám tại nhà
          </span>
        </div>

        <!-- Rating & Distance -->
        <div class="flex items-center gap-4 mt-2.5">
          <!-- Rating -->
          <div
            v-if="clinic.rating"
            class="flex items-center gap-1 bg-amber-50 px-2 py-1 rounded-lg"
          >
            <svg class="w-3.5 h-3.5 text-amber-400 fill-current" viewBox="0 0 20 20">
              <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z"/>
            </svg>
            <span class="text-xs font-medium text-amber-700">{{ clinic.rating.toFixed(1) }}</span>
          </div>

          <!-- Distance -->
          <span
            v-if="clinic.distance_km"
            class="text-xs text-gray-400"
          >
            {{ clinic.distance_km }} km
          </span>
        </div>
      </div>

      <!-- Arrow -->
      <div class="flex-shrink-0">
        <svg
          class="w-5 h-5 text-gray-300 group-hover:text-primary-400 transition-colors duration-150"
          fill="none"
          stroke="currentColor"
          viewBox="0 0 24 24"
        >
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"/>
        </svg>
      </div>
    </div>
  </router-link>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  clinic: {
    type: Object,
    required: true,
  },
})

// Specialty configuration map
const specialtyConfig = computed(() => {
  const specialtyMap = {
    general: {
      label: 'Đa khoa',
      accentColor: 'bg-blue-500',
      iconBg: 'bg-blue-50',
      iconColor: 'text-blue-500',
      badgeClass: 'bg-blue-50 text-blue-700',
    },
    dentistry: {
      label: 'Nha khoa',
      accentColor: 'bg-violet-500',
      iconBg: 'bg-violet-50',
      iconColor: 'text-violet-500',
      badgeClass: 'bg-violet-50 text-violet-700',
    },
    pediatrics: {
      label: 'Nhi khoa',
      accentColor: 'bg-pink-400',
      iconBg: 'bg-pink-50',
      iconColor: 'text-pink-500',
      badgeClass: 'bg-pink-50 text-pink-700',
    },
    cardiology: {
      label: 'Tim mạch',
      accentColor: 'bg-red-500',
      iconBg: 'bg-red-50',
      iconColor: 'text-red-500',
      badgeClass: 'bg-red-50 text-red-700',
    },
    dermatology: {
      label: 'Da liễu',
      accentColor: 'bg-orange-400',
      iconBg: 'bg-orange-50',
      iconColor: 'text-orange-500',
      badgeClass: 'bg-orange-50 text-orange-700',
    },
    orthopedics: {
      label: 'Chỉnh hình',
      accentColor: 'bg-teal-500',
      iconBg: 'bg-teal-50',
      iconColor: 'text-teal-500',
      badgeClass: 'bg-teal-50 text-teal-700',
    },
  }

  // Check clinic.specialty (can be string or array)
  const clinicSpecialty = props.clinic.specialty

  if (Array.isArray(clinicSpecialty)) {
    // Use first specialty for coloring
    const firstSpecialty = clinicSpecialty[0]?.toLowerCase() || 'general'
    return specialtyMap[firstSpecialty] || specialtyMap.general
  }

  if (typeof clinicSpecialty === 'string') {
    const normalized = clinicSpecialty.toLowerCase()
    return specialtyMap[normalized] || specialtyMap.general
  }

  return specialtyMap.general
})
</script>
