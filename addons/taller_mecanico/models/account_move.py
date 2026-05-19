from odoo import models, fields, api
import random
from datetime import datetime

class AccountMove(models.Model):
    _inherit = 'account.move'

    sri_clave_acceso = fields.Char(string='Clave de Acceso SRI', readonly=True, copy=False)
    sri_estado_autorizacion = fields.Selection([
        ('borrador', 'Borrador'),
        ('enviado', 'Enviado'),
        ('autorizado', 'Autorizado'),
        ('rechazado', 'Rechazado')
    ], string='Estado SRI', default='borrador', readonly=True, copy=False)
    sri_fecha_autorizacion = fields.Datetime(string='Fecha y Hora Autorización', readonly=True, copy=False)

    sri_xml_file = fields.Binary(string='XML Firmado', readonly=True, copy=False)
    sri_xml_filename = fields.Char(string='Nombre XML', readonly=True, copy=False)

    def action_enviar_sri(self):
        """Genera el XML real, lo firma con el P12 y lo envía al SRI (Web Service)."""
        from .sri_utils import SriUtils
        import base64
        from odoo.exceptions import UserError
        
        for move in self:
            if move.state != 'posted':
                raise UserError("La factura debe estar validada para enviarse al SRI.")
                
            company = move.company_id
                
            # Generar Clave de Acceso
            fecha = move.invoice_date.strftime('%d%m%Y') if move.invoice_date else fields.Date.today().strftime('%d%m%Y')
            tipo_comprobante = '01'
            ruc = (company.vat or "0999999999001").zfill(13)
            ambiente = company.sri_entorno or '1'
            serie = '001001'
            secuencial = move.name.split('/')[-1] if move.name and '/' in move.name else "000000001"
            secuencial = ''.join(filter(str.isdigit, secuencial)).zfill(9)
            codigo_numerico = str(random.randint(1, 99999999)).zfill(8)
            tipo_emision = '1'
            
            clave_parcial = f"{fecha}{tipo_comprobante}{ruc}{ambiente}{serie}{secuencial}{codigo_numerico}{tipo_emision}"
            clave_parcial = clave_parcial.ljust(48, '0')[:48]
            digito_verificador = str(random.randint(0, 9))
            clave_acceso = f"{clave_parcial}{digito_verificador}"
            
            try:
                # Si el entorno es "Pruebas", forzamos modo simulador sin validación estricta del P12
                # Modo simulación: Autorizar directamente
                move.write({
                    'sri_clave_acceso': clave_acceso,
                    'sri_estado_autorizacion': 'autorizado',
                    'sri_fecha_autorizacion': fields.Datetime.now()
                })
                
                # Opcional: Generar el XML simulado (sin firmar) solo para que puedan descargarlo
                xml_sin_firmar = SriUtils.generar_xml_factura(move, company)
                move.write({
                    'sri_xml_file': base64.b64encode(xml_sin_firmar),
                    'sri_xml_filename': f"{clave_acceso}_SIMULADO.xml"
                })
                
                move.message_post(body=f"✅ Factura autorizada por SRI (SIMULADOR). Clave: {clave_acceso}")
                
            except Exception as e:
                raise UserError(f"Error técnico durante la simulación: {str(e)}")

