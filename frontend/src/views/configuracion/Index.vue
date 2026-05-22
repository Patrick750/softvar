<template>
  <div class="container mt-4">
    <h2>Configuración del Sistema</h2>
    <p class="text-muted mb-4">Administre los parámetros del sistema de nómina y seguridad</p>

    <div class="row g-4">
      <!-- SMMLV Configuration -->
      <div class="col-md-6">
        <div class="card">
          <div class="card-header bg-success text-white">
            <h5 class="mb-0">Parametrización SMMLV</h5>
          </div>
          <div class="card-body">
            <form @submit.prevent="actualizarSMMLV" class="row g-3 needs-validation" novalidate>
              <div class="col-md-6">
                <label for="smmlv" class="form-label">SMMLV *</label>
                <input
                  type="number"
                  class="form-control"
                  id="smmlv"
                  v-model.number="config.smmlv"
                  required
                  min="0"
                >
                <div class="invalid-feedback">Ingrese el valor del SMMLV</div>
              </div>

              <div class="col-md-6">
                <label for="fechaVigencia" class="form-label">Fecha de Vigencia *</label>
                <input
                  type="date"
                  class="form-control"
                  id="fechaVigencia"
                  v-model="config.fechaVigencia"
                  required
                >
                <div class="invalid-feedback">Seleccione la fecha de vigencia</div>
              </div>

              <div class="col-12">
                <label for="observaciones" class="form-label">Observaciones</label>
                <textarea
                  class="form-control"
                  id="observaciones"
                  rows="3"
                  v-model="config.observaciones"
                ></textarea>
              </div>

              <div class="col-12 d-grid">
                <button
                  type="submit"
                  class="btn btn-success"
                >
                  Actualizar Configuración
                </button>
              </div>
            </form>

            <div v-if="configActualizada" class="alert alert-success mt-3">
              Configuración actualizada exitosamente el {{ ultimaActualizacion }}
            </div>
          </div>
        </div>
      </div>

      <!-- Contribution Rates -->
      <div class="col-md-6">
        <div class="card">
          <div class="card-header bg-info text-white">
            <h5 class="mb-0">Porcentajes de Aportes y Deducciones</h5>
          </div>
          <div class="card-body">
            <form @submit.prevent="actualizarPorcentajes" class="row g-3 needs-validation" novalidate>
              <div class="col-md-4">
                <label for="salud" class="form-label">Salud (%) *</label>
                <input
                  type="number"
                  class="form-control"
                  id="salud"
                  v-model.number="porcentajes.salud"
                  required
                  min="0"
                  max="100"
                  step="0.01"
                >
                <div class="invalid-feedback">Ingrese el porcentaje de salud</div>
              </div>

              <div class="col-md-4">
                <label for="pension" class="form-label">Pensión (%) *</label>
                <input
                  type="number"
                  class="form-control"
                  id="pension"
                  v-model.number="porcentajes.pension"
                  required
                  min="0"
                  max="100"
                  step="0.01"
                >
                <div class="invalid-feedback">Ingrese el porcentaje de pensión</div>
              </div>

              <div class="col-md-4">
                <label for="arl" class="form-label">ARL (%) *</label>
                <input
                  type="number"
                  class="form-control"
                  id="arl"
                  v-model.number="porcentajes.arl"
                  required
                  min="0"
                  max="100"
                  step="0.01"
                >
                <div class="invalid-feedback">Ingrese el porcentaje de ARL</div>
              </div>

              <div class="col-12 d-grid">
                <button
                  type="submit"
                  class="btn btn-info"
                >
                  Actualizar Porcentajes
                </button>
              </div>
            </form>

            <div v-if="porcentajesActualizados" class="alert alert-info mt-3">
              Porcentajes actualizados exitosamente
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Role-Based Access Summary -->
    <div class="row g-4 mt-4">
      <div class="col-12">
        <div class="card">
          <div class="card-header bg-warning text-white">
            <h5 class="mb-0">Resumen de Control de Acceso por Rol</h5>
          </div>
          <div class="card-body">
            <div class="table-responsive">
              <table class="table table-hover align-middle">
                <thead class="table-light">
                  <tr>
                    <th>Rol</th>
                    <th>Módulos Accesibles</th>
                    <th>Color UI</th>
                  </tr>
                </thead>
                <tbody>
                  <tr>
                    <td><span class="badge bg-primary">Administrador RRHH</span></td>
                    <td>Gestión de empleados, Desprendibles, Credenciales, Aprobación manual</td>
                    <td><span class="badge bg-primary" style="background: #185FA5 !important; color: white;">#185FA5</span></td>
                  </tr>
                  <tr>
                    <td><span class="badge bg-success">Empleado</span></td>
                    <td>Registro de asistencia, Portal personal</td>
                    <td><span class="badge bg-success" style="background: #378ADD !important; color: white;">#378ADD</span></td>
                  </tr>
                  <tr>
                    <td><span class="badge bg-info">Contador</span></td>
                    <td>Liquidación de nómina, Exportación ACH/Excel</td>
                    <td><span class="badge bg-info" style="background: #3B6D11 !important; color: white;">#3B6D11</span></td>
                  </tr>
                  <tr>
                    <td><span class="badge bg-danger">Gerente</span></td>
                    <td>Dashboard de reportes, Reportes filtrables</td>
                    <td><span class="badge bg-danger" style="background: #042C53 !important; color: white;">#042C53</span></td>
                  </tr>
                  <tr>
                    <td><span class="badge bg-secondary">Administrador Sistema</span></td>
                    <td>Auditoría de cambios, Parametrización SMMLV, Control de acceso</td>
                    <td><span class="badge bg-secondary" style="background: #2C2C2A !important; color: white;">#2C2C2A</span></td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref } from 'vue'

export default {
  setup() {
    const config = ref({
      smmlv: 1160000, // Valor SMMLV 2024 en Colombia
      fechaVigencia: '2024-01-01',
      observaciones: 'Valor legalmente establecido para el año 2024'
    })

    const porcentajes = ref({
      salud: 4.0,
      pension: 4.0,
      arl: 0.5 // ARL varía según riesgo, promedio bajo
    })

    const configActualizada = ref(false)
    const porcentajesActualizados = ref(false)
    const ultimaActualizacion = ref('')

    const actualizarSMMLV = () => {
      configActualizada.value = true
      ultimaActualizacion.value = new Date().toLocaleString()

      // En producción: enviar al API para actualizar en base de datos
      // await axios.put('/api/configuracion/smmlv', config.value)

      alert('Configuración SMMLV actualizada en el sistema')
    }

    const actualizarPorcentajes = () => {
      porcentajesActualizados.value = true

      // En producción: enviar al API para actualizar en base de datos
      // await axios.put('/api/configuracion/porcentajes', porcentajes.value)

      alert('Porcentajes actualizados en el sistema')
    }

    return {
      config,
      porcentajes,
      configActualizada,
      porcentajesActualizados,
      ultimaActualizacion,
      actualizarSMMLV,
      actualizarPorcentajes
    }
  }
}
</script>

<style scoped>
.container {
  max-width: 1000px;
}

.card {
  border: none;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
}

.card-header {
  border-radius: 12px 12px 0 0 !important;
  padding: 1rem 1.5rem;
}

.card-header h5 {
  margin: 0;
  font-size: 1.1rem;
  font-weight: 600;
}

.card-body {
  padding: 1.5rem;
}

.form-control {
  border-radius: 8px;
  border: 1px solid var(--color-neutral-border);
}

.form-control:focus {
  border-color: var(--color-primary-500);
  box-shadow: 0 0 0 0.25rem rgba(55, 138, 171, 0.25);
}

.form-select {
  border-radius: 8px;
  border: 1px solid var(--color-neutral-border);
}

.form-select:focus {
  border-color: var(--color-primary-500);
  box-shadow: 0 0 0 0.25rem rgba(55, 138, 171, 0.25);
}

.btn-success {
  background: var(--color-secondary-700);
  border-color: var(--color-secondary-700);
}

.btn-success:hover {
  background: var(--color-secondary-900);
  border-color: var(--color-secondary-900);
  transform: translateY(-2px);
}

.btn-info {
  background: var(--color-primary-500);
  border-color: var(--color-primary-500);
}

.btn-info:hover {
  background: var(--color-primary-700);
  border-color: var(--color-primary-700);
  transform: translateY(-2px);
}

.alert {
  border: none;
  border-radius: 8px;
  padding: 1rem;
  margin: 1rem 0;
}

.badge {
  font-weight: 500;
  padding: 0.35em 0.65em;
  font-size: 0.85rem;
}

/* Responsive design */
@media (max-width: 768px) {
  .row {
    flex-direction: column;
  }

  .col-md-6 {
    width: 100%;
    margin-bottom: 1.5rem;
  }

  .card-body {
    padding: 1rem;
  }
}
</style>