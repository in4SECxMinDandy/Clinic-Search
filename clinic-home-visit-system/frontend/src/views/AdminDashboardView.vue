<template>
  <div class="min-h-screen bg-gray-50 flex">
    <!-- Sidebar -->
    <aside class="w-64 bg-gray-900 text-white flex flex-col min-h-screen fixed left-0 top-0">
      <div class="px-6 py-5 border-b border-gray-800">
        <div class="flex items-center gap-3">
          <div class="w-9 h-9 bg-indigo-600 rounded-lg flex items-center justify-center">
            <svg class="w-5 h-5 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z"/>
            </svg>
          </div>
          <div>
            <span class="text-lg font-bold">Admin</span>
            <p class="text-xs text-gray-400">ClinicSearch</p>
          </div>
        </div>
      </div>

      <nav class="flex-1 px-3 py-4 space-y-1">
        <router-link to="/admin" class="flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm font-medium transition-colors"
          :class="$route.path === '/admin' ? 'bg-indigo-600 text-white' : 'text-gray-400 hover:bg-gray-800 hover:text-white'">
          <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6"/>
          </svg>
          Dashboard
        </router-link>

        <router-link to="/admin/users" class="flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm font-medium transition-colors"
          :class="$route.path === '/admin/users' ? 'bg-indigo-600 text-white' : 'text-gray-400 hover:bg-gray-800 hover:text-white'">
          <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-5.197m13.5-9a2.5 2.5 0 11-5 0 2.5 2.5 0 015 0z"/>
          </svg>
          Quản lý Users
        </router-link>

        <router-link to="/admin/clinics" class="flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm font-medium transition-colors"
          :class="$route.path === '/admin/clinics' ? 'bg-indigo-600 text-white' : 'text-gray-400 hover:bg-gray-800 hover:text-white'">
          <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4"/>
          </svg>
          Phòng khám
        </router-link>

        <router-link to="/admin/doctors" class="flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm font-medium transition-colors"
          :class="$route.path === '/admin/doctors' ? 'bg-indigo-600 text-white' : 'text-gray-400 hover:bg-gray-800 hover:text-white'">
          <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"/>
          </svg>
          Bác sĩ
        </router-link>

        <router-link to="/admin/clinic-owners" class="flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm font-medium transition-colors"
          :class="$route.path === '/admin/clinic-owners' ? 'bg-indigo-600 text-white' : 'text-gray-400 hover:bg-gray-800 hover:text-white'">
          <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0z"/>
          </svg>
          Chủ phòng khám
        </router-link>
      </nav>

      <div class="px-4 py-4 border-t border-gray-800">
        <div class="flex items-center gap-3">
          <div class="w-8 h-8 bg-indigo-600 rounded-full flex items-center justify-center text-xs font-bold">
            {{ userInitials }}
          </div>
          <div class="flex-1 min-w-0">
            <p class="text-sm font-medium truncate">{{ user?.full_name || 'Admin' }}</p>
            <p class="text-xs text-gray-400 truncate">{{ user?.email }}</p>
          </div>
          <button @click="handleLogout" class="p-1.5 rounded-lg hover:bg-gray-800 text-gray-400 hover:text-red-400 transition-colors" title="Đăng xuất">
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1"/>
            </svg>
          </button>
        </div>
      </div>
    </aside>

    <!-- Main Content -->
    <main class="flex-1 ml-64 min-h-screen">
      <!-- Top Bar -->
      <header class="bg-white border-b border-gray-200 sticky top-0 z-10">
        <div class="px-8 py-4 flex items-center justify-between">
          <div>
            <h1 class="text-xl font-semibold text-gray-900">Dashboard</h1>
            <p class="text-sm text-gray-500">Quản lý đặt lịch khám bệnh</p>
          </div>
          <div class="flex items-center gap-3">
            <span class="inline-flex items-center px-2.5 py-1 rounded-full text-xs font-medium bg-indigo-100 text-indigo-700">
              <span class="w-1.5 h-1.5 rounded-full bg-indigo-500 mr-1.5"></span>
              Admin Panel
            </span>
          </div>
        </div>
      </header>

      <div class="px-8 py-6">
        <!-- Stats Cards -->
        <div class="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-4 mb-6">
          <div class="bg-white rounded-xl shadow-sm border border-gray-100 p-4">
            <p class="text-xs text-gray-500 uppercase tracking-wider font-medium">Tổng đặt lịch</p>
            <p class="text-2xl font-bold text-gray-900 mt-1">{{ stats.total }}</p>
          </div>
          <div class="bg-white rounded-xl shadow-sm border border-gray-100 p-4">
            <div class="flex items-center gap-2 mb-1">
              <div class="w-2 h-2 rounded-full bg-yellow-400"></div>
              <p class="text-xs text-gray-500 uppercase tracking-wider font-medium">Đang chờ</p>
            </div>
            <p class="text-2xl font-bold text-yellow-600">{{ stats.by_status?.pending || 0 }}</p>
          </div>
          <div class="bg-white rounded-xl shadow-sm border border-gray-100 p-4">
            <div class="flex items-center gap-2 mb-1">
              <div class="w-2 h-2 rounded-full bg-blue-400"></div>
              <p class="text-xs text-gray-500 uppercase tracking-wider font-medium">Đã xác nhận</p>
            </div>
            <p class="text-2xl font-bold text-blue-600">{{ stats.by_status?.confirmed || 0 }}</p>
          </div>
          <div class="bg-white rounded-xl shadow-sm border border-gray-100 p-4">
            <div class="flex items-center gap-2 mb-1">
              <div class="w-2 h-2 rounded-full bg-green-400"></div>
              <p class="text-xs text-gray-500 uppercase tracking-wider font-medium">Hoàn thành</p>
            </div>
            <p class="text-2xl font-bold text-green-600">{{ stats.by_status?.completed || 0 }}</p>
          </div>
          <div class="bg-white rounded-xl shadow-sm border border-gray-100 p-4">
            <div class="flex items-center gap-2 mb-1">
              <div class="w-2 h-2 rounded-full bg-purple-400"></div>
              <p class="text-xs text-gray-500 uppercase tracking-wider font-medium">Đang khám</p>
            </div>
            <p class="text-2xl font-bold text-purple-600">{{ stats.by_status?.in_progress || 0 }}</p>
          </div>
          <div class="bg-white rounded-xl shadow-sm border border-gray-100 p-4">
            <div class="flex items-center gap-2 mb-1">
              <div class="w-2 h-2 rounded-full bg-red-400"></div>
              <p class="text-xs text-gray-500 uppercase tracking-wider font-medium">Đã hủy</p>
            </div>
            <p class="text-2xl font-bold text-red-600">{{ stats.by_status?.cancelled || 0 }}</p>
          </div>
        </div>

        <!-- Filters -->
        <div class="bg-white rounded-xl shadow-sm border border-gray-100 p-4 mb-4">
          <div class="flex flex-wrap gap-3">
            <select v-model="filters.status" @change="fetchBookings" class="px-3 py-2 border border-gray-200 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-transparent">
              <option value="">Tất cả trạng thái</option>
              <option value="pending">Đang chờ</option>
              <option value="confirmed">Đã xác nhận</option>
              <option value="in_progress">Đang khám</option>
              <option value="completed">Hoàn thành</option>
              <option value="cancelled">Đã hủy</option>
              <option value="expired">Hết hạn</option>
            </select>
            <select v-model="filters.booking_type" @change="fetchBookings" class="px-3 py-2 border border-gray-200 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-transparent">
              <option value="">Tất cả loại khám</option>
              <option value="at_clinic">Khám tại phòng khám</option>
              <option value="home_visit">Khám tại nhà</option>
            </select>
            <button @click="clearFilters" class="px-3 py-2 border border-gray-200 rounded-lg text-sm text-gray-600 hover:bg-gray-50 transition-colors">
              Xóa bộ lọc
            </button>
            <span class="ml-auto flex items-center text-sm text-gray-500">
              Hiển thị {{ bookings.length }} / {{ total }} lịch hẹn
            </span>
          </div>
        </div>

        <!-- Bookings Table -->
        <div class="bg-white rounded-xl shadow-sm border border-gray-100 overflow-hidden">
          <div v-if="loading" class="text-center py-16">
            <div class="inline-block w-8 h-8 border-4 border-indigo-200 border-t-indigo-600 rounded-full animate-spin"></div>
            <p class="mt-3 text-sm text-gray-500">Đang tải dữ liệu...</p>
          </div>

          <div v-else-if="bookings.length === 0" class="text-center py-16">
            <div class="w-16 h-16 bg-gray-100 rounded-full flex items-center justify-center mx-auto mb-4">
              <svg class="w-8 h-8 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z"/>
              </svg>
            </div>
            <p class="text-gray-500">Không có lịch hẹn nào</p>
          </div>

          <div v-else class="overflow-x-auto">
            <table class="w-full">
              <thead class="bg-gray-50 border-b border-gray-100">
                <tr>
                  <th class="px-4 py-3 text-left text-xs font-semibold text-gray-500 uppercase tracking-wider">ID</th>
                  <th class="px-4 py-3 text-left text-xs font-semibold text-gray-500 uppercase tracking-wider">Thời gian</th>
                  <th class="px-4 py-3 text-left text-xs font-semibold text-gray-500 uppercase tracking-wider">Loại khám</th>
                  <th class="px-4 py-3 text-left text-xs font-semibold text-gray-500 uppercase tracking-wider">Trạng thái</th>
                  <th class="px-4 py-3 text-left text-xs font-semibold text-gray-500 uppercase tracking-wider">Bệnh nhân</th>
                  <th class="px-4 py-3 text-left text-xs font-semibold text-gray-500 uppercase tracking-wider">Phòng khám</th>
                  <th class="px-4 py-3 text-left text-xs font-semibold text-gray-500 uppercase tracking-wider">Ghi chú</th>
                  <th class="px-4 py-3 text-right text-xs font-semibold text-gray-500 uppercase tracking-wider">Hành động</th>
                </tr>
              </thead>
              <tbody class="divide-y divide-gray-50">
                <tr v-for="booking in bookings" :key="booking.id" class="hover:bg-gray-50 transition-colors">
                  <td class="px-4 py-3 text-xs text-gray-400 font-mono">{{ booking.id.slice(0, 8) }}...</td>
                  <td class="px-4 py-3">
                    <div class="text-sm font-medium text-gray-900">{{ formatDate(booking.scheduled_at) }}</div>
                    <div class="text-xs text-gray-400">{{ formatTime(booking.scheduled_at) }}</div>
                  </td>
                  <td class="px-4 py-3">
                    <span :class="booking.booking_type === 'home_visit' ? 'bg-purple-100 text-purple-700' : 'bg-blue-100 text-blue-700'"
                      class="inline-flex items-center px-2 py-0.5 rounded text-xs font-medium">
                      {{ booking.booking_type === 'home_visit' ? 'Tại nhà' : 'Tại phòng khám' }}
                    </span>
                  </td>
                  <td class="px-4 py-3">
                    <span :class="statusClass(booking.status)" class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium">
                      {{ statusLabel(booking.status) }}
                    </span>
                  </td>
                  <td class="px-4 py-3 text-sm text-gray-600">{{ booking.user_id.slice(0, 8) }}...</td>
                  <td class="px-4 py-3 text-sm text-gray-600">{{ booking.clinic_id.slice(0, 8) }}...</td>
                  <td class="px-4 py-3 text-sm text-gray-500 max-w-32 truncate">{{ booking.notes || '—' }}</td>
                  <td class="px-4 py-3 text-right">
                    <div class="flex items-center gap-1 justify-end">
                      <button v-if="booking.status === 'pending'" @click="approveBooking(booking)"
                        class="px-2.5 py-1 bg-green-50 text-green-600 rounded-lg text-xs font-medium hover:bg-green-100 transition-colors">
                        Duyệt
                      </button>
                      <button v-if="['pending', 'confirmed'].includes(booking.status)" @click="showRejectModal(booking)"
                        class="px-2.5 py-1 bg-red-50 text-red-600 rounded-lg text-xs font-medium hover:bg-red-100 transition-colors">
                        Từ chối
                      </button>
                      <button @click="showDetailModal(booking)"
                        class="px-2.5 py-1 bg-gray-100 text-gray-600 rounded-lg text-xs font-medium hover:bg-gray-200 transition-colors">
                        Chi tiết
                      </button>
                    </div>
                  </td>
                </tr>
              </tbody>
            </table>

            <!-- Pagination -->
            <div class="px-4 py-3 border-t border-gray-100 flex items-center justify-between">
              <div class="text-sm text-gray-500">
                Trang {{ page }} / {{ totalPages }}
              </div>
              <div class="flex gap-1">
                <button @click="changePage(page - 1)" :disabled="page <= 1"
                  class="px-3 py-1.5 rounded-lg text-sm border border-gray-200 hover:bg-gray-50 disabled:opacity-40 disabled:cursor-not-allowed transition-colors">
                  ‹
                </button>
                <button v-for="p in visiblePages" :key="p" @click="changePage(p)"
                  :class="p === page ? 'bg-indigo-600 text-white border-indigo-600' : 'bg-white text-gray-700 border-gray-200 hover:bg-gray-50'"
                  class="px-3 py-1.5 rounded-lg text-sm border transition-colors">
                  {{ p }}
                </button>
                <button @click="changePage(page + 1)" :disabled="page >= totalPages"
                  class="px-3 py-1.5 rounded-lg text-sm border border-gray-200 hover:bg-gray-50 disabled:opacity-40 disabled:cursor-not-allowed transition-colors">
                  ›
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </main>

    <!-- Detail Modal -->
    <div v-if="detailModal.show" class="fixed inset-0 bg-black/50 flex items-center justify-center z-50" @click.self="detailModal.show = false">
      <div class="bg-white rounded-xl shadow-xl max-w-lg w-full mx-4 overflow-hidden">
        <div class="px-6 py-4 border-b border-gray-100 flex items-center justify-between">
          <h3 class="text-lg font-semibold text-gray-900">Chi tiết lịch hẹn</h3>
          <button @click="detailModal.show = false" class="p-1 rounded-lg hover:bg-gray-100 text-gray-400 hover:text-gray-600 transition-colors">
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/>
            </svg>
          </button>
        </div>
        <div class="px-6 py-4 space-y-3 text-sm">
          <div class="grid grid-cols-2 gap-3">
            <div>
              <p class="text-gray-500 text-xs">ID Lịch hẹn</p>
              <p class="font-mono text-gray-900">{{ detailModal.booking?.id }}</p>
            </div>
            <div>
              <p class="text-gray-500 text-xs">ID Bệnh nhân</p>
              <p class="font-mono text-gray-900">{{ detailModal.booking?.user_id }}</p>
            </div>
            <div>
              <p class="text-gray-500 text-xs">ID Phòng khám</p>
              <p class="font-mono text-gray-900">{{ detailModal.booking?.clinic_id }}</p>
            </div>
            <div>
              <p class="text-gray-500 text-xs">ID Bác sĩ</p>
              <p class="font-mono text-gray-900">{{ detailModal.booking?.doctor_id || '—' }}</p>
            </div>
            <div>
              <p class="text-gray-500 text-xs">Loại khám</p>
              <p class="font-medium text-gray-900">{{ detailModal.booking?.booking_type === 'home_visit' ? 'Khám tại nhà' : 'Khám tại phòng khám' }}</p>
            </div>
            <div>
              <p class="text-gray-500 text-xs">Thời gian</p>
              <p class="font-medium text-gray-900">{{ detailModal.booking ? formatDate(detailModal.booking.scheduled_at) : '' }} {{ detailModal.booking ? formatTime(detailModal.booking.scheduled_at) : '' }}</p>
            </div>
            <div>
              <p class="text-gray-500 text-xs">Thời lượng</p>
              <p class="font-medium text-gray-900">{{ detailModal.booking?.duration_minutes }} phút</p>
            </div>
            <div>
              <p class="text-gray-500 text-xs">Trạng thái</p>
              <span :class="statusClass(detailModal.booking?.status)" class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium">
                {{ statusLabel(detailModal.booking?.status) }}
              </span>
            </div>
            <div v-if="detailModal.booking?.home_address">
              <p class="text-gray-500 text-xs">Địa chỉ nhà</p>
              <p class="font-medium text-gray-900">{{ detailModal.booking?.home_address }}</p>
            </div>
            <div v-if="detailModal.booking?.payment_method">
              <p class="text-gray-500 text-xs">Thanh toán</p>
              <p class="font-medium text-gray-900">{{ detailModal.booking?.payment_method }}</p>
            </div>
          </div>
          <div v-if="detailModal.booking?.notes">
            <p class="text-gray-500 text-xs">Ghi chú</p>
            <p class="font-medium text-gray-900">{{ detailModal.booking?.notes }}</p>
          </div>
          <div class="grid grid-cols-2 gap-3 text-xs text-gray-400 pt-2 border-t">
            <div>Tạo lúc: {{ detailModal.booking ? new Date(detailModal.booking.created_at).toLocaleString('vi-VN') : '' }}</div>
            <div>Cập nhật: {{ detailModal.booking ? new Date(detailModal.booking.updated_at).toLocaleString('vi-VN') : '' }}</div>
            <div v-if="detailModal.booking?.confirmed_at">Xác nhận: {{ new Date(detailModal.booking.confirmed_at).toLocaleString('vi-VN') }}</div>
            <div v-if="detailModal.booking?.cancelled_at">Hủy lúc: {{ new Date(detailModal.booking.cancelled_at).toLocaleString('vi-VN') }}</div>
          </div>
        </div>
        <div class="px-6 py-4 bg-gray-50 border-t border-gray-100 flex gap-2 justify-end">
          <button v-if="detailModal.booking?.status === 'pending'" @click="approveBooking(detailModal.booking); detailModal.show = false"
            class="px-4 py-2 bg-green-600 text-white rounded-lg text-sm font-medium hover:bg-green-700 transition-colors">
            Duyệt lịch hẹn
          </button>
          <button v-if="['pending', 'confirmed'].includes(detailModal.booking?.status)" @click="detailModal.show = false; showRejectModal(detailModal.booking)"
            class="px-4 py-2 bg-red-600 text-white rounded-lg text-sm font-medium hover:bg-red-700 transition-colors">
            Từ chối
          </button>
          <button @click="detailModal.show = false"
            class="px-4 py-2 bg-gray-200 text-gray-700 rounded-lg text-sm font-medium hover:bg-gray-300 transition-colors">
            Đóng
          </button>
        </div>
      </div>
    </div>

    <!-- Reject Modal -->
    <div v-if="rejectModal.show" class="fixed inset-0 bg-black/50 flex items-center justify-center z-50" @click.self="rejectModal.show = false">
      <div class="bg-white rounded-xl shadow-xl max-w-md w-full mx-4 overflow-hidden">
        <div class="px-6 py-4 border-b border-gray-100 flex items-center justify-between">
          <h3 class="text-lg font-semibold text-gray-900">Từ chối lịch hẹn</h3>
          <button @click="rejectModal.show = false" class="p-1 rounded-lg hover:bg-gray-100 text-gray-400 hover:text-gray-600 transition-colors">
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/>
            </svg>
          </button>
        </div>
        <div class="px-6 py-4">
          <p class="text-sm text-gray-600 mb-3">
            Bạn đang từ chối lịch hẹn <strong class="text-gray-900">{{ rejectModal.booking?.id?.slice(0, 8) }}</strong>.
            Hành động này sẽ đặt trạng thái thành <strong class="text-red-600">cancelled</strong>.
          </p>
          <label class="block text-sm font-medium text-gray-700 mb-1.5">Lý do từ chối (tùy chọn)</label>
          <textarea v-model="rejectModal.reason" rows="3" placeholder="Nhập lý do từ chối..."
            class="w-full px-3 py-2 border border-gray-200 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-red-500 focus:border-transparent resize-none"></textarea>
        </div>
        <div class="px-6 py-4 bg-gray-50 border-t border-gray-100 flex gap-2 justify-end">
          <button @click="rejectModal.show = false"
            class="px-4 py-2 border border-gray-200 text-gray-700 rounded-lg text-sm font-medium hover:bg-gray-200 transition-colors">
            Hủy
          </button>
          <button @click="confirmReject" :disabled="rejectModal.loading"
            class="px-4 py-2 bg-red-600 text-white rounded-lg text-sm font-medium hover:bg-red-700 transition-colors disabled:opacity-60">
            {{ rejectModal.loading ? 'Đang xử lý...' : 'Xác nhận từ chối' }}
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'
import api from '../services/api'

const router = useRouter()
const authStore = useAuthStore()

const user = computed(() => authStore.user)
const userInitials = computed(() => {
  const name = user.value?.full_name || 'A'
  return name.split(' ').map(w => w[0]).join('').toUpperCase().slice(0, 2)
})

const bookings = ref([])
const stats = ref({ by_status: {}, by_booking_type: {}, total: 0 })
const loading = ref(false)
const page = ref(1)
const pageSize = ref(20)
const total = ref(0)

const filters = ref({
  status: '',
  booking_type: '',
})

const detailModal = ref({ show: false, booking: null })
const rejectModal = ref({ show: false, booking: null, reason: '', loading: false })

const totalPages = computed(() => Math.max(1, Math.ceil(total.value / pageSize.value)))

const visiblePages = computed(() => {
  const pages = []
  const total = totalPages.value
  const current = page.value
  let start = Math.max(1, current - 2)
  let end = Math.min(total, start + 4)
  if (end - start < 4) start = Math.max(1, end - 4)
  for (let i = start; i <= end; i++) pages.push(i)
  return pages
})

const statusClass = (status) => {
  const classes = {
    pending: 'bg-yellow-100 text-yellow-700',
    confirmed: 'bg-blue-100 text-blue-700',
    in_progress: 'bg-purple-100 text-purple-700',
    completed: 'bg-green-100 text-green-700',
    cancelled: 'bg-red-100 text-red-700',
    expired: 'bg-gray-100 text-gray-500',
  }
  return classes[status] || 'bg-gray-100 text-gray-700'
}

const statusLabel = (status) => {
  const labels = {
    pending: 'Đang chờ',
    confirmed: 'Đã xác nhận',
    in_progress: 'Đang khám',
    completed: 'Hoàn thành',
    cancelled: 'Đã hủy',
    expired: 'Hết hạn',
  }
  return labels[status] || status
}

const formatDate = (dt) => {
  if (!dt) return ''
  const d = new Date(dt)
  return d.toLocaleDateString('vi-VN', { day: '2-digit', month: '2-digit', year: 'numeric' })
}

const formatTime = (dt) => {
  if (!dt) return ''
  const d = new Date(dt)
  return d.toLocaleTimeString('vi-VN', { hour: '2-digit', minute: '2-digit' })
}

const fetchStats = async () => {
  try {
    const response = await api.get('/bookings/admin/stats')
    stats.value = response.data
  } catch (error) {
    console.error('Error fetching stats:', error)
  }
}

const fetchBookings = async () => {
  loading.value = true
  try {
    const params = { page: page.value, page_size: pageSize.value }
    if (filters.value.status) params.status = filters.value.status
    if (filters.value.booking_type) params.booking_type = filters.value.booking_type
    const response = await api.get('/bookings/admin/all', { params })
    bookings.value = response.data.bookings || []
    total.value = response.data.total || 0
  } catch (error) {
    console.error('Error fetching bookings:', error)
  } finally {
    loading.value = false
  }
}

const clearFilters = () => {
  filters.value = { status: '', booking_type: '' }
  page.value = 1
  fetchBookings()
}

const changePage = (newPage) => {
  page.value = newPage
  fetchBookings()
}

const showDetailModal = (booking) => {
  detailModal.value = { show: true, booking }
}

const showRejectModal = (booking) => {
  rejectModal.value = { show: true, booking, reason: '', loading: false }
}

const approveBooking = async (booking) => {
  try {
    await api.put(`/bookings/admin/${booking.id}/status`, { status: 'confirmed' })
    await fetchStats()
    await fetchBookings()
  } catch (error) {
    console.error('Error approving booking:', error)
  }
}

const confirmReject = async () => {
  rejectModal.value.loading = true
  try {
    await api.put(`/bookings/admin/${rejectModal.value.booking.id}/status`, { status: 'cancelled' })
    rejectModal.value.show = false
    await fetchStats()
    await fetchBookings()
  } catch (error) {
    console.error('Error rejecting booking:', error)
  } finally {
    rejectModal.value.loading = false
  }
}

const handleLogout = async () => {
  await authStore.logout()
  router.push('/login')
}

onMounted(() => {
  fetchStats()
  fetchBookings()
})
</script>
