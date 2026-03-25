import { createRouter, createWebHistory } from 'vue-router'

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
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

router.beforeEach((to, from, next) => {
  const token = document.cookie.includes('access_token')
  const publicRoutes = ['Login', 'Register', 'Home', 'Clinics', 'ClinicDetail']

  if (!token && !publicRoutes.includes(to.name)) {
    next({ name: 'Login' })
  } else {
    next()
  }
})

export default router
