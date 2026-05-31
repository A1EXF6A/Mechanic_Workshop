from odoo import models, fields, api
from odoo.exceptions import UserError

class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    orden_trabajo_count = fields.Integer(string='Órdenes de Trabajo', compute='_compute_orden_trabajo_count')

    def _compute_orden_trabajo_count(self):
        for employee in self:
            count = self.env['taller.orden.trabajo'].search_count([
                ('tecnico_id', '=', employee.id)
            ])
            employee.orden_trabajo_count = count

    def action_view_ordenes_trabajo(self):
        self.ensure_one()
        return {
            'name': 'Mis Órdenes de Trabajo',
            'type': 'ir.actions.act_window',
            'res_model': 'taller.orden.trabajo',
            'view_mode': 'kanban,list,form',
            'domain': [('tecnico_id', '=', self.id)],
            'context': {'default_tecnico_id': self.id},
        }

    @api.model_create_multi
    def create(self, vals_list):
        # Crear los empleados primero
        employees = super(HrEmployee, self).create(vals_list)
        
        # Automatización: Crear usuarios para mecánicos/taller si tienen correo
        for employee in employees:
            if employee.work_email and not employee.user_id:
                job_title = employee.job_title or ''
                dept_name = employee.department_id.name or ''
                
                # Verificar si pertenece al área operativa del taller
                is_taller = any(
                    term in (job_title.lower() + dept_name.lower()) 
                    for term in ['taller', 'mecanico', 'mecánico', 'tecnico', 'técnico', 'operaciones', 'bodega', 'recepcion', 'recepción']
                )
                
                if is_taller:
                    # Buscar si ya existe un usuario con ese correo
                    existing_user = self.env['res.users'].sudo().search([('login', '=', employee.work_email)], limit=1)
                    if not existing_user:
                        # Crear el usuario Odoo automáticamente
                        groups = [employee.env.ref('base.group_user').id]
                        tech_group = employee.env.ref('taller_mecanico.group_taller_technician', raise_if_not_found=False)
                        if tech_group:
                            groups.append(tech_group.id)
                        
                        new_user = self.env['res.users'].sudo().create({
                            'name': employee.name,
                            'login': employee.work_email,
                            'email': employee.work_email,
                            'password': 'Autologic2026!', # Contraseña inicial segura por defecto
                            'company_id': employee.env.company.id,
                            'company_ids': [(6, 0, [employee.env.company.id])],
                            'groups_id': [(6, 0, groups)],
                        })
                        employee.user_id = new_user.id
                    else:
                        employee.user_id = existing_user.id
                        
        return employees

    def write(self, vals):
        res = super(HrEmployee, self).write(vals)
        # Si se actualiza el empleado (por ejemplo, se le asigna un correo)
        if 'work_email' in vals or 'department_id' in vals or 'job_title' in vals:
            for employee in self:
                if employee.work_email and not employee.user_id:
                    job_title = employee.job_title or ''
                    dept_name = employee.department_id.name or ''
                    
                    is_taller = any(
                        term in (job_title.lower() + dept_name.lower()) 
                        for term in ['taller', 'mecanico', 'mecánico', 'tecnico', 'técnico', 'operaciones', 'bodega', 'recepcion', 'recepción']
                    )
                    
                    if is_taller:
                        existing_user = self.env['res.users'].sudo().search([('login', '=', employee.work_email)], limit=1)
                        if not existing_user:
                            groups = [employee.env.ref('base.group_user').id]
                            tech_group = employee.env.ref('taller_mecanico.group_taller_technician', raise_if_not_found=False)
                            if tech_group:
                                groups.append(tech_group.id)
                            
                            new_user = self.env['res.users'].sudo().create({
                                'name': employee.name,
                                'login': employee.work_email,
                                'email': employee.work_email,
                                'password': 'Autologic2026!',
                                'company_id': employee.env.company.id,
                                'company_ids': [(6, 0, [employee.env.company.id])],
                                'groups_id': [(6, 0, groups)],
                            })
                            employee.user_id = new_user.id
                        else:
                            employee.user_id = existing_user.id
        return res
