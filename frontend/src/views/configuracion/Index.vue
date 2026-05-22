<template>
  <div class="page-container">
    <div class="page-header">
      <div class="page-header-content">
        <div class="page-header-icon">
          <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <circle cx="12" cy="12" r="3"/><path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 0 1-2.83 2.83l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-4 0v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 0 1-2.83-2.83l.06-.06A1.65 1.65 0 0 0 4.68 15a1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1 0-4h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 0 1 2.83-2.83l.06.06A1.65 1.65 0 0 0 9 4.68a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 4 0v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 0 1 2.83 2.83l-.06.06A1.65 1.65 0 0 0 19.4 9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 0 4h-.09a1.65 1.65 0 0 0-1.51 1z"/>
          </svg>
        </div>
        <div>
          <h1 class="page-title">Configuración del Sistema</h1>
          <p class="page-description">Administre parámetros del sistema de nómina y seguridad</p>
        </div>
      </div>
    </div>

    <!-- Loading State -->
    <div v-if="loadingParams" class="loading-state">
      <span class="spinner spinner-lg"></span>
      <p>Cargando parámetros del sistema...</p>
    </div>

    <template v-else>
      <div class="grid-2">
        <!-- SMMLV Configuration -->
        <div class="card card-success">
          <div class="card-header">
            <div class="card-header-left">
              <span class="card-icon">
                <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                  <line x1="12" y1="1" x2="12" y2="23"/><path d="M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6"/>
                </svg>
              </span>
              <h3>Parametrización SMMLV</h3>
            </div>
          </div>
          <div class="card-body">
            <form @submit.prevent="actualizarSMMLV" class="form-grid">
              <div class="form-group full-width">
                <label class="form-label">SMMLV <span class="required">*</span></label>
                <div class="input-prefix">
                  <span class="prefix">$</span>
                  <input type="number" v-model.number="config.smmlv" required min="0" step="0.01" class="form-input prefix-input">
                </div>
              </div>
              <div class="form-group full-width">
                <button type="submit" class="btn btn-primary btn-block" :disabled="savingSmmlv">
                  <span v-if="savingSmmlv" class="spinner"></span>
                  <svg v-else width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M19 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h11l5 5v11a2 2 0 0 1-2 2z"/><polyline points="17 21 17 13 7 13 7 21"/><polyline points="7 3 7 8 15 8"/></svg>
                  {{ savingSmmlv ? 'Guardando...' : 'Actualizar SMMLV' }}
                </button>
              </div>
            </form>
          </div>
        </div>

        <!-- Contribution Rates -->
        <div class="card card-info">
          <div class="card-header">
            <div class="card-header-left">
              <span class="card-icon">
                <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                  <path d="M16 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/><circle cx="8.5" cy="7" r="4"/><line x1="20" y1="8" x2="20" y2="14"/><line x1="23" y1="11" x2="17" y2="11"/>
                </svg>
              </span>
              <h3>Porcentajes de Aportes</h3>
            </div>
          </div>
          <div class="card-body">
            <form @submit.prevent="actualizarPorcentajes" class="form-grid">
              <div class="form-group">
                <label class="form-label">Salud (%) <span class="required">*</span></label>
                <div class="input-suffix">
                  <input type="number" v-model.number="porcentajes.salud" required min="0" max="100" step="0.01" class="form-input suffix-input">
                  <span class="suffix">%</span>
                </div>
              </div>
              <div class="form-group">
                <label class="form-label">Pensión (%) <span class="required">*</span></label>
                <div class="input-suffix">
                  <input type="number" v-model.number="porcentajes.pension" required min="0" max="100" step="0.01" class="form-input suffix-input">
                  <span class="suffix">%</span>
                </div>
              </div>
              <div class="form-group full-width">
                <label class="form-label">ARL (%) <span class="required">*</span></label>
                <div class="input-suffix">
                  <input type="number" v-model.number="porcentajes.arl" required min="0" max="100" step="0.01" class="form-input suffix-input">
                  <span class="suffix">%</span>
                </div>
              </div>
              <div class="form-group full-width">
                <button type="submit" class="btn btn-primary btn-block" :disabled="savingPorcentajes">
                  <span v-if="savingPorcentajes" class="spinner"></span>
                  <svg v-else width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M19 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h11l5 5v11a2 2 0 0 1-2 2z"/><polyline points="17 21 17 13 7 13 7 21"/><polyline points="7 3 7 8 15 8"/></svg>
                  {{ savingPorcentajes ? 'Guardando...' : 'Actualizar Porcentajes' }}
                </button>
              </div>
            </form>
          </div>
        </div>
      </div>

      <!-- GPS Office Configuration -->
      <div class="card card-gps" style="margin-top: 1.5rem;">
        <div class="card-header">
          <div class="card-header-left">
            <span class="card-icon card-icon-gps">
              <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"/><circle cx="12" cy="10" r="3"/>
              </svg>
            </span>
            <h3>Ubicación de la Oficina (GPS)</h3>
          </div>
          <span class="badge badge-gps">
            <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><circle cx="12" cy="12" r="10"/><line x1="2" y1="12" x2="22" y2="12"/><path d="M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1-4-10 15.3 15.3 0 0 1 4-10z"/></svg>
            Geolocalización
          </span>
        </div>
        <div class="card-body">
          <div class="gps-description">
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><line x1="12" y1="16" x2="12" y2="12"/><line x1="12" y1="8" x2="12.01" y2="8"/></svg>
            <span>Defina las coordenadas y el radio de la oficina para la validación de asistencia por GPS.</span>
          </div>
          <form @submit.prevent="actualizarGPS" class="form-grid form-grid-3">
            <div class="form-group">
              <label class="form-label">Latitud <span class="required">*</span></label>
              <input type="number" v-model.number="gps.latitud" required step="0.000001" class="form-input" placeholder="ej. 2.927300">
            </div>
            <div class="form-group">
              <label class="form-label">Longitud <span class="required">*</span></label>
              <input type="number" v-model.number="gps.longitud" required step="0.000001" class="form-input" placeholder="ej. -75.281900">
            </div>
            <div class="form-group">
              <label class="form-label">Radio (metros) <span class="required">*</span></label>
              <div class="input-suffix">
                <input type="number" v-model.number="gps.radio" required min="1" step="1" class="form-input suffix-input" placeholder="ej. 100">
                <span class="suffix">m</span>
              </div>
            </div>
            <div class="form-group full-width">
              <button type="submit" class="btn btn-gps btn-block" :disabled="savingGps">
                <span v-if="savingGps" class="spinner"></span>
                <svg v-else width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"/><circle cx="12" cy="10" r="3"/></svg>
                {{ savingGps ? 'Guardando...' : 'Guardar Ubicación' }}
              </button>
            </div>
          </form>
        </div>
      </div>

      <!-- Audit Log Viewer -->
      <div class="card card-audit" style="margin-top: 1.5rem;">
        <div class="card-header card-header-dark">
          <div class="card-header-left">
            <span class="card-icon card-icon-audit">
              <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/><line x1="16" y1="13" x2="8" y2="13"/><line x1="16" y1="17" x2="8" y2="17"/><polyline points="10 9 9 9 8 9"/>
              </svg>
            </span>
            <h3>Registro de Auditoría</h3>
          </div>
          <div class="card-header-actions">
            <span v-if="auditLogs.length" class="badge badge-audit-count">{{ auditLogs.length }} registros</span>
            <button type="button" class="btn btn-sm btn-outline btn-refresh" @click="cargarAuditLogs" :disabled="loadingAudit">
              <span v-if="loadingAudit" class="spinner spinner-sm"></span>
              <svg v-else width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
                <polyline points="23 4 23 10 17 10"/><polyline points="1 20 1 14 7 14"/><path d="M3.51 9a9 9 0 0 1 14.85-3.36L23 10M1 14l4.64 4.36A9 9 0 0 0 20.49 15"/>
              </svg>
              Actualizar
            </button>
          </div>
        </div>
        <div class="card-body p-0">
          <div v-if="loadingAudit && !auditLogs.length" class="loading-state loading-state-sm">
            <span class="spinner"></span>
            <p>Cargando registros de auditoría...</p>
          </div>
          <div v-else-if="auditLogs.length" class="table-wrapper">
            <table class="data-table">
              <thead>
                <tr>
                  <th>Usuario</th>
                  <th>Fecha / Hora</th>
                  <th>Acción</th>
                  <th>Tabla Afectada</th>
                  <th>ID Registro</th>
                  <th>IP</th>
                  <th class="th-detail">Detalle</th>
                </tr>
              </thead>
              <tbody>
                <template v-for="(log, idx) in auditLogs" :key="log.id">
                  <tr class="data-row" :style="{ '--i': idx }" @click="toggleAuditDetail(log.id)">
                    <td>
                      <span class="user-cell">
                        <span class="user-avatar-mini">{{ getInitials(log.usuario) }}</span>
                        {{ log.usuario }}
                      </span>
                    </td>
                    <td class="text-mono">{{ formatFechaHora(log.fecha_hora) }}</td>
                    <td>
                      <span class="badge" :class="accionBadgeClass(log.accion)">{{ log.accion }}</span>
                    </td>
                    <td><span class="tabla-chip">{{ log.tabla_afectada }}</span></td>
                    <td class="text-mono text-muted">{{ log.registro_id }}</td>
                    <td class="text-mono text-muted">{{ log.ip_address || '—' }}</td>
                    <td class="td-toggle">
                      <button type="button" class="btn-toggle-detail" :class="{ 'is-open': expandedLogId === log.id }">
                        <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="6 9 12 15 18 9"/></svg>
                      </button>
                    </td>
                  </tr>
                  <tr v-if="expandedLogId === log.id" class="detail-row">
                    <td colspan="7">
                      <div class="detail-content">
                        <div class="detail-col">
                          <span class="detail-label">Valor Anterior</span>
                          <pre class="detail-value detail-value-old">{{ formatJsonValue(log.valor_anterior) }}</pre>
                        </div>
                        <div class="detail-arrow">
                          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="5" y1="12" x2="19" y2="12"/><polyline points="12 5 19 12 12 19"/></svg>
                        </div>
                        <div class="detail-col">
                          <span class="detail-label">Valor Nuevo</span>
                          <pre class="detail-value detail-value-new">{{ formatJsonValue(log.valor_nuevo) }}</pre>
                        </div>
                      </div>
                    </td>
                  </tr>
                </template>
              </tbody>
            </table>
          </div>
          <div v-else class="empty-state-audit">
            <svg width="40" height="40" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" opacity="0.35">
              <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/><line x1="16" y1="13" x2="8" y2="13"/><line x1="16" y1="17" x2="8" y2="17"/>
            </svg>
            <p>No hay registros de auditoría disponibles</p>
          </div>
        </div>
      </div>

      <!-- Access Control Summary -->
      <div class="card" style="margin-top: 1.5rem;">
        <div class="card-header">
          <div class="card-header-left">
            <span class="card-icon" style="background: var(--color-neutral-text-primary, #1E1E1C);">
              <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="white" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <rect x="3" y="11" width="18" height="11" rx="2" ry="2"/><path d="M7 11V7a5 5 0 0 1 10 0v4"/>
              </svg>
            </span>
            <h3>Control de Acceso por Rol</h3>
          </div>
        </div>
        <div class="card-body p-0">
          <div class="table-wrapper">
            <table class="data-table">
              <thead>
                <tr>
                  <th>Rol</th>
                  <th>Módulos Accesibles</th>
                  <th>Color UI</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="(rol, idx) in roles" :key="rol.nombre" class="data-row" :style="{ '--i': idx }">
                  <td>
                    <span class="role-badge" :style="{ background: rol.color + '20', color: rol.color, border: '1px solid ' + rol.color + '40' }">
                      <span class="role-dot" :style="{ background: rol.color }"></span>
                      {{ rol.nombre }}
                    </span>
                  </td>
                  <td>
                    <div class="role-modules">
                      <span v-for="mod in rol.modulos" :key="mod" class="module-chip">{{ mod }}</span>
                    </div>
                  </td>
                  <td>
                    <span class="color-swatch" :style="{ background: rol.color }">{{ rol.color }}</span>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </template>
  </div>
</template>

<script>
import { ref, onMounted, inject } from 'vue'
import axios from 'axios'

export default {
  setup() {
    const addToast = inject('addToast', () => {})

    // --- State ---
    const loadingParams = ref(true)
    const savingSmmlv = ref(false)
    const savingPorcentajes = ref(false)
    const savingGps = ref(false)
    const loadingAudit = ref(false)

    const config = ref({ smmlv: 0 })
    const porcentajes = ref({ salud: 0, pension: 0, arl: 0 })
    const gps = ref({ latitud: 0, longitud: 0, radio: 100 })

    const auditLogs = ref([])
    const expandedLogId = ref(null)

    const roles = [
      { nombre: 'Administrador RRHH', color: '#185FA5', modulos: ['Gestión empleados', 'Desprendibles', 'Credenciales', 'Aprobación manual'] },
      { nombre: 'Empleado', color: '#378ADD', modulos: ['Registro asistencia', 'Portal personal'] },
      { nombre: 'Contador', color: '#3B6D11', modulos: ['Liquidación nómina', 'Exportación ACH/Excel'] },
      { nombre: 'Gerente', color: '#042C53', modulos: ['Dashboard reportes', 'Reportes filtrables'] },
      { nombre: 'Admin. Sistema', color: '#2C2C2A', modulos: ['Auditoría', 'Parametrización', 'Control acceso'] }
    ]

    // --- API Methods ---
    const cargarParametros = async () => {
      loadingParams.value = true
      try {
        const { data } = await axios.get('/api/configuracion/parametros/')
        if (data.SMMLV) {
          config.value.smmlv = parseFloat(data.SMMLV.valor) || 0
        }
        if (data.SALUD_APORTE) {
          porcentajes.value.salud = parseFloat(data.SALUD_APORTE.valor) || 0
        }
        if (data.PENSION_APORTE) {
          porcentajes.value.pension = parseFloat(data.PENSION_APORTE.valor) || 0
        }
        if (data.ARL_APORTE) {
          porcentajes.value.arl = parseFloat(data.ARL_APORTE.valor) || 0
        }
        if (data.OFICINA_LATITUD) {
          gps.value.latitud = parseFloat(data.OFICINA_LATITUD.valor) || 0
        }
        if (data.OFICINA_LONGITUD) {
          gps.value.longitud = parseFloat(data.OFICINA_LONGITUD.valor) || 0
        }
        if (data.OFICINA_RADIO_METROS) {
          gps.value.radio = parseFloat(data.OFICINA_RADIO_METROS.valor) || 100
        }
      } catch (err) {
        console.error('Error cargando parámetros:', err)
        addToast('Error', 'No se pudieron cargar los parámetros del sistema.', 'error')
      } finally {
        loadingParams.value = false
      }
    }

    const actualizarSMMLV = async () => {
      savingSmmlv.value = true
      try {
        await axios.post('/api/configuracion/parametros/', {
          SMMLV: String(config.value.smmlv)
        })
        addToast('Éxito', 'SMMLV actualizado correctamente.', 'success')
      } catch (err) {
        console.error('Error actualizando SMMLV:', err)
        addToast('Error', 'No se pudo actualizar el SMMLV.', 'error')
      } finally {
        savingSmmlv.value = false
      }
    }

    const actualizarPorcentajes = async () => {
      savingPorcentajes.value = true
      try {
        await axios.post('/api/configuracion/parametros/', {
          SALUD_APORTE: String(porcentajes.value.salud),
          PENSION_APORTE: String(porcentajes.value.pension),
          ARL_APORTE: String(porcentajes.value.arl)
        })
        addToast('Éxito', 'Porcentajes de aportes actualizados correctamente.', 'success')
      } catch (err) {
        console.error('Error actualizando porcentajes:', err)
        addToast('Error', 'No se pudieron actualizar los porcentajes.', 'error')
      } finally {
        savingPorcentajes.value = false
      }
    }

    const actualizarGPS = async () => {
      savingGps.value = true
      try {
        await axios.post('/api/configuracion/parametros/', {
          OFICINA_LATITUD: String(gps.value.latitud),
          OFICINA_LONGITUD: String(gps.value.longitud),
          OFICINA_RADIO_METROS: String(gps.value.radio)
        })
        addToast('Éxito', 'Ubicación de la oficina actualizada correctamente.', 'success')
      } catch (err) {
        console.error('Error actualizando GPS:', err)
        addToast('Error', 'No se pudo actualizar la ubicación de la oficina.', 'error')
      } finally {
        savingGps.value = false
      }
    }

    const cargarAuditLogs = async () => {
      loadingAudit.value = true
      try {
        const { data } = await axios.get('/api/auditoria/logs/')
        auditLogs.value = Array.isArray(data) ? data : []
      } catch (err) {
        console.error('Error cargando auditoría:', err)
        addToast('Error', 'No se pudieron cargar los registros de auditoría.', 'error')
      } finally {
        loadingAudit.value = false
      }
    }

    // --- Helpers ---
    const toggleAuditDetail = (logId) => {
      expandedLogId.value = expandedLogId.value === logId ? null : logId
    }

    const formatFechaHora = (isoStr) => {
      if (!isoStr) return '—'
      const d = new Date(isoStr)
      return d.toLocaleDateString('es-CO', { day: '2-digit', month: 'short', year: 'numeric' }) +
        ' ' + d.toLocaleTimeString('es-CO', { hour: '2-digit', minute: '2-digit', second: '2-digit', hour12: true })
    }

    const formatJsonValue = (val) => {
      if (!val) return '—'
      if (typeof val === 'string') {
        try {
          const parsed = JSON.parse(val)
          return JSON.stringify(parsed, null, 2)
        } catch {
          return val
        }
      }
      return JSON.stringify(val, null, 2)
    }

    const getInitials = (name) => {
      if (!name) return '?'
      const parts = name.split(' ')
      return (parts[0]?.[0] || '').toUpperCase() + (parts[1]?.[0] || '').toUpperCase()
    }

    const accionBadgeClass = (accion) => {
      if (!accion) return 'badge-neutral'
      const a = accion.toLowerCase()
      if (a.includes('crear') || a.includes('create') || a.includes('insert')) return 'badge-success'
      if (a.includes('eliminar') || a.includes('delete') || a.includes('borrar')) return 'badge-error'
      if (a.includes('actualizar') || a.includes('update') || a.includes('editar')) return 'badge-warning'
      return 'badge-info'
    }

    // --- Lifecycle ---
    onMounted(async () => {
      await cargarParametros()
      cargarAuditLogs()
    })

    return {
      loadingParams, savingSmmlv, savingPorcentajes, savingGps, loadingAudit,
      config, porcentajes, gps,
      auditLogs, expandedLogId,
      roles,
      actualizarSMMLV, actualizarPorcentajes, actualizarGPS,
      cargarAuditLogs, toggleAuditDetail,
      formatFechaHora, formatJsonValue, getInitials, accionBadgeClass
    }
  }
}
</script>

<style scoped>
/* ===== Page Layout ===== */
.page-container { max-width: 1100px; margin: 0 auto; }

.page-header { margin-bottom: 2rem; }
.page-header-content { display: flex; align-items: center; gap: 1rem; }
.page-header-icon {
  width: 44px; height: 44px;
  background: var(--color-primary-50); color: var(--color-primary-700);
  border-radius: 12px; display: flex; align-items: center; justify-content: center; flex-shrink: 0;
}
.page-title { font-family: 'Young Serif', Georgia, serif; font-size: 1.5rem; color: var(--color-text-primary, #1E1E1C); margin: 0; }
.page-description { color: var(--color-text-secondary, #5F5E5A); margin: 0.15rem 0 0 0; font-size: 0.875rem; }

/* ===== Loading ===== */
.loading-state {
  display: flex; flex-direction: column; align-items: center; justify-content: center;
  gap: 1rem; padding: 4rem 1rem; color: var(--color-text-secondary, #5F5E5A);
}
.loading-state p { margin: 0; font-size: 0.9rem; }
.loading-state-sm { padding: 2.5rem 1rem; }

.spinner {
  width: 18px; height: 18px;
  border: 2.5px solid rgba(255,255,255,0.3); border-top-color: white;
  border-radius: 50%; animation: spin 0.6s linear infinite; flex-shrink: 0;
}
.spinner-sm { width: 14px; height: 14px; border-width: 2px; }
.spinner-lg {
  width: 32px; height: 32px; border-width: 3px;
  border-color: var(--color-primary-200); border-top-color: var(--color-primary-700);
}
@keyframes spin { to { transform: rotate(360deg); } }

/* ===== Grid ===== */
.grid-2 { display: grid; grid-template-columns: 1fr 1fr; gap: 1.5rem; }
@media (max-width: 800px) { .grid-2 { grid-template-columns: 1fr; } }

/* ===== Cards ===== */
.card {
  background: white; border: 1px solid var(--color-divider, #D3D1C7);
  border-radius: 12px; overflow: hidden;
  transition: box-shadow 0.25s ease;
}
.card:hover { box-shadow: 0 4px 16px rgba(0,0,0,0.06); }
.card-success { border-top: 3px solid var(--color-secondary-700, #3B6D11); }
.card-info { border-top: 3px solid var(--color-primary-500, #378ADD); }
.card-gps { border-top: 3px solid #0891b2; }
.card-audit { border-top: 3px solid var(--color-text-primary, #1E1E1C); }

.card-header {
  padding: 1rem 1.25rem; border-bottom: 1px solid var(--color-divider, #D3D1C7);
  display: flex; align-items: center; justify-content: space-between;
}
.card-header-left { display: flex; align-items: center; gap: 0.75rem; }
.card-header-left h3 { font-family: 'Young Serif', Georgia, serif; font-size: 0.95rem; margin: 0; color: var(--color-text-primary, #1E1E1C); }
.card-header-actions { display: flex; align-items: center; gap: 0.6rem; }

.card-header-dark {
  background: linear-gradient(135deg, #1E1E1C, #3a3a38);
  border-bottom: none;
}
.card-header-dark h3 { color: #fff; }

.card-icon {
  width: 32px; height: 32px; border-radius: 8px;
  display: flex; align-items: center; justify-content: center; color: white; flex-shrink: 0;
}
.card-success .card-icon { background: var(--color-secondary-700, #3B6D11); }
.card-info .card-icon { background: var(--color-primary-500, #378ADD); }
.card-icon-gps { background: #0891b2; }
.card-icon-audit { background: rgba(255,255,255,0.15); }

.card-body { padding: 1.25rem; }
.card-body.p-0 { padding: 0; }

/* ===== GPS Card Extras ===== */
.badge-gps {
  display: inline-flex; align-items: center; gap: 0.3rem;
  padding: 0.2rem 0.65rem; border-radius: 20px; font-size: 0.7rem; font-weight: 600;
  background: #ecfeff; color: #0891b2; border: 1px solid #a5f3fc;
}
.gps-description {
  display: flex; align-items: flex-start; gap: 0.5rem;
  padding: 0.65rem 0.85rem; margin-bottom: 1rem;
  background: #f0fdfa; border: 1px solid #ccfbf1; border-radius: 8px;
  font-size: 0.8rem; color: #0d9488; line-height: 1.45;
}
.gps-description svg { flex-shrink: 0; margin-top: 1px; }

.btn-gps {
  background: #0891b2; color: white; border: none;
}
.btn-gps:hover:not(:disabled) {
  background: #0e7490; transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(8, 145, 178, 0.3);
}

/* ===== Audit Card Extras ===== */
.badge-audit-count {
  display: inline-flex; align-items: center;
  padding: 0.2rem 0.6rem; border-radius: 20px; font-size: 0.7rem; font-weight: 600;
  background: rgba(255,255,255,0.12); color: rgba(255,255,255,0.8);
}
.btn-refresh { color: rgba(255,255,255,0.85); border-color: rgba(255,255,255,0.2); }
.btn-refresh:hover:not(:disabled) { background: rgba(255,255,255,0.1); border-color: rgba(255,255,255,0.35); color: white; }
.btn-refresh .spinner { border-color: rgba(255,255,255,0.25); border-top-color: white; }

.empty-state-audit {
  display: flex; flex-direction: column; align-items: center; gap: 0.6rem;
  padding: 2.5rem 1rem; color: var(--color-text-secondary, #5F5E5A);
}
.empty-state-audit p { margin: 0; font-size: 0.85rem; }

.user-cell { display: inline-flex; align-items: center; gap: 0.5rem; font-weight: 500; }
.user-avatar-mini {
  width: 24px; height: 24px; border-radius: 50%;
  background: var(--color-primary-200, #B5D4F4); color: var(--color-primary-700, #185FA5);
  display: flex; align-items: center; justify-content: center;
  font-size: 0.55rem; font-weight: 700; flex-shrink: 0;
}
.tabla-chip {
  padding: 0.15rem 0.5rem; background: var(--color-bg-subtle, #F8F7F4);
  border-radius: 5px; font-size: 0.72rem; font-weight: 500; color: var(--color-text-secondary, #5F5E5A);
  font-family: 'SF Mono', 'Fira Code', monospace;
}

.td-toggle { text-align: center; width: 48px; }
.btn-toggle-detail {
  width: 26px; height: 26px; border: none; background: var(--color-bg-subtle, #F8F7F4);
  border-radius: 6px; display: inline-flex; align-items: center; justify-content: center;
  color: var(--color-text-secondary, #5F5E5A); cursor: pointer;
  transition: all 0.2s;
}
.btn-toggle-detail:hover { background: var(--color-primary-50, #E6F1FB); color: var(--color-primary-700, #185FA5); }
.btn-toggle-detail svg { transition: transform 0.25s ease; }
.btn-toggle-detail.is-open svg { transform: rotate(180deg); }

.detail-row td {
  padding: 0 !important;
  background: var(--color-bg-subtle, #F8F7F4);
  border-bottom: 2px solid var(--color-divider, #D3D1C7);
}
.detail-content {
  display: flex; align-items: flex-start; gap: 1rem;
  padding: 1rem 1.25rem;
  animation: slideDown 0.2s ease;
}
.detail-col { flex: 1; min-width: 0; }
.detail-arrow {
  display: flex; align-items: center; padding-top: 1.5rem;
  color: var(--color-text-secondary, #5F5E5A); flex-shrink: 0;
}
.detail-label {
  display: block; font-size: 0.65rem; font-weight: 700; text-transform: uppercase;
  letter-spacing: 0.05em; color: var(--color-text-secondary, #5F5E5A); margin-bottom: 0.4rem;
}
.detail-value {
  padding: 0.6rem 0.8rem; border-radius: 6px; font-size: 0.78rem;
  font-family: 'SF Mono', 'Fira Code', monospace; line-height: 1.5;
  white-space: pre-wrap; word-break: break-word; margin: 0; overflow-x: auto;
}
.detail-value-old { background: #fef2f2; color: #991b1b; border: 1px solid #fecaca; }
.detail-value-new { background: #f0fdf4; color: #166534; border: 1px solid #bbf7d0; }

@keyframes slideDown {
  from { opacity: 0; transform: translateY(-6px); }
  to { opacity: 1; transform: translateY(0); }
}

/* ===== Forms ===== */
.form-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 1rem; }
.form-grid-3 { grid-template-columns: 1fr 1fr 1fr; }
@media (max-width: 700px) { .form-grid-3 { grid-template-columns: 1fr; } }
.form-group { display: flex; flex-direction: column; gap: 0.35rem; }
.form-group.full-width { grid-column: 1 / -1; }
.form-label { font-size: 0.75rem; font-weight: 600; color: var(--color-text-secondary, #5F5E5A); text-transform: uppercase; letter-spacing: 0.03em; }
.required { color: var(--color-error-accent, #A32D2D); }

.form-input {
  width: 100%; padding: 0.6rem 0.8rem;
  border: 1px solid var(--color-border, #B4B2A9); border-radius: 8px;
  font-size: 0.875rem; color: var(--color-text-primary, #1E1E1C);
  background: white; transition: all 0.2s; font-family: inherit; box-sizing: border-box;
}
.form-input:focus { outline: none; border-color: var(--color-primary-500, #378ADD); box-shadow: 0 0 0 3px rgba(55, 138, 222, 0.15); }

.input-prefix, .input-suffix { display: flex; align-items: center; }
.prefix, .suffix {
  padding: 0.6rem 0.75rem; background: var(--color-bg-subtle, #F8F7F4);
  border: 1px solid var(--color-border, #B4B2A9); font-size: 0.875rem;
  color: var(--color-text-secondary, #5F5E5A); font-weight: 500;
}
.prefix { border-right: none; border-radius: 8px 0 0 8px; }
.suffix { border-left: none; border-radius: 0 8px 8px 0; }
.prefix-input { border-radius: 0 8px 8px 0 !important; }
.suffix-input { border-radius: 8px 0 0 8px !important; }

textarea.form-input { resize: vertical; min-height: 70px; }

/* ===== Buttons ===== */
.btn {
  display: inline-flex; align-items: center; justify-content: center; gap: 0.5rem;
  padding: 0.65rem 1.25rem; border: none; border-radius: 8px;
  font-size: 0.875rem; font-weight: 600; cursor: pointer;
  transition: all 0.2s; font-family: inherit;
}
.btn:disabled { opacity: 0.6; cursor: not-allowed; }
.btn-primary { background: var(--color-primary-700, #185FA5); color: white; }
.btn-primary:hover:not(:disabled) { background: var(--color-primary-900, #042C53); transform: translateY(-1px); box-shadow: 0 4px 12px rgba(24, 95, 165, 0.3); }
.btn-block { width: 100%; }
.btn-sm { padding: 0.4rem 0.85rem; font-size: 0.8rem; }
.btn-outline { background: transparent; border: 1px solid var(--color-border, #B4B2A9); color: var(--color-text-secondary, #5F5E5A); }
.btn-outline:hover:not(:disabled) { border-color: var(--color-primary-500, #378ADD); color: var(--color-primary-700, #185FA5); background: var(--color-primary-50, #E6F1FB); }

/* ===== Table ===== */
.table-wrapper { overflow-x: auto; }
.data-table { width: 100%; border-collapse: collapse; }
.data-table th {
  background: var(--color-bg-subtle, #F8F7F4); padding: 0.75rem 1rem;
  font-size: 0.72rem; font-weight: 600; text-transform: uppercase;
  letter-spacing: 0.05em; color: var(--color-text-secondary, #5F5E5A);
  border-bottom: 2px solid var(--color-divider, #D3D1C7); white-space: nowrap; text-align: left;
}
.th-detail { text-align: center; width: 48px; }
.data-table td {
  padding: 0.75rem 1rem; font-size: 0.85rem;
  color: var(--color-text-primary, #1E1E1C);
  border-bottom: 1px solid var(--color-divider, #D3D1C7);
}
.text-mono { font-family: 'SF Mono', 'Fira Code', monospace; font-size: 0.78rem; }
.text-muted { color: var(--color-text-secondary, #5F5E5A); }

.data-row {
  opacity: 0; transform: translateY(8px);
  animation: fadeInRow 0.35s ease forwards;
  animation-delay: calc(var(--i, 0) * 60ms);
  transition: background 0.2s, transform 0.15s;
  cursor: pointer;
}
.data-row:hover { background: var(--color-primary-50, #E6F1FB); }
.data-row:active { transform: scale(0.995); }
.data-row:last-child td { border-bottom: none; }

@keyframes fadeInRow {
  from { opacity: 0; transform: translateY(8px); }
  to { opacity: 1; transform: translateY(0); }
}
@media (prefers-reduced-motion: reduce) {
  .data-row { animation: none; opacity: 1; transform: none; }
}

/* ===== Badges (scoped overrides) ===== */
.badge {
  display: inline-flex; align-items: center; gap: 0.25rem;
  padding: 0.2rem 0.6rem; border-radius: 20px;
  font-size: 0.72rem; font-weight: 600; white-space: nowrap;
}
.badge-success { background: var(--color-success-bg, #EAF3DE); color: var(--color-success-accent, #3B6D11); }
.badge-warning { background: var(--color-warning-bg, #FAEEDA); color: var(--color-warning-accent, #854F0B); }
.badge-error { background: var(--color-error-bg, #FCEBEB); color: var(--color-error-accent, #A32D2D); }
.badge-info { background: var(--color-info-bg, #E6F1FB); color: var(--color-info-accent, #185FA5); }
.badge-neutral { background: var(--color-bg-subtle, #F8F7F4); color: var(--color-text-secondary, #5F5E5A); border: 1px solid var(--color-divider, #D3D1C7); }

/* ===== Role / Access Control Table ===== */
.role-badge {
  display: inline-flex; align-items: center; gap: 0.4rem;
  padding: 0.3rem 0.7rem; border-radius: 8px;
  font-size: 0.8rem; font-weight: 600; white-space: nowrap;
}
.role-dot { width: 7px; height: 7px; border-radius: 50%; flex-shrink: 0; }

.role-modules { display: flex; flex-wrap: wrap; gap: 0.35rem; }
.module-chip {
  padding: 0.2rem 0.5rem; background: var(--color-bg-subtle, #F8F7F4);
  border-radius: 5px; font-size: 0.72rem; color: var(--color-text-secondary, #5F5E5A); font-weight: 500;
}

.color-swatch {
  font-family: 'SF Mono', 'Fira Code', monospace; font-size: 0.75rem;
  padding: 0.2rem 0.6rem; border-radius: 5px; color: white; font-weight: 500;
}

/* ===== Responsive ===== */
@media (max-width: 640px) {
  .page-header-content { flex-direction: column; text-align: center; }
  .form-grid { grid-template-columns: 1fr; }
  .role-modules { flex-direction: column; }
  .detail-content { flex-direction: column; gap: 0.75rem; }
  .detail-arrow { display: none; }
  .card-header { flex-direction: column; gap: 0.5rem; align-items: flex-start; }
  .card-header-actions { width: 100%; justify-content: flex-end; }
}
</style>
