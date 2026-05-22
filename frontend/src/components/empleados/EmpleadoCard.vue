<template>
  <div class="empleado-card">
    <div class="card-header">
      <div class="avatar-container">
        <img
          v-if="empleado.foto_facial"
          :src="empleado.foto_facial"
          alt="Foto de empleado"
          class="avatar-img"
        >
        <div v-else class="avatar-placeholder">
          {{ (empleado.nombres ? empleado.nombres.charAt(0) : '?') }}{{ (empleado.apellidos ? empleado.apellidos.charAt(0) : '?') }}
        </div>
      </div>
      <div class="card-info">
        <h3 class="empleado-name">{{ empleado.nombres }} {{ empleado.apellidos }}</h3>
        <p class="empleado-cargo">{{ empleado.cargo }}</p>
        <span :class="['empleado-status', empleado.activo ? 'status-activo' : 'status-inactivo']">
          {{ empleado.activo ? 'Activo' : 'Inactivo' }}
        </span>
      </div>
    </div>

    <div class="card-body">
      <div class="info-row">
        <span class="info-label">Cédula:</span>
        <span class="info-value">{{ empleado.cedula }}</span>
      </div>
      <div class="info-row">
        <span class="info-label">Email:</span>
        <span class="info-value">{{ empleado.email }}</span>
      </div>
      <div class="info-row">
        <span class="info-label">Salario:</span>
        <span class="info-value">{{ formatoMoneda(empleado.salario_base) }}</span>
      </div>
      <div class="info-row">
        <span class="info-label">Contrato:</span>
        <span class="info-value">{{ obtenerTipoContrato(empleado.tipo_contrato) }}</span>
      </div>
    </div>

    <div class="card-footer">
      <router-link
        :to="`/empleados/editar/${empleado.id}`"
        class="btn btn-edit"
      >
        Editar
      </router-link>
      <button
        @click="eliminarEmpleado(empleado.id)"
        class="btn btn-delete"
      >
        Eliminar
      </button>
    </div>
  </div>
</template>

<script>
export default {
  props: {
    empleado: {
      type: Object,
      required: true
    }
  },
  emits: ['empleado-eliminado'],
  setup(props, { emit }) {
    const formatoMoneda = (valor) => {
      return new Intl.NumberFormat('es-CO', {
        style: 'currency',
        currency: 'COP'
      }).format(valor);
    };

    const obtenerTipoContrato = (tipo) => {
      const tipos = {
        'TERMINO_FIJO': 'Término Fijo',
        'TERMINO_INDEFINIDO': 'Término Indefinido',
        'OBRA_LABOR': 'Obra Labor',
        'PRESTACION_SERVICIOS': 'Prestación de Servicios'
      };
      return tipos[tipo] || tipo;
    };

    const eliminarEmpleado = (id) => {
      if (confirm('¿Está seguro de eliminar este empleado?')) {
        emit('empleado-eliminado', id);
      }
    };

    return {
      formatoMoneda,
      obtenerTipoContrato,
      eliminarEmpleado
    };
  }
}
</script>

<style scoped>
.empleado-card {
  background: var(--color-bg-page);
  border-radius: 16px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
  overflow: hidden;
  transition: transform 0.3s ease, box-shadow 0.3s ease;
  height: 100%;
  display: flex;
  flex-direction: column;
}

.empleado-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 15px rgba(0, 0, 0, 0.1);
}

.card-header {
  background: linear-gradient(135deg, var(--color-primary-700), var(--color-primary-500));
  color: white;
  padding: 1.5rem;
  display: flex;
  align-items: center;
  gap: 1.5rem;
}

.avatar-container {
  position: relative;
  width: 60px;
  height: 60px;
  flex-shrink: 0;
}

.avatar-img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  border-radius: 50%;
  border: 3px solid var(--color-primary-50);
}

.avatar-placeholder {
  width: 100%;
  height: 100%;
  background: var(--color-primary-200);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: bold;
  font-size: 1.5rem;
  color: var(--color-primary-700);
  border: 3px solid var(--color-primary-50);
}

.card-info {
  flex: 1;
}

.empleado-name {
  margin: 0 0 0.5rem 0;
  font-size: 1.25rem;
  font-weight: 600;
}

.empleado-cargo {
  margin: 0 0 0.75rem 0;
  opacity: 0.9;
  font-size: 0.95rem;
}

.empleado-status {
  padding: 0.25rem 0.75rem;
  border-radius: 20px;
  font-size: 0.85rem;
  font-weight: 500;
}

.status-activo {
  background: var(--color-semantic-success-bg);
  color: var(--color-semantic-success-accent);
}

.status-inactivo {
  background: var(--color-semantic-error-bg);
  color: var(--color-semantic-error-accent);
}

.card-body {
  flex: 1;
  padding: 1.5rem;
}

.info-row {
  display: flex;
  justify-content: space-between;
  padding: 0.75rem 0;
  border-bottom: 1px solid var(--color-neutral-divider);
}

.info-row:last-child {
  border-bottom: none;
}

.info-label {
  color: var(--color-neutral-text-secondary);
  font-weight: 500;
}

.info-value {
  font-weight: 600;
  color: var(--color-neutral-text-primary);
}

.card-footer {
  padding: 1.5rem;
  display: flex;
  gap: 1rem;
  border-top: 1px solid var(--color-neutral-divider);
  background: var(--color-primary-50);
}

.btn {
  flex: 1;
  padding: 0.75rem;
  border: none;
  border-radius: 8px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s ease;
  font-size: 0.9rem;
}

.btn-edit {
  background: var(--color-secondary-500);
  color: white;
}

.btn-edit:hover {
  background: var(--color-secondary-700);
  transform: translateY(-2px);
}

.btn-delete {
  background: var(--color-semantic-error-bg);
  color: var(--color-semantic-error-accent);
  border: 1px solid var(--color-semantic-error-accent);
}

.btn-delete:hover {
  background: var(--color-semantic-error-accent);
  color: white;
  transform: translateY(-2px);
}

/* Responsive design */
@media (max-width: 640px) {
  .card-header {
    flex-direction: column;
    text-align: center;
    gap: 1rem;
  }

  .card-info {
    text-align: center;
  }

  .info-row {
    flex-direction: column;
    gap: 0.5rem;
    align-items: flex-start;
  }

  .info-label {
    width: 80px;
  }

  .card-footer {
    flex-direction: column;
  }
}
</style>