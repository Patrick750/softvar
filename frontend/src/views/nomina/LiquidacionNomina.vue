<template>
  <div class="container mt-4">
    <h2>Liquidación de Nómina</h2>

    <div class="row g-4 mb-4">
      <div class="col-md-6">
        <div class="card">
          <div class="card-header bg-success text-white">
            <h5 class="mb-0">Período de Liquidación</h5>
          </div>
          <div class="card-body">
            <form @submit.prevent="generarNomina" class="row g-3">
              <div class="col-md-6">
                <label for="mes" class="form-label">Mes *</label>
                <select
                  class="form-select"
                  id="mes"
                  v-model="periodo.mes"
                  required
                >
                  <option value="">Seleccione mes</option>
                  <option value="1">Enero</option>
                  <option value="2">Febrero</option>
                  <option value="3">Marzo</option>
                  <option value="4">Abril</option>
                  <option value="5">Mayo</option>
                  <option value="6">Junio</option>
                  <option value="7">Julio</option>
                  <option value="8">Agosto</option>
                  <option value="9">Septiembre</option>
                  <option value="10">Octubre</option>
                  <option value="11">Noviembre</option>
                  <option value="12">Diciembre</option>
                </select>
                <div class="invalid-feedback">Seleccione el mes</div>
              </div>

              <div class="col-md-6">
                <label for="ano" class="form-label">Año *</label>
                <input
                  type="number"
                  class="form-control"
                  id="ano"
                  v-model.number="periodo.ano"
                  required
                  min="2020"
                  max="2030"
                >
                <div class="invalid-feedback">Ingrese el año</div>
              </div>

              <div class="col-12">
                <button
                  type="submit"
                  class="btn btn-success w-100"
                >
                  Generar Liquidación
                </button>
              </div>
            </form>
          </div>
        </div>
      </div>

      <div class="col-md-6">
        <div class="card">
          <div class="card-header bg-info text-white">
            <h5 class="mb-0">Resumen de Liquidación</h5>
          </div>
          <div class="card-body">
            <div v-if="nominaGenerada">
              <div class="mb-3">
                <h6>Total Empleados: <span class="badge bg-primary">{{ resumen.totalEmpleados }}</span></h6>
                <h6>Nómina Total: <span class="badge bg-success">{{ formatoMoneda(resumen.nominaTotal) }}</span></h6>
                <h6>Devengados: <span class="badge bg-info">{{ formatoMoneda(resumen.totalDevengados) }}</span></h6>
                <h6>Deducciones: <span class="badge bg-warning">{{ formatoMoneda(resumen.totalDeducciones) }}</span></h6>
              </div>

              <div class="d-grid gap-2">
                <button
                  class="btn btn-outline-primary me-2"
                  @click="exportarExcel"
                >
                  <i class="bi bi-file-earmark-excel me-2"></i>
                  Exportar a Excel
                </button>
                <button
                  class="btn btn-outline-success"
                  @click="exportarACH"
                >
                  <i class="bi bi-bank me-2"></i>
                  Exportar ACH
                </button>
              </div>
            </div>
            <div v-else class="text-center py-4">
              <div class="spinner-border text-info" role="status">
                <span class="visually-hidden">Cargando...</span>
              </div>
              <p class="mt-3">Seleccione un período para generar la liquidación</p>
            </div>
          </div>
        </div>
      </div>
    </div>

    <div class="row">
      <div class="col-12">
        <div class="card">
          <div class="card-header bg-primary text-white">
            <h5 class="mb-0">Detalle de Liquidación por Empleado</h5>
          </div>
          <div class="card-body">
            <div v-if="nominaGenerada && detalleNomina.length">
              <div class="table-responsive">
                <table class="table table-hover align-middle">
                  <thead class="table-light">
                    <tr>
                      <th>Empleado</th>
                      <th>Cédula</th>
                      <th>Salario Base</th>
                      <th>Horas Extra Diurnas</th>
                      <th>Horas Extra Nocturnas</th>
                      <th>Devengado Total</th>
                      <th>Salud (4%)</th>
                      <th>Pensión (4%)</th>
                      <th>Deducciones Totales</th>
                      <th>Neto a Pagar</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr v-for="emp in detalleNomina" :key="emp.id">
                      <td>{{ emp.nombres }} {{ emp.apellidos }}</td>
                      <td>{{ emp.cedula }}</td>
                      <td>{{ formatoMoneda(emp.salario_base) }}</td>
                      <td>{{ formatNumber(emp.horas_extra_diurnas) }} hrs</td>
                      <td>{{ formatNumber(emp.horas_extra_nocturnas) }} hrs</td>
                      <td>{{ formatoMoneda(emp.devengado_total) }}</td>
                      <td>{{ formatoMoneda(emp.descuento_salud) }}</td>
                      <td>{{ formatoMoneda(emp.descuento_pension) }}</td>
                      <td>{{ formatoMoneda(emp.deducciones_total) }}</td>
                      <td class="fw-bold">{{ formatoMoneda(emp.neto_pagar) }}</td>
                    </tr>
                  </tbody>
                </table>
              </div>
            </div>
            <div v-else-if="nominaGenerada" class="text-center text-muted py-4">
              No hay datos para mostrar
            </div>
            <div v-else class="text-center text-muted py-4">
              Genere una liquidación para ver los detalles
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'
import { jsPDF } from 'jspdf'

export default {
  setup() {
    const periodo = ref({
      mes: '',
      ano: new Date().getFullYear()
    })

    const nominaGenerada = ref(false)
    const detalleNomina = ref([])
    const resumen = ref({
      totalEmpleados: 0,
      nominaTotal: 0,
      totalDevengados: 0,
      totalDeducciones: 0
    })

    const generarNomina = async () => {
      if (!periodo.value.mes || !periodo.value.ano) {
        alert('Por favor seleccione mes y año')
        return
      }

      try {
        // Simular llamada al API para generar nómina
        // En producción: await axios.post('/api/nomina/generar', periodo.value)

        // Simular delay
        await new Promise(resolve => setTimeout(resolve, 1500))

        // Generar datos de ejemplo
        const empleadosEjemplo = [
          {
            id: 1,
            nombres: 'Juan',
            apellidos: 'Pérez Gómez',
            cedula: '1020304050',
            cargo: 'Asistente Administrativo',
            salario_base: 2000000,
            horas_extra_diurnas: 10,
            horas_extra_nocturnas: 5
          },
          {
            id: 2,
            nombres: 'María',
            apellidos: 'López Rivera',
            cedula: '1030405060',
            cargo: 'Analista de RRHH',
            salario_base: 2800000,
            horas_extra_diurnas: 8,
            horas_extra_nocturnas: 3
          },
          {
            id: 3,
            nombres: 'Carlos',
            apellidos: 'Rodríguez Silva',
            cedula: '1040506070',
            cargo: 'Desarrollador Junior',
            salario_base: 3200000,
            horas_extra_diurnas: 12,
            horas_extra_nocturnas: 0
          }
        ]

        const detalle = empleadosEjemplo.map(emp => {
          const salarioBase = emp.salario_base
          const heDiurnasValor = emp.horas_extra_diurnas * (salarioBase / 240) * 1.25 // 25% recargo
          const heNocturnasValor = emp.horas_extra_nocturnas * (salarioBase / 240) * 1.75 // 75% recargo
          const devengadoTotal = salarioBase + heDiurnasValor + heNocturnasValor
          const descuentoSalud = devengadoTotal * 0.04
          const descuentoPension = devengadoTotal * 0.04
          const deduccionesTotal = descuentoSalud + descuentoPension
          const netoPagar = devengadoTotal - deduccionesTotal

          return {
            ...emp,
            salario_base: salarioBase,
            horas_extra_diurnas: emp.horas_extra_diurnas,
            horas_extra_nocturnas: emp.horas_extra_nocturnas,
            devengado_total: devengadoTotal,
            descuento_salud: descuentoSalud,
            descuento_pension: descuentoPension,
            deducciones_total: deduccionesTotal,
            neto_pagar: netoPagar
          }
        })

        detalleNomina.value = detalle
        nominaGenerada.value = true

        // Calcular resumen
        resumen.value.totalEmpleados = detalle.length
        resumen.value.nominaTotal = detalle.reduce((sum, emp) => sum + emp.neto_pagar, 0)
        resumen.value.totalDevengados = detalle.reduce((sum, emp) => sum + emp.devengado_total, 0)
        resumen.value.totalDeducciones = detalle.reduce((sum, emp) => sum + emp.deducciones_total, 0)

      } catch (error) {
        console.error('Error generating payroll:', error)
        alert('Error al generar la liquidación de nómina')
      }
    }

    const formatoMoneda = (valor) => {
      return new Intl.NumberFormat('es-CO', {
        style: 'currency',
        currency: 'COP'
      }).format(valor || 0)
    }

    const formatNumber = (valor) => {
      return new Intl.NumberFormat('es-CO').format(valor || 0)
    }

    const exportarExcel = () => {
      // Simular exportación a Excel
      alert('Exportando a Excel...')
      // En producción: usar una librería como SheetJS o llamar al backend
    }

    const exportarACH = () => {
      // Simular exportación ACH
      alert('Generando archivo ACH para transferencia bancaria...')
      // En producción: generar formato específico según requerimientos bancarios
    }

    onMounted(() => {
      // Inicializar con el mes actual
      periodo.value.mes = new Date().getMonth() + 1
    })

    return {
      periodo,
      nominaGenerada,
      detalleNomina,
      resumen,
      generarNomina,
      formatoMoneda,
      formatNumber,
      exportarExcel,
      exportarACH
    }
  }
}
</script>

<style scoped>
.container {
  max-width: 1400px;
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

.table {
  margin-bottom: 0;
}

.table th {
  background-color: var(--color-primary-50);
  font-weight: 600;
  color: var(--color-neutral-text-primary);
  border-color: var(--color-neutral-divider);
  text-align: center;
  font-size: 0.85rem;
}

.table td {
  vertical-align: middle;
  border-color: var(--color-neutral-divider);
  font-size: 0.85rem;
}

.table tbody tr:hover {
  background-color: var(--color-primary-50);
}

.btn {
  border-radius: 8px;
  font-weight: 500;
  transition: all 0.2s ease;
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

.btn-outline-primary {
  color: var(--color-primary-500);
  border-color: var(--color-primary-500);
}

.btn-outline-primary:hover {
  background-color: var(--color-primary-500);
  color: white;
}

.btn-outline-success {
  color: var(--color-secondary-500);
  border-color: var(--color-secondary-500);
}

.btn-outline-success:hover {
  background-color: var(--color-secondary-500);
  color: white;
}

/* Responsive design */
@media (max-width: 768px) {
  .table th,
  .table td {
    font-size: 0.75rem;
    padding: 0.5rem;
  }

  .row {
    flex-direction: column;
  }

  .col-md-6 {
    width: 100%;
    margin-bottom: 1.5rem;
  }
}
</style>