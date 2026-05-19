from odoo import models, fields, api

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
