<script setup>
import { ref, computed, watch, onMounted, onUnmounted, provide } from 'vue'
import { useRoute, useRouter } from 'vue-router'

const route = useRoute()
const router = useRouter()

// === Sidebar state ===
const sidebarCollapsed = ref(false)
const mobileSidebarOpen = ref(false)
const isMobile = ref(window.innerWidth < 768)

const toggleSidebar = () => {
  if (isMobile.value) {
    mobileSidebarOpen.value = !mobileSidebarOpen.value
  } else {
    sidebarCollapsed.value = !sidebarCollapsed.value
  }
}

const handleResize = () => {
  isMobile.value = window.innerWidth < 768
  if (!isMobile.value) {
    mobileSidebarOpen.value = false
  }
}

onMounted(() => window.addEventListener('resize', handleResize))
onUnmounted(() => window.removeEventListener('resize', handleResize))

// === Navigation items ===
const navItems = [
  { icon: 'bi-house-door', label: 'Dashboard', to: '/' },
  { icon: 'bi-people', label: 'Empleados', to: '/empleados' },
  { icon: 'bi-clock-history', label: 'Asistencia', to: '/asistencia' },
  { icon: 'bi-cash-stack', label: 'Nómina', to: '/nomina' },
  { icon: 'bi-file-earmark-bar-graph', label: 'Reportes', to: '/reportes' },
  { icon: 'bi-gear', label: 'Configuración', to: '/configuracion' }
]

// === User state ===
const getInitials = (name) => {
  if (!name) return '?'
  return name.split(' ').map(w => w[0]).join('').toUpperCase().slice(0, 2)
}

const user = ref({
  name: localStorage.getItem('userName') || 'Administrador',
  role: localStorage.getItem('userRole') || 'ADMIN_RRHH',
  email: localStorage.getItem('userEmail') || 'admin@empresa.com',
  initials: getInitials(localStorage.getItem('userName')) || 'AD'
})

const userDropdownOpen = ref(false)

const logout = () => {
  localStorage.removeItem('token')
  localStorage.removeItem('userRole')
  localStorage.removeItem('userName')
  localStorage.removeItem('userEmail')
  localStorage.removeItem('userId')
  router.push('/login')
}

const handleClickOutside = (e) => {
  if (!e.target.closest('.user-dropdown')) {
    userDropdownOpen.value = false
  }
}

onMounted(() => document.addEventListener('click', handleClickOutside))
onUnmounted(() => document.removeEventListener('click', handleClickOutside))

// === Toast system ===
const toasts = ref([])
let toastId = 0

const addToast = (title, message, type = 'info', duration = 5000) => {
  const id = ++toastId
  toasts.value.push({ id, title, message, type })
  setTimeout(() => removeToast(id), duration)
}

const removeToast = (id) => {
  const toast = toasts.value.find(t => t.id === id)
  if (toast) toast.exiting = true
  setTimeout(() => {
    toasts.value = toasts.value.filter(t => t.id !== id)
  }, 300)
}

provide('addToast', addToast)

// Monitor for user changes
watch(() => route.path, () => {
  const name = localStorage.getItem('userName')
  user.value = {
    name: name || 'Administrador',
    role: localStorage.getItem('userRole') || 'ADMIN_RRHH',
    email: localStorage.getItem('userEmail') || '',
    initials: getInitials(name) || 'AD'
  }
})

// === Computed ===
const isAuthPage = computed(() => {
  return route.path === '/login' || route.path === '/reset-password'
})

const pageTitle = computed(() => {
  const item = navItems.find(n => route.path.startsWith(n.to) && n.to !== '/')
  if (route.path === '/') return 'Dashboard'
  if (route.path.includes('/nuevo')) return 'Nuevo Empleado'
  if (route.path.includes('/editar')) return 'Editar Empleado'
  if (route.path.includes('/filtros')) return 'Reportes Filtrables'
  return item ? item.label : ''
})

const roleBadgeClass = computed(() => {
  const roles = {
    'ADMIN_RRHH': 'badge-solid-primary',
    'EMPLEADO': 'badge-solid-success',
    'CONTADOR': 'badge-solid-success',
    'GERENTE': 'badge-solid-primary',
    'ADMIN_SISTEMA': 'badge-neutral'
  }
  return roles[user.value.role] || 'badge-neutral'
})
</script>

<template>
  <div class="app-shell">
    <!-- Auth pages (login, reset password) - no layout -->
    <template v-if="isAuthPage">
      <router-view v-slot="{ Component }">
        <Transition name="auth-page" mode="out-in">
          <component :is="Component" />
        </Transition>
      </router-view>
    </template>

    <!-- Main app layout -->
    <template v-else>
      <!-- Overlay for mobile sidebar -->
      <Transition name="fade">
        <div
          v-if="mobileSidebarOpen"
          class="sidebar-overlay"
          @click="mobileSidebarOpen = false"
        />
      </Transition>

      <!-- Sidebar -->
      <aside
        class="sidebar"
        :class="{
          'sidebar-collapsed': !isMobile && sidebarCollapsed,
          'sidebar-mobile-open': isMobile && mobileSidebarOpen
        }"
      >
        <div class="sidebar-brand">
          <div class="brand-icon">
            <i class="bi bi-building"></i>
          </div>
          <Transition name="fade" mode="out-in">
            <span v-if="!sidebarCollapsed || isMobile" class="brand-text" key="text">
              SoftVar
            </span>
          </Transition>
        </div>

        <nav class="sidebar-nav">
          <ul class="nav-list">
            <li v-for="item in navItems" :key="item.to" class="nav-item">
              <router-link
                :to="item.to"
                class="nav-link"
                :class="{ active: route.path === item.to || (item.to !== '/' && route.path.startsWith(item.to)) }"
                @click="isMobile && (mobileSidebarOpen = false)"
              >
                <i :class="`bi ${item.icon}`" class="nav-icon"></i>
                <Transition name="fade" mode="out-in">
                  <span v-if="!sidebarCollapsed || isMobile" class="nav-label" key="label">
                    {{ item.label }}
                  </span>
                </Transition>
              </router-link>
            </li>
          </ul>
        </nav>

        <div class="sidebar-footer">
          <Transition name="fade" mode="out-in">
            <div v-if="!sidebarCollapsed || isMobile" class="sidebar-user" key="user">
              <div class="avatar avatar-sm avatar-placeholder">
                {{ user.initials }}
              </div>
              <div class="sidebar-user-info">
                <div class="sidebar-user-name">{{ user.name }}</div>
                <div class="sidebar-user-role">{{ user.role }}</div>
              </div>
            </div>
            <div v-else key="avatar-only" class="sidebar-user-compact">
              <div class="avatar avatar-sm avatar-placeholder" data-tooltip="Cerrar sesión" @click="logout">
                {{ user.initials }}
              </div>
            </div>
          </Transition>
        </div>
      </aside>

      <!-- Main content area -->
      <div class="main-wrapper" :class="{ 'main-expanded': !isMobile && sidebarCollapsed }">
        <!-- Header -->
        <header class="app-header">
          <div class="header-left">
            <button class="btn btn-icon btn-ghost header-toggle" @click="toggleSidebar">
              <i :class="sidebarCollapsed ? 'bi bi-chevron-right' : 'bi bi-chevron-left'" class="toggle-icon"></i>
            </button>
            <div class="header-title">
              <h2>{{ pageTitle }}</h2>
            </div>
          </div>

          <div class="header-right">
            <!-- Notification bell -->
            <button class="btn btn-icon btn-ghost header-icon-btn" data-tooltip="Notificaciones">
              <i class="bi bi-bell"></i>
              <span class="notification-dot"></span>
            </button>

            <!-- User dropdown -->
            <div class="user-dropdown">
              <button class="user-dropdown-trigger" @click.stop="userDropdownOpen = !userDropdownOpen">
                <div class="avatar avatar-sm avatar-placeholder">{{ user.initials }}</div>
                <div class="user-dropdown-info">
                  <span class="user-dropdown-name">{{ user.name }}</span>
                  <span :class="['badge', roleBadgeClass]">{{ user.role }}</span>
                </div>
                <i class="bi bi-chevron-down dropdown-arrow" :class="{ open: userDropdownOpen }"></i>
              </button>

              <Transition name="dropdown">
                <div v-if="userDropdownOpen" class="dropdown-menu">
                  <div class="dropdown-header">
                    <p class="dropdown-user-name">{{ user.name }}</p>
                    <p class="dropdown-user-email">{{ user.email }}</p>
                  </div>
                  <div class="divider"></div>
                  <button class="dropdown-item" @click="logout">
                    <i class="bi bi-box-arrow-right"></i>
                    Cerrar Sesión
                  </button>
                </div>
              </Transition>
            </div>
          </div>
        </header>

        <!-- Main content -->
        <main class="main-content">
          <router-view v-slot="{ Component }">
            <Transition name="page" mode="out-in">
              <component :is="Component" />
            </Transition>
          </router-view>
        </main>
      </div>

      <!-- Toast container -->
      <div class="toast-container">
        <TransitionGroup name="toast-list">
          <div
            v-for="toast in toasts"
            :key="toast.id"
            class="toast"
            :class="{ 'toast-exit': toast.exiting }"
          >
            <div class="toast-icon" :class="toast.type">
              <i :class="{
                'bi bi-check-lg': toast.type === 'success',
                'bi bi-x-lg': toast.type === 'error',
                'bi bi-exclamation-lg': toast.type === 'warning',
                'bi bi-info-lg': toast.type === 'info'
              }"></i>
            </div>
            <div class="toast-body">
              <div class="toast-title">{{ toast.title }}</div>
              <div class="toast-message">{{ toast.message }}</div>
            </div>
            <button class="toast-close" @click="removeToast(toast.id)">
              <i class="bi bi-x"></i>
            </button>
          </div>
        </TransitionGroup>
      </div>
    </template>
  </div>
</template>

<style>
/* === LAYOUT SHELL === */
.app-shell {
  display: flex;
  min-height: 100vh;
}

/* === AUTH PAGE TRANSITION === */
.auth-page-enter-active,
.auth-page-leave-active {
  transition: opacity 0.3s ease, transform 0.3s ease;
}
.auth-page-enter-from { opacity: 0; transform: scale(0.97); }
.auth-page-leave-to { opacity: 0; transform: scale(1.03); }

/* === SIDEBAR === */
.sidebar {
  width: var(--sidebar-width);
  background: var(--color-bg-white);
  border-right: 1px solid var(--color-divider);
  display: flex;
  flex-direction: column;
  position: fixed;
  top: 0;
  left: 0;
  height: 100vh;
  z-index: 1040;
  transition: width var(--transition-slow);
  overflow: hidden;
}

.sidebar-collapsed {
  width: var(--sidebar-collapsed-width);
}

.sidebar-mobile-open {
  left: 0;
}

.sidebar-overlay {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.35);
  z-index: 1035;
  backdrop-filter: blur(3px);
  -webkit-backdrop-filter: blur(3px);
}

/* Brand */
.sidebar-brand {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 1.25rem;
  border-bottom: 1px solid var(--color-divider);
  min-height: var(--header-height);
  overflow: hidden;
}

.brand-icon {
  width: 38px;
  height: 38px;
  background: linear-gradient(135deg, var(--color-primary-700), var(--color-primary-500));
  border-radius: var(--border-radius-sm);
  display: flex;
  align-items: center;
  justify-content: center;
  color: #fff;
  font-size: 1.125rem;
  flex-shrink: 0;
  transition: transform var(--transition-base);
}

.brand-icon:hover {
  transform: scale(1.05);
}

.brand-text {
  font-family: var(--font-display);
  font-size: 1.2rem;
  color: var(--color-text-primary);
  white-space: nowrap;
  letter-spacing: -0.02em;
}

/* Navigation */
.sidebar-nav {
  flex: 1;
  padding: 0.75rem;
  overflow-y: auto;
  overflow-x: hidden;
}

.nav-list {
  list-style: none;
  padding: 0;
  margin: 0;
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.nav-link {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 0.675rem 0.75rem;
  border-radius: var(--border-radius-sm);
  color: var(--color-text-secondary);
  text-decoration: none;
  transition: all var(--transition-fast);
  white-space: nowrap;
  position: relative;
  font-weight: 500;
  font-size: 0.875rem;
}

.nav-link:hover {
  background: var(--color-primary-50);
  color: var(--color-primary-700);
}

.nav-link.active {
  background: var(--color-primary-700);
  color: #fff;
  box-shadow: 0 2px 8px rgba(24, 95, 165, 0.25);
}

.nav-link.active::before {
  content: '';
  position: absolute;
  left: 0;
  top: 50%;
  transform: translateY(-50%);
  width: 3px;
  height: 20px;
  background: #fff;
  border-radius: 0 3px 3px 0;
}

.nav-icon {
  font-size: 1.2rem;
  width: 24px;
  text-align: center;
  flex-shrink: 0;
}

.nav-label {
  font-size: 0.875rem;
}

/* Sidebar collapsed: show only icons */
.sidebar-collapsed .nav-link {
  justify-content: center;
  padding: 0.675rem;
}

.sidebar-collapsed .nav-link.active::before {
  left: 2px;
  width: 2px;
  height: 16px;
}

/* Sidebar footer */
.sidebar-footer {
  padding: 1rem 1.25rem;
  border-top: 1px solid var(--color-divider);
  overflow: hidden;
}

.sidebar-user {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.sidebar-user-compact {
  display: flex;
  justify-content: center;
}

.sidebar-user-info {
  flex: 1;
  min-width: 0;
}

.sidebar-user-name {
  font-weight: 600;
  font-size: 0.8125rem;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.sidebar-user-role {
  font-size: 0.6875rem;
  color: var(--color-text-secondary);
  text-transform: uppercase;
  letter-spacing: 0.04em;
}

/* === MAIN WRAPPER === */
.main-wrapper {
  flex: 1;
  margin-left: var(--sidebar-width);
  display: flex;
  flex-direction: column;
  min-height: 100vh;
  transition: margin-left var(--transition-slow);
}

.main-expanded {
  margin-left: var(--sidebar-collapsed-width);
}

/* === HEADER === */
.app-header {
  height: var(--header-height);
  background: var(--color-bg-white);
  border-bottom: 1px solid var(--color-divider);
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 1.5rem;
  position: sticky;
  top: 0;
  z-index: 1020;
  box-shadow: var(--shadow-sm);
}

.header-left {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.header-toggle .toggle-icon {
  transition: transform var(--transition-base);
}

.header-title h2 {
  margin: 0;
  font-size: 1.125rem;
  font-weight: 600;
}

.header-right {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.header-icon-btn {
  position: relative;
}

.notification-dot {
  position: absolute;
  top: 8px;
  right: 8px;
  width: 8px;
  height: 8px;
  background: var(--color-error-accent);
  border-radius: 50%;
  border: 2px solid var(--color-bg-white);
  animation: pulse-dot 2s ease-in-out infinite;
}

/* User dropdown */
.user-dropdown {
  position: relative;
}

.user-dropdown-trigger {
  display: flex;
  align-items: center;
  gap: 0.625rem;
  padding: 0.375rem 0.75rem;
  border-radius: var(--border-radius-sm);
  border: none;
  background: transparent;
  cursor: pointer;
  font-family: var(--font-body);
  transition: background var(--transition-fast);
}

.user-dropdown-trigger:hover {
  background: var(--color-primary-50);
}

.user-dropdown-info {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  line-height: 1.3;
  text-align: left;
}

.user-dropdown-name {
  font-weight: 600;
  font-size: 0.8125rem;
  color: var(--color-text-primary);
}

.dropdown-arrow {
  font-size: 0.75rem;
  color: var(--color-text-secondary);
  transition: transform var(--transition-fast);
}

.dropdown-arrow.open {
  transform: rotate(180deg);
}

.dropdown-menu {
  position: absolute;
  top: calc(100% + 0.5rem);
  right: 0;
  background: var(--color-bg-white);
  border: 1px solid var(--color-divider);
  border-radius: var(--border-radius-md);
  box-shadow: var(--shadow-lg);
  min-width: 220px;
  z-index: 1050;
  overflow: hidden;
}

.dropdown-header {
  padding: 1rem 1.125rem;
}

.dropdown-user-name {
  font-weight: 600;
  font-size: 0.9375rem;
  margin-bottom: 0.25rem;
}

.dropdown-user-email {
  font-size: 0.8125rem;
  color: var(--color-text-secondary);
  margin: 0;
}

.dropdown-item {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  width: 100%;
  padding: 0.75rem 1.125rem;
  border: none;
  background: transparent;
  cursor: pointer;
  font-family: var(--font-body);
  font-size: 0.875rem;
  color: var(--color-text-secondary);
  transition: all var(--transition-fast);
}

.dropdown-item:hover {
  background: var(--color-error-bg);
  color: var(--color-error-accent);
}

.dropdown-item i {
  font-size: 1rem;
}

/* Dropdown transition */
.dropdown-enter-active,
.dropdown-leave-active {
  transition: all 0.2s ease;
}
.dropdown-enter-from,
.dropdown-leave-to {
  opacity: 0;
  transform: translateY(-8px) scale(0.98);
}

/* === MAIN CONTENT === */
.main-content {
  flex: 1;
  padding: 1.5rem;
  overflow-y: auto;
  background: var(--color-bg-page);
  animation: fade-in 0.3s ease;
}

/* === TOAST LIST TRANSITIONS === */
.toast-list-enter-active,
.toast-list-leave-active {
  transition: all 0.35s ease;
}
.toast-list-enter-from {
  opacity: 0;
  transform: translateX(100%);
}
.toast-list-leave-to {
  opacity: 0;
  transform: translateX(100%);
}
.toast-list-move {
  transition: transform 0.35s ease;
}

/* === FADE TRANSITION FOR OVERLAY === */
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.25s ease;
}
.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

/* === RESPONSIVE === */
@media (max-width: 767px) {
  .sidebar {
    left: -100%;
    width: 280px !important;
    transition: left var(--transition-slow);
  }

  .sidebar-mobile-open {
    left: 0;
  }

  .main-wrapper {
    margin-left: 0 !important;
  }

  .app-header {
    padding: 0 1rem;
  }

  .user-dropdown-info {
    display: none;
  }

  .main-content {
    padding: 1rem;
  }

  .header-title h2 {
    font-size: 1rem;
  }
}

@media (min-width: 768px) {
  .sidebar {
    left: 0 !important;
  }
}
</style>
