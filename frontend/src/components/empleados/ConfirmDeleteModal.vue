<template>
  <Transition name="modal-fade">
    <div v-if="show" class="modal-backdrop" @click.self="onCancel">
      <div class="modal-card" role="dialog" aria-modal="true">
        <!-- Close button -->
        <button class="modal-close-btn" @click="onCancel" aria-label="Cerrar modal">
          <i class="bi bi-x-lg"></i>
        </button>

        <!-- Warning Icon Badge -->
        <div class="modal-header-icon">
          <div class="icon-pulse-badge">
            <i class="bi bi-trash3-fill"></i>
          </div>
        </div>

        <!-- Title & description -->
        <div class="modal-content-center">
          <h3 class="modal-title">¿Eliminar Empleado?</h3>
          <p class="modal-subtitle">
            ¿Está seguro de que desea inactivar este empleado? No podrá registrar asistencias mientras esté inactivo.
          </p>

          <!-- Employee summary badge -->
          <div v-if="empleado" class="empleado-preview-box">
            <div class="preview-avatar">
              <img v-if="getProfilePhoto(empleado.foto_facial)" :src="getProfilePhoto(empleado.foto_facial)" class="preview-avatar-img" alt="Foto" />
              <div v-else class="preview-avatar-initials">
                {{ getInitials(empleado) }}
              </div>
            </div>
            <div class="preview-details">
              <h4 class="preview-name">{{ empleado.nombres }} {{ empleado.apellidos }}</h4>
              <p class="preview-cargo">{{ empleado.cargo || 'Empleado' }}</p>
              <div class="preview-meta">
                <span class="preview-chip"><i class="bi bi-person-vcard me-1"></i>{{ empleado.cedula }}</span>
                <span v-if="empleado.email" class="preview-chip"><i class="bi bi-envelope me-1"></i>{{ empleado.email }}</span>
              </div>
            </div>
          </div>

          <!-- Actions -->
          <div class="modal-actions">
            <button type="button" class="btn-cancel" @click="onCancel" :disabled="loading">
              Cancelar
            </button>
            <button type="button" class="btn-confirm-delete" @click="onConfirm" :disabled="loading">
              <span v-if="loading" class="spinner-sm me-2"></span>
              <i v-else class="bi bi-trash3 me-1"></i>
              Sí, Eliminar
            </button>
          </div>
        </div>
      </div>
    </div>
  </Transition>
</template>

<script>
import { onMounted, onUnmounted } from 'vue'

export default {
  name: 'ConfirmDeleteModal',
  props: {
    show: {
      type: Boolean,
      default: false
    },
    empleado: {
      type: Object,
      default: null
    },
    loading: {
      type: Boolean,
      default: false
    }
  },
  emits: ['confirm', 'close'],
  setup(props, { emit }) {
    const onCancel = () => {
      if (!props.loading) {
        emit('close')
      }
    }

    const onConfirm = () => {
      emit('confirm')
    }

    const handleKeyDown = (e) => {
      if (e.key === 'Escape' && props.show) {
        onCancel()
      }
    }

    const getProfilePhoto = (fotoFacial) => {
      if (!fotoFacial) return null
      try {
        const parsed = typeof fotoFacial === 'string' ? JSON.parse(fotoFacial) : fotoFacial
        return parsed.image || null
      } catch (e) {
        return fotoFacial
      }
    }

    const getInitials = (emp) => {
      if (!emp) return '?'
      const n = emp.nombres ? emp.nombres.charAt(0) : ''
      const a = emp.apellidos ? emp.apellidos.charAt(0) : ''
      return (n + a).toUpperCase() || '?'
    }

    onMounted(() => window.addEventListener('keydown', handleKeyDown))
    onUnmounted(() => window.removeEventListener('keydown', handleKeyDown))

    return {
      onCancel,
      onConfirm,
      getProfilePhoto,
      getInitials
    }
  }
}
</script>

<style scoped>
.modal-backdrop {
  position: fixed;
  inset: 0;
  background: rgba(15, 23, 42, 0.65);
  backdrop-filter: blur(6px);
  -webkit-backdrop-filter: blur(6px);
  z-index: 2000;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 1.25rem;
}

.modal-card {
  background: #FFFFFF;
  border-radius: 20px;
  max-width: 440px;
  width: 100%;
  padding: 2rem 1.75rem;
  box-shadow: 0 20px 50px rgba(0, 0, 0, 0.2), 0 4px 12px rgba(0, 0, 0, 0.08);
  position: relative;
  border: 1px solid rgba(226, 232, 240, 0.8);
}

.modal-close-btn {
  position: absolute;
  top: 1.25rem;
  right: 1.25rem;
  background: #F1F5F9;
  border: none;
  width: 32px;
  height: 32px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  color: #64748B;
  transition: all 0.2s ease;
}

.modal-close-btn:hover {
  background: #E2E8F0;
  color: #0F172A;
}

.modal-header-icon {
  display: flex;
  justify-content: center;
  margin-bottom: 1.25rem;
}

.icon-pulse-badge {
  width: 64px;
  height: 64px;
  background: #FEE2E2;
  color: #DC2626;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.75rem;
  box-shadow: 0 0 0 8px #FEF2F2;
}

.modal-content-center {
  text-align: center;
}

.modal-title {
  font-size: 1.35rem;
  font-weight: 700;
  color: #0F172A;
  margin-bottom: 0.5rem;
}

.modal-subtitle {
  font-size: 0.875rem;
  color: #64748B;
  line-height: 1.5;
  margin-bottom: 1.25rem;
}

.empleado-preview-box {
  background: #F8FAFC;
  border: 1px solid #E2E8F0;
  border-radius: 14px;
  padding: 1rem;
  display: flex;
  align-items: center;
  gap: 1rem;
  text-align: left;
  margin-bottom: 1.5rem;
}

.preview-avatar {
  flex-shrink: 0;
}

.preview-avatar-img, .preview-avatar-initials {
  width: 48px;
  height: 48px;
  border-radius: 50%;
  object-fit: cover;
}

.preview-avatar-initials {
  background: #3B489E;
  color: #FFFFFF;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 700;
  font-size: 1rem;
}

.preview-details {
  flex: 1;
  min-width: 0;
}

.preview-name {
  font-size: 0.975rem;
  font-weight: 700;
  color: #0F172A;
  margin: 0 0 0.15rem 0;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.preview-cargo {
  font-size: 0.825rem;
  color: #64748B;
  margin: 0 0 0.4rem 0;
}

.preview-meta {
  display: flex;
  flex-wrap: wrap;
  gap: 0.4rem;
}

.preview-chip {
  background: #FFFFFF;
  border: 1px solid #CBD5E1;
  border-radius: 6px;
  padding: 0.15rem 0.45rem;
  font-size: 0.725rem;
  color: #475467;
  font-weight: 500;
}

.modal-actions {
  display: flex;
  gap: 0.75rem;
}

.btn-cancel {
  flex: 1;
  background: #FFFFFF;
  border: 1px solid #D0D5DD;
  border-radius: 10px;
  padding: 0.65rem 1rem;
  font-weight: 600;
  font-size: 0.9rem;
  color: #344054;
  cursor: pointer;
  transition: all 0.2s ease;
}

.btn-cancel:hover:not(:disabled) {
  background: #F8FAFC;
}

.btn-confirm-delete {
  flex: 1;
  background: #DC2626;
  border: none;
  border-radius: 10px;
  padding: 0.65rem 1rem;
  font-weight: 600;
  font-size: 0.9rem;
  color: #FFFFFF;
  cursor: pointer;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  transition: background 0.2s ease;
}

.btn-confirm-delete:hover:not(:disabled) {
  background: #B91C1C;
}

.spinner-sm {
  width: 16px;
  height: 16px;
  border: 2px solid rgba(255,255,255,0.3);
  border-top-color: #FFFFFF;
  border-radius: 50%;
  animation: spin 0.6s linear infinite;
  display: inline-block;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

/* Modal Transition */
.modal-fade-enter-active,
.modal-fade-leave-active {
  transition: opacity 0.25s ease;
}

.modal-fade-enter-active .modal-card,
.modal-fade-leave-active .modal-card {
  transition: transform 0.25s cubic-bezier(0.34, 1.56, 0.64, 1);
}

.modal-fade-enter-from,
.modal-fade-leave-to {
  opacity: 0;
}

.modal-fade-enter-from .modal-card,
.modal-fade-leave-to .modal-card {
  transform: scale(0.92);
}
</style>
