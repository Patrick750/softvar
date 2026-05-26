/**
 * useGpsWatcher — Composable para seguimiento GPS continuo
 * 
 * Usa navigator.geolocation.watchPosition() para mantener las
 * coordenadas actualizadas en segundo plano. Esto elimina la
 * demora al registrar asistencia porque las coordenadas ya
 * están cacheadas cuando el usuario hace clic en "Verificar".
 * 
 * Al cerrar sesión, se llama a resetWatcher() para detener
 * el seguimiento y limpiar los datos.
 */

import { reactive, toRef, readonly, onUnmounted } from 'vue'

// Estado singleton compartido entre todos los componentes
const state = reactive({
  coords: { lat: null, lon: null, accuracy: null },
  status: 'idle', // 'idle' | 'watching' | 'success' | 'error'
  errorMessage: null,
  watchId: null,
  lastUpdated: null,
  permissionGranted: localStorage.getItem('locationGranted') === 'true',
})

/**
 * Inicia el watchPosition continuo.
 * Se llama automáticamente desde App.vue cuando el usuario
 * está autenticado.
 */
function startWatcher() {
  // No reiniciar si ya está activo
  if (state.watchId !== null) return

  if (!navigator.geolocation) {
    state.status = 'error'
    state.errorMessage = 'Geolocalización no soportada'
    return
  }

  state.status = 'watching'

  try {
    state.watchId = navigator.geolocation.watchPosition(
      (position) => {
        state.coords.lat = position.coords.latitude
        state.coords.lon = position.coords.longitude
        state.coords.accuracy = position.coords.accuracy
        state.status = 'success'
        state.lastUpdated = new Date().toISOString()
        state.permissionGranted = true
        localStorage.setItem('locationGranted', 'true')
      },
      (err) => {
        console.warn('[useGpsWatcher] Error de GPS:', err.message)
        state.status = 'error'
        state.errorMessage = err.message
        // No detenemos el watch — puede recuperarse solo
      },
      {
        enableHighAccuracy: true,
        timeout: 15000,
        maximumAge: 60000, // Acepta posiciones de hasta 1 minuto de antigüedad
      }
    )
  } catch (err) {
    console.error('[useGpsWatcher] Error al iniciar watchPosition:', err)
    state.status = 'error'
    state.errorMessage = err.message
  }
}

/**
 * Detiene el watchPosition y resetea el estado.
 * Se llama al cerrar sesión.
 */
function resetWatcher() {
  if (state.watchId !== null) {
    try {
      navigator.geolocation.clearWatch(state.watchId)
    } catch (err) {
      // Ignorar errores al limpiar
    }
    state.watchId = null
  }
  state.coords.lat = null
  state.coords.lon = null
  state.coords.accuracy = null
  state.status = 'idle'
  state.errorMessage = null
  state.lastUpdated = null
  state.permissionGranted = false
}

/**
 * Obtiene las coordenadas cacheadas.
 * Si no hay coordenadas, intenta obtenerlas con getCurrentPosition.
 * Retorna siempre las últimas coordenadas conocidas (podrían ser null).
 */
function getCurrentCoords() {
  // Si ya tenemos coordenadas cacheadas del watchPosition, devolverlas
  if (state.coords.lat !== null && state.coords.lon !== null) {
    return { lat: state.coords.lat, lon: state.coords.lon }
  }

  // Si no hay watch activo pero hay permiso, iniciarlo
  if (state.watchId === null && state.permissionGranted) {
    startWatcher()
  }

  // Devolver lo que tengamos (podría ser null)
  return { lat: state.coords.lat, lon: state.coords.lon }
}

/**
 * Hook de Vue — inicia el watcher automáticamente
 * y lo limpia al desmontar (componente).
 */
export function useGpsWatcher() {
  // El hook no necesita inicialización — el estado es singleton
  // y persiste independientemente del ciclo de vida del componente.

  return {
    coords: state.coords,
    status: state.status,
    errorMessage: state.errorMessage,
    // Usar toRef para mantener reactividad en provide/inject con primitivos
    status: toRef(state, 'status'),
    lastUpdated: toRef(state, 'lastUpdated'),
    permissionGranted: toRef(state, 'permissionGranted'),
    startWatcher,
    resetWatcher,
    getCurrentCoords,
  }
}

// Exportaciones para uso directo sin hook de Vue
export {
  state as gpsState,
  startWatcher,
  resetWatcher,
  getCurrentCoords,
}
