from odoo import models, fields, api
from odoo.exceptions import ValidationError
from datetime import datetime

class TallerVehiculo(models.Model):
    _name = 'taller.vehiculo'
    _description = 'Ficha de identificación del vehículo'
    _rec_name = 'placa'

    placa = fields.Char(string='Placa', required=True)
    propietario_id = fields.Many2one('usuarios_taller.user_profile', string='Propietario', required=True)
    marca_id = fields.Many2one('taller.marca', string='Marca', required=True)
    modelo_id = fields.Many2one('taller.modelo', string='Modelo', required=True, domain="[('marca_id', '=', marca_id)]")
    anio = fields.Integer(string='Año')
    color = fields.Selection([
        ('blanco', 'Blanco'),
        ('negro', 'Negro'),
        ('plata', 'Plata'),
        ('gris', 'Gris'),
        ('rojo', 'Rojo'),
        ('azul', 'Azul'),
        ('verde', 'Verde'),
        ('otro', 'Otro')
    ], string='Color')
    kilometraje = fields.Integer(string='Kilometraje')
    tipo_combustible = fields.Selection([
        ('gasolina', 'Gasolina'),
        ('diesel', 'Diésel'),
        ('hibrido', 'Híbrido'),
        ('electrico', 'Eléctrico')
    ], string='Tipo de Combustible')
    foto = fields.Image(string='Foto del Vehículo')
    historial_servicio_ids = fields.One2many('taller.orden.trabajo', 'vehiculo_id', string='Historial de Servicios')

    @api.constrains('anio')
    def _check_anio(self):
        current_year = datetime.now().year
        for record in self:
            if record.anio and (record.anio <= 1850 or record.anio > current_year):
                raise ValidationError(f"El año del vehículo debe estar entre 1851 y {current_year}.")
