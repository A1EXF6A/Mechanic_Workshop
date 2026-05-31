from odoo import models, fields

class ResCompany(models.Model):
    _inherit = 'res.company'

    sri_entorno = fields.Selection([
        ('1', 'Pruebas'),
        ('2', 'Producción')
    ], string='Ambiente SRI', default='1', required=True)
    
    sri_firma_p12 = fields.Binary(string='Firma Electrónica (.p12)', attachment=False)
    sri_firma_password = fields.Char(string='Contraseña de la Firma')
    
    sri_obligado_contabilidad = fields.Selection([
        ('SI', 'SI'),
        ('NO', 'NO')
    ], string='Obligado a llevar contabilidad', default='NO')
    
    sri_resolucion_contribuyente = fields.Char(string='Resolución Contribuyente Especial (Opcional)')
    sri_agente_retencion = fields.Char(string='Agente de Retención (Resolución)')
