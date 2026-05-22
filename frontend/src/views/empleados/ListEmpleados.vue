<template>
  <div>
    <!-- Page header -->
    <div class="page-header-actions stagger-children">
      <div>
        <h1 class="display-heading">Gestión de Empleados</h1>
        <p class="text-muted">Administre el registro de empleados de la empresa</p>
      </div>
      <router-link to="/empleados/nuevo" class="btn btn-primary">
        <i class="bi bi-plus-lg"></i>
        Nuevo Empleado
      </router-link>
    </div>

    <!-- Loading skeleton -->
    <div v-if="loading" class="grid-auto stagger-children">
      <div v-for="n in 4" :key="n" class="card p-0">
        <div class="skeleton" style="height: 120px; border-radius: 16px 16px 0 0;"></div>
        <div class="card-body">
          <div class="skeleton skeleton-text"></div>
          <div class="skeleton skeleton-text" style="width: 40%;"></div>
          <div class="skeleton skeleton-text mt-3"></div>
          <div class="skeleton skeleton-text"></div>
        </div>
      </div>
    </div>

    <!-- Empty state -->
    <div v-else-if="!empleados.length" class="card">
      <div class="empty-state">
        <div class="empty-state-icon">
          <i class="bi bi-people"></i>
        </div>
        <h3 class="empty-state-title">No hay empleados registrados</h3>
        <p class="empty-state-text">Comience agregando el primer empleado al sistema de nómina.</p>
        <router-link to="/empleados/nuevo" class="btn btn-primary">
          <i class="bi bi-plus-lg"></i>
          Agregar Empleado
        </router-link>
      </div>
    </div>

    <!-- Employee grid -->
    <div v-else class="grid-auto stagger-children">
      <div v-for="empleado in empleados" :key="empleado.id">
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
    const loading = ref(true)

    const fetchEmpleados = async () => {
      try {
        const response = await axios.get('/api/empleados/')
        empleados.value = response.data
      } catch (error) {
        console.error('Error fetching empleados:', error)
      } finally {
        loading.value = false
      }
    }

    const eliminarEmpleado = async (id) => {
      try {
        await axios.delete(`/api/empleados/${id}/`)
        fetchEmpleados()
      } catch (error) {
        console.error('Error deleting empleado:', error)
      }
    }

    onMounted(fetchEmpleados)

    return { empleados, loading, eliminarEmpleado }
  }
}
</script>
