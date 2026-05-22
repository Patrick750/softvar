<template>
  <div class="foto-upload">
    <label class="upload-label">{{ label }}</label>

    <!-- Captured image preview -->
    <div v-if="capturedImage" class="preview-container">
      <div class="preview-frame">
        <img :src="capturedImage" alt="Foto capturada" class="preview-img">
        <div class="preview-overlay">
          <span class="preview-badge">Capturada</span>
        </div>
      </div>
      <button type="button" class="btn btn-outline-danger btn-sm" @click="removePhoto">
        <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/></svg>
        Eliminar foto
      </button>
    </div>

    <!-- Camera launch -->
    <div v-else-if="!videoStream" class="camera-trigger" @click="startCamera">
      <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
        <path d="M23 19a2 2 0 0 1-2 2H3a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h4l2-3h6l2 3h4a2 2 0 0 1 2 2z"/>
        <circle cx="12" cy="13" r="4"/>
      </svg>
      <span>Iniciar Cámara</span>
      <small>Capturar foto facial para biometría</small>
    </div>

    <!-- Live video -->
    <div v-if="videoStream" class="video-section">
      <div class="video-wrapper">
        <video id="videoPreview" autoplay playsinline class="video-preview"></video>
        <div class="video-scan"></div>
        
        <!-- Loading overlays -->
        <div v-if="loadingModels || loadingDetection" class="loading-overlay">
          <span class="spinner"></span>
          <span class="loading-text">{{ loadingModels ? 'Cargando IA...' : 'Analizando Rostro...' }}</span>
        </div>
      </div>
      <div class="video-actions">
        <button type="button" class="btn btn-primary btn-block" @click="capturePhoto" :disabled="loadingModels || loadingDetection">
          <svg v-if="!loadingModels && !loadingDetection" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" style="margin-right: 4px;"><path d="M23 19a2 2 0 0 1-2 2H3a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h4l2-3h6l2 3h4a2 2 0 0 1 2 2z"/><circle cx="12" cy="13" r="4"/></svg>
          <span v-if="loadingModels || loadingDetection">Procesando...</span>
          <span v-else>Capturar Foto</span>
        </button>
        <button type="button" class="btn btn-ghost" @click="stopCamera" :disabled="loadingDetection">
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/></svg>
          Cancelar
        </button>
      </div>
    </div>

    <transition name="fade">
      <div v-if="error" class="error-msg">
        <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><line x1="15" y1="9" x2="9" y2="15"/><line x1="9" y1="9" x2="15" y2="15"/></svg>
        {{ error }}
      </div>
    </transition>
  </div>
</template>

<script>
import { ref, onUnmounted, watch } from 'vue'

export default {
  props: {
    fotoData: { type: [String, Object], default: null },
    label: { type: String, default: 'Capturar Foto Facial' }
  },
  emits: ['update:fotoData'],
  setup(props, { emit }) {
    const videoStream = ref(null)
    const capturedImage = ref(null)
    const error = ref('')
    const loadingModels = ref(false)
    const modelsLoaded = ref(false)
    const loadingDetection = ref(false)

    // Watch for props.fotoData to initialize preview
    watch(() => props.fotoData, (val) => {
      if (val) {
        try {
          const parsed = typeof val === 'string' ? JSON.parse(val) : val
          capturedImage.value = parsed.image || val
        } catch (e) {
          capturedImage.value = val
        }
      } else {
        capturedImage.value = null
      }
    }, { immediate: true })

    const loadModels = async () => {
      if (modelsLoaded.value) return
      if (loadingModels.value) return
      loadingModels.value = true
      error.value = ''
      try {
        const MODEL_URL = 'https://cdn.jsdelivr.net/npm/@vladmandic/face-api/model/'
        // Load required models
        await Promise.all([
          window.faceapi.nets.ssdMobilenetv1.loadFromUri(MODEL_URL),
          window.faceapi.nets.faceLandmark68Net.loadFromUri(MODEL_URL),
          window.faceapi.nets.faceRecognitionNet.loadFromUri(MODEL_URL)
        ])
        modelsLoaded.value = true
      } catch (err) {
        console.error('Error loading face-api models:', err)
        error.value = 'No se pudieron cargar los modelos de reconocimiento facial desde la CDN.'
        throw err
      } finally {
        loadingModels.value = false
      }
    }

    const startCamera = async () => {
      try {
        error.value = ''
        // Pre-load models in parallel so they are ready
        loadModels().catch(() => {})
        
        const stream = await navigator.mediaDevices.getUserMedia({
          video: { facingMode: 'user', width: { ideal: 640 }, height: { ideal: 480 } }
        })
        videoStream.value = stream
        // Wait a tick for the video element to be available
        setTimeout(() => {
          const video = document.getElementById('videoPreview')
          if (video) video.srcObject = stream
        }, 100)
      } catch (err) {
        console.error('Camera error:', err)
        error.value = 'No se pudo acceder a la cámara. Verifique los permisos del navegador.'
      }
    }

    const capturePhoto = async () => {
      if (!videoStream.value) return
      error.value = ''
      const video = document.getElementById('videoPreview')
      if (!video) return

      const canvas = document.createElement('canvas')
      canvas.width = video.videoWidth || 640
      canvas.height = video.videoHeight || 480
      const ctx = canvas.getContext('2d')
      ctx.drawImage(video, 0, 0, canvas.width, canvas.height)
      
      loadingDetection.value = true
      try {
        // Guarantee models are loaded
        await loadModels()
        
        // Detect face on the canvas
        const detection = await window.faceapi.detectSingleFace(
          canvas,
          new window.faceapi.SsdMobilenetv1Options({ minConfidence: 0.5 })
        ).withFaceLandmarks().withFaceDescriptor()
        
        if (!detection) {
          error.value = 'No se detectó ningún rostro en la imagen. Por favor, asegúrese de estar bien iluminado y mirar directamente a la cámara.'
          return
        }
        
        const imageData = canvas.toDataURL('image/jpeg', 0.9)
        const descriptorJson = JSON.stringify({
          image: imageData,
          descriptor: Array.from(detection.descriptor)
        })
        
        emit('update:fotoData', descriptorJson)
        capturedImage.value = imageData
        stopCamera()
      } catch (err) {
        console.error('Face processing error:', err)
        error.value = 'Error al procesar la biometría facial. Por favor intente de nuevo.'
      } finally {
        loadingDetection.value = false
      }
    }

    const stopCamera = () => {
      if (videoStream.value) {
        videoStream.value.getTracks().forEach(track => track.stop())
        videoStream.value = null
      }
    }

    const removePhoto = () => {
      capturedImage.value = null
      emit('update:fotoData', null)
    }

    onUnmounted(() => {
      stopCamera()
    })

    return {
      videoStream,
      capturedImage,
      error,
      loadingModels,
      loadingDetection,
      startCamera,
      capturePhoto,
      stopCamera,
      removePhoto
    }
  }
}
</script>

<style scoped>
.foto-upload {
  max-width: 400px;
}

.upload-label {
  display: block;
  font-size: 0.75rem;
  font-weight: 600;
  color: var(--color-neutral-text-secondary);
  text-transform: uppercase;
  letter-spacing: 0.03em;
  margin-bottom: 0.6rem;
}

/* Camera trigger */
.camera-trigger {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.5rem;
  padding: 2rem 1.5rem;
  border: 2px dashed var(--color-neutral-border);
  border-radius: 12px;
  cursor: pointer;
  transition: all 0.2s;
  color: var(--color-neutral-text-secondary);
  background: var(--color-neutral-bg-page);
}

.camera-trigger:hover {
  border-color: var(--color-primary-500);
  color: var(--color-primary-700);
  background: var(--color-primary-50);
}

.camera-trigger span {
  font-weight: 600;
  font-size: 0.9rem;
}

.camera-trigger small {
  font-size: 0.75rem;
  opacity: 0.7;
}

/* Preview */
.preview-container {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
  align-items: center;
}

.preview-frame {
  position: relative;
  width: 100%;
  border-radius: 12px;
  overflow: hidden;
  border: 2px solid var(--color-secondary-500);
  box-shadow: 0 4px 16px rgba(99, 153, 34, 0.2);
}

.preview-img {
  display: block;
  width: 100%;
  height: auto;
}

.preview-overlay {
  position: absolute;
  top: 0.5rem;
  right: 0.5rem;
}

.preview-badge {
  background: var(--color-secondary-700);
  color: white;
  padding: 0.2rem 0.6rem;
  border-radius: 6px;
  font-size: 0.7rem;
  font-weight: 600;
}

/* Video section */
.video-section {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
  margin-top: 0.5rem;
}

.video-wrapper {
  position: relative;
  border-radius: 12px;
  overflow: hidden;
  background: #000;
  aspect-ratio: 4/3;
}

.video-preview {
  width: 100%;
  height: 100%;
  object-fit: cover;
  display: block;
}

.video-scan {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 3px;
  background: linear-gradient(90deg, transparent, var(--color-primary-500), transparent);
  animation: scanLine 2s ease-in-out infinite;
  opacity: 0.6;
}

@keyframes scanLine {
  0% { top: 0; }
  50% { top: 100%; }
  100% { top: 0; }
}

.video-actions {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

/* Buttons */
.btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 0.4rem;
  padding: 0.55rem 1rem;
  border: none;
  border-radius: 8px;
  font-size: 0.8rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;
  font-family: inherit;
}

.btn-block { width: 100%; }

.btn-primary {
  background: var(--color-primary-700);
  color: white;
}

.btn-primary:hover {
  background: var(--color-primary-900);
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(24, 95, 165, 0.3);
}

.btn-ghost {
  background: transparent;
  color: var(--color-neutral-text-secondary);
}

.btn-ghost:hover {
  background: var(--color-neutral-bg-page);
  color: var(--color-error-accent);
}

.btn-outline-danger {
  background: transparent;
  border: 1px solid var(--color-error-accent);
  color: var(--color-error-accent);
}

.btn-outline-danger:hover {
  background: var(--color-error-bg);
}

.btn-sm { padding: 0.35rem 0.7rem; font-size: 0.75rem; }

/* Error */
.error-msg {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  margin-top: 0.75rem;
  padding: 0.6rem 0.75rem;
  background: var(--color-error-bg);
  color: var(--color-error-accent);
  border-radius: 8px;
  font-size: 0.8rem;
  font-weight: 500;
}

/* Loading Overlay */
.loading-overlay {
  position: absolute;
  inset: 0;
  background: rgba(0, 0, 0, 0.65);
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 0.75rem;
  z-index: 5;
  backdrop-filter: blur(2px);
}

.loading-text {
  color: white;
  font-size: 0.85rem;
  font-weight: 500;
}

/* Transition */
.fade-enter-active, .fade-leave-active { transition: all 0.25s; }
.fade-enter-from, .fade-leave-to { opacity: 0; transform: translateY(-4px); }
</style>
