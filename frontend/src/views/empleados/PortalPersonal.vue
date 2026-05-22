<template>
  <div>
    <div class="page-header">
      <h1 class="display-heading">Portal Personal</h1>
      <p class="text-muted">Bienvenido, {{ employee.nombres }}</p>
    </div>

    <div class="layout-grid grid-2">
      <!-- Profile card -->
      <div class="card card-elevated p-0">
        <div class="card-header-primary">
          <h5><i class="bi bi-person-circle me-2"></i>Mi Información</h5>
        </div>
        <div class="card-body text-center">
          <div class="avatar-container mb-3">
            <img v-if="employee.foto_facial" :src="employee.foto_facial" alt="Mi Foto" class="avatar avatar-xl avatar-placeholder">
            <div v-else class="avatar avatar-xl avatar-placeholder">
              {{ (employee.nombres?.charAt(0) || '') + (employee.apellidos?.charAt(0) || '') }}
            </div>
          </div>
          <h4 class="fw-bold mb-1">{{ employee.nombres }} {{ employee.apellidos }}</h4>
          <p class="text-muted mb-3">{{ employee.cargo }}</p>
          <div class="divider"></div>
          <div class="info-grid">
            <div><span class="text-muted">Cédula:</span> <span class="fw-semibold">{{ employee.cedula }}</span></div>
            <div class="mt-2"><span class="text-muted">Email:</span> <span class="fw-semibold">{{ employee.email }}</span></div>
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
              <button class="btn btn-sm btn-outline-success" @click="filtrarHoy">Hoy</button>
              <button class="btn btn-sm btn-outline-success" @click="filtrarMes">Este Mes</button>
              <button class="btn btn-sm btn-outline-success" @click="filtrarAnio">Este Año</button>
            </div>
            <div class="table-container">
              <table class="table table-compact">
                <thead>
                  <tr><th>Fecha</th><th>Entrada</th><th>Salida</th><th>Horas</th><th>Estado</th></tr>
                </thead>
                <tbody>
                  <tr v-for="att in attendances" :key="att.id">
                    <td>{{ att.fecha }}</td>
                    <td>{{ att.entrada || '-' }}</td>
                    <td>{{ att.salida || '-' }}</td>
                    <td>{{ att.horas }}h</td>
                    <td>
                      <span v-if="att.estado === 'EXITO'" class="badge badge-success">Exitosa</span>
                      <span v-else class="badge badge-error">Fallida</span>
                    </td>
                  </tr>
                  <tr v-if="!attendances.length">
                    <td colspan="5" class="text-center text-muted py-4">No hay registros</td>
                  </tr>
                </tbody>
              </table>
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
                <button type="submit" class="btn btn-warning">
                  <i class="bi bi-shield-lock me-2"></i>
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
import { ref, onMounted } from 'vue'

export default {
  setup() {
    const employee = ref({
      id: 1, nombres: 'María', apellidos: 'González Silva',
      cedula: '0987654321', cargo: 'Analista de RRHH',
      email: 'maria.gonzalez@empresa.com', foto_facial: null,
      salario_base: 2800000, activo: true
    })

    const attendances = ref([
      { id: 1, fecha: '20/05/2026', entrada: '08:00 AM', salida: '05:00 PM', horas: 9, estado: 'EXITO' },
      { id: 2, fecha: '19/05/2026', entrada: '08:05 AM', salida: '04:55 PM', horas: 8.5, estado: 'EXITO' }
    ])

    const passwordForm = ref({ current: '', new: '', confirm: '' })

    const filtrarHoy = () => {}
    const filtrarMes = () => {}
    const filtrarAnio = () => {}

    const changePassword = () => {
      if (passwordForm.value.new !== passwordForm.value.confirm) {
        alert('Las contraseñas no coinciden')
        return
      }
      alert('Contraseña cambiada exitosamente')
      passwordForm.value = { current: '', new: '', confirm: '' }
    }

    return { employee, attendances, passwordForm, changePassword, filtrarHoy, filtrarMes, filtrarAnio }
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

@media (max-width: 768px) {
  .layout-grid { grid-template-columns: 1fr; }
}
</style>
