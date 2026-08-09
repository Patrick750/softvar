<template>
  <tr class="table-row" :style="{ '--i': index }">
    <td class="td-avatar">
      <div class="table-avatar">
        <img
          v-if="getProfilePhoto()"
          :src="getProfilePhoto()"
          alt="Foto"
          class="avatar-img-sm"
        >
        <div v-else class="avatar-placeholder avatar-sm">
          {{ getInitials }}
        </div>
      </div>
    </td>
    <td class="td-name">
      <div class="name-cell">
        <span class="name-text">{{ empleado.nombres }} {{ empleado.apellidos }}</span>
        <span class="cargo-text">{{ empleado.cargo }}</span>
      </div>
    </td>
    <td class="td-cedula">
      <span class="cedula-text">{{ empleado.cedula }}</span>
    </td>
    <td class="td-email">
      <span class="email-text" :title="empleado.email">{{ empleado.email }}</span>
    </td>
    <td class="td-estado">
      <span :class="['badge', empleado.activo ? 'badge-success' : 'badge-error']">
        {{ empleado.activo ? 'Activo' : 'Inactivo' }}
      </span>
    </td>
    <td class="td-acciones">
      <div class="action-btns">
        <router-link
          :to="`/empleados/editar/${empleado.id}`"
          class="btn-icon btn-ghost btn-sm-icon"
          data-tooltip="Editar"
        >
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"/>
            <path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"/>
          </svg>
        </router-link>
        <button
          @click="eliminarEmpleado(empleado.id)"
          class="btn-icon btn-ghost btn-sm-icon btn-delete"
          data-tooltip="Eliminar"
        >
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <polyline points="3 6 5 6 21 6"/>
            <path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"/>
            <line x1="10" y1="11" x2="10" y2="17"/>
            <line x1="14" y1="11" x2="14" y2="17"/>
          </svg>
        </button>
      </div>
    </td>
  </tr>
</template>

<script>
export default {
  props: {
    empleado: { type: Object, required: true },
    index: { type: Number, default: 0 }
  },
  emits: ['eliminar'],
  setup(props, { emit }) {
    const getInitials = (props.empleado.nombres ? props.empleado.nombres.charAt(0) : '?') +
      (props.empleado.apellidos ? props.empleado.apellidos.charAt(0) : '?')

    const getProfilePhoto = () => {
      const foto = props.empleado.foto_facial
      if (!foto) return null
      try {
        const parsed = typeof foto === 'string' ? JSON.parse(foto) : foto
        return parsed.image || null
      } catch (e) {
        return foto
      }
    }

    const eliminarEmpleado = () => {
      emit('eliminar', props.empleado)
    }

    return { getInitials, getProfilePhoto, eliminarEmpleado }
  }
}
</script>

<style scoped>
.table-row {
  transition: background var(--transition-fast);
  animation: rowFadeIn 0.35s ease both;
  animation-delay: calc(var(--i, 0) * 40ms);
}

@keyframes rowFadeIn {
  from { opacity: 0; transform: translateX(-8px); }
  to { opacity: 1; transform: translateX(0); }
}

@media (prefers-reduced-motion: reduce) {
  .table-row { animation: none; }
}

.table-row:hover {
  background: var(--color-primary-50);
}

.table-row:active td {
  background: var(--color-primary-200);
}

.table-row td {
  padding: 0.625rem 0.875rem;
  vertical-align: middle;
  border-bottom: 1px solid var(--color-divider);
  font-size: 0.85rem;
  transition: background var(--transition-fast);
}

/* Avatar column */
.td-avatar {
  width: 48px;
  padding-right: 0 !important;
}

.table-avatar {
  display: flex;
  align-items: center;
  justify-content: center;
}

.avatar-img-sm {
  width: 34px;
  height: 34px;
  object-fit: cover;
  border-radius: 50%;
  border: 2px solid var(--color-primary-200);
}

.avatar-placeholder.avatar-sm {
  width: 34px;
  height: 34px;
  border-radius: 50%;
  font-size: 0.75rem;
  font-weight: 600;
  background: var(--color-primary-200);
  color: var(--color-primary-700);
  display: flex;
  align-items: center;
  justify-content: center;
  border: 2px solid var(--color-primary-50);
}

/* Name + Cargo column */
.td-name {
  min-width: 180px;
}

.name-cell {
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.name-text {
  font-weight: 600;
  color: var(--color-text-primary);
  font-size: 0.875rem;
  line-height: 1.3;
}

.cargo-text {
  font-size: 0.75rem;
  color: var(--color-text-secondary);
  line-height: 1.2;
}

/* Cédula */
.td-cedula {
  min-width: 100px;
}

.cedula-text {
  font-family: var(--font-mono, 'SF Mono', monospace);
  font-size: 0.8125rem;
  color: var(--color-text-primary);
  letter-spacing: 0.01em;
}

/* Email */
.td-email {
  min-width: 160px;
  max-width: 220px;
}

.email-text {
  color: var(--color-text-secondary);
  font-size: 0.8125rem;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  display: block;
}

/* Estado */
.td-estado {
  width: 80px;
}

/* Actions */
.td-acciones {
  width: 80px;
  text-align: right;
}

.action-btns {
  display: flex;
  align-items: center;
  justify-content: flex-end;
  gap: 0.25rem;
  opacity: 0;
  transition: opacity var(--transition-fast);
}

.table-row:hover .action-btns {
  opacity: 1;
}

.action-btns .btn-icon {
  width: 32px;
  height: 32px;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  border: none;
  border-radius: var(--border-radius-sm);
  background: transparent;
  color: var(--color-text-secondary);
  cursor: pointer;
  transition: all var(--transition-fast);
  text-decoration: none;
}

.action-btns .btn-icon:hover {
  background: var(--color-primary-50);
  color: var(--color-primary-700);
}

.action-btns .btn-delete:hover {
  background: var(--color-error-bg);
  color: var(--color-error-accent);
}

/* Show actions always on touch devices */
@media (hover: none) {
  .action-btns {
    opacity: 1;
  }
}

@media (max-width: 768px) {
  .td-email { display: none; }
  .td-cedula { display: none; }
  .table-row td {
    padding: 0.5rem 0.625rem;
  }
}
</style>
