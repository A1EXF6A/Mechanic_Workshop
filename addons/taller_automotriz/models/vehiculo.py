from odoo import models, fields

class TallerVehiculo(models.Model):
    _name = 'taller.vehiculo'
    _description = 'Ficha de identificación del vehículo'
    _rec_name = 'placa'

    placa = fields.Char(string='Placa', required=True)
    propietario_id = fields.Many2one('res.partner', string='Propietario', required=True)
    marca = fields.Char(string='Marca', required=True)
    modelo = fields.Char(string='Modelo', required=True)
    anio = fields.Integer(string='Año')
    color = fields.Char(string='Color')
    kilometraje = fields.Integer(string='Kilometraje')
    tipo_combustible = fields.Selection([
        ('gasolina', 'Gasolina'),
        ('diesel', 'Diésel'),
        ('hibrido', 'Híbrido'),
        ('electrico', 'Eléctrico')
    ], string='Tipo de Combustible')
    foto = fields.Image(string='Foto del Vehículo')
    historial_servicio_ids = fields.One2many('taller.orden.trabajo', 'vehiculo_id', string='Historial de Servicios')
