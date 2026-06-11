<template>
  <div class="auth-page">
    <div class="auth-container">
      <div class="auth-brand">
        <div class="auth-logo">
          <i class="bi bi-key"></i>
        </div>
        <h1 class="auth-title">Recuperar Contraseña</h1>
        <p class="auth-subtitle">Ingrese su correo para recibir una nueva contraseña temporal</p>
      </div>

      <div class="auth-card">
        <div class="auth-card-body">
          <template v-if="success">
            <Transition name="fade">
              <div class="text-center py-3">
                <div class="success-icon mb-3">
                  <i class="bi bi-check-lg"></i>
                </div>
                <h4>Correo Enviado</h4>
                <p class="text-muted mt-2">{{ message }}</p>
              </div>
            </Transition>
          </template>

          <template v-else>
            <Transition name="fade">
              <div v-if="errorMsg" class="alert alert-error mb-4">
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><line x1="12" y1="8" x2="12" y2="12"/><line x1="12" y1="16" x2="12.01" y2="16"/></svg>
                {{ errorMsg }}
              </div>
            </Transition>

            <form @submit.prevent="onSubmit" novalidate>
            <p class="auth-desc">Ingrese su correo electrónico registrado y le enviaremos una nueva contraseña temporal.</p>

            <div class="form-group">
              <label class="form-label" for="email">Correo Electrónico</label>
              <div class="input-with-icon">
                <i class="bi bi-envelope input-icon"></i>
                <input
                  type="email"
                  class="form-input"
                  id="email"
                  v-model="form.email"
                  placeholder="mi.correo@empresa.com"
                  required
                  autofocus
                  autocomplete="email"
                >
              </div>
            </div>

            <button type="submit" class="btn btn-primary btn-block btn-lg" :disabled="loading">
              <span v-if="loading" class="spinner spinner-sm"></span>
              <span v-else>Recuperar Contraseña</span>
            </button>
          </form>
          </template>
        </div>

        <div class="auth-card-footer">
          <router-link to="/login" class="auth-link">
            <i class="bi bi-arrow-left me-2"></i>
            Volver al Inicio de Sesión
          </router-link>
        </div>
      </div>

      <p class="auth-footer-text">
        &copy; 2026 SoftVar &mdash; Control de Asistencia y Nómina v1.0
      </p>
    </div>
  </div>
</template>

<script>
import { ref } from 'vue'

export default {
  setup() {
    const form = ref({ email: '' })
    const loading = ref(false)
    const success = ref(false)
    const message = ref('')
    const errorMsg = ref('')

    function getCookie(name) {
      const value = `; ${document.cookie}`
      const parts = value.split(`; ${name}=`)
      if (parts.length === 2) return parts.pop().split(';').shift()
      return null
    }

    const onSubmit = async () => {
      loading.value = true
      errorMsg.value = ''

      try {
        await fetch('/api/auth/csrf/', { credentials: 'include' })
        const csrfToken = getCookie('csrftoken')

        const response = await fetch('/api/auth/recuperar-contrasena/', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken || '',
          },
          credentials: 'include',
          body: JSON.stringify({
            email: form.value.email,
          }),
        })

        const data = await response.json()

        if (!response.ok) {
          errorMsg.value = data.error || 'Error al procesar la solicitud.'
          return
        }

        success.value = true
        message.value = data.message || 'Si el correo existe en nuestro sistema, recibirá un enlace para restablecer su contraseña.'
      } catch (err) {
        errorMsg.value = 'Error de conexión con el servidor. Verifique que el backend esté corriendo.'
        console.error('Reset password error:', err)
      } finally {
        loading.value = false
      }
    }

    return { form, loading, success, message, errorMsg, onSubmit }
  }
}
</script>

<style scoped>
.auth-page {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background:
    linear-gradient(135deg, var(--color-primary-900) 0%, var(--color-primary-700) 50%, var(--color-primary-500) 100%);
  padding: 2rem 1rem;
  position: relative;
  overflow: hidden;
}

.auth-page::before {
  content: '';
  position: absolute;
  inset: 0;
  background-image:
    linear-gradient(rgba(255,255,255,0.03) 1px, transparent 1px),
    linear-gradient(90deg, rgba(255,255,255,0.03) 1px, transparent 1px);
  background-size: 60px 60px;
}

.auth-container {
  width: 100%;
  max-width: 400px;
  position: relative;
  z-index: 1;
}

.auth-brand {
  text-align: center;
  margin-bottom: 2rem;
  animation: slide-in-up 0.5s ease both;
}

.auth-logo {
  width: 68px;
  height: 68px;
  background: rgba(255, 255, 255, 0.12);
  backdrop-filter: blur(12px);
  -webkit-backdrop-filter: blur(12px);
  border-radius: 20px;
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto 1rem;
  font-size: 1.75rem;
  color: #fff;
  border: 1px solid rgba(255, 255, 255, 0.15);
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
}

.auth-title {
  font-family: var(--font-display);
  font-size: 1.5rem;
  color: #fff;
  margin-bottom: 0.25rem;
}

.auth-subtitle {
  color: rgba(255, 255, 255, 0.65);
  font-size: 0.875rem;
  margin: 0;
}

.auth-card {
  background: var(--color-bg-white);
  border-radius: var(--border-radius-xl);
  box-shadow: 0 25px 80px rgba(0, 0, 0, 0.2);
  overflow: hidden;
  animation: slide-in-up 0.5s ease both;
  animation-delay: 0.1s;
}

.auth-card-body {
  padding: 2rem 2rem 1.5rem;
}

.auth-desc {
  color: var(--color-text-secondary);
  font-size: 0.875rem;
  margin-bottom: 1.5rem;
}

.auth-card-footer {
  padding: 1rem 2rem;
  text-align: center;
  border-top: 1px solid var(--color-divider);
  background: var(--color-bg-subtle);
}

.auth-link {
  color: var(--color-primary-700);
  text-decoration: none;
  font-size: 0.875rem;
  font-weight: 500;
  transition: color var(--transition-fast);
}

.auth-link:hover {
  color: var(--color-primary-900);
  text-decoration: underline;
}

.auth-footer-text {
  text-align: center;
  color: rgba(255, 255, 255, 0.45);
  font-size: 0.75rem;
  margin-top: 1.5rem;
  animation: fade-in 0.5s ease both;
  animation-delay: 0.3s;
}

.success-icon {
  width: 56px;
  height: 56px;
  background: var(--color-success-bg);
  color: var(--color-success-accent);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.5rem;
  margin: 0 auto;
}

@keyframes slide-in-up {
  from { opacity: 0; transform: translateY(20px); }
  to { opacity: 1; transform: translateY(0); }
}

@keyframes fade-in {
  from { opacity: 0; }
  to { opacity: 1; }
}

@media (max-width: 480px) {
  .auth-card-body { padding: 1.5rem; }
  .auth-card-footer { padding: 0.875rem 1.5rem; }
}
</style>
