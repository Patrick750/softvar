<template>
  <div class="container mt-4">
    <h2>Reportes Filtrables</h2>
    <p class="text-muted mb-4">Genere reportes personalizados según sus necesidades</p>

    <div class="row g-4 mb-4">
      <!-- Filtros -->
      <div class="col-md-4">
        <div class="card">
          <div class="card-header bg-info text-white">
            <h5 class="mb-0">Filtros de Reporte</h5>
          </div>
          <div class="card-body">
            <form @submit.prevent="generarReporte" class="row g-3 needs-validation" novalidate>
              <div class="col-12">
                <label for="tipoReporte" class="form-label">Tipo de Reporte *</label>
                <select
                  class="form-select"
                  id="tipoReporte"
                  v-model="filtros.tipo"
                  required
                >
                  <option value="">Seleccione tipo</option>
                  <option value="asistencia">Asistencia</option>
                  <option value="nomina">Nómina</option>
                  <option value="horas-extras">Horas Extras</option>
                  <option value="ausencias">Ausencias</option>
                </select>
                <div class="invalid-feedback">Seleccione el tipo de reporte</div>
              </div>

              <div class="col-12">
                <label for="fechaInicio" class="form-label">Fecha de Inicio *</label>
                <input
                  type="date"
                  class="form-control"
                  id="fechaInicio"
                  v-model="filtros.fechaInicio"
                  required
                  :max="hoy"
                >
                <div class="invalid-feedback">Seleccione la fecha de inicio</div>
              </div>

              <div class="col-12">
                <label for="fechaFin" class="form-label">Fecha de Fin *</label>
                <input
                  type="date"
                  class="form-control"
                  id="fechaFin"
                  v-model="filtros.fechaFin"
                  required
                  :max="hoy"
                  :min="filtros.fechaInicio"
                >
                <div class="invalid-feedback">Seleccione la fecha de fin</div>
              </div>

              <div class="col-12">
                <label for="empleadoId" class="form-label">Empleado (Opcional)</label>
                <select
                  class="form-select"
                  id="empleadoId"
                  v-model="filtros.empleadoId"
                >
                  <option value="">Todos los empleados</option>
                  <option v-for="emp in empleados" :key="emp.id" :value="emp.id">
                    {{ emp.nombres }} {{ emp.apellidos }}
                  </option>
                </select>
              </div>

              <div class="col-12 d-grid">
                <button
                  type="submit"
                  class="btn btn-info"
                >
                  Generar Reporte
                </button>
              </div>
            </form>
          </div>
        </div>
      </div>

      <!-- Resultados -->
      <div class="col-md-8">
        <div class="card">
          <div class="card-header bg-success text-white d-flex justify-content-between align-items-center">
            <h5 class="mb-0">Resultado del Reporte</h5>
            <div>
              <button
                v-if="reporteGenerado"
                class="btn btn-outline-light btn-sm me-2"
                @click="exportarExcel"
              >
                <i class="bi bi-file-earmark-excel me-1"></i>
                Excel
              </button>
              <button
                v-if="reporteGenerado"
                class="btn btn-outline-light btn-sm"
                @click="imprimirPDF"
              >
                <i class="bi bi-file-earmark-pdf me-1"></i>
                PDF
              </button>
            </div>
          </div>
          <div class="card-body">
            <div v-if="cargando" class="text-center py-5">
              <div class="spinner-border text-success" role="status">
                <span class="visually-hidden">Cargando...</span>
              </div>
              <h5 class="mt-3">Generando reporte...</h5>
            </div>

            <div v-else-if="!reporteGenerado && !cargando" class="text-center py-5">
              <div class="opacity-50">
                <i class="bi bi-file-earmark-bar-graph fs-1"></i>
              </div>
              <h5 class="mt-3">Configure los filtros y genere un reporte</h5>
              <p class="text-muted">Los resultados aparecerán aquí</p>
            </div>

            <div v-else-if="reporteGenerado" class="table-responsive">
              <table class="table table-hover align-middle">
                <thead>
                  <tr>
                    <th v-for="th in columnas" :key="th">
                      {{ th }}
                    </th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="fila in datosReporte" :key="fila.id">
                    <td v-for="(valor, indice) in fila" :key="indice">
                      {{ valor }}
                    </td>
                  </tr>
                  <tr v-if="datosReporte.length === 0">
                    <td :colspan="columnas.length" class="text-center text-muted py-4">
                      No se encontraron registros para los filtros seleccionados
                    </td>
                  </tr>
                </tbody>
              </table>

              <div v-if="datosReporte.length > 0" class="mt-3">
                <small class="text-muted">
                  Mostrando {{ datosReporte.length }} registro{{ datosReporte.length !== 1 ? 's' : '' }}
                </small>
              </div>
            </div>
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
    const filtros = ref({
      tipo: '',
      fechaInicio: '',
      fechaFin: '',
      empleadoId: ''
    })

    const reporteGenerado = ref(false)
    const cargando = ref(false)
    const columnas = ref([])
    const datosReporte = ref([])
    const empleados = ref([])

    const hoy = new String(new Date().toISOString().split('T')[0])

    const generarReporte = async () => {
      if (!filtros.value.tipo || !filtros.value.fechaInicio || !filtros.value.fechaFin) {
        alert('Por favor complete los filtros obligatorios')
        return
      }

      cargando.value = true

      try {
        // Simular llamada al API
        await new Promise(resolve => setTimeout(resolve, 1500))

        // Generar datos de ejemplo según el tipo de reporte
        switch (filtros.value.tipo) {
          case 'asistencia':
            generarReporteAsistencia()
            break
          case 'nomina':
            generarReporteNomina()
            break
          case 'horas-extras':
            generarReporteHorasExtras()
            break
          case 'ausencias':
            generarReporteAusencias()
            break
          default:
            columnas.value = ['Fecha', 'Empleado', 'Cédula', 'Detalle']
            datosReporte.value = []
        }

        reporteGenerado.value = true
      } catch (error) {
        console.error('Error generating report:', error)
        alert('Error al generar el reporte')
      } finally {
        cargando.value = false
      }
    }

    const generarReporteAsistencia = () => {
      columnas.value = ['Fecha', 'Empleado', 'Cédula', 'Entrada', 'Salida', 'Horas', 'Estado', 'Observaciones']

      // Simular datos de asistencia
      const registros = []
      const fechaInicio = new Date(filtros.value.fechaInicio)
      const fechaFin = new Date(filtros.value.fechaFin)
      const diffTime = Math.abs(fechaFin - fechaInicio)
      const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24)) + 1

      for (let i = 0; i < diffDays; i++) {
        const fecha = new Date(fechaInicio.getTime() + (i * 24 * 60 * 60 * 1000))
        const fechaStr = fecha.toLocaleDateString('es-CO')

        // Simular registros para varios empleados
        const empleadosDia = empleados.value.slice(0, Math.floor(Math.random() * 5) + 1)

        empleadosDia.forEach(emp => {
          const entrada = Math.random() > 0.2 ? `${String(Math.floor(Math.random() * 2 + 7)).padStart(2, '0')}:${String(Math.floor(Math.random() * 60)).padStart(2, '0')}` : null
          const salida = entrada && Math.random() > 0.1 ? `${String(Math.floor(Math.random() * 3 + 16)).padStart(2, '0')}:${String(Math.floor(Math.random() * 60)).padStart(2, '0')}` : null
          const horas = entrada && salida ?
            ((parseInt(salida.split(':')[0]) - parseInt(entrada.split(':')[0])) +
             (parseInt(salida.split(':')[1]) - parseInt(entrada.split(':')[1])) / 60).toFixed(2) : '0'
          const estado = entrada ? (Math.random() > 0.05 ? 'EXITO' : 'FALLIDO') : 'FALTANTE'

          registros.push({
            id: Date.now() + registros.length,
            fecha: fechaStr,
            empleado: `${emp.nombres} ${emp.apellidos}`,
            cedula: emp.cedula,
            entrada: entrada || '-',
            salida: salida || '-',
            horas: horas,
            estado: estado,
            observaciones: estado === 'FALLIDO' ? 'Verificación fallida' : estado === 'FALTANTE' ? 'No registrado' : ''
          })
        })
      }

      datosReporte.value = registros
    }

    const generarReporteNomina = () => {
      columnas.value = ['Empleado', 'Cédula', 'Salario Base', 'Devengado', 'Deducciones', 'Neto a Pagar', 'Período']

      // Simular datos de nómina
      const registros = []
      empleados.value.slice(0, 8).forEach(emp => {
        const salarioBase = Math.floor(Math.random() * 3000000) + 1000000
        const devengado = salarioBase + Math.floor(Math.random() * 500000)
        const deducciones = devengado * 0.08 // salud + pensión + otros
        const neto = devengado - deducciones

        registros.push({
          id: Date.now() + registros.length,
          empleado: `${emp.nombres} ${emp.apellidos}`,
          cedula: emp.cedula,
          salarioBase: formatoMoneda(salarioBase),
          devengado: formatoMoneda(devengado),
          deducciones: formatoMoneda(deducciones),
          neto: formatoMoneda(neto),
          periodo: `${filtros.value.fechaInicio} a ${filtros.value.fechaFin}`
        })
      })

      datosReporte.value = registros
    }

    const generarReporteHorasExtras = () => {
      columnas.value = ['Empleado', 'Cédula', 'Horas Diurnas', 'Horas Nocturnas', 'Valor Diurno', 'Valor Nocturno', 'Total HE', 'Período']

      // Simular datos de horas extras
      const registros = []
      empleados.value.forEach(emp => {
        const heDiurnas = Math.floor(Math.random() * 15)
        const heNocturnas = Math.floor(Math.random() * 10)
        const salarioBase = Math.floor(Math.random() * 3000000) + 1000000
        const valorHora = salarioBase / 240
        const valorDiurno = heDiurnas * valorHora * 1.25
        const valorNocturno = heNocturnas * valorHora * 1.75
        const totalHE = valorDiurno + valorNocturno

        registros.push({
          id: Date.now() + registros.length,
          empleado: `${emp.nombres} ${emp.apellidos}`,
          cedula: emp.cedula,
          heDiurnas: heDiurnas,
          heNocturnas: heNocturnas,
          valorDiurno: formatoMoneda(valorDiurno),
          valorNocturno: formatoMoneda(valorNocturno),
          totalHE: formatoMoneda(totalHE),
          periodo: `${filtros.value.fechaInicio} a ${filtros.value.fechaFin}`
        })
      })

      datosReporte.value = registros
    }

    const generarReporteAusencias = () => {
      columnas.value = ['Empleado', 'Cédula', 'Fecha Ausencia', 'Tipo', 'Justificada', 'Días']

      // Simular datos de ausencias
      const registros = []
      const ausentes = empleados.value.filter(emp => Math.random() > 0.7)

      ausentes.forEach(emp => {
        const ausenciasCount = Math.floor(Math.random() * 5) + 1
        for (let i = 0; i < ausenciasCount; i++) {
          const fecha = new Date(
            new Date(filtros.value.fechaInicio).getTime() +
            Math.floor(Math.random() * ((new Date(filtros.value.fechaFin).getTime() - new Date(filtros.value.fechaInicio).getTime()) / (1000 * 60 * 60 * 24))) *
            (24 * 60 * 60 * 1000)
          )
          const fechaStr = fecha.toLocaleDateString('es-CO')

          registros.push({
            id: Date.now() + registros.length,
            empleado: `${emp.nombres} ${emp.apellidos}`,
            cedula: emp.cedula,
            fecha: fechaStr,
            tipo: Math.random() > 0.5 ? 'ENFERMEDAD' : 'PERSONAL',
            justificada: Math.random() > 0.3 ? 'SÍ' : 'NO',
            dias: 1
          })
        }
      })

      datosReporte.value = registros
    }

    const formatoMoneda = (valor) => {
      return new Intl.NumberFormat('es-CO', {
        style: 'currency',
        currency: 'COP'
      }).format(valor)
    }

    const exportarExcel = () => {
      alert('Exportando reporte a Excel...')
      // En producción: usar libreria como SheetJS o generar archivo en el backend
    }

    const imprimirPDF = () => {
      alert('Generando PDF del reporte...')
      // En producción: usar libreria como jsPDF o generar PDF en el backend
    }

    onMounted(() => {
      // Cargar lista de empleados (simulado)
      empleados.value = [
        { id: 1, nombres: 'Juan', apellidos: 'Pérez Gómez', cedula: '1020304050' },
        { id: 2, nombres: 'María', apellidos: 'López Rivera', cedula: '1030405060' },
        { id: 3, nombres: 'Carlos', apellidos: 'Rodríguez Silva', cedula: '1040506070' },
        { id: 4, nombres: 'Ana', apellidos: 'González Martínez', cedula: '1050607080' },
        { id: 5, nombres: 'Luis', apellidos: 'Torres Díaz', cedula: '1060708090' },
        { id: 6, nombres: 'Patricia', apellidos: 'Ramírez Castillo', cedula: '1070809010' },
        { id: 7, nombres: 'Diego', apellidos: 'Vargas Ortega', cedula: '1080901020' },
        { id: 8, nombres: 'Claudia', apellidos: 'Herrera Muñoz', cedula: '1090102030' }
      ]
    })

    return {
      filtros,
      reporteGenerado,
      cargando,
      columnas,
      datosReporte,
      generarReporte,
      exportarExcel,
      imprimirPDF,
      hoy,
      formatoMoneda
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
}

.card-header {
  border-radius: 12px 12px 0 0 !important;
  padding: 1rem 1.5rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
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

.btn-info {
  background: var(--color-primary-500);
  border-color: var(--color-primary-500);
}

.btn-info:hover {
  background: var(--color-primary-700);
  border-color: var(--color-primary-700);
  transform: translateY(-2px);
}

.btn-outline-light {
  color: white;
  border-color: white;
}

.btn-outline-light:hover {
  background-color: rgba(255, 255, 255, 0.1);
  color: white;
}

.table {
  margin-bottom: 0;
}

.table th {
  background-color: var(--color-primary-50);
  font-weight: 600;
  color: var(--color-neutral-text-primary);
  border-color: var(--color-neutral-divider);
}

.table td {
  vertical-align: middle;
  border-color: var(--color-neutral-divider);
}

.badge {
  font-weight: 500;
  padding: 0.35em 0.65em;
  font-size: 0.85rem;
}

@media (max-width: 768px) {
  .row {
    flex-direction: column;
  }

  .col-md-4,
  .col-md-8 {
    width: 100%;
    margin-bottom: 1.5rem;
  }

  .card-body {
    padding: 1rem;
  }
}
</style>