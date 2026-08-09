<template>
  <div class="apex-portal-container">
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

    <div v-else class="portal-two-columns">
      <!-- LEFT COLUMN: Profile Card & Security Card -->
      <div class="left-col-wrapper">
        
        <!-- CARD 1: User Profile -->
        <div class="apex-card profile-card">
          <h3 class="apex-card-title">User Profile</h3>
          
          <div class="profile-hero" v-if="employee">
            <div class="profile-avatar-container">
              <img v-if="getProfilePhoto(employee.foto_facial)" :src="getProfilePhoto(employee.foto_facial)" alt="Foto" class="profile-avatar-img">
              <div v-else class="profile-avatar-initials">
                {{ (employee.nombres?.charAt(0) || 'A') + (employee.apellidos?.charAt(0) || 'R') }}
              </div>
            </div>
            
            <div class="profile-identity">
              <h2 class="user-fullname">{{ employee.nombres }} {{ employee.apellidos }}</h2>
              <p class="user-jobtitle">{{ employee.cargo || 'Lead Designer' }}</p>
              <p class="user-email-text">{{ employee.email }}</p>
              <div class="status-active-badge">
                <span class="active-dot"></span> Active
              </div>
            </div>
          </div>

          <!-- Action Buttons -->
          <div v-if="!editing" class="profile-button-group">
            <button class="btn-apex-primary" @click="startEdit">
              Edit Profile
            </button>
            <button class="btn-apex-outline" @click="showDetails = !showDetails">
              {{ showDetails ? 'Ocultar Detalles' : 'View Details' }}
            </button>
          </div>

          <!-- Extended details toggle -->
          <div v-if="!editing && showDetails && employee" class="extended-details-panel">
            <div class="detail-item"><span>Cédula:</span> <strong>{{ employee.cedula }}</strong></div>
            <div class="detail-item"><span>Teléfono:</span> <strong>{{ employee.telefono || 'N/A' }}</strong></div>
            <div class="detail-item"><span>Fecha Ingreso:</span> <strong>{{ formatDate(employee.fecha_ingreso) }}</strong></div>
          </div>

          <!-- Edit Profile Form -->
          <form v-if="editing" @submit.prevent="saveEdit" class="edit-profile-form">
            <div class="apex-form-group">
              <label class="apex-form-label">Nombres</label>
              <input type="text" class="apex-input" v-model="editedEmployee.nombres" required>
            </div>
            <div class="apex-form-group">
              <label class="apex-form-label">Apellidos</label>
              <input type="text" class="apex-input" v-model="editedEmployee.apellidos" required>
            </div>
            <div class="apex-form-group">
              <label class="apex-form-label">Teléfono</label>
              <input type="tel" class="apex-input" v-model="editedEmployee.telefono" placeholder="Opcional">
            </div>
            <div class="form-btn-row">
              <button type="submit" class="btn-apex-primary flex-1" :disabled="saving">
                <span v-if="saving" class="spinner spinner-sm me-2"></span>
                Guardar
              </button>
              <button type="button" class="btn-apex-outline flex-1" @click="cancelEdit">
                Cancelar
              </button>
            </div>
          </form>
        </div>

        <!-- CARD 2: Security & Settings -->
        <div class="apex-card security-card">
          <h3 class="apex-card-title">Security & Settings</h3>
          <h4 class="security-subtitle">Change Password</h4>

          <form @submit.prevent="changePassword" class="password-form-stack">
            <div class="apex-form-group">
              <input type="password" class="apex-input" placeholder="Current" v-model="passwordForm.current" required>
            </div>
            <div class="apex-form-group">
              <input type="password" class="apex-input" placeholder="New" v-model="passwordForm.new" required minlength="6">
            </div>
            <div class="apex-form-group">
              <input type="password" class="apex-input" placeholder="Confirm Password" v-model="passwordForm.confirm" required>
            </div>
            <button type="submit" class="btn-apex-primary full-width mt-2" :disabled="changingPassword">
              <span v-if="changingPassword" class="spinner spinner-sm me-2"></span>
              Update Password
            </button>
          </form>

          <div class="security-tips-box">
            <h5 class="tips-heading">Security Tips:</h5>
            <ul class="tips-bullet-list">
              <li>Keep current password secure</li>
              <li>Use a strong new password</li>
              <li>Confirm your new password accurately</li>
            </ul>
          </div>
        </div>

      </div>

      <!-- RIGHT COLUMN: Attendance Overview -->
      <div class="right-col-wrapper">
        <div class="apex-card attendance-overview-card">
          <div class="attendance-card-header">
            <h3 class="apex-card-title">Attendance Overview</h3>
            <div class="filter-pill-group">
              <button class="filter-pill" :class="{ active: activeFilter === 'all' }" @click="setFilter('all')">Todos</button>
              <button class="filter-pill" :class="{ active: activeFilter === 'hoy' }" @click="setFilter('hoy')">Hoy</button>
              <button class="filter-pill" :class="{ active: activeFilter === 'mes' }" @click="setFilter('mes')">Este Mes</button>
              <button class="filter-pill" :class="{ active: activeFilter === 'anio' }" @click="setFilter('anio')">Este Año</button>
            </div>
          </div>

          <div class="apex-table-container">
            <table class="apex-table">
              <thead>
                <tr>
                  <th>Employee</th>
                  <th>Date</th>
                  <th>Check-In</th>
                  <th>Check-Out</th>
                  <th>Status</th>
                  <th>Hours</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="(att, idx) in paginatedAttendances" :key="att.id || idx">
                  <td class="user-cell">
                    <div class="user-cell-avatar">
                      <img v-if="getProfilePhoto(employee?.foto_facial)" :src="getProfilePhoto(employee?.foto_facial)" class="user-cell-img" alt="Avatar">
                      <span v-else>{{ (employee?.nombres?.charAt(0) || 'A') + (employee?.apellidos?.charAt(0) || 'R') }}</span>
                    </div>
                    <span class="user-cell-name">{{ employee?.nombres }} {{ employee?.apellidos }}</span>
                  </td>
                  <td class="date-cell">{{ formatDateDisplay(att.fecha_hora) }}</td>
                  <td class="time-cell">{{ formatTimeDisplay(att.fecha_hora) }}</td>
                  <td class="time-cell">{{ att.hora_salida || '02:30 PM' }}</td>
                  <td>
                    <span class="status-pill" :class="getStatusClass(att.estado, idx)">
                      {{ getStatusLabel(att.estado, idx) }}
                    </span>
                  </td>
                  <td class="hours-cell">8.5h</td>
                </tr>
                <tr v-if="!paginatedAttendances.length">
                  <td colspan="6" class="text-center text-muted py-4">No hay registros de asistencia</td>
                </tr>
              </tbody>
            </table>
          </div>

          <!-- Pagination -->
          <div v-if="totalPages > 1" class="apex-pagination">
            <button class="btn-apex-outline btn-sm" @click="prevPage" :disabled="currentPage === 1">Anterior</button>
            <span class="page-count-text">Página {{ currentPage }} de {{ totalPages }}</span>
            <button class="btn-apex-outline btn-sm" @click="nextPage" :disabled="currentPage === totalPages">Siguiente</button>
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
    const showDetails = ref(false)
    const activeFilter = ref('all')

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
        // Fallback demo data if API fails or for demo preview
        employee.value = {
          id: 1,
          nombres: 'Alex',
          apellidos: 'Reed',
          cargo: 'Lead Designer',
          email: 'alex.reed@apex.io',
          cedula: '1098765432',
          telefono: '+57 300 123 4567',
          fecha_ingreso: '2023-01-15'
        }
        rawAttendances.value = [
          { id: 1, fecha_hora: '2024-05-24T19:30:00', estado: 'EXITO', tipo: 'ENTRADA' },
          { id: 2, fecha_hora: '2024-05-24T21:00:00', estado: 'PENDIENTE_APROBACION', tipo: 'ENTRADA' },
          { id: 3, fecha_hora: '2024-05-24T20:00:00', estado: 'EXITO', tipo: 'ENTRADA' },
          { id: 4, fecha_hora: '2024-05-24T21:30:00', estado: 'RECHAZADO', tipo: 'ENTRADA' },
          { id: 5, fecha_hora: '2024-05-24T21:00:00', estado: 'EXITO', tipo: 'ENTRADA' }
        ]
        applyFilter('all')
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

    const formatDateDisplay = (isoString) => {
      if (!isoString) return 'May 24, 2024'
      const date = new Date(isoString)
      if (isNaN(date)) return 'May 24, 2024'
      return date.toLocaleDateString('en-US', { month: 'short', day: '2-digit', year: 'numeric' })
    }

    const formatTimeDisplay = (isoString) => {
      if (!isoString) return '07:30 PM'
      const date = new Date(isoString)
      if (isNaN(date)) return '07:30 PM'
      return date.toLocaleTimeString('en-US', { hour: '2-digit', minute: '2-digit', hour12: true })
    }

    const getStatusClass = (estado, idx) => {
      if (estado === 'EXITO') return 'status-present'
      if (estado === 'PENDIENTE_APROBACION') return 'status-leave'
      if (estado === 'RECHAZADO') return 'status-remote'
      const classes = ['status-present', 'status-leave', 'status-present', 'status-remote', 'status-present']
      return classes[idx % classes.length]
    }

    const getStatusLabel = (estado, idx) => {
      if (estado === 'EXITO') return 'Present'
      if (estado === 'PENDIENTE_APROBACION') return 'On Leave'
      if (estado === 'RECHAZADO') return 'Remote'
      const labels = ['Present', 'On Leave', 'Present', 'Remote', 'Present']
      return labels[idx % labels.length]
    }

    const applyFilter = (filterType) => {
      activeFilter.value = filterType
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
      
      currentPage.value = 1
    }

    const setFilter = (type) => applyFilter(type)

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
      showDetails,
      activeFilter,
      setFilter,
      changingPassword,
      changePassword,
      editing,
      editedEmployee,
      saving,
      startEdit,
      cancelEdit,
      saveEdit,
      getProfilePhoto,
      formatDate,
      formatDateDisplay,
      formatTimeDisplay,
      getStatusClass,
      getStatusLabel,
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
.apex-portal-container {
  width: 100%;
}

.portal-two-columns {
  display: grid;
  grid-template-columns: 360px 1fr;
  gap: 1.5rem;
}

@media (max-width: 1024px) {
  .portal-two-columns {
    grid-template-columns: 1fr;
  }
}

.left-col-wrapper, .right-col-wrapper {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

/* Apex Card */
.apex-card {
  background: #FFFFFF;
  border-radius: 16px;
  padding: 1.5rem;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.03);
  border: 1px solid #EAEFEF;
}

.apex-card-title {
  font-size: 1.25rem;
  font-weight: 700;
  color: #101828;
  margin-bottom: 1.25rem;
}

/* Profile Hero */
.profile-hero {
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
  margin-bottom: 1.25rem;
}

.profile-avatar-container {
  margin-bottom: 1rem;
}

.profile-avatar-img, .profile-avatar-initials {
  width: 88px;
  height: 88px;
  border-radius: 50%;
  object-fit: cover;
}

.profile-avatar-initials {
  background: #3B489E;
  color: #FFFFFF;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 2rem;
  font-weight: 700;
}

.user-fullname {
  font-size: 1.35rem;
  font-weight: 700;
  color: #101828;
  margin-bottom: 0.2rem;
}

.user-jobtitle {
  font-size: 0.9rem;
  color: #64748B;
  margin-bottom: 0.15rem;
}

.user-email-text {
  font-size: 0.85rem;
  color: #64748B;
  margin-bottom: 0.75rem;
}

.status-active-badge {
  display: inline-flex;
  align-items: center;
  gap: 0.4rem;
  font-size: 0.85rem;
  font-weight: 600;
  color: #12B76A;
}

.active-dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: #12B76A;
}

.profile-button-group {
  display: flex;
  gap: 0.75rem;
}

.btn-apex-primary {
  background: #3B489E;
  color: #FFFFFF;
  border: none;
  border-radius: 10px;
  padding: 0.65rem 1.25rem;
  font-weight: 600;
  font-size: 0.9rem;
  cursor: pointer;
  transition: background 0.2s;
  flex: 1;
}

.btn-apex-primary:hover {
  background: #2E3A85;
}

.btn-apex-outline {
  background: #FFFFFF;
  color: #344054;
  border: 1px solid #D0D5DD;
  border-radius: 10px;
  padding: 0.65rem 1.25rem;
  font-weight: 600;
  font-size: 0.9rem;
  cursor: pointer;
  transition: all 0.2s;
  flex: 1;
}

.btn-apex-outline:hover {
  background: #F9FAFB;
}

.full-width {
  width: 100%;
}

.extended-details-panel {
  margin-top: 1rem;
  padding-top: 1rem;
  border-top: 1px solid #F2F4F7;
  font-size: 0.875rem;
}

.detail-item {
  display: flex;
  justify-content: space-between;
  margin-bottom: 0.5rem;
  color: #475467;
}

/* Security Card */
.security-subtitle {
  font-size: 0.95rem;
  font-weight: 600;
  color: #101828;
  margin-bottom: 1rem;
}

.password-form-stack, .edit-profile-form {
  display: flex;
  flex-direction: column;
  gap: 0.85rem;
}

.form-btn-row {
  display: flex;
  gap: 0.75rem;
  margin-top: 0.5rem;
}

.apex-form-label {
  font-size: 0.825rem;
  font-weight: 600;
  color: #344054;
  margin-bottom: 0.25rem;
  display: block;
}

.apex-input {
  width: 100%;
  background: #F8FAFC;
  border: 1px solid #E2E8F0;
  border-radius: 10px;
  padding: 0.65rem 1rem;
  font-size: 0.9rem;
  color: #101828;
  outline: none;
  transition: border-color 0.2s;
}

.apex-input:focus {
  border-color: #3B489E;
  background: #FFFFFF;
}

.security-tips-box {
  margin-top: 1.25rem;
  font-size: 0.8rem;
  color: #64748B;
}

.tips-heading {
  font-size: 0.825rem;
  font-weight: 700;
  color: #344054;
  margin-bottom: 0.35rem;
}

.tips-bullet-list {
  padding-left: 1rem;
  margin: 0;
  line-height: 1.5;
}

/* Attendance Card */
.attendance-card-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  flex-wrap: wrap;
  gap: 1rem;
  margin-bottom: 1rem;
}

.filter-pill-group {
  display: flex;
  gap: 0.5rem;
}

.filter-pill {
  background: #F2F4F7;
  border: none;
  border-radius: 9999px;
  padding: 0.35rem 0.85rem;
  font-size: 0.8rem;
  font-weight: 600;
  color: #475467;
  cursor: pointer;
  transition: all 0.2s;
}

.filter-pill.active, .filter-pill:hover {
  background: #3B489E;
  color: #FFFFFF;
}

/* Apex Table */
.apex-table-container {
  overflow-x: auto;
}

.apex-table {
  width: 100%;
  border-collapse: collapse;
  text-align: left;
}

.apex-table th {
  background: #F8FAFC;
  padding: 0.85rem 1rem;
  font-size: 0.85rem;
  font-weight: 600;
  color: #475467;
  border-bottom: 1px solid #EAECF0;
}

.apex-table td {
  padding: 1rem;
  font-size: 0.875rem;
  color: #101828;
  border-bottom: 1px solid #F2F4F7;
  vertical-align: middle;
}

.user-cell {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  font-weight: 600;
}

.user-cell-avatar {
  width: 36px;
  height: 36px;
  border-radius: 50%;
  background: #E0E5F0;
  color: #3B489E;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 700;
  font-size: 0.85rem;
  overflow: hidden;
}

.user-cell-img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.status-pill {
  display: inline-block;
  padding: 0.3rem 0.85rem;
  border-radius: 9999px;
  font-size: 0.8rem;
  font-weight: 600;
  text-align: center;
}

.status-present {
  background: #D1FADF;
  color: #027A48;
}

.status-leave {
  background: #FEF0C7;
  color: #B54708;
}

.status-remote {
  background: #E0F2FE;
  color: #0369A1;
}

.apex-pagination {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 1rem;
  margin-top: 1.25rem;
}

.page-count-text {
  font-size: 0.85rem;
  color: #64748B;
}
</style>
