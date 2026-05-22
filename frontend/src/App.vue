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

// Proveer funcion de toast globalmente
provide('addToast', addToast)

// Actualizar datos del usuario desde localStorage cuando cambie la ruta
// Esto asegura que despues del login el sidebar muestre el usuario real
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
</script>

<template>
  <div class="app-container">
    <!-- Auth pages (login, reset password) - no layout -->
    <template v-if="isAuthPage">
      <router-view />
    </template>

    <!-- Main app layout -->
    <template v-else>
      <!-- Overlay for mobile sidebar -->
      <div
        v-if="mobileSidebarOpen"
        class="sidebar-overlay"
        @click="mobileSidebarOpen = false"
      ></div>

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
          <span class="brand-text" v-show="!sidebarCollapsed || isMobile">
            SoftVar
          </span>
        </div>

        <nav class="sidebar-nav">
          <ul class="nav-list">
            <li v-for="item in navItems" :key="item.to" class="nav-item-custom">
              <router-link
                :to="item.to"
                class="nav-link-custom"
                :class="{ active: route.path === item.to || (item.to !== '/' && route.path.startsWith(item.to)) }"
                @click="isMobile && (mobileSidebarOpen = false)"
              >
                <i :class="`bi ${item.icon}`" class="nav-icon"></i>
                <span class="nav-label-custom" v-show="!sidebarCollapsed || isMobile">
                  {{ item.label }}
                </span>
              </router-link>
            </li>
          </ul>
        </nav>

        <div class="sidebar-footer" v-show="!sidebarCollapsed || isMobile">
          <div class="sidebar-user">
            <div class="sidebar-user-avatar avatar avatar-placeholder avatar-sm">
              {{ user.initials }}
            </div>
            <div class="sidebar-user-info">
              <div class="sidebar-user-name">{{ user.name }}</div>
              <div class="sidebar-user-role">{{ user.role }}</div>
            </div>
          </div>
        </div>
      </aside>

      <!-- Main content area -->
      <div class="main-wrapper" :class="{ 'main-expanded': !isMobile && sidebarCollapsed }">
        <!-- Header -->
        <header class="app-header">
          <div class="header-left">
            <button class="header-toggle" @click="toggleSidebar" :title="sidebarCollapsed ? 'Expandir menú' : 'Colapsar menú'">
              <i class="bi bi-list"></i>
            </button>
            <div class="header-title">
              <h2>{{ pageTitle }}</h2>
            </div>
          </div>

          <div class="header-right">
            <!-- Notification bell -->
            <button class="header-icon-btn" title="Notificaciones">
              <i class="bi bi-bell"></i>
              <span class="notification-dot"></span>
            </button>

            <!-- User dropdown -->
            <div class="user-dropdown" @click="userDropdownOpen = !userDropdownOpen">
              <div class="user-dropdown-trigger">
                <div class="avatar avatar-placeholder avatar-sm">{{ user.initials }}</div>
                <div class="user-dropdown-info">
                  <span class="user-dropdown-name">{{ user.name }}</span>
                  <span class="user-dropdown-role">{{ user.role }}</span>
                </div>
                <i class="bi bi-chevron-down dropdown-arrow" :class="{ open: userDropdownOpen }"></i>
              </div>

              <Transition name="dropdown">
                <div v-if="userDropdownOpen" class="dropdown-menu-custom">
                  <div class="dropdown-header-custom">
                    <p class="dropdown-user-name">{{ user.name }}</p>
                    <p class="dropdown-user-email">{{ user.email }}</p>
                  </div>
                  <div class="dropdown-divider-custom"></div>
                  <button class="dropdown-item-custom" @click="logout">
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
      <div class="toast-container-custom">
        <TransitionGroup name="toast-list">
          <div
            v-for="toast in toasts"
            :key="toast.id"
            class="toast-custom"
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
            <div class="toast-body-custom">
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
/* === LAYOUT === */
.app-container {
  display: flex;
  min-height: 100vh;
}

/* === SIDEBAR === */
.sidebar {
  width: var(--sidebar-width);
  background: #fff;
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
  background: rgba(0, 0, 0, 0.4);
  z-index: 1035;
  backdrop-filter: blur(2px);
}

/* Brand */
.sidebar-brand {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 1.25rem 1.25rem;
  border-bottom: 1px solid var(--color-divider);
  min-height: var(--header-height);
}

.brand-icon {
  width: 36px;
  height: 36px;
  background: var(--color-primary-700);
  border-radius: var(--border-radius-sm);
  display: flex;
  align-items: center;
  justify-content: center;
  color: #fff;
  font-size: 1.125rem;
  flex-shrink: 0;
}

.brand-text {
  font-weight: 700;
  font-size: 1.15rem;
  color: var(--color-text-primary);
  white-space: nowrap;
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

.nav-link-custom {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 0.7rem 0.875rem;
  border-radius: var(--border-radius-sm);
  color: var(--color-text-secondary);
  text-decoration: none;
  transition: all var(--transition-fast);
  white-space: nowrap;
  position: relative;
}

.nav-link-custom:hover {
  background: var(--color-primary-50);
  color: var(--color-primary-700);
}

.nav-link-custom.active {
  background: var(--color-primary-700);
  color: #fff;
}

.nav-icon {
  font-size: 1.25rem;
  width: 24px;
  text-align: center;
  flex-shrink: 0;
}

.nav-label-custom {
  font-weight: 500;
  font-size: 0.9rem;
}

/* Sidebar collapsed: show only icons */
.sidebar-collapsed .nav-link-custom {
  justify-content: center;
  padding: 0.7rem;
}

/* Sidebar footer */
.sidebar-footer {
  padding: 1rem 1.25rem;
  border-top: 1px solid var(--color-divider);
}

.sidebar-user {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.sidebar-user-info {
  flex: 1;
  min-width: 0;
}

.sidebar-user-name {
  font-weight: 600;
  font-size: 0.875rem;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.sidebar-user-role {
  font-size: 0.75rem;
  color: var(--color-text-secondary);
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
  background: #fff;
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
  gap: 1rem;
}

.header-toggle {
  width: 36px;
  height: 36px;
  border: 1px solid var(--color-divider);
  border-radius: var(--border-radius-sm);
  background: transparent;
  color: var(--color-text-secondary);
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all var(--transition-fast);
  font-size: 1.2rem;
}

.header-toggle:hover {
  background: var(--color-primary-50);
  color: var(--color-primary-700);
  border-color: var(--color-primary-200);
}

.header-title h2 {
  margin: 0;
  font-size: 1.25rem;
  font-weight: 600;
}

.header-right {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.header-icon-btn {
  width: 36px;
  height: 36px;
  border: none;
  border-radius: var(--border-radius-sm);
  background: transparent;
  color: var(--color-text-secondary);
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all var(--transition-fast);
  font-size: 1.2rem;
  position: relative;
}

.header-icon-btn:hover {
  background: var(--color-primary-50);
  color: var(--color-primary-700);
}

.notification-dot {
  position: absolute;
  top: 6px;
  right: 6px;
  width: 8px;
  height: 8px;
  background: var(--color-error-accent);
  border-radius: 50%;
  border: 2px solid #fff;
}

/* User dropdown */
.user-dropdown {
  position: relative;
  cursor: pointer;
}

.user-dropdown-trigger {
  display: flex;
  align-items: center;
  gap: 0.625rem;
  padding: 0.375rem 0.75rem;
  border-radius: var(--border-radius-sm);
  transition: background var(--transition-fast);
}

.user-dropdown-trigger:hover {
  background: var(--color-primary-50);
}

.user-dropdown-info {
  display: flex;
  flex-direction: column;
  line-height: 1.3;
}

.user-dropdown-name {
  font-weight: 600;
  font-size: 0.875rem;
}

.user-dropdown-role {
  font-size: 0.75rem;
  color: var(--color-text-secondary);
}

.dropdown-arrow {
  font-size: 0.75rem;
  color: var(--color-text-secondary);
  transition: transform var(--transition-fast);
}

.dropdown-arrow.open {
  transform: rotate(180deg);
}

.dropdown-menu-custom {
  position: absolute;
  top: calc(100% + 0.5rem);
  right: 0;
  background: #fff;
  border: 1px solid var(--color-divider);
  border-radius: var(--border-radius-md);
  box-shadow: var(--shadow-lg);
  min-width: 220px;
  z-index: 1050;
  overflow: hidden;
}

.dropdown-header-custom {
  padding: 1rem 1.125rem;
}

.dropdown-user-name {
  font-weight: 600;
  margin-bottom: 0.25rem;
}

.dropdown-user-email {
  font-size: 0.85rem;
  color: var(--color-text-secondary);
  margin: 0;
}

.dropdown-divider-custom {
  height: 1px;
  background: var(--color-divider);
}

.dropdown-item-custom {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  width: 100%;
  padding: 0.75rem 1.125rem;
  border: none;
  background: transparent;
  cursor: pointer;
  font-size: 0.9rem;
  color: var(--color-text-secondary);
  transition: all var(--transition-fast);
}

.dropdown-item-custom:hover {
  background: var(--color-primary-50);
  color: var(--color-error-accent);
}

/* Dropdown transition */
.dropdown-enter-active,
.dropdown-leave-active {
  transition: all 0.2s ease;
}

.dropdown-enter-from,
.dropdown-leave-to {
  opacity: 0;
  transform: translateY(-8px);
}

/* === MAIN CONTENT === */
.main-content {
  flex: 1;
  padding: 1.5rem;
  overflow-y: auto;
  background: var(--color-bg-page);
}

/* === TOAST TRANSITIONS === */
.toast-list-enter-active,
.toast-list-leave-active {
  transition: all 0.3s ease;
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
  transition: transform 0.3s ease;
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
    font-size: 1.1rem;
  }
}
</style>
