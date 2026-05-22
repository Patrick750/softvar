<template>
  <div>
    <div class="page-header">
      <div class="page-header-left">
        <h1 class="display-heading">
          Aprobaciones de Asistencia
          <span v-if="!loading && pendientes.length" class="badge badge-solid-warning ms-2">
            {{ pendientes.length }}
          </span>
        </h1>
        <p class="text-muted">Revise y gestione las solicitudes de marcación manual pendientes</p>
      </div>
      <div class="page-header-actions">
        <button class="btn btn-outline" @click="fetchPendientes" :disabled="loading">
          <i class="bi bi-arrow-clockwise me-1" :class="{ 'spin': loading }"></i>
          Actualizar
        </button>
      </div>
    </div>

    <!-- Loading Skeleton -->
    <div v-if="loading" class="card card-elevated p-0">
      <div class="card-header-warning">
        <h5><i class="bi bi-hourglass-split me-2"></i>Cargando solicitudes...</h5>
      </div>
      <div class="card-body">
        <div class="skeleton-table">
          <div v-for="n in 4" :key="n" class="skeleton-row">
            <div class="skeleton-cell skeleton-cell-sm"></div>
            <div class="skeleton-cell skeleton-cell-md"></div>
            <div class="skeleton-cell skeleton-cell-xs"></div>
            <div class="skeleton-cell skeleton-cell-lg"></div>
            <div class="skeleton-cell skeleton-cell-actions"></div>
          </div>
        </div>
      </div>
    </div>

    <!-- Empty State -->
    <div v-else-if="!pendientes.length" class="card card-elevated p-0">
      <div class="card-body">
        <div class="empty-state">
          <div class="empty-state-icon">
            <i class="bi bi-check-circle"></i>
          </div>
          <h3 class="empty-state-title">¡Todo al día!</h3>
          <p class="empty-state-text">No hay solicitudes de asistencia pendientes de aprobación.</p>
          <button class="btn btn-outline mt-3" @click="fetchPendientes">
            <i class="bi bi-arrow-clockwise me-1"></i>
            Verificar de nuevo
          </button>
        </div>
      </div>
    </div>

    <!-- Pendientes Table -->
    <div v-else class="card card-elevated p-0">
      <div class="card-header-warning">
        <h5>
          <i class="bi bi-clock-history me-2"></i>
          Solicitudes Pendientes
          <span class="badge badge-solid-warning ms-2">{{ pendientes.length }}</span>
        </h5>
      </div>
      <div class="card-body p-0">
        <div class="table-container">
          <table class="table table-compact">
            <thead>
              <tr>
                <th>Empleado</th>
                <th>Fecha y Hora</th>
                <th>Tipo</th>
                <th>Justificación del Empleado</th>
                <th class="text-center">Acciones</th>
              </tr>
            </thead>
            <tbody>
              <template v-for="(item, idx) in pendientes" :key="item.id">
                <!-- Data Row -->
                <tr class="data-row" :style="{ '--i': idx }">
                  <td>
                    <div class="employee-cell">
                      <div class="avatar avatar-sm avatar-placeholder">
                        {{ getInitials(item.empleado_nombre) }}
                      </div>
                      <span class="employee-name">{{ item.empleado_nombre }}</span>
                    </div>
                  </td>
                  <td>
                    <span class="fecha-display">
                      <i class="bi bi-calendar3 me-1 text-muted"></i>
                      {{ formatFecha(item.fecha_hora) }}
                    </span>
                  </td>
                  <td>
                    <span class="badge" :class="item.tipo === 'ENTRADA' ? 'badge-solid-primary' : 'badge-neutral'">
                      {{ item.tipo }}
                    </span>
                  </td>
                  <td>
                    <span class="justificacion-text">{{ item.justificacion_manual || '—' }}</span>
                  </td>
                  <td class="text-center">
                    <div class="action-buttons" v-if="activeRow !== item.id">
                      <button class="btn btn-success btn-sm" @click="openAction(item.id, true)" title="Aprobar">
                        <i class="bi bi-check-lg me-1"></i>Aprobar
                      </button>
                      <button class="btn btn-error btn-sm" @click="openAction(item.id, false)" title="Rechazar">
                        <i class="bi bi-x-lg me-1"></i>Rechazar
                      </button>
                    </div>
                    <div v-else class="action-buttons">
                      <button class="btn btn-outline btn-sm" @click="cancelAction">
                        <i class="bi bi-arrow-left me-1"></i>Cancelar
                      </button>
                    </div>
                  </td>
                </tr>

                <!-- Inline Expansion Row -->
                <tr v-if="activeRow === item.id" class="expansion-row">
                  <td colspan="5">
                    <div class="expansion-panel" :class="isApproving ? 'expansion-approve' : 'expansion-reject'">
                      <div class="expansion-header">
                        <i :class="isApproving ? 'bi bi-check-circle-fill text-success' : 'bi bi-x-circle-fill text-error'"></i>
                        <h6>{{ isApproving ? 'Confirmar Aprobación' : 'Confirmar Rechazo' }}</h6>
                      </div>
                      <p class="expansion-subtitle">
                        {{ isApproving
                          ? 'La marcación del empleado será registrada como válida.'
                          : 'La solicitud de marcación será rechazada.' }}
                      </p>
                      <div class="form-group mb-3">
                        <label class="form-label">
                          Comentario del Administrador
                          <span class="text-muted text-sm">(opcional)</span>
                        </label>
                        <textarea
                          class="form-input"
                          rows="2"
                          v-model="adminComment"
                          :placeholder="isApproving
                            ? 'Ej: Aprobado por verificación presencial...'
                            : 'Ej: Justificación insuficiente, solicitar soporte...'"
                        ></textarea>
                      </div>
                      <div class="expansion-actions">
                        <button class="btn btn-outline btn-sm" @click="cancelAction" :disabled="submitting">
                          Cancelar
                        </button>
                        <button
                          class="btn btn-sm"
                          :class="isApproving ? 'btn-success' : 'btn-error'"
                          @click="confirmAction(item.id)"
                          :disabled="submitting"
                        >
                          <span v-if="submitting" class="spinner spinner-sm me-1"></span>
                          <i v-else :class="isApproving ? 'bi bi-check-lg me-1' : 'bi bi-x-lg me-1'"></i>
                          {{ isApproving ? 'Confirmar Aprobación' : 'Confirmar Rechazo' }}
                        </button>
                      </div>
                    </div>
                  </td>
                </tr>
              </template>
            </tbody>
          </table>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted, inject } from 'vue'
import axios from 'axios'

export default {
  setup() {
    const addToast = inject('addToast', () => {})

    const pendientes = ref([])
    const loading = ref(true)
    const submitting = ref(false)

    // Action state
    const activeRow = ref(null)
    const isApproving = ref(true)
    const adminComment = ref('')

    const fetchPendientes = async () => {
      loading.value = true
      try {
        const response = await axios.get('/api/asistencia/pendientes/')
        pendientes.value = response.data
      } catch (err) {
        console.error('Error fetching pendientes:', err)
        addToast('Error', 'No se pudieron cargar las solicitudes pendientes.', 'error')
      } finally {
        loading.value = false
      }
    }

    const openAction = (id, approve) => {
      activeRow.value = id
      isApproving.value = approve
      adminComment.value = ''
    }

    const cancelAction = () => {
      activeRow.value = null
      adminComment.value = ''
    }

    const confirmAction = async (asistenciaId) => {
      submitting.value = true
      try {
        await axios.post('/api/asistencia/aprobar/', {
          asistencia_id: asistenciaId,
          aprobar: isApproving.value,
          justificacion_admin: adminComment.value
        })

        const action = isApproving.value ? 'aprobada' : 'rechazada'
        addToast('Éxito', `Solicitud ${action} correctamente.`, 'success')

        cancelAction()
        await fetchPendientes()
      } catch (err) {
        console.error('Error processing action:', err)
        const errMsg = err.response?.data?.error || 'No se pudo procesar la solicitud.'
        addToast('Error', errMsg, 'error')
      } finally {
        submitting.value = false
      }
    }

    const formatFecha = (isoString) => {
      if (!isoString) return '—'
      const date = new Date(isoString)
      return date.toLocaleDateString('es-CO', {
        year: 'numeric',
        month: 'short',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit',
        hour12: true
      })
    }

    const getInitials = (name) => {
      if (!name) return '?'
      return name.split(' ').map(w => w[0]).join('').toUpperCase().slice(0, 2)
    }

    onMounted(fetchPendientes)

    return {
      pendientes,
      loading,
      submitting,
      activeRow,
      isApproving,
      adminComment,
      fetchPendientes,
      openAction,
      cancelAction,
      confirmAction,
      formatFecha,
      getInitials
    }
  }
}
</script>

<style scoped>
/* === Page Header Layout === */
.page-header {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  flex-wrap: wrap;
  gap: 1rem;
}

.page-header-actions {
  flex-shrink: 0;
}

/* === Skeleton Loading === */
.skeleton-table {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.skeleton-row {
  display: flex;
  gap: 1rem;
  align-items: center;
}

.skeleton-cell {
  height: 18px;
  background: linear-gradient(90deg, var(--color-bg-subtle) 25%, var(--color-divider) 50%, var(--color-bg-subtle) 75%);
  background-size: 200% 100%;
  animation: shimmer 1.5s ease-in-out infinite;
  border-radius: var(--border-radius-sm);
}

.skeleton-cell-xs { width: 60px; }
.skeleton-cell-sm { width: 120px; }
.skeleton-cell-md { width: 160px; }
.skeleton-cell-lg { flex: 1; min-width: 140px; }
.skeleton-cell-actions { width: 180px; }

@keyframes shimmer {
  0% { background-position: 200% 0; }
  100% { background-position: -200% 0; }
}

/* === Spin animation for refresh icon === */
.spin {
  animation: spin 0.8s linear infinite;
}

@keyframes spin {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}

/* === Empty State === */
.empty-state {
  text-align: center;
  padding: 3rem 1rem;
}

.empty-state-icon {
  width: 80px;
  height: 80px;
  margin: 0 auto 1.5rem;
  background: linear-gradient(135deg, var(--color-success-bg, #ecfdf5), var(--color-primary-50));
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  animation: pulse-icon 2s ease-in-out infinite;
}

.empty-state-icon i {
  font-size: 2.25rem;
  color: var(--color-success-accent, #10b981);
}

.empty-state-title {
  font-size: 1.375rem;
  font-weight: 700;
  color: var(--color-text-primary);
  margin-bottom: 0.5rem;
}

.empty-state-text {
  color: var(--color-text-secondary);
  font-size: 0.9375rem;
  max-width: 400px;
  margin: 0 auto;
}

@keyframes pulse-icon {
  0%, 100% { transform: scale(1); }
  50% { transform: scale(1.06); }
}

/* === Employee Cell === */
.employee-cell {
  display: flex;
  align-items: center;
  gap: 0.625rem;
}

.employee-name {
  font-weight: 600;
  font-size: 0.875rem;
  color: var(--color-text-primary);
  white-space: nowrap;
}

/* === Fecha Display === */
.fecha-display {
  font-size: 0.8125rem;
  white-space: nowrap;
}

/* === Justificacion === */
.justificacion-text {
  font-size: 0.8125rem;
  color: var(--color-text-secondary);
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
  max-width: 280px;
}

/* === Action Buttons === */
.action-buttons {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
}

/* === Row Animations === */
.data-row {
  opacity: 0;
  transform: translateY(8px);
  animation: fadeInRow 0.35s ease forwards;
  animation-delay: calc(var(--i, 0) * 60ms);
  transition: background 0.2s, transform 0.15s;
}

.data-row:hover {
  background: var(--color-primary-50);
}

.data-row:last-child td {
  border-bottom: none;
}

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

/* === Expansion Panel === */
.expansion-row td {
  padding: 0 !important;
  border-bottom: none;
}

.expansion-panel {
  margin: 0 1rem 1rem;
  padding: 1.25rem;
  border-radius: var(--border-radius-md);
  animation: expandIn 0.3s ease forwards;
  border: 1px solid;
}

.expansion-approve {
  background: var(--color-success-bg, #ecfdf5);
  border-color: var(--color-success-accent, #10b981);
}

.expansion-reject {
  background: var(--color-error-bg, #fef2f2);
  border-color: var(--color-error-accent, #ef4444);
}

.expansion-header {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  margin-bottom: 0.375rem;
}

.expansion-header i {
  font-size: 1.125rem;
}

.expansion-header h6 {
  margin: 0;
  font-weight: 700;
  font-size: 0.9375rem;
}

.expansion-subtitle {
  font-size: 0.8125rem;
  color: var(--color-text-secondary);
  margin-bottom: 1rem;
}

.expansion-actions {
  display: flex;
  align-items: center;
  justify-content: flex-end;
  gap: 0.5rem;
}

@keyframes expandIn {
  from {
    opacity: 0;
    transform: translateY(-8px);
    max-height: 0;
  }
  to {
    opacity: 1;
    transform: translateY(0);
    max-height: 400px;
  }
}

/* === Text helpers === */
.text-success { color: var(--color-success-accent, #10b981); }
.text-error { color: var(--color-error-accent, #ef4444); }

/* === Responsive === */
@media (max-width: 768px) {
  .page-header {
    flex-direction: column;
  }

  .table-container {
    overflow-x: auto;
    -webkit-overflow-scrolling: touch;
  }

  .action-buttons {
    flex-direction: column;
  }

  .action-buttons .btn {
    width: 100%;
  }

  .expansion-panel {
    margin: 0 0.5rem 0.75rem;
  }

  .expansion-actions {
    flex-direction: column;
  }

  .expansion-actions .btn {
    width: 100%;
  }
}

@media (prefers-reduced-motion: reduce) {
  .data-row {
    animation: none;
    opacity: 1;
    transform: none;
  }

  .expansion-panel {
    animation: none;
  }

  .skeleton-cell {
    animation: none;
  }

  .empty-state-icon {
    animation: none;
  }
}
</style>
