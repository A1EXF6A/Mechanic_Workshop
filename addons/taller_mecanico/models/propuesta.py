from odoo import models, fields, api

class TallerPropuesta(models.Model):
    _name = 'taller.propuesta'
    _description = 'Propuesta de Trabajo'
    _order = 'id desc'

    orden_id = fields.Many2one('taller.orden.trabajo', string='Orden de Trabajo', required=True, ondelete='cascade')
    fecha = fields.Datetime(string='Fecha', default=fields.Datetime.now, required=True)
    creador_tipo = fields.Selection([
        ('cliente', 'Cliente'),
        ('taller', 'Taller / Técnico')
    ], string='Tipo de Creador', default='taller', required=True)
    creador_nombre = fields.Char(string='Nombre del Creador', required=True)
    notas = fields.Text(string='Notas / Comentarios')
    
    linea_servicio_ids = fields.One2many('taller.propuesta.linea.servicio', 'propuesta_id', string='Servicios Propuestos')
    linea_repuesto_ids = fields.One2many('taller.propuesta.linea.repuesto', 'propuesta_id', string='Repuestos Propuestos')

class TallerPropuestaLineaServicio(models.Model):
    _name = 'taller.propuesta.linea.servicio'
    _description = 'Servicio Propuesto'

    propuesta_id = fields.Many2one('taller.propuesta', string='Propuesta', required=True, ondelete='cascade')
    producto_id = fields.Many2one('product.product', string='Servicio', domain="[('type', '=', 'service')]", required=True)
    cantidad = fields.Float(string='Cantidad', default=1.0)
    precio_unitario = fields.Float(string='Precio Unitario')
    subtotal = fields.Float(string='Subtotal', compute='_compute_subtotal', store=True)

    @api.onchange('producto_id')
    def _onchange_producto_id(self):
        if self.producto_id:
            self.precio_unitario = self.producto_id.list_price

    @api.depends('cantidad', 'precio_unitario')
    def _compute_subtotal(self):
        for line in self:
            line.subtotal = line.cantidad * line.precio_unitario

class TallerPropuestaLineaRepuesto(models.Model):
    _name = 'taller.propuesta.linea.repuesto'
    _description = 'Repuesto Propuesto'

    propuesta_id = fields.Many2one('taller.propuesta', string='Propuesta', required=True, ondelete='cascade')
    producto_id = fields.Many2one('product.product', string='Repuesto', domain="[('type', '!=', 'service')]", required=True)
    cantidad = fields.Float(string='Cantidad', default=1.0)
    precio_unitario = fields.Float(string='Precio Unitario')
    subtotal = fields.Float(string='Subtotal', compute='_compute_subtotal', store=True)

    @api.onchange('producto_id')
    def _onchange_producto_id(self):
        if self.producto_id:
            self.precio_unitario = self.producto_id.list_price

    @api.depends('cantidad', 'precio_unitario')
    def _compute_subtotal(self):
        for line in self:
            line.subtotal = line.cantidad * line.precio_unitario
