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

    def action_post(self):
        """Sobrescribe la confirmación nativa de la factura para enviar automáticamente al SRI."""
        res = super(AccountMove, self).action_post()
        for move in self:
            if move.move_type == 'out_invoice':
                try:
                    move.action_enviar_sri()
                except Exception as e:
                    # Capturar cualquier error para no bloquear la confirmación contable local de Odoo
                    move.message_post(body=f"⚠️ La facturación automática del SRI falló: {str(e)}. "
                                           f"Puedes intentar de nuevo manualmente usando el botón 'Generar y Firmar XML (SRI)'.")
        return res

    def action_enviar_sri(self):
        """Genera el XML real, lo firma con el P12 y lo envía y autoriza ante el SRI de Ecuador."""
        from .sri_utils import SriUtils
        import base64
        import random
        from odoo.exceptions import UserError
        from dateutil import parser
        import pytz
        
        for move in self:
            if move.state != 'posted':
                raise UserError("La factura debe estar validada (Publicada) para enviarse al SRI.")
                
            company = move.company_id
            if not company.sri_firma_p12:
                raise UserError("Por favor, configure el archivo de firma electrónica (.p12) en la configuración de la compañía (pestaña SRI Ecuador).")
            if not company.sri_firma_password:
                raise UserError("Por favor, configure la contraseña de la firma electrónica en la configuración de la compañía.")
                
            # Validar que tenga al menos una línea de detalle real (no sección ni nota)
            lineas_validas = move.invoice_line_ids.filtered(lambda l: l.display_type not in ('line_section', 'line_note'))
            if not lineas_validas:
                raise UserError("La factura debe contener al menos una línea de producto o servicio (detalle) para poder ser procesada y enviada al SRI.")
                
            # --- Generar o Reutilizar Clave de Acceso ---
            ambiente = company.sri_entorno or '1'
            if move.sri_clave_acceso:
                clave_acceso = move.sri_clave_acceso
                move.write({'sri_estado_autorizacion': 'enviado'})
            else:
                fecha = move.invoice_date.strftime('%d%m%Y') if move.invoice_date else fields.Date.today().strftime('%d%m%Y')
                tipo_comprobante = '01' # Factura
                ruc = (company.vat or "0999999999001").zfill(13)
                serie = '001001' # Establecimiento 001 + Punto de Emisión 001
                
                # Secuencial (9 dígitos)
                nombre = move.name or ""
                partes = nombre.replace('/', '-').split('-')
                secuencial = partes[-1] if partes else "000000001"
                secuencial = ''.join(filter(str.isdigit, secuencial)).zfill(9)
                
                # Código numérico aleatorio de 8 dígitos para mayor seguridad
                codigo_numerico = str(random.randint(1, 99999999)).zfill(8)
                tipo_emision = '1' # Normal
                
                clave_parcial = f"{fecha}{tipo_comprobante}{ruc}{ambiente}{serie}{secuencial}{codigo_numerico}{tipo_emision}"
                clave_parcial = clave_parcial.ljust(48, '0')[:48]
                
                # Calcular Dígito Verificador Módulo 11 Real
                digito_verificador = SriUtils.calcular_modulo_11(clave_parcial)
                clave_acceso = f"{clave_parcial}{digito_verificador}"
                
                # Guardar Clave de Acceso preliminar
                move.write({
                    'sri_clave_acceso': clave_acceso,
                    'sri_estado_autorizacion': 'enviado'
                })
            
            # --- Generar XML de la Factura ---
            try:
                xml_sin_firmar = SriUtils.generar_xml_factura(move, company)
            except Exception as e:
                move.write({'sri_estado_autorizacion': 'borrador'})
                raise UserError(f"Error al generar el XML de la factura: {str(e)}")
                
            # --- Firmar XML con XAdES-BES ---
            try:
                xml_firmado = SriUtils.firmar_xml(xml_sin_firmar, company.sri_firma_p12, company.sri_firma_password)
            except Exception as e:
                move.write({'sri_estado_autorizacion': 'borrador'})
                raise UserError(f"Error al firmar el XML con XAdES-BES: {str(e)}")
                
            # --- Transmitir a SRI Recepción ---
            estado_rec, mensajes_rec = SriUtils.transmitir_sri_recepcion(xml_firmado, ambiente)
            
            if estado_rec not in ("RECEPCIONADO", "RECIBIDA"):
                error_txt = "\n".join(mensajes_rec)
                move.write({'sri_estado_autorizacion': 'rechazado'})
                move.message_post(body=f"❌ SRI Recepción rechazó el comprobante. Detalles:\n{error_txt}")
                raise UserError(f"El SRI rechazó el comprobante durante la recepción:\n{error_txt}")
                
            # --- Transmitir a SRI Autorización (Con reintentos por latencia) ---
            import time
            intentos = 0
            while intentos < 4:
                time.sleep(2.5) # Esperar a que el SRI procese el documento
                estado_aut, fecha_aut, xml_aut, mensajes_aut = SriUtils.transmitir_sri_autorizacion(clave_acceso, ambiente)
                if estado_aut != "EN_PROCESAMIENTO":
                    break
                intentos += 1
            
            if estado_aut == "AUTORIZADO":
                # Convertir fecha de autorización a formato UTC datetime para Odoo
                fecha_aut_dt = fields.Datetime.now()
                if fecha_aut:
                    try:
                        dt = parser.parse(fecha_aut)
                        if dt.tzinfo:
                            dt = dt.astimezone(pytz.utc)
                        fecha_aut_dt = dt.replace(tzinfo=None)
                    except Exception:
                        pass
                
                # Guardar XML autorizado final y actualizar estado
                move.write({
                    'sri_estado_autorizacion': 'autorizado',
                    'sri_fecha_autorizacion': fecha_aut_dt,
                    'sri_xml_file': base64.b64encode(xml_aut if xml_aut else xml_firmado),
                    'sri_xml_filename': f"{clave_acceso}.xml"
                })
                move.message_post(body=f"✅ Factura AUTORIZADA por el SRI. Clave de Acceso: {clave_acceso}")
                
                # --- Enviar Correo con XML y PDF ---
                try:
                    move._send_sri_invoice_email()
                except Exception as mail_err:
                    move.message_post(body=f"⚠️ No se pudo enviar el correo de la factura automáticamente: {str(mail_err)}")
            else:
                error_txt = "\n".join(mensajes_aut)
                move.write({'sri_estado_autorizacion': 'rechazado'})
                move.message_post(body=f"❌ SRI Autorización rechazó/devolvió el comprobante. Detalles:\n{error_txt}")
                raise UserError(f"El SRI no autorizó el comprobante:\n{error_txt}")

    def _send_sri_invoice_email(self):
        """Genera el PDF de Odoo y envía por correo la factura con los adjuntos XML y PDF."""
        import base64
        self.ensure_one()
        partner = self.partner_id
        if not partner.email:
            self.message_post(body="⚠️ El cliente no tiene un correo electrónico configurado. No se pudo enviar el comprobante automáticamente.")
            return False
            
        # 1. Generar Adjunto XML
        if not self.sri_xml_file:
            self.message_post(body="⚠️ No se encontró el archivo XML firmado para adjuntar al correo.")
            return False
            
        xml_attachment = self.env['ir.attachment'].create({
            'name': self.sri_xml_filename or f"{self.sri_clave_acceso}.xml",
            'type': 'binary',
            'datas': self.sri_xml_file,
            'res_model': 'account.move',
            'res_id': self.id,
            'mimetype': 'application/xml',
        })
        
        # 2. Generar Adjunto PDF
        pdf_data, _ = self.env['ir.actions.report']._render_qweb_pdf('account.account_invoices', [self.id])
        pdf_b64 = base64.b64encode(pdf_data)
        pdf_attachment = self.env['ir.attachment'].create({
            'name': f"{self.name.replace('/', '_')}.pdf",
            'type': 'binary',
            'datas': pdf_b64,
            'res_model': 'account.move',
            'res_id': self.id,
            'mimetype': 'application/pdf',
        })
        
        # 3. Preparar el HTML del correo
        invoice_date_str = self.invoice_date.strftime('%d/%m/%Y') if self.invoice_date else fields.Date.today().strftime('%d/%m/%Y')
        body_html = f"""
        <div style="font-family: 'Inter', Helvetica, Arial, sans-serif; max-width: 600px; margin: auto; padding: 20px; border: 1px solid #e2e8f0; border-radius: 12px; background-color: #ffffff; color: #1e293b; box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);">
            <div style="text-align: center; padding-bottom: 20px; border-bottom: 2px solid #f1f5f9;">
                <h2 style="color: #0f172a; margin: 0; font-size: 24px; font-weight: 700; letter-spacing: -0.025em;">Factura Electrónica</h2>
                <p style="color: #64748b; margin: 5px 0 0 0; font-size: 14px;">Taller Mecánico Automotriz</p>
            </div>
            <div style="padding: 20px 0;">
                <p style="font-size: 16px; line-height: 1.6; margin: 0 0 16px 0;">Estimado(a) <strong>{partner.name}</strong>,</p>
                <p style="font-size: 15px; line-height: 1.6; margin: 0 0 20px 0; color: #334155;">
                    Le informamos que su comprobante electrónico ha sido generado exitosamente y autorizado por el <strong>SRI (Servicio de Rentas Internas)</strong> bajo el ambiente de pruebas.
                </p>
                
                <div style="background-color: #f8fafc; border: 1px solid #e2e8f0; border-radius: 8px; padding: 16px; margin-bottom: 20px;">
                    <table style="width: 100%; font-size: 14px; border-collapse: collapse;">
                        <tr>
                            <td style="padding: 4px 0; color: #64748b; font-weight: 500;">Factura Nro:</td>
                            <td style="padding: 4px 0; color: #0f172a; font-weight: 600; text-align: right;">{self.name}</td>
                        </tr>
                        <tr>
                            <td style="padding: 4px 0; color: #64748b; font-weight: 500;">Fecha Emisión:</td>
                            <td style="padding: 4px 0; color: #0f172a; font-weight: 600; text-align: right;">{invoice_date_str}</td>
                        </tr>
                        <tr>
                            <td style="padding: 4px 0; color: #64748b; font-weight: 500;">Total a Pagar:</td>
                            <td style="padding: 4px 0; color: #10b981; font-weight: 700; font-size: 16px; text-align: right;">${self.amount_total:.2f}</td>
                        </tr>
                    </table>
                </div>

                <div style="margin-bottom: 20px;">
                    <p style="font-size: 13px; font-weight: 600; color: #64748b; margin: 0 0 6px 0; text-transform: uppercase; letter-spacing: 0.05em;">Clave de Acceso SRI:</p>
                    <div style="background-color: #f1f5f9; font-family: monospace; font-size: 12px; padding: 10px 14px; border-radius: 6px; border: 1px solid #e2e8f0; word-break: break-all; color: #334155; line-height: 1.4; letter-spacing: 0.025em; text-align: center;">
                        {self.sri_clave_acceso}
                    </div>
                </div>

                <p style="font-size: 14px; line-height: 1.6; color: #475569; margin: 0 0 20px 0;">
                    Adjunto a este correo encontrará la representación impresa de su factura en formato <strong>PDF</strong> y el archivo digital <strong>XML</strong> autorizado por el SRI.
                </p>
            </div>
            <div style="border-top: 1px solid #f1f5f9; padding-top: 20px; font-size: 13px; color: #94a3b8; text-align: center; line-height: 1.5;">
                <p style="margin: 0 0 5px 0;">Gracias por confiar en nosotros.</p>
                <p style="margin: 0; font-weight: 600; color: #64748b;">{self.company_id.name}</p>
            </div>
        </div>
        """
        
        # 4. Crear y enviar el mail
        mail_values = {
            'subject': f"Factura Electrónica Autorizada - {self.name}",
            'body_html': body_html,
            'email_to': partner.email,
            'attachment_ids': [(6, 0, [xml_attachment.id, pdf_attachment.id])],
        }
        
        mail = self.env['mail.mail'].create(mail_values)
        mail.send()
        
        self.message_post(body=f"📧 Correo electrónico enviado al cliente ({partner.email}) con los comprobantes XML y PDF adjuntos.")
        return True

    def action_descargar_xml_masivo(self):
        """Filtra las facturas seleccionadas que tienen XML y retorna la URL de descarga del ZIP."""
        from odoo.exceptions import UserError
        invoices_with_xml = self.filtered(lambda m: m.sri_xml_file)
        if not invoices_with_xml:
            raise UserError("Ninguna de las facturas seleccionadas posee un archivo XML autorizado del SRI.")
        
        ids_str = ','.join(str(i) for i in invoices_with_xml.ids)
        return {
            'type': 'ir.actions.act_url',
            'url': f'/sri/download_xml_zip?ids={ids_str}',
            'target': 'self',
        }


