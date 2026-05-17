from odoo import models, fields, api

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
    
    tecnico_id = fields.Many2one('hr.employee', string='Técnico Asignado', tracking=True)
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

    @api.depends('servicio_linea_ids.subtotal', 'repuesto_linea_ids.subtotal', 'costo_mano_obra')
    def _compute_totales(self):
        for orden in self:
            orden.costo_total_servicios = sum(orden.servicio_linea_ids.mapped('subtotal'))
            orden.costo_total_repuestos = sum(orden.repuesto_linea_ids.mapped('subtotal'))
            orden.costo_total_general = orden.costo_total_servicios + orden.costo_total_repuestos + orden.costo_mano_obra
