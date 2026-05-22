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
        <div class="auth-card-body">
          <h3 class="auth-heading">Iniciar Sesión</h3>
          <p class="auth-desc">Ingrese sus credenciales para acceder al sistema</p>

          <!-- Error message -->
          <Transition name="fade">
            <div v-if="error" class="alert alert-error mb-4">
              <i class="bi bi-exclamation-circle me-2"></i>
              {{ error }}
            </div>
          </Transition>

          <form @submit.prevent="onSubmit" novalidate>
            <div class="form-group">
              <label class="form-label" for="email">Correo Electrónico</label>
              <div class="input-with-icon">
                <i class="bi bi-envelope input-icon"></i>
                <input
                  type="email"
                  class="form-input"
                  id="email"
                  v-model="form.email"
                  placeholder="admin@empresa.com"
                  required
                  autofocus
                  autocomplete="email"
                >
              </div>
            </div>

            <div class="form-group">
              <label class="form-label" for="password">Contraseña</label>
              <div class="input-with-icon">
                <i class="bi bi-lock input-icon"></i>
                <input
                  :type="showPassword ? 'text' : 'password'"
                  class="form-input"
                  id="password"
                  v-model="form.password"
                  placeholder="••••••••"
                  required
                  autocomplete="current-password"
                >
                <button type="button" class="password-toggle" @click="showPassword = !showPassword" tabindex="-1">
                  <i :class="showPassword ? 'bi bi-eye-slash' : 'bi bi-eye'"></i>
                </button>
              </div>
            </div>

            <div class="form-options">
              <label class="checkbox-custom">
                <input type="checkbox" v-model="remember">
                Recordarme
              </label>
            </div>

            <button type="submit" class="btn btn-primary btn-block btn-lg" :disabled="loading">
              <span v-if="loading" class="spinner spinner-sm"></span>
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
        &copy; 2026 SoftVar &mdash; Control de Asistencia y Nómina v1.0
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
        await fetch('/api/auth/csrf/', { credentials: 'include' })
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
  background:
    linear-gradient(135deg, var(--color-primary-900) 0%, var(--color-primary-700) 50%, var(--color-primary-500) 100%);
  padding: 2rem 1rem;
  position: relative;
  overflow: hidden;
}

/* Decorative circles */
.auth-page::before {
  content: '';
  position: absolute;
  width: 500px;
  height: 500px;
  border-radius: 50%;
  background: radial-gradient(circle, rgba(255,255,255,0.06) 0%, transparent 70%);
  top: -200px;
  right: -150px;
}

.auth-page::after {
  content: '';
  position: absolute;
  width: 350px;
  height: 350px;
  border-radius: 50%;
  background: radial-gradient(circle, rgba(255,255,255,0.04) 0%, transparent 70%);
  bottom: -100px;
  left: -80px;
}

/* Grid pattern overlay */
.auth-page::before {
  background-image:
    linear-gradient(rgba(255,255,255,0.03) 1px, transparent 1px),
    linear-gradient(90deg, rgba(255,255,255,0.03) 1px, transparent 1px);
  background-size: 60px 60px;
  width: 100%;
  height: 100%;
  top: 0;
  right: 0;
  border-radius: 0;
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
  font-size: 1.75rem;
  color: #fff;
  margin-bottom: 0.25rem;
  letter-spacing: -0.02em;
}

.auth-subtitle {
  color: rgba(255, 255, 255, 0.65);
  font-size: 0.875rem;
  margin: 0;
}

/* Card */
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

.auth-heading {
  font-size: 1.375rem;
  font-weight: 700;
  margin-bottom: 0.375rem;
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

/* Form elements */
.form-options {
  display: flex;
  align-items: center;
  margin-bottom: 1.25rem;
}

.password-toggle {
  position: absolute;
  right: 0.5rem;
  top: 50%;
  transform: translateY(-50%);
  background: none;
  border: none;
  color: var(--color-text-secondary);
  padding: 0.375rem;
  cursor: pointer;
  font-size: 1.1rem;
  transition: color var(--transition-fast);
  z-index: 2;
}

.password-toggle:hover {
  color: var(--color-primary-700);
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
  .auth-card-body {
    padding: 1.5rem;
  }
  .auth-card-footer {
    padding: 0.875rem 1.5rem;
  }
}
</style>
