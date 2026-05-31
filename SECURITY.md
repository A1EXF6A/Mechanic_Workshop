# Políticas y Prácticas de Seguridad - Terrabyte EC

En **Terrabyte EC**, consideramos que la seguridad de los datos de nuestros clientes, los registros de vehículos y la integridad de las transacciones financieras y contables son una prioridad absoluta.

Este documento establece las políticas de seguridad del proyecto, los canales para reportar vulnerabilidades y los estándares de seguridad aplicados en la configuración de la infraestructura y el código de Odoo.

---

## 1. Política de seguridad

Nuestra política de seguridad de software se enfoca en proteger activamente la confidencialidad, disponibilidad e integridad de los datos de Terrabyte EC.

### Versiones de Software Soportadas
Solo brindamos soporte de seguridad y parches activos a las ramas especificadas a continuación:

| Rama / Versión | Estado de Soporte | Notas |
| :--- | :--- | :--- |
| **`main` (v1.0.x)** | ✅ Soportado activamente | Versión actual de Odoo 18 en producción. |
| **`develop`** | ⚠️ Parches intermedios | Rama de desarrollo integrada con las últimas características; no recomendada para producción directa. |
| **Versiones anteriores** | ❌ No soportadas | Cualquier rama anterior se considera obsoleta. |

---

## 2. Reporte de vulnerabilidades

Si descubre una vulnerabilidad de seguridad en nuestro sistema, le agradecemos encarecidamente que **no la divulgue de manera pública**. Siga nuestro proceso de divulgación responsable:

1. **Envío del Reporte:** Envíe un correo electrónico detallado a **seguridad@terrabyteec.com** con el asunto `[VULNERABILITY] <Breve Descripción>`.
2. **Contenido Requerido:**
   - Una descripción clara del tipo de vulnerabilidad (ej: Inyección SQL, Cross-Site Scripting, Elevación de privilegios).
   - Pasos detallados para reproducir el fallo (código de prueba, capturas de pantalla o peticiones HTTP).
   - El impacto potencial para la infraestructura o datos de Terrabyte EC.
3. **Plazos de Respuesta:**
   - Confirmación de recepción: Menos de **48 horas**.
   - Evaluación inicial y plan de mitigación: Menos de **7 días hábiles**.
   - Solución definitiva (Hotfix) y publicación del parche: Máximo **30 días**, dependiendo de la complejidad de la vulnerabilidad.

---

## 3. Gestión de dependencias

Para evitar la introducción de vulnerabilidades a través de bibliotecas de terceros (ataques de cadena de suministro), adoptamos las siguientes medidas:

- **Imágenes Docker Oficiales:** Usamos exclusivamente imágenes oficiales firmadas de Odoo (`odoo:18`) y PostgreSQL (`postgres:18-alpine` o `postgres:15`) provenientes de registros de confianza de Docker Hub.
- **Lints y Análisis de Código Python:** Empleamos herramientas de análisis estático (como `bandit`) en nuestros submódulos de integración para identificar vulnerabilidades comunes en el código Python de Odoo.
- **Bibliotecas Criptográficas:** Para la firma electrónica del SRI (`xades_bes_sri_ec`), nos apoyamos firmemente en bibliotecas estándar y robustas del ecosistema de Python (`cryptography` y `lxml`), garantizando actualizaciones de seguridad fluidas desde los repositorios de paquetes del host.

---

## 4. Buenas prácticas de seguridad en Odoo

El ORM de Odoo proporciona mecanismos de defensa nativos extremadamente fuertes. En el proyecto de **Terrabyte EC**, los implementamos de la siguiente forma:

- **Prevención de Inyección SQL:**
  - Queda terminantemente prohibido concatenar variables del usuario en sentencias SQL utilizando `self.env.cr.execute()`.
  - *Mal ejemplo (Prohibido):* `self.env.cr.execute("SELECT * FROM res_partner WHERE name = '%s'" % user_input)`
  - *Buen ejemplo (Correcto):* Use siempre el ORM: `self.env['res.partner'].search([('name', '=', user_input)])`. Si una consulta cruda es obligatoria, use parámetros sanitizados: `self.env.cr.execute("SELECT * FROM res_partner WHERE name = %s", (user_input,))`.
- **Validación Estricta de Entradas (Sanitización):**
  - Los datos ingresados en el portal web (como cédulas o emails) son validados mediante expresiones regulares robustas en el backend de Python antes de guardarse en base de datos (conforme se programó en `user_profile.py`).
- **Seguridad a Nivel de Registro (Row-Level Security):**
  - Se estructuraron Reglas de Registro (`ir.rule`) estrictas en `taller_security.xml` para asegurar que los usuarios del portal (Clientes) bajo ninguna circunstancia puedan leer ni modificar datos de vehículos, citas u órdenes que no les pertenezcan, y que los mecánicos (Técnicos) solo visualicen sus tareas asignadas.

---

## 5. Seguridad en PostgreSQL

La base de datos PostgreSQL contiene toda la información de negocio crítica de Terrabyte EC. Su configuración de seguridad incluye:

- **Aislamiento de Red:** El contenedor de la base de datos `db` está ubicado exclusivamente en la red privada `app` con el modificador `internal: true`. No se expone ningún puerto hacia el host o el exterior (no se define la directiva `ports` en el compose para `db`). Solo la instancia de Odoo puede comunicarse con ella.
- **Credenciales Seguras:** El usuario administrador de Odoo se conecta mediante contraseñas complejas definidas dinámicamente mediante variables de entorno `.env` en producción.
- **Parámetros del Sistema Operativo en Docker:**
  - El contenedor de PostgreSQL corre con la opción de seguridad `security_opt: - no-new-privileges:true` activada, impidiendo que procesos internos ganen privilegios de root sobre el contenedor.
  - Se imponen límites físicos de rendimiento (`mem_limit: 1g`, `cpus: 1.0`, y `pids_limit: 256`) para mitigar ataques de denegación de servicio (DoS) por saturación de base de datos.

---

## 6. Buenas prácticas generales de seguridad

1. **Gestión del Certificado de Firma SRI:**
   - La contraseña y el archivo `.p12` de la firma electrónica del SRI se guardan encriptados en base de datos a través de los campos estándar de Odoo. Evite a toda costa guardar la contraseña de la firma en código duro (`hardcoded`) dentro del módulo o en comentarios XML.
2. **Desactivación de Modo Desarrollador en Producción:**
   - El modo de depuración (`debug=1` o `debug=assets`) debe desactivarse en producción para mitigar la fuga de información sobre la estructura interna de los modelos o variables en las respuestas HTTP de Odoo.
3. **Control del Proxy Inverso (Nginx):**
   - El proxy inverso de Nginx (`odoo-proxy`) actúa como cortafuegos perimetral, bloqueando solicitudes directas al puerto `8069` de Odoo y forzando la seguridad de las cabeceras HTTP (deshabilitando métodos innecesarios y previniendo el clickjacking).
4. **Política de Contraseñas Técnicas:**
   - La automatización de creación de usuarios para ingenieros mecánicos (`hr_employee.py`) asigna una contraseña inicial fuerte (`Autologic2026!`). Se exige a los usuarios cambiar esta credencial en su primer inicio de sesión a través del portal.
