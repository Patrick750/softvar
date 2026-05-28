<template>
  <div class="page-container">
    <div class="page-header">
      <div class="page-header-content">
        <div class="page-header-icon">
          <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/>
            <polyline points="14 2 14 8 20 8"/>
            <line x1="16" y1="13" x2="8" y2="13"/>
            <line x1="16" y1="17" x2="8" y2="17"/>
            <polyline points="10 9 9 9 8 9"/>
          </svg>
        </div>
        <div>
          <h1 class="page-title">Desprendibles de Pago PDF</h1>
          <p class="page-description">Genere y envíe desprendibles de nómina por correo electrónico</p>
        </div>
      </div>
    </div>

    <!-- Filtros de período -->
    <div class="card card-info mb-4">
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
          <h3>Filtrar por Período</h3>
        </div>
      </div>
      <div class="card-body">
        <div class="filtros-grid">
          <div class="form-group">
            <label class="form-label">Mes <span class="required">*</span></label>
            <div class="select-wrapper">
              <select v-model="filtro.mes" class="form-select">
                <option value="">Seleccione mes</option>
                <option v-for="(name, key) in meses" :key="key" :value="key">{{ name }}</option>
              </select>
              <svg class="select-chevron" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="6 9 12 15 18 9"/></svg>
            </div>
          </div>
          <div class="form-group">
            <label class="form-label">Año <span class="required">*</span></label>
            <input type="number" v-model.number="filtro.ano" min="2020" max="2030" class="form-input">
          </div>
          <div class="form-group form-actions">
            <label class="form-label">&nbsp;</label>
            <button class="btn btn-primary" @click="cargarLiquidaciones" :disabled="cargando">
              <span v-if="cargando" class="spinner"></span>
              <svg v-else width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="11" cy="11" r="8"/><line x1="21" y1="21" x2="16.65" y2="16.65"/></svg>
              Buscar Liquidaciones
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Tabla de Liquidaciones -->
    <div class="card" v-if="liquidaciones.length > 0">        <div class="card-header">
        <div class="card-header-left">
          <span class="card-icon card-icon-blue">
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="white" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/>
            </svg>
          </span>
          <h3>Liquidaciones del Período</h3>
        </div>
        <div class="card-header-right">
          <span class="badge badge-info me-2">{{ liquidaciones.length }} empleados</span>
          <button
            class="btn btn-sm btn-primary"
            @click="enviarTodos"
            :disabled="enviandoTodos || liquidaciones.length === 0"
            title="Enviar todos los desprendibles de este período"
          >
            <span v-if="enviandoTodos" class="spinner spinner-sm"></span>
            <svg v-else width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z"/>
              <polyline points="22,6 12,13 2,6"/>
            </svg>
            Enviar Todos
          </button>
        </div>
      </div>
      <div class="card-body p-0">
        <div class="table-wrapper">
          <table class="data-table">
            <thead>
              <tr>
                <th>Empleado</th>
                <th>Cédula</th>
                <th class="text-right">Devengado</th>
                <th class="text-right">Deducciones</th>
                <th class="text-right">Neto a Pagar</th>
                <th class="text-center">Estado Desprendible</th>
                <th class="text-center">Acciones</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="(liq, idx) in liquidaciones" :key="liq.id" class="data-row" :style="{ '--i': idx }">
                <td><span class="employee-name">{{ liq.empleado_nombre }}</span></td>
                <td class="text-muted">{{ liq.empleado_cedula }}</td>
                <td class="text-right">{{ formatoMoneda(liq.total_devengado) }}</td>
                <td class="text-right">{{ formatoMoneda(liq.total_deducciones) }}</td>
                <td class="text-right net-pay">{{ formatoMoneda(liq.neto_pagar) }}</td>
                <td class="text-center">
                  <span class="badge" :class="getEstadoBadge(liq.id)">
                    {{ getEstadoTexto(liq.id) }}
                  </span>
                </td>
                <td class="text-center">
                  <div class="action-btns">
                    <button
                      class="btn btn-sm btn-outline btn-action"
                      @click="generarDesprendible(liq)"
                      :disabled="generandoId === liq.id"
                      title="Generar PDF"
                    >
                      <span v-if="generandoId === liq.id" class="spinner spinner-sm"></span>
                      <svg v-else width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/><line x1="16" y1="13" x2="8" y2="13"/><line x1="16" y1="17" x2="8" y2="17"/></svg>
                      Generar
                    </button>
                    <button
                      class="btn btn-sm btn-outline-success btn-action"
                      @click="enviarDesprendible(liq)"
                      :disabled="enviandoId === liq.id || !tieneDesprendibleGenerado(liq.id)"
                      title="Enviar por correo"
                    >
                      <span v-if="enviandoId === liq.id" class="spinner spinner-sm"></span>
                      <svg v-else width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z"/><polyline points="22,6 12,13 2,6"/></svg>
                      Enviar
                    </button>
                    <button
                      v-if="tienePdfDescargable(liq.id)"
                      class="btn btn-sm btn-ghost btn-action"
                      @click="descargarPdf(liq)"
                      title="Descargar PDF"
                    >
                      <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="7 10 12 15 17 10"/><line x1="12" y1="15" x2="12" y2="3"/></svg>
                    </button>
                  </div>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>

    <!-- Modal de resultado de envío masivo -->
    <Teleport to="body">
      <div v-if="resumenVisible" class="modal-overlay" @click.self="resumenVisible = false">
        <div class="modal-card">
          <div class="modal-header">
            <div class="modal-header-content">
              <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="var(--color-primary-700)" stroke-width="2">
                <path d="M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z"/>
                <polyline points="22,6 12,13 2,6"/>
              </svg>
              <h3>Resultado de Envío Masivo</h3>
            </div>
            <button class="modal-close" @click="resumenVisible = false">
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/>
              </svg>
            </button>
          </div>
          <div class="modal-body">
            <div class="resumen-grid">
              <div class="resumen-card resumen-total">
                <span class="resumen-number">{{ resumenDatos.total }}</span>
                <span class="resumen-label">Total empleados</span>
              </div>
              <div class="resumen-card resumen-success">
                <span class="resumen-number">{{ resumenDatos.enviados }}</span>
                <span class="resumen-label">Enviados</span>
              </div>
              <div class="resumen-card resumen-error">
                <span class="resumen-number">{{ resumenDatos.fallidos }}</span>
                <span class="resumen-label">Fallidos</span>
              </div>
            </div>

            <div v-if="resumenDatos.fallidos > 0" class="detalle-fallidos">
              <h4>Detalle de errores</h4>
              <div class="fallido-item" v-for="r in resumenDatos.resultadosFallidos" :key="r.empleado_id">
                <span class="fallido-nombre">{{ r.empleado_nombre }}</span>
                <span class="fallido-error">{{ r.error }}</span>
              </div>
            </div>
          </div>
          <div class="modal-footer">
            <button class="btn btn-primary" @click="resumenVisible = false">
              Cerrar
            </button>
          </div>
        </div>
      </div>
    </Teleport>

    <!-- Empty state -->
    <div v-else-if="!cargando && busquedaRealizada" class="empty-state-card">
      <svg width="64" height="64" viewBox="0 0 24 24" fill="none" stroke="var(--color-neutral-border)" stroke-width="1">
        <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/><line x1="16" y1="13" x2="8" y2="13"/><line x1="16" y1="17" x2="8" y2="17"/>
      </svg>
      <h3>No hay liquidaciones para este período</h3>
      <p>Genere primero la nómina desde el módulo de Liquidación de Nómina.</p>
    </div>

    <div v-else-if="!cargando && !busquedaRealizada" class="empty-state-card">
      <svg width="64" height="64" viewBox="0 0 24 24" fill="none" stroke="var(--color-neutral-border)" stroke-width="1">
        <circle cx="11" cy="11" r="8"/><line x1="21" y1="21" x2="16.65" y2="16.65"/>
      </svg>
      <h3>Seleccione un período para comenzar</h3>
      <p>Elija el mes y año y haga clic en "Buscar Liquidaciones".</p>
    </div>
  </div>
</template>

<script>
import { ref, reactive, computed, inject } from 'vue'
import axios from 'axios'

export default {
  setup() {
    const addToast = inject('addToast', () => {})

    const meses = {
      1: 'Enero', 2: 'Febrero', 3: 'Marzo', 4: 'Abril',
      5: 'Mayo', 6: 'Junio', 7: 'Julio', 8: 'Agosto',
      9: 'Septiembre', 10: 'Octubre', 11: 'Noviembre', 12: 'Diciembre'
    }

    const filtro = reactive({ mes: new Date().getMonth() + 1, ano: new Date().getFullYear() })
    const liquidaciones = ref([])
    const cargando = ref(false)
    const busquedaRealizada = ref(false)
    const generandoId = ref(null)
    const enviandoId = ref(null)

    const enviandoTodos = ref(false)
    const resumenVisible = ref(false)
    const resumenDatos = ref({ total: 0, enviados: 0, fallidos: 0, resultadosFallidos: [] })

    // Estado de desprendibles por liquidación (key: liquidacion_id, value: { estado, desprendible_id, pdf_base64 })
    const desprendiblesMap = ref({})

    const getPeriodoStr = () => `${filtro.ano}-${String(filtro.mes).padStart(2, '0')}`

    const cargarLiquidaciones = async () => {
      if (!filtro.mes || !filtro.ano) return
      cargando.value = true
      busquedaRealizada.value = true

      try {
        const { data } = await axios.get(`/api/nomina/liquidaciones/?periodo=${getPeriodoStr()}`)
        liquidaciones.value = Array.isArray(data) ? data : []
      } catch (err) {
        console.error('Error cargando liquidaciones:', err)
        addToast('Error', 'No se pudieron cargar las liquidaciones.', 'error')
      } finally {
        cargando.value = false
      }
    }

    const getEstadoTexto = (liquidacionId) => {
      const info = desprendiblesMap.value[liquidacionId]
      return info?.estado || 'Pendiente'
    }

    const getEstadoBadge = (liquidacionId) => {
      const estado = desprendiblesMap.value[liquidacionId]?.estado
      if (estado === 'ENVIADO') return 'badge-success'
      if (estado === 'GENERADO') return 'badge-warning'
      if (estado === 'FALLIDO') return 'badge-error'
      return 'badge-neutral'
    }

    const tieneDesprendibleGenerado = (liquidacionId) => {
      const estado = desprendiblesMap.value[liquidacionId]?.estado
      return estado === 'GENERADO' || estado === 'ENVIADO'
    }

    const tienePdfDescargable = (liquidacionId) => {
      const estado = desprendiblesMap.value[liquidacionId]?.estado
      return estado === 'GENERADO' || estado === 'ENVIADO'
    }

    const generarDesprendible = async (liquidacion) => {
      generandoId.value = liquidacion.id
      try {
        const { data } = await axios.post('/api/desprendibles/generar/', {
          liquidacion_id: liquidacion.id
        })

        desprendiblesMap.value = {
          ...desprendiblesMap.value,
          [liquidacion.id]: {
            estado: 'GENERADO',
            desprendible_id: data.desprendible_id,
          }
        }

        // Guardar el desprendible_id y PDF en sessionStorage para descarga/envío
        if (data.desprendible_id) {
          sessionStorage.setItem(`desprendible_id_${liquidacion.id}`, data.desprendible_id)
        }
        if (data.pdf_base64) {
          sessionStorage.setItem(`pdf_${liquidacion.id}`, data.pdf_base64)
        }

        addToast('Éxito', `Desprendible generado para ${liquidacion.empleado_nombre}.`, 'success')
      } catch (err) {
        console.error('Error generando desprendible:', err)
        addToast('Error', err.response?.data?.error || 'Error generando desprendible.', 'error')
      } finally {
        generandoId.value = null
      }
    }

    const enviarDesprendible = async (liquidacion) => {
      enviandoId.value = liquidacion.id
      try {
        // Obtener o generar el desprendible
        let desprendibleId = desprendiblesMap.value[liquidacion.id]?.desprendible_id
          || sessionStorage.getItem(`desprendible_id_${liquidacion.id}`)

        if (!desprendibleId) {
          // Generar primero
          const genResp = await axios.post('/api/desprendibles/generar/', {
            liquidacion_id: liquidacion.id
          })
          desprendibleId = genResp.data.desprendible_id
          sessionStorage.setItem(`desprendible_id_${liquidacion.id}`, desprendibleId)
          if (genResp.data.pdf_base64) {
            sessionStorage.setItem(`pdf_${liquidacion.id}`, genResp.data.pdf_base64)
          }
        }

        const { data } = await axios.post('/api/desprendibles/enviar/', {
          desprendible_id: desprendibleId
        })

        desprendiblesMap.value = {
          ...desprendiblesMap.value,
          [liquidacion.id]: {
            estado: 'ENVIADO',
            desprendible_id: desprendibleId,
          }
        }

        addToast('Éxito', `Desprendible enviado a ${liquidacion.empleado_nombre}.`, 'success')
      } catch (err) {
        console.error('Error enviando desprendible:', err)
        addToast('Error', err.response?.data?.error || 'Error enviando desprendible.', 'error')
      } finally {
        enviandoId.value = null
      }
    }

    const descargarPdf = (liquidacion) => {
      const pdfBase64 = sessionStorage.getItem(`pdf_${liquidacion.id}`)
      if (pdfBase64) {
        const byteCharacters = atob(pdfBase64)
        const byteNumbers = new Array(byteCharacters.length)
        for (let i = 0; i < byteCharacters.length; i++) {
          byteNumbers[i] = byteCharacters.charCodeAt(i)
        }
        const byteArray = new Uint8Array(byteNumbers)
        const blob = new Blob([byteArray], { type: 'application/pdf' })
        const url = URL.createObjectURL(blob)
        const a = document.createElement('a')
        a.href = url
        a.download = `desprendible_${liquidacion.empleado_nombre.replace(/\s+/g, '_')}_${getPeriodoStr()}.pdf`
        document.body.appendChild(a)
        a.click()
        document.body.removeChild(a)
        URL.revokeObjectURL(url)
      } else {
        addToast('Info', 'Primero debe generar el desprendible.', 'info')
      }
    }

    const formatoMoneda = (v) => new Intl.NumberFormat('es-CO', { style: 'currency', currency: 'COP' }).format(parseFloat(v || 0))

    const enviarTodos = async () => {
      const periodo = getPeriodoStr()
      if (!confirm(`¿Enviar desprendibles de nómina a todos los empleados del período ${periodo}?`)) return

      enviandoTodos.value = true
      try {
        const { data } = await axios.post('/api/desprendibles/enviar-masivo/', {
          periodo: periodo
        })

        // Actualizar el estado de todos los desprendibles en el mapa
        const nuevosEstados = { ...desprendiblesMap.value }
        data.resultados.forEach(r => {
          // Encontrar la liquidación por empleado_id
          const liq = liquidaciones.value.find(l => l.empleado_id === r.empleado_id)
          if (liq) {
            // Obtener el desprendible_id desde sessionStorage o dejarlo pendiente
            const existingId = sessionStorage.getItem(`desprendible_id_${liq.id}`)
            nuevosEstados[liq.id] = {
              estado: r.estado === 'ENVIADO' ? 'ENVIADO' : 'FALLIDO',
              desprendible_id: existingId || null,
            }
          }
        })
        desprendiblesMap.value = nuevosEstados

        // Mostrar resumen
        resumenDatos.value = {
          total: data.total,
          enviados: data.enviados,
          fallidos: data.fallidos,
          resultadosFallidos: data.resultados.filter(r => r.estado === 'FALLIDO'),
        }
        resumenVisible.value = true

        addToast(
          'Éxito',
          `Envío masivo completado: ${data.enviados} enviados, ${data.fallidos} fallidos.`,
          data.fallidos > 0 ? 'warning' : 'success'
        )
      } catch (err) {
        const msg = err.response?.data?.error || 'Error en envío masivo'
        addToast('Error', msg, 'error')
      } finally {
        enviandoTodos.value = false
      }
    }

    return {
      meses, filtro, liquidaciones, cargando, busquedaRealizada,
      generandoId, enviandoId, desprendiblesMap,
      enviandoTodos, resumenVisible, resumenDatos,
      cargarLiquidaciones, generarDesprendible, enviarDesprendible, descargarPdf, enviarTodos,
      getEstadoTexto, getEstadoBadge, tieneDesprendibleGenerado, tienePdfDescargable,
      formatoMoneda
    }
  }
}
</script>

<style scoped>
.page-container { max-width: 1400px; margin: 0 auto; }

.page-header { margin-bottom: 2rem; }
.page-header-content { display: flex; align-items: center; gap: 1rem; }
.page-header-icon {
  width: 44px; height: 44px;
  background: var(--color-primary-50); color: var(--color-primary-700);
  border-radius: 12px; display: flex; align-items: center; justify-content: center; flex-shrink: 0;
}
.page-title { font-family: 'Young Serif', Georgia, serif; font-size: 1.5rem; color: var(--color-neutral-text-primary); margin: 0; }
.page-description { color: var(--color-neutral-text-secondary); margin: 0.15rem 0 0 0; font-size: 0.875rem; }

.mb-4 { margin-bottom: 1.5rem; }

.card {
  background: white; border: 1px solid var(--color-neutral-divider);
  border-radius: 12px; overflow: hidden;
}
.card-info { border-top: 3px solid var(--color-primary-500); }

.card-header {
  padding: 1rem 1.5rem; border-bottom: 1px solid var(--color-neutral-divider);
  display: flex; align-items: center; justify-content: space-between;
}
.card-header-left { display: flex; align-items: center; gap: 0.75rem; }
.card-header-left h3 { font-family: 'Young Serif', Georgia, serif; font-size: 1rem; margin: 0; color: var(--color-neutral-text-primary); }

.card-header-right {
  display: flex; align-items: center; gap: 0.75rem;
}

.me-2 { margin-right: 0.5rem; }

.card-icon {
  width: 32px; height: 32px; border-radius: 8px;
  display: flex; align-items: center; justify-content: center; color: white; flex-shrink: 0;
}
.card-info .card-icon { background: var(--color-primary-500); }
.card-icon-blue { background: var(--color-primary-500); }

.card-body { padding: 1.5rem; }
.card-body.p-0 { padding: 0; }

.filtros-grid {
  display: grid;
  grid-template-columns: 1fr 1fr 1fr;
  gap: 1rem;
  align-items: end;
}

@media (max-width: 700px) {
  .filtros-grid { grid-template-columns: 1fr; }
}

.form-group { display: flex; flex-direction: column; gap: 0.35rem; }
.form-label { font-size: 0.8rem; font-weight: 600; color: var(--color-neutral-text-secondary); text-transform: uppercase; letter-spacing: 0.03em; }
.required { color: var(--color-error-accent); }

.form-input, .form-select {
  width: 100%; padding: 0.65rem 0.85rem;
  border: 1px solid var(--color-neutral-border); border-radius: 8px;
  font-size: 0.9rem; color: var(--color-neutral-text-primary);
  background: white; transition: all 0.2s; font-family: inherit; box-sizing: border-box;
}
.form-input:focus, .form-select:focus {
  outline: none; border-color: var(--color-primary-500);
  box-shadow: 0 0 0 3px rgba(55, 138, 222, 0.15);
}
.select-wrapper { position: relative; }
.select-chevron {
  position: absolute; right: 10px; top: 50%; transform: translateY(-50%);
  pointer-events: none; color: var(--color-neutral-text-secondary);
}
.form-select { appearance: none; padding-right: 2rem; }

.btn {
  display: inline-flex; align-items: center; justify-content: center; gap: 0.5rem;
  padding: 0.65rem 1.25rem; border: none; border-radius: 8px;
  font-size: 0.875rem; font-weight: 600; cursor: pointer;
  transition: all 0.2s; font-family: inherit;
}
.btn:disabled { opacity: 0.6; cursor: not-allowed; }
.btn-primary { background: var(--color-primary-700); color: white; }
.btn-primary:hover:not(:disabled) { background: var(--color-primary-900); transform: translateY(-1px); box-shadow: 0 4px 12px rgba(24, 95, 165, 0.3); }
.btn-sm { padding: 0.4rem 0.85rem; font-size: 0.8rem; }
.btn-outline { background: transparent; border: 1px solid var(--color-neutral-border); color: var(--color-neutral-text-secondary); }
.btn-outline:hover:not(:disabled) { border-color: var(--color-primary-500); color: var(--color-primary-700); background: var(--color-primary-50); }
.btn-outline-success { background: transparent; border: 1px solid var(--color-secondary-500); color: var(--color-secondary-700); }
.btn-outline-success:hover:not(:disabled) { background: var(--color-secondary-50); }
.btn-ghost { background: transparent; border: 1px solid transparent; color: var(--color-neutral-text-secondary); }
.btn-ghost:hover:not(:disabled) { background: var(--color-bg-subtle); }

.form-actions .btn { width: 100%; }

.spinner {
  width: 16px; height: 16px;
  border: 2px solid rgba(255,255,255,0.3); border-top-color: white;
  border-radius: 50%; animation: spin 0.6s linear infinite;
}
.spinner-sm { width: 14px; height: 14px; border-width: 2px; border-color: var(--color-neutral-border); border-top-color: var(--color-primary-700); }
@keyframes spin { to { transform: rotate(360deg); } }

/* Table */
.table-wrapper { overflow-x: auto; }
.data-table { width: 100%; border-collapse: collapse; }
.data-table th {
  background: var(--color-neutral-bg-page); padding: 0.85rem 1rem;
  font-size: 0.75rem; font-weight: 600; text-transform: uppercase;
  letter-spacing: 0.05em; color: var(--color-neutral-text-secondary);
  border-bottom: 2px solid var(--color-neutral-divider); white-space: nowrap;
}
.data-table td {
  padding: 0.85rem 1rem; font-size: 0.875rem;
  color: var(--color-neutral-text-primary);
  border-bottom: 1px solid var(--color-neutral-divider);
}
.data-row {
  opacity: 0; transform: translateY(8px);
  animation: fadeInRow 0.35s ease forwards;
  animation-delay: calc(var(--i, 0) * 60ms);
  transition: background 0.2s, transform 0.15s;
}
.data-row:hover { background: var(--color-primary-50); }
.data-row:last-child td { border-bottom: none; }

@keyframes fadeInRow {
  from { opacity: 0; transform: translateY(8px); }
  to { opacity: 1; transform: translateY(0); }
}
@media (prefers-reduced-motion: reduce) {
  .data-row { animation: none; opacity: 1; transform: none; }
}

.text-right { text-align: right; }
.text-center { text-align: center; }
.text-muted { color: var(--color-neutral-text-secondary); }

.employee-name { font-weight: 600; }
.net-pay { font-weight: 700; color: var(--color-secondary-700); }

.action-btns {
  display: flex; align-items: center; justify-content: center; gap: 0.35rem;
}

.btn-action { min-width: 75px; justify-content: center; }

.badge {
  display: inline-flex; align-items: center;
  padding: 0.25rem 0.75rem; border-radius: 20px;
  font-size: 0.75rem; font-weight: 600;
}
.badge-success { background: var(--color-success-bg); color: var(--color-success-accent); }
.badge-warning { background: var(--color-warning-bg); color: var(--color-warning-accent); }
.badge-error { background: var(--color-error-bg); color: var(--color-error-accent); }
.badge-neutral { background: var(--color-bg-subtle); color: var(--color-neutral-text-secondary); border: 1px solid var(--color-neutral-divider); }
.badge-info { background: var(--color-info-bg); color: var(--color-info-accent); }

/* Modal de resumen */
.modal-overlay {
  position: fixed; inset: 0; z-index: 1000;
  background: rgba(0,0,0,0.4);
  display: flex; align-items: center; justify-content: center;
  backdrop-filter: blur(2px);
  animation: fadeIn 0.2s ease;
}
.modal-card {
  background: white; border-radius: 16px;
  width: 90%; max-width: 520px;
  box-shadow: 0 20px 60px rgba(0,0,0,0.2);
  overflow: hidden;
  animation: slideUp 0.25s ease;
}
@keyframes fadeIn { from { opacity: 0; } to { opacity: 1; } }
@keyframes slideUp { from { opacity: 0; transform: translateY(20px); } to { opacity: 1; transform: translateY(0); } }

.modal-header {
  padding: 1.25rem 1.5rem;
  border-bottom: 1px solid var(--color-neutral-divider);
  display: flex; align-items: center; justify-content: space-between;
}
.modal-header-content {
  display: flex; align-items: center; gap: 0.75rem;
}
.modal-header-content h3 {
  font-family: 'Young Serif', Georgia, serif;
  font-size: 1.1rem; margin: 0; color: var(--color-neutral-text-primary);
}
.modal-close {
  background: none; border: none; cursor: pointer;
  color: var(--color-neutral-text-secondary);
  padding: 4px; border-radius: 6px;
  transition: all 0.15s;
}
.modal-close:hover { background: var(--color-neutral-bg-page); color: var(--color-neutral-text-primary); }

.modal-body { padding: 1.5rem; }
.modal-footer {
  padding: 1rem 1.5rem;
  border-top: 1px solid var(--color-neutral-divider);
  display: flex; justify-content: flex-end;
}

.resumen-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 1rem;
  margin-bottom: 1.5rem;
}
.resumen-card {
  text-align: center;
  padding: 1.25rem 0.75rem;
  border-radius: 12px;
  border: 1px solid var(--color-neutral-divider);
}
.resumen-total { background: var(--color-info-bg); border-color: var(--color-primary-200); }
.resumen-success { background: var(--color-success-bg); border-color: var(--color-secondary-200); }
.resumen-error { background: var(--color-error-bg); border-color: transparent; }
.resumen-number {
  display: block;
  font-size: 2rem; font-weight: 800;
  color: var(--color-neutral-text-primary);
  line-height: 1.2;
}
.resumen-label {
  font-size: 0.75rem; font-weight: 600;
  text-transform: uppercase; letter-spacing: 0.04em;
  color: var(--color-neutral-text-secondary);
}
.resumen-success .resumen-number { color: var(--color-success-accent); }
.resumen-error .resumen-number { color: var(--color-error-accent); }

.detalle-fallidos { margin-top: 1rem; }
.detalle-fallidos h4 {
  font-size: 0.85rem; font-weight: 700;
  color: var(--color-error-accent);
  margin: 0 0 0.5rem;
}
.fallido-item {
  display: flex; justify-content: space-between; align-items: flex-start;
  padding: 0.5rem 0.75rem;
  background: var(--color-error-bg);
  border-radius: 8px;
  margin-bottom: 0.35rem;
  font-size: 0.8rem;
}
.fallido-nombre { font-weight: 600; color: var(--color-neutral-text-primary); }
.fallido-error { color: var(--color-error-accent); font-size: 0.75rem; max-width: 50%; text-align: right; word-break: break-word; }

/* Empty state */
.empty-state-card {
  display: flex; flex-direction: column; align-items: center;
  text-align: center; padding: 4rem 2rem;
  background: white; border: 1px solid var(--color-neutral-divider);
  border-radius: 12px;
}
.empty-state-card svg { margin-bottom: 1rem; }
.empty-state-card h3 { font-family: 'Young Serif', Georgia, serif; font-size: 1.1rem; color: var(--color-neutral-text-primary); margin: 0 0 0.5rem; }
.empty-state-card p { color: var(--color-neutral-text-secondary); font-size: 0.9rem; margin: 0; }

@media (max-width: 768px) {
  .card-body { padding: 1rem; }
  .data-table th, .data-table td { padding: 0.65rem 0.5rem; font-size: 0.75rem; }
  .action-btns { flex-direction: column; }
  .btn-action { min-width: 60px; font-size: 0.7rem; }
}
</style>
