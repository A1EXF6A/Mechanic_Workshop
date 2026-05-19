import base64
from lxml import etree
import xml.etree.ElementTree as ET
from signxml import XMLSigner
from cryptography.hazmat.primitives.serialization import pkcs12
import logging

_logger = logging.getLogger(__name__)

class SriUtils:
    
    @staticmethod
    def generar_xml_factura(move, company):
        """Genera el XML básico de una factura para el SRI."""
        # Namespace
        factura = etree.Element("factura", id="comprobante", version="2.1.0")
        
        # --- Info Tributaria ---
        infoTributaria = etree.SubElement(factura, "infoTributaria")
        etree.SubElement(infoTributaria, "ambiente").text = company.sri_entorno
        etree.SubElement(infoTributaria, "tipoEmision").text = "1"
        etree.SubElement(infoTributaria, "razonSocial").text = company.name or "Razón Social Pruebas"
        etree.SubElement(infoTributaria, "nombreComercial").text = company.name or "Nombre Comercial Pruebas"
        etree.SubElement(infoTributaria, "ruc").text = company.vat or "0999999999001"
        etree.SubElement(infoTributaria, "claveAcceso").text = move.sri_clave_acceso
        etree.SubElement(infoTributaria, "codDoc").text = "01"
        etree.SubElement(infoTributaria, "estab").text = "001"
        etree.SubElement(infoTributaria, "ptoEmi").text = "001"
        
        # Secuencial (9 digitos)
        secuencial = move.name.split('/')[-1] if move.name and '/' in move.name else "000000001"
        secuencial = ''.join(filter(str.isdigit, secuencial)).zfill(9)
        etree.SubElement(infoTributaria, "secuencial").text = secuencial
        etree.SubElement(infoTributaria, "dirMatriz").text = company.street or "Dir Matriz Prueba"
        
        # --- Info Factura ---
        infoFactura = etree.SubElement(factura, "infoFactura")
        etree.SubElement(infoFactura, "fechaEmision").text = move.invoice_date.strftime('%d/%m/%Y') if move.invoice_date else fields.Date.today().strftime('%d/%m/%Y')
        etree.SubElement(infoFactura, "dirEstablecimiento").text = company.street or "Dir Establecimiento Prueba"
        if company.sri_obligado_contabilidad:
            etree.SubElement(infoFactura, "obligadoContabilidad").text = company.sri_obligado_contabilidad
        etree.SubElement(infoFactura, "tipoIdentificacionComprador").text = "05" # Cedula (04 RUC, 05 Ced, 07 Consumidor Final)
        etree.SubElement(infoFactura, "razonSocialComprador").text = move.partner_id.name or "Consumidor Final"
        etree.SubElement(infoFactura, "identificacionComprador").text = move.partner_id.vat or "9999999999999"
        etree.SubElement(infoFactura, "totalSinImpuestos").text = f"{move.amount_untaxed:.2f}"
        etree.SubElement(infoFactura, "totalDescuento").text = "0.00"
        
        # Total con Impuestos
        totalConImpuestos = etree.SubElement(infoFactura, "totalConImpuestos")
        totalImpuesto = etree.SubElement(totalConImpuestos, "totalImpuesto")
        etree.SubElement(totalImpuesto, "codigo").text = "2" # IVA
        etree.SubElement(totalImpuesto, "codigoPorcentaje").text = "4" # 15% (depende de la tabla SRI)
        etree.SubElement(totalImpuesto, "baseImponible").text = f"{move.amount_untaxed:.2f}"
        etree.SubElement(totalImpuesto, "valor").text = f"{move.amount_tax:.2f}"
        
        etree.SubElement(infoFactura, "propina").text = "0.00"
        etree.SubElement(infoFactura, "importeTotal").text = f"{move.amount_total:.2f}"
        etree.SubElement(infoFactura, "moneda").text = "DOLAR"
        
        # --- Detalles ---
        detalles = etree.SubElement(factura, "detalles")
        for line in move.invoice_line_ids:
            if not line.display_type:
                detalle = etree.SubElement(detalles, "detalle")
                etree.SubElement(detalle, "codigoPrincipal").text = "001"
                etree.SubElement(detalle, "descripcion").text = line.name or "Servicio/Producto"
                etree.SubElement(detalle, "cantidad").text = f"{line.quantity:.2f}"
                etree.SubElement(detalle, "precioUnitario").text = f"{line.price_unit:.2f}"
                etree.SubElement(detalle, "descuento").text = f"{line.discount or 0.00:.2f}"
                etree.SubElement(detalle, "precioTotalSinImpuesto").text = f"{line.price_subtotal:.2f}"
                
                # Impuestos del detalle
                impuestos = etree.SubElement(detalle, "impuestos")
                impuesto = etree.SubElement(impuestos, "impuesto")
                etree.SubElement(impuesto, "codigo").text = "2"
                etree.SubElement(impuesto, "codigoPorcentaje").text = "4"
                etree.SubElement(impuesto, "tarifa").text = "15.00"
                etree.SubElement(impuesto, "baseImponible").text = f"{line.price_subtotal:.2f}"
                etree.SubElement(impuesto, "valor").text = f"{line.price_total - line.price_subtotal:.2f}"
        
        return etree.tostring(factura, encoding="UTF-8", xml_declaration=True)

    @staticmethod
    def firmar_xml(xml_bytes, p12_b64, password):
        """Intenta firmar el XML con el certificado P12 usando signxml."""
        try:
            # Decodificar el p12
            p12_data = base64.b64decode(p12_b64)
            private_key, certificate, additional_certificates = pkcs12.load_key_and_certificates(
                p12_data,
                password.encode() if password else None
            )
            
            # Parsear XML
            root = etree.fromstring(xml_bytes)
            
            # Firmar usando XMLSigner (Nota: esto genera XML-DSig estandar, el SRI pide XAdES-BES. 
            # Esto es un primer acercamiento para probar la conexión).
            signer = XMLSigner(c14n_algorithm="http://www.w3.org/TR/2001/REC-xml-c14n-20010315")
            signed_root = signer.sign(root, key=private_key, cert=certificate)
            
            return etree.tostring(signed_root, encoding="UTF-8", xml_declaration=True)
            
        except Exception as e:
            _logger.error(f"Error al firmar XML: {str(e)}")
            raise e
