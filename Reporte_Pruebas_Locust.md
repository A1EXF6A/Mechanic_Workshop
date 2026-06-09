# Reporte de Pruebas de Rendimiento y Carga (Locust)

## 1. Objetivo de la Prueba
Evaluar el comportamiento, la estabilidad y la resiliencia del sistema (Odoo 18) bajo una carga de usuarios concurrentes navegando por las funcionalidades principales del portal: **Mi Cuenta (Portal de Usuario)** y **Tienda en Línea (Catálogo)**.

## 2. Herramienta y Metodología
*   **Herramienta utilizada:** `Locust` (ejecutado en entorno virtual de Python).
*   **Escenario de Prueba:** Simulación de usuarios navegando entre la página principal, el portal de clientes (`/my`) y el catálogo de productos de la tienda (`/taller/productos`).
*   **Carga aplicada:** 50 Usuarios concurrentes (Peak concurrency).
*   **Tasa de incremento (Spawn rate):** 1 usuario por segundo hasta alcanzar los 50.
*   **Entorno de ejecución:** Odoo 18 ejecutándose sobre contenedores Podman en entorno de desarrollo.

## 3. Evidencia y Resultados Obtenidos

Se generó un reporte interactivo en formato HTML (`Reporte_Locust_Rendimiento.html`) que documenta las métricas de la prueba. 

**Resumen de Métricas Clave:**

| Métrica | Resultado Obtenido | Estado |
| :--- | :--- | :--- |
| **Usuarios Concurrentes Máximos** | 50 Usuarios | - |
| **Tiempo de Respuesta P(95)** | ~11 segundos | ❌ (Excede el límite aceptable) |
| **Tasa de Errores** | Presencia de errores HTTP 502 | ❌ |
| **Páginas Afectadas** | Tienda en línea y portal | - |

*(Nota: Para visualizar las gráficas interactivas de TPS y latencia a lo largo del tiempo, por favor abra el archivo `Reporte_Locust_Rendimiento.html` en su navegador web).*

## 4. Hallazgos, Errores y Observaciones

A continuación se detallan los cuellos de botella identificados durante la prueba de estrés:

### Hallazgo 1: Tiempos de Respuesta Críticos bajo Alta Concurrencia
*   **Descripción:** A medida que la cantidad de usuarios simultáneos se acercaba a 50, el tiempo de respuesta del percentil 95 (P95) escaló hasta aproximadamente 11 segundos, deteriorando significativamente la experiencia del usuario.
*   **Nivel de Severidad:** Alto.
*   **Posible Causa:** El servidor integrado de Odoo (Werkzeug) está diseñado para desarrollo y, por defecto, procesa las peticiones en un solo hilo (single-thread). Al recibir múltiples peticiones pesadas (como la carga de imágenes del catálogo), las peticiones se encolan.
*   **Recomendación de Corrección:** Para un entorno de producción, es obligatorio configurar el archivo `odoo.conf` habilitando el modo multiproceso (`workers = [Núcleos de CPU * 2 + 1]`).

### Hallazgo 2: Errores 502 (Bad Gateway) y Conexiones Rechazadas
*   **Descripción:** Durante el pico de estrés, la herramienta Locust registró fallos en las peticiones que retornaron un código de estado `502 Bad Gateway`.
*   **Nivel de Severidad:** Alto.
*   **Posible Causa:** El encolamiento excesivo provocó que el servidor no pudiera despachar las peticiones a tiempo, agotando el tiempo de espera (timeout) o el límite de conexiones concurrentes tanto a nivel de red como en la base de datos PostgreSQL.
*   **Recomendación de Corrección:** 
    1. Implementar un servidor proxy inverso (como Nginx o Apache) frente a Odoo. Esto mitigará los errores 502 al manejar mejor las conexiones de red.
    2. Delegar la carga de archivos estáticos (imágenes, CSS, JS) al servidor proxy (Nginx) para liberar carga computacional de los workers de Odoo.
    3. Ajustar el límite de conexiones en la base de datos (`db_maxconn`).
