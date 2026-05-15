from odoo import models, fields

class TallerCitasLinea(models.Model):
    _name = 'taller.citas.linea'
    _description = 'Lineas de la cita'

    cita_id = fields.Many2one('taller.citas', string="Cita")

    producto = fields.Char(string="Producto / Pieza")
    marca = fields.Char(string="Marca deseada")
    cantidad = fields.Integer(string="Cantidad", default=1)