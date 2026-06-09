from odoo import models, fields, api
from odoo.exceptions import UserError

class TallerOrdenLineaServicio(models.Model):
    _name = 'taller.orden.linea.servicio'
    _description = 'Línea de Servicio'

    orden_id = fields.Many2one('taller.orden.trabajo', string='Orden de Trabajo', required=True, ondelete='cascade')
    producto_id = fields.Many2one('product.product', string='Servicio', domain="[('type', '=', 'service')]", required=True)
    cantidad = fields.Float(string='Cantidad', default=1.0)
    precio_unitario = fields.Float(string='Precio Unitario')
    subtotal = fields.Float(string='Subtotal', compute='_compute_subtotal', store=True)
    is_extra = fields.Boolean(string='Es Extra', default=False)
    state_extra = fields.Selection([
        ('pendiente', 'Pendiente'),
        ('aprobado', 'Aprobado'),
        ('rechazado', 'Rechazado')
    ], string='Estado Extra', default='pendiente')
    agregado_por_cliente = fields.Boolean(string='Solicitado por Cliente', default=False)


    @api.onchange('producto_id')
    def _onchange_producto_id(self):
        if self.producto_id:
            self.precio_unitario = self.producto_id.list_price

    @api.depends('cantidad', 'precio_unitario')
    def _compute_subtotal(self):
        for line in self:
            line.subtotal = line.cantidad * line.precio_unitario

class TallerOrdenLineaRepuesto(models.Model):
    _name = 'taller.orden.linea.repuesto'
    _description = 'Línea de Repuesto'

    orden_id = fields.Many2one('taller.orden.trabajo', string='Orden de Trabajo', required=True, ondelete='cascade')
    producto_id = fields.Many2one('product.product', string='Repuesto', domain="[('type', '!=', 'service')]", required=True)
    cantidad = fields.Float(string='Cantidad', default=1.0)
    precio_unitario = fields.Float(string='Precio Unitario')
    subtotal = fields.Float(string='Subtotal', compute='_compute_subtotal', store=True)
    is_extra = fields.Boolean(string='Es Extra', default=False)
    state_extra = fields.Selection([
        ('pendiente', 'Pendiente'),
        ('aprobado', 'Aprobado'),
        ('rechazado', 'Rechazado')
    ], string='Estado Extra', default='pendiente')
    agregado_por_cliente = fields.Boolean(string='Solicitado por Cliente', default=False)


    @api.onchange('producto_id')
    def _onchange_producto_id(self):
        if self.producto_id:
            self.precio_unitario = self.producto_id.list_price

    @api.depends('cantidad', 'precio_unitario')
    def _compute_subtotal(self):
        for line in self:
            line.subtotal = line.cantidad * line.precio_unitario

class TallerOrdenTrabajo(models.Model):
    _name = 'taller.orden.trabajo'
    _description = 'Orden de Trabajo'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Código', default='NUEVA', copy=False, readonly=True, tracking=True)
    vehiculo_id = fields.Many2one('taller.vehiculo', string='Vehículo', required=True, tracking=True)
    cita_id = fields.Many2one('taller.cita', string='Cita Base', tracking=True)
    prioridad = fields.Selection(related='cita_id.prioridad', string='Prioridad')
    
    tecnico_id = fields.Many2one('hr.employee', string='Técnico Asignado', tracking=True, domain="['|', ('job_title', 'ilike', 'tecnico'), ('job_title', 'ilike', 'técnico')]")
    tecnico_cargo = fields.Char(string='Cargo del Técnico', related='tecnico_id.job_title', readonly=True)
    
    fecha_ingreso = fields.Datetime(string='Fecha de Ingreso', default=fields.Datetime.now, tracking=True)
    diagnostico = fields.Text(string='Diagnóstico')
    notas_cliente_propuesta = fields.Text(string='Notas/Peticiones del Cliente')
    
    servicio_linea_ids = fields.One2many('taller.orden.linea.servicio', 'orden_id', string='Servicios Realizados')
    repuesto_linea_ids = fields.One2many('taller.orden.linea.repuesto', 'orden_id', string='Repuestos Utilizados')
    propuesta_ids = fields.One2many('taller.propuesta', 'orden_id', string='Historial de Propuestas')
    
    costo_mano_obra = fields.Float(string='Costo Técnico Fijo', tracking=True)
    
    costo_total_servicios = fields.Float(string='Total Servicios', compute='_compute_totales', store=True)
    costo_total_repuestos = fields.Float(string='Total Repuestos', compute='_compute_totales', store=True)
    costo_total_general = fields.Float(string='Gran Total', compute='_compute_totales', store=True, tracking=True)

    estado = fields.Selection([
        ('recibido', 'Recibido'),
        ('cotizacion_enviada', 'Propuesta Enviada'),
        ('cotizacion_devuelta', 'Propuesta Devuelta'),
        ('cotizacion_aprobada', 'Propuesta Aprobada'),
        ('listo', 'Listo'),
        ('entregado', 'Entregado')
    ], string='Estado', default='recibido', tracking=True, group_expand='_expand_estados')

    @api.model
    def _expand_estados(self, states, domain, order=None, **kwargs):
        return ['recibido', 'cotizacion_enviada', 'cotizacion_devuelta', 'cotizacion_aprobada', 'listo', 'entregado']

    # ==========================================
    # Checklist de Recepción
    # ==========================================
    nivel_gasolina = fields.Selection([
        ('reserva', 'Reserva'),
        ('cuarto', '1/4'),
        ('medio', '1/2'),
        ('tres_cuartos', '3/4'),
        ('lleno', 'Lleno')
    ], string='Nivel de Gasolina', default='medio', tracking=True)
    
    llanta_repuesto = fields.Boolean(string='Llanta de Repuesto', default=True)
    herramientas = fields.Boolean(string='Kit de Herramientas', default=True)
    gata = fields.Boolean(string='Gata Hidráulica', default=True)
    
    rayones_golpes = fields.Text(string='Rayones o Golpes Previos', help='Describa cualquier daño existente en la carrocería antes de ingresar al taller.')
    objetos_personales = fields.Text(string='Objetos Personales', help='Enumere los objetos de valor dejados dentro del vehículo.')

    factura_id = fields.Many2one('account.move', string='Factura', readonly=True, copy=False, tracking=True)
    factura_estado = fields.Selection(related='factura_id.state', string='Estado Factura', readonly=True)
    reminder_sent = fields.Boolean(string='Recordatorio Enviado', default=False, copy=False)


    kilometraje = fields.Integer(string='Kilometraje de Ingreso', default=0, tracking=True)
    proximo_kilometraje_mto = fields.Integer(string='Mantenimiento Próximo (km)', compute='_compute_proximo_mantenimiento', store=True)
    proxima_fecha_mto = fields.Date(string='Fecha Próximo Mantenimiento', compute='_compute_proximo_mantenimiento', store=True)

    @api.depends('kilometraje', 'fecha_ingreso')
    def _compute_proximo_mantenimiento(self):
        from datetime import timedelta
        for orden in self:
            if orden.kilometraje:
                orden.proximo_kilometraje_mto = orden.kilometraje + 5000
            else:
                orden.proximo_kilometraje_mto = 0
            
            if orden.fecha_ingreso:
                orden.proxima_fecha_mto = (orden.fecha_ingreso + timedelta(days=180)).date()
            else:
                orden.proxima_fecha_mto = False

    @api.onchange('vehiculo_id')
    def _onchange_vehiculo_id_kilometraje(self):
        if self.vehiculo_id:
            self.kilometraje = self.vehiculo_id.kilometraje

    @api.depends('servicio_linea_ids.subtotal', 'servicio_linea_ids.is_extra', 'servicio_linea_ids.state_extra',
                 'repuesto_linea_ids.subtotal', 'repuesto_linea_ids.is_extra', 'repuesto_linea_ids.state_extra', 'costo_mano_obra')
    def _compute_totales(self):
        for orden in self:
            orden.costo_total_servicios = sum(line.subtotal for line in orden.servicio_linea_ids if line.state_extra != 'rechazado')
            orden.costo_total_repuestos = sum(line.subtotal for line in orden.repuesto_linea_ids if line.state_extra != 'rechazado')
            orden.costo_total_general = orden.costo_total_servicios + orden.costo_total_repuestos + orden.costo_mano_obra


    # ==========================================
    # Botones de Transición de Estado
    # ==========================================

    def action_enviar_propuesta(self):
        for orden in self:
            if not orden.servicio_linea_ids and not orden.repuesto_linea_ids:
                raise UserError('Debe registrar al menos un servicio o repuesto para enviar una propuesta.')
            # Marcar todas las líneas como pendientes si no tienen estado de aprobación
            for l in orden.servicio_linea_ids:
                if not l.state_extra:
                    l.state_extra = 'pendiente'
            for l in orden.repuesto_linea_ids:
                if not l.state_extra:
                    l.state_extra = 'pendiente'
            orden.estado = 'cotizacion_enviada'
            
            # Crear un registro de propuesta automático
            user_name = self.env.user.name or 'Taller Mecánico'
            prop_vals = {
                'orden_id': orden.id,
                'fecha': fields.Datetime.now(),
                'creador_tipo': 'taller',
                'creador_nombre': user_name,
                'notas': 'Se ha enviado la propuesta de trabajo con los servicios y repuestos detallados.',
                'linea_servicio_ids': [(0, 0, {
                    'producto_id': l.producto_id.id,
                    'cantidad': l.cantidad,
                    'precio_unitario': l.precio_unitario or l.producto_id.list_price,
                }) for l in orden.servicio_linea_ids],
                'linea_repuesto_ids': [(0, 0, {
                    'producto_id': l.producto_id.id,
                    'cantidad': l.cantidad,
                    'precio_unitario': l.precio_unitario or l.producto_id.list_price,
                }) for l in orden.repuesto_linea_ids],
            }
            self.env['taller.propuesta'].create(prop_vals)
            
            orden.message_post(body="La propuesta ha sido enviada al cliente para su revisión.")

    def action_aprobar_propuesta(self):
        for orden in self:
            orden.estado = 'cotizacion_aprobada'
            orden.message_post(body="La propuesta ha sido aprobada (forzada internamente).")


    def action_listo(self):
        """Cotización Aprobada -> Listo. Requiere al menos un servicio o repuesto."""
        for orden in self:
            if orden.estado != 'cotizacion_aprobada':
                raise UserError('No se puede marcar como listo hasta que la propuesta haya sido aprobada por el cliente (Estado: Propuesta Aprobada).')
            if not orden.kilometraje or orden.kilometraje <= 0:
                raise UserError('Debe ingresar el kilometraje actual del vehículo en la hoja de trabajo antes de marcar la orden como lista.')
            if not orden.servicio_linea_ids and not orden.repuesto_linea_ids and not orden.costo_mano_obra:
                raise UserError('Debe registrar al menos un servicio, repuesto o costo de mano de obra antes de marcar como listo.')
            orden.estado = 'listo'
            if orden.vehiculo_id and orden.kilometraje > orden.vehiculo_id.kilometraje:
                orden.vehiculo_id.kilometraje = orden.kilometraje
            try:
                orden._send_vehicle_ready_email()
            except Exception as e:
                # Registrar error pero no bloquear el estado operativo
                orden.message_post(body=f"⚠️ Error al enviar correo de vehículo listo: {str(e)}")

    def _send_vehicle_ready_email(self):
        self.ensure_one()
        propietario = self.vehiculo_id.propietario_id
        partner = propietario.partner_id if propietario else False
        if not partner or not partner.email:
            return False

        # Desglose de servicios y repuestos
        servicios_html = ""
        for line in self.servicio_linea_ids:
            servicios_html += f"<tr><td style='padding: 6px 0; color: #334155;'>• {line.producto_id.name}</td><td style='padding: 6px 0; text-align: right; color: #0f172a; font-weight: 600;'>${line.subtotal:.2f}</td></tr>"
        
        repuestos_html = ""
        for line in self.repuesto_linea_ids:
            repuestos_html += f"<tr><td style='padding: 6px 0; color: #334155;'>• {line.producto_id.name} (x{int(line.cantidad)})</td><td style='padding: 6px 0; text-align: right; color: #0f172a; font-weight: 600;'>${line.subtotal:.2f}</td></tr>"

        body_html = f"""
        <div style="font-family: 'Inter', Helvetica, Arial, sans-serif; max-width: 600px; margin: 0 auto; border: 1px solid #e2e8f0; border-radius: 12px; overflow: hidden; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.05), 0 2px 4px -1px rgba(0,0,0,0.03);">
            <div style="background: linear-gradient(135deg, #10b981, #059669); padding: 30px; text-align: center; color: white;">
                <h1 style="margin: 0; font-size: 24px; font-weight: 700; letter-spacing: -0.025em;">¡Su Vehículo está Listo!</h1>
                <p style="margin: 6px 0 0 0; color: #d1fae5; font-size: 14px;">Los trabajos de reparación han concluido con éxito</p>
            </div>
            <div style="padding: 30px; background-color: white;">
                <p style="font-size: 15px; color: #334155; line-height: 1.6; margin: 0 0 20px 0;">
                    Estimado(a) <strong>{partner.name}</strong>,
                </p>
                <p style="font-size: 14px; color: #475569; line-height: 1.6; margin: 0 0 20px 0;">
                    Nos complace informarle que los trabajos de mantenimiento y reparación de su vehículo han concluido. Su auto se encuentra en estado <strong>Listo para Retirar</strong>.
                </p>
                
                <div style="background-color: #f8fafc; border: 1px solid #e2e8f0; border-radius: 8px; padding: 16px; margin-bottom: 20px;">
                    <h3 style="margin: 0 0 10px 0; font-size: 14px; color: #0f172a; text-transform: uppercase; letter-spacing: 0.05em; font-weight: 700;">Resumen del Vehículo</h3>
                    <table style="width: 100%; font-size: 13px; border-collapse: collapse;">
                        <tr>
                            <td style="padding: 3px 0; color: #64748b;">Vehículo:</td>
                            <td style="padding: 3px 0; color: #0f172a; font-weight: 600; text-align: right;">{self.vehiculo_id.marca_id.name} {self.vehiculo_id.modelo_id.name}</td>
                        </tr>
                        <tr>
                            <td style="padding: 3px 0; color: #64748b;">Placa:</td>
                            <td style="padding: 3px 0; color: #0f172a; font-weight: 600; text-align: right;">{self.vehiculo_id.placa}</td>
                        </tr>
                        <tr>
                            <td style="padding: 3px 0; color: #64748b;">Orden Nro:</td>
                            <td style="padding: 3px 0; color: #0f172a; font-weight: 600; text-align: right;">{self.name}</td>
                        </tr>
                    </table>
                </div>

                <div style="margin-bottom: 20px;">
                    <h3 style="margin: 0 0 10px 0; font-size: 14px; color: #0f172a; text-transform: uppercase; letter-spacing: 0.05em; font-weight: 700; border-bottom: 1px solid #e2e8f0; padding-bottom: 4px;">Trabajos Realizados</h3>
                    <table style="width: 100%; font-size: 13px; border-collapse: collapse;">
                        {servicios_html}
                        {repuestos_html}
                        <tr>
                            <td style="padding: 8px 0; color: #0f172a; font-weight: 700; border-top: 1px solid #e2e8f0;">Total Acumulado:</td>
                            <td style="padding: 8px 0; text-align: right; color: #10b981; font-weight: 700; font-size: 15px; border-top: 1px solid #e2e8f0;">${self.costo_total_general:.2f}</td>
                        </tr>
                    </table>
                </div>

                <div style="background-color: #ecfdf5; border: 1px solid #a7f3d0; border-radius: 8px; padding: 16px; font-size: 13px; color: #065f46; line-height: 1.5; margin-bottom: 10px;">
                    <strong>🕒 Horarios de Atención para Retiro:</strong><br/>
                    Lunes a Viernes de 8:00 AM a 6:00 PM. Sábados de 8:00 AM a 1:00 PM.
                </div>
            </div>
            <div style="border-top: 1px solid #f1f5f9; padding-top: 20px; font-size: 13px; color: #94a3b8; text-align: center; line-height: 1.5; padding-bottom: 20px; background-color: #fafafa;">
                <p style="margin: 0 0 5px 0;">¡Que tenga un excelente viaje!</p>
                <p style="margin: 0; font-weight: 600; color: #64748b;">{self.env.company.name}</p>
            </div>
        </div>
        """
        mail_values = {
            'subject': f"¡Su vehículo {self.vehiculo_id.placa} está listo para ser retirado!",
            'body_html': body_html,
            'email_to': partner.email,
        }
        self.env['mail.mail'].create(mail_values).send()
        self.message_post(body=f"📧 Correo de notificación de vehículo listo enviado con éxito a {partner.email}.")
        return True

    def action_facturar(self):
        """Genera una factura de cliente (account.move) con las líneas de la orden."""
        self.ensure_one()
        if self.factura_id:
            raise UserError('Esta orden ya tiene una factura generada.')

        # Obtener el partner del propietario del vehículo
        propietario = self.vehiculo_id.propietario_id
        if not propietario:
            raise UserError('El vehículo no tiene propietario asignado.')
        
        partner = propietario.partner_id
        if not partner:
            # Crear partner si no existe
            partner = self.env['res.partner'].create({
                'name': f"{propietario.nombre} {propietario.apellido}",
                'email': propietario.email,
                'phone': propietario.celular,
                'street': propietario.direccion,
                'vat': propietario.cedula,
                'company_type': 'person',
                'lang': 'es_EC',
            })
            propietario.partner_id = partner.id

        # Construir líneas de factura
        invoice_lines = []

        # Líneas de servicios
        for linea in self.servicio_linea_ids:
            if linea.state_extra == 'rechazado':
                continue
            invoice_lines.append((0, 0, {
                'product_id': linea.producto_id.id,
                'name': linea.producto_id.name,
                'quantity': linea.cantidad,
                'price_unit': linea.precio_unitario,
            }))

        # Líneas de repuestos
        for linea in self.repuesto_linea_ids:
            if linea.state_extra == 'rechazado':
                continue
            invoice_lines.append((0, 0, {
                'product_id': linea.producto_id.id,
                'name': linea.producto_id.name,
                'quantity': linea.cantidad,
                'price_unit': linea.precio_unitario,
            }))

        # Línea de mano de obra (si hay costo fijo)
        if self.costo_mano_obra > 0:
            invoice_lines.append((0, 0, {
                'name': f'Mano de Obra - {self.name}',
                'quantity': 1,
                'price_unit': self.costo_mano_obra,
            }))

        if not invoice_lines:
            raise UserError('No hay líneas para facturar. Agregue servicios, repuestos o costo de mano de obra.')

        # Crear la factura
        factura = self.env['account.move'].create({
            'move_type': 'out_invoice',
            'partner_id': partner.id,
            'invoice_origin': self.name,
            'narration': f'Orden de Trabajo: {self.name}\nVehículo: {self.vehiculo_id.placa}\nDiagnóstico: {self.diagnostico or "N/A"}',
            'invoice_line_ids': invoice_lines,
        })

        self.factura_id = factura.id
        
        # Confirmar la factura automáticamente
        factura.action_post()
        self.message_post(body=f"Factura {factura.name} generada y confirmada exitosamente.")

        # Regresar a la misma orden de trabajo actual
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'taller.orden.trabajo',
            'res_id': self.id,
            'view_mode': 'form',
            'views': [(False, 'form')],
            'target': 'current',
        }

    def action_entregado(self):
        """Listo -> Entregado."""
        for orden in self:
            if not orden.factura_id:
                raise UserError('No se puede entregar el vehículo hasta que un administrador haya generado la factura respectiva.')
            orden.estado = 'entregado'

    def action_ver_factura(self):
        """Abrir la factura vinculada."""
        self.ensure_one()
        if not self.factura_id:
            raise UserError('No hay factura vinculada a esta orden.')
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'account.move',
            'res_id': self.factura_id.id,
            'views': [(False, 'form')],
            'target': 'current',
        }

    def get_state_history(self):
        self.ensure_one()
        history = []
        
        # 1. Cita asociada
        if self.cita_id:
            history.append({
                'date': self.cita_id.create_date,
                'description': 'Cita Solicitada (Creada)',
                'author': self.cita_id.create_uid.name or 'Cliente',
                'type': 'cita'
            })
            
            try:
                messages = self.env['mail.message'].sudo().search([
                    ('model', '=', 'taller.cita'),
                    ('res_id', '=', self.cita_id.id),
                ])
                for msg in messages:
                    for track in msg.tracking_value_ids:
                        field_name = track.field_id.name if track.field_id else ''
                        if field_name == 'estado':
                            old_val = track.old_value_char or ''
                            new_val = track.new_value_char or ''
                            state_labels = {
                                'solicitada': 'Solicitada',
                                'confirmada': 'Confirmada',
                                'cancelada': 'Cancelada'
                            }
                            old_label = state_labels.get(old_val.lower(), old_val)
                            new_label = state_labels.get(new_val.lower(), new_val)
                            
                            history.append({
                                'date': msg.date,
                                'description': f"Cita cambió de '{old_label}' a '{new_label}'",
                                'author': msg.author_id.name or 'Sistema',
                                'type': 'cita'
                            })
            except Exception as e:
                pass
                
        # 2. Orden de Trabajo
        history.append({
            'date': self.create_date,
            'description': 'Orden de Trabajo Recibida (Creada)',
            'author': self.create_uid.name or 'Sistema',
            'type': 'orden'
        })
        
        try:
            messages_ot = self.env['mail.message'].sudo().search([
                ('model', '=', 'taller.orden.trabajo'),
                ('res_id', '=', self.id),
            ])
            for msg in messages_ot:
                for track in msg.tracking_value_ids:
                    field_name = track.field_id.name if track.field_id else ''
                    if field_name == 'estado':
                        old_val = track.old_value_char or ''
                        new_val = track.new_value_char or ''
                        state_labels_ot = {
                            'recibido': 'Recibido',
                            'listo': 'Listo',
                            'entregado': 'Entregado'
                        }
                        old_label = state_labels_ot.get(old_val.lower(), old_val)
                        new_label = state_labels_ot.get(new_val.lower(), new_val)
                        
                        history.append({
                            'date': msg.date,
                            'description': f"Orden de Trabajo cambió de '{old_label}' a '{new_label}'",
                            'author': msg.author_id.name or 'Sistema',
                            'type': 'orden'
                        })
        except Exception as e:
            pass
            
        history = sorted(history, key=lambda x: x['date'])
        return history
