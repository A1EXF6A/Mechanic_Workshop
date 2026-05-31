import os
import sys

# Agregamos la ruta para poder importar xades
sys.path.append(os.path.abspath('addons/taller_mecanico/models/xades_bes_sri_ec'))

from xades import firmar_comprobante
from signxml import XMLVerifier
from lxml import etree

xml_dummy = '''<?xml version="1.0" encoding="UTF-8"?>
<factura id="comprobante" version="2.1.0">
    <infoTributaria>
        <ambiente>1</ambiente>
        <tipoEmision>1</tipoEmision>
        <razonSocial>Test</razonSocial>
        <ruc>0123456789001</ruc>
        <claveAcceso>0123456789012345678901234567890123456789012345678</claveAcceso>
        <codDoc>01</codDoc>
        <estab>001</estab>
        <ptoEmi>001</ptoEmi>
        <secuencial>000000001</secuencial>
        <dirMatriz>Matriz</dirMatriz>
    </infoTributaria>
    <infoFactura>
        <fechaEmision>01/01/2023</fechaEmision>
        <dirEstablecimiento>Dir</dirEstablecimiento>
        <obligadoContabilidad>NO</obligadoContabilidad>
        <tipoIdentificacionComprador>04</tipoIdentificacionComprador>
        <razonSocialComprador>Comprador</razonSocialComprador>
        <identificacionComprador>0123456789</identificacionComprador>
        <totalSinImpuestos>10.00</totalSinImpuestos>
        <totalDescuento>0.00</totalDescuento>
        <totalConImpuestos>
            <totalImpuesto>
                <codigo>2</codigo>
                <codigoPorcentaje>2</codigoPorcentaje>
                <baseImponible>10.00</baseImponible>
                <valor>1.20</valor>
            </totalImpuesto>
        </totalConImpuestos>
        <propina>0.00</propina>
        <importeTotal>11.20</importeTotal>
        <moneda>dolar</moneda>
    </infoFactura>
    <detalles>
        <detalle>
            <codigoPrincipal>001</codigoPrincipal>
            <descripcion>Test</descripcion>
            <cantidad>1</cantidad>
            <precioUnitario>10.00</precioUnitario>
            <descuento>0.00</descuento>
            <precioTotalSinImpuesto>10.00</precioTotalSinImpuesto>
            <impuestos>
                <impuesto>
                    <codigo>2</codigo>
                    <codigoPorcentaje>2</codigoPorcentaje>
                    <tarifa>12</tarifa>
                    <baseImponible>10.00</baseImponible>
                    <valor>1.20</valor>
                </impuesto>
            </impuestos>
        </detalle>
    </detalles>
</factura>
'''

try:
    print("Firmando comprobante...")
    with open('test.p12', 'rb') as f:
        p12_data = f.read()
        
    signed_xml_str = firmar_comprobante(p12_data, '123456', xml_dummy)
    print("¡Firma exitosa!")
    
    with open('factura_firmada_test.xml', 'w') as f:
        f.write(signed_xml_str)
        
    print("Verificando firma con signxml...")
    # Verificar firma
    root = etree.fromstring(signed_xml_str.encode('utf-8'))
    # Load cert to verify
    with open('cert.pem', 'r') as f:
        cert_pem = f.read()
        
    # Validar
    XMLVerifier().verify(root, x509_cert=cert_pem)
    print("¡VERIFICACION XML-DSIG EXITOSA!")
    
except Exception as e:
    print(f"Error: {str(e)}")
    import traceback
    traceback.print_exc()
