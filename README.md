# Proyecto Integrador Parcial II

## Tema

Desarrollo e Implementación de un Pipeline CI/CD Seguro con integración de IA para la Detección Automática de Vulnerabilidades en código fuente mediante un Modelo de Minería de Datos.

## Links Importantes

### Datasets

1. [Kaggle Dataset](https://www.kaggle.com/datasets/jiscecseaiml/vulnerability-fix-dataset/data)
2. [HuggingFace Dataset](https://huggingface.co/datasets/nuojohnchen/devign-processed/viewer/default/train)

### GitHub Pipeline

[GitHub Actions](https://docs.github.com/en/actions/get-started/understand-github-actions)

## Objetivo

Diseñar, implementar y demostrar un pipeline CI/CD completamente automatizado y seguro que integre un modelo de inteligencia artificial basado en técnicas de minería de datos capaz de clasificar código fuente como **seguro** o **vulnerable**, permitiendo que únicamente el código considerado seguro llegue a producción.

El proyecto debe aplicar principios de:

- Secure DevOps
- Shift-Left Security

## Flujo de Trabajo Requerido

### Estructura de ramas

```text
dev   → Desarrollo
test  → Staging / Pruebas
main  → Producción
```

### Trigger del Pipeline

El pipeline debe ejecutarse automáticamente al crear un Pull Request desde:

```text
dev → test
```

## Etapas del Pipeline

### Etapa 1: Revisión de Seguridad con Modelo de Minería de Datos

1. Descargar el diff del Pull Request.
2. Procesar el código modificado.
3. Extraer características del código:
   - Tokens
   - AST simplificado
   - Llamadas a funciones peligrosas
   - Uso de sanitización
   - Otras métricas relevantes
4. Clasificar el código como:
   - SEGURO
   - VULNERABLE

Si el modelo detecta vulnerabilidades:

- Bloquear el merge.
- Marcar el Pull Request como rechazado.
- Crear comentario automático indicando:
  - Tipo de vulnerabilidad.
  - Probabilidad detectada.
- Enviar notificación inmediata vía Telegram.
- Agregar etiqueta:

```text
fixing-required
```

- Crear automáticamente una Issue vinculada.

Si el modelo clasifica como seguro

```text
Continuar con la siguiente etapa
```

### Etapa 2: Merge Automático a `test` y Ejecución de Pruebas

- Merge automático hacia la rama `test`.
- Ejecución de pruebas:
  - Unitarias
  - Integración

Ejemplos:

- pytest
- Jest
- JUnit

Si alguna prueba falla

- Bloquear el proceso.
- Notificar vía Telegram.
- Agregar etiqueta:

```text
tests-failed
```

### Etapa 3: Merge a Producción y Despliegue

Esta etapa se ejecuta únicamente si todas las etapas anteriores fueron exitosas.

- Merge automático hacia `main`.
- Construcción de imagen Docker.
- Despliegue automático.

Proveedores permitidos

- Render
- Railway
- Fly.io
- Vercel (Frontend)
- Northflank
- Docker Hub + Play with Docker
- Heroku (si existe plan gratuito)
- Otro proveedor equivalente

Resultado

- Aplicación desplegada en producción.
- Notificación final vía Telegram y/o correo electrónico.

## Notificaciones Obligatorias

El sistema debe notificar los siguientes eventos:

- Inicio de revisión de seguridad.
- Resultado de clasificación:
  - Seguro
  - Vulnerable
  - Probabilidad asociada
- Merge exitoso a `test`.
- Resultado de pruebas.
- Despliegue exitoso o fallido.
- Rechazo por vulnerabilidad detectada.

## Requisitos

### Modelo de Machine Learning

- Entrenado por el estudiante.
- Entregar:
  - `.pkl`
  - `.joblib`

Datasets recomendados

- Big-Vul
- DiverseVul
- CVEFixes
- Juliet Test Suite
- Kaggle
- Dataset propio

Features mínimas

- Tokens
- Profundidad del AST
- Llamadas a funciones peligrosas:
  - `eval`
  - `exec`
  - `subprocess`
  - SQL sin parametrizar
- Presencia de sanitización o escapes

Precisión mínima

```text
Accuracy ≥ 82%
```

Debe demostrarse mediante validación cruzada y mostrarse en el README.

### Telegram Bot

- Bot propio.
- Token almacenado mediante Secrets.

### Despliegue

- Debe estar online.
- Debe ser accesible públicamente.

### Protección de ramas

Configurar Branch Protection Rules para:

- `test`
- `main`

Debe requerirse aprobación de la revisión de seguridad antes de permitir merges.

## Criterios de Evaluación

| Criterio | Puntaje |
|-----------|----------|
| Automatización completa del pipeline | 6 |
| Modelo de minería de datos propio (sin LLM) | 6 |
| Notificaciones e issues automáticas | 3 |
| Despliegue funcional en proveedor gratuito | 3 |
| Calidad del README e informe | 2 |

**Total: 20 puntos**
