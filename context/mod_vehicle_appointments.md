# Especificación Técnica: Módulo Personalizado `taller_mecanico` (Odoo 18)

[cite_start]Este documento contiene las directrices de arquitectura, diseño de datos, reglas de negocio e interfaz para la generación automática de código del módulo personalizado de gestión para el **Grupo 5: Taller Mecánico Automotriz**[cite: 309, 310].

---

## 1. Configuración General del Módulo (`__manifest__.py`)
- **Nombre Técnico:** `taller_mecanico`
- **Versión:** `18.0.1.0.0`
- **Categoría:** `Services`
- [cite_start]**Dependencias Nativas:** `['base', 'contacts', 'hr', 'stock']` [cite: 99, 121]
- **Archivos de Datos a Cargar:**
  - [cite_start]`security/ir.model.access.csv` [cite: 117, 122]
  - [cite_start]`views/vehiculo_views.xml` [cite: 113]
  - `views/orden_trabajo_views.xml`
  - `views/cita_taller_views.xml`
  - [cite_start]`views/menus.xml` [cite: 114]

---

## 2. Convenciones de Código Obligatorias
- [cite_start]**Nomenclatura de Campos:** Estricto `snake_case` (ej. `fecha_ingreso`, `tipo_combustible`)[cite: 200]. [cite_start]No usar CamelCase ni mayúsculas[cite: 200].
- [cite_start]**Vistas de Lista:** En Odoo 18, la etiqueta raíz para vistas jerárquicas de lista es `<list>`, reemplazando la antigua etiqueta `<tree>`[cite: 14, 113].
- [cite_start]**Seguridad:** Bloquear accesos por defecto y definirlos explícitamente en el archivo `ir.model.access.csv` para el grupo `base.group_user`[cite: 117, 118, 122].

---

## 3. Arquitectura del Modelo de Datos (Python Models)

### [cite_start]Modelo 1: Vehículo del Cliente (`taller.vehiculo`) [cite: 310]
[cite_start]Ficha técnica y de identificación de los vehículos ingresados al taller[cite: 310].
- **Campos:**
  - [cite_start]`propietario_id` (`Many2one` -> `res.partner`): Propietario del vehículo[cite: 121, 310]. Relación obligatoria (`required=True`)[cite: 121].
  - [cite_start]`marca` (`Char`): Marca del auto (ej. Chevrolet, Toyota)[cite: 310].
  - [cite_start]`modelo` (`Char`): Modelo del auto (ej. Sail, Hilux)[cite: 310].
  - [cite_start]`anio` (`Integer`): Año de fabricación[cite: 310].
  - [cite_start]`placa` (`Char`): Identificador único del vehículo (Placa vehicular)[cite: 310].
  - [cite_start]`color` (`Char`): Color exterior[cite: 310].
  - [cite_start]`kilometraje` (`Integer`): Kilometraje actual[cite: 310].
  - [cite_start]`tipo_combustible` (`Selection`): Opciones: `gasolina` (Gasolina), `diesel` (Diésel), `hibrido` (Híbrido), `electrico` (Eléctrico)[cite: 310].
  - [cite_start]`foto` (`Binary`): Almacenamiento de imagen del auto[cite: 310].
  - [cite_start]`historial_servicio_ids` (`One2many` -> `taller.orden.trabajo`): Relación inversa que mapea todas las órdenes de trabajo asociadas a este vehículo[cite: 310].
- **Atributo Especial:** `_rec_name = 'placa'` para que al relacionar el vehículo en otros modelos se visualice la placa.

### [cite_start]Modelo 2: Orden de Trabajo (`taller.orden.trabajo`) [cite: 310]
[cite_start]Documento operativo que registra los servicios y componentes aplicados a un vehículo en reparación[cite: 310].
- **Campos:**
  - `name` (`Char`): Código correlativo único de la orden (ej. OT-0001). Autogenerado o por secuencia por defecto 'NUEVA'.
  - [cite_start]`vehiculo_id` (`Many2one` -> `taller.vehiculo`): Vehículo que ingresa a reparación[cite: 310]. Obligatorio.
  - [cite_start]`tecnico_id` (`Many2one` -> `hr.employee`): Mecánico responsable del servicio[cite: 121, 310].
  - [cite_start]`fecha_ingreso` (`Datetime`): Fecha y hora de entrada al taller[cite: 310]. Por defecto `now`.
  - [cite_start]`diagnostico` (`Text`): Reporte o síntomas iniciales detectados[cite: 310].
  - [cite_start]`servicio_ids` (`Many2many` -> `product.product`): Catálogo nativo de servicios realizados[cite: 121]. Filtrar en la vista con el dominio `[('type', '=', 'service')]`.
  - [cite_start]`repuesto_ids` (`Many2many` -> `product.product`): Catálogo nativo de repuestos o piezas de almacén consumidas[cite: 121, 310]. Filtrar en la vista con el dominio `[('type', '!=', 'service')]`.
  - [cite_start]`costo_mano_obra` (`Float`): Valor monetario del servicio técnico[cite: 310].
  - [cite_start]`estado` (`Selection`): Opciones de flujo de trabajo: `recibido` (Recibido), `proceso` (En Proceso), `listo` (Listo para entrega), `entregado` (Entregado al cliente)[cite: 310].

### Modelo 3: Cita de Taller (`taller.cita`)
[cite_start]Modelo propuesto por el grupo para agendar revisiones previas a la generación de una orden de trabajo[cite: 91, 125].
- **Campos:**
  - [cite_start]`cliente_id` (`Many2one` -> `res.partner`): Cliente que solicita la cita[cite: 121].
  - `vehiculo_id` (`Many2one` -> `taller.vehiculo`): Vehículo registrado. Aplicar dominio dinámico en vista: `[('propietario_id', '=', cliente_id)]` para mostrar solo los vehículos de ese cliente.
  - `fecha_cita` (`Datetime`): Fecha y hora agendada.
  - `motivo` (`Text`): Razón de la cita o descripción de la falla.
  - `estado` (`Selection`): `solicitada` (Solicitada), `confirmada` (Confirmada), `cancelada` (Cancelada).
  - `orden_trabajo_id` (`Many2one` -> `taller.orden.trabajo`): Enlace de trazabilidad si la cita pasa a convertirse en una reparación real.

---

## 4. Requisitos de Interfaz de Usuario (XML Views)

### [cite_start]Formulario de Vehículo (`taller.vehiculo`) [cite: 113, 119]
- Utilizar el widget `widget="image"` y la clase `oe_avatar` para el campo `foto` colocado en la parte superior izquierda.
- Organizar los datos de identificación y los datos técnicos en dos columnas usando etiquetas `<group>`.
- Agregar un componente `<notebook>` al final con una pestaña (`<page>`) titulada "Historial de Mantenimientos" para desplegar la lista de `historial_servicio_ids` en modo de solo lectura.

### [cite_start]Formulario de Orden de Trabajo (`taller.orden.trabajo`) [cite: 119]
- Colocar el campo `estado` en la parte superior derecha del formulario utilizando el componente de cabecera estándar de Odoo con el widget de barra de estado: `widget="statusbar"`.
- Utilizar pestañas desplegables (`<notebook>`) para separar limpiamente la sección de "Diagnóstico", el listado de "Servicios" y el listado de "Repuestos Utilizados".

### [cite_start]Menú de Navegación (`menus.xml`) [cite: 114, 120]
- [cite_start]**Menú Raíz:** "Taller Mecánico" (Visible en la barra principal de Odoo)[cite: 120].
- [cite_start]**Categoría Intermedia:** "Operaciones"[cite: 116].
- **Sub-Menús Finales:**
  - "Vehículos de Clientes" (Llama a la acción de `taller.vehiculo`).
  - "Órdenes de Trabajo" (Llama a la acción de `taller.orden.trabajo`).
  - "Citas de Revisión" (Llama a la acción de `taller.cita`).

---

## [cite_start]5. Archivo de Permisos Básicos (`security/ir.model.access.csv`) [cite: 117, 122]
[cite_start]Garantizar acceso CRUD total para el grupo base de usuarios de Odoo para pruebas de desarrollo[cite: 122]:
```csv
id,name,model_id:id,group_id:id,perm_read,perm_write,perm_create,perm_unlink
access_taller_vehiculo,taller.vehiculo,model_taller_vehiculo,base.group_user,1,1,1,1
access_taller_orden_trabajo,taller.orden.trabajo,model_taller_orden_trabajo,base.group_user,1,1,1,1
access_taller_cita,taller.cita,model_taller_cita,base.group_user,1,1,1,1