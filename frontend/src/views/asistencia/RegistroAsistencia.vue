<template>
  <div>
    <div class="page-header">
      <h1 class="display-heading">Registro de Asistencia</h1>
      <p class="text-muted">Verifique su identidad para registrar entrada o salida</p>
    </div>

    <div class="layout-grid grid-2">
      <!-- Camera Card -->
      <div class="card card-elevated p-0">
        <div class="card-header-primary">
          <h5><i class="bi bi-camera-video me-2"></i>Registro Biométrico</h5>
        </div>
        <div class="card-body">
          <!-- Video container -->
          <div class="camera-frame mb-3">
            <video
              id="videoElement"
              autoplay
              playsinline
              class="camera-video"
              :class="{ 'camera-active': isCameraActive }"
            ></video>
            <div v-if="!isCameraActive" class="camera-overlay">
              <i class="bi bi-camera-video-off camera-overlay-icon"></i>
              <p>Cámara inactiva</p>
            </div>
          </div>

          <!-- Controls -->
          <div class="flex-row gap-sm">
            <button class="btn btn-success" @click="startCamera" :disabled="isCameraActive">
              <i class="bi bi-camera-video me-2"></i>
              Iniciar Cámara
            </button>
            <button class="btn btn-primary" @click="captureAndVerify" :disabled="!isCameraActive">
              <i class="bi bi-check-circle me-2"></i>
              Verificar Asistencia
            </button>
            <button class="btn btn-outline" @click="stopCamera" :disabled="!isCameraActive">
              <i class="bi bi-x-circle me-2"></i>
              Detener
            </button>
          </div>

          <!-- Captured preview -->
          <div v-if="capturedImage" class="mt-3 text-center">
            <img :src="capturedImage" alt="Captura" class="img-capture">
          </div>
        </div>
      </div>

      <!-- Info Card -->
      <div class="card card-elevated p-0">
        <div class="card-header-info">
          <h5><i class="bi bi-info-circle me-2"></i>Información de Asistencia</h5>
        </div>
        <div class="card-body">
          <div v-if="employeeInfo" class="employee-section">
            <div class="flex-row items-center gap-md mb-3">
              <div class="avatar avatar-md avatar-placeholder">
                {{ (employeeInfo.nombres?.charAt(0) || '') + (employeeInfo.apellidos?.charAt(0) || '') }}
              </div>
              <div>
                <h6 class="fw-semibold mb-1">{{ employeeInfo.nombres }} {{ employeeInfo.apellidos }}</h6>
                <span class="badge badge-info">{{ employeeInfo.cargo }}</span>
              </div>
            </div>
            <div class="divider"></div>
            <div class="d-flex justify-between mb-2">
              <span class="text-muted">Último registro:</span>
              <span class="fw-semibold">{{ lastAttendance?.fecha_hora || 'N/A' }}</span>
            </div>
          </div>

          <div v-else class="text-center py-4">
            <div class="spinner spinner-lg mx-auto"></div>
            <p class="mt-3 text-muted">Verificando identidad...</p>
          </div>

          <!-- Verification status -->
          <div v-if="showVerification" class="mt-4">
            <h6 class="fw-semibold mb-2">Estado de Verificación:</h6>
            <div class="alert" :class="'alert-' + verificationState.type">
              <div class="flex-row items-start gap-md">
                <i :class="'bi ' + verificationIcon" class="flex-shrink: 0" style="font-size: 1.25rem;"></i>
                <div>
                  <div class="fw-semibold">{{ verificationState.message }}</div>
                  <small class="opacity-75" v-if="verificationState.details">{{ verificationState.details }}</small>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Today's history -->
    <div class="card card-elevated mt-4 p-0">
      <div class="card-header-accent">
        <h5><i class="bi bi-clock-history me-2"></i>Historial de Asistencia Hoy</h5>
      </div>
      <div class="card-body">
        <div class="table-container">
          <table class="table table-compact">
            <thead>
              <tr><th>Hora</th><th>Tipo</th><th>Estado</th><th>Observaciones</th></tr>
            </thead>
            <tbody>
              <tr v-for="(attendance, idx) in todayAttendances" :key="attendance.id" class="data-row" :style="{ '--i': idx }">
                <td>{{ attendance.fecha_hora }}</td>
                <td>
                  <span class="badge" :class="attendance.tipo === 'ENTRADA' ? 'badge-info' : 'badge-neutral'">
                    {{ attendance.tipo }}
                  </span>
                </td>
                <td>
                  <span class="badge" :class="attendance.estado === 'EXITO' ? 'badge-success' : 'badge-error'">
                    {{ attendance.estado }}
                  </span>
                </td>
                <td>{{ attendance.observaciones || '-' }}</td>
              </tr>
              <tr v-if="!todayAttendances.length" class="empty-row">
                <td colspan="4" class="text-center text-muted py-4">No hay registros de asistencia hoy</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, reactive, computed, onMounted, onUnmounted } from 'vue'

export default {
  setup() {
    const isCameraActive = ref(false)
    const capturedImage = ref(null)
    const employeeInfo = ref(null)
    const lastAttendance = ref(null)
    const todayAttendances = ref([])
    let videoStream = null

    const verificationState = reactive({
      show: false, message: '', details: '', type: 'info'
    })

    const loadEmployeeData = async () => {
      employeeInfo.value = {
        id: 1, nombres: 'Juan Pablo', apellidos: 'García López',
        cedula: '1234567890', cargo: 'Asistente Administrativo',
        email: 'juan.garcia@empresa.com', foto_facial: null
      }
      lastAttendance.value = {
        fecha_hora: new Date().toLocaleTimeString('es-CO', { hour: '2-digit', minute: '2-digit' })
      }
      todayAttendances.value = [
        { id: 1, fecha_hora: '08:05 AM', tipo: 'ENTRADA', estado: 'EXITO', observaciones: 'Registro exitoso' }
      ]
    }

    const startCamera = async () => {
      try {
        const stream = await navigator.mediaDevices.getUserMedia({ video: { width: 640, height: 480 } })
        videoStream = stream
        const video = document.getElementById('videoElement')
        video.srcObject = stream
        isCameraActive.value = true
        verificationState.show = false
        capturedImage.value = null
      } catch (err) {
        console.error('Error accessing camera:', err)
        alert('No se pudo acceder a la cámara. Verifique permisos.')
      }
    }

    const stopCamera = () => {
      if (videoStream) {
        videoStream.getTracks().forEach(track => track.stop())
        videoStream = null
      }
      isCameraActive.value = false
      const video = document.getElementById('videoElement')
      video.srcObject = null
    }

    const captureAndVerify = async () => {
      if (!videoStream) return
      const video = document.getElementById('videoElement')
      const canvas = document.createElement('canvas')
      canvas.width = video.videoWidth
      canvas.height = video.videoHeight
      const ctx = canvas.getContext('2d')
      ctx.drawImage(video, 0, 0, canvas.width, canvas.height)
      capturedImage.value = canvas.toDataURL('image/jpeg')
      await simulateVerification()
      stopCamera()
    }

    const simulateVerification = async () => {
      Object.assign(verificationState, {
        show: true, message: 'Verificando identidad...',
        details: 'Analizando características faciales y ubicación GPS', type: 'info'
      })
      await new Promise(r => setTimeout(r, 2000))

      const isFaceMatch = Math.random() > 0.2
      const isGpsValid = Math.random() > 0.1

      if (isFaceMatch && isGpsValid) {
        Object.assign(verificationState, {
          message: 'Asistencia registrada exitosamente',
          details: 'Facial: 92% coincidencia | GPS: Dentro del rango permitido', type: 'success'
        })
        const newAttendance = {
          id: Date.now(),
          fecha_hora: new Date().toLocaleTimeString('es-CO', { hour: '2-digit', minute: '2-digit' }),
          tipo: lastAttendance.value?.tipo === 'ENTRADA' ? 'SALIDA' : 'ENTRADA',
          estado: 'EXITO', observaciones: 'Registro biométrico exitoso'
        }
        todayAttendances.value.unshift(newAttendance)
        lastAttendance.value = newAttendance
      } else if (!isFaceMatch) {
        Object.assign(verificationState, {
          message: 'Verificación facial fallida',
          details: 'La coincidencia facial es inferior al 80% requerido', type: 'error'
        })
      } else {
        Object.assign(verificationState, {
          message: 'Ubicación fuera de rango',
          details: 'El GPS indica que está fuera del rango permitido (100m)', type: 'warning'
        })
      }
    }

    const verificationAlertClass = computed(() => ({
      success: 'alert-success', error: 'alert-error', warning: 'alert-warning', info: 'alert-info'
    }[verificationState.type] || 'alert-info'))

    const verificationIcon = computed(() => ({
      success: 'bi-check-circle-fill', error: 'bi-exclamation-triangle-fill',
      warning: 'bi-exclamation-triangle', info: 'bi-info-circle-fill'
    }[verificationState.type] || 'bi-info-circle-fill'))

    const showVerification = computed(() => verificationState.show)

    onMounted(loadEmployeeData)
    onUnmounted(stopCamera)

    return {
      isCameraActive, capturedImage, employeeInfo, lastAttendance,
      todayAttendances, verificationState, startCamera, stopCamera,
      captureAndVerify, verificationAlertClass, verificationIcon, showVerification
    }
  }
}
</script>

<style scoped>
.camera-frame {
  position: relative;
  border-radius: var(--border-radius-md);
  overflow: hidden;
  background: var(--color-bg-subtle);
  aspect-ratio: 4/3;
}

.camera-video {
  width: 100%;
  height: 100%;
  object-fit: cover;
  opacity: 0.3;
  transition: opacity var(--transition-base);
}

.camera-video.camera-active {
  opacity: 1;
}

.camera-overlay {
  position: absolute;
  inset: 0;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  color: var(--color-text-secondary);
}

.camera-overlay-icon {
  font-size: 3rem;
  margin-bottom: 0.5rem;
  opacity: 0.4;
}

.img-capture {
  max-width: 200px;
  border-radius: var(--border-radius-sm);
  box-shadow: var(--shadow-md);
}

.employee-section {
  background: var(--color-bg-subtle);
  border-radius: var(--border-radius-md);
  padding: 1.25rem;
}

.data-row {
  opacity: 0;
  transform: translateY(8px);
  animation: fadeInRow 0.35s ease forwards;
  animation-delay: calc(var(--i, 0) * 60ms);
  transition: background 0.2s, transform 0.15s;
  cursor: pointer;
}

.data-row:hover {
  background: var(--color-primary-50);
}

.data-row:active {
  transform: scale(0.995);
}

.data-row:last-child td {
  border-bottom: none;
}

.empty-row td {
  border-bottom: none;
}

@keyframes fadeInRow {
  from {
    opacity: 0;
    transform: translateY(8px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

@media (prefers-reduced-motion: reduce) {
  .data-row {
    animation: none;
    opacity: 1;
    transform: none;
  }
}

@media (max-width: 768px) {
  .layout-grid { grid-template-columns: 1fr; }
}
</style>
