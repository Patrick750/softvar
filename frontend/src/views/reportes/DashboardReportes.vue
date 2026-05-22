<template>
  <div class="container mt-4">
    <h2>Dashboard de Reportes</h2>
    <p class="text-muted mb-4">Visualice las métricas clave de asistencia y nómina de su empresa</p>

    <div class="row g-4 mb-4">
      <!-- Tarjetas de métricas resumidas -->
      <div class="col-md-3">
        <div class="card h-100 border-primary">
          <div class="card-body text-center">
            <h5 class="card-title">Empleados Activos</h5>
            <div class="display-4 fw-bold text-primary">{{ metrics.activeEmployees }}</div>
            <p class="text-muted">+2% vs mes anterior</p>
          </div>
        </div>
      </div>

      <div class="col-md-3">
        <div class="card h-100 border-success">
          <div class="card-body text-center">
            <h5 class="card-title">Asistencia Promedio</h5>
            <div class="display-4 fw-bold text-success">{{ metrics.attendanceRate }}%</div>
            <p class="text-muted">+1.5% vs mes anterior</p>
          </div>
        </div>
      </div>

      <div class="col-md-3">
        <div class="card h-100 border-warning">
          <div class="card-body text-center">
            <h5 class="card-title">Horas Extras Totales</h5>
            <div class="display-4 fw-bold text-warning">{{ formatHours(metrics.totalOvertime) }}</div>
            <p class="text-muted">-3% vs mes anterior</p>
          </div>
        </div>
      </div>

      <div class="col-md-3">
        <div class="card h-100 border-info">
          <div class="card-body text-center">
            <h5 class="card-title">Costo Nómina Mensual</h5>
            <div class="display-4 fw-bold text-info">{{ formatCurrency(metrics.monthlyPayrollCost) }}</div>
            <p class="text-muted">+4.5% vs mes anterior</p>
          </div>
        </div>
      </div>
    </div>

    <div class="row g-4">
      <!-- Gráfica de Barras: Días Trabajados y Ausencias -->
      <div class="col-lg-6">
        <div class="card h-100">
          <div class="card-header bg-primary text-white">
            <h5 class="mb-0">Días Trabajados vs Ausencias (Últimos 6 Meses)</h5>
          </div>
          <div class="card-body p-0">
            <div class="chart-container" style="height: 300px;">
              <canvas id="workDaysChart"></canvas>
            </div>
          </div>
        </div>
      </div>

      <!-- Gráfica de Líneas: Horas Extras y Costo -->
      <div class="col-lg-6">
        <div class="card h-100">
          <div class="card-header bg-success text-white">
            <h5 class="mb-0">Horas Extras y Costo Nómina (Últimos 6 Meses)</h5>
          </div>
          <div class="card-body p-0">
            <div class="chart-container" style="height: 300px;">
              <canvas id="overtimeCostChart"></canvas>
            </div>
          </div>
        </div>
      </div>
    </div>

    <div class="row g-4 mt-4">
      <!-- Gráfica de Pastel: Distribución por Departamento -->
      <div class="col-lg-6">
        <div class="card h-100">
          <div class="card-header bg-info text-white">
            <h5 class="mb-0">Distribución de Empleados por Departamento</h5>
          </div>
          <div class="card-body p-0">
            <div class="chart-container" style="height: 300px;">
              <canvas id="deptChart"></canvas>
            </div>
          </div>
        </div>
      </div>

      <!-- Gráfica de Barra Horizontal: Top 5 Empleados con Más Horas Extras -->
      <div class="col-lg-6">
        <div class="card h-100">
          <div class="card-header bg-warning text-white">
            <h5 class="mb-0">Top 5 Empleados con Más Horas Extras</h5>
          </div>
          <div class="card-body p-0">
            <div class="chart-container" style="height: 300px;">
              <canvas id="topOvertimeChart"></canvas>
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
    const metrics = ref({
      activeEmployees: 124,
      attendanceRate: 96.8,
      totalOvertime: 145.5, // horas
      monthlyPayrollCost: 87500000 // COP
    })

    // Datos para las gráficas (simulados)
    const chartData = ref({
      workDaysLabels: ['Dic', 'Ene', 'Feb', 'Mar', 'Abr', 'May'],
      workDaysData: [22, 20, 19, 21, 22, 21], // días trabajados promedio
      absenceData: [3, 5, 6, 4, 3, 4], // días de ausencia promedio

      overtimeLabels: ['Dic', 'Ene', 'Feb', 'Mar', 'Abr', 'May'],
      overtimeData: [120, 135, 142, 138, 150, 145.5], // horas extras
      costData: [82000000, 84500000, 86000000, 85500000, 88000000, 87500000], // costo nómina

      deptLabels: ['Administrativo', 'Ventas', 'Operaciones', 'TI', 'RRHH'],
      deptData: [35, 25, 20, 12, 8], // porcentaje por departamento

      topEmployees: [
        { name: 'Juan Pérez', hours: 28.5 },
        { name: 'María López', hours: 25.3 },
        { name: 'Carlos Rodríguez', hours: 22.1 },
        { name: 'Ana Gómez', hours: 19.8 },
        { name: 'Luis Torres', hours: 17.2 }
      ]
    })

    const formatCurrency = (value) => {
      return new Intl.NumberFormat('es-CO', {
        style: 'currency',
        currency: 'COP'
      }).format(value)
    }

    const formatHours = (hours) => {
      return new Intl.NumberFormat('es-CO', {
        minimumFractionDigits: 1,
        maximumFractionDigits: 1
      }).format(hours)
    }

    // Inicializar gráficas cuando se monte el componente
    onMounted(() => {
      // Simular delay para asegurar que el DOM esté listo
      setTimeout(() => {
        initCharts()
      }, 100)
    })

    const initCharts = () => {
      // Gráfica de Barras: Días Trabajados vs Ausencias
      const workDaysCtx = document.getElementById('workDaysChart')
      if (workDaysCtx) {
        new Chart(workDaysCtx, {
          type: 'bar',
          data: {
            labels: chartData.value.workDaysLabels,
            datasets: [
              {
                label: 'Días Trabajados',
                data: chartData.value.workDaysData,
                backgroundColor: 'rgba(24, 95, 165, 0.8)', // --color-primary-700
                borderColor: 'rgba(24, 95, 165, 1)',
                borderWidth: 1
              },
              {
                label: 'Ausencias',
                data: chartData.value.absenceData,
                backgroundColor: 'rgba(163, 45, 45, 0.8)', // --color-error-accent
                borderColor: 'rgba(163, 45, 45, 1)',
                borderWidth: 1
              }
            ]
          },
          options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
              y: {
                beginAtZero: true,
                title: {
                  display: true,
                  text: 'Días'
                }
              }
            },
            plugins: {
              legend: {
                position: 'top',
              },
              title: {
                display: false
              }
            }
          }
        })
      }

      // Gráfica de Líneas: Horas Extras y Costo
      const overtimeCostCtx = document.getElementById('overtimeCostChart')
      if (overtimeCostCtx) {
        new Chart(overtimeCostCtx, {
          type: 'line',
          data: {
            labels: chartData.value.overtimeLabels,
            datasets: [
              {
                label: 'Horas Extras',
                data: chartData.value.overtimeData,
                borderColor: 'rgba(99, 153, 34, 1)', // --color-secondary-700
                backgroundColor: 'rgba(99, 153, 34, 0.1)',
                tension: 0.3,
                fill: false,
                yAxisID: 'y'
              },
              {
                label: 'Costo Nómina (Millones COP)',
                data: chartData.value.costData.map(val => val / 1000000), // convertir a millones
                borderColor: 'rgba(24, 95, 165, 1)', // --color-primary-700
                backgroundColor: 'rgba(24, 95, 165, 0.1)',
                tension: 0.3,
                fill: false,
                yAxisID: 'y1'
              }
            ]
          },
          options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
              y: {
                type: 'linear',
                display: true,
                position: 'left',
                title: {
                  display: true,
                  text: 'Horas Extras'
                },
                grid: {
                  drawOnChartArea: false,
                }
              },
              y1: {
                type: 'linear',
                display: true,
                position: 'right',
                title: {
                  display: true,
                  text: 'Costo (Millones COP)'
                },
                grid: {
                  drawOnChartArea: false,
                }
              }
            },
            plugins: {
              legend: {
                position: 'top',
              }
            }
          }
        })
      }

      // Gráfica de Pastel: Distribución por Departamento
      const deptCtx = document.getElementById('deptChart')
      if (deptCtx) {
        new Chart(deptCtx, {
          type: 'doughnut',
          data: {
            labels: chartData.value.deptLabels,
            datasets: [{
              label: 'Distribución por Departamento (%)',
              data: chartData.value.deptData,
              backgroundColor: [
                'rgba(24, 95, 165, 0.8)',   // --color-primary-700
                'rgba(99, 153, 34, 0.8)',    // --color-secondary-700
                'rgba(55, 138, 171, 0.8)',   // --color-primary-500
                'rgba(181, 212, 244, 0.8)',  // --color-primary-200
                'rgba(44, 62, 80, 0.8)'      // tonos más oscuros
              ],
              borderColor: [
                'rgba(24, 95, 165, 1)',
                'rgba(99, 153, 34, 1)',
                'rgba(55, 138, 171, 1)',
                'rgba(181, 212, 244, 1)',
                'rgba(44, 62, 80, 1)'
              ],
              borderWidth: 2
            }]
          },
          options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
              legend: {
                position: 'right',
                labels: {
                  boxWidth: 12,
                  font: {
                    size: 10
                  }
                }
              },
              tooltip: {
                callbacks: {
                  label: function(context) {
                    const label = context.label || '';
                    const value = context.parsed || 0;
                    const sum = context.dataset.data.reduce((a, b) => a + b, 0);
                    const percentage = (value / sum * 100).toFixed(1) + '%';
                    return label + ': ' + percentage;
                  }
                }
              }
            }
          }
        })
      }

      // Gráfica de Barra Horizontal: Top 5 Empleados con Más Horas Extras
      const topOvertimeCtx = document.getElementById('topOvertimeChart')
      if (topOvertimeCtx) {
        new Chart(topOvertimeCtx, {
          type: 'bar',
          data: {
            labels: chartData.value.topEmployees.map(emp => emp.name),
            datasets: [{
              label: 'Horas Extras',
              data: chartData.value.topEmployees.map(emp => emp.hours),
              backgroundColor: 'rgba(255, 193, 7, 0.8)', // --color-warning-500 aproximado
              borderColor: 'rgba(255, 193, 7, 1)',
              borderWidth: 1
            }]
          },
          options: {
            responsive: true,
            maintainAspectRatio: false,
            indexAxis: 'y', // barras horizontales
            scales: {
              x: {
                beginAtZero: true,
                title: {
                  display: true,
                  text: 'Horas Extras'
                }
              }
            },
            plugins: {
              legend: {
                display: false
              },
              tooltip: {
                callbacks: {
                  label: function(context) {
                    return context.parsed + ' hrs';
                  }
                }
              }
            }
          }
        })
      }
    }

    return {
      metrics,
      formatCurrency,
      formatHours
    }
  }
}
</script>

<style scoped>
.container {
  max-width: 1600px;
}

.card {
  border: none;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
  margin-bottom: 1.5rem;
  height: 100%; /* para hacer las tarjetas de igual altura en filas */
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

.chart-container {
  width: 100%;
  height: 100%;
  position: relative;
}

/* Estilos para las tarjetas de métricas */
.card.border-primary {
  border-top: 3px solid var(--color-primary-700);
}

.card.border-success {
  border-top: 3px solid var(--color-secondary-700);
}

.card.border-warning {
  border-top: 3px solid var(--color-secondary-500);
}

.card.border-info {
  border-top: 3px solid var(--color-primary-500);
}

/* Responsive design */
@media (max-width: 1200px) {
  .container {
    max-width: 95%;
  }

  .row.g-4 {
    --bs-gutter-x: 1rem;
    --bs-gutter-y: 1rem;
  }
}

@media (max-width: 768px) {
  .col-lg-6 {
    width: 100%;
    margin-bottom: 1.5rem;
  }

  .card-body {
    padding: 1rem;
  }

  .chart-container {
    height: 250px !important;
  }
}
</style>