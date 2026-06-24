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
import axios from 'axios'

export default {
  setup() {
    const filtros = ref({ tipo: '', fechaInicio: '', fechaFin: '', empleadoId: '' })
    const reporteGenerado = ref(false)
    const cargando = ref(false)
    const columnas = ref([])
    const datosReporte = ref([])
    const empleados = ref([])
    const hoy = new Date().toISOString().split('T')[0]

    const fMoneda = (v) => new Intl.NumberFormat('es-CO', { style: 'currency', currency: 'COP' }).format(v)

    const generarReporte = async () => {
      if (!filtros.value.tipo || !filtros.value.fechaInicio || !filtros.value.fechaFin) return
      cargando.value = true

      try {
        const response = await axios.get('/api/reportes/generar/', {
          params: {
            tipo: filtros.value.tipo,
            fechaInicio: filtros.value.fechaInicio,
            fechaFin: filtros.value.fechaFin,
            empleadoId: filtros.value.empleadoId
          }
        })
        
        datosReporte.value = response.data

        switch (filtros.value.tipo) {
          case 'asistencia':
            columnas.value = ['Fecha', 'Empleado', 'Cédula', 'Entrada', 'Salida', 'Horas', 'Estado']
            break
          case 'nomina':
            columnas.value = ['Empleado', 'Cédula', 'Salario Base', 'Devengado', 'Deducciones', 'Neto']
            break
          case 'horas-extras':
            columnas.value = ['Empleado', 'Cédula', 'H. Diurnas', 'H. Nocturnas', 'Valor Total']
            break
          case 'ausencias':
            columnas.value = ['Empleado', 'Cédula', 'Fecha', 'Tipo', 'Justificada']
            break
        }
        reporteGenerado.value = true
      } catch (err) {
        console.error('Error generando reporte:', err)
        alert('Error generando el reporte. Por favor intente de nuevo.')
      } finally {
        cargando.value = false
      }
    }

    const exportarExcel = () => {
      if (datosReporte.value.length === 0) return
      
      let csvContent = "data:text/csv;charset=utf-8,\uFEFF"
      csvContent += columnas.value.join(",") + "\n"
      
      datosReporte.value.forEach(row => {
        let rowArray = []
        columnas.value.forEach(col => {
          let val = row[col] || ""
          if (typeof val === 'string' && val.includes(',')) {
            val = `"${val}"`
          }
          rowArray.push(val)
        })
        csvContent += rowArray.join(",") + "\n"
      })
      
      const encodedUri = encodeURI(csvContent)
      const link = document.createElement("a")
      link.setAttribute("href", encodedUri)
      link.setAttribute("download", `Reporte_${filtros.value.tipo}_${filtros.value.fechaInicio}.csv`)
      document.body.appendChild(link)
      link.click()
      document.body.removeChild(link)
    }
    
    const imprimirPDF = () => {
      window.print()
    }

    onMounted(async () => {
      try {
        const response = await axios.get('/api/empleados/')
        empleados.value = response.data.results || response.data
      } catch (error) {
        console.error('Error cargando empleados:', error)
      }
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
.data-row {
  opacity: 0;
  transform: translateY(8px);
  animation: fadeInRow 0.35s ease forwards;
  animation-delay: calc(var(--i, 0) * 60ms);
  transition: background 0.2s, transform 0.15s;
  cursor: pointer;
}
.data-row:hover { background: var(--color-primary-50); }
.data-row:active { transform: scale(0.995); }
.data-row:last-child td { border-bottom: none; }

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
.empty-cell { text-align: center; color: var(--color-neutral-text-secondary); padding: 2rem !important; }
.table-footer { padding: 0.75rem 0.85rem; font-size: 0.75rem; color: var(--color-neutral-text-secondary); border-top: 1px solid var(--color-neutral-divider); }

/* Responsive */
@media (max-width: 900px) {
  .layout-sidebar { grid-template-columns: 1fr; }
  .filters-card { position: static; }
  .page-header-content { flex-direction: column; text-align: center; }
}
</style>
