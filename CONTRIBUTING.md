# 🤝 Guía de Contribución para Terrabyte EC (Odoo 18)

¡Bienvenido al proyecto de desarrollo del **Sistema de Gestión de Taller Mecánico** para **Terrabyte EC**! Como equipo de ingeniería, nos regimos por los más altos estándares de calidad de software, diseño de arquitectura limpia y cumplimiento de estándares de desarrollo de Odoo.

Esta guía está diseñada para orientar a desarrolladores nuevos y experimentados en las políticas del repositorio, flujo de ramas, convenciones de commits y lineamientos técnicos para el desarrollo de módulos personalizados.

---

## 1. Flujo de Git adoptado 🔀

Para asegurar la estabilidad en producción y la velocidad en la entrega de nuevas características, adoptamos el flujo de trabajo **Gitflow**:

```text
  main       _____________________________________________________ (Producción Estable)
                               ^                          ^
                             [Merge]                    [Merge]
                               |                          |
  hotfix/                      |                  [hotfix/sri-connection-fix]
                               |                          ^
  develop    ____[Merge]_______|__________________________|______ (Línea Base de Dev)
                   ^                                 ^
                 [Merge]                           [Merge]
                   |                                 |
  feature/    [feature/api-nhtsa-sync]     [feature/sri-zip-download]
```

### Ramas principales
- **`main`:** Contiene únicamente código estable en producción. Cada cambio en esta rama debe estar exhaustivamente probado y etiquetado con una versión semántica (ej. `v1.0.0`, `v1.0.1`).
- **`develop`:** Línea de integración principal para el desarrollo. Es la rama base donde se unen las características terminadas. Debe compilar y pasar todas las pruebas automáticas en todo momento.

### Ramas Auxiliares
- **`feature/*`:** Ramas creadas para el desarrollo de nuevas características (ej: `feature/api-nhtsa-sync`). Se crean a partir de `develop` y se re-integran a ella mediante Pull Requests.
- **`hotfix/*`:** Ramas de emergencia destinadas a corregir errores críticos detectados directamente en producción (ej: `hotfix/sri-connection-error`). Se crean a partir de `main` y, una vez solucionado el problema, se integran de regreso tanto a `main` como a `develop`.

---

## 2. Convención de nombres de ramas

Las ramas deben nombrarse siguiendo un patrón claro y autodescriptivo que permita asociarlas inmediatamente a una tarea o issue:

```text
<tipo>/<ticket_id>-<breve_descripcion_en_ingles_o_espanol>
```

### Tipos Permitidos
- **`feature/`:** Nuevas características o extensiones.
  - *Ejemplo:* `feature/412-sri-zip-download`
- **`bugfix/`:** Corrección de errores que están en la rama `develop`.
  - *Ejemplo:* `bugfix/308-fix-validation-age`
- **`hotfix/`:** Corrección de fallos urgentes detectados directamente en producción.
  - *Ejemplo:* `hotfix/sri-xml-signing-error`
- **`docs/`:** Tareas exclusivas de redacción de documentación técnica.
  - *Ejemplo:* `docs/architecture-mermaid-update`
- **`refactor/`:** Reestructuración de código existente sin alterar su comportamiento externo.
  - *Ejemplo:* `refactor/sri-utils-cleanup`

---

## 3. Convención de commits

Adoptamos estrictamente la especificación de **Conventional Commits** para mantener un historial de cambios legible y facilitar la generación automatizada del archivo `CHANGELOG.md`.

### Estructura del Mensaje de Commit
```text
<tipo>(<alcance_opcional>): <descripcion_corta_en_imperativo>

[Cuerpo del commit detallando el "por qué", no el "cómo"]

[Pie del commit para indicar el ID del Ticket o cambios disruptivos]
```

### Tipos de commit aceptados
- **`feat`:** Incorporación de una nueva funcionalidad.
  - *Ejemplo:* `feat(portal): agregar validación automática para cédulas ecuatorianas`
- **`fix`:** Solución a un error o bug del sistema.
  - *Ejemplo:* `fix(core): corregir cálculo de zona horaria para citas del taller`
- **`docs`:** Modificaciones en documentación técnica, comentarios de código o docstrings.
  - *Ejemplo:* `docs(readme): actualizar instrucciones de despliegue para host Windows`
- **`refactor`:** Cambios en el código que no corrigen errores ni añaden funcionalidades.
  - *Ejemplo:* `refactor(sri): modularizar construcción del sobre SOAP XML en sri_utils`
- **`test`:** Creación, corrección o actualización de pruebas unitarias.
  - *Ejemplo:* `test(portal): añadir suite de pruebas para controladores de disponibilidad del taller`
- **`chore`:** Tareas auxiliares de mantenimiento de dependencias, scripts de construcción, etc.
  - *Ejemplo:* `chore(docker): actualizar versión de la imagen Nginx alpine en compose`

---

## 4. Proceso de Pull Requests (PR)

El paso de cambios de una rama auxiliar a una rama principal se realiza exclusivamente mediante Pull Requests controlados. Siga este proceso metódico:

1. **Sincronización:** Asegúrese de tener su rama local sincronizada y con rebase aplicado sobre la última versión de `develop`.
2. **Pruebas Locales:** Ejecute su código localmente. Valide que los contenedores de Odoo y PostgreSQL levanten correctamente sin arrojar excepciones de base de datos en los logs (`docker-compose logs -f odoo`).
3. **Creación del PR:** Abra el PR apuntando a `develop`. Utilice la plantilla estándar completando los campos:
   - **Descripción del Cambio:** Detalle qué resuelve y el impacto.
   - **Pasos para Reproducir / Probar:** Detalle cómo los evaluadores pueden comprobar el cambio.
   - **Checklist del Desarrollador:** Confirme que el código cumple con las guías de estilo, pruebas y seguridad.
4. **Validación del Pipeline (CI):** Si el repositorio cuenta con flujos automatizados de CI, verifique que los lints pasen correctamente.
5. **Asignación de Revisores:** Asigne al menos a dos revisores técnicos experimentados.

---

## 5. Checklist de revisión de código

Al revisar el código de un compañero de equipo, siga esta lista de verificación exhaustiva:

- [ ] **Funcionalidad:** ¿El cambio cumple exactamente con los requisitos especificados en la historia de usuario / ticket?
- [ ] **Estilo de Odoo:** ¿El código sigue los lineamientos oficiales de Odoo (nombres de modelos, herencias, decoradores de API)?
- [ ] **Seguridad (OWASP):** ¿Se evitan inyecciones de código SQL? (Uso estricto del ORM de Odoo, no consultas CRUD crudas en `self.env.cr.execute` a menos que sea inevitable y sanitizado).
- [ ] **Rendimiento de Base de Datos:** ¿Se evitan consultas en bucles (efecto N+1)? (Uso correcto de `mapped`, `filtered` e instrucciones batch en la medida de lo posible).
- [ ] **Manejo de Excepciones:** ¿Las integraciones externas (NHTSA API y SRI WS) están envueltas en bloques `try-except` orientados a fallos?
- [ ] **Traducciones e Internacionalización:** ¿Todos los textos visibles para el usuario en la UI backend o frontend utilizan marcas de traducción (ej: `string="Texto"` o `_("Mensaje")` en Python)?
- [ ] **Seguridad CSV:** ¿Se definieron correctamente las políticas de seguridad y lectura en `ir.model.access.csv` para cada nuevo modelo creado?

---

## 6. Estándares de desarrollo en Odoo

Para conservar la coherencia y mantenibilidad de la suite de software de **Terrabyte EC**, todo desarrollo debe seguir estos estándares estrictos de diseño de Odoo 18:

### Modelos (Python)
- **Nombres de Modelos:** Use siempre minúsculas y punto como separador jerárquico. Anteponga el prefijo de taller.
  - *Correcto:* `taller.orden.trabajo`
  - *Incorrecto:* `TallerOrdenTrabajo` o `taller_orden_trabajo`
- **Nombres de Clases:** Use PascalCase.
  - *Correcto:* `class TallerOrdenTrabajo(models.Model):`
- **Estructuración:** Los atributos del modelo deben colocarse al inicio del archivo, seguidos por campos computados (`compute`), restricciones SQL (`_sql_constraints`), restricciones Python (`@api.constrains`), onchanges (`@api.onchange`) y finalmente métodos de negocio.

### Vistas (XML)
- **Nombres de Archivos:** Deben ser descriptivos y seguir la nomenclatura `<modelo>_views.xml` (ej: `vehiculo_views.xml`).
- **Nombres de IDs:** Use siempre nombres descriptivos que eviten colisiones de namespaces de Odoo.
  - *Correcto:* `<record id="view_taller_vehiculo_form" model="ir.ui.view">`
- **Etiquetas Semánticas:** En Odoo 18, use `<list>` en lugar de `<tree>` para listados de datos convencionales (conforme a los estándares modernos de Odoo 18, aunque sea retrocompatible).

### Seguridad (Seguridad y permisos)
- **Regla del Menor Privilegio:** Ningún modelo personalizado debe crearse sin su respectiva declaración en `ir.model.access.csv`.
- **Reglas de Registro (Record Rules):** Defina dominios precisos para segmentar datos multi-compañía o multi-rol (como se implementó en `taller_security.xml` para separar la visibilidad de técnicos y clientes en el portal).

### Convenciones de nomenclatura (Nomenclatura general)
- **Campos Relacionales:**
  - `Many2one` debe terminar en `_id` (ej. `vehiculo_id`).
  - `One2many` y `Many2many` deben terminar en `_ids` (ej. `servicio_linea_ids`).
- **Campos Booleanos:** Deben formularse como preguntas o estados.
  - *Correcto:* `llanta_repuesto` (Boolean), `activo` (Boolean).

---

## 7. Gestión de issues

- **Creación de Issues:** Describa con precisión el problema técnico o la mejora requerida. Agregue capturas, logs de Odoo y pasos de reproducción detallados si se trata de un bug.
- **Asignación de Labels:** Use etiquetas semánticas de color para categorizar el issue:
  - `bug`: Comportamiento incorrecto del sistema.
  - `enhancement`: Nueva característica o mejora funcional.
  - `refactor`: Mejora de la base de código.
  - `sri-ecuador`: Temas relacionados a la integración fiscal del SRI.

---

## 8. Buenas prácticas

1. **Uso Exclusivo del ORM:** Evite modificar directamente registros a nivel de base de datos usando consultas SQL (`self.env.cr.execute`). El ORM de Odoo gestiona la invalidación de caché y triggers de seguridad automáticamente.
2. **Comentarios de Código Limpios:** Escriba código descriptivo por sí mismo. Use comentarios de código solo para documentar el por qué de una decisión no obvia o la especificación técnica de una API externa.
3. **No Dejar Código Muerto:** Elimine bloques de código comentados, variables sin uso o imports redundantes antes de abrir su PR.
4. **Frecuencia de Commits:** Realice commits pequeños y específicos. Evite commits gigantescos que mezclen lógica de negocio, estilos SCSS y cambios de seguridad XML.
