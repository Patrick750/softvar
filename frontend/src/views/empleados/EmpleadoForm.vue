<template>
  <div>
    <!-- Page header -->
    <div class="page-header-actions">
      <div>
        <h1 class="display-heading">{{ isEdit ? 'Editar Empleado' : 'Nuevo Empleado' }}</h1>
        <p class="text-muted">{{ isEdit ? 'Modifique los datos del empleado' : 'Registre un nuevo empleado en el sistema' }}</p>
      </div>
    </div>

    <div class="card card-elevated">
      <div class="card-body">
        <form @submit.prevent="onSubmit" class="layout-grid grid-2">
          <!-- Personal Information Section -->
          <div class="form-section col-span-2">
            <h4 class="form-section-title">
              <i class="bi bi-person-badge me-2"></i>
              Información Personal
            </h4>
            <div class="divider"></div>
          </div>

          <div class="form-group">
            <label for="cedula" class="form-label">Cédula <span class="required">*</span></label>
            <input type="text" class="form-input" id="cedula" v-model="form.cedula" required>
          </div>

          <div class="form-group">
            <label for="nombres" class="form-label">Nombres <span class="required">*</span></label>
            <input type="text" class="form-input" id="nombres" v-model="form.nombres" required>
          </div>

          <div class="form-group">
            <label for="apellidos" class="form-label">Apellidos <span class="required">*</span></label>
            <input type="text" class="form-input" id="apellidos" v-model="form.apellidos" required>
          </div>

          <div class="form-group">
            <label for="email" class="form-label">Email <span class="required">*</span></label>
            <input type="email" class="form-input" id="email" v-model="form.email" required placeholder="correo@empresa.com">
          </div>

          <!-- Labor Information Section -->
          <div class="form-section col-span-2 mt-3">
            <h4 class="form-section-title">
              <i class="bi bi-briefcase me-2"></i>
              Información Laboral
            </h4>
            <div class="divider"></div>
          </div>

          <div class="form-group">
            <label for="cargo" class="form-label">Cargo <span class="required">*</span></label>
            <input type="text" class="form-input" id="cargo" v-model="form.cargo" required>
          </div>

          <div class="form-group">
            <label for="tipo_contrato" class="form-label">Tipo de Contrato <span class="required">*</span></label>
            <select class="form-select" id="tipo_contrato" v-model="form.tipo_contrato" required>
              <option value="">Seleccione...</option>
              <option value="TERMINO_FIJO">Término Fijo</option>
              <option value="TERMINO_INDEFINIDO">Término Indefinido</option>
              <option value="OBRA_LABOR">Obra Labor</option>
              <option value="PRESTACION_SERVICIOS">Prestación de Servicios</option>
            </select>
          </div>

          <div class="form-group">
            <label for="salario_base" class="form-label">Salario Base <span class="required">*</span></label>
            <div class="input-with-icon">
              <span class="input-icon">$</span>
              <input type="number" class="form-input" id="salario_base" v-model.number="form.salario_base" required min="0" placeholder="0">
            </div>
          </div>

          <div class="form-group">
            <label for="fecha_ingreso" class="form-label">Fecha de Ingreso <span class="required">*</span></label>
            <input type="date" class="form-input" id="fecha_ingreso" v-model="form.fecha_ingreso" required>
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

          <div class="form-group">
            <label for="eps" class="form-label">EPS <span class="required">*</span></label>
            <input type="text" class="form-input" id="eps" v-model="form.eps" required>
          </div>

          <div class="form-group">
            <label for="afp" class="form-label">AFP <span class="required">*</span></label>
            <input type="text" class="form-input" id="afp" v-model="form.afp" required>
          </div>

          <div class="form-group">
            <label for="arl" class="form-label">ARL <span class="required">*</span></label>
            <input type="text" class="form-input" id="arl" v-model="form.arl" required>
          </div>

          <!-- Bank Information Section -->
          <div class="form-section col-span-2 mt-3">
            <h4 class="form-section-title">
              <i class="bi bi-bank me-2"></i>
              Información Bancaria
            </h4>
            <div class="divider"></div>
          </div>

          <div class="form-group">
            <label for="cuenta_bancaria" class="form-label">Cuenta Bancaria</label>
            <input type="text" class="form-input" id="cuenta_bancaria" v-model="form.cuenta_bancaria">
          </div>

          <div class="form-group">
            <label for="banco" class="form-label">Banco</label>
            <input type="text" class="form-input" id="banco" v-model="form.banco">
          </div>

          <div class="form-group">
            <label for="tipo_cuenta" class="form-label">Tipo de Cuenta</label>
            <select class="form-select" id="tipo_cuenta" v-model="form.tipo_cuenta">
              <option value="">Seleccione...</option>
              <option value="AHORROS">Ahorros</option>
              <option value="CORRIENTE">Corriente</option>
            </select>
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
            <button type="submit" class="btn btn-primary btn-lg">
              <i :class="isEdit ? 'bi bi-check-lg' : 'bi bi-plus-lg'"></i>
              {{ isEdit ? 'Actualizar Empleado' : 'Crear Empleado' }}
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

    const onSubmit = async () => {
      try {
        if (isEdit.value) {
          await axios.put(`/api/empleados/${empleadoId.value}/`, form.value)
        } else {
          await axios.post('/api/empleados/', form.value)
        }
        router.push({ name: 'empleados-list' })
      } catch (error) {
        console.error('Error saving empleado:', error)
      }
    }

    return { isEdit, form, onSubmit }
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

@media (max-width: 768px) {
  .layout-grid {
    grid-template-columns: 1fr;
  }
}
</style>
