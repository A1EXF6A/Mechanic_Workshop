import base64
import requests
from lxml import etree
import logging
from odoo import fields
from .xades_bes_sri_ec.xades import firmar_comprobante

_logger = logging.getLogger(__name__)

class SriUtils:
    
    @staticmethod
    def generar_xml_factura(move, company):
        """Genera el XML básico de una factura para el SRI."""
        # Namespace
        factura = etree.Element("factura", id="comprobante", version="2.1.0")
        
        # --- Info Tributaria ---
        infoTributaria = etree.SubElement(factura, "infoTributaria")
        etree.SubElement(infoTributaria, "ambiente").text = company.sri_entorno or "1"
        etree.SubElement(infoTributaria, "tipoEmision").text = "1"
        etree.SubElement(infoTributaria, "razonSocial").text = company.name or "Razón Social Pruebas"
        etree.SubElement(infoTributaria, "nombreComercial").text = company.name or "Nombre Comercial Pruebas"
        etree.SubElement(infoTributaria, "ruc").text = company.vat or "0999999999001"
        etree.SubElement(infoTributaria, "claveAcceso").text = move.sri_clave_acceso or ""
        etree.SubElement(infoTributaria, "codDoc").text = "01"
        etree.SubElement(infoTributaria, "estab").text = "001"
        etree.SubElement(infoTributaria, "ptoEmi").text = "001"
        
        # Secuencial (9 digitos)
        nombre = move.name or ""
        partes = nombre.replace('/', '-').split('-')
        secuencial = partes[-1] if partes else "000000001"
        secuencial = ''.join(filter(str.isdigit, secuencial)).zfill(9)
        etree.SubElement(infoTributaria, "secuencial").text = secuencial
        etree.SubElement(infoTributaria, "dirMatriz").text = company.street or "Dir Matriz Prueba"
        
        # --- Info Factura ---
        infoFactura = etree.SubElement(factura, "infoFactura")
        etree.SubElement(infoFactura, "fechaEmision").text = move.invoice_date.strftime('%d/%m/%Y') if move.invoice_date else fields.Date.today().strftime('%d/%m/%Y')
        etree.SubElement(infoFactura, "dirEstablecimiento").text = company.street or "Dir Establecimiento Prueba"
        if company.sri_obligado_contabilidad:
            etree.SubElement(infoFactura, "obligadoContabilidad").text = company.sri_obligado_contabilidad
        identificacion = move.partner_id.vat or "9999999999999"
        if identificacion == "9999999999999":
            tipo_ident = "07" # Consumidor Final
        elif len(identificacion) == 13:
            tipo_ident = "04" # RUC
        elif len(identificacion) == 10:
            tipo_ident = "05" # Cédula
        else:
            tipo_ident = "06" # Pasaporte / Otros
            
        etree.SubElement(infoFactura, "tipoIdentificacionComprador").text = tipo_ident
        etree.SubElement(infoFactura, "razonSocialComprador").text = move.partner_id.name or "Consumidor Final"
        etree.SubElement(infoFactura, "identificacionComprador").text = identificacion
        etree.SubElement(infoFactura, "totalSinImpuestos").text = f"{move.amount_untaxed:.2f}"
        etree.SubElement(infoFactura, "totalDescuento").text = "0.00"
        
        # Acumuladores para agrupar los impuestos
        base_imponible_0 = 0.0
        base_imponible_15 = 0.0
        valor_iva_15 = 0.0
        
        # --- Detalles y cálculo de impuestos ---
        detalles_xml = []
        for line in move.invoice_line_ids:
            if line.display_type not in ('line_section', 'line_note') and line.price_subtotal > 0:
                # Determinar si la línea tiene IVA basándonos en si el total es mayor al subtotal
                tiene_iva = line.price_total > line.price_subtotal
                
                if tiene_iva:
                    base_imponible_15 += line.price_subtotal
                    valor_iva_15 += (line.price_total - line.price_subtotal)
                    codigo_porcentaje = "4" # 15% IVA
                    tarifa = "15.00"
                else:
                    base_imponible_0 += line.price_subtotal
                    codigo_porcentaje = "0" # 0% IVA
                    tarifa = "0.00"
                    
                detalle_xml = {
                    'codigoPrincipal': "001",
                    'descripcion': (line.name or "Servicio/Producto").replace('\n', ' ').replace('\r', '').strip(),
                    'cantidad': f"{line.quantity:.2f}",
                    'precioUnitario': f"{line.price_unit:.2f}",
                    'descuento': f"{line.discount or 0.00:.2f}",
                    'precioTotalSinImpuesto': f"{line.price_subtotal:.2f}",
                    'impuesto': {
                        'codigo': "2",
                        'codigoPorcentaje': codigo_porcentaje,
                        'tarifa': tarifa,
                        'baseImponible': f"{line.price_subtotal:.2f}",
                        'valor': f"{line.price_total - line.price_subtotal:.2f}"
                    }
                }
                detalles_xml.append(detalle_xml)

        # Total con Impuestos
        totalConImpuestos = etree.SubElement(infoFactura, "totalConImpuestos")
        
        if base_imponible_0 > 0:
            totalImpuesto0 = etree.SubElement(totalConImpuestos, "totalImpuesto")
            etree.SubElement(totalImpuesto0, "codigo").text = "2"
            etree.SubElement(totalImpuesto0, "codigoPorcentaje").text = "0" # 0% IVA
            etree.SubElement(totalImpuesto0, "baseImponible").text = f"{base_imponible_0:.2f}"
            etree.SubElement(totalImpuesto0, "valor").text = "0.00"
            
        if base_imponible_15 > 0:
            totalImpuesto15 = etree.SubElement(totalConImpuestos, "totalImpuesto")
            etree.SubElement(totalImpuesto15, "codigo").text = "2"
            etree.SubElement(totalImpuesto15, "codigoPorcentaje").text = "4" # 15% IVA
            etree.SubElement(totalImpuesto15, "baseImponible").text = f"{base_imponible_15:.2f}"
            etree.SubElement(totalImpuesto15, "valor").text = f"{valor_iva_15:.2f}"
            
        # Si no hay ninguno (factura en cero?), enviamos 0% por defecto
        if base_imponible_0 == 0 and base_imponible_15 == 0:
            totalImpuesto0 = etree.SubElement(totalConImpuestos, "totalImpuesto")
            etree.SubElement(totalImpuesto0, "codigo").text = "2"
            etree.SubElement(totalImpuesto0, "codigoPorcentaje").text = "0"
            etree.SubElement(totalImpuesto0, "baseImponible").text = "0.00"
            etree.SubElement(totalImpuesto0, "valor").text = "0.00"
        
        etree.SubElement(infoFactura, "propina").text = "0.00"
        etree.SubElement(infoFactura, "importeTotal").text = f"{move.amount_total:.2f}"
        etree.SubElement(infoFactura, "moneda").text = "DOLAR"
        
        # --- Escribir Detalles en XML ---
        detalles = etree.SubElement(factura, "detalles")
        for d in detalles_xml:
            detalle = etree.SubElement(detalles, "detalle")
            etree.SubElement(detalle, "codigoPrincipal").text = d['codigoPrincipal']
            etree.SubElement(detalle, "descripcion").text = d['descripcion']
            etree.SubElement(detalle, "cantidad").text = d['cantidad']
            etree.SubElement(detalle, "precioUnitario").text = d['precioUnitario']
            etree.SubElement(detalle, "descuento").text = d['descuento']
            etree.SubElement(detalle, "precioTotalSinImpuesto").text = d['precioTotalSinImpuesto']
            
            impuestos = etree.SubElement(detalle, "impuestos")
            impuesto = etree.SubElement(impuestos, "impuesto")
            etree.SubElement(impuesto, "codigo").text = d['impuesto']['codigo']
            etree.SubElement(impuesto, "codigoPorcentaje").text = d['impuesto']['codigoPorcentaje']
            etree.SubElement(impuesto, "tarifa").text = d['impuesto']['tarifa']
            etree.SubElement(impuesto, "baseImponible").text = d['impuesto']['baseImponible']
            etree.SubElement(impuesto, "valor").text = d['impuesto']['valor']
        
        return etree.tostring(factura, encoding="UTF-8", xml_declaration=True)

    @staticmethod
    def calcular_modulo_11(clave_parcial):
        """Calcula el dígito verificador módulo 11 para la clave de acceso de 48 dígitos."""
        factores = [2, 3, 4, 5, 6, 7]
        suma = 0
        for i, char in enumerate(reversed(clave_parcial)):
            factor = factores[i % len(factores)]
            suma += int(char) * factor
        
        residuo = suma % 11
        digito = 11 - residuo
        if digito == 11:
            return "0"
        elif digito == 10:
            return "1"
        else:
            return str(digito)

    @staticmethod
    def firmar_xml(xml_bytes, p12_b64, password):
        """Firma el XML con el certificado P12 usando XAdES-BES en memoria."""
        try:
            p12_data = base64.b64decode(p12_b64)
            # Llamar a la librería nativa XAdES-BES
            xml_firmado = firmar_comprobante(p12_data, password, xml_bytes)
            # Asegurar que devuelva bytes codificados en utf-8 si devuelve un string
            if isinstance(xml_firmado, str):
                xml_firmado = xml_firmado.encode('utf-8')
            return xml_firmado
        except Exception as e:
            _logger.error(f"Error al firmar XML con XAdES-BES: {str(e)}")
            raise e

    @staticmethod
    def transmitir_sri_recepcion(xml_firmado, ambiente):
        """
        Envía el XML firmado al Web Service de Recepción del SRI.
        Retorna (estado, lista_mensajes)
        """
        # URLs de Recepción
        url = "https://celcer.sri.gob.ec/comprobantes-electronicos-ws/RecepcionComprobantesOffline" if ambiente == "1" else "https://cel.sri.gob.ec/comprobantes-electronicos-ws/RecepcionComprobantesOffline"
        
        xml_b64 = base64.b64encode(xml_firmado).decode('utf-8')
        
        envelope = f"""<?xml version="1.0" encoding="utf-8"?>
<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:ec="http://ec.gob.sri.ws.recepcion">
   <soapenv:Header/>
   <soapenv:Body>
      <ec:validarComprobante>
         <xml>{xml_b64}</xml>
      </ec:validarComprobante>
   </soapenv:Body>
</soapenv:Envelope>"""
        
        headers = {
            'Content-Type': 'text/xml;charset=utf-8',
            'SOAPAction': '',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Accept': '*/*',
            'Connection': 'keep-alive'
        }
        
        try:
            response = requests.post(url, data=envelope.encode('utf-8'), headers=headers, timeout=60, verify=False)
            if response.status_code not in (200, 500):
                return "ERROR_CONEXION", [f"Error de red SRI Recepción (HTTP {response.status_code})"]
            
            # Parsear respuesta
            parser = etree.XMLParser(recover=True, resolve_entities=False)
            root = etree.fromstring(response.content, parser=parser)
            
            # Buscar namespaces dinámicos
            namespaces = {'soap': 'http://schemas.xmlsoap.org/soap/envelope/', 'sri': 'http://ec.gob.sri.ws.recepcion'}
            
            # Extraer el estado
            estado_node = root.xpath('//estado/text()', namespaces=namespaces)
            estado = estado_node[0] if estado_node else "DEVUELTA"
            
            mensajes = []
            if estado not in ("RECEPCIONADO", "RECIBIDA"):
                # 1. Intentar extraer mensajes usando namespace
                mensajes_nodes = root.xpath('//mensaje', namespaces=namespaces)
                for node in mensajes_nodes:
                    identificador = node.xpath('identificador/text()')
                    msg = node.xpath('mensaje/text()')
                    info = node.xpath('informacionAdicional/text()')
                    tipo = node.xpath('tipo/text()')
                    
                    id_txt = identificador[0] if identificador else ""
                    msg_txt = msg[0] if msg else ""
                    info_txt = info[0] if info else ""
                    tipo_txt = tipo[0] if tipo else "ERROR"
                    
                    mensajes.append(f"[{tipo_txt} {id_txt}] {msg_txt} - {info_txt}")
                
                # 2. Fallback: Buscar soap:Fault (servidor caído o XML roto)
                if not mensajes:
                    fault_node = root.xpath('//soap:Fault//faultstring/text()', namespaces={'soap': 'http://schemas.xmlsoap.org/soap/envelope/'})
                    if fault_node:
                        mensajes.append(f"Fallo del Servidor SOAP del SRI (soap:Fault): {fault_node[0]}")
                
                # 3. Fallback: Buscar cualquier etiqueta 'mensaje' sin namespace
                if not mensajes:
                    gen_messages = root.xpath('//*[local-name()="mensaje"]')
                    for node in gen_messages:
                        identificador = node.xpath('*[local-name()="identificador"]/text()')
                        msg = node.xpath('*[local-name()="mensaje"]/text()')
                        info = node.xpath('*[local-name()="informacionAdicional"]/text()')
                        tipo = node.xpath('*[local-name()="tipo"]/text()')
                        
                        id_txt = identificador[0] if identificador else ""
                        msg_txt = msg[0] if msg else ""
                        info_txt = info[0] if info else ""
                        tipo_txt = tipo[0] if tipo else "ERROR"
                        
                        mensajes.append(f"[{tipo_txt} {id_txt}] {msg_txt} - {info_txt}")
                
                # 4. Fallback extremo: Si sigue vacío, devolver los primeros 300 caracteres del XML de respuesta
                if not mensajes:
                    res_str = etree.tostring(root, encoding='utf-8').decode('utf-8')[:300]
                    mensajes.append(f"Respuesta cruda del SRI (sin mensajes estructurados): {res_str}")
                    
            return estado, mensajes
            
        except Exception as e:
            _logger.error(f"Error al transmitir a SRI Recepción: {str(e)}")
            return "ERROR_CONEXION", [f"Excepción de conexión SRI Recepción: {str(e)}"]

    @staticmethod
    def transmitir_sri_autorizacion(clave_acceso, ambiente):
        """
        Envía la clave de acceso al Web Service de Autorización del SRI.
        Retorna (estado, fecha_autorizacion, xml_autorizado, lista_mensajes)
        """
        # URLs de Autorización
        url = "https://celcer.sri.gob.ec/comprobantes-electronicos-ws/AutorizacionComprobantesOffline" if ambiente == "1" else "https://cel.sri.gob.ec/comprobantes-electronicos-ws/AutorizacionComprobantesOffline"
        
        envelope = f"""<?xml version="1.0" encoding="utf-8"?>
<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:ec="http://ec.gob.sri.ws.autorizacion">
   <soapenv:Header/>
   <soapenv:Body>
      <ec:autorizacionComprobante>
         <claveAccesoComprobante>{clave_acceso}</claveAccesoComprobante>
      </ec:autorizacionComprobante>
   </soapenv:Body>
</soapenv:Envelope>"""
        
        headers = {
            'Content-Type': 'text/xml;charset=utf-8',
            'SOAPAction': '',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Accept': '*/*',
            'Connection': 'keep-alive'
        }
        
        try:
            response = requests.post(url, data=envelope.encode('utf-8'), headers=headers, timeout=60, verify=False)
            if response.status_code not in (200, 500):
                return "ERROR_CONEXION", None, None, [f"Error de red SRI Autorización (HTTP {response.status_code})"]
            
            parser = etree.XMLParser(recover=True, resolve_entities=False)
            root = etree.fromstring(response.content, parser=parser)
            
            # Buscar namespaces dinámicos
            namespaces = {'soap': 'http://schemas.xmlsoap.org/soap/envelope/', 'sri': 'http://ec.gob.sri.ws.autorizacion'}
            
            # Extraer la primera autorizacion
            autorizacion_node = root.xpath('//autorizacion', namespaces=namespaces)
            if not autorizacion_node:
                res_str = etree.tostring(root, encoding='utf-8').decode('utf-8')
                return "EN_PROCESAMIENTO", None, None, [f"No se encontró nodo de autorización (El SRI probablemente sigue procesando). Respuesta: {res_str[:300]}"]
            
            node = autorizacion_node[0]
            estado = node.xpath('estado/text()')[0] if node.xpath('estado/text()') else "NO AUTORIZADO"
            
            fecha_aut = None
            xml_aut = None
            mensajes = []
            
            if estado == "AUTORIZADO":
                fecha_node = node.xpath('fechaAutorizacion/text()')
                fecha_aut = fecha_node[0] if fecha_node else None
                
                # Obtener el comprobante que viene escapado en CDATA o texto directo
                comp_node = node.xpath('comprobante/text()')
                if comp_node:
                    # En Odoo y el SRI, el XML autorizado final de verdad es el elemento <autorizacion> que envuelve al comprobante y la firma.
                    # Serializamos el nodo <autorizacion> completo como el XML final para validez legal.
                    xml_aut = etree.tostring(node, encoding='utf-8')
            else:
                mensajes_nodes = node.xpath('.//mensaje')
                for m_node in mensajes_nodes:
                    identificador = m_node.xpath('identificador/text()')
                    msg = m_node.xpath('mensaje/text()')
                    info = m_node.xpath('informacionAdicional/text()')
                    tipo = m_node.xpath('tipo/text()')
                    
                    id_txt = identificador[0] if identificador else ""
                    msg_txt = msg[0] if msg else ""
                    info_txt = info[0] if info else ""
                    tipo_txt = tipo[0] if tipo else "ERROR"
                    
                    mensajes.append(f"[{tipo_txt} {id_txt}] {msg_txt} - {info_txt}")
                    
            return estado, fecha_aut, xml_aut, mensajes
            
        except Exception as e:
            _logger.error(f"Error al transmitir a SRI Autorización: {str(e)}")
            return "ERROR_CONEXION", None, None, [f"Excepción de conexión SRI Autorización: {str(e)}"]
