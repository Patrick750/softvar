<template>
  <div class="location-picker">
    <!-- Mapa -->
    <div ref="mapContainer" class="map-container"></div>

    <!-- Cabecera del mapa -->
    <div class="map-header">
      <div class="map-header-left">
        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
          <path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"/><circle cx="12" cy="10" r="3"/>
        </svg>
        <span>Seleccione la ubicación de la oficina en el mapa</span>
      </div>
      <div class="map-header-right">
        <button type="button" class="btn btn-sm btn-outline-primary" @click="detectMyLocation" :disabled="detectingLocation">
          <span v-if="detectingLocation" class="spinner spinner-sm"></span>
          <svg v-else width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
            <circle cx="12" cy="12" r="10"/><circle cx="12" cy="12" r="3"/><line x1="2" y1="12" x2="6" y2="12"/><line x1="18" y1="12" x2="22" y2="12"/>
          </svg>
          {{ detectingLocation ? 'Detectando...' : 'Mi ubicación' }}
        </button>
        <button type="button" class="btn btn-sm btn-outline" @click="resetToDefault" title="Restablecer coordenadas por defecto">
          <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
            <polyline points="23 4 23 10 17 10"/><polyline points="1 20 1 14 7 14"/><path d="M3.51 9a9 9 0 0 1 14.85-3.36L23 10M1 14l4.64 4.36A9 9 0 0 0 20.49 15"/>
          </svg>
          Restablecer
        </button>
      </div>
    </div>

    <!-- Info de coordenadas -->
    <div class="map-coords">
      <div class="coord-item">
        <span class="coord-label">Latitud</span>
        <span class="coord-value">{{ lat.toFixed(6) }}</span>
        <span class="coord-copy" @click="copyToClipboard(lat.toFixed(6))" title="Copiar">
          <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="9" y="9" width="13" height="13" rx="2" ry="2"/><path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"/></svg>
        </span>
      </div>
      <div class="coord-divider"></div>
      <div class="coord-item">
        <span class="coord-label">Longitud</span>
        <span class="coord-value">{{ lng.toFixed(6) }}</span>
        <span class="coord-copy" @click="copyToClipboard(lng.toFixed(6))" title="Copiar">
          <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="9" y="9" width="13" height="13" rx="2" ry="2"/><path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"/></svg>
        </span>
      </div>
      <div class="coord-divider"></div>
      <div class="coord-item">
        <span class="coord-label">Radio</span>
        <span class="coord-value">{{ radius }} <small>m</small></span>
      </div>
    </div>

    <!-- Indicador de precisión GPS -->
    <transition name="fade">
      <div v-if="gpsAccuracy !== null" class="map-gps-accuracy">
        <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
          <circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/>
        </svg>
        <span>Precisión GPS: <strong>{{ gpsAccuracy }} m</strong></span>
        <button type="button" class="btn-dismiss-accuracy" @click="gpsAccuracy = null">&times;</button>
      </div>
    </transition>

    <!-- Mensaje de error -->
    <transition name="fade">
      <div v-if="error" class="map-error">
        <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><line x1="12" y1="8" x2="12" y2="12"/><line x1="12" y1="16" x2="12.01" y2="16"/></svg>
        {{ error }}
      </div>
    </transition>
  </div>
</template>

<script>
import { ref, watch, onMounted, onBeforeUnmount } from 'vue'
import L from 'leaflet'

export default {
  props: {
    lat: { type: Number, default: 2.927300 },
    lng: { type: Number, default: -75.281800 },
    radius: { type: Number, default: 100 }
  },
  emits: ['update:lat', 'update:lng', 'update:radius'],
  setup(props, { emit }) {
    const mapContainer = ref(null)
    const detectingLocation = ref(false)
    const error = ref('')
    const gpsAccuracy = ref(null)

    let map = null
    let marker = null
    let circle = null
    let pulseCircle = null
    let gpsCircle = null
    let tileLayer = null

    // Initialize the map
    const initMap = () => {
      if (map) return

      map = L.map(mapContainer.value, {
        center: [props.lat, props.lng],
        zoom: 16,
        zoomControl: true,
        scrollWheelZoom: true,
        attributionControl: false
      })

      // OpenStreetMap tiles
      tileLayer = L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        maxZoom: 19,
        minZoom: 3,
        attribution: '&copy; <a href="https://openstreetmap.org/copyright">OpenStreetMap</a>'
      }).addTo(map)

      // Custom marker icon
      const icon = L.divIcon({
        html: `<div class="map-marker-pin">
          <svg width="28" height="36" viewBox="0 0 28 36" fill="none">
            <path d="M14 0C6.27 0 0 6.27 0 14c0 10.5 14 22 14 22s14-11.5 14-22C28 6.27 21.73 0 14 0z" fill="#185FA5" stroke="#042C53" stroke-width="1.5"/>
            <circle cx="14" cy="14" r="6" fill="white"/>
          </svg>
        </div>`,
        className: 'custom-marker-icon',
        iconSize: [28, 36],
        iconAnchor: [14, 36],
        popupAnchor: [0, -36]
      })

      // Draggable marker
      marker = L.marker([props.lat, props.lng], {
        icon: icon,
        draggable: true
      }).addTo(map)

      // Radius circle
      circle = L.circle([props.lat, props.lng], {
        radius: props.radius,
        color: '#185FA5',
        fillColor: '#185FA5',
        fillOpacity: 0.08,
        weight: 2,
        dashArray: '6, 6',
        opacity: 0.6
      }).addTo(map)

      // Click on map to move marker
      map.on('click', (e) => {
        moveMarker(e.latlng.lat, e.latlng.lng)
      })

      // Drag marker
      marker.on('dragend', () => {
        const pos = marker.getLatLng()
        moveMarker(pos.lat, pos.lng)
      })
    }

    // Move marker and update all visuals
    const moveMarker = (newLat, newLng) => {
      if (marker) marker.setLatLng([newLat, newLng])
      if (circle) circle.setLatLng([newLat, newLng])
      if (map) map.panTo([newLat, newLng], { animate: true, duration: 0.3 })
      
      emit('update:lat', newLat)
      emit('update:lng', newLng)
    }

    // Create pulse animation circle
    const createPulseCircle = (centerLat, centerLng, accuracy) => {
      // Remove previous pulse circles
      if (pulseCircle && map) map.removeLayer(pulseCircle)
      if (gpsCircle && map) map.removeLayer(gpsCircle)

      // GPS accuracy circle (semi-transparent)
      const radius = Math.max(accuracy || 50, 20)
      gpsCircle = L.circle([centerLat, centerLng], {
        radius: radius,
        color: '#0891b2',
        fillColor: '#0891b2',
        fillOpacity: 0.06,
        weight: 1.5,
        opacity: 0.4,
        dashArray: '4, 4',
        className: 'gps-accuracy-circle'
      }).addTo(map)

      // Pulsing animated circle (CSS animation driven)
      pulseCircle = L.circleMarker([centerLat, centerLng], {
        radius: 10,
        color: '#0891b2',
        fillColor: '#0891b2',
        fillOpacity: 0.4,
        weight: 2,
        className: 'gps-pulse-marker'
      }).addTo(map)

      // Auto-remove pulse circles after animation (3 seconds)
      setTimeout(() => {
        if (pulseCircle && map) {
          map.removeLayer(pulseCircle)
          pulseCircle = null
        }
        if (gpsCircle && map) {
          map.removeLayer(gpsCircle)
          gpsCircle = null
        }
      }, 3000)
    }

    // Animated marker drop effect
    const animateMarkerDrop = (targetLat, targetLng) => {
      if (!marker) return

      // Start position (above the target)
      const startLat = targetLat + 0.002
      marker.setLatLng([startLat, targetLng])
      marker.setOpacity(1)

      // Animate falling down
      let frame = 0
      const totalFrames = 20
      const animate = () => {
        frame++
        const progress = frame / totalFrames
        // Ease out bounce effect
        const easeOutBounce = (t) => {
          const n1 = 7.5625
          const d1 = 2.75
          if (t < 1 / d1) return n1 * t * t
          else if (t < 2 / d1) return n1 * (t -= 1.5 / d1) * t + 0.75
          else if (t < 2.5 / d1) return n1 * (t -= 2.25 / d1) * t + 0.9375
          else return n1 * (t -= 2.625 / d1) * t + 0.984375
        }

        const currentLat = startLat + (targetLat - startLat) * easeOutBounce(progress)
        marker.setLatLng([currentLat, targetLng])

        if (frame < totalFrames) {
          requestAnimationFrame(animate)
        }
      }
      requestAnimationFrame(animate)
    }

    // Show "You are here" popup
    const showHerePopup = (centerLat, centerLng) => {
      const popup = L.popup({
        closeButton: true,
        className: 'gps-here-popup',
        offset: [0, -20]
      }).setLatLng([centerLat, centerLng])
        .setContent(`
          <div class="popup-here-content">
            <span class="popup-here-icon">📍</span>
            <span class="popup-here-text">Usted está aquí</span>
          </div>
        `)
        .openOn(map)

      // Auto-close popup after animation
      setTimeout(() => {
        if (map) map.closePopup()
      }, 4000)
    }

    // Detect user's location via browser GPS
    const detectMyLocation = async () => {
      if (!navigator.geolocation) {
        error.value = 'La geolocalización no está disponible en este navegador.'
        return
      }

      detectingLocation.value = true
      error.value = ''
      gpsAccuracy.value = null

      navigator.geolocation.getCurrentPosition(
        (position) => {
          const newLat = position.coords.latitude
          const newLng = position.coords.longitude
          const accuracy = Math.round(position.coords.accuracy)

          // Show accuracy info
          gpsAccuracy.value = accuracy

          // Zoom out first, then zoom in to animate the detection
          if (map) {
            map.setView([newLat, newLng], 14, { animate: true, duration: 0.6 })

            // After initial zoom, create pulse animation and zoom in further
            setTimeout(() => {
              createPulseCircle(newLat, newLng, accuracy)
              animateMarkerDrop(newLat, newLng)
              showHerePopup(newLat, newLng)

              // Final zoom to street level with smooth animation
              map.flyTo([newLat, newLng], 17, {
                animate: true,
                duration: 1.2,
                easeLinearity: 0.25
              })

              // When fly animation completes, set final marker position
              map.once('moveend', () => {
                if (marker && circle) {
                  marker.setLatLng([newLat, newLng])
                  circle.setLatLng([newLat, newLng])
                  emit('update:lat', newLat)
                  emit('update:lng', newLng)
                }
              })
            }, 700)
          }

          detectingLocation.value = false
        },
        (err) => {
          console.error('GPS error:', err)
          if (err.code === 1) {
            error.value = 'Permiso de ubicación denegado. Active la ubicación en su navegador.'
          } else if (err.code === 2) {
            error.value = 'No se pudo determinar la ubicación. Intente de nuevo.'
          } else {
            error.value = 'Error al obtener ubicación. Verifique que el GPS esté activo.'
          }
          detectingLocation.value = false
        },
        { enableHighAccuracy: true, timeout: 10000, maximumAge: 30000 }
      )
    }

    // Reset to default coordinates (Neiva, Colombia)
    const resetToDefault = () => {
      if (map) {
        map.flyTo([2.927300, -75.281800], 16, {
          animate: true,
          duration: 1.0
        })
        map.once('moveend', () => {
          moveMarker(2.927300, -75.281800)
        })
      }
      emit('update:radius', 100)
    }

    // Copy to clipboard
    const copyToClipboard = (text) => {
      navigator.clipboard.writeText(text).catch(() => {})
    }

    // Watch for radius changes from parent
    watch(() => props.radius, (newRadius) => {
      if (circle) circle.setRadius(newRadius)
    })

    // Watch for lat/lng changes from parent (when user types in inputs)
    watch([() => props.lat, () => props.lng], ([newLat, newLng]) => {
      if (marker && (marker.getLatLng().lat !== newLat || marker.getLatLng().lng !== newLng)) {
        moveMarker(newLat, newLng)
      }
    })

    onMounted(() => {
      // Small delay to ensure DOM is ready
      setTimeout(initMap, 100)
    })

    onBeforeUnmount(() => {
      if (map) {
        map.remove()
        map = null
        marker = null
        circle = null
        pulseCircle = null
        gpsCircle = null
        tileLayer = null
      }
    })

    return {
      mapContainer,
      detectingLocation,
      error,
      gpsAccuracy,
      detectMyLocation,
      resetToDefault,
      copyToClipboard
    }
  }
}
</script>

<style scoped>
.location-picker {
  position: relative;
  border: 1px solid var(--color-divider);
  border-radius: var(--border-radius-lg);
  overflow: hidden;
  background: var(--color-bg-white);
}

.map-container {
  width: 100%;
  height: 380px;
  z-index: 1;
}

/* Custom marker override */
:deep(.custom-marker-icon) {
  background: none !important;
  border: none !important;
}

:deep(.custom-marker-icon .map-marker-pin) {
  filter: drop-shadow(0 2px 6px rgba(4, 44, 83, 0.3));
  transition: filter 0.2s;
}

:deep(.custom-marker-icon .map-marker-pin:hover) {
  filter: drop-shadow(0 3px 10px rgba(4, 44, 83, 0.45));
}

/* ===== GPS Pulse Animation ===== */
:deep(.gps-pulse-marker) {
  animation: gps-pulse 1.5s ease-out infinite !important;
}

@keyframes gps-pulse {
  0% {
    r: 6;
    fill-opacity: 0.7;
    stroke-opacity: 0.8;
  }
  50% {
    r: 14;
    fill-opacity: 0.2;
    stroke-opacity: 0.4;
  }
  100% {
    r: 20;
    fill-opacity: 0;
    stroke-opacity: 0;
  }
}

:deep(.gps-accuracy-circle) {
  animation: gps-fade-in 0.5s ease-out;
}

@keyframes gps-fade-in {
  from {
    opacity: 0;
    stroke-dashoffset: 100;
  }
  to {
    opacity: 0.4;
    stroke-dashoffset: 0;
  }
}

/* ===== "You are here" Popup ===== */
:deep(.gps-here-popup .leaflet-popup-content-wrapper) {
  background: white;
  border-radius: 12px;
  box-shadow: 0 8px 32px rgba(0,0,0,0.15);
  border: 2px solid #0891b2;
  padding: 0;
  overflow: hidden;
}

:deep(.gps-here-popup .leaflet-popup-tip) {
  background: white;
  border: 2px solid #0891b2;
  border-top: none;
  border-left: none;
}

:deep(.gps-here-popup .leaflet-popup-content) {
  margin: 0;
  padding: 8px 14px 8px 12px;
  min-width: 140px;
}

.popup-here-content {
  display: flex;
  align-items: center;
  gap: 8px;
}

.popup-here-icon {
  font-size: 1.2rem;
  animation: popup-bounce 1s ease infinite;
}

@keyframes popup-bounce {
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(-3px); }
}

.popup-here-text {
  font-weight: 600;
  font-size: 0.85rem;
  color: #0f172a;
  white-space: nowrap;
}

/* ===== Map Header ===== */
.map-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 0.75rem;
  padding: 0.65rem 1rem;
  border-bottom: 1px solid var(--color-divider);
  background: var(--color-bg-subtle);
  flex-wrap: wrap;
}

.map-header-left {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.82rem;
  color: var(--color-text-secondary);
  font-weight: 500;
}

.map-header-left svg {
  color: var(--color-primary-500);
  flex-shrink: 0;
}

.map-header-right {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

/* ===== Coordinates Bar ===== */
.map-coords {
  display: flex;
  align-items: center;
  gap: 0;
  padding: 0.5rem 1rem;
  border-top: 1px solid var(--color-divider);
  background: var(--color-bg-white);
}

.coord-item {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0 0.75rem;
  flex: 1;
  min-width: 0;
}

.coord-label {
  font-size: 0.65rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.04em;
  color: var(--color-text-secondary);
  white-space: nowrap;
}

.coord-value {
  font-family: var(--font-mono);
  font-size: 0.8rem;
  font-weight: 600;
  color: var(--color-text-primary);
}

.coord-value small {
  font-weight: 400;
  color: var(--color-text-secondary);
}

.coord-copy {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 20px;
  height: 20px;
  border-radius: 4px;
  cursor: pointer;
  color: var(--color-text-secondary);
  opacity: 0.4;
  transition: all 0.15s;
  flex-shrink: 0;
}

.coord-copy:hover {
  opacity: 1;
  background: var(--color-primary-50);
  color: var(--color-primary-700);
}

.coord-divider {
  width: 1px;
  height: 24px;
  background: var(--color-divider);
  flex-shrink: 0;
}

/* ===== GPS Accuracy Banner ===== */
.map-gps-accuracy {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.55rem 1rem;
  background: #ecfeff;
  color: #0e7490;
  font-size: 0.78rem;
  font-weight: 500;
  border-top: 1px solid #a5f3fc;
  animation: accuracy-slide-in 0.3s ease-out;
}

@keyframes accuracy-slide-in {
  from {
    opacity: 0;
    transform: translateY(-6px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.map-gps-accuracy svg {
  flex-shrink: 0;
  animation: accuracy-pulse 2s ease-in-out infinite;
}

@keyframes accuracy-pulse {
  0%, 100% { opacity: 0.6; }
  50% { opacity: 1; }
}

.map-gps-accuracy strong {
  color: #155e75;
}

.btn-dismiss-accuracy {
  margin-left: auto;
  background: none;
  border: none;
  font-size: 1rem;
  line-height: 1;
  cursor: pointer;
  color: #5f9ea0;
  padding: 0 4px;
  border-radius: 4px;
  transition: all 0.15s;
}

.btn-dismiss-accuracy:hover {
  background: rgba(0,0,0,0.05);
  color: #0e7490;
}

/* ===== Error message ===== */
.map-error {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.6rem 1rem;
  background: var(--color-error-bg);
  color: var(--color-error-accent);
  font-size: 0.8rem;
  font-weight: 500;
  border-top: 1px solid var(--color-error-bg);
}

/* ===== Buttons ===== */
.btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 0.4rem;
  padding: 0.4rem 0.85rem;
  border: 1.5px solid transparent;
  border-radius: 6px;
  font-family: inherit;
  font-weight: 500;
  font-size: 0.78rem;
  cursor: pointer;
  transition: all 0.15s;
  white-space: nowrap;
}

.btn:disabled {
  opacity: 0.55;
  cursor: not-allowed;
}

.btn-sm { padding: 0.3rem 0.7rem; font-size: 0.75rem; }

.btn-outline-primary {
  background: transparent;
  border-color: var(--color-primary-500);
  color: var(--color-primary-700);
}
.btn-outline-primary:hover:not(:disabled) {
  background: var(--color-primary-700);
  color: #fff;
}

.btn-outline {
  background: transparent;
  border-color: var(--color-border);
  color: var(--color-text-secondary);
}
.btn-outline:hover:not(:disabled) {
  border-color: var(--color-primary-500);
  color: var(--color-primary-700);
  background: var(--color-primary-50);
}

/* ===== Spinner ===== */
.spinner {
  width: 14px;
  height: 14px;
  border: 2px solid rgba(0,0,0,0.1);
  border-top-color: currentColor;
  border-radius: 50%;
  animation: spin 0.6s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

/* ===== Fade transition ===== */
:deep(.fade-enter-active), :deep(.fade-leave-active) {
  transition: opacity 0.25s;
}
:deep(.fade-enter-from), :deep(.fade-leave-to) {
  opacity: 0;
}

/* ===== Responsive ===== */
@media (max-width: 640px) {
  .map-container { height: 280px; }
  .map-header { flex-direction: column; align-items: flex-start; }
  .map-coords { flex-wrap: wrap; gap: 0.25rem; }
  .coord-item { padding: 0.25rem 0.5rem; }
  .coord-divider { display: none; }
}
</style>
