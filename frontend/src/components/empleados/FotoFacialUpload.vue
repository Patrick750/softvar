<template>
  <div class="foto-facial-upload">
    <label class="form-label">{{ label }}</label>

    <div v-if="capturedImage" class="image-preview mb-3">
      <img :src="capturedImage" alt="Foto capturada" class="img-thumbnail">
      <button
        type="button"
        class="btn btn-sm btn-outline-danger"
        @click="capturedImage = null"
      >
        Eliminar Foto
      </button>
    </div>

    <div v-else class="mb-3">
      <button
        type="button"
        class="btn btn-outline-primary w-100"
        @click="startCamera"
      >
        <i class="bi bi-camera-video me-2"></i>
        Iniciar Cámara
      </button>
    </div>

    <div v-if="videoStream" class="ratio ratio-16x9 mb-3">
      <video
        id="videoPreview"
        autoplay
        playsinline
        class="w-100 h-100 object-fit-contain"
      ></video>
    </div>

    <div v-if="videoStream" class="d-grid gap-2">
      <button
        type="button"
        class="btn btn-success"
        @click="capturePhoto"
      >
        <i class="bi bi-camera me-2"></i>
        Capturar Foto
      </button>

      <button
        type="button"
        class="btn btn-outline-secondary"
        @click="stopCamera"
      >
        <i class="bi bi-x-circle me-2"></i>
        Detener Cámara
      </button>
    </div>

    <div v-if="error" class="alert alert-danger mt-3">
      {{ error }}
    </div>
  </div>
</template>

<script>
import { ref } from 'vue'

export default {
  props: {
    fotoData: {
      type: [String, Object],
      default: null
    },
    label: {
      type: String,
      default: 'Capturar Foto Facial'
    }
  },
  emits: ['update:fotoData'],
  setup(props, { emit }) {
    const videoStream = ref(null)
    const capturedImage = ref(null)
    const error = ref('')

    const startCamera = async () => {
      try {
        error.value = ''
        const stream = await navigator.mediaDevices.getUserMedia({ video: true })
        videoStream.value = stream
        const video = document.getElementById('videoPreview')
        video.srcObject = stream
      } catch (err) {
        console.error('Error accessing camera:', err)
        error.value = 'No se pudo acceder a la cámara. Asegúrese de que esté conectada y tenga permisos.'
      }
    }

    const capturePhoto = () => {
      if (!videoStream.value) return
      error.value = ''

      const video = document.getElementById('videoPreview')
      const canvas = document.createElement('canvas')
      canvas.width = video.videoWidth
      canvas.height = video.videoHeight
      const ctx = canvas.getContext('2d')
      ctx.drawImage(video, 0, 0, canvas.width, canvas.height)
      const imageData = canvas.toDataURL('image/jpeg')

      // Store as base64 for now - in real implementation, use face-api.js to compute descriptor
      const descriptor = {
        image: imageData,
        timestamp: new Date().toISOString()
      }

      emit('update:fotoData', JSON.stringify(descriptor))
      capturedImage.value = imageData

      // Stop stream after capture
      stopCamera()
    }

    const stopCamera = () => {
      if (videoStream.value) {
        videoStream.value.getTracks().forEach(track => track.stop())
        videoStream.value = null
      }
    }

    // Stop stream when component unmounts
    // onUnmounted(() => {
    //   stopCamera()
    // })

    return {
      videoStream,
      capturedImage,
      error,
      startCamera,
      capturePhoto,
      stopCamera
    }
  }
}
</script>

<style scoped>
.foto-facial-upload {
  max-width: 500px;
}

.image-preview {
  text-align: center;
}

.image-preview img {
  max-width: 100%;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.btn-outline-primary {
  border-color: var(--color-primary-500);
  color: var(--color-primary-500);
}

.btn-outline-primary:hover {
  background-color: var(--color-primary-500);
  color: white;
}

.btn-success {
  background-color: var(--color-secondary-700);
  border-color: var(--color-secondary-700);
}

.btn-success:hover {
  background-color: var(--color-secondary-900);
  border-color: var(--color-secondary-900);
}

.btn-outline-secondary {
  border-color: var(--color-neutral-border);
  color: var(--color-neutral-text-secondary);
}

.btn-outline-secondary:hover {
  background-color: var(--color-neutral-border);
  color: white;
}
</style>