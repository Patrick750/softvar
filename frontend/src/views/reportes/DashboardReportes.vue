<template>
  <div class="page-container">
    <div class="page-header">
      <div class="page-header-content">
        <div class="page-header-icon">
          <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <line x1="18" y1="20" x2="18" y2="10"/><line x1="12" y1="20" x2="12" y2="4"/><line x1="6" y1="20" x2="6" y2="14"/>
          </svg>
        </div>
        <div>
          <h1 class="page-title">Dashboard de Reportes</h1>
          <p class="page-description">Métricas clave de asistencia y nómina de su empresa</p>
        </div>
      </div>
      <button class="btn btn-refresh" @click="cargarDatos" :disabled="cargando" title="Actualizar datos">
        <span v-if="cargando" class="spinner spinner-sm"></span>
        <svg v-else width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="1 4 1 10 7 10"/><path d="M3.51 15a9 9 0 1 0 2.13-9.36L1 10"/></svg>
        Actualizar
      </button>
    </div>

    <!-- Loading State -->
    <div v-if="cargando && !datosCargados" class="loading-dashboard">
      <div class="spinner-lg"></div>
      <p>Cargando datos del dashboard...</p>
    </div>

    <!-- Error State -->
    <div v-else-if="error" class="error-state-card">
      <svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="var(--color-error-accent)" stroke-width="1.5"><circle cx="12" cy="12" r="10"/><line x1="12" y1="8" x2="12" y2="12"/><line x1="12" y1="16" x2="12.01" y2="16"/></svg>
      <h3>Error al cargar datos</h3>
      <p>{{ error }}</p>
      <button class="btn btn-primary" @click="cargarDatos">Reintentar</button>
    </div>

    <!-- Dashboard Content -->
    <template v-if="datosCargados">
      <!-- KPI Cards -->
      <div class="kpi-grid">
        <div class="kpi-card kpi-primary">
          <div class="kpi-icon"><svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M16 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/><circle cx="8.5" cy="7" r="4"/><polyline points="17 11 19 13 23 9"/></svg></div>
          <div class="kpi-body">
            <span class="kpi-label">Empleados Activos</span>
            <span class="kpi-value">{{ metrics.activeEmployees }}</span>
            <span class="kpi-trend positive">{{ metrics.activeEmployees > 0 ? 'Incluye todos los roles' : 'Sin datos' }}</span>
          </div>
        </div>

        <div class="kpi-card kpi-success">
          <div class="kpi-icon"><svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"/><polyline points="22 4 12 14.01 9 11.01"/></svg></div>
          <div class="kpi-body">
            <span class="kpi-label">Asistencia Promedio</span>
            <span class="kpi-value">{{ metrics.attendanceRate }}<small>%</small></span>
            <span class="kpi-trend positive" v-if="ultimoMes">{{ ultimoMes }}</span>
          </div>
        </div>

        <div class="kpi-card kpi-warning">
          <div class="kpi-icon"><svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><path d="M12 6v6l4 2"/></svg></div>
          <div class="kpi-body">
            <span class="kpi-label">Horas Extras Totales</span>
            <span class="kpi-value">{{ formatHours(metrics.totalOvertimeHours) }}</span>
            <span class="kpi-trend neutral" v-if="ultimoMes">Último mes: {{ ultimoMes }}</span>
          </div>
        </div>

        <div class="kpi-card kpi-info">
          <div class="kpi-icon"><svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="12" y1="1" x2="12" y2="23"/><path d="M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6"/></svg></div>
          <div class="kpi-body">
            <span class="kpi-label">Costo Nómina Mensual</span>
            <span class="kpi-value">{{ formatCurrency(metrics.monthlyPayrollCost) }}</span>
            <span class="kpi-trend neutral" v-if="ultimoMes">{{ ultimoMes }}</span>
          </div>
        </div>
      </div>

      <!-- Charts Row 1 -->
      <div class="chart-grid">
        <div class="card">
          <div class="card-header">
            <div class="card-header-left">
              <span class="card-dot" style="background: var(--color-primary-700);"></span>
              <h3>Días Trabajados vs Ausencias</h3>
            </div>
            <span class="card-badge">Últimos 6 meses</span>
          </div>
          <div class="card-body chart-body">
            <div class="chart-container">
              <canvas id="workDaysChart"></canvas>
            </div>
          </div>
        </div>

        <div class="card">
          <div class="card-header">
            <div class="card-header-left">
              <span class="card-dot" style="background: var(--color-secondary-700);"></span>
              <h3>Horas Extras y Costo Nómina</h3>
            </div>
            <span class="card-badge">Últimos 6 meses</span>
          </div>
          <div class="card-body chart-body">
            <div class="chart-container">
              <canvas id="overtimeCostChart"></canvas>
            </div>
          </div>
        </div>
      </div>

      <!-- Charts Row 2 -->
      <div class="chart-grid">
        <div class="card">
          <div class="card-header">
            <div class="card-header-left">
              <span class="card-dot" style="background: var(--color-primary-500);"></span>
              <h3>Distribución por Cargo</h3>
            </div>
          </div>
          <div class="card-body chart-body">
            <div class="chart-container">
              <canvas id="deptChart"></canvas>
            </div>
          </div>
        </div>

        <div class="card">
          <div class="card-header">
            <div class="card-header-left">
              <span class="card-dot" style="background: var(--color-warning-accent);"></span>
              <h3>Top — Horas Extras</h3>
            </div>
          </div>
          <div class="card-body chart-body">
            <div v-if="topOvertimeEmployees.length === 0" class="empty-chart">
              <svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="var(--color-neutral-border)" stroke-width="1.5"><circle cx="12" cy="12" r="10"/><path d="M12 6v6l4 2"/></svg>
              <p>Sin horas extras este mes</p>
            </div>
            <div v-else class="chart-container">
              <canvas id="topOvertimeChart"></canvas>
            </div>
          </div>
        </div>
      </div>
    </template>
  </div>
</template>

<script>
import { ref, onMounted, onUnmounted } from 'vue'
import axios from 'axios'
import { Chart, registerables } from 'chart.js'

Chart.register(...registerables)

export default {
  name: 'DashboardReportes',
  setup() {
    const cargando = ref(true)
    const datosCargados = ref(false)
    const error = ref('')
    const ultimoMes = ref('')

    const metrics = ref({
      activeEmployees: 0,
      attendanceRate: 0,
      totalOvertimeHours: 0,
      monthlyPayrollCost: 0,
    })

    let monthlyData = ref([])
    let topOvertimeEmployees = ref([])
    let departmentData = ref([])

    let chartInstances = {}

    const formatCurrency = (v) => {
      if (!v && v !== 0) return '$0'
      return new Intl.NumberFormat('es-CO', { style: 'currency', currency: 'COP', minimumFractionDigits: 0 }).format(v)
    }

    const formatHours = (v) => {
      if (!v && v !== 0) return '0 hrs'
      return new Intl.NumberFormat('es-CO', { minimumFractionDigits: 1, maximumFractionDigits: 1 }).format(v) + ' hrs'
    }

    const destruirGraficos = () => {
      Object.values(chartInstances).forEach(c => { if (c) c.destroy() })
      chartInstances = {}
    }

    const renderizarGraficos = () => {
      destruirGraficos()
      if (!monthlyData.value || monthlyData.value.length === 0) return

      const labels = monthlyData.value.map(m => m.mes)
      const diasTrabajados = monthlyData.value.map(m => m.dias_trabajados)
      const ausencias = monthlyData.value.map(m => m.ausencias)
      const horasExtras = monthlyData.value.map(m => m.horas_extras)
      const costoNomina = monthlyData.value.map(m => m.costo_nomina / 1000000)

      const commonOpts = (id) => {
        const canvas = document.getElementById(id)
        if (!canvas) return null
        return canvas
      }

      // Chart 1: Días Trabajados vs Ausencias
      const wCtx = commonOpts('workDaysChart')
      if (wCtx) {
        chartInstances.workDays = new Chart(wCtx, {
          type: 'bar',
          data: {
            labels,
            datasets: [
              { label: 'Días Trabajados', data: diasTrabajados, backgroundColor: 'rgba(24, 95, 165, 0.8)', borderColor: '#185FA5', borderWidth: 1, borderRadius: 4 },
              { label: 'Ausencias', data: ausencias, backgroundColor: 'rgba(163, 45, 45, 0.7)', borderColor: '#A32D2D', borderWidth: 1, borderRadius: 4 }
            ]
          },
          options: {
            responsive: true, maintainAspectRatio: false,
            plugins: {
              legend: { position: 'top', labels: { boxWidth: 12, usePointStyle: true, padding: 15, font: { family: "'Work Sans', sans-serif", size: 11 } } }
            },
            scales: {
              y: { beginAtZero: true, grid: { color: 'rgba(0,0,0,0.04)' }, ticks: { font: { family: "'Work Sans', sans-serif", size: 11 } } },
              x: { grid: { display: false }, ticks: { font: { family: "'Work Sans', sans-serif", size: 11 } } }
            }
          }
        })
      }

      // Chart 2: Horas Extras y Costo Nómina
      const oCtx = commonOpts('overtimeCostChart')
      if (oCtx) {
        chartInstances.overtime = new Chart(oCtx, {
          type: 'line',
          data: {
            labels,
            datasets: [
              { label: 'Horas Extras', data: horasExtras, borderColor: '#3B6D11', backgroundColor: 'transparent', tension: 0.4, pointBackgroundColor: '#3B6D11', pointRadius: 4, pointHoverRadius: 6, yAxisID: 'y' },
              { label: 'Costo Nómina (Millones COP)', data: costoNomina, borderColor: '#185FA5', backgroundColor: 'transparent', tension: 0.4, pointBackgroundColor: '#185FA5', pointRadius: 4, pointHoverRadius: 6, yAxisID: 'y1' }
            ]
          },
          options: {
            responsive: true, maintainAspectRatio: false,
            interaction: { intersect: false, mode: 'index' },
            plugins: {
              legend: { position: 'top', labels: { boxWidth: 12, usePointStyle: true, padding: 15, font: { family: "'Work Sans', sans-serif", size: 11 } } }
            },
            scales: {
              y: { type: 'linear', position: 'left', title: { display: true, text: 'Horas', font: { family: "'Work Sans', sans-serif", size: 11 } }, grid: { drawOnChartArea: false }, ticks: { font: { family: "'Work Sans', sans-serif", size: 11 } } },
              y1: { type: 'linear', position: 'right', title: { display: true, text: 'Millones COP', font: { family: "'Work Sans', sans-serif", size: 11 } }, grid: { drawOnChartArea: false }, ticks: { font: { family: "'Work Sans', sans-serif", size: 11 } } },
              x: { grid: { display: false }, ticks: { font: { family: "'Work Sans', sans-serif", size: 11 } } }
            }
          }
        })
      }

      // Chart 3: Distribución por Cargo (Doughnut)
      const dCtx = commonOpts('deptChart')
      if (dCtx && departmentData.value.length > 0) {
        const colors = ['rgba(24, 95, 165, 0.85)', 'rgba(99, 153, 34, 0.85)', 'rgba(55, 138, 222, 0.7)', 'rgba(181, 212, 244, 0.9)', 'rgba(44, 62, 80, 0.7)', 'rgba(192, 221, 151, 0.8)', 'rgba(163, 45, 45, 0.6)']
        chartInstances.dept = new Chart(dCtx, {
          type: 'doughnut',
          data: {
            labels: departmentData.value.map(d => d.cargo),
            datasets: [{
              data: departmentData.value.map(d => d.empleados),
              backgroundColor: colors.slice(0, departmentData.value.length),
              borderColor: 'white',
              borderWidth: 3,
              hoverOffset: 8
            }]
          },
          options: {
            responsive: true, maintainAspectRatio: false,
            cutout: '60%',
            plugins: {
              legend: { position: 'right', labels: { boxWidth: 12, padding: 12, font: { family: "'Work Sans', sans-serif", size: 11 }, usePointStyle: true } },
              tooltip: {
                callbacks: {
                  label: function(ctx) {
                    const total = ctx.dataset.data.reduce((a, b) => a + b, 0)
                    return ctx.label + ': ' + ctx.parsed + ' (' + ((ctx.parsed / total) * 100).toFixed(1) + '%)'
                  }
                }
              }
            }
          }
        })
      }

      // Chart 4: Top Horas Extras (Horizontal Bar)
      const tCtx = commonOpts('topOvertimeChart')
      if (tCtx && topOvertimeEmployees.value.length > 0) {
        chartInstances.topOvertime = new Chart(tCtx, {
          type: 'bar',
          data: {
            labels: topOvertimeEmployees.value.map(e => e.nombre.split(' ').slice(0, 2).join(' ')),
            datasets: [{
              label: 'Horas Extras',
              data: topOvertimeEmployees.value.map(e => e.horas_extras),
              backgroundColor: 'rgba(255, 193, 7, 0.7)',
              borderColor: '#FFC107',
              borderWidth: 1,
              borderRadius: 4
            }]
          },
          options: {
            responsive: true, maintainAspectRatio: false,
            indexAxis: 'y',
            plugins: {
              legend: { display: false },
              tooltip: { callbacks: { label: ctx => ctx.parsed + ' hrs' } }
            },
            scales: {
              x: { beginAtZero: true, grid: { color: 'rgba(0,0,0,0.04)' }, ticks: { font: { family: "'Work Sans', sans-serif", size: 11 } } },
              y: { grid: { display: false }, ticks: { font: { family: "'Work Sans', sans-serif", size: 10 } } }
            }
          }
        })
      }
    }

    const cargarDatos = async () => {
      cargando.value = true
      error.value = ''
      try {
        const { data } = await axios.get('/api/reportes/dashboard/')
        metrics.value = data.kpis
        monthlyData.value = data.monthlyData || []
        topOvertimeEmployees.value = data.topOvertimeEmployees || []
        departmentData.value = data.departmentData || []

        if (monthlyData.value.length > 0) {
          const last = monthlyData.value[monthlyData.value.length - 1]
          ultimoMes.value = last.mes
        }

        datosCargados.value = true
        setTimeout(renderizarGraficos, 100)
      } catch (err) {
        const msg = err.response?.data?.error || err.message || 'Error de conexión con el servidor'
        error.value = msg
      } finally {
        cargando.value = false
      }
    }

    onMounted(() => {
      cargarDatos()
    })

    onUnmounted(() => {
      destruirGraficos()
    })

    return {
      cargando, datosCargados, error, metrics, ultimoMes,
      topOvertimeEmployees, formatCurrency, formatHours,
      cargarDatos
    }
  }
}
</script>

<style scoped>
.page-container { max-width: 1600px; margin: 0 auto; }

.page-header {
  margin-bottom: 2rem;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 1rem;
}
.page-header-content { display: flex; align-items: center; gap: 1rem; }
.page-header-icon { width: 44px; height: 44px; background: var(--color-primary-50); color: var(--color-primary-700); border-radius: 12px; display: flex; align-items: center; justify-content: center; flex-shrink: 0; }
.page-title { font-family: 'Young Serif', Georgia, serif; font-size: 1.5rem; color: var(--color-neutral-text-primary); margin: 0; }
.page-description { color: var(--color-neutral-text-secondary); margin: 0.15rem 0 0 0; font-size: 0.875rem; }

.btn-refresh {
  display: inline-flex;
  align-items: center;
  gap: 0.4rem;
  padding: 0.5rem 1rem;
  border: 1px solid var(--color-neutral-border);
  border-radius: 8px;
  font-size: 0.8rem;
  font-weight: 600;
  cursor: pointer;
  background: white;
  color: var(--color-neutral-text-secondary);
  transition: all 0.2s;
  font-family: inherit;
}
.btn-refresh:hover:not(:disabled) {
  border-color: var(--color-primary-500);
  color: var(--color-primary-700);
  background: var(--color-primary-50);
}
.btn-refresh:disabled { opacity: 0.6; cursor: not-allowed; }

/* Loading Dashboard */
.loading-dashboard {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 1rem;
  padding: 4rem 2rem;
  color: var(--color-neutral-text-secondary);
}
.loading-dashboard p { margin: 0; font-size: 0.95rem; }

.spinner-lg {
  width: 36px; height: 36px;
  border: 3px solid var(--color-neutral-divider);
  border-top-color: var(--color-primary-500);
  border-radius: 50%;
  animation: spin 0.7s linear infinite;
}
@keyframes spin { to { transform: rotate(360deg); } }

/* Error State */
.error-state-card {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.75rem;
  padding: 3rem 2rem;
  background: var(--color-error-bg);
  border: 1px solid transparent;
  border-radius: 12px;
  text-align: center;
}
.error-state-card h3 { margin: 0; color: var(--color-error-accent); font-family: 'Young Serif', Georgia, serif; }
.error-state-card p { margin: 0; color: var(--color-neutral-text-secondary); font-size: 0.875rem; }

.btn { display: inline-flex; align-items: center; justify-content: center; gap: 0.4rem; padding: 0.6rem 1rem; border: none; border-radius: 8px; font-size: 0.8rem; font-weight: 600; cursor: pointer; transition: all 0.2s; font-family: inherit; }
.btn-primary { background: var(--color-primary-700); color: white; }
.btn-primary:hover { background: var(--color-primary-900); transform: translateY(-1px); box-shadow: 0 4px 12px rgba(24, 95, 165, 0.3); }

.spinner-sm { width: 14px; height: 14px; border: 2px solid rgba(255,255,255,0.3); border-top-color: white; border-radius: 50%; animation: spin 0.6s linear infinite; display: inline-block; }

/* KPI Grid */
.kpi-grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 1.25rem; margin-bottom: 1.5rem; }

.kpi-card { background: white; border: 1px solid var(--color-neutral-divider); border-radius: 12px; padding: 1.25rem; display: flex; gap: 1rem; transition: all 0.2s; }
.kpi-card:hover { transform: translateY(-2px); box-shadow: 0 8px 24px rgba(0,0,0,0.08); }
.kpi-primary { border-top: 3px solid var(--color-primary-700); }
.kpi-success { border-top: 3px solid var(--color-secondary-700); }
.kpi-warning { border-top: 3px solid var(--color-warning-accent); }
.kpi-info { border-top: 3px solid var(--color-primary-500); }

.kpi-icon { width: 40px; height: 40px; border-radius: 10px; display: flex; align-items: center; justify-content: center; flex-shrink: 0; }
.kpi-primary .kpi-icon { background: var(--color-primary-50); color: var(--color-primary-700); }
.kpi-success .kpi-icon { background: var(--color-secondary-50); color: var(--color-secondary-700); }
.kpi-warning .kpi-icon { background: var(--color-warning-bg); color: var(--color-warning-accent); }
.kpi-info .kpi-icon { background: var(--color-info-bg); color: var(--color-info-accent); }

.kpi-body { display: flex; flex-direction: column; gap: 0.15rem; }
.kpi-label { font-size: 0.75rem; font-weight: 600; color: var(--color-neutral-text-secondary); text-transform: uppercase; letter-spacing: 0.04em; }
.kpi-value { font-family: 'Young Serif', Georgia, serif; font-size: 1.75rem; color: var(--color-neutral-text-primary); line-height: 1.2; }
.kpi-value small { font-family: 'Work Sans', sans-serif; font-size: 0.875rem; font-weight: 600; color: var(--color-neutral-text-secondary); }
.kpi-trend { font-size: 0.75rem; font-weight: 500; }
.kpi-trend.positive { color: var(--color-secondary-700); }
.kpi-trend.negative { color: var(--color-error-accent); }
.kpi-trend.neutral { color: var(--color-neutral-text-secondary); }

/* Charts */
.chart-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 1.25rem; margin-bottom: 1.25rem; }

.card { background: white; border: 1px solid var(--color-neutral-divider); border-radius: 12px; overflow: hidden; }
.card-header { padding: 1rem 1.25rem; border-bottom: 1px solid var(--color-neutral-divider); display: flex; align-items: center; justify-content: space-between; }
.card-header-left { display: flex; align-items: center; gap: 0.5rem; }
.card-dot { width: 8px; height: 8px; border-radius: 50%; flex-shrink: 0; }
.card-header h3 { font-family: 'Young Serif', Georgia, serif; font-size: 0.9rem; margin: 0; color: var(--color-neutral-text-primary); }
.card-badge { font-size: 0.7rem; padding: 0.2rem 0.6rem; background: var(--color-neutral-bg-page); border-radius: 20px; color: var(--color-neutral-text-secondary); font-weight: 500; }
.card-body { padding: 1.25rem; }
.chart-body { padding: 0.75rem; }
.chart-container { width: 100%; height: 300px; position: relative; }

.empty-chart {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  height: 300px;
  color: var(--color-neutral-text-secondary);
  font-size: 0.875rem;
}

@media (max-width: 1200px) {
  .kpi-grid { grid-template-columns: repeat(2, 1fr); }
  .chart-grid { grid-template-columns: 1fr; }
}

@media (max-width: 640px) {
  .kpi-grid { grid-template-columns: 1fr; }
  .page-header { flex-direction: column; text-align: center; }
  .page-header-content { flex-direction: column; text-align: center; }
  .chart-container { height: 240px; }
}
</style>
