# 📝 Changelog - Terrabyte EC (Odoo 18 Mechanic Workshop)

Todos los cambios notables en este proyecto serán documentados en este archivo.

El formato está basado en [Keep a Changelog](https://keepachangelog.com/es-ES/1.1.0/) y este proyecto se adhiere a [Versionamiento Semántico](https://semver.org/spec/v2.0.0.html).

---

## [1.0.0] - 2026-05-31

Este es el lanzamiento inicial del **Sistema de Gestión de Taller Mecánico Automotriz** para **Terrabyte EC**, consolidando toda la suite operativa y la integración fiscal con el SRI de Ecuador en Odoo 18.

### Added ➕
- **Core de Taller Mecánico (`taller_mecanico`):**
  - Modelo `taller.vehiculo` para el registro técnico de autos (placas únicas, combustible, año de fabricación y kilometraje).
  - Modelo `taller.cita` para la agenda y control de turnos en el taller con alertas de solapamiento de horarios en backend.
  - Modelo `taller.orden.trabajo` con soporte para checklists de recepción (gasolina, herramientas, golpes, gata) y desglose de servicios prestados e insumos utilizados.
  - Sincronización en tiempo real de Marcas (`taller.marca`) y Modelos (`taller.modelo`) mediante consumo de la **API de NHTSA** (EE. UU.) con filtrado inteligente de marcas populares.
  - Asistente wizard interactivo `taller.marca.buscar.wizard` para buscar y agregar marcas de forma selectiva desde la API.
  - Triggers automáticos por correo electrónico: notificación HTML al cliente al confirmar una cita y breakdown completo de costos cuando el vehículo se marca como "Listo para Retirar".
- **Integración Fiscal Ecuatoriana (SRI Offline Billing):**
  - Generación dinámica de XML estructurado bajo el esquema oficial de facturación SRI v2.1.0.
  - Algoritmo para calcular el Dígito Verificador Módulo 11 para la Clave de Acceso de 49 dígitos.
  - Firma digital en formato **XAdES-BES** integrada en memoria usando bibliotecas criptográficas de Python y certificados `.p12`.
  - Transmisión síncrona mediante protocolos SOAP con reintentos automáticos ante latencia hacia los endpoints SRI de Recepción y Autorización.
  - Envío automático de correo con la representación impresa de la factura en **PDF** y el archivo original **XML** autorizado adjuntos.
- **Módulo de Perfiles de Usuario (`usuarios_taller`):**
  - Registro seguro de clientes con validación estricta de cédula de identidad ecuatoriana única, celular con solo dígitos y edad mínima de 18 años.
  - Sincronización automática bidireccional de datos con los contactos oficiales de Odoo (`res.partner`).
- **Módulo Técnico (`taller_mecanico_tecnico`):**
  - Vista adaptada para mecánicos que restringe el acceso de forma que solo puedan visualizar y operar sobre sus órdenes de trabajo asignadas.
  - Smart Button en la ficha del empleado (`hr.employee`) para auditar la cantidad de órdenes a su cargo.
  - Automatización del alta de empleados: creación inmediata de usuarios Odoo (`res.users`) con el rol de técnico (`group_taller_technician`) y contraseña por defecto al pertenecer al área operativa.
- **Módulo Administrativo y Dashboard SRI (`taller_mecanico_admin`):**
  - SRI Dashboard contable para el monitoreo en tiempo real de facturas en estado autorizado, rechazado, borrador y en proceso.
  - Descarga masiva en bloque ZIP de archivos XML autorizados para conciliaciones tributarias simplificadas.
  - Reporte QWeb personalizado e impreso para facturas con clave de acceso SRI integrada.
- **Módulo de Portal y E-commerce (`taller_mecanico_portal`):**
  - Portal de clientes "Mi Cuenta" para visualización histórica de vehículos, citas y estados de reparación.
  - Agenda pública de citas web en `/taller/cita` con validación interactiva de disponibilidad y choques.
  - E-commerce optimizado (`/taller/productos`) con filtros por categoría, promociones, novedades y validación en tiempo real de stock físico en bodegas.
- **Configuración de Infraestructura y Despliegue:**
  - Contenedor proxy Nginx configurado para Odoo con políticas de seguridad estrictas.
  - Archivo `docker-compose.yml` parametrizado con variables de entorno optimizadas para entornos Windows y Linux (con soporte para políticas SELinux mediante modificador `:Z`).
  - Archivo de configuración operativa `config/odoo.conf` parametrizado con limitaciones de memoria y tiempos de ejecución.
  - Colección de datos base reales en formato CSV en `data_import/` conteniendo 30+ registros por módulo (clientes, proveedores, repuestos, empleados, órdenes).

### Changed
- Reemplazado el archivo básico `README.md` original por una versión exhaustiva y profesional detallando el ecosistema tecnológico de Terrabyte EC.

### Fixed
- Corregida la latencia de respuesta en la verificación del SRI implementando un bucle controlado de espera de 2.5 segundos con un máximo de 4 intentos en el backend contable.

### Removed
- Eliminadas referencias de prueba locales que causaban colisiones con el módulo estándar de Enterprise en la configuración del docker-compose.
