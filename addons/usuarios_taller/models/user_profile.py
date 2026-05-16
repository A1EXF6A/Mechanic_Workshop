from odoo import api, fields, models, tools
from odoo.exceptions import ValidationError


class TallerUserProfile(models.Model):
    _name = "usuarios_taller.user_profile"
    _description = "Usuarios Taller"
    _order = "apellido, nombre"

  
 

    cedula = fields.Char(string="Cedula", required=True)
    nombre = fields.Char(string="Nombre", required=True)
    apellido = fields.Char(string="Apellido", required=True)
    email = fields.Char(string="Direccion de correo", required=True)
    direccion = fields.Char(string="Direccion donde vive", required=True)
    password = fields.Char(string="Password", required=True)
    celular = fields.Char(string="Celular", required=True)
    edad = fields.Integer(string="Edad", required=True)

    

    _sql_constraints = [
        ("cedula_unique", "unique(cedula)", "La cedula ya existe."),
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
                raise ValidationError("La direccion de correo no es valida.")

    @api.constrains("celular")
    def _check_celular(self):
        for record in self:
            if record.celular and not record.celular.isdigit():
                raise ValidationError("El celular debe contener solo numeros.")

