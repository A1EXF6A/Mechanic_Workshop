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
    can_edit_delete = fields.Boolean(compute='_compute_can_edit_delete')

    def _compute_can_edit_delete(self):
        for record in self:
            citas_activas = self.env['taller.cita'].search_count([
                ('vehiculo_id', '=', record.id),
                ('estado', '=', 'solicitada')
            ])
            ordenes_activas = self.env['taller.orden.trabajo'].search_count([
                ('vehiculo_id', '=', record.id),
                ('estado', '!=', 'entregado')
            ])
            record.can_edit_delete = (citas_activas == 0 and ordenes_activas == 0)

    @api.constrains('anio')
    def _check_anio(self):
        current_year = datetime.now().year
        for record in self:
            if record.anio and (record.anio <= 1850 or record.anio > current_year):
                raise ValidationError(f"El año del vehículo debe estar entre 1851 y {current_year}.")

    @api.model
    def action_cron_send_preventive_reminders(self):
        """
        Calcula de forma automática cuándo enviar recordatorios de mantenimiento
        basados en el tiempo transcurrido (6 meses) o kilometraje estimado (5,000 km)
        desde la última orden de trabajo entregada.
        """
        from datetime import date
        today = date.today()
        
        vehicles = self.search([])
        for vehicle in vehicles:
            # Obtener la última orden de trabajo entregada
            last_order = self.env['taller.orden.trabajo'].search([
                ('vehiculo_id', '=', vehicle.id),
                ('estado', '=', 'entregado'),
                ('reminder_sent', '=', False)
            ], order='fecha_ingreso desc', limit=1)
            
            if last_order:
                # Criterio 1: Tiempo (>= 180 días / 6 meses)
                needs_reminder_time = last_order.proxima_fecha_mto and last_order.proxima_fecha_mto <= today
                # Criterio 2: Kilometraje (>= 5000 km más que el de la orden)
                needs_reminder_km = last_order.proximo_kilometraje_mto and last_order.proximo_kilometraje_mto <= vehicle.kilometraje
                
                if needs_reminder_time or needs_reminder_km:
                    vehicle._send_preventive_reminder_email(last_order)

    def _send_preventive_reminder_email(self, last_order):
        self.ensure_one()
        # Buscar plantilla de correo
        template = self.env.ref('taller_mecanico.email_template_recordatorio_mantenimiento', raise_if_not_found=False)
        if template:
            # Enviar correo a través de la plantilla
            template.send_mail(self.id, force_send=True)
            # Marcar la orden para no repetir recordatorio
            last_order.write({'reminder_sent': True})
            # Publicar nota en el chatter de la orden para trazabilidad
            msg = f"Recordatorio de mantenimiento preventivo enviado automáticamente. Último mantenimiento: {last_order.name}."
            last_order.message_post(body=msg)



class TallerUserProfile(models.Model):
    _inherit = "usuarios_taller.user_profile"

    vehiculo_ids = fields.One2many(
        'taller.vehiculo',
        'propietario_id',
        string="Vehículos"
    )
