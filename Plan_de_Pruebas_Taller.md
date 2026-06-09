# Plan de Pruebas del Proyecto: Sistema de Gestión para Taller Mecánico Automotriz

## 1. Objetivo de las Pruebas
Validar el correcto funcionamiento de los módulos desarrollados y configurados en Odoo 18 para el "Taller Mecánico Automotriz". El objetivo principal es garantizar que las funcionalidades operativas (portal web, comercio electrónico, gestión interna del taller y facturación electrónica SRI) operen de acuerdo con los requerimientos técnicos y de negocio establecidos, asegurando la integridad de los datos y una experiencia de usuario óptima.

## 2. Alcance
Este plan de pruebas abarca los módulos principales del proyecto:
*   **Módulo de Taller Mecánico (Backend):** Gestión de Vehículos, Citas, Órdenes de Trabajo, Catálogo de Marcas/Modelos y seguimiento de estados.
*   **Portal de Clientes (Frontend/Sitio Web):** Panel "Mi Cuenta" para visualización de vehículos, agendamiento de citas, trazabilidad de órdenes, e historial de facturación.
*   **Comercio Electrónico (eCommerce):** Flujo de compra de repuestos en línea.
*   **Facturación Electrónica (Integración SRI):** Generación de XML, firma electrónica (XAdES-BES), transmisión al entorno de Pruebas del SRI, y descarga de comprobantes (PDF y XML).

*Fuera del alcance:* Pruebas de estrés masivo (rendimiento bajo concurrencia extrema) y pruebas de penetración de seguridad a nivel de servidor.

## 3. Funcionalidades a Evaluar
Las pruebas se centrarán en los siguientes flujos de negocio:
1.  **Registro y Autenticación:** Registro de clientes en el portal web y creación automática del contacto en el backend.
2.  **Gestión de Vehículos (Portal):** Creación de nuevos vehículos, subida de foto, edición de datos y eliminación (con bloqueo si el vehículo posee historial activo).
3.  **Agendamiento de Citas:** Solicitud de citas en el portal con validación de reglas de negocio (horarios de atención y prevención de cruces/solapamientos de horario).
4.  **Flujo de Órdenes de Trabajo:** Ciclo de vida de la orden de trabajo (Recepción -> Diagnóstico -> Reparación -> Listo -> Entregado), incluyendo la adición de servicios y repuestos al presupuesto.
5.  **Facturación Electrónica:** Generación de la factura desde la orden de trabajo o tienda en línea, validación de impuestos (IVA 0% y 15%), firma electrónica y recepción de autorización del SRI (sin errores de base de datos o estructura).
6.  **Trazabilidad:** Consulta del estado en tiempo real de la orden de trabajo mediante el número de placa o código desde el sitio web.

## 4. Tipos de Pruebas Seleccionadas
*   **Pruebas Funcionales (Caja Negra):** Verificación de que cada módulo realiza su función especificada en la interfaz de usuario.
*   **Pruebas de Integración:** Validación de la correcta comunicación entre los módulos internos (Ej: Orden de Trabajo -> Contabilidad -> Envío SRI).
*   **Pruebas de Usabilidad:** Comprobación del diseño responsivo y la accesibilidad de la interfaz del portal del cliente desde dispositivos de escritorio y simuladores móviles.
*   **Pruebas de Borde y Validaciones:** Comprobación de reglas estrictas de negocio (Ej: envío de facturas con rubros en $0.00, ingreso de fechas pasadas para citas, introducción de RUCs/Cédulas matemáticamente inválidas).

## 5. Responsables
*   **Líder de Calidad / QA Tester:** [Nombre del Evaluador / Tu Nombre] - Encargado de ejecutar los casos de prueba, reportar errores y documentar los resultados.
*   **Desarrollador / Administrador Odoo:** Responsable de aplicar parches y corregir las incidencias detectadas en los flujos o controladores de Python/QWeb.

## 6. Datos de Prueba
Para la ejecución se utilizará el siguiente conjunto de datos simulados:
*   **Usuarios de Portal:**
    *   Cliente Natural (Cédula válida de 10 dígitos, ej: 2100941414).
    *   Cliente Empresa / RUC (13 dígitos válidos).
    *   Consumidor Final (9999999999999).
*   **Vehículos:** Placas con formato ecuatoriano (ej. ABC-1234, Pichincha).
*   **Catálogo de Productos:** 
    *   Repuestos (Bienes) con IVA 15%.
    *   Servicios de mano de obra.
*   **Credenciales SRI (Pruebas):** Archivo `.p12` válido de pruebas del Banco Central o de la entidad certificadora, con su respectiva contraseña. RUC del emisor configurado en los ajustes de compañía de Odoo.

## 7. Entorno Utilizado
*   **Infraestructura:** Contenedores Podman/Docker.
*   **Servidor de Base de Datos:** PostgreSQL 15+.
*   **ERP:** Odoo 18.0 Community Edition.
*   **Sistema Operativo Host:** Linux.
*   **Navegadores de prueba:** Google Chrome, Mozilla Firefox, Safari (Últimas versiones).

## 8. Herramientas Aplicadas
*   **Entorno de Odoo 18:** Para la interfaz de usuario y configuraciones maestras.
*   **Terminal (Logs):** Uso de comandos del sistema de contenedores para monitorear trazas del servidor (Stacktraces, errores HTTP 500) en tiempo real.
*   **Cliente SQL (psql):** Para consultas directas a la base de datos (verificación de actualización de estados y consistencia).
*   **Herramientas para Desarrolladores del Navegador:** Consola y pestaña "Red" (Network) para monitorear solicitudes y depurar bloqueos en el portal web.

## 9. Criterios de Aceptación
Para considerar el proyecto como exitoso, el sistema debe cumplir con los siguientes criterios al finalizar la etapa de pruebas:
1.  **Cero Errores Críticos (Bloqueantes):** El flujo principal de negocio (Cliente agenda cita -> Taller genera orden -> Taller factura electrónicamente) debe poder completarse de principio a fin sin excepciones de servidor (Tracebacks).
2.  **Autorización SRI Exitosa:** Al menos el 95% de las facturas generadas correctamente deben recibir el estado `Autorizado` por parte del ambiente de Pruebas del SRI, o en su defecto, mostrar errores legibles al usuario si los datos de prueba fueron introducidos de manera incorrecta intencionalmente.
3.  **Seguridad y Restricciones:** Los usuarios del portal no pueden acceder a datos de otros clientes (vehículos, citas, facturas) mediante manipulación de URLs.
4.  **Integridad Interfaz:** El portal debe aplicar los estilos correctamente y los botones de acción (Editar, Eliminar Vehículo, Descargar PDF) deben responder de manera visualmente amigable (Modales de Bootstrap) sin comportamientos duplicados o erróneos.
