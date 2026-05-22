<template>
  <div class="page-container">
    <div class="page-header">
      <div class="page-header-content">
        <div class="page-header-icon">
          <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <polygon points="22 3 2 3 10 12.46 10 19 14 21 14 12.46 22 3"/>
          </svg>
        </div>
        <div>
          <h1 class="page-title">Reportes Filtrables</h1>
          <p class="page-description">Genere reportes personalizados según sus necesidades</p>
        </div>
      </div>
    </div>

    <div class="layout-sidebar">
      <!-- Filters Panel -->
      <div class="card filters-card">
        <div class="card-header">
          <div class="card-header-left">
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polygon points="22 3 2 3 10 12.46 10 19 14 21 14 12.46 22 3"/></svg>
            <h3>Filtros</h3>
          </div>
        </div>
        <div class="card-body">
          <form @submit.prevent="generarReporte" class="filters-form">
            <div class="form-group">
              <label class="form-label">Tipo de Reporte <span class="required">*</span></label>
              <div class="select-wrapper">
                <select v-model="filtros.tipo" required class="form-select">
                  <option value="">Seleccione tipo</option>
                  <option value="asistencia">Asistencia</option>
                  <option value="nomina">Nómina</option>
                  <option value="horas-extras">Horas Extras</option>
                  <option value="ausencias">Ausencias</option>
                </select>
                <svg class="select-chevron" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="6 9 12 15 18 9"/></svg>
              </div>
            </div>

            <div class="form-group">
              <label class="form-label">Fecha Inicio <span class="required">*</span></label>
              <input type="date" v-model="filtros.fechaInicio" required :max="hoy" class="form-input">
            </div>

            <div class="form-group">
              <label class="form-label">Fecha Fin <span class="required">*</span></label>
              <input type="date" v-model="filtros.fechaFin" required :max="hoy" :min="filtros.fechaInicio" class="form-input">
            </div>

            <div class="form-group">
              <label class="form-label">Empleado</label>
              <div class="select-wrapper">
                <select v-model="filtros.empleadoId" class="form-select">
                  <option value="">Todos los empleados</option>
                  <option v-for="emp in empleados" :key="emp.id" :value="emp.id">{{ emp.nombres }} {{ emp.apellidos }}</option>
                </select>
                <svg class="select-chevron" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="6 9 12 15 18 9"/></svg>
              </div>
            </div>

            <button type="submit" class="btn btn-primary btn-block" :disabled="cargando">
              <span v-if="cargando" class="spinner"></span>
              <svg v-else width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polygon points="22 3 2 3 10 12.46 10 19 14 21 14 12.46 22 3"/></svg>
              Generar Reporte
            </button>
          </form>
        </div>
      </div>

      <!-- Results Panel -->
      <div class="card results-card">
        <div class="card-header">
          <div class="card-header-left">
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/><line x1="16" y1="13" x2="8" y2="13"/><line x1="16" y1="17" x2="8" y2="17"/></svg>
            <h3>Resultado del Reporte</h3>
          </div>
          <div class="card-header-actions" v-if="reporteGenerado">
            <button class="btn btn-sm btn-outline" @click="exportarExcel">
              <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/><line x1="8" y1="13" x2="16" y2="13"/><line x1="8" y1="17" x2="16" y2="17"/></svg>
              Excel
            </button>
            <button class="btn btn-sm btn-outline" @click="imprimirPDF">
              <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/><line x1="16" y1="13" x2="8" y2="13"/><line x1="16" y1="17" x2="8" y2="17"/></svg>
              PDF
            </button>
          </div>
        </div>
        <div class="card-body">
          <!-- Loading -->
          <div v-if="cargando" class="loading-state">
            <div class="spinner-lg"></div>
            <p>Generando reporte...</p>
          </div>

          <!-- Empty -->
          <div v-else-if="!reporteGenerado" class="empty-state">
            <svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="var(--color-neutral-border)" stroke-width="1.5"><polygon points="22 3 2 3 10 12.46 10 19 14 21 14 12.46 22 3"/></svg>
            <h4>Configure los filtros</h4>
            <p>Seleccione tipo de reporte, rango de fechas y genere</p>
          </div>

          <!-- Results Table -->
          <div v-else class="table-wrapper">
            <table class="data-table">
              <thead>
                <tr>
                  <th v-for="th in columnas" :key="th">{{ th }}</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="(fila, idx) in datosReporte" :key="idx" class="data-row">
                  <td v-for="(valor, key) in fila" :key="key" v-if="key !== 'id'">{{ valor }}</td>
                </tr>
                <tr v-if="datosReporte.length === 0">
                  <td :colspan="columnas.length" class="empty-cell">No se encontraron registros</td>
                </tr>
              </tbody>
            </table>
            <div v-if="datosReporte.length > 0" class="table-footer">
              <span>{{ datosReporte.length }} registro{{ datosReporte.length !== 1 ? 's' : '' }}</span>
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
    const filtros = ref({ tipo: '', fechaInicio: '', fechaFin: '', empleadoId: '' })
    const reporteGenerado = ref(false)
    const cargando = ref(false)
    const columnas = ref([])
    const datosReporte = ref([])
    const empleados = ref([])
    const hoy = new Date().toISOString().split('T')[0]

    const generarReporte = async () => {
      if (!filtros.value.tipo || !filtros.value.fechaInicio || !filtros.value.fechaFin) return
      cargando.value = true

      try {
        await new Promise(resolve => setTimeout(resolve, 1200))

        switch (filtros.value.tipo) {
          case 'asistencia':
            columnas.value = ['Fecha', 'Empleado', 'Cédula', 'Entrada', 'Salida', 'Horas', 'Estado']
            datosReporte.value = generarAsistencia()
            break
          case 'nomina':
            columnas.value = ['Empleado', 'Cédula', 'Salario Base', 'Devengado', 'Deducciones', 'Neto']
            datosReporte.value = generarNomina()
            break
          case 'horas-extras':
            columnas.value = ['Empleado', 'Cédula', 'H. Diurnas', 'H. Nocturnas', 'Valor Total']
            datosReporte.value = generarHorasExtras()
            break
          case 'ausencias':
            columnas.value = ['Empleado', 'Cédula', 'Fecha', 'Tipo', 'Justificada']
            datosReporte.value = generarAusencias()
            break
        }
        reporteGenerado.value = true
      } catch (err) {
        console.error('Error:', err)
      } finally {
        cargando.value = false
      }
    }

    const fMoneda = (v) => new Intl.NumberFormat('es-CO', { style: 'currency', currency: 'COP' }).format(v)

    const generarAsistencia = () => {
      const start = new Date(filtros.value.fechaInicio)
      const end = new Date(filtros.value.fechaFin)
      const days = Math.ceil((end - start) / (1000 * 60 * 60 * 24)) + 1
      const data = []
      for (let i = 0; i < Math.min(days, 15); i++) {
        const d = new Date(start.getTime() + i * 86400000)
        const ds = d.toLocaleDateString('es-CO')
        empleados.value.slice(0, 3).forEach(emp => {
          const ok = Math.random() > 0.2
          const hIn = ok ? `${String(7 + Math.floor(Math.random() * 2)).padStart(2, '0')}:${String(Math.floor(Math.random() * 60)).padStart(2, '0')}` : '-'
          const hOut = ok ? `${String(16 + Math.floor(Math.random() * 3)).padStart(2, '0')}:${String(Math.floor(Math.random() * 60)).padStart(2, '0')}` : '-'
          const hrs = ok ? ((parseInt(hOut.split(':')[0]) - parseInt(hIn.split(':')[0])) + (parseInt(hOut.split(':')[1]) - parseInt(hIn.split(':')[1])) / 60).toFixed(1) : '0'
          const estado = ok ? (Math.random() > 0.05 ? 'Registrado' : 'Fallido') : 'Faltante'
          data.push({ id: data.length + 1, fecha: ds, empleado: `${emp.nombres} ${emp.apellidos}`, cedula: emp.cedula, entrada: hIn, salida: hOut, horas: hrs, estado })
        })
      }
      return data
    }

    const generarNomina = () => {
      return empleados.value.slice(0, 8).map(emp => {
        const sb = Math.floor(Math.random() * 3000000) + 1300000
        const dev = sb + Math.floor(Math.random() * 500000)
        const ded = dev * 0.08
        return { id: Date.now() + Math.random(), empleado: `${emp.nombres} ${emp.apellidos}`, cedula: emp.cedula, salario: fMoneda(sb), devengado: fMoneda(dev), deducciones: fMoneda(ded), neto: fMoneda(dev - ded) }
      })
    }

    const generarHorasExtras = () => {
      return empleados.value.slice(0, 6).map(emp => {
        const heD = Math.floor(Math.random() * 15)
        const heN = Math.floor(Math.random() * 8)
        const sb = Math.floor(Math.random() * 3000000) + 1300000
        const vh = sb / 240
        const total = heD * vh * 1.25 + heN * vh * 1.75
        return { id: Date.now() + Math.random(), empleado: `${emp.nombres} ${emp.apellidos}`, cedula: emp.cedula, hd: heD, hn: heN, total: fMoneda(total) }
      })
    }

    const generarAusencias = () => {
      return empleados.value.filter(() => Math.random() > 0.6).map(emp => {
        const fecha = new Date(new Date(filtros.value.fechaInicio).getTime() + Math.floor(Math.random() * ((new Date(filtros.value.fechaFin).getTime() - new Date(filtros.value.fechaInicio).getTime()) / 86400000)) * 86400000)
        return { id: Date.now() + Math.random(), empleado: `${emp.nombres} ${emp.apellidos}`, cedula: emp.cedula, fecha: fecha.toLocaleDateString('es-CO'), tipo: Math.random() > 0.5 ? 'Enfermedad' : 'Personal', justificada: Math.random() > 0.3 ? 'Sí' : 'No' }
      })
    }

    const exportarExcel = () => alert('Exportando reporte a Excel...')
    const imprimirPDF = () => alert('Generando PDF del reporte...')

    onMounted(() => {
      empleados.value = [
        { id: 1, nombres: 'Juan', apellidos: 'Pérez Gómez', cedula: '1020304050' },
        { id: 2, nombres: 'María', apellidos: 'López Rivera', cedula: '1030405060' },
        { id: 3, nombres: 'Carlos', apellidos: 'Rodríguez Silva', cedula: '1040506070' },
        { id: 4, nombres: 'Ana', apellidos: 'González Martínez', cedula: '1050607080' },
        { id: 5, nombres: 'Luis', apellidos: 'Torres Díaz', cedula: '1060708090' },
        { id: 6, nombres: 'Patricia', apellidos: 'Ramírez Castillo', cedula: '1070809010' }
      ]
    })

    return { filtros, reporteGenerado, cargando, columnas, datosReporte, empleados, hoy, generarReporte, exportarExcel, imprimirPDF }
  }
}
</script>

<style scoped>
.page-container { max-width: 1400px; margin: 0 auto; }

.page-header { margin-bottom: 2rem; }
.page-header-content { display: flex; align-items: center; gap: 1rem; }
.page-header-icon { width: 44px; height: 44px; background: var(--color-primary-50); color: var(--color-primary-700); border-radius: 12px; display: flex; align-items: center; justify-content: center; flex-shrink: 0; }
.page-title { font-family: 'Young Serif', Georgia, serif; font-size: 1.5rem; color: var(--color-neutral-text-primary); margin: 0; }
.page-description { color: var(--color-neutral-text-secondary); margin: 0.15rem 0 0 0; font-size: 0.875rem; }

/* Sidebar Layout */
.layout-sidebar { display: grid; grid-template-columns: 320px 1fr; gap: 1.5rem; align-items: start; }

.card { background: white; border: 1px solid var(--color-neutral-divider); border-radius: 12px; overflow: hidden; }

.card-header { padding: 1rem 1.25rem; border-bottom: 1px solid var(--color-neutral-divider); display: flex; align-items: center; justify-content: space-between; gap: 0.75rem; }
.card-header-left { display: flex; align-items: center; gap: 0.5rem; color: var(--color-neutral-text-secondary); }
.card-header-left h3 { font-family: 'Young Serif', Georgia, serif; font-size: 0.9rem; margin: 0; color: var(--color-neutral-text-primary); }

.card-header-actions { display: flex; gap: 0.4rem; }

.card-body { padding: 1.25rem; }

/* Filters */
.filters-card { position: sticky; top: 1rem; }
.filters-form { display: flex; flex-direction: column; gap: 1rem; }

.form-group { display: flex; flex-direction: column; gap: 0.35rem; }
.form-label { font-size: 0.75rem; font-weight: 600; color: var(--color-neutral-text-secondary); text-transform: uppercase; letter-spacing: 0.03em; }
.required { color: var(--color-error-accent); }

.form-input, .form-select { width: 100%; padding: 0.6rem 0.8rem; border: 1px solid var(--color-neutral-border); border-radius: 8px; font-size: 0.875rem; color: var(--color-neutral-text-primary); background: white; transition: border-color 0.2s, box-shadow 0.2s; font-family: inherit; box-sizing: border-box; }
.form-input:focus, .form-select:focus { outline: none; border-color: var(--color-primary-500); box-shadow: 0 0 0 3px rgba(55, 138, 222, 0.15); }

.select-wrapper { position: relative; }
.select-chevron { position: absolute; right: 10px; top: 50%; transform: translateY(-50%); pointer-events: none; color: var(--color-neutral-text-secondary); }
.form-select { appearance: none; padding-right: 2rem; }

/* Buttons */
.btn { display: inline-flex; align-items: center; justify-content: center; gap: 0.4rem; padding: 0.6rem 1rem; border: none; border-radius: 8px; font-size: 0.8rem; font-weight: 600; cursor: pointer; transition: all 0.2s; font-family: inherit; }
.btn:disabled { opacity: 0.6; cursor: not-allowed; }
.btn-sm { padding: 0.4rem 0.75rem; font-size: 0.75rem; }

.btn-primary { background: var(--color-primary-700); color: white; }
.btn-primary:hover:not(:disabled) { background: var(--color-primary-900); transform: translateY(-1px); box-shadow: 0 4px 12px rgba(24, 95, 165, 0.3); }
.btn-block { width: 100%; }

.btn-outline { background: transparent; border: 1px solid var(--color-neutral-border); color: var(--color-neutral-text-secondary); }
.btn-outline:hover { border-color: var(--color-primary-500); color: var(--color-primary-700); background: var(--color-primary-50); }

/* Loading */
.loading-state, .empty-state { display: flex; flex-direction: column; align-items: center; gap: 0.75rem; padding: 3rem; color: var(--color-neutral-text-secondary); text-align: center; }
.loading-state p, .empty-state p { margin: 0; font-size: 0.9rem; }
.empty-state h4 { margin: 0; font-size: 1rem; color: var(--color-neutral-text-primary); }

.spinner-lg { width: 32px; height: 32px; border: 3px solid var(--color-neutral-divider); border-top-color: var(--color-primary-500); border-radius: 50%; animation: spin 0.7s linear infinite; }
.spinner { width: 16px; height: 16px; border: 2px solid rgba(255,255,255,0.3); border-top-color: white; border-radius: 50%; animation: spin 0.6s linear infinite; }
@keyframes spin { to { transform: rotate(360deg); } }

/* Table */
.table-wrapper { overflow-x: auto; }
.data-table { width: 100%; border-collapse: collapse; }
.data-table th { background: var(--color-neutral-bg-page); padding: 0.75rem 0.85rem; font-size: 0.72rem; font-weight: 600; text-transform: uppercase; letter-spacing: 0.05em; color: var(--color-neutral-text-secondary); border-bottom: 2px solid var(--color-neutral-divider); white-space: nowrap; }
.data-table td { padding: 0.7rem 0.85rem; font-size: 0.825rem; color: var(--color-neutral-text-primary); border-bottom: 1px solid var(--color-neutral-divider); }
.data-row { transition: background 0.15s; }
.data-row:hover { background: var(--color-primary-50); }
.data-row:last-child td { border-bottom: none; }
.empty-cell { text-align: center; color: var(--color-neutral-text-secondary); padding: 2rem !important; }
.table-footer { padding: 0.75rem 0.85rem; font-size: 0.75rem; color: var(--color-neutral-text-secondary); border-top: 1px solid var(--color-neutral-divider); }

/* Responsive */
@media (max-width: 900px) {
  .layout-sidebar { grid-template-columns: 1fr; }
  .filters-card { position: static; }
  .page-header-content { flex-direction: column; text-align: center; }
}
</style>
