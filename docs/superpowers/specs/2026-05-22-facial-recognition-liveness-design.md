# Diseño de Integración de Detección de Vitalidad por Análisis Temporal

## Visión General

Este documento detalla la implementación de detección de vitalidad (liveness detection) utilizando análisis temporal para prevenir ataques de suplantación en el sistema de reconocimiento facial del Sistema de Control de Asistencia y Nómina. El enfoque propuesto analiza micro-movimientos naturales y variaciones en secuencias de video para distinguir entre rostros vivos y ataques usando fotos, videos o máscaras.

## Problema a Resolver

El sistema actual de reconocimiento facial es vulnerable a ataques de suplantación donde un atacante podría usar:
- Fotografías estáticas de un empleado autorizado
- Videos reproducidos del empleado
- Máscaras 3D o impresión de alta calidad

Esto comprometería la seguridad del sistema de registro de asistencia, permitiendo registros fraudulentos.

## Enfoque Seleccionado: Análisis Temporal de Micro-movimientos

En lugar de requerir acciones explícitas del usuario (como parpadear o girar la cabeza), este enfoque analiza secuencias de video capturadas durante el proceso normal de reconocimiento para detectar:
- Micro-movimientos involuntarios de ojos, boca y cabeza
- Variaciones en textura de piel y reflexión de luz
- Cambios sutiles en expresiones faciales que ocurren naturalmente

## Arquitectura del Sistema

### Componentes Principales

1. **Buffer de Frames Temporal** - Almacena los últimos N frames de video para análisis
2. **Módulo de Detección de Vitalidad** - Analiza el buffer para calcular una puntuación de vitalidad
3. **Integración con Pipeline Existente** - Se coloca después de la detección facial pero antes de la verificación
4. **Interfaz de Usuario de Feedback** - Indica visualmente el progreso y resultado de la verificación de vitalidad

### Flujo de Procesamiento

```
Captura de Video → Detección de Facial → [BUFFER TEMPORAL] → 
Análisis de Vitalidad → Verificación Facial → Registro de Asistencia
```

### Algoritmo de Detección de Vitalidad

El análisis temporal calculará una puntuación basada en:

1. **Variación de Landmarks Faciales** - Movimiento de puntos clave (ojos, boca, nariz) entre frames
2. **Cambios en Textura de Piel** - Análisis de patrones de alta frecuencia que indican tejido vivo
3. **Consistencia de Iluminación** - Variaciones naturales en reflexión que faltan en pantallas/fotos
4. **Score Combinado** - Ponderación de los factores anteriores para decisión final

## Detalles de Implementación

### Modificaciones al Frontend

#### 1. RegistroAsistencia.vue
- Añadir buffer de frames para almacenar los últimos 30 frames (1 segundo a 30fps)
- Implementar función `analyzeLiveness(framesBuffer)` que retorna puntuación 0-1
- Modificar `captureAndVerify()` para incluir análisis de vitalidad antes de enviar al backend
- Añadir indicadores visuales de progreso de vitalidad durante la captura
- Actualizar estado de verificación para incluir resultados de vitalidad

#### 2. FotoFacialUpload.vue (para enrollamiento)
- Añadir funcionalidad similar para asegurar que las fotos de enrollamiento sean de rostros vivos
- Implementar buffer temporal durante el proceso de captura de foto de perfil
- Validar que la foto almacenada provenga de un frame que pasaron la prueba de vitalidad

### Modificaciones al Backend

#### 1. views.py - registrar_asistencia_view
- Aceptar opcionalmente un array de descriptores faciales (promedio de múltiples frames) en lugar de un solo descriptor
- Almacenar metadata de vitalidad en la tabla Asistencia para auditoría
- Opcionalmente, requerir umbral mínimo de vitalidad para autenticación exitosa

#### 2. Modelo Asistencia (si es necesario)
- Añadir campo `liveness_score`DecimalField para almacenar la puntuación de vitalidad
- Añadir campo `liveness_validated`BooleanField para indicar si pasó la validación de vitalidad

### Algoritmo de Análisis Temporal (Pseudocódigo)

```javascript
function analyzeLiveness(framesBuffer) {
  if (framesBuffer.length < MIN_FRAMES) return 0.0;
  
  // 1. Extraer landmarks de todos los frames
  const landmarksSequence = framesBuffer.map(frame => extractLandmarks(frame));
  
  // 2. Calcular variación en posición de landmarks (ojos, cejas, boca)
  const eyeMovement = calculateLandmarkVariation(landmarksSequence, EYE_LANDMARKS);
  const mouthMovement = calculateLandmarkVariation(landmarksSequence, MOUTH_LANDMARKS);
  const eyebrowMovement = calculateLandmarkVariation(landmarksSequence, EYEBROW_LANDMARKS);
  
  // 3. Analizar variación de textura (usando LBP o similares en regiones faciales)
  const textureVariation = analyzeTextureVariation(framesBuffer);
  
  // 4. Analizar consistencia de iluminación
  const illuminationConsistency = analyzeIlluminationConsistency(framesBuffer);
  
  // 5. Combinar scores con pesos
  const livenessScore = 
    0.3 * normalize(eyeMovement) +
    0.25 * normalize(mouthMovement) +
    0.2 * normalize(eyebrowMovement) +
    0.15 * normalize(textureVariation) +
    0.1 * normalize(illuminationConsistency);
  
  return Math.min(1.0, Math.max(0.0, livenessScore));
}
```

### Umbrales y Configuración

- **Umbral de Aceptación**: 0.7 (70% de confianza en vitalidad)
- **Frames Mínimos para Análisis**: 10 frames (~0.33 segundos a 30fps)
- **Frames Máximos en Buffer**: 30 frames (1 segundo)
- **Frecuencia de Análisis**: Cada 5 frames durante el proceso de captura
- **Configurables vía ParametrosSistema**: 
  - `LIVENESS_THRESHOLD` (default: 0.7)
  - `LIVENESS_MIN_FRAMES` (default: 10)
  - `LIVENESS_MAX_FRAMES` (default: 30)

## Manejo de Errores y Casos Especiales

### Condiciones de Baja Iluminación
- Reducir dependencia de análisis de textura
- Aumentar peso en análisis de movimiento de landmarks
- Proveer feedback visual al usuario para mejorar iluminación

### Movimientos Excesivos del Usuario
- Detectar y compensar movimientos grandes de cabeza
- Enfocar análisis en movimientos relativos defeatures faciales
- Limitar análisis a región normalizada alrededor de la cara detectada

### Fallos en Detección de Facial
- Si no se detecta cara en suficientes frames, marcar como fallido
- Proveer reintentos automáticos con feedback claro

### Rendimiento en Dispositivos Limitados
- Opcionalmente reducir resolución de frames para análisis
- Implementar downsampling inteligente manteniendo regiones faciales clave
- Cachear resultados de detección de landmarks cuando sea posible

## Consideraciones de Seguridad

### Resistencia a Ataques Conocidos
- **Fotos Estáticas**: Detectadas por falta de micro-movimientos y variación de textura
- **Videos Reproducidos**: Detectados por inconsistencias en iluminación y patrones de compresión
- **Máscaras 3D**: Detectadas por falta de variación subcutánea y patrones de reflejo anómalos

### Privacidad y Almacenamiento
- Los frames de video solo se mantienen en memoria durante el análisis
- No se almacenan ni transmiten frames de video crudos
- Solo se almacenan los descriptors faciales y puntuaciones de vitalidad
- Cumplimiento con regulaciones de protección de datos (Habeas Data colombiano)

## Experiencia de Usuario

### Feedback Visual
- Durante captura: Indicador progresivo de "Analizando vitalidad..." 
- Éxito: Animación de check verde + mensaje "Vitalidad verificada"
- Fallo: Animación de advertencia + sugerencia específica ("Mejor iluminación", "Menos movimiento", etc.)

### Accesibilidad
- Instrucciones claras y concisas en múltiples formatos (visual, textual)
- Tiempos de respuesta adecuados para usuarios con diferentes capacidades
- Compatibilidad con lectores de pantalla mediante ARIA labels apropiados

## Testing y Validación

### Pruebas Unitarias
- Mock de secuencia de frames con variaciones conocidas
- Verificación de cálculo correcto de puntuaciones de liveness
- Pruebas de edge cases (buffer vacío, un solo frame, etc.)

### Pruebas de Integración
- Flujo completo desde captura hasta registro con vitalidad exitosa
- Flujo completo con fallo de vitalidad que activa solicitud manual
- Verificación de que los scores se almacenan correctamente en BD

### Pruebas de Seguridad
- Pruebas con ataques de foto estática (deben fallar)
- Pruebas con ataques de video reproducido (deben fallar)
- Pruebas con usuarios reales en diversas condiciones (deben pasar mayormente)
- Pruebas con usuarios usando gafas, sombreros, maquillaje ligeros (deben pasar)

### Métricas de Rendimiento
- Tiempo adicional de procesamiento objetivo: < 500ms
- Tasa de falsos positivos objetivo: < 1%
- Tasa de falsos negativos objetivo: < 5% (balanceando seguridad y usabilidad)

## Dependencias

No se requieren dependencias adicionales más allá de:
- face-api.js (ya incluido)
- Posible uso de algoritmos de visión por computadora básicos implementados directamente
- potencialmente tf.js para operaciones de tensor si se necesita aceleración (opcional)

## Plan de Implementación por Fase

### Fase 1: Core Algorithm
- Implementar buffer de frames temporal
- Desarrollar algoritmo básico de análisis de landmarks
- Integrar con flujo existente de captura
- Pruebas unitarias básicas

### Fase 2: Mejora de Algoritmo
- Añadir análisis de textura e iluminación
- Optimizar pesos mediante pruebas empíricas
- Implementar manejo de condiciones edge
- Pruebas de integración completas

### Fase 3: Interfaz de Usuario
- Diseñar e implementar feedback visual
- Añadir indicadores de progreso y estados
- Optimizar experiencia basada en pruebas de usuario
- Pruebas de usabilidad

### Fase 4: Backend y Auditoría
- Modificar endpoints para aceptar/scores de vitalidad
- Actualizar modelo de base de datos si es necesario
- Implementar logging de auditoría para validaciones de vitalidad
- Pruebas de seguridad completas

## Riesgos y Mitigaciones

### Riesgo 1: Impacto en Rendimiento
- **Mitigación**: Optimizar algoritmos, usar requestAnimationFrame, procesar en web worker si disponible

### Riesgo 2: Falsos Negativos Altos
- **Mitigación**: Calibrar umbrales con datos reales, proporcionar reintentos intelligentes

### Riesgo 3: Complejidad de Implementación
- **Mitigación**: Enfoque incremental, comenzar con detección básica de movimiento y aumentar sofisticación

### Riesgo 4: Problemas de Compatibilidad de Dispositivos
- **Mitigación**: Detección de capacidades, fallback a métodos más simples en dispositivos limitados

## Métricas de Éxito

1. **Reducción Intentos Fraudulentos**: Objetivo >95% de блокировка de ataques de suplantación
2. **Tasa de Aceptación Usuario Legítimo**: Objetivo >99% en condiciones normales
3. **Tiempo Promedio de Procesamiento**: Objetivo < 800ms adicional al proceso actual
4. **Satisfacción de Usuario**: Objetivo >4.5/5 en encuestas de usabilidad
5. **Costo de Implementación**: Dentro estimado de 2 sprints de desarrollo

## Conclusión

La integración de detección de vitalidad mediante análisis temporal proporciona un equilibrio efectivo entre seguridad y usabilidad para el Sistema de Control de Asistencia y Nómina. Al aprovechar la secuencia natural de video ya capturada durante el proceso de reconocimiento facial, este enfoque agrega una capa significativa de defensa contra ataques de suplantación sin requerir cambios significativos en el flujo de trabajo del usuario ni acciones explícitas que puedan causar frustración.

Este diseño es extensible para futuras mejoras como la incorporación de detección específica de parpadeo, análisis de profundidad mediante cámaras estéreo, o integración con soluciones de vitality detection basadas en aprendizaje profundo si se requiere mayor nivel de seguridad en el futuro.