import { createRouter, createWebHistory } from 'vue-router'
import ListEmpleados from '@/views/empleados/ListEmpleados.vue'
import EmpleadoForm from '@/views/empleados/EmpleadoForm.vue'
// Import other views as they are created

const routes = [
  {
    path: '/',
    name: 'home',
    redirect: () => {
      const userRole = localStorage.getItem('userRole')
      if (userRole === 'EMPLEADO') {
        return '/portal-personal'
      }
      return '/empleados'
    }
  },
  {
    path: '/portal-personal',
    name: 'portal-personal',
    component: () => import('@/views/empleados/PortalPersonal.vue'),
    meta: { requiresAuth: true, roles: ['EMPLEADO', 'ADMIN_RRHH', 'CONTADOR', 'GERENTE', 'ADMIN_SISTEMA'] }
  },
  {
    path: '/empleados',
    name: 'empleados-list',
    component: ListEmpleados,
    meta: { requiresAuth: true, roles: ['ADMIN_RRHH'] }
  },
  {
    path: '/empleados/nuevo',
    name: 'empleados-nuevo',
    component: EmpleadoForm,
    meta: { requiresAuth: true, roles: ['ADMIN_RRHH'] }
  },
  {
    path: '/empleados/editar/:id',
    name: 'empleados-editar',
    component: EmpleadoForm,
    meta: { requiresAuth: true, roles: ['ADMIN_RRHH'] }
  },
  {
    path: '/asistencia/aprobaciones',
    name: 'asistencia-aprobaciones',
    component: () => import('@/views/asistencia/AprobacionesAsistencia.vue'),
    meta: { requiresAuth: true, roles: ['ADMIN_RRHH'] }
  },
  {
    path: '/asistencia',
    name: 'asistencia-registro',
    component: () => import('@/views/asistencia/RegistroAsistencia.vue'),
    meta: { requiresAuth: true, roles: ['EMPLEADO', 'ADMIN_RRHH'] }
  },
  {
    path: '/nomina',
    name: 'nomina-liquidacion',
    component: () => import('@/views/nomina/LiquidacionNomina.vue'),
    meta: { requiresAuth: true, roles: ['CONTADOR', 'ADMIN_RRHH'] }
  },
  {
    path: '/reportes',
    name: 'reportes-dashboard',
    component: () => import('@/views/reportes/DashboardReportes.vue'),
    meta: { requiresAuth: true, roles: ['GERENTE', 'ADMIN_RRHH', 'CONTADOR'] }
  },
  {
    path: '/reportes/filtros',
    name: 'reportes-filtros',
    component: () => import('@/views/reportes/ReportesFiltrables.vue'),
    meta: { requiresAuth: true, roles: ['GERENTE', 'ADMIN_RRHH', 'CONTADOR'] }
  },
  {
    path: '/configuracion',
    name: 'configuracion-index',
    component: () => import('@/views/configuracion/Index.vue'),
    meta: { requiresAuth: true, roles: ['ADMIN_SISTEMA', 'ADMIN_RRHH'] }
  },
  {
    path: '/login',
    name: 'login',
    component: () => import('@/views/auth/Login.vue')
  },
  {
    path: '/reset-password',
    name: 'reset-password',
    component: () => import('@/views/auth/ResetPassword.vue')
  },
  {
    path: '/403',
    name: 'forbidden',
    component: {
      template: '<div class="container mt-5"><h2>Acceso Denegado</h2><p>No tiene permisos para acceder a esta página</p><router-link to="/" class="btn btn-link">Volver al inicio</router-link></div>'
    }
  }
  // Other routes will be added here as modules are implemented
]

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes
})

// Navigation guard for authentication and role-based access
router.beforeEach((to, from, next) => {
  // In a real app, we would check auth state from Pinia or localStorage
  // For now, we'll allow all navigation for development
  // TODO: Implement proper auth check with Pinia or Vuex

  // Simulate auth check - replace with real implementation
  const isAuthenticated = localStorage.getItem('token') !== null
  const userRole = localStorage.getItem('userRole') || 'ADMIN_RRHH' // Default for dev

  // Avoid infinite redirect loops
  if (to.meta.requiresAuth && !isAuthenticated) {
    // Redirect to login only if we're not already going to login or reset-password
    if (to.name !== 'login' && to.name !== 'reset-password') {
      next({ name: 'login', query: { redirect: to.fullPath } }) // Redirect to login if not authenticated
    } else {
      next() // Continue to login page
    }
  } else if (to.meta.roles && !to.meta.roles.includes(userRole)) {
    // Redirect to 403 only if we're not already going to 403
    if (to.path !== '/403') {
      next({ path: '/403' }) // Redirect to forbidden if insufficient permissions
    } else {
      next() // Continue to 403 page
    }
  } else {
    next()
  }
})

export default router