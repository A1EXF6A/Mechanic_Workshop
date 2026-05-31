# Documentación de referencia de módulos personalizados - Terrabyte EC

Esta documentación describe detalladamente cada uno de los módulos de Odoo personalizados que conforman el **Sistema de Gestión de Taller Mecánico** para **Terrabyte EC**.

---

## 1. Módulo: `usuarios_taller`

### Propósito
Establecer un sistema seguro para el registro de clientes del taller en Ecuador, aplicando validaciones obligatorias que garantizan la integridad de la base de datos antes de transferir la información al directorio principal de contactos de Odoo.

### Dependencias
- `base` (Módulo raíz de Odoo)

### Modelos
- **`usuarios_taller.user_profile` (Ficha de Usuario Taller):**
  - Representa el perfil del usuario del portal del taller.
  - *Campos principales:*
    - `cedula` (Char, Requerido, Único): Documento nacional de identidad.
    - `nombre` (Char, Requerido).
    - `apellido` (Char, Requerido).
    - `email` (Char, Requerido): Valida formato de correo mediante expresión regular.
    - `direccion` (Char, Requerido).
    - `password` (Char, Requerido).
    - `celular` (Char, Requerido): Valida que contenga únicamente números.
    - `edad` (Integer, Requerido): Valida que sea estrictamente mayor o igual a 18 años.
    - `display_name_full` (Char, Computado): Concatenación del nombre y apellido.
    - `partner_id` (Many2one, res.partner, Readonly): Contacto vinculado automáticamente en Odoo.

### Triggers y automatizaciones
- **Sincronización `create` / `write`:** Al crear o modificar un registro en `usuarios_taller.user_profile`, el sistema crea o actualiza automáticamente un registro coincidente en `res.partner` (sincronizando campos como `name`, `email`, `phone`, `street` y `vat`), asegurando compatibilidad nativa con la facturación y ventas de Odoo.

### Permisos
- **ir.model.access.csv:**
  - El grupo `base.group_system` (Administradores del sistema) tiene control total CRUD sobre el modelo `usuarios_taller.user_profile`.

### Vistas
- **`views/user_profile_views.xml`:** Define la vista lista y el formulario backend para auditar los perfiles registrados desde la web.

---

## 2. Módulo: `taller_mecanico` (Core)

### Propósito
Encapsular toda la lógica de negocio central del taller. Administra la flota de vehículos de clientes, controla la asignación e historial de citas, gestiona las hojas de ruta y checklists de reparación, y coordina la integración externa con la NHTSA (EE. UU.) y la facturación electrónica del SRI (Ecuador).

### Dependencias
- `stock`, `sale`, `account`, `usuarios_taller`, `contacts`, `hr`, `mail`, `payment_stripe`, `payment_paypal`

### Models
- **`taller.vehiculo` (Ficha del Vehículo):**
  - Almacena la hoja de ruta física de cada automóvil.
  - *Campos principales:* `placa` (Char, Único), `propietario_id` (`usuarios_taller.user_profile`), `marca_id` (`taller.marca`), `modelo_id` (`taller.modelo`), `anio` (Integer, validado entre 1851 y año actual), `color` (Char), `kilometraje` (Integer), `tipo_combustible` (Selection), `foto` (Image) e `historial_servicio_ids` (One2many taller.orden.trabajo).
- **`taller.cita` (Cita de Servicio):**
  - Agenda de turnos. Vinculado al chatter de Odoo para rastreo de actividad.
  - *Campos principales:* `vehiculo_id`, `cliente_id`, `fecha_cita` (Datetime), `fecha_fin` (Computado, fecha_cita + 1 hora), `motivo` (Selection), `descripcion` (Text), `prioridad` (Selection), `estado` ("solicitada", "confirmada", "cancelada") e `orden_trabajo_id` (`taller.orden.trabajo`).
  - *Acciones:* `action_confirmar` y `action_cancelar`.
- **`taller.orden.trabajo` (Orden de Trabajo):**
  - Hoja de servicio del mecánico. Vinculada a chatter.
  - *Campos principales:* `name` (Código autogenerado), `vehiculo_id`, `cita_id`, `tecnico_id` (`hr.employee`), `fecha_ingreso` (Datetime), `diagnostico` (Text), `servicio_linea_ids` (`taller.orden.linea.servicio`), `repuesto_linea_ids` (`taller.orden.linea.repuesto`), `costo_mano_obra` (Float), `costo_total_servicios` (Float), `costo_total_repuestos` (Float), `costo_total_general` (Float, Computado), `estado` ("recibido", "listo", "entregado"), `nivel_gasolina` (Selection), `llanta_repuesto` (Boolean), `herramientas` (Boolean), `gata` (Boolean), `rayones_golpes` (Text), `objetos_personales` (Text), `factura_id` (`account.move`), `kilometraje` e historial de próximo mantenimiento (`proximo_kilometraje_mto` y `proxima_fecha_mto`).
  - *Acciones:* `action_listo` (valida insumos, actualiza kilometraje del auto y despacha correo HTML), `action_facturar` (genera factura contable a partir de repuestos y servicios) y `action_ver_factura`.
- **`taller.orden.linea.servicio` y `taller.orden.linea.repuesto`:**
  - Líneas de detalle asociadas a productos tipo servicio o storable de Odoo.
- **`taller.marca` y `taller.modelo`:**
  - Tablas de marcas y modelos automotrices integradas con API NHTSA para importación y sincronización dinámica.
- **`taller.marca.buscar.wizard`:**
  - Transient model para buscar marcas de forma interactiva.
- **`account.move` (Extensión SRI Ecuador):**
  - Extiende el diario de facturas de Odoo con campos tributarios: `sri_clave_acceso`, `sri_estado_autorizacion` ("borrador", "enviado", "autorizado", "rechazado"), `sri_fecha_autorizacion` (Datetime) y adjuntos XML oficiales (`sri_xml_file` y `sri_xml_filename`).
  - *Acciones:* Sobrescribe `action_post()` para automatizar el envío al SRI y define `action_enviar_sri()`, `_send_sri_invoice_email()` y `action_descargar_xml_masivo()`.

### Triggers y Automatizaciones
- **Auto-Creación de Orden:** La creación exitosa de una cita (`taller.cita`) genera inmediatamente una orden de trabajo (`taller.orden.trabajo`) en estado "Recibido" con diagnóstico base pre-cargado.

### Permissions
- **ir.model.access.csv:**
  - El grupo `group_taller_manager` (Administrador) posee permisos CRUD totales sobre marcas, modelos, vehículos, citas, órdenes y asistentes.
  - El grupo `group_taller_technician` (Técnicos) posee permisos de lectura general, y escritura/creación exclusiva sobre vehículos y órdenes de trabajo (restringido por reglas de registro).
  - El grupo `group_taller_customer` (Clientes Portal) posee permisos de lectura sobre marcas y modelos, y acceso restringido a sus vehículos, citas y órdenes.
- **taller_security.xml (Record Rules):**
  - Restricciones basadas en dominio para que el cliente solo visualice información vinculada a su `partner_id` y el mecánico visualice únicamente las órdenes asignadas a su perfil técnico.

### Views
- **`views/vehiculo_views.xml`:** Kanban interactivo para visualizar vehículos con imagen y especificaciones.
- **`views/orden_trabajo_views.xml`:** Formulario completo para control técnico.
- **`views/cita_taller_views.xml`:** Lista y formulario de agenda.
- **`views/menus.xml`:** Estructura jerárquica del backend.

---

## 3. Módulo: `taller_mecanico_tecnico`

### Propósito
Facilitar la operación cotidiana de los mecánicos de Terrabyte EC proporcionándoles vistas simplificadas y automatizando la creación de sus usuarios del sistema en Odoo cuando se registra su ingreso laboral en recursos humanos.

### Dependencias
- `taller_mecanico`, `hr`

### Models
- **`hr.employee` (Extensión Técnico):**
  - Incorpora el conteo de órdenes de trabajo asociadas (`orden_trabajo_count`).
  - *Acciones:* `action_view_ordenes_trabajo` para abrir el listado de reparaciones pendientes del mecánico por Smart Button.

### Triggers y Automatizaciones
- **Autoprovisionamiento de Cuentas (Mecánicos):** Al crear un empleado (`hr.employee`) en Odoo con un cargo u oficina asociada al taller (verificando palabras clave como "mecanico", "tecnico", "taller", "bodega") y que posea un correo válido corporativo, el sistema **crea automáticamente un usuario de Odoo (`res.users`)**, le asigna la contraseña inicial segura (`Autologic2026!`) y le otorga de forma predeterminada el rol operativo `group_taller_technician`, permitiéndole iniciar sesión de inmediato.

### Views
- **`views/tecnico_menus.xml`:** Inyección visual de Smart Buttons en la ficha del empleado y creación del menú simplificado "Mi Perfil" para técnicos.

---

## 4. Módulo: `taller_mecanico_admin`

### Propósito
Centralizar las tareas contables, de facturación y cumplimiento tributario ante el SRI de Ecuador.

### Dependencias
- `taller_mecanico`

### Views
- **`views/res_company_views.xml`:** Pestaña "SRI Ecuador" en los ajustes de compañía para que el administrador suba el archivo binario de la firma `.p12`, digite la contraseña y configure el entorno de ejecución (pruebas o producción).
- **`views/sri_dashboard_views.xml`:** Panel de control con gráficos interactivos y métricas de estados de facturación electrónica.
- **`views/account_move_views.xml`:** Vistas de factura extendidas con campos SRI y botones de acción manuales.
- **`views/report_invoice_sri.xml`:** Plantilla impresa en formato PDF oficial de Odoo que inyecta la clave de acceso de 49 dígitos para su lectura física.

---

## 5. Módulo: `taller_mecanico_portal`

### Propósito
Implementar la interfaz web pública de cara al cliente final, habilitando registros de cuenta seguros, cotizaciones de citas con validador dinámico de choques y una tienda en línea optimizada de repuestos con control de inventarios.

### Dependencies
- `taller_mecanico`, `website`, `website_sale`, `usuarios_taller`

### Controllers (Rutas HTTP)
- **`controllers/main.py` (Controlador Core):**
  - `/taller/mi_cuenta`: Dashboard del cliente mostrando vehículos, citas, órdenes activas y facturas descargables.
  - `/taller/consulta` (GET/POST): Consulta interactiva pública del estado del vehículo mediante placa.
  - `/taller/cita` y `/taller/cita/submit`: Formulario y controlador de agenda web.
  - `/taller/cita/check_availability` (JSON API): Endpoint dinámico para consultar si un horario está ocupado en tiempo real.
  - `/taller/login` / `/taller/registro`: Autenticación segura personalizada.
  - `/taller/factura/<id>/pdf` y `/taller/factura/<id>/xml`: Descargas de comprobantes fiscales.
- **`controllers/shop.py` (E-commerce Custom):**
  - `/taller/productos`: Catálogo dinámico de repuestos interactuando con stock físico en bodegas.
  - `/taller/carrito/agregar` / `/taller/carrito/actualizar`: Gestión de carrito de compras respetando máximos de stock disponibles.
  - `/taller/confirmar-compra`: Envía el carrito personalizado al motor nativo de Odoo para el checkout oficial.

### Views & Templates (Frontend QWeb)
- **`views/pages/`:** Contiene todas las plantillas QWeb estilizadas (`home.xml`, `servicios.xml`, `cita.xml`, `mi_cuenta.xml`, `login.xml`, etc.) que renderizan la interfaz interactiva.
