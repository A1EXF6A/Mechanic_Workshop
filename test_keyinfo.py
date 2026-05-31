from lxml import etree
import hashlib
import base64

XML_NAMESPACES = 'xmlns:ds="http://www.w3.org/2000/09/xmldsig#" xmlns:etsi="http://uri.etsi.org/01903/v1.3.2#"'

key_info = f"""
    <ds:KeyInfo Id="Certificate123">
        <ds:X509Data>
            <ds:X509Certificate>
                ABC
            </ds:X509Certificate>
        </ds:X509Data>
        <ds:KeyValue>
            <ds:RSAKeyValue>
                <ds:Modulus>
                    DEF
                </ds:Modulus>
                <ds:Exponent>123</ds:Exponent>
            </ds:RSAKeyValue>
        </ds:KeyValue>
    </ds:KeyInfo>
    """
    
key_info_for_hash = key_info.replace('<ds:KeyInfo', '<ds:KeyInfo ' + XML_NAMESPACES)

# Raw hash
h1 = base64.b64encode(hashlib.sha1(key_info_for_hash.encode('utf-8')).digest())
print("Raw hash:", h1)

# Canonicalized hash
root = etree.fromstring(key_info_for_hash.encode('utf-8'))
canonical_xml = etree.tostring(root, method="c14n", exclusive=False, with_comments=False)
h2 = base64.b64encode(hashlib.sha1(canonical_xml).digest())
print("Canonicalized hash:", h2)

print(canonical_xml.decode('utf-8'))
