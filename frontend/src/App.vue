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
const navItems = computed(() => {
  const role = user.value.role
  const items = [
    { icon: 'bi-person-circle', label: 'Mi Portal', to: '/portal-personal' },
    { icon: 'bi-people', label: 'Empleados', to: '/empleados', roles: ['ADMIN_RRHH'] },
    { icon: 'bi-clock-history', label: 'Asistencia', to: '/asistencia', roles: ['EMPLEADO', 'ADMIN_RRHH'] },
    { icon: 'bi-check2-square', label: 'Aprobaciones', to: '/asistencia/aprobaciones', roles: ['ADMIN_RRHH'] },
    { icon: 'bi-cash-stack', label: 'Nómina', to: '/nomina', roles: ['CONTADOR', 'ADMIN_RRHH'] },
    { icon: 'bi-file-earmark-bar-graph', label: 'Reportes', to: '/reportes', roles: ['GERENTE', 'ADMIN_RRHH', 'CONTADOR'] },
    { icon: 'bi-gear', label: 'Configuración', to: '/configuracion', roles: ['ADMIN_SISTEMA', 'ADMIN_RRHH'] }
  ]
  return items.filter(item => !item.roles || item.roles.includes(role))
})

// === User state ===
const getInitials = (name) => {
  if (!name) return '?'
  return name.split(' ').map(w => w[0]).join('').toUpperCase().slice(0, 2)
}

const user = ref({
  name: localStorage.getItem('userName') || 'Alex Reed',
  role: localStorage.getItem('userRole') || 'ADMIN_RRHH',
  email: localStorage.getItem('userEmail') || 'alex.reed@apex.io',
  initials: getInitials(localStorage.getItem('userName')) || 'AR'
})

const userFirstName = computed(() => {
  const full = user.value.name || 'Alex'
  return full.split(' ')[0]
})

const userShortName = computed(() => {
  const parts = (user.value.name || 'Alex Reed').split(' ')
  if (parts.length > 1) {
    return `${parts[0]} ${parts[1].charAt(0)}.`
  }
  return parts[0]
})

const userDropdownOpen = ref(false)

const logout = () => {
  localStorage.removeItem('token')
  localStorage.removeItem('userRole')
  localStorage.removeItem('userName')
  localStorage.removeItem('userEmail')
  localStorage.removeItem('userId')
  localStorage.removeItem('locationGranted')
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
    name: name || 'Alex Reed',
    role: localStorage.getItem('userRole') || 'ADMIN_RRHH',
    email: localStorage.getItem('userEmail') || 'alex.reed@apex.io',
    initials: getInitials(name) || 'AR'
  }
})

// === Computed ===
const isAuthPage = computed(() => {
  return route.path === '/login' || route.path === '/reset-password'
})

const pageTitle = computed(() => {
  const item = navItems.value.find(n => route.path.startsWith(n.to) && n.to !== '/')
  if (route.path === '/') return 'Dashboard'
  if (route.path.includes('/portal-personal')) return 'Portal Personal'
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
            <i class="bi bi-triangle-fill" style="transform: rotate(90deg); font-size: 1rem;"></i>
          </div>
          <Transition name="fade" mode="out-in">
            <span v-if="!sidebarCollapsed || isMobile" class="brand-text" key="text">
              Apex HRM
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
            <div class="header-welcome-container">
              <h1 class="welcome-heading">Welcome Back, {{ user.name }}!</h1>
            </div>
          </div>

          <div class="header-right">
            <!-- Notification bell with badge -->
            <button class="header-icon-btn" data-tooltip="Notificaciones">
              <i class="bi bi-bell"></i>
              <span class="notification-badge-count">3</span>
            </button>

            <!-- User profile dropdown trigger -->
            <div class="user-dropdown">
              <button class="user-dropdown-trigger" @click.stop="userDropdownOpen = !userDropdownOpen">
                <div class="avatar avatar-sm avatar-pill">{{ user.initials }}</div>
                <span class="user-dropdown-name">{{ userShortName }}</span>
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
:root {
  --color-apex-bg: #F3F5FA;
  --color-apex-card: #FFFFFF;
  --color-apex-primary: #3B489E;
  --color-apex-primary-hover: #2E3A85;
  --color-apex-text: #101828;
  --color-apex-muted: #64748B;
  --color-apex-border: #E2E8F0;
  --color-apex-active-item: #E0E5F0;
}

body {
  background-color: var(--color-apex-bg) !important;
}

.app-shell {
  display: flex;
  min-height: 100vh;
  width: 100%;
  max-width: 100vw;
  overflow-x: hidden;
  background-color: var(--color-apex-bg);
}

/* === SIDEBAR === */
.sidebar {
  width: var(--sidebar-width);
  background: var(--color-apex-bg);
  border-right: 1px solid rgba(226, 232, 240, 0.7);
  display: flex;
  flex-direction: column;
  position: fixed;
  top: 0;
  left: 0;
  height: 100vh;
  z-index: 1040;
  transition: width var(--transition-slow);
  overflow: hidden;
  padding: 0 0.5rem;
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
  padding: 1.5rem 1rem;
  min-height: var(--header-height);
  overflow: hidden;
}

.brand-icon {
  width: 36px;
  height: 36px;
  background: var(--color-apex-primary);
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #fff;
  font-size: 1rem;
  flex-shrink: 0;
  transition: transform var(--transition-base);
}

.brand-icon:hover {
  transform: scale(1.05);
}

.brand-text {
  font-family: var(--font-body);
  font-size: 1.35rem;
  font-weight: 700;
  color: var(--color-apex-text);
  white-space: nowrap;
  letter-spacing: -0.02em;
}

/* Navigation */
.sidebar-nav {
  flex: 1;
  padding: 0.5rem 0.25rem;
  overflow-y: auto;
}

.nav-list {
  list-style: none;
  padding: 0;
  margin: 0;
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.nav-link {
  display: flex;
  align-items: center;
  gap: 0.85rem;
  padding: 0.7rem 1rem;
  border-radius: 12px;
  color: var(--color-apex-muted);
  text-decoration: none;
  transition: all var(--transition-fast);
  white-space: nowrap;
  position: relative;
  font-weight: 500;
  font-size: 0.9375rem;
}

.nav-link:hover {
  background: #E8EEF8;
  color: var(--color-apex-text);
}

.nav-link.active {
  background: var(--color-apex-active-item);
  color: var(--color-apex-text);
  font-weight: 700;
  box-shadow: none;
}

.nav-link.active .nav-icon {
  color: var(--color-apex-primary);
}

.nav-icon {
  font-size: 1.15rem;
  width: 22px;
  text-align: center;
  flex-shrink: 0;
}

.nav-label {
  font-size: 0.9375rem;
}

/* Sidebar collapsed: show only icons */
.sidebar-collapsed .nav-link {
  justify-content: center;
  padding: 0.7rem;
}

/* Sidebar footer */
.sidebar-footer {
  padding: 1rem 1rem;
  border-top: 1px solid var(--color-apex-border);
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
  font-size: 0.85rem;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  color: var(--color-apex-text);
}

.sidebar-user-role {
  font-size: 0.7rem;
  color: var(--color-apex-muted);
  text-transform: uppercase;
  letter-spacing: 0.04em;
}

/* === MAIN WRAPPER === */
.main-wrapper {
  flex: 1;
  min-width: 0;
  margin-left: var(--sidebar-width);
  display: flex;
  flex-direction: column;
  min-height: 100vh;
  transition: margin-left var(--transition-slow);
  background: var(--color-apex-bg);
}

.main-expanded {
  margin-left: var(--sidebar-collapsed-width);
}

/* === HEADER === */
.app-header {
  height: auto;
  min-height: 80px;
  background: var(--color-apex-bg);
  border-bottom: none;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 1.25rem 2rem;
  position: sticky;
  top: 0;
  z-index: 1020;
}

.header-left {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.welcome-heading {
  font-size: 1.65rem;
  font-weight: 800;
  color: var(--color-apex-text);
  margin: 0;
  letter-spacing: -0.02em;
}

.header-right {
  display: flex;
  align-items: center;
  gap: 1.25rem;
}

.header-search-bar {
  position: relative;
  display: flex;
  align-items: center;
}

.header-search-input {
  background: #FFFFFF;
  border: 1px solid var(--color-apex-border);
  border-radius: 9999px;
  padding: 0.5rem 2.5rem 0.5rem 1.25rem;
  font-size: 0.9rem;
  color: var(--color-apex-text);
  outline: none;
  width: 220px;
  box-shadow: 0 1px 3px rgba(0,0,0,0.03);
  transition: all 0.2s ease;
}

.header-search-input:focus {
  width: 280px;
  border-color: var(--color-apex-primary);
  box-shadow: 0 0 0 3px rgba(59, 72, 158, 0.15);
}

.header-search-icon {
  position: absolute;
  right: 14px;
  color: var(--color-apex-muted);
  font-size: 0.95rem;
  pointer-events: none;
}

.header-icon-btn {
  position: relative;
  background: #FFFFFF;
  border: 1px solid var(--color-apex-border);
  width: 40px;
  height: 40px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  color: var(--color-apex-text);
  font-size: 1.15rem;
  box-shadow: 0 1px 3px rgba(0,0,0,0.03);
  transition: background 0.2s;
}

.header-icon-btn:hover {
  background: #F8FAFC;
}

.notification-badge-count {
  position: absolute;
  top: -4px;
  right: -4px;
  background: var(--color-apex-primary);
  color: #FFFFFF;
  font-size: 0.7rem;
  font-weight: 700;
  width: 20px;
  height: 20px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  border: 2px solid #FFFFFF;
}

/* User dropdown */
.user-dropdown {
  position: relative;
}

.user-dropdown-trigger {
  display: flex;
  align-items: center;
  gap: 0.6rem;
  padding: 0.25rem 0.5rem;
  border-radius: 9999px;
  border: none;
  background: transparent;
  cursor: pointer;
  font-family: var(--font-body);
}

.avatar-pill {
  width: 38px;
  height: 38px;
  border-radius: 50%;
  background: #2D3748;
  color: #FFFFFF;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 700;
  font-size: 0.9rem;
}

.user-dropdown-name {
  font-weight: 700;
  font-size: 0.95rem;
  color: var(--color-apex-text);
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
  min-width: 0;
  padding: 1.5rem;
  overflow-y: auto;
  overflow-x: hidden;
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

/* === RESPONSIVE SHELL === */
@media (min-width: 768px) and (max-width: 1024px) {
  .welcome-heading {
    font-size: 1.3rem;
  }

  .app-header {
    padding: 1rem 1.25rem;
  }

  .main-content {
    padding: 1.25rem;
  }
}

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
    padding: 0.85rem 1rem;
    min-height: 64px;
  }

  .welcome-heading {
    font-size: 1.15rem;
  }

  .user-dropdown-info {
    display: none;
  }

  .user-dropdown-name {
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
