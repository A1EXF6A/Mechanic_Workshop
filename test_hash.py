import os
import sys

sys.path.append(os.path.abspath('addons/taller_mecanico/models/xades_bes_sri_ec'))

from xades import firmar_comprobante
from lxml import etree
import hashlib
import base64

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

signed_xml_str = firmar_comprobante(p12_data, '123456', xml_dummy)

# Parse and canonicalize the generated XML using lxml
root = etree.fromstring(signed_xml_str.encode('utf-8'))
namespaces = {"ds": "http://www.w3.org/2000/09/xmldsig#", "etsi": "http://uri.etsi.org/01903/v1.3.2#"}

# Verify Reference 1 (Invoice)
ref_invoice = root.xpath('//ds:Reference[@URI="#comprobante"]/ds:DigestValue', namespaces=namespaces)[0].text
print("Digest from XML (Invoice):", ref_invoice)

# C14N of invoice (without signature)
factura_clone = etree.fromstring(xml_dummy.encode('utf-8'))
canonical_invoice = etree.tostring(factura_clone, method="c14n", exclusive=False, with_comments=False)
calc_digest_invoice = base64.b64encode(hashlib.sha1(canonical_invoice).digest()).decode('utf-8')
print("Calculated Digest (Invoice):", calc_digest_invoice)
print("Invoice Digest MATCH?", ref_invoice == calc_digest_invoice)


# Verify Reference 2 (KeyInfo)
ref_keyinfo = root.xpath('//ds:Reference[starts-with(@URI, "#Certificate")]/ds:DigestValue', namespaces=namespaces)[0].text
keyinfo_node = root.xpath('//ds:KeyInfo', namespaces=namespaces)[0]
canonical_keyinfo = etree.tostring(keyinfo_node, method="c14n", exclusive=False, with_comments=False)
calc_digest_keyinfo = base64.b64encode(hashlib.sha1(canonical_keyinfo).digest()).decode('utf-8')
print("Digest from XML (KeyInfo):", ref_keyinfo)
print("Calculated Digest (KeyInfo):", calc_digest_keyinfo)
print("KeyInfo Digest MATCH?", ref_keyinfo == calc_digest_keyinfo)


# Verify Reference 3 (SignedProperties)
ref_props = root.xpath('//ds:Reference[contains(@URI, "SignedProperties")]/ds:DigestValue', namespaces=namespaces)[0].text
props_node = root.xpath('//etsi:SignedProperties', namespaces=namespaces)[0]
canonical_props = etree.tostring(props_node, method="c14n", exclusive=False, with_comments=False)
calc_digest_props = base64.b64encode(hashlib.sha1(canonical_props).digest()).decode('utf-8')
print("Digest from XML (SignedProperties):", ref_props)
print("Calculated Digest (SignedProperties):", calc_digest_props)
print("SignedProperties Digest MATCH?", ref_props == calc_digest_props)

