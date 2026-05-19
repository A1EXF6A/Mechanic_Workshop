from odoo import models, fields, api
from odoo.exceptions import UserError

class TallerOrdenLineaServicio(models.Model):
    _name = 'taller.orden.linea.servicio'
    _description = 'Línea de Servicio'

    orden_id = fields.Many2one('taller.orden.trabajo', string='Orden de Trabajo', required=True, ondelete='cascade')
    producto_id = fields.Many2one('product.product', string='Servicio', domain="[('type', '=', 'service')]", required=True)
    cantidad = fields.Float(string='Cantidad', default=1.0)
    precio_unitario = fields.Float(string='Precio Unitario', related='producto_id.list_price', readonly=False)
    subtotal = fields.Float(string='Subtotal', compute='_compute_subtotal', store=True)

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
    precio_unitario = fields.Float(string='Precio Unitario', related='producto_id.list_price', readonly=False)
    subtotal = fields.Float(string='Subtotal', compute='_compute_subtotal', store=True)

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
    
    servicio_linea_ids = fields.One2many('taller.orden.linea.servicio', 'orden_id', string='Servicios Realizados')
    repuesto_linea_ids = fields.One2many('taller.orden.linea.repuesto', 'orden_id', string='Repuestos Utilizados')
    
    costo_mano_obra = fields.Float(string='Costo Técnico Fijo', tracking=True)
    
    costo_total_servicios = fields.Float(string='Total Servicios', compute='_compute_totales', store=True)
    costo_total_repuestos = fields.Float(string='Total Repuestos', compute='_compute_totales', store=True)
    costo_total_general = fields.Float(string='Gran Total', compute='_compute_totales', store=True, tracking=True)

    estado = fields.Selection([
        ('recibido', 'Recibido'),
        ('proceso', 'En Proceso'),
        ('listo', 'Listo'),
        ('entregado', 'Entregado')
    ], string='Estado', default='recibido', tracking=True)

    factura_id = fields.Many2one('account.move', string='Factura', readonly=True, copy=False, tracking=True)
    factura_estado = fields.Selection(related='factura_id.state', string='Estado Factura', readonly=True)

    @api.depends('servicio_linea_ids.subtotal', 'repuesto_linea_ids.subtotal', 'costo_mano_obra')
    def _compute_totales(self):
        for orden in self:
            orden.costo_total_servicios = sum(orden.servicio_linea_ids.mapped('subtotal'))
            orden.costo_total_repuestos = sum(orden.repuesto_linea_ids.mapped('subtotal'))
            orden.costo_total_general = orden.costo_total_servicios + orden.costo_total_repuestos + orden.costo_mano_obra

    # ==========================================
    # Botones de Transición de Estado
    # ==========================================

    def action_en_proceso(self):
        """Recibido -> En Proceso. Requiere técnico asignado."""
        for orden in self:
            if not orden.tecnico_id:
                raise UserError('Debe asignar un técnico antes de iniciar el trabajo.')
            orden.estado = 'proceso'

    def action_listo(self):
        """En Proceso -> Listo. Requiere al menos un servicio o repuesto."""
        for orden in self:
            if not orden.servicio_linea_ids and not orden.repuesto_linea_ids and not orden.costo_mano_obra:
                raise UserError('Debe registrar al menos un servicio, repuesto o costo de mano de obra antes de marcar como listo.')
            orden.estado = 'listo'

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
            })
            propietario.partner_id = partner.id

        # Construir líneas de factura
        invoice_lines = []

        # Líneas de servicios
        for linea in self.servicio_linea_ids:
            invoice_lines.append((0, 0, {
                'product_id': linea.producto_id.id,
                'name': linea.producto_id.name,
                'quantity': linea.cantidad,
                'price_unit': linea.precio_unitario,
            }))

        # Líneas de repuestos
        for linea in self.repuesto_linea_ids:
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

        # Abrir la factura generada
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'account.move',
            'res_id': factura.id,
            'views': [(False, 'form')],
            'target': 'current',
        }

    def action_entregado(self):
        """Listo -> Entregado."""
        for orden in self:
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
