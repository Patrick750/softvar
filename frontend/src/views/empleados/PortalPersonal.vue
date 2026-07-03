<template>
  <div>
    <div class="page-header">
      <h1 class="display-heading">Portal Personal</h1>
      <p class="text-muted" v-if="employee">Bienvenido, {{ employee.nombres }}</p>
    </div>

    <!-- Loading State -->
    <div v-if="loading" class="text-center py-5">
      <div class="spinner spinner-lg mx-auto"></div>
      <p class="mt-3 text-muted">Cargando información del portal...</p>
    </div>

    <!-- Error State -->
    <div v-else-if="error" class="alert alert-error mb-4">
      <i class="bi bi-exclamation-triangle-fill me-2"></i>
      {{ error }}
    </div>

    <div v-else class="layout-grid grid-2">
      <!-- Profile card -->
      <div class="card card-elevated p-0">
        <div class="card-header-primary">
          <h5><i class="bi bi-person-circle me-2"></i>Mi Información</h5>
        </div>
        <div class="card-body" v-if="employee">
          <div class="avatar-container mb-3 text-center">
            <img v-if="getProfilePhoto(employee.foto_facial)" :src="getProfilePhoto(employee.foto_facial)" alt="Mi Foto" class="avatar avatar-xl avatar-placeholder">
            <div v-else class="avatar avatar-xl avatar-placeholder">
              {{ (employee.nombres?.charAt(0) || '') + (employee.apellidos?.charAt(0) || '') }}
            </div>
          </div>
          <h4 class="fw-bold mb-1 text-center">{{ employee.nombres }} {{ employee.apellidos }}</h4>
          <p class="text-muted mb-3 text-center">{{ employee.cargo }}</p>
          <div class="divider"></div>

          <div v-if="!editing" class="info-grid text-center">
            <div><span class="text-muted">Cédula:</span> <span class="fw-semibold">{{ employee.cedula }}</span></div>
            <div class="mt-2"><span class="text-muted">Email:</span> <span class="fw-semibold">{{ employee.email }}</span></div>
            <div class="mt-2"><span class="text-muted">Teléfono:</span> <span class="fw-semibold">{{ employee.telefono || 'N/A' }}</span></div>
            <div class="mt-2"><span class="text-muted">Fecha Ingreso:</span> <span class="fw-semibold">{{ formatDate(employee.fecha_ingreso) }}</span></div>
          </div>

          <form v-if="editing" @submit.prevent="saveEdit" class="mt-3">
            <div class="mb-3">
              <label class="form-label">Nombres</label>
              <input type="text" class="form-input" v-model="editedEmployee.nombres" required>
            </div>
            <div class="mb-3">
              <label class="form-label">Apellidos</label>
              <input type="text" class="form-input" vmodel="editedEmployee.apellidos" required>
            </div>
            <div class="mb-3">
              <label class="form-label">Teléfono</label>
              <input type="tel" class="form-input" v-model="editedEmployee.telefono" placeholder="Opcional">
            </div>
            <div class="flex-row gap-sm mt-3">
              <button type="submit" class="btn btn-primary flex-1">
                <span v-if="saving" class="spinner spinner-sm me-2"></span>
                Guardar Cambios
              </button>
              <button type="button" class="btn btn-outline flex-1" @click="cancelEdit">
                Cancelar
              </button>
            </div>
          </form>

          <div class="mt-3 text-center">
            <button class="btn btn-outline-primary" @click="startEdit">
              <i class="bi bi-pencil me-2"></i>Editar Información
            </button>
          </div>
        </div>
      </div>

      <!-- Attendance & Password -->
      <div class="flex-col" style="gap: 1.25rem;">
        <!-- Attendance section -->
        <div class="card card-elevated p-0">
          <div class="card-header-success">
            <h5><i class="bi bi-clock-history me-2"></i>Mis Asistencias</h5>
          </div>
          <div class="card-body">
            <div class="flex-row gap-sm mb-3">
              <button class="btn btn-sm btn-outline-success" @click="mostrarTodos">Todos</button>
              <button class="btn btn-sm btn-outline-success" @click="filtrarHoy">Hoy</button>
              <button class="btn btn-sm btn-outline-success" @click="filtrarMes">Este Mes</button>
              <button class="btn btn-sm btn-outline-success" @click="filtrarAnio">Este Año</button>
            </div>
            <div class="table-container">
              <table class="table table-compact">
                <thead>
                  <tr>
                    <th>Fecha y Hora</th>
                    <th>Tipo</th>
                    <th>Estado</th>
                    <th>Observaciones/Detalles</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="(att, idx) in paginatedAttendances" :key="att.id" class="data-row" :style="{ '--i': idx }">
                    <td>{{ formatDateTime(att.fecha_hora) }}</td>
                    <td>
                      <span class="badge" :class="att.tipo === 'ENTRADA' ? 'badge-solid-primary' : 'badge-neutral'">
                        {{ att.tipo }}
                      </span>
                    </td>
                    <td>
                      <span v-if="att.estado === 'EXITO'" class="badge badge-solid-success">Exitosa</span>
                      <span v-else-if="att.estado === 'PENDIENTE_APROBACION'" class="badge badge-warning">Pendiente RRHH</span>
                      <span v-else-if="att.estado === 'RECHAZADO'" class="badge badge-neutral">Rechazada</span>
                      <span v-else class="badge badge-solid-error">Fallida</span>
                    </td>
                    <td>
                      <span class="text-sm">{{ att.observaciones || att.justificacion_manual || '-' }}</span>
                    </td>
                  </tr>
                  <tr v-if="!paginatedAttendances.length" class="empty-row">
                    <td colspan="4" class="text-center text-muted py-4">No hay registros de asistencia</td>
                  </tr>
                </tbody>
              </table>
            </div>

            <!-- Controles de Paginación -->
            <div v-if="totalPages > 1" class="flex-row gap-sm mt-3" style="justify-content: center; align-items: center;">
              <button class="btn btn-sm btn-outline" @click="prevPage" :disabled="currentPage === 1">Anterior</button>
              <span class="text-muted text-sm mx-3">Página {{ currentPage }} de {{ totalPages }}</span>
              <button class="btn btn-sm btn-outline" @click="nextPage" :disabled="currentPage === totalPages">Siguiente</button>
            </div>

          </div>
        </div>

        <!-- Password change -->
        <div class="card card-elevated p-0">
          <div class="card-header-warning">
            <h5><i class="bi bi-key me-2"></i>Cambiar Contraseña</h5>
          </div>
          <div class="card-body">
            <form @submit.prevent="changePassword" class="layout-grid grid-3">
              <div class="form-group">
                <label class="form-label" for="currentPassword">Contraseña Actual *</label>
                <input type="password" class="form-input" id="currentPassword" v-model="passwordForm.current" required>
              </div>
              <div class="form-group">
                <label class="form-label" for="newPassword">Nueva Contraseña *</label>
                <input type="password" class="form-input" id="newPassword" v-model="passwordForm.new" required minlength="6">
              </div>
              <div class="form-group">
                <label class="form-label" for="confirmPassword">Confirmar *</label>
                <input type="password" class="form-input" id="confirmPassword" v-model="passwordForm.confirm" required>
              </div>
              <div class="col-span-2">
                <button type="submit" class="btn btn-warning" :disabled="changingPassword">
                  <span v-if="changingPassword" class="spinner spinner-sm me-2"></span>
                  <i v-else class="bi bi-shield-lock me-2"></i>
                  Cambiar Contraseña
                </button>
              </div>
            </form>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, computed, onMounted, inject } from 'vue'
import axios from 'axios'

export default {
  setup() {
    const employee = ref(null)
    const rawAttendances = ref([])
    const attendances = ref([])
    const loading = ref(true)
    const error = ref('')
    const addToast = inject('addToast', () => {})

    const passwordForm = ref({ current: '', new: '', confirm: '' })
    const changingPassword = ref(false)

    // Edit profile state
    const editing = ref(false)
    const editedEmployee = ref({ nombres: '', apellidos: '', telefono: '' })
    const saving = ref(false)

    // Pagination state
    const currentPage = ref(1)
    const itemsPerPage = ref(5)

    const paginatedAttendances = computed(() => {
      const start = (currentPage.value - 1) * itemsPerPage.value
      const end = start + itemsPerPage.value
      return attendances.value.slice(start, end)
    })

    const totalPages = computed(() => {
      return Math.ceil(attendances.value.length / itemsPerPage.value) || 1
    })

    const nextPage = () => {
      if (currentPage.value < totalPages.value) currentPage.value++
    }

    const prevPage = () => {
      if (currentPage.value > 1) currentPage.value--
    }

    const loadData = async () => {
      loading.value = true
      error.value = ''
      try {
        // Fetch personal details
        const empResponse = await axios.get('/api/empleados/me/')
        employee.value = empResponse.data

        // Fetch attendance logs
        const attResponse = await axios.get('/api/asistencia/historial/')
        rawAttendances.value = attResponse.data
        applyFilter('all')
      } catch (err) {
        console.error('Error loading personal portal data:', err)
        error.value = 'No se pudieron cargar sus datos personales de la API. Verifique su conexión y sesión.'
      } finally {
        loading.value = false
      }
    }

    const getProfilePhoto = (fotoFacial) => {
      if (!fotoFacial) return null
      try {
        const parsed = typeof fotoFacial === 'string' ? JSON.parse(fotoFacial) : fotoFacial
        return parsed.image || null
      } catch (e) {
        return null
      }
    }

    const formatDate = (dateStr) => {
      if (!dateStr) return '-'
      const parts = dateStr.split('-')
      if (parts.length === 3) {
        return `${parts[2]}/${parts[1]}/${parts[0]}`
      }
      return dateStr
    }

    const formatDateTime = (isoString) => {
      if (!isoString) return '-'
      const date = new Date(isoString)
      return date.toLocaleString('es-CO', {
        day: '2-digit',
        month: '2-digit',
        year: 'numeric',
        hour: '2-digit',
        minute: '2-digit',
        second: '2-digit',
        hour12: true
      })
    }

    const applyFilter = (filterType) => {
      const now = new Date()
      const todayStr = now.toISOString().split('T')[0]
      const currentMonth = now.getMonth()
      const currentYear = now.getFullYear()

      if (filterType === 'hoy') {
        attendances.value = rawAttendances.value.filter(att => {
          if (!att.fecha_hora) return false
          return att.fecha_hora.split('T')[0] === todayStr
        })
      } else if (filterType === 'mes') {
        attendances.value = rawAttendances.value.filter(att => {
          if (!att.fecha_hora) return false
          const d = new Date(att.fecha_hora)
          return d.getMonth() === currentMonth && d.getFullYear() === currentYear
        })
      } else if (filterType === 'anio') {
        attendances.value = rawAttendances.value.filter(att => {
          if (!att.fecha_hora) return false
          const d = new Date(att.fecha_hora)
          return d.getFullYear() === currentYear
        })
      } else {
        attendances.value = [...rawAttendances.value]
      }
      
      currentPage.value = 1 // Reset pagination on filter change
    }

    const filtrarHoy = () => applyFilter('hoy')
    const filtrarMes = () => applyFilter('mes')
    const filtrarAnio = () => applyFilter('anio')
    const mostrarTodos = () => applyFilter('all')

    const changePassword = async () => {
      if (passwordForm.value.new !== passwordForm.value.confirm) {
        addToast('Error', 'Las contraseñas nuevas no coinciden.', 'error')
        return
      }

      changingPassword.value = true
      try {
        await axios.post('/api/auth/password/', {
          current_password: passwordForm.value.current,
          new_password: passwordForm.value.new
        })
        addToast('Éxito', 'Su contraseña ha sido cambiada correctamente.', 'success')
        passwordForm.value = { current: '', new: '', confirm: '' }
      } catch (err) {
        console.error('Password change error:', err)
        const errMsg = err.response?.data?.error || 'No se pudo cambiar la contraseña.'
        addToast('Error', errMsg, 'error')
      } finally {
        changingPassword.value = false
      }
    }

    // Edit profile functions
    const startEdit = () => {
      if (employee.value) {
        editedEmployee.value = {
          nombres: employee.value.nombres,
          apellidos: employee.value.apellidos,
          telefono: employee.value.telefono || ''
        }
        editing.value = true
      }
    }

    const cancelEdit = () => {
      editing.value = false
    }

    const saveEdit = async () => {
      saving.value = true
      try {
        await axios.patch(`/api/empleados/${employee.value.id}/`, {
          nombres: editedEmployee.value.nombres,
          apellidos: editedEmployee.value.apellidos,
          telefono: editedEmployee.value.telefono || null
        })
        // Update the displayed employee
        employee.value.nombres = editedEmployee.value.nombres
        employee.value.apellidos = editedEmployee.value.apellidos
        employee.value.telefono = editedEmployee.value.telefono || null
        addToast('Éxito', 'Información actualizada correctamente.', 'success')
        editing.value = false
      } catch (err) {
        console.error('Error updating employee:', err)
        const errMsg = err.response?.data?.error || 'No se pudo actualizar la información.'
        addToast('Error', errMsg, 'error')
      } finally {
        saving.value = false
      }
    }

    onMounted(loadData)

    return {
      employee,
      attendances,
      passwordForm,
      loading,
      error,
      changingPassword,
      changePassword,
      filtrarHoy,
      filtrarMes,
      filtrarAnio,
      mostrarTodos,
      getProfilePhoto,
      formatDate,
      formatDateTime,
      currentPage,
      totalPages,
      paginatedAttendances,
      nextPage,
      prevPage
    }
  }
}
</script>

<style scoped>
.col-span-2 {
  grid-column: 1 / -1;
}

.avatar-container {
  display: flex;
  justify-content: center;
}

.info-grid {
  text-align: left;
  max-width: 320px;
  margin: 0 auto;
}

.data-row {
  opacity: 0;
  transform: translateY(8px);
  animation: fadeInRow 0.35s ease forwards;
  animation-delay: calc(var(--i, 0) * 60ms);
  transition: background 0.2s, transform 0.15s;
}

.data-row:hover {
  background: var(--color-primary-50);
}

.data-row:last-child td {
  border-bottom: none;
}

.empty-row td {
  border-bottom: none;
}

@keyframes fadeInRow {
  from {
    opacity: 0;
    transform: translateY(8px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

@media (prefers-reduced-motion: reduce) {
  .data-row {
    animation: none;
    opacity: 1;
    transform: none;
  }
}

@media (max-width: 768px) {
  .layout-grid { grid-template-columns: 1fr; }
}
</style>
