<template>
  <div class="page-container">
    <div class="page-header">
      <div class="page-header-content">
        <div class="page-header-icon">
          <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <rect x="2" y="3" width="20" height="14" rx="2" ry="2"/>
            <line x1="8" y1="21" x2="16" y2="21"/>
            <line x1="12" y1="17" x2="12" y2="21"/>
          </svg>
        </div>
        <div>
          <h1 class="page-title">Liquidación de Nómina</h1>
          <p class="page-description">Gestione la liquidación de nómina por período</p>
        </div>
      </div>
    </div>

    <div class="grid-2">
      <!-- Período de Liquidación -->
      <div class="card card-success">
        <div class="card-header">
          <div class="card-header-left">
            <span class="card-icon">
              <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <rect x="3" y="4" width="18" height="18" rx="2" ry="2"/>
                <line x1="16" y1="2" x2="16" y2="6"/>
                <line x1="8" y1="2" x2="8" y2="6"/>
                <line x1="3" y1="10" x2="21" y2="10"/>
              </svg>
            </span>
            <h3>Período de Liquidación</h3>
          </div>
        </div>
        <div class="card-body">
          <form @submit.prevent="generarNomina" class="form-grid">
            <div class="form-group">
              <label for="mes" class="form-label">Mes <span class="required">*</span></label>
              <div class="select-wrapper">
                <select id="mes" v-model="periodo.mes" required class="form-select">
                  <option value="">Seleccione mes</option>
                  <option v-for="(name, key) in meses" :key="key" :value="key">{{ name }}</option>
                </select>
                <svg class="select-chevron" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="6 9 12 15 18 9"/></svg>
              </div>
            </div>
            <div class="form-group">
              <label for="ano" class="form-label">Año <span class="required">*</span></label>
              <input type="number" id="ano" v-model.number="periodo.ano" required min="2020" max="2030" class="form-input">
            </div>
            <div class="form-group full-width">
              <button type="submit" class="btn btn-primary btn-block" :disabled="generando">
                <span v-if="generando" class="spinner"></span>
                <svg v-else width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="9 11 12 14 22 4"/><path d="M21 12v7a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h11"/></svg>
                Generar Liquidación
              </button>
            </div>
          </form>
        </div>
      </div>

      <!-- Resumen de Liquidación -->
      <div class="card card-info">
        <div class="card-header">
          <div class="card-header-left">
            <span class="card-icon">
              <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <line x1="12" y1="1" x2="12" y2="23"/><path d="M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6"/>
              </svg>
            </span>
            <h3>Resumen de Liquidación</h3>
          </div>
        </div>
        <div class="card-body">
          <div v-if="nominaGenerada" class="summary-stats">
            <div class="summary-item">
              <span class="summary-label">Total Empleados</span>
              <span class="summary-value">{{ resumen.totalEmpleados }}</span>
            </div>
            <div class="summary-item">
              <span class="summary-label">Nómina Total</span>
              <span class="summary-value accent-success">{{ formatoMoneda(resumen.nominaTotal) }}</span>
            </div>
            <div class="summary-item">
              <span class="summary-label">Devengados</span>
              <span class="summary-value accent-info">{{ formatoMoneda(resumen.totalDevengados) }}</span>
            </div>
            <div class="summary-item">
              <span class="summary-label">Deducciones</span>
              <span class="summary-value accent-warning">{{ formatoMoneda(resumen.totalDeducciones) }}</span>
            </div>
            <div class="summary-actions">
              <button class="btn btn-outline btn-excel" @click="exportarExcel">
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/><line x1="8" y1="13" x2="16" y2="13"/><line x1="8" y1="17" x2="16" y2="17"/></svg>
                Exportar a Excel
              </button>
              <button class="btn btn-outline btn-ach" @click="enviarDesprendibles">
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="2" y="3" width="20" height="14" rx="2" ry="2"/><line x1="8" y1="21" x2="16" y2="21"/><line x1="12" y1="17" x2="12" y2="21"/></svg>
                Enviar Desprendibles
              </button>
            </div>
          </div>
          <div v-else class="empty-state">
            <svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="var(--color-neutral-border)" stroke-width="1.5"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></svg>
            <p>Seleccione un período y genere la liquidación</p>
          </div>
        </div>
      </div>
    </div>

    <!-- Detalle de Liquidación -->
    <div class="card">
      <div class="card-header">
        <div class="card-header-left">
          <span class="card-icon">
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/><line x1="16" y1="13" x2="8" y2="13"/><line x1="16" y1="17" x2="8" y2="17"/><polyline points="10 9 9 9 8 9"/>
            </svg>
          </span>
          <h3>Detalle de Liquidación por Empleado</h3>
        </div>
        <span v-if="nominaGenerada" class="badge badge-info">{{ periodoLabel }}</span>
      </div>
      <div class="card-body p-0">
        <div v-if="nominaGenerada && detalleNomina.length" class="table-wrapper">
          <table class="data-table">
            <thead>
              <tr>
                <th>Empleado</th>
                <th>Cédula</th>
                <th class="text-right">Salario Base</th>
                <th class="text-right">HE Diurnas</th>
                <th class="text-right">HE Nocturnas</th>
                <th class="text-right">Devengado</th>
                <th class="text-right">Salud (4%)</th>
                <th class="text-right">Pensión (4%)</th>
                <th class="text-right">Deducciones</th>
                <th class="text-right">Neto a Pagar</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="(emp, idx) in detalleNomina" :key="emp.id" class="data-row" :style="{ '--i': idx }">
                <td><span class="employee-name">{{ emp.nombres }} {{ emp.apellidos }}</span></td>
                <td class="text-muted">{{ emp.cedula }}</td>
                <td class="text-right">{{ formatoMoneda(emp.salario_base) }}</td>
                <td class="text-right">{{ formatNumber(emp.horas_extra_diurnas) }} <small class="text-muted">hrs</small></td>
                <td class="text-right">{{ formatNumber(emp.horas_extra_nocturnas) }} <small class="text-muted">hrs</small></td>
                <td class="text-right">{{ formatoMoneda(emp.devengado_total) }}</td>
                <td class="text-right">{{ formatoMoneda(emp.descuento_salud) }}</td>
                <td class="text-right">{{ formatoMoneda(emp.descuento_pension) }}</td>
                <td class="text-right">{{ formatoMoneda(emp.deducciones_total) }}</td>
                <td class="text-right net-pay">{{ formatoMoneda(emp.neto_pagar) }}</td>
              </tr>
            </tbody>
          </table>
        </div>
        <div v-else class="empty-state">
          <svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="var(--color-neutral-border)" stroke-width="1.5"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/><line x1="16" y1="13" x2="8" y2="13"/><line x1="16" y1="17" x2="8" y2="17"/></svg>
          <p>Genere una liquidación para ver los detalles</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, computed, onMounted } from 'vue'
import axios from 'axios'

export default {
  setup() {
    const meses = {
      1: 'Enero', 2: 'Febrero', 3: 'Marzo', 4: 'Abril',
      5: 'Mayo', 6: 'Junio', 7: 'Julio', 8: 'Agosto',
      9: 'Septiembre', 10: 'Octubre', 11: 'Noviembre', 12: 'Diciembre'
    }

    const periodo = ref({ mes: '', ano: new Date().getFullYear() })
    const nominaGenerada = ref(false)
    const generando = ref(false)
    const detalleNomina = ref([])
    const resumen = ref({ totalEmpleados: 0, nominaTotal: 0, totalDevengados: 0, totalDeducciones: 0 })
    const nominaId = ref(null)

    const periodoLabel = computed(() => `${meses[periodo.value.mes] || ''} ${periodo.value.ano}`)

    const generarNomina = async () => {
      if (!periodo.value.mes || !periodo.value.ano) return
      generando.value = true

      try {
        const response = await axios.post('/api/nomina/generar/', {
          mes: periodo.value.mes,
          ano: periodo.value.ano,
          novedades: {} // En el futuro se puede añadir una interfaz para esto
        })

        const nomina = response.data
        nominaId.value = nomina.id
        detalleNomina.value = nomina.detalles || []

        nominaGenerada.value = true
        resumen.value = {
          totalEmpleados: detalleNomina.value.length,
          nominaTotal: parseFloat(nomina.total_nomina),
          totalDevengados: parseFloat(nomina.total_devengados),
          totalDeducciones: parseFloat(nomina.total_deducciones)
        }
      } catch (err) {
        console.error('Error:', err)
        alert(err.response?.data?.message || 'Error al generar la nómina.')
      } finally {
        generando.value = false
      }
    }

    const formatoMoneda = (v) => new Intl.NumberFormat('es-CO', { style: 'currency', currency: 'COP' }).format(v || 0)
    const formatNumber = (v) => new Intl.NumberFormat('es-CO').format(v || 0)

    const exportarExcel = () => alert('Exportando a Excel...')
    const enviarDesprendibles = async () => {
      if (!nominaId.value) return
      try {
        const res = await axios.post(`/api/nomina/${nominaId.value}/enviar-desprendibles/`)
        alert(res.data.message || 'Desprendibles enviados.')
      } catch (e) {
        alert('Error enviando desprendibles.')
      }
    }

    onMounted(() => { periodo.value.mes = String(new Date().getMonth() + 1) })

    return { meses, periodo, nominaGenerada, generando, detalleNomina, resumen, periodoLabel, generarNomina, formatoMoneda, formatNumber, exportarExcel, enviarDesprendibles }
  }
}
</script>

<style scoped>
/* Page structure */
.page-container {
  max-width: 1400px;
  width: 100%;
  margin: 0 auto;
  box-sizing: border-box;
}

.page-header {
  margin-bottom: 2rem;
}

.page-header-content {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.page-header-icon {
  width: 44px;
  height: 44px;
  background: var(--color-primary-50);
  color: var(--color-primary-700);
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.page-title {
  font-family: 'Young Serif', Georgia, serif;
  font-size: 1.5rem;
  color: var(--color-neutral-text-primary);
  margin: 0;
}

.page-description {
  color: var(--color-neutral-text-secondary);
  margin: 0.15rem 0 0 0;
  font-size: 0.875rem;
}

/* Grid layout */
.grid-2 {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 1.5rem;
  margin-bottom: 1.5rem;
  width: 100%;
}

@media (max-width: 900px) {
  .grid-2 { grid-template-columns: 1fr; }
}

/* Cards */
.card {
  background: white;
  border: 1px solid var(--color-neutral-divider);
  border-radius: 12px;
  overflow: hidden;
  width: 100%;
  max-width: 100%;
}

.card-success { border-top: 3px solid var(--color-secondary-700); }
.card-info { border-top: 3px solid var(--color-primary-500); }

.card-header {
  padding: 1rem 1.5rem;
  border-bottom: 1px solid var(--color-neutral-divider);
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.card-header-left {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.card-icon {
  width: 32px;
  height: 32px;
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
}

.card-success .card-icon { background: var(--color-secondary-700); }
.card-info .card-icon { background: var(--color-primary-500); }

.card-header h3 {
  font-family: 'Young Serif', Georgia, serif;
  font-size: 1rem;
  margin: 0;
  color: var(--color-neutral-text-primary);
}

.card-body {
  padding: 1.5rem;
}

.card-body.p-0 { padding: 0; }

/* Form elements */
.form-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1rem;
}

.form-group { display: flex; flex-direction: column; gap: 0.35rem; }
.form-group.full-width { grid-column: 1 / -1; }

.form-label {
  font-size: 0.8rem;
  font-weight: 600;
  color: var(--color-neutral-text-secondary);
  text-transform: uppercase;
  letter-spacing: 0.03em;
}

.required { color: var(--color-error-accent); }

.form-input, .form-select {
  width: 100%;
  padding: 0.65rem 0.85rem;
  border: 1px solid var(--color-neutral-border);
  border-radius: 8px;
  font-size: 0.9rem;
  color: var(--color-neutral-text-primary);
  background: white;
  transition: border-color 0.2s, box-shadow 0.2s;
  font-family: inherit;
}

.form-input:focus, .form-select:focus {
  outline: none;
  border-color: var(--color-primary-500);
  box-shadow: 0 0 0 3px rgba(55, 138, 222, 0.15);
}

.select-wrapper { position: relative; }

.select-chevron {
  position: absolute;
  right: 10px;
  top: 50%;
  transform: translateY(-50%);
  pointer-events: none;
  color: var(--color-neutral-text-secondary);
}

.form-select { appearance: none; padding-right: 2rem; }

/* Buttons */
.btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  padding: 0.65rem 1.25rem;
  border: none;
  border-radius: 8px;
  font-size: 0.875rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;
  font-family: inherit;
}

.btn:disabled { opacity: 0.6; cursor: not-allowed; }

.btn-primary {
  background: var(--color-primary-700);
  color: white;
}

.btn-primary:hover:not(:disabled) {
  background: var(--color-primary-900);
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(24, 95, 165, 0.3);
}

.btn-block { width: 100%; }

.btn-outline {
  background: transparent;
  border: 1px solid var(--color-neutral-border);
  color: var(--color-neutral-text-secondary);
}

.btn-outline:hover {
  border-color: var(--color-primary-500);
  color: var(--color-primary-700);
  background: var(--color-primary-50);
}

.btn-excel:hover { border-color: var(--color-secondary-500); color: var(--color-secondary-700); background: var(--color-secondary-50); }
.btn-ach:hover { border-color: var(--color-primary-500); color: var(--color-primary-700); background: var(--color-primary-50); }

/* Summary stats */
.summary-stats {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 1rem;
}

.summary-item {
  background: var(--color-neutral-bg-page);
  border-radius: 8px;
  padding: 1rem;
  display: flex;
  flex-direction: column;
  gap: 0.35rem;
}

.summary-label {
  font-size: 0.75rem;
  font-weight: 600;
  color: var(--color-neutral-text-secondary);
  text-transform: uppercase;
  letter-spacing: 0.04em;
}

.summary-value {
  font-size: 1.25rem;
  font-weight: 700;
  color: var(--color-neutral-text-primary);
}

.summary-value.accent-success { color: var(--color-secondary-700); }
.summary-value.accent-info { color: var(--color-primary-500); }
.summary-value.accent-warning { color: var(--color-warning-accent); }

.summary-actions {
  grid-column: 1 / -1;
  display: flex;
  gap: 0.75rem;
  margin-top: 0.5rem;
}

.summary-actions .btn { flex: 1; }

/* Empty state */
.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.75rem;
  padding: 3rem;
  color: var(--color-neutral-text-secondary);
}

.empty-state p { margin: 0; font-size: 0.9rem; }

/* Badge */
.badge {
  display: inline-flex;
  align-items: center;
  padding: 0.25rem 0.75rem;
  border-radius: 20px;
  font-size: 0.75rem;
  font-weight: 600;
}

.badge-info {
  background: var(--color-info-bg);
  color: var(--color-info-accent);
}

/* Data table */
.table-wrapper {
  overflow-x: auto;
  width: 100%;
  max-width: 100%;
}

.data-table {
  width: 100%;
  border-collapse: collapse;
}

.data-table th {
  background: var(--color-neutral-bg-page);
  padding: 0.85rem 1rem;
  font-size: 0.75rem;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  color: var(--color-neutral-text-secondary);
  border-bottom: 2px solid var(--color-neutral-divider);
  white-space: nowrap;
}

.data-table td {
  padding: 0.85rem 1rem;
  font-size: 0.875rem;
  color: var(--color-neutral-text-primary);
  border-bottom: 1px solid var(--color-neutral-divider);
  white-space: nowrap;
}

.data-row {
  opacity: 0;
  transform: translateY(8px);
  animation: fadeInRow 0.35s ease forwards;
  animation-delay: calc(var(--i, 0) * 60ms);
  transition: background 0.2s, transform 0.15s;
  cursor: pointer;
}

.data-row:hover {
  background: var(--color-primary-50);
}

.data-row:active {
  transform: scale(0.995);
}

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

.text-right { text-align: right; }
.text-muted { color: var(--color-neutral-text-secondary); }

.employee-name {
  font-weight: 600;
  color: var(--color-neutral-text-primary);
}

.net-pay {
  font-weight: 700;
  color: var(--color-secondary-700);
}

/* Spinner */
.spinner {
  width: 16px;
  height: 16px;
  border: 2px solid rgba(255,255,255,0.3);
  border-top-color: white;
  border-radius: 50%;
  animation: spin 0.6s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

/* Responsive */
@media (max-width: 768px) {
  .card-body { padding: 1rem; }
  .form-grid { grid-template-columns: 1fr; }
  .summary-stats { grid-template-columns: 1fr; }
  .summary-actions { flex-direction: column; }
  .data-table th, .data-table td { padding: 0.65rem 0.5rem; font-size: 0.75rem; }
}
</style>
