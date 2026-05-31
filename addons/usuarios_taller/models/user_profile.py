from odoo import api, fields, models, tools
from odoo.exceptions import ValidationError


class TallerUserProfile(models.Model):
    _name = "usuarios_taller.user_profile"
    _description = "Usuarios Taller"
    _order = "apellido, nombre"
    _rec_name = "display_name_full"

    cedula = fields.Char(string="Cedula", required=True)
    nombre = fields.Char(string="Nombre", required=True)
    apellido = fields.Char(string="Apellido", required=True)
    email = fields.Char(string="Direccion de correo", required=True)
    direccion = fields.Char(string="Direccion donde vive", required=True)
    password = fields.Char(string="Password", required=True)
    celular = fields.Char(string="Celular", required=True)
    edad = fields.Integer(string="Edad", required=True)

    display_name_full = fields.Char(
        string="Nombre Completo",
        compute="_compute_display_name_full",
        store=False
    )

    partner_id = fields.Many2one('res.partner', string='Contacto Odoo', readonly=True, ondelete='set null',
                                  help='Contacto vinculado en Odoo para facturación')

    @api.depends("nombre", "apellido")
    def _compute_display_name_full(self):
        for rec in self:
            rec.display_name_full = f"{rec.nombre} {rec.apellido}"

    @api.model_create_multi
    def create(self, vals_list):
        records = super().create(vals_list)
        for rec in records:
            if not rec.partner_id:
                partner = self.env['res.partner'].create({
                    'name': f"{rec.nombre} {rec.apellido}",
                    'email': rec.email,
                    'phone': rec.celular,
                    'street': rec.direccion,
                    'vat': rec.cedula,
                    'company_type': 'person',
                })
                rec.partner_id = partner.id
        return records

    def write(self, vals):
        res = super().write(vals)
        # Sincronizar cambios al partner vinculado
        for rec in self:
            if rec.partner_id and any(f in vals for f in ('nombre', 'apellido', 'email', 'celular', 'direccion', 'cedula')):
                update_vals = {}
                if 'nombre' in vals or 'apellido' in vals:
                    update_vals['name'] = f"{rec.nombre} {rec.apellido}"
                if 'email' in vals:
                    update_vals['email'] = rec.email
                if 'celular' in vals:
                    update_vals['phone'] = rec.celular
                if 'direccion' in vals:
                    update_vals['street'] = rec.direccion
                if 'cedula' in vals:
                    update_vals['vat'] = rec.cedula
                if update_vals:
                    rec.partner_id.write(update_vals)
        return res

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
