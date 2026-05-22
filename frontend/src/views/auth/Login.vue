<template>
  <div class="auth-page">
    <!-- ===== LEFT: LOGIN FORM (40%) ===== -->
    <div class="auth-left">
      <div class="auth-container">
        <!-- Branding -->
        <div class="auth-brand">
          <div class="auth-logo">
            <svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
              <path d="M22 12h-4l-3 9L9 3l-3 9H2"/>
            </svg>
          </div>
          <h1 class="auth-title">SoftVar</h1>
          <p class="auth-subtitle">Sistema de Asistencia y Nómina</p>
        </div>

        <!-- Login Card -->
        <div class="auth-card">
          <div class="auth-card-body">
            <h3 class="auth-heading">Iniciar Sesión</h3>
            <p class="auth-desc">Ingrese sus credenciales para acceder al sistema</p>

            <Transition name="fade">
              <div v-if="error" class="alert alert-error mb-4">
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><line x1="12" y1="8" x2="12" y2="12"/><line x1="12" y1="16" x2="12.01" y2="16"/></svg>
                {{ error }}
              </div>
            </Transition>

            <form @submit.prevent="onSubmit" novalidate>
              <div class="form-group">
                <label class="form-label" for="email">Correo Electrónico</label>
                <div class="input-with-icon">
                  <svg class="input-icon" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z"/><polyline points="22,6 12,13 2,6"/></svg>
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
                  <svg class="input-icon" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="11" width="18" height="11" rx="2" ry="2"/><path d="M7 11V7a5 5 0 0 1 10 0v4"/></svg>
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
                    <svg v-if="showPassword" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M17.94 17.94A10.07 10.07 0 0 1 12 20c-7 0-11-8-11-8a18.45 18.45 0 0 1 5.06-5.94M9.9 4.24A9.12 9.12 0 0 1 12 4c7 0 11 8 11 8a18.5 18.5 0 0 1-2.16 3.19m-6.72-1.07a3 3 0 1 1-4.24-4.24"/><line x1="1" y1="1" x2="23" y2="23"/></svg>
                    <svg v-else width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"/><circle cx="12" cy="12" r="3"/></svg>
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

    <!-- ===== RIGHT: ANIMATED BANNER (60%) ===== -->
    <div class="auth-right">
      <!-- Animated background shapes -->
      <div class="banner-bg">
        <div class="floating-shape shape-1"></div>
        <div class="floating-shape shape-2"></div>
        <div class="floating-shape shape-3"></div>
        <div class="floating-shape shape-4"></div>
        <div class="floating-shape shape-5"></div>
        <div class="floating-shape shape-6"></div>

        <!-- Glow orbs -->
        <div class="glow-orb orb-1"></div>
        <div class="glow-orb orb-2"></div>
        <div class="glow-orb orb-3"></div>

        <!-- Floating particles -->
        <div class="particle p1"></div><div class="particle p2"></div>
        <div class="particle p3"></div><div class="particle p4"></div>
        <div class="particle p5"></div><div class="particle p6"></div>
        <div class="particle p7"></div><div class="particle p8"></div>
        <div class="particle p9"></div><div class="particle p10"></div>
        <div class="particle p11"></div><div class="particle p12"></div>
      </div>

      <!-- Banner content -->
      <div class="banner-content">
        <!-- Tagline -->
        <div class="banner-tagline">
          <span class="tagline-line">Control Inteligente</span>
          <span class="tagline-line accent">de Asistencia y Nómina</span>
        </div>

        <!-- Sub-tagline -->
        <p class="banner-sub">La solución integral para la gestión de recursos humanos en tu empresa</p>

        <!-- Feature cards grid -->
        <div class="banner-features">
          <div class="feature-card" style="--i: 0">
            <div class="feature-icon" style="--icon-bg: rgba(59, 109, 17, 0.25)">
              <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="#3B6D11" stroke-width="1.8"><rect x="3" y="3" width="18" height="18" rx="2"/><circle cx="12" cy="12" r="3"/><path d="M12 9v3l2 1"/></svg>
            </div>
            <div class="feature-info">
              <span class="feature-stat">98.5%</span>
              <span class="feature-label">Precisión Facial</span>
            </div>
          </div>

          <div class="feature-card" style="--i: 1">
            <div class="feature-icon" style="--icon-bg: rgba(24, 95, 165, 0.2)">
              <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="#185FA5" stroke-width="1.8"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/><line x1="16" y1="13" x2="8" y2="13"/><line x1="16" y1="17" x2="8" y2="17"/></svg>
            </div>
            <div class="feature-info">
              <span class="feature-stat">Liquidación</span>
              <span class="feature-label">Automática CST</span>
            </div>
          </div>

          <div class="feature-card" style="--i: 2">
            <div class="feature-icon" style="--icon-bg: rgba(133, 79, 11, 0.2)">
              <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="#854F0B" stroke-width="1.8"><polygon points="22 3 2 3 10 12.46 10 19 14 21 14 12.46 22 3"/></svg>
            </div>
            <div class="feature-info">
              <span class="feature-stat">Dashboard</span>
              <span class="feature-label">en Tiempo Real</span>
            </div>
          </div>

          <div class="feature-card" style="--i: 3">
            <div class="feature-icon" style="--icon-bg: rgba(163, 45, 45, 0.2)">
              <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="#A32D2D" stroke-width="1.8"><rect x="3" y="11" width="18" height="11" rx="2"/><path d="M7 11V7a5 5 0 0 1 10 0v4"/></svg>
            </div>
            <div class="feature-info">
              <span class="feature-stat">Auditoría</span>
              <span class="feature-label">Inmutable</span>
            </div>
          </div>
        </div>

        <!-- Circular metrics -->
        <div class="banner-metrics">
          <div class="metric-item" style="--i: 0">
            <div class="metric-ring" style="--pct: 85; --color: #378ADD">
              <div class="ring-fill">
                <span class="ring-value">500+</span>
              </div>
            </div>
            <span class="metric-label">Empresas</span>
          </div>
          <div class="metric-item" style="--i: 1">
            <div class="metric-ring" style="--pct: 92; --color: #3B6D11">
              <div class="ring-fill">
                <span class="ring-value">50K+</span>
              </div>
            </div>
            <span class="metric-label">Usuarios</span>
          </div>
          <div class="metric-item" style="--i: 2">
            <div class="metric-ring" style="--pct: 78; --color: #185FA5">
              <div class="ring-fill">
                <span class="ring-value">99.9%</span>
              </div>
            </div>
            <span class="metric-label">Uptime</span>
          </div>
          <div class="metric-item" style="--i: 3">
            <div class="metric-ring" style="--pct: 95; --color: #639922">
              <div class="ring-fill">
                <span class="ring-value">4.9★</span>
              </div>
            </div>
            <span class="metric-label">Satisfacción</span>
          </div>
        </div>

        <!-- Bottom tagline -->
        <div class="banner-footer">
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"/><circle cx="12" cy="10" r="3"/></svg>
          <span>Transformando la gestión de RRHH en Colombia</span>
        </div>
      </div>
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
/* ========================================
   SPLIT LAYOUT
   ======================================== */
.auth-page {
  min-height: 100vh;
  display: flex;
}

/* Left panel */
.auth-left {
  width: 40%;
  min-width: 420px;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 2rem;
  background: var(--color-bg-white);
  position: relative;
  overflow: hidden;
}

.auth-left::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 4px;
  background: linear-gradient(90deg, var(--color-primary-700), var(--color-primary-500), var(--color-secondary-700));
}

.auth-left::after {
  content: '';
  position: absolute;
  width: 400px;
  height: 400px;
  border-radius: 50%;
  background: radial-gradient(circle, var(--color-primary-50) 0%, transparent 70%);
  bottom: -150px;
  right: -150px;
  pointer-events: none;
}

.auth-container {
  width: 100%;
  max-width: 390px;
  position: relative;
  z-index: 1;
}

/* Brand */
.auth-brand {
  text-align: center;
  margin-bottom: 1.75rem;
  animation: slide-in-up 0.5s ease both;
}

.auth-logo {
  width: 60px;
  height: 60px;
  background: linear-gradient(135deg, var(--color-primary-700), var(--color-primary-500));
  border-radius: 16px;
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto 0.875rem;
  color: #fff;
  box-shadow: 0 8px 24px rgba(24, 95, 165, 0.25);
  animation: logo-float 3s ease-in-out infinite;
}

@keyframes logo-float {
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(-4px); }
}

.auth-title {
  font-family: 'Young Serif', Georgia, serif;
  font-size: 1.75rem;
  color: var(--color-text-primary);
  margin-bottom: 0.25rem;
  letter-spacing: -0.02em;
}

.auth-subtitle {
  color: var(--color-text-secondary);
  font-size: 0.875rem;
  margin: 0;
}

/* Card */
.auth-card {
  background: var(--color-bg-white);
  border: 1px solid var(--color-divider);
  border-radius: var(--border-radius-xl);
  box-shadow: var(--shadow-lg);
  overflow: hidden;
  animation: slide-in-up 0.5s ease both;
  animation-delay: 0.1s;
}

.auth-card-body {
  padding: 2rem 2rem 1.5rem;
}

.auth-heading {
  font-size: 1.25rem;
  font-weight: 700;
  margin-bottom: 0.375rem;
  color: var(--color-text-primary);
}

.auth-desc {
  color: var(--color-text-secondary);
  font-size: 0.85rem;
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
  color: var(--color-text-secondary);
  font-size: 0.75rem;
  margin-top: 1.5rem;
  opacity: 0.6;
  animation: fade-in 0.5s ease both;
  animation-delay: 0.3s;
}

/* Form elements */
.form-group { margin-bottom: 1.25rem; }

.form-label {
  display: block;
  font-weight: 500;
  font-size: 0.8rem;
  color: var(--color-text-primary);
  margin-bottom: 0.375rem;
}

.form-input {
  display: block;
  width: 100%;
  padding: 0.6rem 0.875rem 0.6rem 2.5rem;
  font-family: inherit;
  font-size: 0.9rem;
  line-height: 1.5;
  color: var(--color-text-primary);
  background: var(--color-bg-white);
  border: 1.5px solid var(--color-border);
  border-radius: var(--border-radius-sm);
  transition: border-color var(--transition-fast), box-shadow var(--transition-fast);
}

.form-input:focus {
  border-color: var(--color-primary-500);
  box-shadow: 0 0 0 3px rgba(55, 138, 221, 0.12);
  outline: none;
}

.form-input::placeholder {
  color: var(--color-text-secondary);
  opacity: 0.45;
}

.input-with-icon {
  position: relative;
}

.input-icon {
  position: absolute;
  left: 0.875rem;
  top: 50%;
  transform: translateY(-50%);
  color: var(--color-text-secondary);
  pointer-events: none;
  z-index: 1;
  opacity: 0.5;
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
  transition: color var(--transition-fast);
  z-index: 2;
  opacity: 0.5;
}

.password-toggle:hover {
  opacity: 1;
  color: var(--color-primary-700);
}

.form-options {
  display: flex;
  align-items: center;
  margin-bottom: 1.25rem;
}

.checkbox-custom {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  cursor: pointer;
  font-size: 0.85rem;
  color: var(--color-text-secondary);
  user-select: none;
}

.checkbox-custom input[type="checkbox"] {
  width: 17px;
  height: 17px;
  accent-color: var(--color-primary-700);
  border-radius: 4px;
  cursor: pointer;
}

/* ========================================
   RIGHT PANEL — ANIMATED BANNER
   ======================================== */
.auth-right {
  flex: 1;
  position: relative;
  display: flex;
  align-items: center;
  justify-content: center;
  overflow: hidden; 
  background:
    radial-gradient(ellipse at 20% 50%, #0a3d7a 0%, transparent 50%),
    radial-gradient(ellipse at 80% 20%, #042C53 0%, transparent 40%),
    radial-gradient(ellipse at 50% 80%, #185FA5 0%, transparent 40%),
    linear-gradient(135deg, #021B36 0%, #042C53 30%, #0a3d7a 60%, #185FA5 100%);

}

/* Animated overlay grid */
.banner-bg {
  position: absolute;
  inset: 0;
  pointer-events: none;
}

.banner-bg::before {
  content: '';
  position: absolute;
  inset: 0;
  background-image:
    linear-gradient(rgba(255,255,255,0.03) 1px, transparent 1px),
    linear-gradient(90deg, rgba(255,255,255,0.03) 1px, transparent 1px);
  background-size: 50px 50px;
  animation: grid-scroll 20s linear infinite;
}

@keyframes grid-scroll {
  0% { transform: translate(0, 0); }
  100% { transform: translate(50px, 50px); }
}

/* Glow orbs */
.glow-orb {
  position: absolute;
  border-radius: 50%;
  filter: blur(60px);
  pointer-events: none;
}

.orb-1 {
  width: 350px;
  height: 350px;
  background: rgba(55, 138, 222, 0.15);
  top: -100px;
  right: 10%;
  animation: orb-drift 12s ease-in-out infinite;
}

.orb-2 {
  width: 250px;
  height: 250px;
  background: rgba(99, 153, 34, 0.1);
  bottom: 15%;
  left: 5%;
  animation: orb-drift 15s ease-in-out infinite reverse;
}

.orb-3 {
  width: 200px;
  height: 200px;
  background: rgba(24, 95, 165, 0.12);
  top: 40%;
  left: 30%;
  animation: orb-drift 18s ease-in-out infinite 2s;
}

@keyframes orb-drift {
  0%, 100% { transform: translate(0, 0) scale(1); }
  33% { transform: translate(30px, -40px) scale(1.1); }
  66% { transform: translate(-20px, 20px) scale(0.95); }
}

/* Floating geometric shapes */
.floating-shape {
  position: absolute;
  border-radius: 50%;
  pointer-events: none;
  opacity: 0.08;
}

.shape-1 {
  width: 120px;
  height: 120px;
  border: 2px solid rgba(255,255,255,0.4);
  top: 10%;
  left: 15%;
  animation: float-shape 8s ease-in-out infinite;
  border-radius: 30% 70% 70% 30% / 30% 30% 70% 70%;
}

.shape-2 {
  width: 80px;
  height: 80px;
  border: 2px solid rgba(99, 153, 34, 0.3);
  top: 60%;
  right: 20%;
  animation: float-shape 10s ease-in-out infinite 1s;
  border-radius: 50% 50% 20% 80% / 50% 50% 50% 50%;
}

.shape-3 {
  width: 60px;
  height: 60px;
  background: rgba(55, 138, 222, 0.1);
  top: 25%;
  right: 30%;
  animation: float-shape 7s ease-in-out infinite 2s;
  border-radius: 14px;
  transform: rotate(45deg);
}

.shape-4 {
  width: 100px;
  height: 100px;
  border: 2px solid rgba(255,255,255,0.15);
  bottom: 20%;
  left: 25%;
  animation: float-shape 12s ease-in-out infinite 0.5s;
  border-radius: 60% 40% 30% 70% / 60% 30% 70% 40%;
}

.shape-5 {
  width: 40px;
  height: 40px;
  background: rgba(99, 153, 34, 0.08);
  top: 50%;
  left: 10%;
  animation: float-shape 6s ease-in-out infinite 3s;
  border-radius: 8px;
  transform: rotate(30deg);
}

.shape-6 {
  width: 140px;
  height: 140px;
  border: 1px solid rgba(255,255,255,0.06);
  top: 70%;
  right: 10%;
  animation: float-shape 15s ease-in-out infinite 1.5s;
  border-radius: 30% 70% 50% 50% / 50% 60% 40% 50%;
}

@keyframes float-shape {
  0%, 100% {
    transform: translateY(0) rotate(0deg);
  }
  25% {
    transform: translateY(-20px) rotate(90deg);
  }
  50% {
    transform: translateY(-10px) rotate(180deg);
  }
  75% {
    transform: translateY(-25px) rotate(270deg);
  }
}

/* Particles */
.particle {
  position: absolute;
  width: 4px;
  height: 4px;
  border-radius: 50%;
  background: rgba(255,255,255,0.4);
  pointer-events: none;
  animation: particle-rise linear infinite;
}

.p1  { left: 10%; animation-duration: 6s; animation-delay: 0s; }
.p2  { left: 20%; animation-duration: 8s; animation-delay: 1s; }
.p3  { left: 35%; animation-duration: 7s; animation-delay: 2s; }
.p4  { left: 45%; animation-duration: 9s; animation-delay: 0.5s; }
.p5  { left: 55%; animation-duration: 6.5s; animation-delay: 3s; }
.p6  { left: 65%; animation-duration: 8.5s; animation-delay: 1.5s; }
.p7  { left: 75%; animation-duration: 7.5s; animation-delay: 2.5s; }
.p8  { left: 82%; animation-duration: 9.5s; animation-delay: 0.8s; }
.p9  { left: 15%; animation-duration: 10s; animation-delay: 4s; width: 3px; height: 3px; opacity: 0.3; }
.p10 { left: 50%; animation-duration: 11s; animation-delay: 3.5s; width: 5px; height: 5px; opacity: 0.5; }
.p11 { left: 70%; animation-duration: 7s; animation-delay: 5s; width: 3px; height: 3px; opacity: 0.3; }
.p12 { left: 90%; animation-duration: 8s; animation-delay: 2.2s; }

@keyframes particle-rise {
  0% {
    transform: translateY(100vh) scale(0);
    opacity: 0;
  }
  10% {
    opacity: 0.8;
    transform: translateY(80vh) scale(1);
  }
  90% {
    opacity: 0.6;
  }
  100% {
    transform: translateY(-10vh) scale(0.5);
    opacity: 0;
  }
}

/* Banner content */
.banner-content {
  position: relative;
  z-index: 2;
  max-width: 560px;
  padding: 3rem 2rem;
  text-align: center;
}

/* Tagline */
.banner-tagline {
  margin-bottom: 1rem;
}

.tagline-line {
  display: block;
  font-family: 'Young Serif', Georgia, serif;
  font-size: clamp(2rem, 4vw, 2.75rem);
  line-height: 1.15;
  color: #fff;
  opacity: 0;
  animation: tagline-reveal 0.8s ease both;
}

.tagline-line:first-child {
  animation-delay: 0.2s;
  font-weight: 300;
}

.tagline-line.accent {
  background: linear-gradient(135deg, #fff 30%, #B5D4F4 60%, #639922 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  font-weight: 400;
  animation-delay: 0.4s;
}

@keyframes tagline-reveal {
  from {
    opacity: 0;
    transform: translateY(20px);
    filter: blur(4px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
    filter: blur(0);
  }
}

.banner-sub {
  color: rgba(255, 255, 255, 0.5);
  font-size: 0.95rem;
  margin: 0 auto 2.5rem;
  max-width: 420px;
  animation: fade-in-up 0.6s ease both;
  animation-delay: 0.6s;
}

/* Feature cards grid */
.banner-features {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1rem;
  margin-bottom: 2.5rem;
}

.feature-card {
  display: flex;
  align-items: center;
  gap: 0.875rem;
  background: rgba(255, 255, 255, 0.06);
  backdrop-filter: blur(12px);
  -webkit-backdrop-filter: blur(12px);
  border: 1px solid rgba(255, 255, 255, 0.08);
  border-radius: 14px;
  padding: 1rem 1.125rem;
  cursor: default;
  opacity: 0;
  animation: card-enter 0.6s ease both;
  animation-delay: calc(0.8s + var(--i, 0) * 0.12s);
  transition: transform 0.3s ease, box-shadow 0.3s ease, border-color 0.3s ease;
}

.feature-card:hover {
  transform: translateY(-4px) scale(1.02);
  box-shadow: 0 12px 40px rgba(0, 0, 0, 0.25);
  border-color: rgba(255, 255, 255, 0.2);
  background: rgba(255, 255, 255, 0.1);
}

@keyframes card-enter {
  from {
    opacity: 0;
    transform: translateY(20px) scale(0.95);
  }
  to {
    opacity: 1;
    transform: translateY(0) scale(1);
  }
}

.feature-icon {
  width: 44px;
  height: 44px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
  transition: transform 0.3s ease;
}

.feature-card:hover .feature-icon {
  transform: scale(1.15) rotate(-5deg);
}

.feature-info {
  text-align: left;
}

.feature-stat {
  display: block;
  font-size: 1rem;
  font-weight: 700;
  color: #fff;
  line-height: 1.2;
}

.feature-label {
  display: block;
  font-size: 0.75rem;
  color: rgba(255, 255, 255, 0.5);
  font-weight: 400;
}

/* Circular metrics */
.banner-metrics {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 1.5rem;
  margin-bottom: 2rem;
}

.metric-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.6rem;
  opacity: 0;
  animation: fade-in-up 0.6s ease both;
  animation-delay: calc(1.4s + var(--i, 0) * 0.15s);
}

.metric-ring {
  width: 80px;
  height: 80px;
  border-radius: 50%;
  position: relative;
  display: flex;
  align-items: center;
  justify-content: center;
  background: conic-gradient(
    var(--color) 0%,
    var(--color) calc(var(--pct) * 1%),
    rgba(255, 255, 255, 0.08) calc(var(--pct) * 1%),
    rgba(255, 255, 255, 0.08) 100%
  );
  animation: ring-enter 1s ease both;
  animation-delay: calc(1.6s + var(--i, 0) * 0.15s);
}

.metric-ring::before {
  content: '';
  position: absolute;
  inset: 6px;
  border-radius: 50%;
  background: rgba(4, 44, 83, 0.85);
}

.ring-fill {
  position: relative;
  z-index: 1;
}

.ring-value {
  font-size: 0.85rem;
  font-weight: 700;
  color: #fff;
  line-height: 1;
}

@keyframes ring-enter {
  from {
    opacity: 0;
    transform: scale(0) rotate(-180deg);
  }
  to {
    opacity: 1;
    transform: scale(1) rotate(0deg);
  }
}

.metric-item .metric-label {
  font-size: 0.72rem;
  color: rgba(255, 255, 255, 0.5);
  text-transform: uppercase;
  letter-spacing: 0.05em;
  font-weight: 500;
}

/* Pulse ring animation on hover */
.metric-item:hover .metric-ring {
  animation: ring-pulse 0.8s ease;
}

@keyframes ring-pulse {
  0% { box-shadow: 0 0 0 0 rgba(255,255,255,0.15); }
  50% { box-shadow: 0 0 0 12px rgba(255,255,255,0); }
  100% { box-shadow: 0 0 0 0 rgba(255,255,255,0); }
}

/* Banner footer */
.banner-footer {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  color: rgba(255, 255, 255, 0.35);
  font-size: 0.8rem;
  opacity: 0;
  animation: fade-in 0.6s ease both;
  animation-delay: 2.2s;
}

/* Animations */
@keyframes slide-in-up {
  from { opacity: 0; transform: translateY(20px); }
  to { opacity: 1; transform: translateY(0); }
}

@keyframes fade-in {
  from { opacity: 0; }
  to { opacity: 1; }
}

@keyframes fade-in-up {
  from { opacity: 0; transform: translateY(12px); }
  to { opacity: 1; transform: translateY(0); }
}

/* ========================================
   RESPONSIVE
   ======================================== */
@media (max-width: 1024px) {
  .auth-left {
    width: 45%;
    min-width: 380px;
  }
  .banner-metrics {
    gap: 1rem;
  }
  .metric-ring {
    width: 68px;
    height: 68px;
  }
  .metric-ring::before {
    inset: 5px;
  }
  .ring-value {
    font-size: 0.75rem;
  }
}

@media (max-width: 820px) {
  .auth-page {
    flex-direction: column;
  }
  .auth-left {
    width: 100%;
    min-width: unset;
    padding: 1.5rem 1rem;
    min-height: 100vh;
  }
  .auth-right {
    display: none;
  }
  .auth-container {
    max-width: 380px;
  }
  .banner-features {
    grid-template-columns: 1fr;
  }
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
