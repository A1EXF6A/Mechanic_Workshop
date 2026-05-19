from odoo import models, fields, api

class TallerCita(models.Model):
    _name = 'taller.cita'
    _description = 'Cita de Servicio'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = 'vehiculo_id'

    vehiculo_id = fields.Many2one('taller.vehiculo', string='Vehículo', required=True, tracking=True)
    cliente_id = fields.Many2one('usuarios_taller.user_profile', string='Cliente', required=True, tracking=True)
    fecha_cita = fields.Datetime(string='Fecha Programada', required=True, tracking=True)
    
    motivo = fields.Selection([
        ('mantenimiento', 'Mantenimiento Preventivo'),
        ('revision', 'Revisión General'),
        ('falla_mecanica', 'Falla Mecánica'),
        ('falla_electrica', 'Falla Eléctrica'),
        ('colision', 'Reparación por Colisión'),
        ('otro', 'Otro')
    ], string='Motivo de la Cita', required=True, tracking=True)
    
    descripcion = fields.Text(string='Detalle / Observaciones')
    
    prioridad = fields.Selection([
        ('rutinario', 'Rutinario'),
        ('mantenimiento', 'Mantenimiento'),
        ('urgente', 'Urgente')
    ], string='Prioridad', default='rutinario', tracking=True)
    
    estado = fields.Selection([
        ('solicitada', 'Solicitada'),
        ('confirmada', 'Confirmada'),
        ('cancelada', 'Cancelada')
    ], string='Estado', default='solicitada', tracking=True)
    
    orden_trabajo_id = fields.Many2one('taller.orden.trabajo', string='Orden de Trabajo Vinculada', readonly=True)

    @api.onchange('vehiculo_id')
    def _onchange_vehiculo_id(self):
        if self.vehiculo_id and self.vehiculo_id.propietario_id:
            self.cliente_id = self.vehiculo_id.propietario_id

    @api.model_create_multi
    def create(self, vals_list):
        citas = super().create(vals_list)
        for cita in citas:
            nombre_cliente = f"{cita.cliente_id.nombre} {cita.cliente_id.apellido}"
            nombre_orden = f"{cita.vehiculo_id.placa}-{nombre_cliente[:10]}-{cita.fecha_cita.strftime('%Y%m%d')}"
            
            orden = self.env['taller.orden.trabajo'].create({
                'name': nombre_orden.upper(),
                'vehiculo_id': cita.vehiculo_id.id,
                'fecha_ingreso': cita.fecha_cita,
                'diagnostico': cita.descripcion,
                'cita_id': cita.id
            })
            cita.orden_trabajo_id = orden.id
        return citas
