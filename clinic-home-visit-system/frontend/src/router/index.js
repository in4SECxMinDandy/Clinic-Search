import { createRouter, createWebHistory } from 'vue-router'
import { pinia } from '../pinia'
import { useAuthStore } from '../stores/auth'

const routes = [
  {
    path: '/',
    name: 'Home',
    component: () => import('../views/HomeView.vue'),
  },
  {
    path: '/login',
    name: 'Login',
    component: () => import('../views/LoginView.vue'),
  },
  {
    path: '/register',
    name: 'Register',
    component: () => import('../views/RegisterView.vue'),
  },
  {
    path: '/clinics',
    name: 'Clinics',
    component: () => import('../views/ClinicsView.vue'),
  },
  {
    path: '/clinics/:id',
    name: 'ClinicDetail',
    component: () => import('../views/ClinicDetailView.vue'),
  },
  {
    path: '/bookings',
    name: 'Bookings',
    component: () => import('../views/BookingsView.vue'),
  },
  {
    path: '/profile',
    name: 'Profile',
    component: () => import('../views/ProfileView.vue'),
  },
  {
    path: '/admin',
    name: 'AdminDashboard',
    component: () => import('../views/AdminDashboardView.vue'),
    meta: { requiresAdmin: true },
  },
  {
    path: '/admin/users',
    name: 'AdminUsers',
    component: () => import('../views/AdminUsersView.vue'),
    meta: { requiresAdmin: true },
  },
  {
    path: '/admin/clinics',
    name: 'AdminClinics',
    component: () => import('../views/AdminClinicsView.vue'),
    meta: { requiresClinicOwnerOrAdmin: true },
  },
  {
    path: '/admin/doctors',
    name: 'AdminDoctors',
    component: () => import('../views/AdminDoctorsView.vue'),
    meta: { requiresClinicOwnerOrAdmin: true },
  },
  {
    path: '/admin/clinic-owners',
    name: 'AdminClinicOwners',
    component: () => import('../views/AdminClinicOwnersView.vue'),
    meta: { requiresAdmin: true },
  },
  {
    path: '/owner/dashboard',
    name: 'OwnerDashboard',
    component: () => import('../views/OwnerDashboardView.vue'),
    meta: { requiresClinicOwner: true },
  },
  {
    path: '/owner/clinics',
    name: 'OwnerClinics',
    component: () => import('../views/OwnerClinicsView.vue'),
    meta: { requiresClinicOwner: true },
  },
  {
    path: '/owner/doctors',
    name: 'OwnerDoctors',
    component: () => import('../views/OwnerDoctorsView.vue'),
    meta: { requiresClinicOwner: true },
  },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

router.beforeEach((to, from, next) => {
  const auth = useAuthStore(pinia)
  const hasToken =
    !!auth.token || !!sessionStorage.getItem('access_token')
  const publicRoutes = ['Login', 'Register', 'Home', 'Clinics', 'ClinicDetail']

  if (!hasToken && !publicRoutes.includes(to.name)) {
    // Save return URL for post-login redirect
    sessionStorage.setItem('returnUrl', to.fullPath)
    next({ name: 'Login' })
  } else if (hasToken && to.name === 'Login') {
    // If already logged in, redirect to returnUrl or default
    const returnUrl = sessionStorage.getItem('returnUrl')
    sessionStorage.removeItem('returnUrl')
    next(returnUrl || '/clinics')
  } else if (to.meta.requiresAdmin && !auth.isAdmin) {
    next({ name: 'Home' })
  } else if (to.meta.requiresClinicOwner && !auth.isClinicOwner) {
    next({ name: 'Home' })
  } else if (to.meta.requiresClinicOwnerOrAdmin && !auth.isAdmin && !auth.isClinicOwner) {
    next({ name: 'Home' })
  } else {
    next()
  }
})

export default router
