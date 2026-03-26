import { defineStore } from 'pinia'
import api from '../services/api'

export const useClinicStore = defineStore('clinic', {
  state: () => ({
    clinics: [],
    currentClinic: null,
    total: 0,
    loading: false,
    filters: {
      lat: null,
      lng: null,
      radius_km: 10,
      specialty: null,
      supports_home_visit: null,
      sort_by: 'distance',
    },
    locationSource: null,
  }),

  actions: {
    async fetchClinics(params = {}) {
      this.loading = true
      try {
        const response = await api.get('/clinics', { params: { ...this.filters, ...params } })
        this.clinics = response.data.clinics
        this.total = response.data.total
      } finally {
        this.loading = false
      }
    },

    async fetchClinic(id) {
      this.loading = true
      try {
        const response = await api.get(`/clinics/${id}`, { params: { lat: this.filters.lat, lng: this.filters.lng } })
        this.currentClinic = response.data
        return response.data
      } finally {
        this.loading = false
      }
    },

    setUserLocation(lat, lng, source = null) {
      this.filters.lat = lat
      this.filters.lng = lng
      if (source) {
        this.locationSource = source
      }
    },

    updateFilters(filters) {
      this.filters = { ...this.filters, ...filters }
    },
  },
})
