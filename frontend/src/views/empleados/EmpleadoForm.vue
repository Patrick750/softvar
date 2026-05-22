<template>
  <div class="container mt-4">
    <h2>{{ isEdit ? 'Editar Empleado' : 'Nuevo Empleado' }}</h2>
    <form @submit.prevent="onSubmit" class="row g-4 needs-validation" novalidate>
      <!-- Form fields -->
      <div class="col-md-6">
        <label for="cedula" class="form-label">Cédula *</label>
        <input
          type="text"
          class="form-control"
          id="cedula"
          v-model="form.cedula"
          required
        >
        <div class="invalid-feedback">Por favor ingrese la cédula</div>
      </div>

      <div class="col-md-6">
        <label for="nombres" class="form-label">Nombres *</label>
        <input
          type="text"
          class="form-control"
          id="nombres"
          v-model="form.nombres"
          required
        >
        <div class="invalid-feedback">Por favor ingrese los nombres</div>
      </div>

      <div class="col-md-6">
        <label for="apellidos" class="form-label">Apellidos *</label>
        <input
          type="text"
          class="form-control"
          id="apellidos"
          v-model="form.apellidos"
          required
        >
        <div class="invalid-feedback">Por favor ingrese los apellidos</div>
      </div>

      <div class="col-md-6">
        <label for="email" class="form-label">Email *</label>
        <input
          type="email"
          class="form-control"
          id="email"
          v-model="form.email"
          required
        >
        <div class="invalid-feedback">Por favor ingrese un email válido</div>
      </div>

      <div class="col-12">
        <label for="cargo" class="form-label">Cargo *</label>
        <input
          type="text"
          class="form-control"
          id="cargo"
          v-model="form.cargo"
          required
        >
        <div class="invalid-feedback">Por favor ingrese el cargo</div>
      </div>

      <div class="col-md-6">
        <label for="tipo_contrato" class="form-label">Tipo de Contrato *</label>
        <select
          class="form-select"
          id="tipo_contrato"
          v-model="form.tipo_contrato"
          required
        >
          <option value="">Seleccione...</option>
          <option value="TERMINO_FIJO">Término Fijo</option>
          <option value="TERMINO_INDEFINIDO">Término Indefinido</option>
          <option value="OBRA_LABOR">Obra Labor</option>
          <option value="PRESTACION_SERVICIOS">Prestación de Servicios</option>
        </select>
        <div class="invalid-feedback">Por favor seleccione el tipo de contrato</div>
      </div>

      <div class="col-md-6">
        <label for="salario_base" class="form-label">Salario Base *</label>
        <input
          type="number"
          class="form-control"
          id="salario_base"
          v-model.number="form.salario_base"
          required
          min="0"
        >
        <div class="invalid-feedback">Por favor ingrese el salario base</div>
      </div>

      <div class="col-md-6">
        <label for="fecha_ingreso" class="form-label">Fecha de Ingreso *</label>
        <input
          type="date"
          class="form-control"
          id="fecha_ingreso"
          v-model="form.fecha_ingreso"
          required
        >
        <div class="invalid-feedback">Por favor seleccione la fecha de ingreso</div>
      </div>

      <div class="col-md-6">
        <label for="fecha_retiro" class="form-label">Fecha de Retiro</label>
        <input
          type="date"
          class="form-control"
          id="fecha_retiro"
          v-model="form.fecha_retiro"
        >
      </div>

      <div class="col-md-6">
        <label for="eps" class="form-label">EPS *</label>
        <input
          type="text"
          class="form-control"
          id="eps"
          v-model="form.eps"
          required
        >
        <div class="invalid-feedback">Por favor ingrese la EPS</div>
      </div>

      <div class="col-md-6">
        <label for="afp" class="form-label">AFP *</label>
        <input
          type="text"
          class="form-control"
          id="afp"
          v-model="form.afp"
          required
        >
        <div class="invalid-feedback">Por favor ingrese la AFP</div>
      </div>

      <div class="col-md-6">
        <label for="arl" class="form-label">ARL *</label>
        <input
          type="text"
          class="form-control"
          id="arl"
          v-model="form.arl"
          required
        >
        <div class="invalid-feedback">Por favor ingrese la ARL</div>
      </div>

      <div class="col-12">
        <label for="cuenta_bancaria" class="form-label">Cuenta Bancaria</label>
        <input
          type="text"
          class="form-control"
          id="cuenta_bancaria"
          v-model="form.cuenta_bancaria"
        >
      </div>

      <div class="col-md-6">
        <label for="banco" class="form-label">Banco</label>
        <input
          type="text"
          class="form-control"
          id="banco"
          v-model="form.banco"
        >
      </div>

      <div class="col-md-6">
        <label for="tipo_cuenta" class="form-label">Tipo de Cuenta</label>
        <select
          class="form-select"
          id="tipo_cuenta"
          v-model="form.tipo_cuenta"
        >
          <option value="">Seleccione...</option>
          <option value="AHORROS">Ahorros</option>
          <option value="CORRIENTE">Corriente</option>
        </select>
      </div>

      <div class="col-12">
        <label for="foto_facial" class="form-label">Foto Facial (para reconocimiento)</label>
        <FotoFacialUpload v-model:fotoData="form.foto_facial" />
      </div>

      <div class="col-12">
        <button
          type="submit"
          class="btn btn-primary"
        >
          {{ isEdit ? 'Actualizar' : 'Crear' }}
        </button>
        <button
          type="button"
          class="btn btn-secondary"
          @click="$router.go(-1)"
        >
          Cancelar
        </button>
      </div>
    </form>
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

    // Load employee data if editing
    watch(() => route.params.id, async (newId) => {
      if (newId) {
        isEdit.value = true
        empleadoId.value = newId
        try {
          const response = await axios.get(`/api/empleados/${newId}/`)
          form.value = { ...response.data }
          // Convert date strings to proper format for input
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
        alert('Error al guardar el empleado')
      }
    }

    return {
      isEdit,
      empleadoId,
      form,
      onSubmit
    }
  }
}
</script>

<style scoped>
/* Add some custom styling to match the design system */
.form-control {
  border-radius: 8px;
  border: 1px solid var(--color-neutral-border);
}

.form-control:focus {
  border-color: var(--color-primary-500);
  box-shadow: 0 0 0 0.25rem rgba(55, 138, 171, 0.25);
}

.form-select {
  border-radius: 8px;
  border: 1px solid var(--color-neutral-border);
}

.form-select:focus {
  border-color: var(--color-primary-500);
  box-shadow: 0 0 0 0.25rem rgba(55, 138, 171, 0.25);
}

.btn-primary {
  background: var(--color-primary-700);
  border: none;
}

.btn-primary:hover {
  background: var(--color-primary-900);
  transform: translateY(-2px);
}

.btn-secondary {
  background: var(--color-neutral-bg-page);
  border: 1px solid var(--color-neutral-border);
  color: var(--color-neutral-text-primary);
}

.btn-secondary:hover {
  background: var(--color-neutral-divider);
  transform: translateY(-2px);
}
</style>