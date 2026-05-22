# Frontend — SoftVar

Este directorio contiene el frontend del **Sistema de Control de Asistencia y Nómina**.

> Para documentación completa del proyecto, consulta el [`README.md`](../README.md) en la raíz.

## Stack

- **Vue 3** + **Composition API**
- **Vue Router** (SPA con rutas protegidas por rol)
- **Vite** (bundler)
- **Chart.js** (gráficas interactivas)
- **Axios** (cliente HTTP)
- **jsPDF** (generación de PDF)

## Comandos

```bash
npm install       # Instalar dependencias
npm run dev       # Servidor de desarrollo (localhost:5173)
npm run build     # Build producción
npm run preview   # Vista previa del build
```

## Sistema de diseño

El frontend implementa un sistema de diseño corporativo definido en `../CLAUDE.md`:

- **Paleta:** Azul primario (`#185FA5`) + Verde secundario (`#3B6D11`) + Neutros
- **Tipografía:** Work Sans (cuerpo) + Young Serif (títulos)
- **Micro-interacciones:** Animaciones CSS, hover states, transiciones
- **Responsive:** Adaptable a desktop, tablet y móvil
