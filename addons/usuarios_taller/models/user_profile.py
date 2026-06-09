import logging
import uuid
from odoo import api, fields, models, tools
from odoo.exceptions import ValidationError

_logger = logging.getLogger(__name__)


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
    edad = fields.Integer(
        string="Edad",
        compute="_compute_edad",
        store=True,
        readonly=False,
    )
    
    fecha_nacimiento = fields.Date(string="Fecha de Nacimiento", required=True)
    street = fields.Char(string="Calle Principal")
    street2 = fields.Char(string="Calle Secundaria / Referencia")
    city = fields.Char(string="Ciudad / Cantón")
    state_id = fields.Many2one('res.country.state', string="Provincia")
    country_id = fields.Many2one('res.country', string="País", default=lambda self: self.env.ref('base.ec', raise_if_not_found=False))
    is_verified = fields.Boolean(string="Verificado", default=False)
    verification_token = fields.Char(string="Token de Verificación", copy=False)
    foto = fields.Binary(string="Foto de Perfil")

    display_name_full = fields.Char(
        string="Nombre Completo",
        compute="_compute_display_name_full",
        store=False
    )

    partner_id = fields.Many2one('res.partner', string='Contacto Odoo', readonly=True, ondelete='set null',
                                  help='Contacto vinculado en Odoo para facturación')
    user_id = fields.Many2one('res.users', string='Usuario Portal Odoo', readonly=True, ondelete='set null',
                               help='Usuario portal vinculado en Odoo para autenticación nativa')

    @api.depends("nombre", "apellido")
    def _compute_display_name_full(self):
        for rec in self:
            rec.display_name_full = f"{rec.nombre} {rec.apellido}"

    @api.depends('fecha_nacimiento')
    def _compute_edad(self):
        from datetime import date
        today = date.today()
        for rec in self:
            if rec.fecha_nacimiento:
                dob = fields.Date.from_string(rec.fecha_nacimiento)
                rec.edad = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))
            else:
                rec.edad = rec.edad or 0

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if not vals.get('verification_token'):
                vals['verification_token'] = str(uuid.uuid4())
        records = super().create(vals_list)
        portal_group = self.env.ref('base.group_portal')
        for rec in records:
            if not rec.partner_id:
                partner = self.env['res.partner'].create({
                    'name': f"{rec.nombre} {rec.apellido}",
                    'email': rec.email,
                    'phone': rec.celular,
                    'street': rec.street or rec.direccion,
                    'street2': rec.street2,
                    'city': rec.city or 'Ambato',
                    'state_id': rec.state_id.id if rec.state_id else False,
                    'country_id': rec.country_id.id if rec.country_id else 63,
                    'vat': rec.cedula,
                    'company_type': 'person',
                    'lang': 'es_EC',
                    'image_1920': rec.foto,
                })
                rec.partner_id = partner.id

            # Crear usuario portal nativo de Odoo vinculado al partner
            if not rec.user_id and rec.partner_id:
                existing_user = self.env['res.users'].sudo().search([
                    '|', ('login', '=', rec.email), ('partner_id', '=', rec.partner_id.id)
                ], limit=1)
                if existing_user:
                    rec.user_id = existing_user.id
                else:
                    try:
                        # Usar login con email para que puedan ingresar si quieren, pero taller_user_id maneja el portal taller
                        new_user = self.env['res.users'].sudo().with_context(no_reset_password=True).create({
                            'name': f"{rec.nombre} {rec.apellido}",
                            'login': f"taller_{rec.partner_id.id}@portal",
                            'password': rec.password,
                            'partner_id': rec.partner_id.id,
                            'groups_id': [(6, 0, [portal_group.id])],
                        })
                        rec.user_id = new_user.id
                        _logger.info('Usuario portal creado para %s', rec.email)
                    except Exception as e:
                        _logger.warning('No se pudo crear usuario portal para %s: %s', rec.email, e)
        return records

    def write(self, vals):
        res = super().write(vals)
        # Sincronizar cambios al partner vinculado
        for rec in self:
            if rec.partner_id:
                update_vals = {}
                if 'nombre' in vals or 'apellido' in vals:
                    update_vals['name'] = f"{rec.nombre} {rec.apellido}"
                if 'email' in vals:
                    update_vals['email'] = rec.email
                if 'celular' in vals:
                    update_vals['phone'] = rec.celular
                if 'street' in vals:
                    update_vals['street'] = rec.street
                elif 'direccion' in vals:
                    update_vals['street'] = rec.direccion
                if 'street2' in vals:
                    update_vals['street2'] = rec.street2
                if 'city' in vals:
                    update_vals['city'] = rec.city
                if 'state_id' in vals:
                    update_vals['state_id'] = rec.state_id.id if rec.state_id else False
                if 'country_id' in vals:
                    update_vals['country_id'] = rec.country_id.id if rec.country_id else False
                if 'cedula' in vals:
                    update_vals['vat'] = rec.cedula
                if 'foto' in vals:
                    update_vals['image_1920'] = vals['foto']
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
