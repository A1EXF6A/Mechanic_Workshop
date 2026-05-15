from odoo import models, fields, api

class TallerCitas(models.Model):
    _name = 'taller.citas'
    _description = 'Citas del Taller'

    name = fields.Char(string="Referencia", default="Nueva")
    trabajo = fields.Text(string="Trabajo a realizar")

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

    preferencias = fields.Text(
    string="Preferencias del cliente",
    help="Ej: usar aceite marca Castrol"
    )

    linea_ids = fields.One2many(
    'taller.citas.linea',
    'cita_id',
    string="Piezas / Trabajos"
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

    @api.onchange('vehiculo_id')
    def _onchange_vehiculo(self):
        if self.vehiculo_id:
            self.usuario_id = self.vehiculo_id.usuario_id