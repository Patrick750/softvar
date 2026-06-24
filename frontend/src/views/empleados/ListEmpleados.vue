<template>
  <div>
    <!-- Page header -->
    <div class="page-header-actions stagger-children">
      <div>
        <h1 class="display-heading">Gestión de Empleados</h1>
        <p class="text-muted">Administre el registro de empleados de la empresa</p>
      </div>
      <router-link to="/empleados/nuevo" class="btn btn-primary">
        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
          <line x1="12" y1="5" x2="12" y2="19"/>
          <line x1="5" y1="12" x2="19" y2="12"/>
        </svg>
        Nuevo Empleado
      </router-link>
    </div>

    <!-- Toolbar -->
    <div class="toolbar">
      <!-- Search -->
      <div class="toolbar-search">
        <svg class="search-icon" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
          <circle cx="11" cy="11" r="8"/>
          <line x1="21" y1="21" x2="16.65" y2="16.65"/>
        </svg>
        <input
          type="text"
          class="search-input"
          v-model="searchQuery"
          placeholder="Buscar por nombre o cédula..."
        />
        <button v-if="searchQuery" class="search-clear" @click="searchQuery = ''">
          <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round"><line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/></svg>
        </button>
      </div>

      <!-- Filters -->
      <div class="toolbar-filters">
        <select class="filter-select" v-model="filterEstado">
          <option value="">Todos los estados</option>
          <option value="true">Activo</option>
          <option value="false">Inactivo</option>
        </select>

        <select class="filter-select" v-model="filterContrato">
          <option value="">Todos los contratos</option>
          <option value="TERMINO_FIJO">Término Fijo</option>
          <option value="TERMINO_INDEFINIDO">Término Indefinido</option>
          <option value="OBRA_LABOR">Obra Labor</option>
          <option value="PRESTACION_SERVICIOS">Prestación de Servicios</option>
        </select>

        <select class="filter-select" v-model="filterCargo">
          <option value="">Todos los cargos</option>
          <option v-for="cargo in uniqueCargos" :key="cargo" :value="cargo">{{ cargo }}</option>
        </select>
      </div>

      <!-- View toggle & Export -->
      <div class="toolbar-actions">
        <button class="btn btn-outline btn-sm" @click="exportToExcel" data-tooltip="Exportar a Excel">
          <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/>
            <polyline points="7 10 12 15 17 10"/>
            <line x1="12" y1="15" x2="12" y2="3"/>
          </svg>
          Exportar
        </button>

        <div class="toolbar-view">
          <button
            class="view-toggle-btn"
            :class="{ active: viewMode === 'cards' }"
            @click="viewMode = 'cards'"
            data-tooltip="Vista de tarjetas"
          >
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">
              <rect x="3" y="3" width="7" height="7" rx="1"/>
              <rect x="14" y="3" width="7" height="7" rx="1"/>
              <rect x="3" y="14" width="7" height="7" rx="1"/>
              <rect x="14" y="14" width="7" height="7" rx="1"/>
            </svg>
          </button>
          <button
            class="view-toggle-btn"
            :class="{ active: viewMode === 'table' }"
            @click="viewMode = 'table'"
            data-tooltip="Vista compacta"
          >
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">
              <line x1="8" y1="6" x2="21" y2="6"/>
              <line x1="8" y1="12" x2="21" y2="12"/>
              <line x1="8" y1="18" x2="21" y2="18"/>
              <line x1="3" y1="6" x2="3.01" y2="6"/>
              <line x1="3" y1="12" x2="3.01" y2="12"/>
              <line x1="3" y1="18" x2="3.01" y2="18"/>
            </svg>
          </button>
        </div>
      </div>

      <!-- Result count -->
      <div class="toolbar-count">
        <span class="count-badge">{{ sortedEmpleados.length }}</span>
        <span class="count-label">de {{ empleados.length }} empleados</span>
      </div>
    </div>

    <!-- Loading skeleton -->
    <div v-if="loading" class="loading-area">
      <div v-if="viewMode === 'cards'" class="grid-auto">
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
      <div v-else class="table-card">
        <div v-for="n in 5" :key="n" class="skeleton-row">
          <div class="skeleton skeleton-avatar"></div>
          <div class="skeleton skeleton-text" style="width: 30%;"></div>
          <div class="skeleton skeleton-text" style="width: 15%;"></div>
          <div class="skeleton skeleton-text" style="width: 25%;"></div>
          <div class="skeleton skeleton-text" style="width: 10%;"></div>
        </div>
      </div>
    </div>

    <!-- Empty state (no employees) -->
    <div v-else-if="!empleados.length" class="card">
      <div class="empty-state">
        <div class="empty-state-icon">
          <svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1" stroke-linecap="round" stroke-linejoin="round">
            <path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/>
            <circle cx="9" cy="7" r="4"/>
            <path d="M23 21v-2a4 4 0 0 0-3-3.87"/>
            <path d="M16 3.13a4 4 0 0 1 0 7.75"/>
          </svg>
        </div>
        <h3 class="empty-state-title">No hay empleados registrados</h3>
        <p class="empty-state-text">Comience agregando el primer empleado al sistema de nómina.</p>
        <router-link to="/empleados/nuevo" class="btn btn-primary">
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
            <line x1="12" y1="5" x2="12" y2="19"/>
            <line x1="5" y1="12" x2="19" y2="12"/>
          </svg>
          Agregar Empleado
        </router-link>
      </div>
    </div>

    <!-- No results state (with filters) -->
    <div v-else-if="!sortedEmpleados.length" class="card">
      <div class="empty-state">
        <div class="empty-state-icon">
          <svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1" stroke-linecap="round" stroke-linejoin="round">
            <circle cx="11" cy="11" r="8"/>
            <line x1="21" y1="21" x2="16.65" y2="16.65"/>
            <line x1="8" y1="11" x2="14" y2="11"/>
          </svg>
        </div>
        <h3 class="empty-state-title">Sin resultados</h3>
        <p class="empty-state-text">No se encontraron empleados con los filtros aplicados. Intente con otros criterios de búsqueda.</p>
        <button class="btn btn-outline" @click="clearFilters">
          <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/></svg>
          Limpiar filtros
        </button>
      </div>
    </div>

    <!-- Employee grid (cards view) -->
    <div v-else-if="viewMode === 'cards'" class="grid-auto stagger-children">
      <div v-for="empleado in paginatedEmpleados" :key="empleado.id">
        <EmpleadoCard
          :empleado="empleado"
          @empleado-eliminado="eliminarEmpleado"
        />
      </div>
    </div>

    <!-- Employee table (compact view) -->
    <div v-else class="table-card">
      <div class="table-scroll">
        <table class="table-empleados">
          <thead>
            <tr>
              <th class="th-avatar"></th>
              <th class="th-name sortable" @click="toggleSort('nombre')">
                <span>
                  Nombre y Cargo
                  <span v-if="sortField === 'nombre'" class="sort-arrow">
                    <svg v-if="sortDirection === 'asc'" width="10" height="10" viewBox="0 0 24 24" fill="currentColor"><path d="M12 5l-7 7h14l-7-7z"/></svg>
                    <svg v-else width="10" height="10" viewBox="0 0 24 24" fill="currentColor"><path d="M12 19l7-7H5l7 7z"/></svg>
                  </span>
                  <span v-else class="sort-arrow sort-inactive">
                    <svg width="10" height="14" viewBox="0 0 24 24" fill="currentColor" opacity="0.3"><path d="M12 5l-7 7h14l-7-7z"/><path d="M12 19l7-7H5l7 7z"/></svg>
                  </span>
                </span>
              </th>
              <th class="th-cedula sortable" @click="toggleSort('cedula')">
                <span>
                  Cédula
                  <span v-if="sortField === 'cedula'" class="sort-arrow">
                    <svg v-if="sortDirection === 'asc'" width="10" height="10" viewBox="0 0 24 24" fill="currentColor"><path d="M12 5l-7 7h14l-7-7z"/></svg>
                    <svg v-else width="10" height="10" viewBox="0 0 24 24" fill="currentColor"><path d="M12 19l7-7H5l7 7z"/></svg>
                  </span>
                  <span v-else class="sort-arrow sort-inactive">
                    <svg width="10" height="14" viewBox="0 0 24 24" fill="currentColor" opacity="0.3"><path d="M12 5l-7 7h14l-7-7z"/><path d="M12 19l7-7H5l7 7z"/></svg>
                  </span>
                </span>
              </th>
              <th class="th-email sortable" @click="toggleSort('email')">
                <span>
                  Email
                  <span v-if="sortField === 'email'" class="sort-arrow">
                    <svg v-if="sortDirection === 'asc'" width="10" height="10" viewBox="0 0 24 24" fill="currentColor"><path d="M12 5l-7 7h14l-7-7z"/></svg>
                    <svg v-else width="10" height="10" viewBox="0 0 24 24" fill="currentColor"><path d="M12 19l7-7H5l7 7z"/></svg>
                  </span>
                  <span v-else class="sort-arrow sort-inactive">
                    <svg width="10" height="14" viewBox="0 0 24 24" fill="currentColor" opacity="0.3"><path d="M12 5l-7 7h14l-7-7z"/><path d="M12 19l7-7H5l7 7z"/></svg>
                  </span>
                </span>
              </th>
              <th class="th-estado sortable" @click="toggleSort('estado')">
                <span>
                  Estado
                  <span v-if="sortField === 'estado'" class="sort-arrow">
                    <svg v-if="sortDirection === 'asc'" width="10" height="10" viewBox="0 0 24 24" fill="currentColor"><path d="M12 5l-7 7h14l-7-7z"/></svg>
                    <svg v-else width="10" height="10" viewBox="0 0 24 24" fill="currentColor"><path d="M12 19l7-7H5l7 7z"/></svg>
                  </span>
                  <span v-else class="sort-arrow sort-inactive">
                    <svg width="10" height="14" viewBox="0 0 24 24" fill="currentColor" opacity="0.3"><path d="M12 5l-7 7h14l-7-7z"/><path d="M12 19l7-7H5l7 7z"/></svg>
                  </span>
                </span>
              </th>
              <th class="th-acciones"><span>Acciones</span></th>
            </tr>
          </thead>
          <tbody>
            <EmpleadoTableRow
              v-for="(empleado, index) in paginatedEmpleados"
              :key="empleado.id"
              :empleado="empleado"
              :index="index"
              @eliminar="eliminarEmpleado"
            />
          </tbody>
        </table>
      </div>
    </div>

    <!-- Pagination -->
    <div v-if="sortedEmpleados.length > 0 && totalPages > 1" class="pagination-bar">
      <div class="pagination-info">
        <span class="pagination-label">Mostrando</span>
        <span class="pagination-range">
          {{ (currentPage - 1) * pageSize + 1 }}–{{ Math.min(currentPage * pageSize, sortedEmpleados.length) }}
        </span>
        <span class="pagination-label">de {{ sortedEmpleados.length }}</span>
      </div>

      <div class="pagination-controls">
        <button class="page-btn" :disabled="currentPage <= 1" @click="currentPage = 1" data-tooltip="Primera página">
          <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round"><polyline points="11 17 6 12 11 7"/><polyline points="18 17 13 12 18 7"/></svg>
        </button>
        <button class="page-btn" :disabled="currentPage <= 1" @click="currentPage--" data-tooltip="Anterior">
          <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round"><polyline points="15 18 9 12 15 6"/></svg>
        </button>

        <template v-for="page in visiblePages" :key="page">
          <button
            v-if="page === '...'"
            class="page-btn page-ellipsis"
            disabled
          >...</button>
          <button
            v-else
            class="page-btn"
            :class="{ active: page === currentPage }"
            @click="currentPage = page"
          >{{ page }}</button>
        </template>

        <button class="page-btn" :disabled="currentPage >= totalPages" @click="currentPage++" data-tooltip="Siguiente">
          <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round"><polyline points="9 18 15 12 9 6"/></svg>
        </button>
        <button class="page-btn" :disabled="currentPage >= totalPages" @click="currentPage = totalPages" data-tooltip="Última página">
          <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round"><polyline points="13 17 18 12 13 7"/><polyline points="6 17 11 12 6 7"/></svg>
        </button>
      </div>

      <div class="pagination-size">
        <label class="size-label">Por página</label>
        <select v-model.number="pageSize" class="size-select">
          <option :value="5">5</option>
          <option :value="10">10</option>
          <option :value="20">20</option>
          <option :value="50">50</option>
        </select>
      </div>
    </div>
  </div>
</template>

<script>
import EmpleadoCard from '@/components/empleados/EmpleadoCard.vue'
import EmpleadoTableRow from '@/components/empleados/EmpleadoTableRow.vue'
import { ref, computed, onMounted, watch } from 'vue'
import axios from 'axios'
import * as XLSX from 'xlsx'

export default {
  components: { EmpleadoCard, EmpleadoTableRow },
  setup() {
    const empleados = ref([])
    const loading = ref(true)
    const searchQuery = ref('')
    const filterEstado = ref('')
    const filterContrato = ref('')
    const filterCargo = ref('')
    const viewMode = ref('cards')
    const sortField = ref('nombre')
    const sortDirection = ref('asc')
    const currentPage = ref(1)
    const pageSize = ref(10)

    // Reset to page 1 when filters change
    watch([searchQuery, filterEstado, filterContrato, filterCargo, sortField, sortDirection], () => {
      currentPage.value = 1
    })

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

    // Unique cargos for filter dropdown
    const uniqueCargos = computed(() => {
      const cargos = new Set(empleados.value.map(e => e.cargo).filter(Boolean))
      return [...cargos].sort()
    })

    // Filtered empleados
    const filteredEmpleados = computed(() => {
      let result = empleados.value

      if (searchQuery.value.trim()) {
        const q = searchQuery.value.trim().toLowerCase()
        result = result.filter(e =>
          `${e.nombres} ${e.apellidos}`.toLowerCase().includes(q) ||
          e.cedula.toLowerCase().includes(q)
        )
      }

      if (filterEstado.value !== '') {
        const isActive = filterEstado.value === 'true'
        result = result.filter(e => e.activo === isActive)
      }

      if (filterContrato.value) {
        result = result.filter(e => e.tipo_contrato === filterContrato.value)
      }

      if (filterCargo.value) {
        result = result.filter(e => e.cargo === filterCargo.value)
      }

      return result
    })

    // Sorted empleados
    const sortedEmpleados = computed(() => {
      const list = [...filteredEmpleados.value]
      const dir = sortDirection.value === 'asc' ? 1 : -1

      list.sort((a, b) => {
        let valA, valB

        switch (sortField.value) {
          case 'nombre':
            valA = `${a.nombres} ${a.apellidos}`.toLowerCase()
            valB = `${b.nombres} ${b.apellidos}`.toLowerCase()
            break
          case 'cedula':
            valA = a.cedula.toLowerCase()
            valB = b.cedula.toLowerCase()
            break
          case 'email':
            valA = a.email.toLowerCase()
            valB = b.email.toLowerCase()
            break
          case 'estado':
            valA = a.activo ? 0 : 1
            valB = b.activo ? 0 : 1
            break
          default:
            return 0
        }

        if (valA < valB) return -1 * dir
        if (valA > valB) return 1 * dir
        return 0
      })

      return list
    })

    // Pagination
    const totalPages = computed(() => Math.max(1, Math.ceil(sortedEmpleados.value.length / pageSize.value)))

    const paginatedEmpleados = computed(() => {
      const start = (currentPage.value - 1) * pageSize.value
      const end = start + pageSize.value
      return sortedEmpleados.value.slice(start, end)
    })

    // Visible page numbers for pagination controls
    const visiblePages = computed(() => {
      const total = totalPages.value
      const current = currentPage.value
      const pages = []

      if (total <= 7) {
        for (let i = 1; i <= total; i++) pages.push(i)
        return pages
      }

      pages.push(1)

      if (current > 3) pages.push('...')

      const start = Math.max(2, current - 1)
      const end = Math.min(total - 1, current + 1)

      for (let i = start; i <= end; i++) pages.push(i)

      if (current < total - 2) pages.push('...')

      pages.push(total)

      return pages
    })

    // Toggle sort
    const toggleSort = (field) => {
      if (sortField.value === field) {
        sortDirection.value = sortDirection.value === 'asc' ? 'desc' : 'asc'
      } else {
        sortField.value = field
        sortDirection.value = 'asc'
      }
    }

    const eliminarEmpleado = async (id) => {
      if (!confirm('¿Está seguro de que desea inactivar este empleado?')) return
      
      try {
        await axios.delete(`/api/empleados/${id}/`)
        fetchEmpleados()
      } catch (error) {
        console.error('Error deleting empleado:', error)
      }
    }

    const clearFilters = () => {
      searchQuery.value = ''
      filterEstado.value = ''
      filterContrato.value = ''
      filterCargo.value = ''
    }

    // Export to Excel
    const exportToExcel = () => {
      const data = sortedEmpleados.value.map(e => ({
        Cédula: e.cedula,
        Nombres: e.nombres,
        Apellidos: e.apellidos,
        Email: e.email,
        Cargo: e.cargo,
        'Tipo Contrato': e.tipo_contrato,
        'Salario Base': Number(e.salario_base),
        'Fecha Ingreso': e.fecha_ingreso,
        'Fecha Retiro': e.fecha_retiro || '',
        EPS: e.eps,
        AFP: e.afp,
        ARL: e.arl,
        Estado: e.activo ? 'Activo' : 'Inactivo',
        Banco: e.banco || '',
        'Cuenta Bancaria': e.cuenta_bancaria || '',
        'Tipo Cuenta': e.tipo_cuenta || ''
      }))

      const ws = XLSX.utils.json_to_sheet(data)

      // Column widths
      ws['!cols'] = [
        { wch: 14 },  // Cédula
        { wch: 18 },  // Nombres
        { wch: 18 },  // Apellidos
        { wch: 28 },  // Email
        { wch: 20 },  // Cargo
        { wch: 16 },  // Tipo Contrato
        { wch: 16 },  // Salario Base
        { wch: 14 },  // Fecha Ingreso
        { wch: 14 },  // Fecha Retiro
        { wch: 14 },  // EPS
        { wch: 14 },  // AFP
        { wch: 14 },  // ARL
        { wch: 10 },  // Estado
        { wch: 18 },  // Banco
        { wch: 16 },  // Cuenta Bancaria
        { wch: 14 },  // Tipo Cuenta
      ]

      const wb = XLSX.utils.book_new()
      XLSX.utils.book_append_sheet(wb, ws, 'Empleados')

      const fileName = `empleados_${new Date().toISOString().split('T')[0]}.xlsx`
      XLSX.writeFile(wb, fileName)
    }

    onMounted(fetchEmpleados)

    return {
      empleados,
      loading,
      searchQuery,
      filterEstado,
      filterContrato,
      filterCargo,
      viewMode,
      sortField,
      sortDirection,
      currentPage,
      pageSize,
      uniqueCargos,
      sortedEmpleados,
      totalPages,
      paginatedEmpleados,
      visiblePages,
      toggleSort,
      eliminarEmpleado,
      clearFilters,
      exportToExcel
    }
  }
}
</script>

<style scoped>
/* ========================================
   TOOLBAR
   ======================================== */
.toolbar {
  display: flex;
  align-items: center;
  flex-wrap: wrap;
  gap: 0.75rem;
  margin-bottom: 1.5rem;
  background: var(--color-bg-white);
  border: 1px solid var(--color-divider);
  border-radius: var(--border-radius-lg);
  padding: 0.75rem 1rem;
  box-shadow: var(--shadow-xs);
  position: relative;
  animation: toolbarSlideIn 0.45s ease both;
}

@keyframes toolbarSlideIn {
  from { opacity: 0; transform: translateY(-8px); }
  to { opacity: 1; transform: translateY(0); }
}

/* Search */
.toolbar-search {
  position: relative;
  flex: 1;
  min-width: 200px;
  max-width: 320px;
}

.search-icon {
  position: absolute;
  left: 0.75rem;
  top: 50%;
  transform: translateY(-50%);
  color: var(--color-text-secondary);
  pointer-events: none;
  opacity: 0.45;
  z-index: 1;
}

.search-input {
  width: 100%;
  padding: 0.5rem 2.25rem 0.5rem 2.25rem;
  font-family: var(--font-body);
  font-size: 0.85rem;
  line-height: 1.5;
  color: var(--color-text-primary);
  background: var(--color-bg-page);
  border: 1.5px solid transparent;
  border-radius: var(--border-radius-sm);
  transition: all var(--transition-fast);
}

.search-input::placeholder {
  color: var(--color-text-secondary);
  opacity: 0.5;
}

.search-input:focus {
  outline: none;
  border-color: var(--color-primary-500);
  background: var(--color-bg-white);
  box-shadow: 0 0 0 3px rgba(55, 138, 221, 0.12);
}

.search-clear {
  position: absolute;
  right: 0.375rem;
  top: 50%;
  transform: translateY(-50%);
  width: 22px;
  height: 22px;
  display: flex;
  align-items: center;
  justify-content: center;
  border: none;
  border-radius: 50%;
  background: var(--color-bg-subtle);
  color: var(--color-text-secondary);
  cursor: pointer;
  opacity: 0.7;
  transition: all var(--transition-fast);
  padding: 0;
  line-height: 1;
}

.search-clear:hover {
  opacity: 1;
  background: var(--color-divider);
}

/* Filters */
.toolbar-filters {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  flex-wrap: wrap;
}

.filter-select {
  padding: 0.5rem 2rem 0.5rem 0.75rem;
  font-family: var(--font-body);
  font-size: 0.8rem;
  color: var(--color-text-primary);
  background: var(--color-bg-page) url("data:image/svg+xml,%3csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 16 16'%3e%3cpath fill='none' stroke='%235F5E5A' stroke-linecap='round' stroke-linejoin='round' stroke-width='2' d='m2 5 6 6 6-6'/%3e%3c/svg%3e") no-repeat right 0.6rem center / 12px 9px;
  border: 1.5px solid transparent;
  border-radius: var(--border-radius-sm);
  cursor: pointer;
  transition: all var(--transition-fast);
  appearance: none;
  min-width: 130px;
}

.filter-select:focus {
  outline: none;
  border-color: var(--color-primary-500);
  background-color: var(--color-bg-white);
  box-shadow: 0 0 0 3px rgba(55, 138, 221, 0.12);
}

.filter-select:hover {
  border-color: var(--color-border);
  background-color: var(--color-bg-white);
}

/* Toolbar right actions */
.toolbar-actions {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  margin-left: auto;
}

/* View toggle */
.toolbar-view {
  display: flex;
  align-items: center;
  gap: 2px;
  padding: 2px;
  background: var(--color-bg-page);
  border-radius: var(--border-radius-sm);
}

.view-toggle-btn {
  width: 34px;
  height: 34px;
  display: flex;
  align-items: center;
  justify-content: center;
  border: none;
  border-radius: 4px;
  background: transparent;
  color: var(--color-text-secondary);
  cursor: pointer;
  transition: all var(--transition-fast);
  position: relative;
}

.view-toggle-btn:hover {
  color: var(--color-text-primary);
}

.view-toggle-btn.active {
  background: var(--color-bg-white);
  color: var(--color-primary-700);
  box-shadow: var(--shadow-xs);
}

/* Result count */
.toolbar-count {
  display: flex;
  align-items: center;
  gap: 0.375rem;
  padding: 0.25rem 0 0.25rem 0.75rem;
  border-left: 1px solid var(--color-divider);
  font-size: 0.8rem;
  color: var(--color-text-secondary);
  white-space: nowrap;
}

.count-badge {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  min-width: 22px;
  height: 22px;
  padding: 0 6px;
  background: var(--color-primary-50);
  color: var(--color-primary-700);
  font-size: 0.75rem;
  font-weight: 600;
  border-radius: 11px;
  line-height: 1;
}

.count-label {
  color: var(--color-text-secondary);
}

/* ========================================
   SORTABLE HEADERS
   ======================================== */
.sortable {
  cursor: pointer;
  user-select: none;
}

.sortable:hover {
  color: var(--color-primary-700);
}

.sort-arrow {
  display: inline-flex;
  align-items: center;
  vertical-align: middle;
  margin-left: 2px;
  transition: opacity var(--transition-fast);
}

.sort-inactive {
  opacity: 0.25;
}

.sortable:hover .sort-inactive {
  opacity: 0.5;
}

/* ========================================
   TABLE VIEW
   ======================================== */
.table-card {
  background: var(--color-bg-white);
  border: 1px solid var(--color-divider);
  border-radius: var(--border-radius-lg);
  overflow: hidden;
  box-shadow: var(--shadow-xs);
  animation: tableFadeIn 0.35s ease both;
}

@keyframes tableFadeIn {
  from { opacity: 0; transform: translateY(6px); }
  to { opacity: 1; transform: translateY(0); }
}

@media (prefers-reduced-motion: reduce) {
  .table-card { animation: none; }
}

.table-scroll {
  overflow-x: auto;
  -webkit-overflow-scrolling: touch;
}

.table-empleados {
  width: 100%;
  border-collapse: collapse;
  font-size: 0.875rem;
}

.table-empleados thead th {
  background: var(--color-bg-subtle);
  color: var(--color-text-secondary);
  font-weight: 600;
  font-size: 0.7rem;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  padding: 0.75rem 0.875rem;
  border-bottom: 2px solid var(--color-divider);
  white-space: nowrap;
  text-align: left;
  position: sticky;
  top: 0;
  z-index: 2;
  transition: color var(--transition-fast), background var(--transition-fast);
}

.table-empleados thead th span {
  display: inline-flex;
  align-items: center;
  gap: 0.25rem;
}

.th-avatar { width: 48px; }
.th-name { min-width: 180px; }
.th-cedula { min-width: 100px; }
.th-email { min-width: 160px; }
.th-estado { width: 80px; }
.th-acciones { width: 80px; text-align: right; }
.th-acciones span { justify-content: flex-end; }

/* ========================================
   PAGINATION
   ======================================== */
.pagination-bar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  flex-wrap: wrap;
  gap: 1rem;
  margin-top: 1.25rem;
  padding: 0.75rem 1rem;
  background: var(--color-bg-white);
  border: 1px solid var(--color-divider);
  border-radius: var(--border-radius-lg);
  box-shadow: var(--shadow-xs);
  animation: paginationFadeIn 0.35s ease both;
}

@keyframes paginationFadeIn {
  from { opacity: 0; transform: translateY(6px); }
  to { opacity: 1; transform: translateY(0); }
}

.pagination-info {
  display: flex;
  align-items: center;
  gap: 0.375rem;
  font-size: 0.85rem;
  color: var(--color-text-secondary);
}

.pagination-range {
  font-weight: 600;
  color: var(--color-text-primary);
}

.pagination-controls {
  display: flex;
  align-items: center;
  gap: 2px;
}

.page-btn {
  min-width: 34px;
  height: 34px;
  padding: 0 0.5rem;
  display: flex;
  align-items: center;
  justify-content: center;
  border: 1px solid transparent;
  border-radius: var(--border-radius-sm);
  background: transparent;
  color: var(--color-text-secondary);
  font-size: 0.8rem;
  font-weight: 500;
  cursor: pointer;
  transition: all var(--transition-fast);
  font-family: var(--font-body);
}

.page-btn:hover:not(:disabled) {
  background: var(--color-primary-50);
  color: var(--color-primary-700);
  border-color: var(--color-primary-200);
}

.page-btn.active {
  background: var(--color-primary-700);
  color: #fff;
  border-color: var(--color-primary-700);
  box-shadow: 0 2px 8px rgba(24, 95, 165, 0.25);
}

.page-btn:disabled {
  opacity: 0.3;
  cursor: not-allowed;
}

.page-ellipsis {
  cursor: default !important;
  background: transparent !important;
  color: var(--color-text-secondary) !important;
  border-color: transparent !important;
}

/* Page size selector */
.pagination-size {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.size-label {
  font-size: 0.8rem;
  color: var(--color-text-secondary);
  white-space: nowrap;
}

.size-select {
  padding: 0.375rem 1.75rem 0.375rem 0.5rem;
  font-family: var(--font-body);
  font-size: 0.8rem;
  color: var(--color-text-primary);
  background: var(--color-bg-page) url("data:image/svg+xml,%3csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 16 16'%3e%3cpath fill='none' stroke='%235F5E5A' stroke-linecap='round' stroke-linejoin='round' stroke-width='2' d='m2 5 6 6 6-6'/%3e%3c/svg%3e") no-repeat right 0.5rem center / 10px 7px;
  border: 1.5px solid var(--color-border);
  border-radius: var(--border-radius-sm);
  cursor: pointer;
  transition: all var(--transition-fast);
  appearance: none;
  width: 64px;
}

.size-select:focus {
  outline: none;
  border-color: var(--color-primary-500);
  box-shadow: 0 0 0 3px rgba(55, 138, 221, 0.12);
}

/* ========================================
   LOADING SKELETON
   ======================================== */
.loading-area {
  animation: fadeIn 0.3s ease;
}

.skeleton-row {
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 0.875rem 1rem;
  border-bottom: 1px solid var(--color-divider);
  height: 56px;
}

.skeleton-row:last-child {
  border-bottom: none;
}

/* ========================================
   RESPONSIVE
   ======================================== */
@media (max-width: 900px) {
  .toolbar {
    flex-direction: column;
    align-items: stretch;
  }

  .toolbar-search {
    max-width: 100%;
  }

  .toolbar-filters {
    flex-wrap: wrap;
  }

  .filter-select {
    flex: 1;
    min-width: 120px;
  }

  .toolbar-actions {
    margin-left: 0;
    justify-content: flex-end;
  }

  .pagination-bar {
    flex-direction: column;
    align-items: center;
    gap: 0.75rem;
  }

  .pagination-controls {
    order: -1;
  }
}

@media (max-width: 640px) {
  .toolbar {
    padding: 0.625rem;
    gap: 0.5rem;
  }

  .toolbar-filters {
    flex-direction: column;
  }

  .filter-select {
    width: 100%;
  }

  .th-email { display: none; }
  .th-cedula { display: none; }

  .pagination-info {
    font-size: 0.8rem;
  }

  .page-btn {
    min-width: 30px;
    height: 30px;
    font-size: 0.75rem;
  }
}

@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}
</style>
