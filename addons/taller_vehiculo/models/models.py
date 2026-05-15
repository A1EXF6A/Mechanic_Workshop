from odoo import models, fields


class TallerVehiculo(models.Model):
    _name = 'taller.vehiculo'
    _description = 'Vehículo del Taller'
    _order = 'matricula'

    matricula = fields.Char(string='Matrícula', required=True)
    marca = fields.Char(string='Marca', required=True)
    modelo = fields.Char(string='Modelo', required=True)
    anio = fields.Integer(string='Año')
    color = fields.Char(string='Color')
    usuario_id = fields.Many2one(
        comodel_name='res.partner',
        string='Propietario',
        required=True,
    )
    historial_ids = fields.One2many(
        comodel_name='taller.historial',
        inverse_name='vehiculo_id',
        string='Historial',
    )

    _sql_constraints = [
        ('matricula_unique', 'unique(matricula)', 'La matrícula ya existe.'),
    ]


class TallerHistorial(models.Model):
    _name = 'taller.historial'
    _description = 'Historial del Vehículo'
    _order = 'fecha desc'

    vehiculo_id = fields.Many2one(
        comodel_name='taller.vehiculo',
        string='Vehículo',
        required=True,
    )
    fecha = fields.Date(string='Fecha', required=True, default=fields.Date.today)
    descripcion = fields.Text(string='Descripción', required=True)
    tipo = fields.Selection([
        ('entrada', 'Entrada'),
        ('salida', 'Salida'),
        ('mantenimiento', 'Mantenimiento'),
        ('otro', 'Otro'),
    ], string='Tipo', required=True, default='entrada')
