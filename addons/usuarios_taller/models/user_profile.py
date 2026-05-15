from odoo import api, fields, models, tools
from odoo.exceptions import ValidationError


class Partner(models.Model):
    _inherit = 'res.partner'

    cedula = fields.Char(string="Cédula")
    celular = fields.Char(string="Celular")
    edad = fields.Integer(string="Edad")

    _sql_constraints = [
        ("cedula_unique", "unique(cedula)", "La cédula ya existe."),
    ]

    @api.constrains("edad")
    def _check_edad(self):
        for record in self:
            if record.edad and record.edad < 18:
                raise ValidationError("La edad debe ser mayor de edad (18+).")

    @api.constrains("email")
    def _check_email(self):
        for record in self:
            if record.email and not tools.single_email_re.match(record.email):
                raise ValidationError("La dirección de correo no es válida.")

    @api.constrains("celular")
    def _check_celular(self):
        for record in self:
            if record.celular and not record.celular.isdigit():
                raise ValidationError("El celular debe contener solo números.")
