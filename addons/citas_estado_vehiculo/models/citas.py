from odoo import models, fields, api

class TallerCitas(models.Model):
    _name = 'taller.citas'
    _description = 'Citas del Taller'

    name = fields.Char(string="Referencia", default="Nueva")

    usuario_id = fields.Many2one(
        'usuarios_taller.user_profile',
        string="Cliente",
        required=True
    )

    vehiculo_id = fields.Many2one(
        'taller.vehiculo',
        string="Vehículo",
        required=True,
        domain="[('usuario_id', '=', usuario_id)]"
    )

    estado = fields.Selection([
        ('recibido', 'Recibido'),
        ('proceso', 'En Proceso'),
        ('entregado', 'Entregado'),
    ], default='recibido')

    fecha = fields.Datetime(
        string="Fecha",
        default=fields.Datetime.now
    )

    tipo_cita_id = fields.Many2one(
        'taller.tipo.cita',
        string="Tipo de Cita"
    )
    
    @api.onchange('vehiculo_id')
    def _onchange_vehiculo(self):
        if self.vehiculo_id:
            self.usuario_id = self.vehiculo_id.usuario_id