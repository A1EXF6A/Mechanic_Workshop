import os
import sys

sys.path.append(os.path.abspath('addons/taller_mecanico/models/xades_bes_sri_ec'))

from xades import firmar_comprobante
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives.serialization import pkcs12
import base64
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
</factura>
'''

with open('test.p12', 'rb') as f:
    p12_data = f.read()

private_key, cert, _ = pkcs12.load_key_and_certificates(p12_data, b'123456')

signed_xml_str = firmar_comprobante(p12_data, '123456', xml_dummy)
root = etree.fromstring(signed_xml_str.encode('utf-8'))
namespaces = {"ds": "http://www.w3.org/2000/09/xmldsig#", "etsi": "http://uri.etsi.org/01903/v1.3.2#"}

# Verify the SignatureValue against SignedInfo
signed_info_node = root.xpath('//ds:SignedInfo', namespaces=namespaces)[0]
# C14N of SignedInfo
canonical_signed_info = etree.tostring(signed_info_node, method="c14n", exclusive=False, with_comments=False)

signature_b64 = root.xpath('//ds:SignatureValue', namespaces=namespaces)[0].text.replace('\n', '')
signature_bytes = base64.b64decode(signature_b64)

try:
    cert.public_key().verify(
        signature_bytes,
        canonical_signed_info,
        padding.PKCS1v15(),
        hashes.SHA1()
    )
    print("RSA Signature is CRYPTOGRAPHICALLY VALID!")
except Exception as e:
    print("RSA Signature VERIFICATION FAILED:", str(e))
    
    # Print canonical_signed_info from generated XML
    print("--- Canonical SignedInfo extracted from XML ---")
    print(canonical_signed_info.decode('utf-8'))
