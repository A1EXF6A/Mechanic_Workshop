from odoo import models, fields

class FleetVehicle(models.Model):
    _inherit = 'fleet.vehicle'

    taller_user_id = fields.Many2one(
        comodel_name='res.partner',
        string='Usuario de Taller',
        required=True,
    )

    brand = fields.Char(required=True)
    model = fields.Char(required=True)
    license_plate = fields.Char(string='License Plate', required=True)
    color = fields.Char(string='Color')
