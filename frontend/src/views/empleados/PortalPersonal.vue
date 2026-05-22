<template>
  <div class="container mt-4">
    <h2>Portal Personal</h2>
    <div class="row g-4">
      <div class="col-md-4">
        <div class="card">
          <div class="card-header bg-primary text-white">
            <h5 class="mb-0">Mi Información</h5>
          </div>
          <div class="card-body text-center">
            <div class="avatar-container mb-3">
              <img
                v-if="employee.foto_facial"
                :src="employee.foto_facial"
                alt="Mi Foto"
                class="avatar-img-lg"
              >
              <div v-else class="avatar-placeholder-lg">
                {{ employee.nombres.charAt(0) }}{{ employee.apellidos.charAt(0) }}
              </div>
            </div>
            <h4>{{ employee.nombres }} {{ employee.apellidos }}</h4>
            <p class="text-muted">{{ employee.cargo }}</p>
            <p><strong>Cédula:</strong> {{ employee.cedula }}</p>
            <p><strong>Email:</strong> {{ employee.email }}</p>
          </div>
        </div>
      </div>

      <div class="col-md-8">
        <div class="row g-4">
          <div class="col-md-6">
            <div class="card">
              <div class="card-header bg-success text-white">
                <h5 class="mb-0">Mis Asistencias</h5>
              </div>
              <div class="card-body">
                <div class="mb-3">
                  <button class="btn btn-outline-success me-2" @click="filtrarHoy">
                    Hoy
                  </button>
                  <button class="btn btn-outline-success me-2" @click="filtrarMes">
                    Este Mes
                  </button>
                  <button class="btn btn-outline-success" @click="filtrarAnio">
                    Este Año
                  </button>
                </div>
                <div class="table-responsive">
                  <table class="table table-hover align-middle">
                    <thead>
                      <tr>
                        <th>Fecha</th>
                        <th>Entrada</th>
                        <th>Salida</th>
                        <th>Horas</th>
                        <th>Estado</th>
                      </tr>
                    </thead>
                    <tbody>
                      <tr v-for="att in attendances" :key="att.id">
                        <td>{{ att.fecha }}</td>
                        <td>{{ att.entrada || '-' }}</td>
                        <td>{{ att.salida || '-' }}</td>
                        <td>{{ att.horas }}h</td>
                        <td>
                          <span v-if="att.estado === 'EXITO'" class="badge bg-success">Exitosa</span>
                          <span v-else class="badge bg-danger">Fallida</span>
                        </td>
                      </tr>
                      <tr v-if="!attendances.length">
                        <td colspan="5" class="text-center text-muted">No hay registros</td>
                      </tr>
                    </tbody>
                  </table>
                </div>
              </div>
            </div>
          </div>

          <div class="col-md-6">
            <div class="card">
              <div class="card-header bg-info text-white">
                <h5 class="mb-0">Solicitudes Pendientes</h5>
              </div>
              <div class="card-body">
                <div v-if="pendingRequests.length" class="list-group">
                  <div v-for="req in pendingRequests" :key="req.id" class="list-group-item">
                    <div class="d-flex w-100 justify-content-between">
                      <h6 class="mb-1">{{ req.tipo }}</h6>
                      <small class="text-muted">{{ req.fecha }}</small>
                    </div>
                    <p class="mb-1">{{ req.descripcion }}</p>
                    <div class="d-flex justify-content-between">
                      <small>{{ req.estado }}</small>
                      <div>
                        <button v-if="req.estado === 'PENDIENTE'" class="btn btn-sm btn-outline-success me-1" @click="aprobarSolicitud(req.id)">
                          Aprobar
                        </button>
                        <button v-if="req.estado === 'PENDIENTE'" class="btn btn-sm btn-outline-danger" @click="rechazarSolicitud(req.id)">
                          Rechazar
                        </button>
                      </div>
                    </div>
                  </div>
                </div>
                <div v-else class="text-center text-muted py-3">
                  No tienes solicitudes pendientes
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <div class="mt-4">
      <div class="card">
        <div class="card-header bg-warning text-white">
          <h5 class="mb-0">Cambiar Contraseña</h5>
        </div>
        <div class="card-body">
          <form @submit.prevent="changePassword" class="row g-3 needs-validation" novalidate>
            <div class="col-md-4">
              <label for="currentPassword" class="form-label">Contraseña Actual *</label>
              <input
                type="password"
                class="form-control"
                id="currentPassword"
                v-model="passwordForm.current"
                required
              >
              <div class="invalid-feedback">Ingrese su contraseña actual</div>
            </div>

            <div class="col-md-4">
              <label for="newPassword" class="form-label">Nueva Contraseña *</label>
              <input
                type="password"
                class="form-control"
                id="newPassword"
                v-model="passwordForm.new"
                required
                minlength="6"
              >
              <div class="invalid-feedback">La contraseña debe tener al menos 6 caracteres</div>
            </div>

            <div class="col-md-4">
              <label for="confirmPassword" class="form-label">Confirmar Contraseña *</label>
              <input
                type="password"
                class="form-control"
                id="confirmPassword"
                v-model="passwordForm.confirm"
                required
              >
              <div class="invalid-feedback">Confirme su nueva contraseña</div>
            </div>

            <div class="col-12">
              <button
                type="submit"
                class="btn btn-warning"
              >
                Cambiar Contraseña
              </button>
            </div>
          </form>
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
      id: 1,
      nombres: 'María',
      apellidos: 'González Silva',
      cedula: '0987654321',
      cargo: 'Analista de RRHH',
      email: 'maria.gonzalez@empresa.com',
      foto_facial: null,
      salario_base: 2800000,
      activo: true
    })

    const attendances = ref([
      {
        id: 1,
        fecha: '20/05/2026',
        entrada: '08:00 AM',
        salida: '05:00 PM',
        horas: 9,
        estado: 'EXITO'
      },
      {
        id: 2,
        fecha: '19/05/2026',
        entrada: '08:05 AM',
        salida: '04:55 PM',
        horas: 8.5,
        estado: 'EXITO'
      }
    ])

    const pendingRequests = ref([
      {
        id: 1,
        tipo: 'Solicitud de Licencia',
        descripcion: 'Licencia médica por 3 días del 25 al 27 de mayo',
        fecha: '18/05/2026',
        estado: 'PENDIENTE'
      }
    ])

    const passwordForm = ref({
      current: '',
      new: '',
      confirm: ''
    })

    const filtrarHoy = () => {
      // Filtrar asistencias del día de hoy
      console.log('Filtrando asistencias de hoy')
    }

    const filtrarMes = () => {
      // Filtrar asistencias del mes actual
      console.log('Filtrando asistencias del mes')
    }

    const filtrarAnio = () => {
      // Filtrar asistencias del año actual
      console.log('Filtrando asistencias del año')
    }

    const aprobarSolicitud = (id) => {
      const index = pendingRequests.value.findIndex(r => r.id === id)
      if (index !== -1) {
        pendingRequests.value[index].estado = 'APROBADO'
      }
    }

    const rechazarSolicitud = (id) => {
      const index = pendingRequests.value.findIndex(r => r.id === id)
      if (index !== -1) {
        pendingRequests.value[index].estado = 'RECHAZADO'
      }
    }

    const changePassword = () => {
      if (passwordForm.value.new !== passwordForm.value.confirm) {
        alert('Las contraseñas no coinciden')
        return
      }
      // Aquí iría la llamada al API para cambiar la contraseña
      alert('Contraseña cambiada exitosamente')
      passwordForm.value.current = ''
      passwordForm.value.new = ''
      passwordForm.value.confirm = ''
    }

    onMounted(() => {
      // En una app real, cargar datos del empleado desde auth context
      console.log('Portal personal cargado')
    })

    return {
      employee,
      attendances,
      pendingRequests,
      passwordForm,
      changePassword
    }
  }
}
</script>

<style scoped>
.container {
  max-width: 1400px;
}

.avatar-img-lg {
  width: 120px;
  height: 120px;
  object-fit: cover;
  border-radius: 50%;
  border: 4px solid var(--color-primary-50);
  margin: 0 auto;
  display: block;
}

.avatar-placeholder-lg {
  width: 120px;
  height: 120px;
  background: var(--color-primary-200);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: bold;
  font-size: 2.5rem;
  color: var(--color-primary-700);
  border: 4px solid var(--color-primary-50);
  margin: 0 auto;
  display: block;
}

.card {
  border: none;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
  margin-bottom: 1.5rem;
}

.card-header {
  border-radius: 12px 12px 0 0 !important;
  padding: 1rem;
}

.table th {
  background-color: var(--color-primary-50);
  font-weight: 600;
  color: var(--color-neutral-text-primary);
}

.table td {
  vertical-align: middle;
}

.btn-outline-success {
  color: var(--color-secondary-700);
  border-color: var(--color-secondary-700);
}

.btn-outline-success:hover {
  background-color: var(--color-secondary-700);
  color: white;
}

.btn-outline-danger {
  color: var(--color-semantic-error-accent);
  border-color: var(--color-semantic-error-accent);
}

.btn-outline-danger:hover {
  background-color: var(--color-semantic-error-accent);
  color: white;
}

.btn-warning {
  background: var(--color-secondary-500);
  border-color: var(--color-secondary-500);
}

.btn-warning:hover {
  background: var(--color-secondary-700);
  border-color: var(--color-secondary-700);
  transform: translateY(-2px);
}

/* Responsive design */
@media (max-width: 768px) {
  .row {
    flex-direction: column;
  }

  .col-md-4,
  .col-md-6,
  .col-md-8 {
    width: 100%;
    margin-bottom: 1.5rem;
  }
}
</style>