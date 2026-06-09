# Reporte de Pruebas de Estrés (Stress Testing)

## 1. Objetivo de la Prueba
Determinar el **punto de ruptura (breaking point)** del servidor actual de Odoo 18. A diferencia de la prueba de carga normal, el objetivo aquí es someter la aplicación a un tráfico extremo repentino para observar cómo falla el sistema, documentar los mensajes de error y evaluar el límite absoluto de su capacidad.

## 2. Herramienta y Metodología
*   **Herramienta utilizada:** `Locust` (ejecutado en entorno virtual de Python).
*   **Escenario de Prueba:** Simulación de un pico de tráfico masivo navegando simultáneamente por el Catálogo de Productos (`/taller/productos`), Inicio (`/`) y la página de Nosotros (`/taller/nosotros`).
*   **Carga aplicada:** 500 Usuarios concurrentes.
*   **Tasa de Inyección (Spawn Rate):** 50 usuarios nuevos por segundo (llegando a 500 en apenas 10 segundos).
*   **Duración:** 30 segundos.
*   **Entorno de ejecución:** Odoo 18 ejecutándose sobre contenedores Podman en entorno de desarrollo.

## 3. Evidencia y Resultados Obtenidos

Se generó la evidencia interactiva en el archivo `Reporte_Locust_Stress.html`. 

**Resumen de Métricas Críticas (El Colapso):**

| Métrica | Resultado Obtenido | Estado |
| :--- | :--- | :--- |
| **Usuarios Concurrentes Máximos** | 500 Usuarios | - |
| **Tiempo de Respuesta P(95)** | ~12.0 segundos | ❌ Crítico |
| **Tiempo Máximo de Espera** | 24.2 segundos | ❌ Inaceptable |
| **Tasa de Peticiones Fallidas** | 4.24% (19 peticiones caídas) | ❌ |
| **Código de Error Devuelto** | `HTTP 502 Bad Gateway` | - |

*(Nota: En el archivo `Reporte_Locust_Stress.html` se puede observar claramente la gráfica de "Failures" comenzando a elevarse drásticamente al llegar a los 300-400 usuarios).*

## 4. Análisis de Fallos y Cuellos de Botella

Al exigir el sistema por encima de sus capacidades, se registraron los siguientes comportamientos críticos:

### Fallo Crítico 1: Colapso por Encolamiento (HTTP 502)
*   **Descripción:** Antes de terminar los 30 segundos de prueba, el servidor comenzó a rechazar activamente las conexiones de los usuarios. La herramienta Locust capturó múltiples errores `502 Server Error: Bad Gateway`.
*   **Posible Causa:** Un error 502 en este contexto indica que el proceso de Odoo (que está corriendo en *single-thread*) no pudo aceptar más conexiones. El límite de la cola del servidor web integrado (Werkzeug) se saturó debido a que no despachaba a la misma velocidad que entraban las peticiones (50 peticiones nuevas por segundo).

### Fallo Crítico 2: Latencia Extrema (Picos de 24 segundos)
*   **Descripción:** A los usuarios que no les dio error 502, el sistema los dejó en "espera" cargando la página. Algunos usuarios virtuales llegaron a esperar hasta 24 segundos para ver el contenido del inicio o de la tienda.
*   **Posible Causa:** Agotamiento de recursos en el contenedor, bloqueo de operaciones de entrada y salida (I/O) al intentar cargar imágenes simultáneas, o saturación del *pool* de conexiones hacia la base de datos PostgreSQL.

## 5. Recomendación Técnica Fundamental
Esta prueba de estrés demuestra empíricamente que **bajo ninguna circunstancia** se debe exponer el servidor integrado de Odoo directamente a internet sin optimizaciones. 

**Para un paso a Producción es mandatorio:**
1. Desplegar un **Proxy Inverso (Nginx)** configurado para realizar balanceo de carga.
2. Modificar la configuración de Odoo a modo **Multiproceso**, asignando un pool de workers (`workers = 5` o según los cores disponibles) para manejar peticiones concurrentes en paralelo.
3. Configurar **Nginx** para que almacene en caché (Cache) los archivos estáticos de la tienda (imágenes, CSS) para no consumir recursos del servidor de aplicaciones de Odoo.
