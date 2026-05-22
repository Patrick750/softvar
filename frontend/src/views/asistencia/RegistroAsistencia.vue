<template>
  <div class="container mt-4">
    <h2>Registro de Asistencia</h2>
    <div class="row g-4">
      <div class="col-md-6">
        <div class="card">
          <div class="card-header bg-primary text-white">
            <h5 class="mb-0">Registro de Entrada/Salida</h5>
          </div>
          <div class="card-body">
            <div id="videoContainer" class="ratio ratio-16x9 mb-3">
              <video
                id="videoElement"
                autoplay
                playsinline
                class="w-100 h-100 object-fit-cover"
              ></video>
            </div>

            <div class="d-grid gap-2">
              <button
                id="startButton"
                class="btn btn-success"
                @click="startCamera"
              >
                <i class="bi bi-camera-video me-2"></i>
                Iniciar Cámara
              </button>

              <button
                id="captureButton"
                class="btn btn-primary"
                @click="captureAndVerify"
                :disabled="!isCameraActive"
              >
                <i class="bi bi-check-circle me-2"></i>
                Verificar Asistencia
              </button>

              <button
                id="stopButton"
                class="btn btn-outline-secondary"
                @click="stopCamera"
                :disabled="!isCameraActive"
              >
                <i class="bi bi-x-circle me-2"></i>
                Detener Cámara
              </button>
            </div>

            <div class="mt-3" v-if="capturedImage">
              <div class="text-center">
                <img
                  :src="capturedImage"
                  alt="Foto capturada"
                  class="img-thumbnail"
                  style="max-width: 200px;"
                >
              </div>
            </div>
          </div>
        </div>
      </div>

      <div class="col-md-6">
        <div class="card">
          <div class="card-header bg-info text-white">
            <h5 class="mb-0">Información de Asistencia</h5>
          </div>
          <div class="card-body">
            <div v-if="employeeInfo" class="employee-info mb-3">
              <div class="d-flex align-items-center mb-2">
                <div class="avatar-me">
                  <img
                    v-if="employeeInfo.foto_facial"
                    :src="employeeInfo.foto_facial"
                    alt="Foto"
                    class="avatar-img-sm"
                  >
                  <div v-else class="avatar-placeholder-sm">
                    {{ employeeInfo.nombres.charAt(0) }}{{ employeeInfo.apellidos.charAt(0) }}
                  </div>
                </div>
                <div class="ms-3">
                  <h6 class="mb-1">{{ employeeInfo.nombres }} {{ employeeInfo.apellidos }}</h6>
                  <small class="text-muted">{{ employeeInfo.cargo }}</small>
                </div>
              </div>

              <div class="border-top pt-3">
                <div class="d-flex justify-content-between">
                  <span>Último registro:</span>
                  <span class="fw-bold">{{ lastAttendance?.fecha_hora || 'N/A' }}</span>
                </div>
              </div>
            </div>

            <div v-else class="text-center py-4">
              <div class="spinner-border text-primary" role="status">
                <span class="visually-hidden">Cargando...</span>
              </div>
              <p class="mt-3">Verificando identidad...</p>
            </div>

            <div class="mt-4">
              <h6>Estado de la Verificación:</h6>
              <div class="alert" :class="verificationAlertClass" v-if="showVerification">
                <div class="d-flex align-items-start">
                  <div class="flex-shrink-0">
                    <i class="bi" :class="verificationIcon" font-size="1.5rem"></i>
                  </div>
                  <div class="ms-3">
                    <div>{{ verificationMessage }}</div>
                    <small v-if="verificationDetails" class="text-muted">{{ verificationDetails }}</small>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <div class="mt-4">
      <h3>Historial de Asistencia Hoy</h3>
      <div class="table-responsive">
        <table class="table table-hover align-middle">
          <thead class="table-light">
            <tr>
              <th>Hora</th>
              <th>Tipo</th>
              <th>Estado</th>
              <th>Observaciones</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="attendance in todayAttendances" :key="attendance.id">
              <td>{{ attendance.fecha_hora }}</td>
              <td>
                <span v-if="attendance.tipo === 'ENTRADA'" class="badge bg-info">{{ attendance.tipo }}</span>
                <span v-else class="badge bg-secondary">{{ attendance.tipo }}</span>
              </td>
              <td>
                <span v-if="attendance.estado === 'EXITO'" class="badge bg-success">{{ attendance.estado }}</span>
                <span v-else class="badge bg-danger">{{ attendance.estado }}</span>
              </td>
              <td>{{ attendance.observaciones || '-' }}</td>
            </tr>
            <tr v-if="!todayAttendances.length">
              <td colspan="4" class="text-center text-muted">No hay registros de asistencia hoy</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted, onUnmounted } from 'vue'

export default {
  setup() {
    const isCameraActive = ref(false)
    const capturedImage = ref(null)
    const employeeInfo = ref(null)
    const lastAttendance = ref(null)
    const todayAttendances = ref([])

    const verificationState = ref({
      show: false,
      message: '',
      details: '',
      type: 'info' // info, success, error, warning
    })

    let videoStream = null

    // Simular carga de datos del empleado (en producción vendría de la sesión/auth)
    const loadEmployeeData = async () => {
      try {
        // En una app real, esto vendría del contexto de autenticación
        // Por ahora, usamos datos simulados
        employeeInfo.value = {
          id: 1,
          nombres: 'Juan Pablo',
          apellidos: 'García López',
          cedula: '1234567890',
          cargo: 'Asistente Administrativo',
          email: 'juan.garcia@empresa.com',
          foto_facial: null // Se llenaría con los datos faciales reales
        }

        // Simular último registro
        lastAttendance.value = {
          fecha_hora: new Date().toLocaleString('es-CO', {
            hour: '2-digit',
            minute: '2-digit'
          })
        }

        // Simular asistencias de hoy
        todayAttendances.value = [
          {
            id: 1,
            fecha_hora: '08:05 AM',
            tipo: 'ENTRADA',
            estado: 'EXITO',
            observaciones: 'Registro exitoso'
          }
        ]
      } catch (error) {
        console.error('Error loading employee data:', error)
      }
    }

    const startCamera = async () => {
      try {
        const stream = await navigator.mediaDevices.getUserMedia({ video: { width: 640, height: 480 } })
        videoStream = stream
        const videoElement = document.getElementById('videoElement')
        videoElement.srcObject = stream
        isCameraActive.value = true

        // Reiniciar estado de verificación
        verificationState.value = { show: false, message: '', details: '', type: 'info' }
        capturedImage.value = null
      } catch (err) {
        console.error('Error accessing camera:', err)
        alert('No se pudo acceder a la cámara. Asegúrese de que esté conectada y tenga permisos.')
      }
    }

    const stopCamera = () => {
      if (videoStream) {
        videoStream.getTracks().forEach(track => track.stop())
        videoStream = null
      }
      isCameraActive.value = false
      const videoElement = document.getElementById('videoElement')
      videoElement.srcObject = null
    }

    const captureAndVerify = async () => {
      if (!videoStream) return

      try {
        const videoElement = document.getElementById('videoElement')
        const canvas = document.createElement('canvas')
        canvas.width = videoElement.videoWidth
        canvas.height = videoElement.videoHeight
        const ctx = canvas.getContext('2d')
        ctx.drawImage(videoElement, 0, 0, canvas.width, canvas.height)
        const imageData = canvas.toDataURL('image/jpeg')

        capturedImage.value = imageData

        // Simular proceso de verificación facial y GPS
        await simulateVerification()

        // Detener cámara después de la captura
        stopCamera()
      } catch (error) {
        console.error('Error during capture:', error)
        alert('Error al procesar la imagen')
      }
    }

    const simulateVerification = async () => {
      // Mostrar estado de procesamiento
      verificationState.value = {
        show: true,
        message: 'Verificando identidad...',
        details: 'Analizando características faciales y ubicación GPS',
        type: 'info'
      }

      // Simular delay de procesamiento
      await new Promise(resolve => setTimeout(resolve, 2000))

      // Simular resultados (en producción, esto vendría del backend con face-api.js y validación GPS)
      const isFaceMatch = Math.random() > 0.2 // 80% de éxito simulado
      const isGpsValid = Math.random() > 0.1  // 90% de GPS válido simulado

      if (isFaceMatch && isGpsValid) {
        verificationState.value = {
          show: true,
          message: 'Asistencia registrada exitosamente',
          details: 'Facial: 92% coincidencia | GPS: Dentro del rango permitido',
          type: 'success'
        }

        // Actualizar historial
        const newAttendance = {
          id: Date.now(),
          fecha_hora: new Date().toLocaleTimeString('es-CO', {
            hour: '2-digit',
            minute: '2-digit'
          }),
          tipo: lastAttendance.value && lastAttendance.value.tipo === 'ENTRADA' ? 'SALIDA' : 'ENTRADA',
          estado: 'EXITO',
          observaciones: 'Registro biométrico exitoso'
        }

        todayAttendances.value.unshift(newAttendance)
        lastAttendance.value = newAttendance
      } else if (!isFaceMatch) {
        verificationState.value = {
          show: true,
          message: 'Verificación facial fallida',
          details: 'La coincidencia facial es inferior al 80% requerido',
          type: 'error'
        }
      } else {
        verificationState.value = {
          show: true,
          message: 'Ubicación fuera de rango',
          details: 'El GPS indica que está fuera del rango permitido (100m)',
          type: 'warning'
        }
      }
    }

    // Getters para el template
    const verificationAlertClass = () => {
      switch (verificationState.value.type) {
        case 'success': return 'alert-success'
        case 'error': return 'alert-danger'
        case 'warning': return 'alert-warning'
        default: return 'alert-info'
      }
    }

    const verificationIcon = () => {
      switch (verificationState.value.type) {
        case 'success': return 'bi-check-circle-fill'
        case 'error': return 'bi-exclamation-triangle-fill'
        case 'warning': return 'bi-exclamation-triangle'
        default: return 'bi-info-circle-fill'
      }
    }

    // Lifecycle hooks
    onMounted(() => {
      loadEmployeeData()
    })

    onUnmounted(() => {
      stopCamera()
    })

    return {
      isCameraActive,
      capturedImage,
      employeeInfo,
      lastAttendance,
      todayAttendances,
      verificationState,
      startCamera,
      stopCamera,
      captureAndVerify,
      verificationAlertClass,
      verificationIcon,
      // Computed properties as methods for template
      get verificationMessage() {
        return verificationState.value.message
      },
      get verificationDetails() {
        return verificationState.value.details
      },
      get showVerification() {
        return verificationState.value.show
      }
    }
  }
}
</script>

<style scoped>
.container {
  max-width: 1200px;
}

.card {
  border: none;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
}

.card-header {
  border-radius: 12px 12px 0 0 !important;
}

.avatar-me {
  width: 50px;
  height: 50px;
  flex-shrink: 0;
}

.avatar-img-sm {
  width: 100%;
  height: 100%;
  object-fit: cover;
  border-radius: 50%;
  border: 2px solid var(--color-primary-50);
}

.avatar-placeholder-sm {
  width: 100%;
  height: 100%;
  background: var(--color-primary-200);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: bold;
  font-size: 1rem;
  color: var(--color-primary-700);
  border: 2px solid var(--color-primary-50);
}

.employee-info {
  border-bottom: 1px solid var(--color-neutral-divider);
}

#videoContainer {
  border-radius: 8px;
  overflow: hidden;
  border: 2px solid var(--color-neutral-border);
}

.btn {
  border-radius: 8px;
  font-weight: 500;
  transition: all 0.2s ease;
}

.btn-success {
  background: var(--color-secondary-700);
  border-color: var(--color-secondary-700);
}

.btn-success:hover {
  background: var(--color-secondary-900);
  border-color: var(--color-secondary-900);
  transform: translateY(-2px);
}

.btn-primary {
  background: var(--color-primary-700);
  border-color: var(--color-primary-700);
}

.btn-primary:hover {
  background: var(--color-primary-900);
  border-color: var(--color-primary-900);
  transform: translateY(-2px);
}

.btn-outline-secondary {
  color: var(--color-neutral-text-secondary);
  border-color: var(--color-neutral-border);
}

.btn-outline-secondary:hover {
  background: var(--color-neutral-border);
  color: white;
}

.table {
  margin-bottom: 0;
}

.table th {
  background-color: var(--color-primary-50);
  font-weight: 600;
  color: var(--color-neutral-text-primary);
  border-color: var(--color-neutral-divider);
}

.table td {
  vertical-align: middle;
  border-color: var(--color-neutral-divider);
}

.badge {
  font-weight: 500;
  padding: 0.35em 0.65em;
  font-size: 0.85rem;
}

.alert {
  border: none;
  border-radius: 8px;
  padding: 1rem;
  margin: 1rem 0;
}

/* Responsive design */
@media (max-width: 768px) {
  .row {
    flex-direction: column;
  }

  .col-md-6 {
    width: 100%;
    margin-bottom: 1.5rem;
  }
}
</style>