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

    <div class="grid-2">
      <!-- SMMLV Configuration -->
      <div class="card card-success">
        <div class="card-header">
          <div class="card-header-left">
            <span class="card-icon">
              <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <path d="M12 1a3 3 0 0 0-3 3v8a3 3 0 0 0 6 0V4a3 3 0 0 0-3-3z"/>
                <path d="M19 10v2a7 7 0 0 1-14 0v-2"/>
                <line x1="12" y1="19" x2="12" y2="23"/>
                <line x1="8" y1="23" x2="16" y2="23"/>
              </svg>
            </span>
            <h3>Parametrización SMMLV</h3>
          </div>
        </div>
        <div class="card-body">
          <form @submit.prevent="actualizarSMMLV" class="form-grid">
            <div class="form-group">
              <label class="form-label">SMMLV <span class="required">*</span></label>
              <div class="input-prefix">
                <span class="prefix">$</span>
                <input type="number" v-model.number="config.smmlv" required min="0" class="form-input prefix-input">
              </div>
            </div>
            <div class="form-group">
              <label class="form-label">Vigencia <span class="required">*</span></label>
              <input type="date" v-model="config.fechaVigencia" required class="form-input">
            </div>
            <div class="form-group full-width">
              <label class="form-label">Observaciones</label>
              <textarea v-model="config.observaciones" rows="3" class="form-input" placeholder="Notas sobre esta configuración..."></textarea>
            </div>
            <div class="form-group full-width">
              <button type="submit" class="btn btn-primary btn-block">
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M19 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h11l5 5v11a2 2 0 0 1-2 2z"/><polyline points="17 21 17 13 7 13 7 21"/><polyline points="7 3 7 8 15 8"/></svg>
                Actualizar SMMLV
              </button>
            </div>
          </form>
          <transition name="fade">
            <div v-if="configActualizada" class="alert alert-success">
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="20 6 9 17 4 12"/></svg>
              Configuración actualizada — {{ ultimaActualizacion }}
            </div>
          </transition>
        </div>
      </div>

      <!-- Contribution Rates -->
      <div class="card card-info">
        <div class="card-header">
          <div class="card-header-left">
            <span class="card-icon">
              <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <line x1="12" y1="1" x2="12" y2="23"/><path d="M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6"/>
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
              <button type="submit" class="btn btn-primary btn-block">
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M19 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h11l5 5v11a2 2 0 0 1-2 2z"/><polyline points="17 21 17 13 7 13 7 21"/><polyline points="7 3 7 8 15 8"/></svg>
                Actualizar Porcentajes
              </button>
            </div>
          </form>
          <transition name="fade">
            <div v-if="porcentajesActualizados" class="alert alert-info">
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="20 6 9 17 4 12"/></svg>
              Porcentajes actualizados exitosamente
            </div>
          </transition>
        </div>
      </div>
    </div>

    <!-- Access Control Summary -->
    <div class="card" style="margin-top: 1.5rem;">
      <div class="card-header">
        <div class="card-header-left">
          <span class="card-icon" style="background: var(--color-neutral-text-primary);">
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
              <tr v-for="rol in roles" :key="rol.nombre" class="data-row">
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
  </div>
</template>

<script>
import { ref } from 'vue'

export default {
  setup() {
    const config = ref({ smmlv: 1160000, fechaVigencia: '2024-01-01', observaciones: 'Valor SMMLV 2024 legalmente establecido' })
    const porcentajes = ref({ salud: 4.0, pension: 4.0, arl: 0.5 })
    const configActualizada = ref(false)
    const porcentajesActualizados = ref(false)
    const ultimaActualizacion = ref('')

    const roles = [
      { nombre: 'Administrador RRHH', color: '#185FA5', modulos: ['Gestión empleados', 'Desprendibles', 'Credenciales', 'Aprobación manual'] },
      { nombre: 'Empleado', color: '#378ADD', modulos: ['Registro asistencia', 'Portal personal'] },
      { nombre: 'Contador', color: '#3B6D11', modulos: ['Liquidación nómina', 'Exportación ACH/Excel'] },
      { nombre: 'Gerente', color: '#042C53', modulos: ['Dashboard reportes', 'Reportes filtrables'] },
      { nombre: 'Admin. Sistema', color: '#2C2C2A', modulos: ['Auditoría', 'Parametrización', 'Control acceso'] }
    ]

    const actualizarSMMLV = () => {
      configActualizada.value = true
      ultimaActualizacion.value = new Date().toLocaleString()
      setTimeout(() => { configActualizada.value = false }, 4000)
    }

    const actualizarPorcentajes = () => {
      porcentajesActualizados.value = true
      setTimeout(() => { porcentajesActualizados.value = false }, 4000)
    }

    return { config, porcentajes, configActualizada, porcentajesActualizados, ultimaActualizacion, roles, actualizarSMMLV, actualizarPorcentajes }
  }
}
</script>

<style scoped>
.page-container { max-width: 1000px; margin: 0 auto; }

.page-header { margin-bottom: 2rem; }
.page-header-content { display: flex; align-items: center; gap: 1rem; }
.page-header-icon { width: 44px; height: 44px; background: var(--color-primary-50); color: var(--color-primary-700); border-radius: 12px; display: flex; align-items: center; justify-content: center; flex-shrink: 0; }
.page-title { font-family: 'Young Serif', Georgia, serif; font-size: 1.5rem; color: var(--color-neutral-text-primary); margin: 0; }
.page-description { color: var(--color-neutral-text-secondary); margin: 0.15rem 0 0 0; font-size: 0.875rem; }

.grid-2 { display: grid; grid-template-columns: 1fr 1fr; gap: 1.5rem; }
@media (max-width: 800px) { .grid-2 { grid-template-columns: 1fr; } }

.card { background: white; border: 1px solid var(--color-neutral-divider); border-radius: 12px; overflow: hidden; }
.card-success { border-top: 3px solid var(--color-secondary-700); }
.card-info { border-top: 3px solid var(--color-primary-500); }

.card-header { padding: 1rem 1.25rem; border-bottom: 1px solid var(--color-neutral-divider); display: flex; align-items: center; justify-content: space-between; }
.card-header-left { display: flex; align-items: center; gap: 0.75rem; }
.card-header-left h3 { font-family: 'Young Serif', Georgia, serif; font-size: 0.95rem; margin: 0; color: var(--color-neutral-text-primary); }

.card-icon { width: 32px; height: 32px; border-radius: 8px; display: flex; align-items: center; justify-content: center; color: white; flex-shrink: 0; }
.card-success .card-icon { background: var(--color-secondary-700); }
.card-info .card-icon { background: var(--color-primary-500); }

.card-body { padding: 1.25rem; }
.card-body.p-0 { padding: 0; }

/* Form */
.form-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 1rem; }
.form-group { display: flex; flex-direction: column; gap: 0.35rem; }
.form-group.full-width { grid-column: 1 / -1; }
.form-label { font-size: 0.75rem; font-weight: 600; color: var(--color-neutral-text-secondary); text-transform: uppercase; letter-spacing: 0.03em; }
.required { color: var(--color-error-accent); }

.form-input { width: 100%; padding: 0.6rem 0.8rem; border: 1px solid var(--color-neutral-border); border-radius: 8px; font-size: 0.875rem; color: var(--color-neutral-text-primary); background: white; transition: all 0.2s; font-family: inherit; box-sizing: border-box; }
.form-input:focus { outline: none; border-color: var(--color-primary-500); box-shadow: 0 0 0 3px rgba(55, 138, 222, 0.15); }

.input-prefix, .input-suffix { display: flex; align-items: center; }
.prefix, .suffix { padding: 0.6rem 0.75rem; background: var(--color-neutral-bg-page); border: 1px solid var(--color-neutral-border); font-size: 0.875rem; color: var(--color-neutral-text-secondary); font-weight: 500; }
.prefix { border-right: none; border-radius: 8px 0 0 8px; }
.suffix { border-left: none; border-radius: 0 8px 8px 0; }
.prefix-input { border-radius: 0 8px 8px 0 !important; }
.suffix-input { border-radius: 8px 0 0 8px !important; }

textarea.form-input { resize: vertical; min-height: 70px; }

/* Buttons */
.btn { display: inline-flex; align-items: center; justify-content: center; gap: 0.5rem; padding: 0.65rem 1.25rem; border: none; border-radius: 8px; font-size: 0.875rem; font-weight: 600; cursor: pointer; transition: all 0.2s; font-family: inherit; }
.btn-primary { background: var(--color-primary-700); color: white; }
.btn-primary:hover { background: var(--color-primary-900); transform: translateY(-1px); box-shadow: 0 4px 12px rgba(24, 95, 165, 0.3); }
.btn-block { width: 100%; }

/* Alert */
.alert { display: flex; align-items: center; gap: 0.5rem; padding: 0.75rem 1rem; border-radius: 8px; margin-top: 1rem; font-size: 0.825rem; font-weight: 500; }
.alert-success { background: var(--color-semantic-success-bg, #EAF3DE); color: var(--color-semantic-success-accent, #3B6D11); border: 1px solid rgba(59, 109, 17, 0.15); }
.alert-info { background: var(--color-semantic-info-bg, #E6F1FB); color: var(--color-semantic-info-accent, #185FA5); border: 1px solid rgba(24, 95, 165, 0.15); }

.fade-enter-active, .fade-leave-active { transition: all 0.3s; }
.fade-enter-from, .fade-leave-to { opacity: 0; transform: translateY(-4px); }

/* Table */
.table-wrapper { overflow-x: auto; }
.data-table { width: 100%; border-collapse: collapse; }
.data-table th { background: var(--color-neutral-bg-page); padding: 0.75rem 1rem; font-size: 0.72rem; font-weight: 600; text-transform: uppercase; letter-spacing: 0.05em; color: var(--color-neutral-text-secondary); border-bottom: 2px solid var(--color-neutral-divider); }
.data-table td { padding: 0.75rem 1rem; font-size: 0.85rem; color: var(--color-neutral-text-primary); border-bottom: 1px solid var(--color-neutral-divider); }
.data-row { transition: background 0.15s; }
.data-row:hover { background: var(--color-primary-50); }
.data-row:last-child td { border-bottom: none; }

.role-badge { display: inline-flex; align-items: center; gap: 0.4rem; padding: 0.3rem 0.7rem; border-radius: 8px; font-size: 0.8rem; font-weight: 600; white-space: nowrap; }
.role-dot { width: 7px; height: 7px; border-radius: 50%; flex-shrink: 0; }

.role-modules { display: flex; flex-wrap: wrap; gap: 0.35rem; }
.module-chip { padding: 0.2rem 0.5rem; background: var(--color-neutral-bg-page); border-radius: 5px; font-size: 0.72rem; color: var(--color-neutral-text-secondary); font-weight: 500; }

.color-swatch { font-family: 'Space Mono', monospace; font-size: 0.75rem; padding: 0.2rem 0.6rem; border-radius: 5px; color: white; font-weight: 500; }

@media (max-width: 640px) {
  .page-header-content { flex-direction: column; text-align: center; }
  .form-grid { grid-template-columns: 1fr; }
  .role-modules { flex-direction: column; }
}
</style>
