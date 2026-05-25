<template>
  <div class="empleado-card card p-0">
    <div class="card-header-avatar">
      <div class="avatar-container">
        <img
          v-if="getProfilePhoto()"
          :src="getProfilePhoto()"
          alt="Foto de empleado"
          class="avatar-img"
        >
        <div v-else class="avatar-placeholder avatar-lg">
          {{ getInitials }}
        </div>
      </div>
      <div class="card-info">
        <h3 class="empleado-name">{{ empleado.nombres }} {{ empleado.apellidos }}</h3>
        <p class="empleado-cargo">{{ empleado.cargo }}</p>
        <span :class="['badge', empleado.activo ? 'badge-success' : 'badge-error']">
          {{ empleado.activo ? 'Activo' : 'Inactivo' }}
        </span>
      </div>
    </div>

    <div class="card-body">
      <div class="info-row">
        <span class="info-label"><i class="bi bi-person-vcard me-2"></i>Cédula</span>
        <span class="info-value">{{ empleado.cedula }}</span>
      </div>
      <div class="info-row">
        <span class="info-label"><i class="bi bi-envelope me-2"></i>Email</span>
        <span class="info-value">{{ empleado.email }}</span>
      </div>
      <div class="info-row">
        <span class="info-label"><i class="bi bi-coin me-2"></i>Salario</span>
        <span class="info-value">{{ formatoMoneda(empleado.salario_base) }}</span>
      </div>
      <div class="info-row">
        <span class="info-label"><i class="bi bi-file-text me-2"></i>Contrato</span>
        <span class="info-value">{{ obtenerTipoContrato(empleado.tipo_contrato) }}</span>
      </div>
    </div>

    <div class="card-footer">
      <router-link
        :to="`/empleados/editar/${empleado.id}`"
        class="btn btn-outline-primary btn-sm"
      >
        <i class="bi bi-pencil"></i>
        Editar
      </router-link>
      <button
        @click="eliminarEmpleado(empleado.id)"
        class="btn btn-outline-danger btn-sm"
      >
        <i class="bi bi-trash"></i>
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
      }).format(valor)
    }

    const obtenerTipoContrato = (tipo) => {
      const tipos = {
        'TERMINO_FIJO': 'Término Fijo',
        'TERMINO_INDEFINIDO': 'Término Indefinido',
        'OBRA_LABOR': 'Obra Labor',
        'PRESTACION_SERVICIOS': 'Prestación de Servicios'
      }
      return tipos[tipo] || tipo
    }

    const eliminarEmpleado = (id) => {
      if (confirm('¿Está seguro de eliminar este empleado?')) {
        emit('empleado-eliminado', id)
      }
    }

    const getProfilePhoto = () => {
      const foto = props.empleado.foto_facial
      if (!foto) return null
      try {
        const parsed = typeof foto === 'string' ? JSON.parse(foto) : foto
        return parsed.image || null
      } catch (e) {
        // Si no es JSON, asumir que es una URL directa
        return foto
      }
    }

    return {
      formatoMoneda,
      obtenerTipoContrato,
      eliminarEmpleado,
      getProfilePhoto,
      getInitials: (props.empleado.nombres ? props.empleado.nombres.charAt(0) : '?') +
        (props.empleado.apellidos ? props.empleado.apellidos.charAt(0) : '?')
    }
  }
}
</script>

<style scoped>
.empleado-card {
  overflow: hidden;
  transition: transform var(--transition-base), box-shadow var(--transition-base);
  height: 100%;
  display: flex;
  flex-direction: column;
}

.empleado-card:hover {
  transform: translateY(-4px);
  box-shadow: var(--shadow-lg);
}

.card-header-avatar {
  background: linear-gradient(135deg, var(--color-primary-700), var(--color-primary-500));
  color: white;
  padding: 1.5rem;
  display: flex;
  align-items: center;
  gap: 1.25rem;
}

.avatar-container {
  flex-shrink: 0;
}

.avatar-img {
  width: 64px;
  height: 64px;
  object-fit: cover;
  border-radius: 50%;
  border: 3px solid rgba(255, 255, 255, 0.3);
}

.card-info {
  flex: 1;
  min-width: 0;
}

.empleado-name {
  margin: 0 0 0.25rem;
  font-size: 1.125rem;
  font-weight: 700;
  color: #fff;
}

.empleado-cargo {
  margin: 0 0 0.75rem;
  opacity: 0.85;
  font-size: 0.875rem;
}

.card-body {
  flex: 1;
  padding: 1.25rem 1.5rem;
}

.info-row {
  display: flex;
  justify-content: space-between;
  padding: 0.625rem 0;
  border-bottom: 1px solid var(--color-divider);
  font-size: 0.875rem;
}

.info-row:last-child {
  border-bottom: none;
}

.info-label {
  color: var(--color-text-secondary);
  display: flex;
  align-items: center;
}

.info-label i {
  font-size: 0.875rem;
}

.info-value {
  font-weight: 600;
  color: var(--color-text-primary);
  text-align: right;
}

.card-footer {
  display: flex;
  gap: 0.75rem;
  padding: 1rem 1.5rem;
  background: var(--color-bg-subtle);
  border-top: 1px solid var(--color-divider);
}

.card-footer .btn {
  flex: 1;
}

@media (max-width: 640px) {
  .card-header-avatar {
    flex-direction: column;
    text-align: center;
  }
  .card-info {
    text-align: center;
  }
  .info-row {
    flex-direction: column;
    gap: 0.25rem;
  }
  .card-footer {
    flex-direction: column;
  }
}
</style>
