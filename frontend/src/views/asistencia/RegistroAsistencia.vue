<template>
  <div>
    <div class="page-header">
      <h1 class="display-heading">Registro de Asistencia</h1>
      <p class="text-muted">Verifique su identidad y ubicación para registrar entrada o salida</p>
    </div>

    <!-- Loading Employee State -->
    <div v-if="loadingEmployee" class="text-center py-5">
      <div class="spinner spinner-lg mx-auto"></div>
      <p class="mt-3 text-muted">Cargando información del empleado...</p>
    </div>

    <div v-else class="layout-grid grid-2">
      <!-- Camera Card -->
      <div class="card card-elevated p-0">
        <div class="card-header-primary">
          <h5><i class="bi bi-camera-video me-2"></i>Registro Biométrico</h5>
        </div>
        <div class="card-body">
          <!-- Type selector -->
          <div class="form-group mb-3">
            <label class="form-label">Tipo de Marcación</label>
            <div class="flex-row gap-sm">
              <button
                type="button"
                class="btn flex-1"
                :class="selectedTipo === 'ENTRADA' ? 'btn-primary' : 'btn-outline'"
                @click="selectedTipo = 'ENTRADA'"
              >
                Entrada
              </button>
              <button
                type="button"
                class="btn flex-1"
                :class="selectedTipo === 'SALIDA' ? 'btn-primary' : 'btn-outline'"
                @click="selectedTipo = 'SALIDA'"
              >
                Salida
              </button>
            </div>
          </div>

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

            <!-- Loading overlay -->
            <div v-if="isProcessing || loadingModels" class="camera-loading-overlay">
              <span class="spinner"></span>
              <p class="mt-2 text-white text-sm">
                <template v-if="loadingModels">Cargando modelos IA...</template>
                <template v-else>Procesando marcación...</template>
              </p>
            </div>
          </div>

          <!-- Controls -->
          <div class="flex-row gap-sm">
            <button class="btn btn-success" @click="startCamera" :disabled="isCameraActive || isProcessing">
              <i class="bi bi-camera-video me-2"></i>
              Iniciar Cámara
            </button>
            <button class="btn btn-primary" @click="captureAndVerify" :disabled="!isCameraActive || isProcessing">
              <i class="bi bi-check-circle me-2"></i>
              Verificar Asistencia
            </button>
            <button class="btn btn-outline" @click="stopCamera" :disabled="!isCameraActive || isProcessing">
              <i class="bi bi-x-circle me-2"></i>
              Detener
            </button>
          </div>

          <!-- Captured preview -->
          <div v-if="capturedImage" class="mt-3 text-center">
            <p class="text-sm text-muted mb-1">Última captura:</p>
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
              <span class="text-muted">Último registro del sistema:</span>
              <span class="fw-semibold">{{ lastAttendance ? `${lastAttendance.tipo} - ${formatDateTime(lastAttendance.fecha_hora)}` : 'N/A' }}</span>
            </div>
            
            <!-- GPS coordinates display -->
            <div class="d-flex justify-between mt-2" v-if="currentCoords.lat">
              <span class="text-muted">Mis Coordenadas:</span>
              <span class="fw-mono text-sm">{{ currentCoords.lat.toFixed(5) }}, {{ currentCoords.lon.toFixed(5) }}</span>
            </div>
            <div class="d-flex justify-between mt-2">
              <span class="text-muted">Estado del GPS:</span>
              <span>
                <span v-if="gpsStatus === 'fetching'" class="badge badge-warning"><span class="spinner spinner-xs me-1"></span>Buscando...</span>
                <span v-else-if="gpsStatus === 'success'" class="badge badge-success">Localizado</span>
                <span v-else-if="gpsStatus === 'error'" class="badge badge-error">Error / Inactivo</span>
                <span v-else-if="locationPreviouslyGranted" class="badge badge-info">Permiso concedido</span>
                <span v-else class="badge badge-neutral">Inactivo</span>
              </span>
              <small v-if="locationPreviouslyGranted && gpsStatus === 'idle'" class="text-xs text-muted mt-1">
                <i class="bi bi-check-circle me-1"></i>Ubicación ya aprobada — al iniciar cámara se obtendrán coordenadas
              </small>
            </div>
          </div>

          <!-- Verification status -->
          <div v-if="verificationState.show" class="mt-4">
            <h6 class="fw-semibold mb-2">Resultado de la Verificación:</h6>
            <div class="alert" :class="verificationAlertClass">
              <div class="flex-row items-start gap-md">
                <i :class="'bi ' + verificationIcon" style="font-size: 1.25rem;"></i>
                <div>
                  <div class="fw-semibold">{{ verificationState.message }}</div>
                  <small class="opacity-75" v-if="verificationState.details">{{ verificationState.details }}</small>
                </div>
              </div>
            </div>
          </div>

          <!-- Manual approval request form -->
          <Transition name="fade">
            <div v-if="showManualForm" class="card mt-3 p-3 border-warning">
              <h6 class="fw-semibold text-warning mb-2">
                <i class="bi bi-file-earmark-text me-2"></i>Solicitar Aprobación Manual
              </h6>
              <p class="text-sm text-muted mb-3">
                Si las validaciones automáticas fallaron (por fallas de geolocalización o biometría), puede enviar una justificación para que Recursos Humanos apruebe su marcación manualmente.
              </p>
              <div class="form-group mb-3">
                <label for="justificacion" class="form-label">Justificación / Motivo <span class="required">*</span></label>
                <textarea
                  id="justificacion"
                  class="form-input"
                  rows="3"
                  v-model="manualJustification"
                  placeholder="Escriba aquí la razón detallada de su solicitud..."
                  required
                ></textarea>
              </div>
              <button
                type="button"
                class="btn btn-warning btn-block"
                @click="submitManualRequest"
                :disabled="submittingManual || !manualJustification.trim()"
              >
                <span v-if="submittingManual" class="spinner spinner-sm me-2"></span>
                Enviar Solicitud
              </button>
            </div>
          </Transition>
        </div>
      </div>
    </div>

    <!-- Today's history -->
    <div class="card card-elevated mt-4 p-0" v-if="!loadingEmployee">
      <div class="card-header-accent">
        <h5><i class="bi bi-clock-history me-2"></i>Historial de Asistencia de Hoy</h5>
      </div>
      <div class="card-body">
        <div class="table-container">
          <table class="table table-compact">
            <thead>
              <tr>
                <th>Hora</th>
                <th>Tipo</th>
                <th>Estado</th>
                <th>Detalles/Observaciones</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="(attendance, idx) in todayAttendances" :key="attendance.id" class="data-row" :style="{ '--i': idx }">
                <td>{{ formatDateTime(attendance.fecha_hora) }}</td>
                <td>
                  <span class="badge" :class="attendance.tipo === 'ENTRADA' ? 'badge-solid-primary' : 'badge-neutral'">
                    {{ attendance.tipo }}
                  </span>
                </td>
                <td>
                  <span v-if="attendance.estado === 'EXITO'" class="badge badge-solid-success">Exitosa</span>
                  <span v-else-if="attendance.estado === 'PENDIENTE_APROBACION'" class="badge badge-warning">Pendiente RRHH</span>
                  <span v-else-if="attendance.estado === 'RECHAZADO'" class="badge badge-neutral">Rechazada</span>
                  <span v-else class="badge badge-solid-error">Fallida</span>
                </td>
                <td>{{ attendance.observaciones || attendance.justificacion_manual || '-' }}</td>
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
import { ref, reactive, computed, onMounted, onUnmounted, inject } from 'vue'
import axios from 'axios'
// face-api.js loaded from CDN via index.html

export default {
  setup() {
    const isCameraActive = ref(false)
    const capturedImage = ref(null)
    const employeeInfo = ref(null)
    const lastAttendance = ref(null)
    const todayAttendances = ref([])
    const isProcessing = ref(false)
    const loadingEmployee = ref(true)
    const gpsStatus = ref('idle') // 'idle', 'fetching', 'success', 'error'
    const currentCoords = reactive({ lat: null, lon: null })
    const locationPreviouslyGranted = ref(localStorage.getItem('locationGranted') === 'true')
    
    // Form selections
    const selectedTipo = ref('ENTRADA')
    
    // Face API loading states
    const loadingModels = ref(false)
    const modelsLoaded = ref(false)
    let modelsLoadingPromise = null
    
    // Face detection ready flag
    const faceDetected = ref(false)

    // Manual Request Form
    const showManualForm = ref(false)
    const manualJustification = ref('')
    const submittingManual = ref(false)

    // Verification Result State
    const verificationState = reactive({
      show: false,
      message: '',
      details: '',
      type: 'info'
    })

    const addToast = inject('addToast', () => {})
    let videoStream = null

    // Load employee and history
    const loadData = async () => {
      loadingEmployee.value = true
      let hasError = false

      // 1. Load employee profile
      try {
        const empResponse = await axios.get('/api/empleados/me/')
        employeeInfo.value = empResponse.data
      } catch (err) {
        console.error('Error loading employee profile:', err)
        hasError = true
        if (err.response?.status === 404) {
          addToast('Atención', 'Su usuario no tiene un perfil de empleado asociado. Contacte a RRHH.', 'warning')
        } else {
          addToast('Error', 'No se pudo cargar su perfil. Verifique su conexión.', 'error')
        }
      }

      // 2. Load attendance history (even if profile failed, try history)
      try {
        const histResponse = await axios.get('/api/asistencia/historial/')
        const allLogs = histResponse.data

        const todayStr = new Date().toISOString().split('T')[0]
        todayAttendances.value = allLogs.filter(log => {
          if (!log.fecha_hora) return false
          return log.fecha_hora.split('T')[0] === todayStr
        })

        if (allLogs.length > 0) {
          lastAttendance.value = allLogs[0]
          selectedTipo.value = lastAttendance.value.tipo === 'ENTRADA' ? 'SALIDA' : 'ENTRADA'
        } else {
          selectedTipo.value = 'ENTRADA'
        }
      } catch (err) {
        console.error('Error loading attendance history:', err)
        if (!hasError) {
          addToast('Error', 'No se pudo cargar el historial de asistencia.', 'error')
        }
        hasError = true
      } finally {
        loadingEmployee.value = false
      }
    }

    const loadModels = async () => {
      if (modelsLoaded.value) return
      if (loadingModels.value && modelsLoadingPromise) {
        return modelsLoadingPromise
      }
      loadingModels.value = true
      const promise = (async () => {
        const MODEL_URL = 'https://unpkg.com/@vladmandic/face-api@1.7.15/model/'
        await Promise.all([
          window.faceapi.nets.ssdMobilenetv1.loadFromUri(MODEL_URL),
          window.faceapi.nets.faceLandmark68Net.loadFromUri(MODEL_URL),
          window.faceapi.nets.faceRecognitionNet.loadFromUri(MODEL_URL)
        ])
        modelsLoaded.value = true
      })()
      modelsLoadingPromise = promise
      try {
        await promise
      } catch (err) {
        console.error('Error loading face-api models:', err)
        addToast('Error', `Error al cargar modelos de reconocimiento facial: ${err.message || err}`, 'error')
      } finally {
        loadingModels.value = false
        modelsLoadingPromise = null
      }
    }

    const startCamera = async () => {
      try {
        verificationState.show = false
        showManualForm.value = false
        capturedImage.value = null
        
        // Parallel model loading
        loadModels().catch(() => {})

        const stream = await navigator.mediaDevices.getUserMedia({
          video: { facingMode: 'user', width: { ideal: 640 }, height: { ideal: 480 } }
        })
        videoStream = stream
        isCameraActive.value = true
        
        setTimeout(() => {
          const video = document.getElementById('videoElement')
          if (video) video.srcObject = stream
        }, 100)
      } catch (err) {
        console.error('Error accessing camera:', err)
        addToast('Error', 'No se pudo acceder a la cámara. Verifique permisos.', 'error')
      }
    }

    const stopCamera = () => {
      if (videoStream) {
        videoStream.getTracks().forEach(track => track.stop())
        videoStream = null
      }
      isCameraActive.value = false
      const video = document.getElementById('videoElement')
      if (video) video.srcObject = null
    }

    // Get position via GPS
    const getCoordinates = () => {
      return new Promise((resolve, reject) => {
        gpsStatus.value = 'fetching'
        if (!navigator.geolocation) {
          gpsStatus.value = 'error'
          reject(new Error('Geolocalización no soportada por el navegador.'))
          return
        }
        navigator.geolocation.getCurrentPosition(
          (position) => {
            currentCoords.lat = position.coords.latitude
            currentCoords.lon = position.coords.longitude
            gpsStatus.value = 'success'
            // Guardar en localStorage que el usuario aprobó la ubicación
            localStorage.setItem('locationGranted', 'true')
            resolve(position.coords)
          },
          (err) => {
            console.error('GPS error:', err)
            gpsStatus.value = 'error'
            reject(err)
          },
          { enableHighAccuracy: true, timeout: 8000, maximumAge: 0 }
        )
      })
    }

    const captureAndVerify = async () => {
      if (!isCameraActive.value) return
      const video = document.getElementById('videoElement')
      if (!video) return

      isProcessing.value = true

      Object.assign(verificationState, {
        show: true,
        message: 'Capturando imagen...',
        details: 'Por favor manténgase quieto mirando a la cámara.',
        type: 'info'
      })

      try {        // 1. Ensure face models are loaded
        if (!modelsLoaded.value) {
            await loadModels()
            if (!modelsLoaded.value) {
                // Model loading failed — was already reported via toast
                return
            }
        }

        // 2. Get Coordinates in parallel with face detection
        let coords = null
        try {
          coords = await getCoordinates()
        } catch (gpsErr) {
          console.warn('GPS failed:', gpsErr)
        }

        // 3. Capture a single frame from the video
        const canvas = document.createElement('canvas')
        canvas.width = video.videoWidth || 640
        canvas.height = video.videoHeight || 480
        const ctx = canvas.getContext('2d')
        ctx.drawImage(video, 0, 0, canvas.width, canvas.height)
        const imageDataUrl = canvas.toDataURL('image/jpeg', 0.9)
        capturedImage.value = imageDataUrl

        // Stop camera now
        stopCamera()        // 4. Detect face and extract descriptor (single pass, instant)
        // Note: withFaceLandmarks() is required BEFORE withFaceDescriptor() in @vladmandic/face-api
        const detection = await window.faceapi.detectSingleFace(
          canvas,
          new window.faceapi.SsdMobilenetv1Options({ minConfidence: 0.5 })
        ).withFaceLandmarks().withFaceDescriptor()
        
        if (!detection) {
          Object.assign(verificationState, {
            show: true,
            message: 'Rostro no detectado',
            details: 'No pudimos localizar un rostro en la captura. Intente de nuevo con buena luz y de frente a la cámara.',
            type: 'error'
          })
          showManualForm.value = true
          return
        }

        const descriptor = Array.from(detection.descriptor)

        // 5. Send to API for verification
        const response = await axios.post('/api/asistencia/registrar/', {
          tipo: selectedTipo.value,
          latitud: coords ? coords.latitude : null,
          longitud: coords ? coords.longitude : null,
          descriptor_facial: descriptor
        })

        // Success!
        Object.assign(verificationState, {
          show: true,
          message: 'Asistencia registrada con éxito',
          details: response.data.message || 'Verificaciones biométricas y de ubicación correctas.',
          type: 'success'
        })
        addToast('Éxito', 'Asistencia registrada.', 'success')
        loadData()
      } catch (err) {
        console.error('Verification error:', err)
        const resData = err.response?.data
        
        if (resData) {
          const isValidationError = ['DUPLICADO', 'FALTA_ENTRADA', 'FUERA_DE_HORARIO'].includes(resData.status)
          const detailsMsg = resData.message || `GPS_OK: ${resData.gps_ok ? 'Sí' : 'No'} | Facial_OK: ${resData.face_ok ? 'Sí' : 'No'}`
          
          Object.assign(verificationState, {
            show: true,
            message: isValidationError ? 'Registro no permitido' : 'Verificación automática fallida',
            details: detailsMsg,
            type: isValidationError ? 'error' : 'warning'
          })
          
          if (!isValidationError) {
            showManualForm.value = true
          }
        } else {
          Object.assign(verificationState, {
            show: true,
            message: 'Error de comunicación',
            details: 'Ocurrió un error al enviar los datos al servidor.',
            type: 'error'
          })
          showManualForm.value = true
        }
      } finally {
        isProcessing.value = false
      }
    }

    const submitManualRequest = async () => {
      if (!manualJustification.value.trim()) {
        addToast('Error', 'La justificación es obligatoria.', 'error')
        return
      }

      submittingManual.value = true

      // Intentar obtener coordenadas GPS si el permiso fue concedido previamente pero aún no tenemos coordenadas
      if (locationPreviouslyGranted.value && !currentCoords.lat) {
        try {
          await getCoordinates()
        } catch (gpsErr) {
          console.warn('No se pudieron obtener coordenadas para solicitud manual:', gpsErr)
        }
      }

      try {
        const response = await axios.post('/api/asistencia/registrar/', {
          tipo: selectedTipo.value,
          latitud: currentCoords.lat,
          longitud: currentCoords.lon,
          solicitar_manual: true,
          justificacion: manualJustification.value
        })

        Object.assign(verificationState, {
          show: true,
          message: 'Solicitud manual enviada',
          details: response.data.message || 'Su solicitud está pendiente de revisión por RRHH.',
          type: 'info'
        })
        
        addToast('Solicitud Registrada', 'En espera de aprobación.', 'info')
        showManualForm.value = false
        manualJustification.value = ''
        loadData() // Refresh logs
      } catch (err) {
        console.error('Error submitting manual request:', err)
        const errMsg = err.response?.data?.error || 'No se pudo enviar la solicitud.'
        addToast('Error', errMsg, 'error')
      } finally {
        submittingManual.value = false
      }
    }

    const verificationAlertClass = computed(() => ({
      success: 'alert-success', error: 'alert-error', warning: 'alert-warning', info: 'alert-info'
    }[verificationState.type] || 'alert-info'))

    const verificationIcon = computed(() => ({
      success: 'bi-check-circle-fill', error: 'bi-exclamation-triangle-fill',
      warning: 'bi-exclamation-triangle-fill', info: 'bi-info-circle-fill'
    }[verificationState.type] || 'bi-info-circle-fill'))

    const formatDateTime = (isoString) => {
      if (!isoString) return '-'
      const date = new Date(isoString)
      return date.toLocaleTimeString('es-CO', { hour: '2-digit', minute: '2-digit', second: '2-digit', hour12: true })
    }

    // Precargar coordenadas GPS automáticamente si el permiso ya fue concedido
    const prefetchCoordinates = async () => {
      if (!locationPreviouslyGranted.value) return
      try {
        await getCoordinates()
        console.log('GPS coordenadas precargadas automáticamente (permiso previamente concedido)')
      } catch (err) {
        // Silencioso — no molestar al usuario si falla la precarga
        console.warn('Precarga de GPS no disponible:', err.message)
      }
    }

    onMounted(async () => {
      await loadData()
      // Precarga silenciosa de GPS si el permiso ya fue concedido
      prefetchCoordinates()
    })
    onUnmounted(stopCamera)

    return {
      isCameraActive,
      capturedImage,
      employeeInfo,
      lastAttendance,
      todayAttendances,
      isProcessing,
      loadingEmployee,
      gpsStatus,
      currentCoords,
      locationPreviouslyGranted,
      selectedTipo,
      loadingModels,
      showManualForm,
      manualJustification,
      submittingManual,
      verificationState,
      verificationAlertClass,
      verificationIcon,
      // Face detection ready
      faceDetected,
      // Methods
      startCamera,
      stopCamera,
      captureAndVerify,
      submitManualRequest,
      formatDateTime
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
  border: 1px solid var(--color-divider);
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

.camera-loading-overlay {
  position: absolute;
  inset: 0;
  background: rgba(0, 0, 0, 0.75);
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  z-index: 5;
  color: white;
  text-align: center;
  backdrop-filter: blur(2px);
}

.img-capture {
  max-width: 200px;
  border-radius: var(--border-radius-sm);
  box-shadow: var(--shadow-md);
  border: 2px solid var(--color-divider);
}

.employee-section {
  background: var(--color-bg-subtle);
  border-radius: var(--border-radius-md);
  padding: 1.25rem;
}

.border-warning {
  border: 1px solid var(--color-warning-accent);
}

.required {
  color: var(--color-error-accent);
}

.data-row {
  opacity: 0;
  transform: translateY(8px);
  animation: fadeInRow 0.35s ease forwards;
  animation-delay: calc(var(--i, 0) * 60ms);
  transition: background 0.2s, transform 0.15s;
}

.data-row:hover {
  background: var(--color-primary-50);
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
