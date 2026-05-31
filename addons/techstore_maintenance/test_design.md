# Plan de Pruebas — Módulo `techstore_maintenance`

## Alcance de las Pruebas Funcionales

### 1. Modelo `techstore.technician`

| Acción a probar | Detalle |
|---|---|
| **Creación** | Crear técnico con todos los campos obligatorios. Crear técnico sin email (opcional). |
| **Validaciones** | `_check_email`: formato inválido → `ValidationError`. `_check_phone`: vacío → `ValidationError`. `unique_identification`: duplicado → `ValidationError`. |
| **Campos calculados** | `maintenance_count`: conteo de mantenimientos activos (excluye `finalizado` y `cancelado`). `workload_level`: low (≤2), medium (≤5), high (≤8), critical (>8). |
| **Modificación** | Cambiar `specialty`, `email`, desactivar técnico (`active=False`). |
| **Tracking** | Verificar que cambios en campos `tracking=True` generan mensajes en chatter. |

### 2. Modelo `techstore.equipment`

| Acción a probar | Detalle |
|---|---|
| **Creación** | Crear equipo válido. Verificar asignación automática de `code` mediante secuencia (`EQUIP/año/XXXXX`). |
| **Validaciones** | `unique_serial_number`: serial duplicado → `ValidationError`. |
| **Estado** | Transiciones: `received` → `under_repair` → `repaired` → `delivered`. |
| **Tracking** | Verificar chatter en campos con `tracking=True`. |

### 3. Modelo `techstore.maintenance`

| Acción a probar | Detalle |
|---|---|
| **Creación** | Crear mantenimiento válido. Verificar `number` secuencial (`MAINT/año/XXXXX`). Verificar creación automática de registro en `techstore.maintenance.history` y `techstore.maintenance.metrics`. |
| **Ciclo de estados** | `nuevo` → `asignado` → `en_proceso` → `pendiente` → `finalizado`. También `nuevo` → `cancelado`. |
| **Auto-asignación de fechas** | `start_date` se establece automáticamente al pasar a `en_proceso`. `end_date` se establece automáticamente al pasar a `finalizado`. |
| **Campos calculados** | `real_time`: diferencia entre `end_date` y `start_date` en horas. |
| **Onchange** | `priority = '3'` (Critical) → warning emergente. |
| **Historial** | Cada cambio de estado crea un registro en `history` con `old_state`, `new_state`, `user_id`. |
| **Eliminación** | Borrar mantenimiento → elimina en cascada `history` y `metrics` asociados. |

### 4. Modelo `techstore.maintenance.history`

| Acción a probar | Detalle |
|---|---|
| **Creación automática** | Cada cambio de estado en `techstore.maintenance` genera un registro histórico. |
| **Campos** | `old_state`, `new_state`, `user_id`, `change_date`, `comment`. |
| **Orden** | Por defecto descendente por `change_date`. |

### 5. Modelo `techstore.maintenance.metrics`

| Acción a probar | Detalle |
|---|---|
| **Creación automática** | Al crear un mantenimiento se crea su registro de métricas asociado (`maintenance.create`). |
| **Campos calculados** | `attention_time` = (`start_date` - `request_date`) en horas. `resolution_time` = `real_time`. `sla_compliance` = `real_time` ≤ `estimated_time`. `delay` = max(0, `real_time` - `estimated_time`). `technician_efficiency` = (`estimated_time` / `real_time`) × 100. `state_changes_count` = cantidad de registros en `history`. `quality_indicator` = (`customer_satisfaction` / 4) × 100. |
| **Escenarios** | SLA cumplido, SLA incumplido (delay calculado), eficiencia 100%, eficiencia menor al 100%, calidad según satisfacción (Poor=1, Fair=2, Good=3, Excellent=4). |

### 6. Seguridad y Permisos

| Acción a probar | Detalle |
|---|---|
| **Grupo Technician** | Solo lectura de mantenimientos propios. Sin permiso de borrado. |
| **Grupo Supervisor** | Lectura y escritura sobre todos los mantenimientos. Sin permiso de borrado. |
| **Grupo Admin** | Permisos totales (crear, leer, escribir, borrar). |
| **Record rule** | `rule_techstore_maintenance_technician`: el técnico solo ve mantenimientos donde `technician_id.user_id = user.id`. |
| **Acceso por modelo** | Verificar permisos individuales según CSV `ir.model.access.csv`. |

---

## Casos de Prueba (Funciones)

| # | Función | Modelo | Descripción |
|---|---|---|---|
| 1 | `test_technician_create` | `technician` | Crear técnico válido, verificar campos guardados correctamente. |
| 2 | `test_technician_duplicate_identification` | `technician` | Intentar crear dos técnicos con mismo `identification` → `ValidationError`. |
| 3 | `test_technician_invalid_email` | `technician` | Email sin formato válido → `ValidationError`. |
| 4 | `test_technician_empty_phone` | `technician` | Teléfono vacío → `ValidationError`. |
| 5 | `test_technician_maintenance_count` | `technician` | Crear mantenimientos activos e inactivos; verificar que `maintenance_count` solo cuenta activos. |
| 6 | `test_technician_workload_level_low` | `technician` | 0-2 mantenimientos activos → `workload_level = 'low'`. |
| 7 | `test_technician_workload_level_medium` | `technician` | 3-5 mantenimientos activos → `workload_level = 'medium'`. |
| 8 | `test_technician_workload_level_high` | `technician` | 6-8 mantenimientos activos → `workload_level = 'high'`. |
| 9 | `test_technician_workload_level_critical` | `technician` | 9+ mantenimientos activos → `workload_level = 'critical'`. |
| 10 | `test_equipment_create` | `equipment` | Crear equipo válido, verificar `code` generado y campos. |
| 11 | `test_equipment_code_sequence` | `equipment` | Verificar formato `EQUIP/año/XXXXX` en el código. |
| 12 | `test_equipment_duplicate_serial` | `equipment` | Serial duplicado → `ValidationError`. |
| 13 | `test_equipment_state_transitions` | `equipment` | Transición completa `received → under_repair → repaired → delivered`. |
| 14 | `test_maintenance_create` | `maintenance` | Crear mantenimiento, verificar `number`, `history` y `metrics` creados automáticamente. |
| 15 | `test_maintenance_number_sequence` | `maintenance` | Verificar formato `MAINT/año/XXXXX`. |
| 16 | `test_maintenance_state_flow_new_to_finalized` | `maintenance` | Ciclo completo: nuevo → asignado → en_proceso → pendiente → finalizado. |
| 17 | `test_maintenance_state_cancel` | `maintenance` | Transición nuevo → cancelado. |
| 18 | `test_maintenance_auto_start_date` | `maintenance` | Al pasar a `en_proceso` sin `start_date`, se asigna automáticamente. |
| 19 | `test_maintenance_auto_end_date` | `maintenance` | Al pasar a `finalizado` sin `end_date`, se asigna automáticamente. |
| 20 | `test_maintenance_history_on_state_change` | `maintenance` | Cada cambio de estado genera un registro en `history`. |
| 21 | `test_maintenance_history_content` | `maintenance` | Verificar `old_state`, `new_state`, `user_id` en el history. |
| 22 | `test_maintenance_real_time_computation` | `maintenance` | `real_time` = `end_date - start_date` en horas. |
| 23 | `test_maintenance_critical_priority_warning` | `maintenance` | `priority = '3'` → warning en onchange. |
| 24 | `test_maintenance_estimated_fields` | `maintenance` | Guardar y recuperar `estimated_cost`, `final_cost`, `estimated_time`. |
| 25 | `test_maintenance_cascade_delete` | `maintenance` | Borrar mantenimiento → history y metrics también borrados. |
| 26 | `test_metrics_auto_creation` | `metrics` | Al crear maintenance, existe registro en `techstore.maintenance.metrics`. |
| 27 | `test_metrics_attention_time` | `metrics` | `attention_time` = (`start_date` - `request_date`) / 3600. |
| 28 | `test_metrics_sla_compliance_ok` | `metrics` | `real_time ≤ estimated_time` → `sla_compliance = True`, `delay = 0`. |
| 29 | `test_metrics_sla_breach` | `metrics` | `real_time > estimated_time` → `sla_compliance = False`, `delay > 0`. |
| 30 | `test_metrics_technician_efficiency` | `metrics` | `technician_efficiency = (estimated_time / real_time) × 100`. |
| 31 | `test_metrics_quality_indicator` | `metrics` | `quality_indicator = (satisfaction / 4) × 100`. |
| 32 | `test_metrics_state_changes_count` | `metrics` | `state_changes_count` = número de entradas en history del maintenance. |
| 33 | `test_history_order` | `history` | History ordenado descendente por `change_date`. |
| 34 | `test_security_technician_read_own` | `security` | Usuario technician solo ve sus mantenimientos asignados. |
| 35 | `test_security_technician_no_unlink` | `security` | Technician no puede borrar mantenimientos. |
| 36 | `test_security_supervisor_read_all` | `security` | Usuario supervisor ve todos los mantenimientos. |
| 37 | `test_security_supervisor_no_unlink` | `security` | Supervisor no puede borrar mantenimientos. |
| 38 | `test_security_admin_full_access` | `security` | Admin puede crear, leer, escribir y borrar. |
| 39 | `test_security_technician_create_restrictions` | `security` | Technician no puede crear técnicos (según CSV: perm_create=0). |
| 40 | `test_security_technician_equipment_read` | `security` | Technician puede leer equipos (perm_read=1) pero no crear (perm_create=0 según CSV). |

---

## Notas Técnicas

- **Framework de test:** `odoo.tests.common.TransactionCase` (estándar Odoo).
- **Ubicación del archivo:** `addons/techstore_maintenance/tests/__init__.py` + `addons/techstore_maintenance/tests/test_maintenance.py`.
- **Datos de prueba:** Usar `self.env` con `demo=True` o crear registros inline.
- **Usuarios de prueba:** Crear usuarios con `groups_id` para cada nivel de seguridad:
  - `group_techstore_technician`
  - `group_techstore_supervisor`
  - `group_techstore_admin`
- **Ejecución:** `odoo-bin --test-enable --addons-path=addons -d test_db --stop-after-init -i techstore_maintenance`
