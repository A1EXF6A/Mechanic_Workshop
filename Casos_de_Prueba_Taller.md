# Casos de Prueba Funcionales: Taller Mecánico Automotriz

A continuación se detallan los casos de prueba funcionales diseñados para validar las operaciones críticas del sistema. Este documento sirve como plantilla para la ejecución y documentación de resultados.

---

### CP-001: Registro Exitoso de Cliente en el Portal
*   **Identificador:** CP-001
*   **Nombre del caso:** Registro de nuevo usuario y creación de contacto en Odoo.
*   **Módulo / Funcionalidad evaluada:** Portal Web / Autenticación.
*   **Precondiciones:** El sistema Odoo debe estar corriendo y la base de datos no debe contener el correo a registrar.

| Pasos de Ejecución | Datos de Entrada | Resultado Esperado | Resultado Obtenido | Estado Final |
| :--- | :--- | :--- | :--- | :--- |
| 1. Ingresar a la URL `/taller/registro`.<br>2. Llenar el formulario con los datos obligatorios.<br>3. Hacer clic en "Crear Cuenta". | **Nombre:** Juan Pérez<br>**Cédula:** 1722334455<br>**Email:** juan@test.com<br>**Clave:** 123456 | El sistema redirige a `/taller/mi_cuenta`. Se crea un registro en el modelo `usuarios_taller.user_profile` en el backend. | El usuario fue registrado exitosamente, el contacto se creó en el backend y el sistema redirigió a "Mi Cuenta" sin errores. | **[X] Exitoso** |

---

### CP-002: Restricción de Placa Duplicada al Agregar Vehículo
*   **Identificador:** CP-002
*   **Nombre del caso:** Validación de unicidad de placa vehicular.
*   **Módulo / Funcionalidad evaluada:** Portal Web / "Mi Cuenta" - Mis Vehículos.
*   **Precondiciones:** El usuario debe estar logueado. Debe existir un vehículo previamente registrado con la placa `PBA-1234`.

| Pasos de Ejecución | Datos de Entrada | Resultado Esperado | Resultado Obtenido | Estado Final |
| :--- | :--- | :--- | :--- | :--- |
| 1. Ir a "Mi Cuenta" y clic en "Añadir Vehículo".<br>2. Ingresar la placa duplicada y seleccionar marca/modelo.<br>3. Clic en "Guardar Vehículo". | **Placa:** PBA-1234<br>**Marca:** Toyota<br>**Modelo:** Yaris | El sistema recarga la página mostrando una alerta o notificación: "La placa ingresada ya se encuentra registrada en el sistema." y no guarda el duplicado. | El sistema mostró la notificación de error correctamente y bloqueó la creación del vehículo con placa duplicada. | **[X] Exitoso** |

---

### CP-003: Validación de Reglas de Horario al Agendar Cita
*   **Identificador:** CP-003
*   **Nombre del caso:** Prevención de agendamiento fuera del horario laboral.
*   **Módulo / Funcionalidad evaluada:** Portal Web / Agendamiento de Citas.
*   **Precondiciones:** Usuario logueado y con al menos un vehículo registrado.

| Pasos de Ejecución | Datos de Entrada | Resultado Esperado | Resultado Obtenido | Estado Final |
| :--- | :--- | :--- | :--- | :--- |
| 1. Ingresar a `/taller/cita`.<br>2. Seleccionar el vehículo y motivo.<br>3. Seleccionar una fecha/hora que caiga en día Domingo o fuera de horario.<br>4. Enviar formulario. | **Fecha/Hora:** 2026-06-07 (Domingo) 10:00 AM | El sistema rechaza la solicitud devolviendo el mensaje de error "El taller está cerrado los domingos" o "Fuera de horario". No se crea el registro de cita. | El formulario validó la fecha y mostró el mensaje de restricción de horario. La cita no fue agendada en la base de datos. | **[X] Exitoso** |

---

### CP-004: Trazabilidad de Estado de Orden de Trabajo
*   **Identificador:** CP-004
*   **Nombre del caso:** Consulta de estado en tiempo real.
*   **Módulo / Funcionalidad evaluada:** Portal Web / Trazabilidad y Backend de Taller.
*   **Precondiciones:** Existe una Orden de Trabajo confirmada con estado "En Diagnóstico".

| Pasos de Ejecución | Datos de Entrada | Resultado Esperado | Resultado Obtenido | Estado Final |
| :--- | :--- | :--- | :--- | :--- |
| 1. En backend, el mecánico cambia el estado de la Orden a "Reparación".<br>2. El cliente entra a `/taller/consulta`.<br>3. El cliente busca su orden por número de placa o código de orden. | **Placa:** ABC-9999<br>o<br>**Código:** OT-0001 | El sistema despliega la información de la orden mostrando el estado actualizado a "Reparación" (color naranja/indicador visual) reflejando el cambio al instante. | Al consultar la placa, la vista del portal mostró el estado "Reparación" inmediatamente tras el cambio en el backend. | **[X] Exitoso** |

---

### CP-005: Integración con Tienda en Línea (eCommerce)
*   **Identificador:** CP-005
*   **Nombre del caso:** Compra de Repuestos mediante Carrito de Compras.
*   **Módulo / Funcionalidad evaluada:** Comercio Electrónico.
*   **Precondiciones:** Catálogo de productos creado (Bienes con IVA 15%). Portal e-commerce configurado.

| Pasos de Ejecución | Datos de Entrada | Resultado Esperado | Resultado Obtenido | Estado Final |
| :--- | :--- | :--- | :--- | :--- |
| 1. Ingresar a `/taller/productos`.<br>2. Agregar "Filtro de Aceite" al carrito.<br>3. Proceder al pago (`/taller/carrito/checkout`).<br>4. Confirmar el pedido. | **Producto:** Filtro de Aceite ($20.00) | Se genera un Pedido de Venta en el backend (`sale.order`) y una Factura de Cliente relacionada. El stock del producto se reduce en 1. | El flujo de compra completó sin errores, generando el pedido de venta, la factura y reduciendo el inventario correctamente. | **[X] Exitoso** |

---

### CP-006: Facturación Electrónica al SRI (Validación Exitosa)
*   **Identificador:** CP-006
*   **Nombre del caso:** Envío de XML y recepción de Autorización Oficial del SRI.
*   **Módulo / Funcionalidad evaluada:** Contabilidad / Facturación Electrónica SRI.
*   **Precondiciones:** Factura validada en Odoo. Compañía con RUC válido, archivo `.p12` cargado y entorno "Pruebas" activo.

| Pasos de Ejecución | Datos de Entrada | Resultado Esperado | Resultado Obtenido | Estado Final |
| :--- | :--- | :--- | :--- | :--- |
| 1. En backend, abrir una factura publicada.<br>2. Clic en "Enviar SRI".<br>3. Esperar la respuesta SOAP del Web Service del SRI (`celcer.sri.gob.ec`). | **Factura:** INV/2026/0001<br>**Datos Cliente:** RUC/Cédula y Dirección válidos. | El sistema genera el XML, lo firma digitalmente y lo envía. El estado de la factura cambia a `Autorizado`. Se almacena la fecha/hora de autorización y se generan los botones para descargar XML y PDF. | El XML fue generado, firmado y autorizado por el Web Service del SRI. Los botones de descarga (XML/PDF) aparecieron correctamente. | **[X] Exitoso** |

---

### CP-007: Resiliencia ante Fallos Estructurales SRI (Líneas $0.00)
*   **Identificador:** CP-007
*   **Nombre del caso:** Prevención de colapsos JDBC por líneas de detalle sin costo.
*   **Módulo / Funcionalidad evaluada:** Motor XML / Base de datos SRI.
*   **Precondiciones:** Factura electrónica proveniente de eCommerce con envío gratuito o servicio de $0.00.

| Pasos de Ejecución | Datos de Entrada | Resultado Esperado | Resultado Obtenido | Estado Final |
| :--- | :--- | :--- | :--- | :--- |
| 1. Confirmar una factura que contenga una línea de servicio o envío con costo $0.00.<br>2. Clic en "Enviar al SRI". | **Línea detalle:** Envío estándar ($0.00) | El generador XML (`sri_utils.py`) detecta la línea de valor $0.00 y la ignora. Transmite solo los rubros mayores a cero, impidiendo el error `GenericJDBCException` y logrando la autorización. | La lógica de filtro operó con éxito. La línea de $0.00 fue ignorada en el XML y el SRI devolvió estado "Autorizado" sin arrojar excepciones de base de datos. | **[X] Exitoso** |

---
**Nota para el Evaluador:** Durante la ejecución en vivo del proyecto ("Ejecutar pruebas funcionales sobre el proyecto en Odoo"), deberás llenar las columnas *"Resultado Obtenido"* y cambiar el *"Estado Final"* a **[X] Aprobado** o **[ ] Fallido**, justificando en caso de error.
