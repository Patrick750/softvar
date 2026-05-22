<template>
  <div class="auth-page">
    <div class="auth-container">
      <!-- Branding -->
      <div class="auth-brand">
        <div class="auth-logo">
          <i class="bi bi-building"></i>
        </div>
        <h1 class="auth-title">SoftVar</h1>
        <p class="auth-subtitle">Sistema de Asistencia y Nómina</p>
      </div>

      <!-- Login Card -->
      <div class="auth-card">
        <div class="auth-card-header">
          <h3>Iniciar Sesión</h3>
          <p>Ingrese sus credenciales para acceder al sistema</p>
        </div>

        <div class="auth-card-body">
          <!-- Error message -->
          <div v-if="error" class="auth-error">
            <i class="bi bi-exclamation-circle"></i>
            {{ error }}
          </div>

          <form @submit.prevent="onSubmit" novalidate>
            <div class="form-group">
              <label class="form-label-modern" for="email">Correo Electrónico</label>
              <div class="input-with-icon">
                <i class="bi bi-envelope"></i>
                <input
                  type="email"
                  class="form-control-modern"
                  id="email"
                  v-model="form.email"
                  placeholder="admin@empresa.com"
                  required
                  autofocus
                >
              </div>
            </div>

            <div class="form-group">
              <label class="form-label-modern" for="password">Contraseña</label>
              <div class="input-with-icon">
                <i class="bi bi-lock"></i>
                <input
                  :type="showPassword ? 'text' : 'password'"
                  class="form-control-modern"
                  id="password"
                  v-model="form.password"
                  placeholder="••••••••"
                  required
                >
                <button type="button" class="password-toggle" @click="showPassword = !showPassword">
                  <i :class="showPassword ? 'bi bi-eye-slash' : 'bi bi-eye'"></i>
                </button>
              </div>
            </div>

            <div class="form-options">
              <label class="checkbox-custom">
                <input type="checkbox" v-model="remember">
                <span class="checkmark"></span>
                Recordarme
              </label>
            </div>

            <button type="submit" class="auth-btn" :disabled="loading">
              <span v-if="loading" class="spinner-custom"></span>
              <span v-else>Ingresar al Sistema</span>
            </button>
          </form>
        </div>

        <div class="auth-card-footer">
          <router-link to="/reset-password" class="auth-link">
            ¿Olvidó su contraseña?
          </router-link>
        </div>
      </div>

      <p class="auth-footer-text">
        &copy; 2026 SoftVar — Control de Asistencia y Nómina v1.0
      </p>
    </div>
  </div>
</template>

<script>
import { ref } from 'vue'
import { useRouter, useRoute } from 'vue-router'

export default {
  setup() {
    const router = useRouter()
    const route = useRoute()
    const form = ref({ email: '', password: '' })
    const loading = ref(false)
    const error = ref('')
    const remember = ref(false)
    const showPassword = ref(false)

    function getCookie(name) {
      const value = `; ${document.cookie}`
      const parts = value.split(`; ${name}=`)
      if (parts.length === 2) return parts.pop().split(';').shift()
      return null
    }

    const onSubmit = async () => {
      error.value = ''
      loading.value = true

      try {
        // Primero obtener el token CSRF haciendo un GET al backend
        await fetch('/api/auth/csrf/', {
          credentials: 'include',
        })

        const csrfToken = getCookie('csrftoken')

        const response = await fetch('/api/auth/login/', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken || '',
          },
          credentials: 'include',
          body: JSON.stringify({
            email: form.value.email,
            password: form.value.password,
          }),
        })

        if (!response.ok) {
          const data = await response.json()
          error.value = data.error || 'Correo electrónico o contraseña incorrectos'
          return
        }

        const data = await response.json()

        // Guardar datos del usuario en localStorage
        localStorage.setItem('token', 'session-' + Date.now())
        localStorage.setItem('userRole', data.rol)
        localStorage.setItem('userName', data.nombre)
        localStorage.setItem('userEmail', data.email)
        localStorage.setItem('userId', data.id)

        const redirectTo = route.query.redirect || '/empleados'
        router.push(redirectTo)
      } catch (err) {
        error.value = 'Error de conexión con el servidor. Verifique que el backend esté corriendo.'
        console.error('Login error:', err)
      } finally {
        loading.value = false
      }
    }

    return { form, loading, error, remember, showPassword, onSubmit }
  }
}
</script>

<style scoped>
.auth-page {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, var(--color-primary-900) 0%, var(--color-primary-700) 100%);
  padding: 2rem 1rem;
  position: relative;
  overflow: hidden;
}

.auth-page::before {
  content: '';
  position: absolute;
  width: 600px;
  height: 600px;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.03);
  top: -200px;
  right: -200px;
}

.auth-page::after {
  content: '';
  position: absolute;
  width: 400px;
  height: 400px;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.03);
  bottom: -100px;
  left: -100px;
}

.auth-container {
  width: 100%;
  max-width: 400px;
  position: relative;
  z-index: 1;
}

/* Brand */
.auth-brand {
  text-align: center;
  margin-bottom: 2rem;
}

.auth-logo {
  width: 64px;
  height: 64px;
  background: rgba(255, 255, 255, 0.15);
  backdrop-filter: blur(10px);
  border-radius: 18px;
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto 1rem;
  font-size: 1.75rem;
  color: #fff;
  border: 1px solid rgba(255, 255, 255, 0.1);
}

.auth-title {
  font-size: 1.75rem;
  font-weight: 700;
  color: #fff;
  margin-bottom: 0.25rem;
  letter-spacing: -0.02em;
}

.auth-subtitle {
  color: rgba(255, 255, 255, 0.7);
  font-size: 0.925rem;
  margin: 0;
}

/* Card */
.auth-card {
  background: #fff;
  border-radius: var(--border-radius-lg);
  box-shadow: var(--shadow-xl);
  overflow: hidden;
}

.auth-card-header {
  padding: 1.75rem 2rem 0 2rem;
}

.auth-card-header h3 {
  margin: 0 0 0.375rem;
  font-size: 1.25rem;
  font-weight: 700;
}

.auth-card-header p {
  margin: 0;
  color: var(--color-text-secondary);
  font-size: 0.875rem;
}

.auth-card-body {
  padding: 1.5rem 2rem;
}

.auth-card-footer {
  padding: 1rem 2rem;
  text-align: center;
  border-top: 1px solid var(--color-divider);
  background: var(--color-bg-page);
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
  color: rgba(255, 255, 255, 0.5);
  font-size: 0.8rem;
  margin-top: 1.5rem;
}

/* Form elements */
.form-group {
  margin-bottom: 1.25rem;
}

.input-with-icon {
  position: relative;
  display: flex;
  align-items: center;
}

.input-with-icon > .bi {
  position: absolute;
  left: 0.875rem;
  color: var(--color-text-secondary);
  font-size: 1rem;
  z-index: 2;
  pointer-events: none;
}

.input-with-icon .form-control-modern {
  padding-left: 2.5rem;
  padding-right: 0.875rem;
  width: 100%;
}

.password-toggle {
  position: absolute;
  right: 0.5rem;
  background: none;
  border: none;
  color: var(--color-text-secondary);
  padding: 0.375rem;
  cursor: pointer;
  font-size: 1rem;
  transition: color var(--transition-fast);
  z-index: 2;
}

.password-toggle:hover {
  color: var(--color-primary-700);
}

.form-options {
  display: flex;
  align-items: center;
  margin-bottom: 1.25rem;
}

.checkbox-custom {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  cursor: pointer;
  font-size: 0.875rem;
  color: var(--color-text-secondary);
}

.checkbox-custom input {
  accent-color: var(--color-primary-700);
}

.auth-btn {
  width: 100%;
  padding: 0.75rem;
  background: var(--color-primary-700);
  color: #fff;
  border: none;
  border-radius: var(--border-radius-sm);
  font-weight: 600;
  font-size: 0.95rem;
  cursor: pointer;
  transition: all var(--transition-base);
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: 46px;
}

.auth-btn:hover:not(:disabled) {
  background: var(--color-primary-900);
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(24, 95, 165, 0.3);
}

.auth-btn:disabled {
  opacity: 0.7;
  cursor: not-allowed;
}

/* Error */
.auth-error {
  background: var(--color-error-bg);
  color: var(--color-error-accent);
  padding: 0.75rem 1rem;
  border-radius: var(--border-radius-sm);
  font-size: 0.875rem;
  margin-bottom: 1rem;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.auth-error i {
  font-size: 1rem;
  flex-shrink: 0;
}

@media (max-width: 480px) {
  .auth-card-body {
    padding: 1.25rem;
  }
  .auth-card-header {
    padding: 1.5rem 1.25rem 0;
  }
  .auth-card-footer {
    padding: 0.875rem 1.25rem;
  }
}
</style>
