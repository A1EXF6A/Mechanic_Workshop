from odoo import models, fields

class TallerTipoCita(models.Model):
    _name = 'taller.tipo.cita'
    _description = 'Tipos de Cita'

    name = fields.Char(string="Nombre", required=True)
    descripcion = fields.Text(string="Descripción")