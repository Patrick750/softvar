<template>
  <div class="container mt-4">
    <h2>Gestión de Empleados</h2>
    <div class="mb-4">
      <router-link
        to="/empleados/nuevo"
        class="btn btn-primary"
      >
        Nuevo Empleado
      </router-link>
    </div>

    <div v-if="!empleados.length" class="alert alert-info text-center py-4">
      No hay empleados registrados
    </div>

    <div v-else class="row g-4">
      <div
        v-for="empleado in empleados"
        :key="empleado.id"
        class="col-lg-3 col-md-4 col-sm-6"
      >
        <EmpleadoCard
          :empleado="empleado"
          @empleado-eliminado="eliminarEmpleado"
        />
      </div>
    </div>
  </div>
</template>

<script>
import EmpleadoCard from '@/components/empleados/EmpleadoCard.vue'
import { ref, onMounted } from 'vue'
import axios from 'axios'

export default {
  components: { EmpleadoCard },
  setup() {
    const empleados = ref([])

    const fetchEmpleados = async () => {
      try {
        const response = await axios.get('/api/empleados/')
        empleados.value = response.data
      } catch (error) {
        console.error('Error fetching empleados:', error)
      }
    }

    const eliminarEmpleado = async (id) => {
      try {
        await axios.delete(`/api/empleados/${id}/`)
        fetchEmpleados() // Refresh list
      } catch (error) {
        console.error('Error deleting empleado:', error)
        alert('Error al eliminar el empleado')
      }
    }

    onMounted(fetchEmpleados)

    return { empleados, eliminarEmpleado }
  }
}
</script>

<style scoped>
.container {
  max-width: 1400px;
}
</style>