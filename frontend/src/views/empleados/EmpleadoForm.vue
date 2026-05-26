<template>
  <div>
    <!-- Page header -->
    <div class="page-header-actions">
      <div class="header-left">
        <router-link to="/empleados" class="btn-back" data-tooltip="Volver a la lista">
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <line x1="19" y1="12" x2="5" y2="12"/>
            <polyline points="12 19 5 12 12 5"/>
          </svg>
        </router-link>
        <div>
          <h1 class="display-heading">{{ isEdit ? 'Editar Empleado' : 'Nuevo Empleado' }}</h1>
          <p class="text-muted">{{ isEdit ? 'Modifique los datos del empleado' : 'Registre un nuevo empleado en el sistema' }}</p>
        </div>
      </div>
    </div>

    <div class="card card-elevated">
      <div class="card-body">
        <!-- === Error Summary Banner === -->
        <div v-if="hasErrors" class="form-error-summary">
          <!-- Error general del servidor -->
          <div v-if="formError" class="alert alert-error mb-2">
            <div class="flex-row items-start gap-sm">
              <i class="bi bi-exclamation-triangle-fill" style="font-size: 1.25rem;"></i>
              <div>
                <strong>Error al guardar</strong>
                <p class="text-sm mt-1" style="margin-bottom: 0;">{{ formError }}</p>
              </div>
            </div>
          </div>

          <!-- Lista de campos con errores -->
          <div class="alert alert-warning">
            <div class="flex-row items-start gap-sm">
              <i class="bi bi-exclamation-circle-fill" style="font-size: 1.25rem;"></i>
              <div style="flex: 1;">
                <strong>Campos incompletos o inválidos</strong>
                <ul class="form-error-list mt-1" v-if="fieldErrorList.length">
                  <li v-for="(err, idx) in fieldErrorList" :key="idx">
                    <strong>{{ err.label }}:</strong> {{ err.message }}
                  </li>
                </ul>
              </div>
            </div>
          </div>
        </div>

        <form @submit.prevent="onSubmit" class="layout-grid grid-2" novalidate>
          <!-- Personal Information Section -->
          <div class="form-section col-span-2">
            <h4 class="form-section-title">
              <i class="bi bi-person-badge me-2"></i>
              Información Personal
            </h4>
            <div class="divider"></div>
          </div>

          <div class="form-group" :class="{ 'has-error': fieldErrors.cedula }">
            <label for="cedula" class="form-label">Cédula <span class="required">*</span></label>
            <input type="text" class="form-input" :class="{ 'is-invalid': fieldErrors.cedula }" id="cedula" v-model="form.cedula" @input="clearFieldError('cedula')">
            <span v-if="fieldErrors.cedula" class="form-error">{{ fieldErrors.cedula }}</span>
          </div>

          <div class="form-group" :class="{ 'has-error': fieldErrors.nombres }">
            <label for="nombres" class="form-label">Nombres <span class="required">*</span></label>
            <input type="text" class="form-input" :class="{ 'is-invalid': fieldErrors.nombres }" id="nombres" v-model="form.nombres" @input="clearFieldError('nombres')">
            <span v-if="fieldErrors.nombres" class="form-error">{{ fieldErrors.nombres }}</span>
          </div>

          <div class="form-group" :class="{ 'has-error': fieldErrors.apellidos }">
            <label for="apellidos" class="form-label">Apellidos <span class="required">*</span></label>
            <input type="text" class="form-input" :class="{ 'is-invalid': fieldErrors.apellidos }" id="apellidos" v-model="form.apellidos" @input="clearFieldError('apellidos')">
            <span v-if="fieldErrors.apellidos" class="form-error">{{ fieldErrors.apellidos }}</span>
          </div>

          <div class="form-group" :class="{ 'has-error': fieldErrors.email }">
            <label for="email" class="form-label">Email <span class="required">*</span></label>
            <input type="email" class="form-input" :class="{ 'is-invalid': fieldErrors.email }" id="email" v-model="form.email" @input="clearFieldError('email')" placeholder="correo@empresa.com">
            <span v-if="fieldErrors.email" class="form-error">{{ fieldErrors.email }}</span>
          </div>

          <!-- Labor Information Section -->
          <div class="form-section col-span-2 mt-3">
            <h4 class="form-section-title">
              <i class="bi bi-briefcase me-2"></i>
              Información Laboral
            </h4>
            <div class="divider"></div>
          </div>

          <div class="form-group" :class="{ 'has-error': fieldErrors.cargo }">
            <label for="cargo" class="form-label">Cargo <span class="required">*</span></label>
            <select class="form-select" :class="{ 'is-invalid': fieldErrors.cargo }" id="cargo" v-model="form.cargo" @change="clearFieldError('cargo')">
              <option value="">Seleccione un cargo...</option>
              <option value="Desarrollador Senior">Desarrollador Senior</option>
              <option value="Desarrollador Junior">Desarrollador Junior</option>
              <option value="Analista de Calidad">Analista de Calidad</option>
              <option value="Analista de Desarrollo">Analista de Desarrollo</option>
              <option value="Diseñador UX/UI">Diseñador UX/UI</option>
              <option value="Scrum Master">Scrum Master</option>
              <option value="Product Owner">Product Owner</option>
              <option value="Administrador de RRHH">Administrador de RRHH</option>
              <option value="Contador General">Contador General</option>
              <option value="Gerente General">Gerente General</option>
              <option value="Administrador del Sistema">Administrador del Sistema</option>
              <option value="Auxiliar Contable">Auxiliar Contable</option>
              <option value="Secretario(a)">Secretario(a)</option>
              <option value="Practicante">Practicante</option>
            </select>
            <span v-if="fieldErrors.cargo" class="form-error">{{ fieldErrors.cargo }}</span>
          </div>

          <div class="form-group" :class="{ 'has-error': fieldErrors.tipo_contrato }">
            <label for="tipo_contrato" class="form-label">Tipo de Contrato <span class="required">*</span></label>
            <select class="form-select" :class="{ 'is-invalid': fieldErrors.tipo_contrato }" id="tipo_contrato" v-model="form.tipo_contrato" @change="clearFieldError('tipo_contrato')">
              <option value="">Seleccione...</option>
              <option value="TERMINO_FIJO">Término Fijo</option>
              <option value="TERMINO_INDEFINIDO">Término Indefinido</option>
              <option value="OBRA_LABOR">Obra Labor</option>
              <option value="PRESTACION_SERVICIOS">Prestación de Servicios</option>
            </select>
            <span v-if="fieldErrors.tipo_contrato" class="form-error">{{ fieldErrors.tipo_contrato }}</span>
          </div>

          <div class="form-group" :class="{ 'has-error': fieldErrors.salario_base }">
            <label for="salario_base" class="form-label">Salario Base <span class="required">*</span></label>
            <div class="input-with-icon">
              <span class="input-icon">$</span>
              <input type="number" class="form-input" :class="{ 'is-invalid': fieldErrors.salario_base }" id="salario_base" v-model.number="form.salario_base" min="0" placeholder="0" @input="clearFieldError('salario_base')">
            </div>
            <span v-if="fieldErrors.salario_base" class="form-error">{{ fieldErrors.salario_base }}</span>
          </div>

          <div class="form-group" :class="{ 'has-error': fieldErrors.fecha_ingreso }">
            <label for="fecha_ingreso" class="form-label">Fecha de Ingreso <span class="required">*</span></label>
            <input type="date" class="form-input" :class="{ 'is-invalid': fieldErrors.fecha_ingreso }" id="fecha_ingreso" v-model="form.fecha_ingreso" @input="clearFieldError('fecha_ingreso')">
            <span v-if="fieldErrors.fecha_ingreso" class="form-error">{{ fieldErrors.fecha_ingreso }}</span>
          </div>

          <div class="form-group">
            <label for="fecha_retiro" class="form-label">Fecha de Retiro</label>
            <input type="date" class="form-input" id="fecha_retiro" v-model="form.fecha_retiro">
          </div>

          <!-- Social Security Section -->
          <div class="form-section col-span-2 mt-3">
            <h4 class="form-section-title">
              <i class="bi bi-shield-check me-2"></i>
              Seguridad Social
            </h4>
            <div class="divider"></div>
          </div>

          <div class="form-group" :class="{ 'has-error': fieldErrors.eps }">
            <label for="eps" class="form-label">EPS <span class="required">*</span></label>
            <select class="form-select" :class="{ 'is-invalid': fieldErrors.eps }" id="eps" v-model="form.eps" @change="clearFieldError('eps')">
              <option value="">Seleccione una EPS...</option>
              <option value="Sanitas">Sanitas</option>
              <option value="Nueva EPS">Nueva EPS</option>
              <option value="Compensar">Compensar</option>
              <option value="Colsanitas">Colsanitas</option>
              <option value="Sura">Sura</option>
              <option value="Salud Total">Salud Total</option>
              <option value="Coomeva">Coomeva</option>
              <option value="Famisanar">Famisanar</option>
              <option value="Cafam">Cafam</option>
              <option value="Cruz Blanca">Cruz Blanca</option>
              <option value="Capital Salud">Capital Salud</option>
              <option value="Mutual Ser">Mutual Ser</option>
              <option value="Comfamiliar">Comfamiliar</option>
            </select>
            <span v-if="fieldErrors.eps" class="form-error">{{ fieldErrors.eps }}</span>
          </div>

          <div class="form-group" :class="{ 'has-error': fieldErrors.afp }">
            <label for="afp" class="form-label">AFP <span class="required">*</span></label>
            <select class="form-select" :class="{ 'is-invalid': fieldErrors.afp }" id="afp" v-model="form.afp" @change="clearFieldError('afp')">
              <option value="">Seleccione una AFP...</option>
              <option value="Porvenir">Porvenir</option>
              <option value="Colfondos">Colfondos</option>
              <option value="Protección">Protección</option>
              <option value="Old Mutual">Old Mutual</option>
              <option value="Skandia">Skandia</option>
            </select>
            <span v-if="fieldErrors.afp" class="form-error">{{ fieldErrors.afp }}</span>
          </div>

          <div class="form-group" :class="{ 'has-error': fieldErrors.arl }">
            <label for="arl" class="form-label">ARL <span class="required">*</span></label>
            <select class="form-select" :class="{ 'is-invalid': fieldErrors.arl }" id="arl" v-model="form.arl" @change="clearFieldError('arl')">
              <option value="">Seleccione una ARL...</option>
              <option value="Positiva">Positiva</option>
              <option value="Sura">Sura</option>
              <option value="Bolívar">Bolívar</option>
              <option value="Colpatria">Colpatria</option>
              <option value="Mapfre">Mapfre</option>
              <option value="Colmena">Colmena</option>
              <option value="Equidad">Equidad</option>
              <option value="Aurora">Aurora</option>
              <option value="Seguros del Estado">Seguros del Estado</option>
            </select>
            <span v-if="fieldErrors.arl" class="form-error">{{ fieldErrors.arl }}</span>
          </div>

          <!-- Bank Information Section -->
          <div class="form-section col-span-2 mt-3">
            <h4 class="form-section-title">
              <i class="bi bi-bank me-2"></i>
              Información Bancaria
            </h4>
            <div class="divider"></div>
          </div>

          <div class="form-group" :class="{ 'has-error': fieldErrors.cuenta_bancaria }">
            <label for="cuenta_bancaria" class="form-label">Cuenta Bancaria</label>
            <input type="text" class="form-input" :class="{ 'is-invalid': fieldErrors.cuenta_bancaria }" id="cuenta_bancaria" v-model="form.cuenta_bancaria" @input="clearFieldError('cuenta_bancaria')">
            <span v-if="fieldErrors.cuenta_bancaria" class="form-error">{{ fieldErrors.cuenta_bancaria }}</span>
          </div>

          <div class="form-group" :class="{ 'has-error': fieldErrors.banco }">
            <label for="banco" class="form-label">Banco</label>
            <select class="form-select" :class="{ 'is-invalid': fieldErrors.banco }" id="banco" v-model="form.banco" @change="clearFieldError('banco')">
              <option value="">Seleccione un banco...</option>
              <option value="Bancolombia">Bancolombia</option>
              <option value="Davivienda">Davivienda</option>
              <option value="Banco de Bogotá">Banco de Bogotá</option>
              <option value="Banco Popular">Banco Popular</option>
              <option value="Banco de Occidente">Banco de Occidente</option>
              <option value="BBVA">BBVA</option>
              <option value="Colpatria">Colpatria</option>
              <option value="AV Villas">AV Villas</option>
              <option value="Itaú">Itaú</option>
              <option value="Banco Agrario">Banco Agrario</option>
              <option value="Bancoomeva">Bancoomeva</option>
              <option value="Scotiabank Colpatria">Scotiabank Colpatria</option>
              <option value="Banco Caja Social">Banco Caja Social</option>
              <option value="Nequi">Nequi</option>
              <option value="DaviPlata">DaviPlata</option>
            </select>
            <span v-if="fieldErrors.banco" class="form-error">{{ fieldErrors.banco }}</span>
          </div>

          <div class="form-group" :class="{ 'has-error': fieldErrors.tipo_cuenta }">
            <label for="tipo_cuenta" class="form-label">Tipo de Cuenta</label>
            <select class="form-select" :class="{ 'is-invalid': fieldErrors.tipo_cuenta }" id="tipo_cuenta" v-model="form.tipo_cuenta" @change="clearFieldError('tipo_cuenta')">
              <option value="">Seleccione...</option>
              <option value="AHORROS">Ahorros</option>
              <option value="CORRIENTE">Corriente</option>
            </select>
            <span v-if="fieldErrors.tipo_cuenta" class="form-error">{{ fieldErrors.tipo_cuenta }}</span>
          </div>

          <!-- Facial Photo Section -->
          <div class="form-section col-span-2 mt-3">
            <h4 class="form-section-title">
              <i class="bi bi-camera me-2"></i>
              Foto Facial
            </h4>
            <div class="divider"></div>
          </div>

          <div class="col-span-2">
            <FotoFacialUpload v-model:fotoData="form.foto_facial" />
          </div>

          <!-- Actions -->
          <div class="col-span-2 flex-row justify-end mt-4" style="border-top: 1px solid var(--color-divider); padding-top: 1.5rem;">
            <button type="button" class="btn btn-outline" @click="$router.go(-1)">
              Cancelar
            </button>
            <button type="submit" class="btn btn-primary btn-lg" :disabled="submitting">
              <span v-if="submitting" class="spinner spinner-sm me-2"></span>
              <i v-else :class="isEdit ? 'bi bi-check-lg' : 'bi bi-plus-lg'"></i>
              {{ submitting ? 'Guardando...' : (isEdit ? 'Actualizar Empleado' : 'Crear Empleado') }}
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script>
import FotoFacialUpload from '@/components/empleados/FotoFacialUpload.vue'
import { ref, computed, watch } from 'vue'
import axios from 'axios'
import { useRoute, useRouter } from 'vue-router'

export default {
  components: { FotoFacialUpload },
  setup() {
    const route = useRoute()
    const router = useRouter()
    const isEdit = ref(false)
    const empleadoId = ref(null)
    const form = ref({
      cedula: '',
      nombres: '',
      apellidos: '',
      email: '',
      telefono: '',
      cargo: '',
      tipo_contrato: '',
      salario_base: null,
      fecha_ingreso: '',
      fecha_retiro: null,
      eps: '',
      afp: '',
      arl: '',
      cuenta_bancaria: '',
      banco: '',
      tipo_cuenta: '',
      foto_facial: null,
      foto_facial_registrada: false,
      activo: true
    })

    // --- Validation state ---
    const fieldErrors = ref({})
    const formError = ref('')
    const submitting = ref(false)

    // --- Field display labels (for error messages) ---
    const fieldLabels = {
      cedula: 'Cédula',
      nombres: 'Nombres',
      apellidos: 'Apellidos',
      email: 'Email',
      cargo: 'Cargo',
      tipo_contrato: 'Tipo de Contrato',
      salario_base: 'Salario Base',
      fecha_ingreso: 'Fecha de Ingreso',
      eps: 'EPS',
      afp: 'AFP',
      arl: 'ARL',
      cuenta_bancaria: 'Cuenta Bancaria',
      banco: 'Banco',
      tipo_cuenta: 'Tipo de Cuenta',
    }

    // Lista de campos requeridos con sus etiquetas
    const requiredFields = [
      'cedula', 'nombres', 'apellidos', 'email', 'cargo',
      'tipo_contrato', 'salario_base', 'fecha_ingreso',
      'eps', 'afp', 'arl'
    ]

    // --- Limpiar errores al escribir ---
    const clearFieldError = (field) => {
      delete fieldErrors.value[field]
      if (formError.value) formError.value = ''
    }

    // --- Client-side validation ---
    const validateForm = () => {
      // Limpiar errores previos
      Object.keys(fieldErrors.value).forEach(k => delete fieldErrors.value[k])
      formError.value = ''

      const fields = form.value
      let hasError = false

      // Validar campos requeridos vacíos
      requiredFields.forEach(field => {
        const val = fields[field]
        if (val === null || val === undefined || String(val).trim() === '') {
          fieldErrors.value[field] = `${fieldLabels[field] || field} es obligatorio`
          hasError = true
        }
      })

      // Validaciones de formato
      const cedula = String(fields.cedula || '').trim()
      if (cedula && cedula.length < 5) {
        fieldErrors.value.cedula = 'La cédula debe tener al menos 5 caracteres'
        hasError = true
      }

      const email = String(fields.email || '').trim()
      if (email && !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) {
        fieldErrors.value.email = 'El formato del email no es válido'
        hasError = true
      }

      if (fields.salario_base !== null && fields.salario_base !== '' && Number(fields.salario_base) <= 0) {
        fieldErrors.value.salario_base = 'El salario base debe ser mayor a 0'
        hasError = true
      }

      return !hasError
    }

    // --- Parsear errores del backend (DRF style) ---
    const parseBackendErrors = (error) => {
      if (!error.response || !error.response.data) return

      const data = error.response.data

      // Errores de campo: { campo: ['mensaje'] }
      Object.entries(data).forEach(([field, messages]) => {
        if (field === 'non_field_errors') {
          formError.value = Array.isArray(messages) ? messages.join('. ') : String(messages)
        } else {
          const msg = Array.isArray(messages) ? messages[0] : String(messages)
          fieldErrors.value[field] = msg
        }
      })
    }

    // Lista plana de errores para mostrar en el resumen
    const fieldErrorList = computed(() => {
      return Object.entries(fieldErrors.value).map(([field, msg]) => ({
        label: fieldLabels[field] || field,
        message: msg
      }))
    })

    // Verificar si hay errores
    const hasErrors = computed(() => Object.keys(fieldErrors.value).length > 0 || !!formError.value)

    // --- Auto-set foto_facial_registrada ---
    watch(() => form.value.foto_facial, (val) => {
      if (val) {
        form.value.foto_facial_registrada = true
      }
    })

    // --- Cargar datos en modo edición ---
    watch(() => route.params.id, async (newId) => {
      if (newId) {
        isEdit.value = true
        empleadoId.value = newId
        try {
          const response = await axios.get(`/api/empleados/${newId}/`)
          form.value = { ...response.data }
          if (form.value.fecha_ingreso) {
            form.value.fecha_ingreso = form.value.fecha_ingreso.split('T')[0]
          }
          if (form.value.fecha_retiro) {
            form.value.fecha_retiro = form.value.fecha_retiro.split('T')[0]
          }
        } catch (error) {
          console.error('Error loading empleado:', error)
          router.push({ name: 'empleados-list' })
        }
      }
    }, { immediate: true })

    // --- Submit con validación ---
    const onSubmit = async () => {
      // Validación client-side primero
      if (!validateForm()) {
        // Scroll al inicio del formulario para mostrar errores
        const el = document.querySelector('.form-error-summary')
        if (el) el.scrollIntoView({ behavior: 'smooth', block: 'center' })
        return  // ← NO reinicia el formulario, solo muestra errores
      }

      submitting.value = true

      try {
        if (isEdit.value) {
          await axios.put(`/api/empleados/${empleadoId.value}/`, form.value)
        } else {
          await axios.post('/api/empleados/', form.value)
        }
        router.push({ name: 'empleados-list' })
      } catch (error) {
        console.error('Error saving empleado:', error)
        // Parsear errores del backend y mostrarlos en el formulario
        parseBackendErrors(error)
        if (!hasErrors.value) {
          formError.value = error.response?.data?.message || error.message || 'Error al guardar el empleado'
        }
        // Scroll para mostrar errores
        const el = document.querySelector('.form-error-summary')
        if (el) el.scrollIntoView({ behavior: 'smooth', block: 'center' })
      } finally {
        submitting.value = false
      }
    }

    return { isEdit, form, fieldErrors, formError, submitting, fieldErrorList, hasErrors, clearFieldError, onSubmit }
  }
}
</script>

<style scoped>
.col-span-2 {
  grid-column: 1 / -1;
}

.form-section-title {
  font-size: 1rem;
  font-weight: 600;
  color: var(--color-text-primary);
  display: flex;
  align-items: center;
}

.form-section-title i {
  color: var(--color-primary-500);
  font-size: 1.125rem;
}

.required {
  color: var(--color-error-accent);
}

/* === Error Summary Banner Animation === */
.form-error-summary {
  animation: slideDown 0.3s ease;
  margin-bottom: 1.5rem;
}

@keyframes slideDown {
  from { opacity: 0; transform: translateY(-10px); }
  to { opacity: 1; transform: translateY(0); }
}

.form-error-list {
  margin: 0.5rem 0 0 0;
  padding-left: 1.25rem;
  list-style: none;
}

.form-error-list li {
  position: relative;
  padding: 0.2rem 0;
  font-size: 0.875rem;
  line-height: 1.4;
  color: var(--color-text-primary);
}

.form-error-list li::before {
  content: '•';
  position: absolute;
  left: -1rem;
  color: var(--color-warning-accent);
  font-weight: bold;
  font-size: 1.125rem;
}

/* === Field Error Styles === */
.has-error {
  animation: shakeField 0.3s ease;
}

@keyframes shakeField {
  0%, 100% { transform: translateX(0); }
  20% { transform: translateX(-4px); }
  40% { transform: translateX(4px); }
  60% { transform: translateX(-3px); }
  80% { transform: translateX(3px); }
}

/* Input error border */
.form-input.is-invalid,
.form-select.is-invalid {
  border-color: var(--color-error-accent) !important;
  box-shadow: 0 0 0 2px rgba(163, 45, 45, 0.15);
}

.form-input.is-invalid:focus,
.form-select.is-invalid:focus {
  border-color: var(--color-error-accent) !important;
  box-shadow: 0 0 0 3px rgba(163, 45, 45, 0.2);
}

/* Error message below field */
.form-error {
  display: flex;
  align-items: center;
  gap: 0.375rem;
  margin-top: 0.375rem;
  font-size: 0.8125rem;
  color: var(--color-error-accent);
  animation: fadeIn 0.25s ease;
}

.form-error::before {
  content: '⚠';
  font-size: 0.8125rem;
}

@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}

/* Label error color */
.has-error .form-label {
  color: var(--color-error-accent);
}

/* Back button */
.header-left {
  display: flex;
  align-items: flex-start;
  gap: 0.875rem;
}

.btn-back {
  width: 38px;
  height: 38px;
  display: flex;
  align-items: center;
  justify-content: center;
  border: 1.5px solid var(--color-divider);
  border-radius: var(--border-radius-sm);
  background: var(--color-bg-white);
  color: var(--color-text-secondary);
  text-decoration: none;
  flex-shrink: 0;
  transition: all var(--transition-fast);
  margin-top: 2px;
}

.btn-back:hover {
  border-color: var(--color-primary-500);
  color: var(--color-primary-700);
  background: var(--color-primary-50);
  transform: translateX(-3px);
}

.btn-back:active {
  transform: translateX(-1px) scale(0.96);
}

@media (max-width: 768px) {
  .layout-grid {
    grid-template-columns: 1fr;
  }
}
</style>
