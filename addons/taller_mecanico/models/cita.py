from odoo import models, fields, api

class TallerCita(models.Model):
    _name = 'taller.cita'
    _description = 'Cita de Servicio'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = 'vehiculo_id'

    vehiculo_id = fields.Many2one('taller.vehiculo', string='Vehículo', required=True, tracking=True)
    cliente_id = fields.Many2one('usuarios_taller.user_profile', string='Cliente', required=True, tracking=True)
    fecha_cita = fields.Datetime(string='Fecha Programada', required=True, tracking=True)
    
    motivo = fields.Selection([
        ('mantenimiento', 'Mantenimiento Preventivo'),
        ('revision', 'Revisión General'),
        ('falla_mecanica', 'Falla Mecánica'),
        ('falla_electrica', 'Falla Eléctrica'),
        ('colision', 'Reparación por Colisión'),
        ('otro', 'Otro')
    ], string='Motivo de la Cita', required=True, tracking=True)
    
    descripcion = fields.Text(string='Detalle / Observaciones')
    
    prioridad = fields.Selection([
        ('rutinario', 'Rutinario'),
        ('mantenimiento', 'Mantenimiento'),
        ('urgente', 'Urgente')
    ], string='Prioridad', default='rutinario', tracking=True)
    
    estado = fields.Selection([
        ('solicitada', 'Solicitada'),
        ('confirmada', 'Confirmada'),
        ('cancelada', 'Cancelada')
    ], string='Estado', default='solicitada', tracking=True)
    
    orden_trabajo_id = fields.Many2one('taller.orden.trabajo', string='Orden de Trabajo Vinculada', readonly=True)
    
    fecha_fin = fields.Datetime(string='Fecha Fin', compute='_compute_fecha_fin', store=True)

    @api.depends('fecha_cita')
    def _compute_fecha_fin(self):
        from datetime import timedelta
        for cita in self:
            if cita.fecha_cita:
                cita.fecha_fin = cita.fecha_cita + timedelta(hours=1)
            else:
                cita.fecha_fin = False

    @api.onchange('vehiculo_id')
    def _onchange_vehiculo_id(self):
        if self.vehiculo_id and self.vehiculo_id.propietario_id:
            self.cliente_id = self.vehiculo_id.propietario_id

    @api.model_create_multi
    def create(self, vals_list):
        citas = super().create(vals_list)
        for cita in citas:
            nombre_cliente = f"{cita.cliente_id.nombre} {cita.cliente_id.apellido}"
            nombre_orden = f"{cita.vehiculo_id.placa}-{nombre_cliente[:10]}-{cita.fecha_cita.strftime('%Y%m%d')}"
            
            orden = self.env['taller.orden.trabajo'].create({
                'name': nombre_orden.upper(),
                'vehiculo_id': cita.vehiculo_id.id,
                'fecha_ingreso': cita.fecha_cita,
                'diagnostico': cita.descripcion,
                'cita_id': cita.id
            })
            cita.orden_trabajo_id = orden.id
        return citas

    def write(self, vals):
        res = super(TallerCita, self).write(vals)
        if 'estado' in vals and vals['estado'] == 'confirmada':
            for cita in self:
                try:
                    cita._send_appointment_confirmed_email()
                except Exception as e:
                    # Registrar advertencia en logs pero no bloquear la edición
                    self.env['mail.message'].create({
                        'model': 'taller.cita',
                        'res_id': cita.id,
                        'body': f"⚠️ Error al enviar correo de confirmación de cita: {str(e)}",
                        'message_type': 'notification',
                    })
        return res

    def _send_appointment_confirmed_email(self):
        self.ensure_one()
        partner = self.cliente_id.partner_id if self.cliente_id else False
        if not partner or not partner.email:
            return False
            
        fecha_str = self.fecha_cita.strftime('%d/%m/%Y a las %H:%M') if self.fecha_cita else ''
        motivo_label = dict(self._fields['motivo'].selection).get(self.motivo, 'Revisión General')
        
        body_html = f"""
        <div style="font-family: 'Inter', Helvetica, Arial, sans-serif; max-width: 600px; margin: 0 auto; border: 1px solid #e2e8f0; border-radius: 12px; overflow: hidden; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.05), 0 2px 4px -1px rgba(0,0,0,0.03);">
            <div style="background: linear-gradient(135deg, #1e293b, #0f172a); padding: 30px; text-align: center; color: white;">
                <h1 style="margin: 0; font-size: 24px; font-weight: 700; letter-spacing: -0.025em;">Cita Confirmada</h1>
                <p style="margin: 6px 0 0 0; color: #94a3b8; font-size: 14px;">Su reserva en el taller ha sido aprobada</p>
            </div>
            <div style="padding: 30px; background-color: white;">
                <p style="font-size: 15px; color: #334155; line-height: 1.6; margin: 0 0 20px 0;">
                    Estimado(a) <strong>{partner.name}</strong>,
                </p>
                <p style="font-size: 14px; color: #475569; line-height: 1.6; margin: 0 0 20px 0;">
                    Le confirmamos que su cita de servicio ha sido programada con éxito en nuestro taller mecánico. A continuación, le detallamos la información de su reserva:
                </p>
                
                <div style="background-color: #f8fafc; border: 1px solid #e2e8f0; border-radius: 8px; padding: 16px; margin-bottom: 20px;">
                    <table style="width: 100%; font-size: 14px; border-collapse: collapse;">
                        <tr>
                            <td style="padding: 4px 0; color: #64748b; font-weight: 500;">Vehículo:</td>
                            <td style="padding: 4px 0; color: #0f172a; font-weight: 600; text-align: right;">{self.vehiculo_id.marca_id.name} {self.vehiculo_id.modelo_id.name} ({self.vehiculo_id.placa})</td>
                        </tr>
                        <tr>
                            <td style="padding: 4px 0; color: #64748b; font-weight: 500;">Fecha Programada:</td>
                            <td style="padding: 4px 0; color: #0f172a; font-weight: 600; text-align: right;">{fecha_str}</td>
                        </tr>
                        <tr>
                            <td style="padding: 4px 0; color: #64748b; font-weight: 500;">Motivo de Cita:</td>
                            <td style="padding: 4px 0; color: #3b82f6; font-weight: 600; text-align: right;">{motivo_label}</td>
                        </tr>
                    </table>
                </div>

                <div style="background-color: #eff6ff; border: 1px solid #bfdbfe; border-radius: 8px; padding: 16px; margin-bottom: 20px; font-size: 13px; color: #1e3a8a; line-height: 1.5;">
                    <strong>💡 Recomendaciones para su cita:</strong>
                    <ul style="margin: 6px 0 0 0; padding-left: 20px;">
                        <li>Por favor, asista 10 minutos antes del horario reservado.</li>
                        <li>Recuerde llevar consigo los documentos de circulación del vehículo.</li>
                        <li>Si no puede asistir, contáctenos para reprogramar a tiempo.</li>
                    </ul>
                </div>
            </div>
            <div style="border-top: 1px solid #f1f5f9; padding-top: 20px; font-size: 13px; color: #94a3b8; text-align: center; line-height: 1.5; padding-bottom: 20px; background-color: #fafafa;">
                <p style="margin: 0 0 5px 0;">Gracias por confiar su vehículo a nuestras manos.</p>
                <p style="margin: 0; font-weight: 600; color: #64748b;">{self.env.company.name}</p>
            </div>
        </div>
        """
        mail_values = {
            'subject': f"Confirmación de Cita de Servicio - Vehículo {self.vehiculo_id.placa}",
            'body_html': body_html,
            'email_to': partner.email,
        }
        self.env['mail.mail'].create(mail_values).send()
        # Agregar mensaje al chatter de la cita
        self.message_post(body=f"📧 Correo de confirmación de cita enviado con éxito a {partner.email}.")
        return True

    def action_confirmar(self):
        for cita in self:
            cita.estado = 'confirmada'

    def action_cancelar(self):
        for cita in self:
            cita.estado = 'cancelada'
