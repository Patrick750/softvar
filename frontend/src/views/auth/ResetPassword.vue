<template>
  <div class="auth-page">
    <div class="auth-container">
      <div class="auth-brand">
        <div class="auth-logo">
          <i class="bi bi-key"></i>
        </div>
        <h1 class="auth-title">Restablecer Contraseña</h1>
        <p class="auth-subtitle">Ingrese su correo para recibir un enlace</p>
      </div>

      <div class="auth-card">
        <div class="auth-card-body">
          <!-- Success -->
          <div v-if="success" class="auth-success">
            <div class="success-icon">
              <i class="bi bi-check-lg"></i>
            </div>
            <h4>Correo Enviado</h4>
            <p>{{ message }}</p>
          </div>

          <!-- Form -->
          <form v-else @submit.prevent="onSubmit" novalidate>
            <div class="form-group">
              <label class="form-label-modern" for="email">Correo Electrónico</label>
              <div class="input-with-icon">
                <i class="bi bi-envelope"></i>
                <input
                  type="email"
                  class="form-control-modern"
                  id="email"
                  v-model="form.email"
                  placeholder="mi.correo@empresa.com"
                  required
                  autofocus
                >
              </div>
            </div>

            <button type="submit" class="auth-btn" :disabled="loading">
              <span v-if="loading" class="spinner-custom"></span>
              <span v-else>Enviar Enlace de Recuperación</span>
            </button>
          </form>
        </div>

        <div class="auth-card-footer">
          <router-link to="/login" class="auth-link">
            <i class="bi bi-arrow-left me-1"></i>
            Volver al Inicio de Sesión
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

export default {
  setup() {
    const form = ref({ email: '' })
    const loading = ref(false)
    const success = ref(false)
    const message = ref('')

    const onSubmit = async () => {
      loading.value = true
      try {
        await new Promise(resolve => setTimeout(resolve, 1500))
        success.value = true
        message.value = 'Si el correo existe en nuestro sistema, recibirá un enlace para restablecer su contraseña.'
      } catch (err) {
        message.value = 'Error al procesar la solicitud.'
      } finally {
        loading.value = false
      }
    }

    return { form, loading, success, message, onSubmit }
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
  width: 500px;
  height: 500px;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.03);
  top: -150px;
  right: -150px;
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
  font-size: 1.5rem;
  font-weight: 700;
  color: #fff;
  margin-bottom: 0.25rem;
}

.auth-subtitle {
  color: rgba(255, 255, 255, 0.7);
  font-size: 0.9rem;
  margin: 0;
}

.auth-card {
  background: #fff;
  border-radius: var(--border-radius-lg);
  box-shadow: var(--shadow-xl);
  overflow: hidden;
}

.auth-card-body {
  padding: 2rem;
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

.form-group {
  margin-bottom: 1.5rem;
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
}

.input-with-icon .form-control-modern {
  padding-left: 2.5rem;
  width: 100%;
}

.auth-btn {
  width: 100%;
  padding: 0.75rem;
  background: var(--color-primary-700);
  color: #fff;
  border: none;
  border-radius: var(--border-radius-sm);
  font-weight: 600;
  cursor: pointer;
  transition: all var(--transition-base);
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: 46px;
  font-size: 0.95rem;
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

/* Success state */
.auth-success {
  text-align: center;
  padding: 1rem 0;
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
  margin: 0 auto 1rem;
}

.auth-success h4 {
  margin-bottom: 0.5rem;
}

.auth-success p {
  color: var(--color-text-secondary);
  font-size: 0.9rem;
  margin: 0;
  line-height: 1.5;
}
</style>
