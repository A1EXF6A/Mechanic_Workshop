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
    ], string='Estado', default='solicitada', tracking=True, group_expand='_expand_estados')

    @api.model
    def _expand_estados(self, states, domain, order=None, **kwargs):
        return ['solicitada', 'confirmada', 'cancelada']
    
    tecnico_id = fields.Many2one('hr.employee', string='Técnico Asignado', domain="['|', ('job_title', 'ilike', 'tecnico'), ('job_title', 'ilike', 'técnico')]", tracking=True)
    
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

    def write(self, vals):
        res = super(TallerCita, self).write(vals)
        for cita in self:
            if 'tecnico_id' in vals:
                if cita.orden_trabajo_id:
                    cita.orden_trabajo_id.tecnico_id = vals['tecnico_id']
                if cita.tecnico_id:
                    try:
                        cita._send_technician_assignment_email()
                    except Exception as e:
                        self.env['mail.message'].create({
                            'model': 'taller.cita',
                            'res_id': cita.id,
                            'body': f"⚠️ Error al enviar correo de asignación al técnico: {str(e)}",
                            'message_type': 'notification',
                        })
            
            if 'estado' in vals and vals['estado'] == 'confirmada':
                try:
                    cita._send_appointment_confirmed_email()
                except Exception as e:
                    self.env['mail.message'].create({
                        'model': 'taller.cita',
                        'res_id': cita.id,
                        'body': f"⚠️ Error al enviar correo de confirmación de cita: {str(e)}",
                        'message_type': 'notification',
                    })
        return res

    @api.model_create_multi
    def create(self, vals_list):
        citas = super().create(vals_list)
        for cita in citas:
            try:
                cita._send_new_appointment_notification()
            except Exception as e:
                # Registrar advertencia en logs
                cita.message_post(body=f"⚠️ Error al enviar notificación a gerentes: {str(e)}")
            
            if cita.tecnico_id:
                try:
                    cita._send_technician_assignment_email()
                except Exception as e:
                    self.env['mail.message'].create({
                        'model': 'taller.cita',
                        'res_id': cita.id,
                        'body': f"⚠️ Error al enviar correo de asignación al técnico: {str(e)}",
                        'message_type': 'notification',
                    })
        return citas

    def _send_technician_assignment_email(self):
        self.ensure_one()
        if not self.tecnico_id or not self.tecnico_id.work_email:
            return False
            
        fecha_str = self.fecha_cita.strftime('%d/%m/%Y a las %H:%M') if self.fecha_cita else ''
        motivo_label = dict(self._fields['motivo'].selection).get(self.motivo, 'Revisión General')
        
        body_html = f"""
        <div style="font-family: 'Inter', Helvetica, Arial, sans-serif; max-width: 600px; margin: 0 auto; border: 1px solid #e2e8f0; border-radius: 12px; overflow: hidden; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.05);">
            <div style="background: linear-gradient(135deg, #10b981, #047857); padding: 30px; text-align: center; color: white;">
                <h1 style="margin: 0; font-size: 24px; font-weight: 700;">Nueva Cita Asignada</h1>
                <p style="margin: 6px 0 0 0; color: #d1fae5; font-size: 14px;">Se le ha asignado una nueva tarea en el sistema</p>
            </div>
            <div style="padding: 30px; background-color: white;">
                <p style="font-size: 15px; color: #334155; line-height: 1.6; margin: 0 0 20px 0;">
                    Hola <strong>{self.tecnico_id.name}</strong>,
                </p>
                <p style="font-size: 14px; color: #475569; line-height: 1.6; margin: 0 0 20px 0;">
                    Por medio del presente correo le informamos que ha sido asignado(a) como técnico responsable para la siguiente cita de servicio:
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
                            <td style="padding: 4px 0; color: #10b981; font-weight: 600; text-align: right;">{motivo_label}</td>
                        </tr>
                    </table>
                </div>
            </div>
            <div style="border-top: 1px solid #f1f5f9; padding-top: 20px; font-size: 13px; color: #94a3b8; text-align: center; line-height: 1.5; padding-bottom: 20px; background-color: #fafafa;">
                <p style="margin: 0 0 5px 0;">Por favor revise el sistema para más detalles.</p>
                <p style="margin: 0; font-weight: 600; color: #64748b;">{self.env.company.name}</p>
            </div>
        </div>
        """
        mail_values = {
            'subject': f"Nueva Cita Asignada - Vehículo {self.vehiculo_id.placa}",
            'body_html': body_html,
            'email_to': self.tecnico_id.work_email,
        }
        self.env['mail.mail'].create(mail_values).send()
        self.message_post(body=f"📧 Correo de asignación de técnico enviado con éxito a {self.tecnico_id.work_email}.")
        return True

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
        from odoo.exceptions import ValidationError
        for cita in self:
            if not cita.tecnico_id:
                raise ValidationError("Debe asignar un técnico a la cita antes de poder confirmarla y generar la orden de trabajo.")
                
            cita.estado = 'confirmada'
            if not cita.orden_trabajo_id:
                nombre_cliente = f"{cita.cliente_id.nombre} {cita.cliente_id.apellido}" if cita.cliente_id else "Desconocido"
                nombre_orden = f"{cita.vehiculo_id.placa}-{nombre_cliente[:10]}-{cita.fecha_cita.strftime('%Y%m%d')}"
                
                orden = self.env['taller.orden.trabajo'].create({
                    'name': nombre_orden.upper(),
                    'vehiculo_id': cita.vehiculo_id.id,
                    'fecha_ingreso': cita.fecha_cita,
                    'diagnostico': cita.descripcion,
                    'cita_id': cita.id,
                    'tecnico_id': cita.tecnico_id.id,
                })
                cita.orden_trabajo_id = orden.id

    def action_cancelar(self):
        for cita in self:
            cita.estado = 'cancelada'
            if cita.orden_trabajo_id:
                if cita.orden_trabajo_id.estado == 'recibido' and not cita.orden_trabajo_id.factura_id:
                    orden = cita.orden_trabajo_id
                    cita.orden_trabajo_id = False
                    orden.unlink()

    def _send_new_appointment_notification(self):
        self.ensure_one()
        group_manager = self.env.ref('taller_mecanico.group_taller_manager', raise_if_not_found=False)
        group_admin = self.env.ref('base.group_erp_manager', raise_if_not_found=False)
        
        users_to_notify = self.env['res.users']
        if group_manager:
            users_to_notify |= group_manager.users
        if group_admin:
            users_to_notify |= group_admin.users
            
        emails = [user.email for user in users_to_notify if user.email]
        if not emails:
            return
            
        fecha_str = self.fecha_cita.strftime('%d/%m/%Y a las %H:%M') if self.fecha_cita else ''
        motivo_label = dict(self._fields['motivo'].selection).get(self.motivo, 'Revisión General')
        
        body_html = f"""
        <div style="font-family: 'Inter', Helvetica, Arial, sans-serif; max-width: 600px; margin: 0 auto; border: 1px solid #e2e8f0; border-radius: 12px; overflow: hidden;">
            <div style="background: #3b82f6; padding: 20px; text-align: center; color: white;">
                <h2 style="margin: 0;">Nueva Cita Solicitada</h2>
            </div>
            <div style="padding: 20px;">
                <p>Se ha solicitado una nueva cita en el taller.</p>
                <ul>
                    <li><strong>Cliente:</strong> {self.cliente_id.nombre} {self.cliente_id.apellido}</li>
                    <li><strong>Vehículo:</strong> {self.vehiculo_id.marca_id.name} {self.vehiculo_id.modelo_id.name} ({self.vehiculo_id.placa})</li>
                    <li><strong>Fecha:</strong> {fecha_str}</li>
                    <li><strong>Motivo:</strong> {motivo_label}</li>
                </ul>
                <p>Por favor, ingrese al sistema para confirmar la cita y asignar un técnico responsable.</p>
            </div>
        </div>
        """
        
        mail_values = {
            'subject': f"Nueva Cita Solicitada - {self.vehiculo_id.placa}",
            'body_html': body_html,
            'email_to': ','.join(emails),
        }
        self.env['mail.mail'].create(mail_values).send()
