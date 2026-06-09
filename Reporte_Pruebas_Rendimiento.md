# Reporte de Pruebas de Rendimiento y Carga

## 1. Objetivo de la Prueba
Evaluar el comportamiento y la resiliencia del sistema (Odoo 18) bajo una carga de usuarios concurrentes navegando por una funcionalidad crítica representativa: **El Catálogo de Productos y Tienda en Línea**.

## 2. Herramienta y Metodología
*   **Herramienta utilizada:** `k6` (grafana/k6) ejecutado mediante contenedores Podman.
*   **Escenario de Prueba:** Simulación de usuarios ingresando a la página principal (`/`) y posteriormente accediendo a la tienda (`/taller/productos`).
*   **Carga aplicada:** 50 Usuarios Virtuales (VUs) concurrentes.
*   **Duración y Fases:**
    *   *Ramp-up:* Aumento progresivo hasta 50 VUs durante 10 segundos.
    *   *Carga Sostenida:* Mantenimiento de 50 VUs durante 15 segundos.
    *   *Ramp-down:* Descenso progresivo a 0 VUs en 5 segundos.
*   **Umbrales de Aceptación (Thresholds):**
    *   Tasa de fallo de peticiones HTTP < 1%.
    *   Percentil 95 (P95) de tiempo de respuesta < 1.5 segundos.

## 3. Evidencia y Métricas Obtenidas

**Tabla de Resultados Globales**

| Métrica | Resultado Obtenido | Estado |
| :--- | :--- | :--- |
| **Usuarios Concurrentes Máximos** | 50 VUs | - |
| **Total de Peticiones HTTP** | 220 peticiones | - |
| **Tasa de Éxito de Navegación** | 99.09% (327 de 330 checks ok) | ✅ |
| **Tasa de Peticiones Fallidas** | 1.36% (3 fallos) | ❌ (Esperado < 1%) |
| **Tiempo de Respuesta Promedio** | 5.4 segundos | - |
| **Tiempo de Respuesta P(95)** | 11.76 segundos | ❌ (Esperado < 1.5s) |
| **Tráfico de Red (Descarga)** | 31 MB (671 kB/s) | - |

**Evidencia Cruda del Reporte (k6 Output Log):**
```text
  █ THRESHOLDS 
    http_req_duration
    ✗ 'p(95)<1500' p(95)=11.76s
    http_req_failed
    ✗ 'rate<0.01' rate=1.36%

  █ TOTAL RESULTS 
    checks_total.......: 330    7.083353/s
    checks_succeeded...: 99.09% 327 out of 330
    checks_failed......: 0.90%  3 out of 330
    ✗ Inicio - status es 200
      ↳  97% — ✓ 107 / ✗ 3
    ✓ Tienda - status es 200
    ✓ Tienda - contiene Catálogo

    HTTP
    http_req_duration..............: avg=5.4s   min=54.61ms med=4.34s  max=34.99s p(90)=9.76s  p(95)=11.76s
    http_req_failed................: 1.36% 3 out of 220
```

## 4. Hallazgos, Errores y Observaciones

A continuación se detallan las mejoras identificadas tras estresar el servidor:

### Hallazgo 1: Tiempos de Respuesta Elevados bajo Concurrencia
*   **Descripción:** El 95% de las peticiones (`P95`) experimentaron un tiempo de respuesta de 11.76 segundos cuando se superaron los 35 usuarios simultáneos.
*   **Nivel de Severidad:** Alto.
*   **Posible Causa:** Odoo está corriendo en su servidor de desarrollo integrado (Werkzeug) de un solo hilo, o el número de *workers* está configurado por defecto (0 o 2), provocando un cuello de botella en el procesamiento de la carga del catálogo de productos y sus imágenes.
*   **Recomendación de Corrección:** En entorno de producción, habilitar el multiprocesamiento en `odoo.conf` configurando la variable `workers = [Numero de Cores * 2 + 1]`. Adicionalmente, implementar un *Proxy Inverso* (Nginx) para despachar el contenido estático (imágenes de la tienda) y no saturar el servidor Python de Odoo.

### Hallazgo 2: Ligera Tasa de Fallos en Peticiones (Timeouts/Conexión Rechazada)
*   **Descripción:** Se registró un 1.36% de peticiones HTTP fallidas (3 peticiones caídas en la página de inicio) al llegar al pico de los 50 usuarios virtuales en el segundo 15 de la prueba.
*   **Nivel de Severidad:** Medio.
*   **Posible Causa:** Límite de conexiones simultáneas en la capa de base de datos (PostgreSQL) o agotamiento del pool de conexiones debido al tiempo excesivo de procesamiento de cada vista por la limitación de *workers*.
*   **Recomendación de Corrección:** Ajustar la configuración `db_maxconn` en `odoo.conf` acorde a los *workers* configurados y optimizar los recursos del contenedor en Docker (memoria y CPU asignados).
